import unittest

from measure_usage import collect_usage


def usage_event(source="child", identity="one", nano=1_500_000_000, status="complete"):
    return {
        "type": "session.usage_record", "id": identity,
        "timestamp": "2026-10-16T14:00:01Z",
        "data": {"usage": {
            "model": "test-model", "cost": 999,
            "inputTokens": 100, "outputTokens": 20,
            "accounting": {"sourceSessionId": source, "usageId": identity},
            "copilotUsage": {"totalNanoAiu": nano},
            "aiCreditsStatus": status,
        }},
    }


class UsageTests(unittest.TestCase):
    def test_credit_conversion_not_legacy_cost(self):
        source = collect_usage([usage_event()])["sources"][0]
        self.assertEqual(source["ai_credits"], 1.5)
        self.assertEqual(source["usd_equivalent"], 0.015)

    def test_duplicate_records_not_double_counted(self):
        source = collect_usage([usage_event(), usage_event()])["sources"][0]
        self.assertEqual(source["api_calls"], 1)

    def test_parent_and_child_separated(self):
        report = collect_usage([usage_event(), usage_event(source="parent")])
        self.assertEqual(len(report["sources"]), 2)

    def test_missing_credit_amount_is_not_zero(self):
        source = collect_usage([usage_event(nano=None)])["sources"][0]
        self.assertIsNone(source["ai_credits"])
        self.assertEqual(source["unresolved_credit_records"], 1)

    def test_pending_measurement_is_not_complete(self):
        source = collect_usage([usage_event(status="pending")])["sources"][0]
        self.assertIsNone(source["usd_equivalent"])

    def test_completed_update_replaces_pending(self):
        source = collect_usage([usage_event(status="pending"), usage_event()])["sources"][0]
        self.assertEqual(source["ai_credits"], 1.5)
        self.assertEqual(source["api_calls"], 1)

    def test_invalid_credit_amount_is_explicit_error(self):
        with self.assertRaises(ValueError):
            collect_usage([usage_event(nano=-1)])

    def test_missing_accounting_source_is_error(self):
        event = usage_event()
        del event["data"]["usage"]["accounting"]["sourceSessionId"]
        with self.assertRaises(ValueError):
            collect_usage([event])

    def test_checkpoint_total_not_added_again(self):
        report = collect_usage([
            usage_event(),
            {"type": "session.usage_checkpoint", "data": {"totalNanoAiu": 1_500_000_000}},
        ])
        self.assertEqual(report["sources"][0]["ai_credits"], 1.5)

    def test_association_with_completed_subagent_window(self):
        report = collect_usage([
            {"type": "subagent.started", "timestamp": "2026-10-16T14:00:00Z",
             "data": {"toolCallId": "call"}},
            usage_event(),
            {"type": "subagent.completed", "timestamp": "2026-10-16T14:00:02Z",
             "data": {"toolCallId": "call", "durationMs": 2000,
                      "totalToolCalls": 1, "totalTokens": 120}},
        ])
        self.assertEqual(report["sources"][0]["subagent_execution"]["duration_seconds"], 2)


if __name__ == "__main__":
    unittest.main()
