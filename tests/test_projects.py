import tempfile
import unittest
from pathlib import Path

from tui.config import ProjectDiscoverySettings
from tui.projects import discover_projects


class ProjectDiscoveryTests(unittest.TestCase):
    def test_finds_only_immediate_child_projects_in_deterministic_order(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "feature_files").mkdir()
            (root / "zeta" / "feature_files").mkdir(parents=True)
            (root / "daedalus" / "feature_files").mkdir(parents=True)
            (root / "project-initialization" / "feature_files").mkdir(parents=True)
            (root / "daedalus" / "project-initialization" / "other-project" / "feature_files").mkdir(
                parents=True
            )
            (root / "project-initialization" / "other-project" / "feature_files").mkdir(
                parents=True
            )
            (root / ".daedalus-worktrees" / "ignored" / "feature_files").mkdir(parents=True)
            (root / "node_modules" / "dependency" / "feature_files").mkdir(parents=True)
            (root / ".git" / "ignored" / "feature_files").mkdir(parents=True)
            (root / ".venv" / "ignored" / "feature_files").mkdir(parents=True)
            (root / "__pycache__" / "ignored" / "feature_files").mkdir(parents=True)

            projects = discover_projects(root)

            self.assertEqual(
                [project.path for project in projects],
                [
                    (root / "daedalus").resolve(),
                    (root / "project-initialization").resolve(),
                    (root / "zeta").resolve(),
                ],
            )
            self.assertEqual(
                [project.display_name for project in projects],
                ["daedalus", "project-initialization", "zeta"],
            )

    def test_ignores_launch_root_feature_files_when_no_child_is_eligible(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "feature_files").mkdir()

            self.assertEqual(discover_projects(root), ())

    def test_lists_plain_git_checkouts_alongside_daedalus_projects(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "formatted" / "feature_files").mkdir(parents=True)
            (root / "plain-repo" / ".git").mkdir(parents=True)
            (root / "just-a-folder").mkdir()

            projects = discover_projects(
                root, ProjectDiscoverySettings(include_git_repositories=True)
            )

            self.assertEqual(
                [project.display_name for project in projects],
                ["formatted", "plain-repo (unformatted)"],
            )
            self.assertTrue(projects[0].formatted)
            self.assertFalse(projects[1].formatted)
            self.assertTrue(projects[1].git_repository)

    def test_lists_every_child_directory_when_configured(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "formatted" / "feature_files").mkdir(parents=True)
            (root / "just-a-folder").mkdir()
            (root / "node_modules").mkdir()

            projects = discover_projects(
                root, ProjectDiscoverySettings(include_all_directories=True)
            )

            self.assertEqual(
                [project.display_name for project in projects],
                ["formatted", "just-a-folder (unformatted)"],
            )

    def test_unformatted_folders_stay_hidden_by_default(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "formatted" / "feature_files").mkdir(parents=True)
            (root / "plain-repo" / ".git").mkdir(parents=True)

            self.assertEqual(
                [project.name for project in discover_projects(root)],
                ["formatted"],
            )

    def test_returns_no_projects_for_missing_root(self):
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "missing"

            self.assertEqual(discover_projects(missing), ())


if __name__ == "__main__":
    unittest.main()
