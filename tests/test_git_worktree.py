import unittest
import tempfile
from pathlib import Path
from unittest.mock import call, patch

from tui.git_worktree import GitWorktreeError, GitWorktreeManager, WorktreeContext
from tui.project_config import ProjectWorktreeSettings


class GitWorktreeTests(unittest.TestCase):
    def test_list_local_branches_returns_short_ref_names(self):
        with patch("tui.git_worktree.subprocess.run") as run:
            run.return_value = type(
                "Process",
                (),
                {"returncode": 0, "stdout": "main\njames\ndevelop\n", "stderr": ""},
            )()
            from tui.git_worktree import list_local_branches

            self.assertEqual(list_local_branches(Path("/repo")), ["main", "james", "develop"])
            self.assertEqual(
                run.call_args.args[0],
                ["git", "for-each-ref", "--format=%(refname:short)", "refs/heads"],
            )

    def test_list_local_branches_returns_empty_on_git_failure(self):
        with patch("tui.git_worktree.subprocess.run") as run:
            run.return_value = type(
                "Process",
                (),
                {"returncode": 128, "stdout": "", "stderr": "not a git repository"},
            )()
            from tui.git_worktree import list_local_branches

            self.assertEqual(list_local_branches(Path("/repo")), [])

    def test_create_uses_primary_sha_and_task_branch(self):
        with tempfile.TemporaryDirectory() as directory:
            manager = GitWorktreeManager(Path(directory) / "repo")
            with patch.object(manager, "_validate_primary"), patch.object(manager, "git_output", return_value="abc123"), patch.object(manager, "run_git") as run_git:
                context = manager.create("task-1")

            self.assertEqual(context.base_commit, "abc123")
            self.assertEqual(context.branch_name, "agent/task-task-1")
            self.assertEqual(context.path, Path(directory).resolve() / ".daedalus-worktrees" / "repo" / "task-task-1")
            self.assertEqual(run_git.call_args.args[0][:4], ["worktree", "add", "-b", "agent/task-task-1"])

    def test_primary_validation_rejects_dirty_repository_when_target_checked_out(self):
        manager = GitWorktreeManager(Path("/repo"))
        with patch("tui.git_worktree.subprocess.run") as run, patch.object(
            manager, "git_output", side_effect=["main", " M changed.py"]
        ):
            run.return_value = type("Process", (), {"returncode": 0, "stdout": "", "stderr": ""})()
            with self.assertRaises(GitWorktreeError):
                manager._validate_primary()

    def test_primary_validation_allows_other_checked_out_branch(self):
        manager = GitWorktreeManager(Path("/repo"), primary_branch="develop")
        with patch("tui.git_worktree.subprocess.run") as run, patch.object(
            manager, "git_output", return_value="feature"
        ):
            run.return_value = type("Process", (), {"returncode": 0, "stdout": "", "stderr": ""})()
            manager.validate_primary()

    def test_primary_validation_rejects_missing_target_branch(self):
        manager = GitWorktreeManager(Path("/repo"), primary_branch="missing")
        with patch("tui.git_worktree.subprocess.run") as run:
            run.return_value = type("Process", (), {"returncode": 1, "stdout": "", "stderr": ""})()
            with self.assertRaisesRegex(GitWorktreeError, "does not exist"):
                manager.validate_primary()

    def test_promote_fast_forwards_checked_out_target_with_merge(self):
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory) / "repo"
            worktree = Path(directory) / "task"
            worktree.mkdir()
            manager = GitWorktreeManager(repository, primary_branch="main")
            context = WorktreeContext(repository, "task-1", "base", "agent/task-task-1", worktree)
            with patch.object(manager, "_validate_primary"), patch.object(
                manager, "git_output", side_effect=["base", "tip", "main"]
            ), patch.object(manager, "run_git") as run_git, patch(
                "tui.git_worktree.subprocess.run"
            ) as run:
                run.return_value = type("Process", (), {"returncode": 0, "stdout": "", "stderr": ""})()
                manager.promote(context, "base")

            self.assertEqual(run_git.call_args.args[0], ["merge", "--ff-only", "agent/task-task-1"])

    def test_promote_updates_target_ref_when_not_checked_out(self):
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory) / "repo"
            worktree = Path(directory) / "task"
            worktree.mkdir()
            manager = GitWorktreeManager(repository, primary_branch="develop")
            context = WorktreeContext(repository, "task-1", "base", "agent/task-task-1", worktree)
            with patch.object(manager, "_validate_primary"), patch.object(
                manager, "git_output", side_effect=["base", "tip", "feature"]
            ), patch.object(manager, "run_git") as run_git, patch(
                "tui.git_worktree.subprocess.run"
            ) as run:
                run.return_value = type("Process", (), {"returncode": 0, "stdout": "", "stderr": ""})()
                manager.promote(context, "base")

            self.assertEqual(
                run_git.call_args.args[0],
                ["update-ref", "refs/heads/develop", "tip", "base"],
            )

    def test_prepare_primary_checkout_reuses_repository_when_target_checked_out(self):
        manager = GitWorktreeManager(Path("/repo"), primary_branch="main")
        with patch.object(manager, "is_primary_checked_out", return_value=True):
            checkout, temporary = manager.prepare_primary_checkout()
        self.assertEqual(checkout, Path("/repo").resolve())
        self.assertIsNone(temporary)

    def test_prepare_primary_checkout_adds_temporary_worktree_when_needed(self):
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory) / "repo"
            repository.mkdir()
            manager = GitWorktreeManager(repository, primary_branch="develop")
            with patch.object(manager, "is_primary_checked_out", return_value=False), patch.object(
                manager, "run_git"
            ) as run_git:
                checkout, temporary = manager.prepare_primary_checkout()

            self.assertEqual(checkout, temporary)
            self.assertEqual(checkout.parent, manager.repository.parent / manager.root_name / manager.repository.name)
            self.assertTrue(checkout.name.startswith(".graphify-"))
            self.assertEqual(run_git.call_args.args[0][:2], ["worktree", "add"])
            self.assertEqual(run_git.call_args.args[0][3], "develop")

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

    def test_provision_reuses_existing_correct_readonly_symlink(self):
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory) / "repo"
            worktree = Path(directory) / "task"
            repository.mkdir()
            worktree.mkdir()
            source = repository / "food-data"
            source.mkdir()
            target = worktree / "food-data"
            target.symlink_to(source, target_is_directory=True)
            context = WorktreeContext(repository, "task-1", "base", "agent/task-task-1", worktree)
            manager = GitWorktreeManager(repository)

            manager.provision_worktree(context, ProjectWorktreeSettings(readonly_paths=("food-data",)))

            self.assertTrue(target.is_symlink())
            self.assertEqual(target.resolve(), source.resolve())

    def test_provision_rejects_existing_real_readonly_destination(self):
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory) / "repo"
            worktree = Path(directory) / "task"
            repository.mkdir()
            worktree.mkdir()
            (repository / "food-data").mkdir()
            (worktree / "food-data").mkdir()
            context = WorktreeContext(repository, "task-1", "base", "agent/task-task-1", worktree)
            manager = GitWorktreeManager(repository)

            with self.assertRaisesRegex(GitWorktreeError, "destination exists"):
                manager.provision_worktree(context, ProjectWorktreeSettings(readonly_paths=("food-data",)))


if __name__ == "__main__":
    unittest.main()
