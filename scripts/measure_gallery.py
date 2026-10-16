"""Export reconciled numeric gallery accounting, never raw prompts or request IDs."""

import argparse
from collections import defaultdict
from datetime import datetime, timezone
from decimal import Decimal
import json
from pathlib import Path
import statistics

from measure_usage import collect_usage

ROOT = Path(__file__).resolve().parents[1]


def reconcile(records):
    unique = {}
    for event in records:
        usage = event["data"]["usage"]
        account = usage["accounting"]
        unique[(account["sourceSessionId"], account["usageId"])] = event
    ordered = sorted(unique.values(), key=lambda e: e["data"]["usage"]["accounting"]["sequence"])
    if not ordered:
        raise ValueError("No metered model calls")
    calls = []
    for event in ordered:
        usage = event["data"]["usage"]
        credit = usage.get("copilotUsage", {})
        details = credit.get("tokenDetails", [])
        if usage.get("aiCreditsStatus") != "complete" or not details or credit.get("totalNanoAiu") is None:
            raise ValueError("Incomplete token or credit measurement")
        buckets = defaultdict(int)
        calculated = Decimal(0)
        for detail in details:
            if detail["batchSize"] <= 0 or detail["tokenCount"] < 0 or detail["costPerBatch"] < 0:
                raise ValueError("Invalid billing rate or token count")
            buckets[detail["tokenType"]] += detail["tokenCount"]
            calculated += Decimal(str(detail["costPerBatch"])) * detail["tokenCount"] / detail["batchSize"]
        unknown = set(buckets) - {"input", "cache_read", "cache_write", "output"}
        if unknown:
            raise ValueError(f"Unrecognized billing token categories: {sorted(unknown)}")
        expected = {
            "inputTokens": buckets["input"] + buckets["cache_read"] + buckets["cache_write"],
            "outputTokens": buckets["output"],
            "cacheReadTokens": buckets["cache_read"],
            "cacheWriteTokens": buckets["cache_write"],
        }
        for name, count in expected.items():
            if usage.get(name) != count:
                raise ValueError(f"Token partition mismatch for {name}: {usage.get(name)} != {count}")
        error = abs(calculated - Decimal(str(credit["totalNanoAiu"])))
        if error > len(details):
            raise ValueError(f"Billing recomputation differs by {error} nano-AIU")
        calls.append({
            "input_tokens": usage["inputTokens"], "output_tokens": usage["outputTokens"],
            "cache_read_tokens": usage["cacheReadTokens"], "cache_write_tokens": usage["cacheWriteTokens"],
            "reasoning_tokens": usage.get("reasoningTokens", 0),
            "model_seconds": usage["duration"] / 1000,
            "reported_nano_aiu": credit["totalNanoAiu"],
            "recomputed_nano_aiu": float(calculated), "billing_delta_nano_aiu": float(error),
        })
    inputs = [call["input_tokens"] for call in calls]
    return {
        "first_input_tokens": inputs[0], "last_input_tokens": inputs[-1],
        "min_input_tokens": min(inputs), "max_input_tokens": max(inputs),
        "model_seconds": sum(call["model_seconds"] for call in calls),
        "reasoning_tokens": sum(call["reasoning_tokens"] for call in calls),
        "max_billing_delta_nano_aiu": max(call["billing_delta_nano_aiu"] for call in calls),
        "calls": calls,
    }


