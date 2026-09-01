"""Pytest hooks shared across the test suite."""

from __future__ import annotations

import subprocess
import sys


def pytest_configure(config) -> None:
  """Install pyan3 when call-graph tests run in an environment missing it."""
  try:
    import pyan  # noqa: F401
  except ImportError:
    subprocess.check_call(
      [sys.executable, "-m", "pip", "install", "pyan3>=2.8,<3"],
    )
