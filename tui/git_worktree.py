"""Local Git worktree lifecycle used by the standalone orchestrator."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess

from .project_config import ProjectWorktreeSettings


class GitWorktreeError(RuntimeError):
    pass


@dataclass(frozen=True)
class WorktreeContext:
    repository: Path
    task_id: str
    base_commit: str
    branch_name: str
    path: Path


class GitWorktreeManager:
    def __init__(self, repository: Path, primary_branch: str = "main", root_name: str = ".daedalus-worktrees"):
        self.repository = repository.resolve()
        self.primary_branch = primary_branch
        self.root_name = root_name

    def create(self, task_id: str) -> WorktreeContext:
        self._validate_primary()
        base_commit = self.git_output(["rev-parse", self.primary_branch])
        branch_name = f"agent/task-{task_id}"
        path = self.repository.parent / self.root_name / self.repository.name / f"task-{task_id}"
        path.parent.mkdir(parents=True, exist_ok=True)
        self.run_git(["worktree", "add", "-b", branch_name, str(path), base_commit])
        return WorktreeContext(self.repository, task_id, base_commit, branch_name, path)

    def provision_worktree(self, context: WorktreeContext, settings: ProjectWorktreeSettings) -> None:
        """Install project resources and link declared shared read-only paths."""
        if settings.install_command:
            process = subprocess.run(
                list(settings.install_command),
                cwd=context.path,
                capture_output=True,
                text=True,
            )
            if process.returncode != 0:
                raise GitWorktreeError(
                    self.format_failure(list(settings.install_command), process)
                )

        for relative_path in settings.readonly_paths:
            source = self.repository / relative_path
            target = context.path / relative_path
            if not source.exists():
                raise GitWorktreeError(
                    f"Configured read-only path is missing from the primary worktree: {source}"
                )
            if target.is_symlink():
                if target.resolve(strict=False) == source.resolve():
                    continue
                raise GitWorktreeError(
                    f"Cannot link configured read-only path because the worktree destination exists: {target}"
                )
            if target.exists():
                raise GitWorktreeError(
                    f"Cannot link configured read-only path because the worktree destination exists: {target}"
                )
            target.parent.mkdir(parents=True, exist_ok=True)
            target.symlink_to(source, target_is_directory=source.is_dir())

    def commit_changes(self, directory: Path, message: str) -> bool:
        if not self.git_output(["status", "--porcelain"], directory):
            return False
        self.stage_changes(directory)
        self.run_git(["commit", "-m", message], directory)
        return True

    def stage_changes(self, directory: Path) -> None:
        """Stage the current worktree contents for orchestration checks or commit."""
        self.run_git(["add", "-A"], directory)

    def discard_graphify_changes(self, directory: Path) -> None:
        """Remove graphify output changes from an agent worktree.

        Graphify refreshes belong to the primary-repository post-promotion
        hook.  A task agent that runs one in its isolated worktree must not
        turn generated graph files into task changes or merge conflicts.
        """
        graphify_path = "graphify-out"
        if not (directory / graphify_path).exists():
            return
        self.run_git(["restore", "--source=HEAD", "--staged", "--worktree", "--", graphify_path], directory)
        self.run_git(["clean", "-fd", "--", graphify_path], directory)

    def reset_task_to_base(self, context: WorktreeContext) -> None:
        """Keep a read-only planning pass from becoming an implementation change."""
        self.run_git(["reset", "--hard", context.base_commit], context.path)
        self.run_git(["clean", "-fd"], context.path)

    def commit_graphify_changes(self, message: str) -> bool:
        """Commit only the generated graph after a successful primary update."""
        if not self.git_output(["status", "--porcelain", "--", "graphify-out"]):
            return False
        self.run_git(["add", "--", "graphify-out"])
        self.run_git(["commit", "-m", message])
        return True

    def merge_primary_into_task(self, context: WorktreeContext) -> None:
        self.run_git(["merge", "--no-ff", "--no-edit", self.primary_branch], context.path)

    def promote(self, context: WorktreeContext, expected_base: str | None = None) -> None:
        self._validate_primary()
        expected_base = expected_base or context.base_commit
        current = self.git_output(["rev-parse", self.primary_branch])
        if current != expected_base:
            raise GitWorktreeError("Primary branch advanced outside the integration run.")
        self.run_git(["merge", "--ff-only", context.branch_name])

    def capture_primary(self) -> str:
        self._validate_primary()
        return self.git_output(["rev-parse", self.primary_branch])

    def remove_successful(self, context: WorktreeContext) -> None:
        if context.path.exists():
            self.run_git(["worktree", "remove", "--force", str(context.path)])
        else:
            self.run_git(["worktree", "prune"])
        self.run_git(["branch", "-d", context.branch_name])

    def remove_cancelled(self, context: WorktreeContext) -> None:
        """Remove a cancelled task even when its branch was never integrated."""
        if context.path.exists():
            self.run_git(["worktree", "remove", "--force", str(context.path)])
        else:
            self.run_git(["worktree", "prune"])
        self.run_git(["branch", "-D", context.branch_name])

    def is_clean(self, directory: Path) -> bool:
        return not self.git_output(["status", "--porcelain"], directory)

    def head(self, directory: Path) -> str:
        return self.git_output(["rev-parse", "HEAD"], directory)

    def has_unmerged_paths(self, directory: Path) -> bool:
        return bool(self.git_output(["diff", "--name-only", "--diff-filter=U"], directory))

    def validate_primary(self) -> None:
        if self.git_output(["branch", "--show-current"]) != self.primary_branch:
            raise GitWorktreeError(f"Primary worktree must have {self.primary_branch} checked out.")
        if not self.is_clean(self.repository):
            raise GitWorktreeError("Primary worktree must be clean before starting or promoting an agent.")

    def _validate_primary(self) -> None:
        """Compatibility alias for callers that used the original private helper."""
        self.validate_primary()

    def run_git(self, arguments: list[str], directory: Path | None = None) -> subprocess.CompletedProcess[str]:
        process = subprocess.run(
            ["git", *arguments],
            cwd=directory or self.repository,
            capture_output=True,
            text=True,
        )
        if process.returncode != 0:
            raise GitWorktreeError(self.format_failure(["git", *arguments], process))
        return process

    def git_output(self, arguments: list[str], directory: Path | None = None) -> str:
        return self.run_git(arguments, directory).stdout.strip()

    @staticmethod
    def format_failure(arguments: list[str], process: subprocess.CompletedProcess[str]) -> str:
        return (
            f"COMMAND: {' '.join(arguments)}\n"
            f"STDOUT:\n{process.stdout}\nSTDERR:\n{process.stderr}"
        ).strip()