def gallery_usage(events, subjects, root=ROOT):
    collected = collect_usage(events)
    windows, names = {}, {}
    records = defaultdict(list)
    for event in events:
        data = event.get("data", {})
        if event["type"] == "tool.execution_start" and data.get("toolName") == "task":
            arguments = data.get("arguments", {})
            if isinstance(arguments, str):
                arguments = json.loads(arguments)
            name = arguments.get("name", "")
            if name.startswith("gallery-"):
                names[data["toolCallId"]] = name.removeprefix("gallery-")
        elif event["type"] in ("subagent.started", "subagent.completed"):
            window = windows.setdefault(data["toolCallId"], {})
            if event["type"] == "subagent.started":
                window["start"] = event["timestamp"]
            else:
                window["end"] = event["timestamp"]
        elif event["type"] == "session.usage_record":
            records[data["usage"]["accounting"]["sourceSessionId"]].append(event)
    rows = []
    used = set()
    previous_end = ""
    for subject in subjects:
        slug = subject["slug"]
        matches = [windows[identity] for identity, name in names.items() if name == slug]
        if len(matches) != 1 or "end" not in matches[0]:
            raise ValueError(f"{slug}: expected one completed fresh subagent")
        window = matches[0]
        if window["start"] < previous_end:
            raise ValueError("Gallery subagent windows overlap")
        previous_end = window["end"]
        sources = [
            source for source in collected["sources"]
            if source["first_usage_at"] >= window["start"] and source["last_usage_at"] <= window["end"]
        ]
        if len(sources) != 1:
            raise ValueError(f"{slug}: ambiguous source association ({len(sources)})")
        source = sources[0]
        identity = source["source_session_id"]
        if identity in used:
            raise ValueError("Gallery subjects reused a child session")
        used.add(identity)
        execution = source["subagent_execution"]
        if source["input_tokens"] + source["output_tokens"] != execution["tokens_reported"]:
            raise ValueError(f"{slug}: child completion token total does not reconcile")
        numeric = reconcile(records[identity])
        manifest = json.loads((root / "results" / "gallery" / f"{slug}.json").read_text())
        attempts = manifest["attempts"]
        if attempts[-1]["status"] != "success":
            raise ValueError(f"{slug}: final runner attempt failed")
        phases = defaultdict(float)
        for attempt in attempts:
            for phase, seconds in attempt["phases_seconds"].items():
                phases[phase] += seconds
        row = {
            "slug": slug, "title": subject["title"], "models": dict(source["models"]),
            **{key: source[key] for key in (
                "api_calls", "input_tokens", "output_tokens", "cache_read_tokens", "cache_write_tokens",
                "ai_credits", "usd_equivalent", "billing_status", "rates_usd_per_million_tokens",
            )},
            **numeric, "subagent_seconds": execution["duration_seconds"],
            "subagent_tool_calls": execution["tool_calls"],
            "started_at_utc": window["start"], "ended_at_utc": window["end"],
            "attempts": len(attempts),
            "failed_attempts": sum(attempt["status"] != "success" for attempt in attempts),
            "objects": attempts[-1]["scene"]["objects"],
            "runner_all_attempts_seconds": sum(attempt["total_seconds"] for attempt in attempts),
            "runner_final_seconds": attempts[-1]["total_seconds"],
            "all_attempts_phases_seconds": dict(phases),
            "final_phases_seconds": attempts[-1]["phases_seconds"],
            "cache_read_fraction_of_input": source["cache_read_tokens"] / source["input_tokens"],
            "helper_sha256": attempts[-1]["common_sha256"],
        }
        if row["runner_all_attempts_seconds"] > row["subagent_seconds"] + 1:
            raise ValueError(f"{slug}: runner time exceeds full agent time")
        rows.append(row)
    first = [row["first_input_tokens"] for row in rows]
    totals = {
        key: sum(row[key] for row in rows)
        for key in ("api_calls", "input_tokens", "output_tokens", "cache_read_tokens", "cache_write_tokens",
                    "reasoning_tokens", "ai_credits", "usd_equivalent", "subagent_seconds",
                    "runner_all_attempts_seconds", "model_seconds", "attempts", "failed_attempts", "objects")
    }
    totals["elapsed_creation_window_seconds"] = (
        datetime.fromisoformat(rows[-1]["ended_at_utc"].replace("Z", "+00:00"))
        - datetime.fromisoformat(rows[0]["started_at_utc"].replace("Z", "+00:00"))
    ).total_seconds()
    coordinator = [
        event for event in events
        if event["type"] == "session.usage_record"
        and event["timestamp"] >= rows[0]["started_at_utc"]
        and event["data"]["usage"]["accounting"]["sourceSessionId"] not in used
    ]
    coordinator_sources = collect_usage(coordinator)["sources"] if coordinator else []
    coordinator_snapshot = {
        "scope": "Non-child accounting since the first gallery agent started; snapshot only, excludes later work and earlier setup.",
        "api_calls": sum(source["api_calls"] for source in coordinator_sources),
        "input_tokens": sum(source["input_tokens"] for source in coordinator_sources),
        "output_tokens": sum(source["output_tokens"] for source in coordinator_sources),
        "ai_credits": (
            sum(source["ai_credits"] for source in coordinator_sources)
            if all(source["ai_credits"] is not None for source in coordinator_sources) else None
        ),
    }
    return {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "Ten fresh sequential child agents only. Parent coordination, web viewer, exports and validation excluded.",
        "conversion": collected["conversion"],
        "deduplication": collected["deduplication"],
        "checks": {
            "ten_unique_child_contexts": len(used) == 10, "no_overlapping_child_windows": True,
            "token_partitions_and_child_totals_reconciled": True,
            "billing_recomputed_from_runtime_token_rates": True,
            "one_shared_helper_hash": len({row["helper_sha256"] for row in rows}) == 1,
        },
        "initial_context": {
            "min_tokens": min(first), "max_tokens": max(first),
            "spread_tokens": max(first) - min(first),
            "spread_fraction_of_median": (max(first) - min(first)) / statistics.median(first),
            "successive_deltas": [b - a for a, b in zip(first, first[1:])],
        },
        "totals": totals, "coordinator_snapshot": coordinator_snapshot, "subjects": rows,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", required=True, type=Path)
    args = parser.parse_args()
    with args.events.open(encoding="utf-8") as stream:
        events = [json.loads(line) for line in stream if line.strip()]
    report = gallery_usage(events, json.loads((ROOT / "scenes" / "subjects.json").read_text()))
    (ROOT / "results" / "gallery" / "usage.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"checks": report["checks"], "totals": report["totals"], "initial_context": report["initial_context"]}))


if __name__ == "__main__":
    main()
