"""Export numeric Copilot usage only, without conversation text or request IDs."""

import argparse
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal
import json
from pathlib import Path

NANO_PER_CREDIT = Decimal(1_000_000_000)
USD_PER_CREDIT = Decimal("0.01")


def collect_usage(events):
    records = {}
    windows = {}
    shutdowns = []
    for event in events:
        kind = event["type"]
        data = event.get("data", {})
        if kind in ("subagent.started", "subagent.completed"):
            window = windows.setdefault(data["toolCallId"], {})
            if kind == "subagent.started":
                window["started_at"] = event["timestamp"]
            else:
                window.update({
                    "completed_at": event["timestamp"],
                    "duration_seconds": data["durationMs"] / 1000,
                    "tool_calls": data["totalToolCalls"],
                    "tokens_reported": data["totalTokens"],
                })
        if kind == "session.shutdown":
            nano = data.get("totalNanoAiu")
            if nano is not None:
                shutdowns.append({
                    "timestamp": event["timestamp"],
                    "ai_credits": float(Decimal(str(nano)) / NANO_PER_CREDIT),
                    "usd_equivalent": float(Decimal(str(nano)) / NANO_PER_CREDIT * USD_PER_CREDIT),
                })
        if kind != "session.usage_record":
            continue
        usage = data["usage"]
        accounting = usage.get("accounting", {})
        source = accounting.get("sourceSessionId")
        identity = accounting.get("usageId") or usage.get("apiCallId") or event.get("id")
        if not source or not identity:
            raise ValueError("Usage record lacks a source session or deduplication identity")
        records[(source, identity)] = (event["timestamp"], usage)

    by_source = {}
    for (source, _), (timestamp, usage) in records.items():
        group = by_source.setdefault(source, {
            "source_session_id": source, "api_calls": 0, "models": Counter(),
            "first_usage_at": timestamp, "last_usage_at": timestamp,
            "input_tokens": 0, "output_tokens": 0,
            "cache_read_tokens": 0, "cache_write_tokens": 0,
            "complete_credit_records": 0, "unresolved_credit_records": 0,
            "reported_nano_aiu": 0, "tool_counts": Counter(),
            "rates_usd_per_million_tokens": {},
        })
        group["api_calls"] += 1
        group["models"][usage["model"]] += 1
        group["first_usage_at"] = min(group["first_usage_at"], timestamp)
        group["last_usage_at"] = max(group["last_usage_at"], timestamp)
        for output, field in (
            ("input_tokens", "inputTokens"), ("output_tokens", "outputTokens"),
            ("cache_read_tokens", "cacheReadTokens"), ("cache_write_tokens", "cacheWriteTokens"),
        ):
            group[output] += usage.get(field, 0)
        group["tool_counts"].update(usage.get("toolCounts", {}))
        credits = usage.get("copilotUsage", {})
        nano = credits.get("totalNanoAiu")
        if usage.get("aiCreditsStatus") != "complete" or nano is None:
            group["unresolved_credit_records"] += 1
            continue
        if isinstance(nano, bool) or not isinstance(nano, (int, float)) or nano < 0:
            raise ValueError("Invalid reported AI-credit amount")
        group["complete_credit_records"] += 1
        group["reported_nano_aiu"] += nano
        for detail in credits.get("tokenDetails", []):
            rate = (
                Decimal(str(detail["costPerBatch"])) / NANO_PER_CREDIT
                * USD_PER_CREDIT * Decimal(1_000_000) / Decimal(detail["batchSize"])
            )
            group["rates_usd_per_million_tokens"].setdefault(
                detail["model"], {}
            )[detail["tokenType"]] = float(rate)

    for group in by_source.values():
        complete = group["unresolved_credit_records"] == 0
        group["billing_status"] = "runtime_reported_complete" if complete else "incomplete"
        amount = Decimal(str(group["reported_nano_aiu"])) / NANO_PER_CREDIT
        group["ai_credits"] = float(amount) if complete else None
        group["usd_equivalent"] = float(amount * USD_PER_CREDIT) if complete else None
        matches = [
            window for window in windows.values()
            if window.get("started_at", "z") <= group["first_usage_at"]
            and window.get("completed_at", "") >= group["last_usage_at"]
        ]
        if len(matches) == 1:
            group["subagent_execution"] = matches[0]
        elif len(matches) > 1:
            raise ValueError("Ambiguous overlapping subagent usage windows")
    return {
        "measurement": "Local runtime accounting, not an invoice or account-balance check",
        "conversion": {"nano_aiu_per_ai_credit": int(NANO_PER_CREDIT), "usd_per_ai_credit": 0.01},
        "deduplication": "sourceSessionId + accounting.usageId; no checkpoint totals added",
        "sources": sorted(by_source.values(), key=lambda item: item["first_usage_at"]),
        "prior_session_shutdowns": shutdowns,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--label", action="append", default=[], help="source-session-id=example-label")
    args = parser.parse_args()
    with args.events.open(encoding="utf-8") as stream:
        report = collect_usage(json.loads(line) for line in stream if line.strip())
    labels = dict(label.split("=", 1) for label in args.label)
    for source in report["sources"]:
        if source["source_session_id"] in labels:
            source["label"] = labels[source["source_session_id"]]
    missing = set(labels) - {source["source_session_id"] for source in report["sources"]}
    if missing:
        raise ValueError(f"Requested sources absent: {sorted(missing)}")
    report["captured_at_utc"] = datetime.now(timezone.utc).isoformat()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    for source in report["sources"]:
        if "label" in source:
            print(json.dumps({key: source.get(key) for key in (
                "label", "api_calls", "ai_credits", "usd_equivalent", "billing_status",
                "subagent_execution",
            )}))


if __name__ == "__main__":
    main()
