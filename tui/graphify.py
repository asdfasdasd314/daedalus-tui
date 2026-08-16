"""Best-effort graph refresh owned by the local orchestration layer."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil
import subprocess


@dataclass(frozen=True)
class GraphifyResult:
    attempted: bool
    succeeded: bool
    output: str = ""


def update_repository(repository: Path, executable: str = "graphify") -> GraphifyResult:
    """Refresh the primary repository graph without affecting task success."""
    if shutil.which(executable) is None:
        return GraphifyResult(False, False, f"{executable} is not available on PATH.")
    try:
        process = subprocess.run(
            [executable, "update", "."],
            cwd=repository,
            capture_output=True,
            text=True,
        )
    except OSError as error:
        return GraphifyResult(True, False, str(error))
    output = "\n".join(part.strip() for part in (process.stdout, process.stderr) if part.strip())
    return GraphifyResult(True, process.returncode == 0, output)
