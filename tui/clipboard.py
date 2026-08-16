"""System clipboard helpers for terminals without OSC 52 support."""

from __future__ import annotations

import shutil
import subprocess


def copy_to_system_clipboard(text: str) -> bool:
    commands = (
        ["pbcopy"],
        ["wl-copy"],
        ["xclip", "-selection", "clipboard"],
        ["xsel", "--clipboard", "--input"],
        ["clip"],
    )
    for command in commands:
        if shutil.which(command[0]) is None:
            continue
        try:
            process = subprocess.run(
                command,
                input=text,
                text=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
        except OSError:
            continue
        if process.returncode == 0:
            return True
    return False


def paste_from_system_clipboard() -> str | None:
    """Read clipboard text using the native command available on the host."""
    commands = (
        ["pbpaste"],
        ["wl-paste", "--no-newline"],
        ["xclip", "-selection", "clipboard", "-o"],
        ["xsel", "--clipboard", "--output"],
    )
    for command in commands:
        if shutil.which(command[0]) is None:
            continue
        try:
            process = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
            )
        except OSError:
            continue
        if process.returncode == 0:
            return process.stdout
    return None
