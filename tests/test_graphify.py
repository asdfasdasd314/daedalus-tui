import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from tui.graphify import update_repository


class GraphifyTests(unittest.TestCase):
    @patch("tui.graphify.shutil.which", return_value=None)
    def test_missing_graphify_is_non_blocking(self, _which):
        result = update_repository(Path("/repo"))
        self.assertFalse(result.attempted)
        self.assertFalse(result.succeeded)

    @patch("tui.graphify.shutil.which", return_value="/usr/local/bin/graphify")
    @patch("tui.graphify.subprocess.run")
    def test_runs_update_from_primary_repository(self, run, _which):
        run.return_value = Mock(returncode=0, stdout="updated\n", stderr="")
        result = update_repository(Path("/repo"))
        self.assertTrue(result.attempted)
        self.assertTrue(result.succeeded)
        self.assertEqual(run.call_args.args[0], ["graphify", "update", "."])
        self.assertEqual(run.call_args.kwargs["cwd"], Path("/repo"))

    @patch("tui.graphify.shutil.which", return_value="/usr/local/bin/graphify")
    @patch("tui.graphify.subprocess.run")
    def test_failed_update_returns_diagnostics_without_raising(self, run, _which):
        run.return_value = Mock(returncode=1, stdout="partial output", stderr="Operation not permitted")
        result = update_repository(Path("/repo"))
        self.assertTrue(result.attempted)
        self.assertFalse(result.succeeded)
        self.assertIn("Operation not permitted", result.output)


if __name__ == "__main__":
    unittest.main()
