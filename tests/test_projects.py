import tempfile
import unittest
from pathlib import Path

from tui.projects import discover_projects


class ProjectDiscoveryTests(unittest.TestCase):
    def test_finds_root_and_nested_feature_file_projects(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "feature_files").mkdir()
            (root / "apps" / "flockdock" / "feature_files").mkdir(parents=True)
            (root / "apps" / "other" / "feature_files").mkdir(parents=True)
            (root / ".daedalus-worktrees" / "ignored" / "feature_files").mkdir(parents=True)
            (root / "node_modules" / "dependency" / "feature_files").mkdir(parents=True)

            projects = discover_projects(root)

            self.assertEqual(
                [project.path for project in projects],
                [
                    root.resolve(),
                    (root / "apps" / "flockdock").resolve(),
                    (root / "apps" / "other").resolve(),
                ],
            )
            self.assertEqual(projects[0].display_name, f"{root.name} (root)")
            self.assertEqual(projects[1].display_name, "apps/flockdock")

    def test_returns_no_projects_for_missing_root(self):
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "missing"

            self.assertEqual(discover_projects(missing), ())


if __name__ == "__main__":
    unittest.main()
