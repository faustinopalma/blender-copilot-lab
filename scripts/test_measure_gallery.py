import copy
import unittest

from measure_gallery import reconcile


def event():
    return {
        "timestamp": "2026-10-16T14:00:01Z", "type": "session.usage_record",
        "data": {"usage": {
            "accounting": {"sourceSessionId": "child", "usageId": "one", "sequence": 1},
            "inputTokens": 100, "outputTokens": 20, "cacheReadTokens": 60, "cacheWriteTokens": 10,
            "reasoningTokens": 5, "duration": 1000, "aiCreditsStatus": "complete",
            "copilotUsage": {"totalNanoAiu": 29100000, "tokenDetails": [
                {"tokenType": kind, "tokenCount": count, "costPerBatch": rate, "batchSize": 1000000}
                for kind, count, rate in (
                    ("input", 30, 200000000000), ("cache_read", 60, 10000000000),
                    ("cache_write", 10, 250000000000), ("output", 20, 1000000000000),
                )
            ]},
        }},
    }


class ReconcileTests(unittest.TestCase):
    def test_exact_rate_and_partition_reconciliation(self):
        result = reconcile([event()])
        self.assertEqual(result["max_billing_delta_nano_aiu"], 0)
        self.assertEqual(result["model_seconds"], 1)
        self.assertEqual(result["first_input_tokens"], 100)
        self.assertEqual(result["reasoning_tokens"], 5)

    def test_duplicate_not_added_twice(self):
        self.assertEqual(len(reconcile([event(), event()])["calls"]), 1)

    def test_final_update_replaces_pending(self):
        pending = event()
        pending["data"]["usage"]["aiCreditsStatus"] = "pending"
        self.assertEqual(len(reconcile([pending, event()])["calls"]), 1)

    def test_cache_is_part_of_input_not_added_on_top(self):
        wrong = event()
        wrong["data"]["usage"]["inputTokens"] = 170
        with self.assertRaisesRegex(ValueError, "partition mismatch"):
            reconcile([wrong])

    def test_wrong_credit_amount_is_rejected(self):
        wrong = event()
        wrong["data"]["usage"]["copilotUsage"]["totalNanoAiu"] += 100
        with self.assertRaisesRegex(ValueError, "recomputation differs"):
            reconcile([wrong])

    def test_incomplete_not_silently_zero(self):
        wrong = event()
        wrong["data"]["usage"]["copilotUsage"]["tokenDetails"] = []
        with self.assertRaisesRegex(ValueError, "Incomplete"):
            reconcile([wrong])

    def test_order_uses_sequence_not_delivery_order(self):
        second = copy.deepcopy(event())
        usage = second["data"]["usage"]
        usage["accounting"].update(usageId="two", sequence=2)
        usage["inputTokens"] += 10
        usage["copilotUsage"]["tokenDetails"][0]["tokenCount"] += 10
        usage["copilotUsage"]["totalNanoAiu"] += 2000000
        result = reconcile([second, event()])
        self.assertEqual(result["first_input_tokens"], 100)
        self.assertEqual(result["last_input_tokens"], 110)

    def test_unknown_billing_category_rejected(self):
        wrong = event()
        wrong["data"]["usage"]["copilotUsage"]["tokenDetails"][0]["tokenType"] = "other"
        with self.assertRaisesRegex(ValueError, "Unrecognized"):
            reconcile([wrong])


if __name__ == "__main__":
    unittest.main()
