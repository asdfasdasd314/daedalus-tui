import json
import tempfile
import unittest
from pathlib import Path

from tui.memory import TokenUsageStore


class TokenUsageStoreTests(unittest.TestCase):
    def test_records_usage_metadata_with_nullable_provider_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / ".daedalus-memory.json"
            store = TokenUsageStore(path)

            store.record(0, 165, "codex", "gpt-5.6-luna", "high")
            store.record(1, 321, "cursor")

            self.assertEqual(
                json.loads(path.read_text(encoding="utf-8")),
                [
                    {
                        "timestamp": "1970-01-01T00:00:00Z",
                        "tokens": 165,
                        "provider": "codex",
                        "model": "gpt-5.6-luna",
                        "reasoning": "high",
                    },
                    {
                        "timestamp": "1970-01-01T00:00:01Z",
                        "tokens": 321,
                        "provider": "cursor",
                        "model": None,
                        "reasoning": None,
                    },
                ],
            )

    def test_normalizes_legacy_usage_entries_when_appending(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / ".daedalus-memory.json"
            path.write_text(
                json.dumps([{"timestamp": "1970-01-01T00:00:00Z", "tokens": 165}]),
                encoding="utf-8",
            )

            TokenUsageStore(path).record(1, 321, "codex", "gpt-5.6-terra", "medium")

            self.assertEqual(
                json.loads(path.read_text(encoding="utf-8")),
                [
                    {
                        "timestamp": "1970-01-01T00:00:00Z",
                        "tokens": 165,
                        "provider": None,
                        "model": None,
                        "reasoning": None,
                    },
                    {
                        "timestamp": "1970-01-01T00:00:01Z",
                        "tokens": 321,
                        "provider": "codex",
                        "model": "gpt-5.6-terra",
                        "reasoning": "medium",
                    },
                ],
            )

    def test_does_not_replace_a_corrupt_memory_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / ".daedalus-memory.json"
            path.write_text("not json", encoding="utf-8")

            with self.assertRaises(ValueError):
                TokenUsageStore(path).record(0, 1)

            self.assertEqual(path.read_text(encoding="utf-8"), "not json")

    def test_tracks_last_opened_project_without_replacing_token_usage(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / ".daedalus-memory.json"
            store = TokenUsageStore(path)
            first_project = Path(directory) / "first"
            second_project = Path(directory) / "second"

            store.record(0, 165)
            store.record_last_opened_project(first_project)
            store.record_last_opened_project(second_project)

            self.assertEqual(store.get_last_opened_project(), second_project.resolve())
            self.assertEqual(
                json.loads(path.read_text(encoding="utf-8")),
                [
                    {
                        "timestamp": "1970-01-01T00:00:00Z",
                        "tokens": 165,
                        "provider": None,
                        "model": None,
                        "reasoning": None,
                    },
                    {"last_opened_project": str(second_project.resolve())},
                ],
            )


if __name__ == "__main__":
    unittest.main()
