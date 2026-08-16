import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tui.verification import discover_commands, run_verification


class VerificationTests(unittest.TestCase):
    def test_discovers_root_and_nested_test_suites(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "tests").mkdir()
            (root / "package.json").write_text('{"scripts":{"test":"pytest"}}', encoding="utf-8")
            child = root / "child"
            child.mkdir()
            (child / "tests").mkdir()
            self.assertEqual(
                discover_commands(root, []),
                [["npm", "test"], ["python", "-m", "pytest"], ["python", "-m", "pytest", "child/tests"]],
            )

    @patch("tui.verification.subprocess.run")
    def test_stops_at_first_failed_command(self, run):
        success = unittest.mock.Mock(returncode=0, stdout="ok", stderr="")
        failure = unittest.mock.Mock(returncode=1, stdout="", stderr="failed")
        run.side_effect = [success, failure]

        result = run_verification(Path("/worktree"), [["first"], ["second"], ["third"]])

        self.assertFalse(result.succeeded)
        self.assertEqual(run.call_count, 2)
        self.assertIn("failed", result.output)


if __name__ == "__main__":
    unittest.main()
