import tempfile
import unittest
from pathlib import Path

from tui.topics import (
    TOPIC_NONE_VALUE,
    TOPIC_START,
    embed_topic,
    list_topic_slugs,
    load_topic_text,
    topic_select_options,
    validate_topic_markdown,
)


SAMPLE_TOPIC = """# Kalman BTC Trading Strategy

## Topic Goal
Build a Kalman-filter BTC strategy MVP.

## Topic Status
open

## State Log
- 2026-08-24: Scaffolded research notes.
"""


class TopicsTests(unittest.TestCase):
    def test_list_and_load_topics_from_project_checkout(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            topics = root / "topic_files"
            topics.mkdir()
            (topics / "kalman-btc.md").write_text(SAMPLE_TOPIC, encoding="utf-8")
            (topics / "mvp.md").write_text(SAMPLE_TOPIC.replace("Kalman", "MVP"), encoding="utf-8")
            (topics / "notes.txt").write_text("ignored", encoding="utf-8")

            self.assertEqual(list_topic_slugs(root), ["kalman-btc", "mvp"])
            self.assertEqual(load_topic_text(root, "kalman-btc"), SAMPLE_TOPIC)
            self.assertIsNone(load_topic_text(root, "missing"))
            self.assertIsNone(load_topic_text(root, TOPIC_NONE_VALUE))
            self.assertEqual(
                topic_select_options(root),
                [("(None)", TOPIC_NONE_VALUE), ("kalman-btc", "kalman-btc"), ("mvp", "mvp")],
            )

    def test_missing_or_empty_topic_dir_yields_only_none_option(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual(list_topic_slugs(root), [])
            self.assertEqual(topic_select_options(root), [("(None)", TOPIC_NONE_VALUE)])
            (root / "topic_files").mkdir()
            self.assertEqual(topic_select_options(root), [("(None)", TOPIC_NONE_VALUE)])

    def test_validate_topic_markdown_reports_missing_headings(self):
        self.assertEqual(validate_topic_markdown(SAMPLE_TOPIC), [])
        self.assertEqual(
            validate_topic_markdown("# Incomplete\n\n## Topic Goal\nwhy\n"),
            ["Topic Status", "State Log"],
        )

    def test_embed_topic_includes_instructions_and_omits_when_unused(self):
        coding = embed_topic(SAMPLE_TOPIC, "coding")
        ask = embed_topic(SAMPLE_TOPIC, "ask")

        self.assertIn(TOPIC_START, coding)
        self.assertIn("Kalman-filter BTC strategy MVP", coding)
        self.assertIn("State Log", coding)
        self.assertIn("immutable", coding)
        self.assertIn("append one State Log entry", coding)
        self.assertIn("read-only for topic files", ask)
        self.assertNotIn("append one State Log entry", ask)


if __name__ == "__main__":
    unittest.main()
