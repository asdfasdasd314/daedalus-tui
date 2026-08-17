import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from tui.memory import TaskMemoryStore
from tui.token_usage import TokenUsageEntry, calculate_token_usage, usage_entries_from_memory


class TokenUsageTests(unittest.TestCase):
    def test_calculates_windows_projection_and_provider_split(self):
        now = datetime(2026, 8, 17, 12, 0, tzinfo=timezone.utc)
        entries = (
            TokenUsageEntry("one", datetime(2026, 8, 17, 11, 30, tzinfo=timezone.utc), "codex", 100),
            TokenUsageEntry("two", datetime(2026, 8, 16, 12, 0, tzinfo=timezone.utc), "cursor", 300),
        )

        stats = calculate_token_usage(entries, now=now)

        self.assertEqual(stats.cumulative_tokens, 400)
        self.assertEqual(stats.daily_tokens, 100)
        self.assertEqual(stats.last_hour_tokens, 100)
        self.assertEqual(stats.average_tokens_per_prompt, 200)
        self.assertEqual(stats.seven_day_expected_tokens, 1400)
        self.assertEqual(stats.provider_tokens, (("cursor", 300), ("codex", 100)))
        self.assertEqual(dict(stats.provider_percentages), {"cursor": 75.0, "codex": 25.0})

    def test_reads_task_usage_from_persisted_memory(self):
        with tempfile.TemporaryDirectory() as directory:
            store = TaskMemoryStore(Path(directory) / ".daedalus-memory.json")
            store.record_task(
                "task-one",
                "Implement statistics",
                "codex",
                "luna",
                "high",
                "coding",
                "completed",
                submitted_at=0,
                tokens=165,
            )

            entries = usage_entries_from_memory(store)

            self.assertEqual(len(entries), 1)
            self.assertEqual(entries[0].task_id, "task-one")
            self.assertEqual(entries[0].provider, "codex")
            self.assertEqual(entries[0].tokens, 165)

    def test_rejects_invalid_window_settings(self):
        with self.assertRaises(ValueError):
            calculate_token_usage((), recent_window_hours=0)
        with self.assertRaises(ValueError):
            calculate_token_usage((), forecast_days=0)


if __name__ == "__main__":
    unittest.main()
