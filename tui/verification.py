"""Local verification discovery and execution."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import subprocess


@dataclass(frozen=True)
class VerificationResult:
    succeeded: bool
    output: str


def discover_commands(root: Path, configured: list[list[str]]) -> list[list[str]]:
    if configured:
        return configured

    commands: list[list[str]] = []
    if package_has_test_script(root / "package.json"):
        commands.append(["npm", "test"])
    if (root / "tests").is_dir():
        commands.append(["python", "-m", "pytest"])

    for child in sorted(root.iterdir()):
        if not child.is_dir() or child.name.startswith("."):
            continue
        if package_has_test_script(child / "package.json"):
            commands.append(["npm", "--prefix", child.name, "test"])
        if (child / "tests").is_dir():
            commands.append(["python", "-m", "pytest", str(Path(child.name) / "tests")])
    return commands


def package_has_test_script(path: Path) -> bool:
    if not path.is_file():
        return False
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    scripts = value.get("scripts") if isinstance(value, dict) else None
    return isinstance(scripts, dict) and isinstance(scripts.get("test"), str)


def run_verification(directory: Path, commands: list[list[str]]) -> VerificationResult:
    outputs: list[str] = []
    for command in commands:
        try:
            process = subprocess.run(command, cwd=directory, capture_output=True, text=True)
        except OSError as error:
            return VerificationResult(False, f"COMMAND: {' '.join(command)}\nERROR: {error}")
        output = format_process_result(command, process)
        outputs.append(output)
        if process.returncode != 0:
            return VerificationResult(False, "\n\n".join(outputs))
    return VerificationResult(True, "\n\n".join(outputs))


def format_process_result(command: list[str], process: subprocess.CompletedProcess[str]) -> str:
    return (
        f"COMMAND: {' '.join(command)}\n"
        f"STDOUT:\n{process.stdout}\nSTDERR:\n{process.stderr}"
    ).strip()
