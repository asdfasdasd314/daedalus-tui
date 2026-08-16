"""Discovery of Daedalus-supported repositories beneath a launch root."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os


@dataclass(frozen=True)
class DaedalusProject:
    """A repository recognized by the presence of a ``feature_files`` folder."""

    path: Path
    launch_root: Path

    @property
    def name(self) -> str:
        return self.path.name or str(self.path)

    @property
    def display_name(self) -> str:
        if self.path == self.launch_root:
            return f"{self.name} (root)"
        try:
            return str(self.path.relative_to(self.launch_root))
        except ValueError:
            return self.name


_SKIPPED_DIRECTORY_NAMES = {
    ".git",
    ".daedalus-worktrees",
    ".venv",
    "__pycache__",
    "node_modules",
}


def discover_projects(root: Path) -> tuple[DaedalusProject, ...]:
    """Recursively find folders containing a direct ``feature_files`` child.

    Git metadata, generated worktrees, virtual environments, and dependency
    folders are skipped so a project's own copies of metadata cannot be
    mistaken for separate supported projects.
    """

    launch_root = root.expanduser().resolve()
    if not launch_root.is_dir():
        return ()

    discovered: list[DaedalusProject] = []
    for current, directories, _files in os.walk(launch_root, followlinks=False):
        directories[:] = sorted(
            directory
            for directory in directories
            if directory not in _SKIPPED_DIRECTORY_NAMES
        )
        current_path = Path(current).resolve()
        if (current_path / "feature_files").is_dir():
            discovered.append(DaedalusProject(current_path, launch_root))

    return tuple(
        sorted(
            discovered,
            key=lambda project: (project.path != launch_root, project.display_name),
        )
    )


__all__ = ["DaedalusProject", "discover_projects"]
