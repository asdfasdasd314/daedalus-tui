import unittest
import tempfile
from pathlib import Path
from unittest.mock import call, patch

from tui.git_worktree import GitWorktreeError, GitWorktreeManager, WorktreeContext
from tui.project_config import ProjectWorktreeSettings


class GitWorktreeTests(unittest.TestCase):
    def test_create_uses_primary_sha_and_task_branch(self):
        with tempfile.TemporaryDirectory() as directory:
            manager = GitWorktreeManager(Path(directory) / "repo")
            with patch.object(manager, "_validate_primary"), patch.object(manager, "git_output", return_value="abc123"), patch.object(manager, "run_git") as run_git:
                context = manager.create("task-1")

            self.assertEqual(context.base_commit, "abc123")
            self.assertEqual(context.branch_name, "agent/task-task-1")
            self.assertEqual(context.path, Path(directory).resolve() / ".daedalus-worktrees" / "repo" / "task-task-1")
            self.assertEqual(run_git.call_args.args[0][:4], ["worktree", "add", "-b", "agent/task-task-1"])

    def test_primary_validation_rejects_dirty_repository(self):
        manager = GitWorktreeManager(Path("/repo"))
        with patch.object(manager, "git_output", side_effect=["main", " M changed.py"]):
            with self.assertRaises(GitWorktreeError):
                manager._validate_primary()

    def test_successful_cleanup_forces_worktree_removal_before_branch_delete(self):
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory) / "repo"
            worktree = Path(directory) / "task"
            worktree.mkdir()
            manager = GitWorktreeManager(repository)
            context = WorktreeContext(repository, "task-1", "base", "agent/task-task-1", worktree)
            with patch.object(manager, "run_git") as run_git:
                manager.remove_successful(context)

            self.assertEqual(run_git.call_args_list[0].args[0], ["worktree", "remove", "--force", str(worktree)])
            self.assertEqual(run_git.call_args_list[1].args[0], ["branch", "-d", "agent/task-task-1"])

    def test_cancel_cleanup_force_deletes_unintegrated_branch(self):
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory) / "repo"
            worktree = Path(directory) / "task"
            worktree.mkdir()
            manager = GitWorktreeManager(repository)
            context = WorktreeContext(repository, "task-1", "base", "agent/task-task-1", worktree)
            with patch.object(manager, "run_git") as run_git:
                manager.remove_cancelled(context)

            self.assertEqual(run_git.call_args_list[0].args[0], ["worktree", "remove", "--force", str(worktree)])
            self.assertEqual(run_git.call_args_list[1].args[0], ["branch", "-D", "agent/task-task-1"])

    def test_discard_graphify_changes_restores_and_cleans_only_graph_output(self):
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory) / "repo"
            (repository / "graphify-out").mkdir(parents=True)
            manager = GitWorktreeManager(repository)
            with patch.object(manager, "run_git") as run_git:
                manager.discard_graphify_changes(repository)

            self.assertEqual(
                [call.args[0] for call in run_git.call_args_list],
                [
                    ["restore", "--source=HEAD", "--staged", "--worktree", "--", "graphify-out"],
                    ["clean", "-fd", "--", "graphify-out"],
                ],
            )

    def test_stage_changes_stages_the_entire_worktree(self):
        with tempfile.TemporaryDirectory() as directory:
            manager = GitWorktreeManager(Path(directory) / "repo")
            worktree = Path(directory) / "task"
            with patch.object(manager, "run_git") as run_git:
                manager.stage_changes(worktree)

            run_git.assert_called_once_with(["add", "-A"], worktree)

    @patch("tui.git_worktree.subprocess.run")
    def test_provision_runs_install_and_links_readonly_path(self, run):
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory) / "repo"
            worktree = Path(directory) / "task"
            repository.mkdir()
            worktree.mkdir()
            (repository / "food-data").mkdir()
            context = WorktreeContext(repository, "task-1", "base", "agent/task-task-1", worktree)
            run.return_value = type("Process", (), {"returncode": 0, "stdout": "", "stderr": ""})()
            manager = GitWorktreeManager(repository)

            manager.provision_worktree(
                context,
                ProjectWorktreeSettings(("npm", "ci"), ("food-data",)),
            )

            self.assertTrue((worktree / "food-data").is_symlink())
            self.assertEqual((worktree / "food-data").resolve(), (repository / "food-data").resolve())
            run.assert_called_once_with(["npm", "ci"], cwd=worktree, capture_output=True, text=True)

    def test_provision_rejects_missing_readonly_path(self):
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory) / "repo"
            worktree = Path(directory) / "task"
            repository.mkdir()
            worktree.mkdir()
            context = WorktreeContext(repository, "task-1", "base", "agent/task-task-1", worktree)
            manager = GitWorktreeManager(repository)

            with self.assertRaises(GitWorktreeError):
                manager.provision_worktree(context, ProjectWorktreeSettings(readonly_paths=("food-data",)))


if __name__ == "__main__":
    unittest.main()
