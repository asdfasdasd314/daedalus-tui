"""Small local JSON stores for persistent task telemetry."""

from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import tempfile
from threading import Lock


DEFAULT_MEMORY_FILE = ".daedalus-memory.json"


class TokenUsageStore:
    """Append completed-task token usage to a local JSON list."""

    def __init__(self, path: Path):
        self.path = path
        self._lock = Lock()

    def record(self, submitted_at: float, tokens: int) -> None:
        entry = {
            "timestamp": datetime.fromtimestamp(submitted_at, timezone.utc)
            .isoformat()
            .replace("+00:00", "Z"),
            "tokens": max(0, int(tokens)),
        }
        with self._lock:
            entries = self._read_entries()
            entries.append(entry)
            self._write_entries(entries)

    def _read_entries(self) -> list[dict[str, object]]:
        try:
            value = json.loads(self.path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            return []
        except OSError as error:
            raise ValueError(f"Could not read memory file {self.path}: {error}") from error
        except json.JSONDecodeError as error:
            raise ValueError(f"Memory file {self.path} is not valid JSON.") from error
        if not isinstance(value, list):
            raise ValueError(f"Memory file {self.path} must contain a JSON list.")
        return [entry for entry in value if isinstance(entry, dict)]

    def _write_entries(self, entries: list[dict[str, object]]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self.path.parent,
                prefix=f".{self.path.name}.",
                suffix=".tmp",
                delete=False,
            ) as temporary:
                temporary_path = Path(temporary.name)
                json.dump(entries, temporary, indent=2)
                temporary.write("\n")
                temporary.flush()
                os.fsync(temporary.fileno())
            os.replace(temporary_path, self.path)
            temporary_path = None
        finally:
            if temporary_path is not None:
                try:
                    temporary_path.unlink()
                except FileNotFoundError:
                    pass
