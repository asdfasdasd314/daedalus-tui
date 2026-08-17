"""Small local JSON stores for persistent task telemetry."""

from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import tempfile
from threading import Lock


DEFAULT_MEMORY_FILE = ".daedalus-memory.json"
LAST_OPENED_PROJECT_KEY = "last_opened_project"


class TokenUsageStore:
    """Persist task telemetry and the most recently opened project."""

    _locks_guard = Lock()
    _locks: dict[Path, Lock] = {}

    def __init__(self, path: Path):
        self.path = path
        lock_key = path.expanduser().resolve()
        with self._locks_guard:
            self._lock = self._locks.setdefault(lock_key, Lock())

    def record(
        self,
        submitted_at: float,
        tokens: int,
        provider: str | None = None,
        model: str | None = None,
        reasoning: str | None = None,
    ) -> None:
        entry = {
            "timestamp": datetime.fromtimestamp(submitted_at, timezone.utc)
            .isoformat()
            .replace("+00:00", "Z"),
            "tokens": max(0, int(tokens)),
            "provider": provider,
            "model": model,
            "reasoning": reasoning,
        }
        with self._lock:
            entries = self._read_entries()
            entries.append(entry)
            self._write_entries(entries)

    def get_last_opened_project(self) -> Path | None:
        """Return the remembered project path, if the memory contains one."""
        with self._lock:
            entries = self._read_entries()
        for entry in reversed(entries):
            value = entry.get(LAST_OPENED_PROJECT_KEY)
            if isinstance(value, str) and value:
                return Path(value).expanduser().resolve()
        return None

    def record_last_opened_project(self, project_path: Path) -> None:
        """Update the single last-opened-project entry without losing telemetry."""
        entry = {LAST_OPENED_PROJECT_KEY: str(project_path.expanduser().resolve())}
        with self._lock:
            entries = self._read_entries()
            updated_entries: list[dict[str, object]] = []
            replaced = False
            for existing in entries:
                if LAST_OPENED_PROJECT_KEY in existing:
                    if not replaced:
                        updated_entries.append(entry)
                        replaced = True
                    continue
                updated_entries.append(existing)
            if not replaced:
                updated_entries.append(entry)
            self._write_entries(updated_entries)

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
        return [self._normalize_entry(entry) for entry in value if isinstance(entry, dict)]

    @staticmethod
    def _normalize_entry(entry: dict[str, object]) -> dict[str, object]:
        """Give legacy telemetry entries the current nullable metadata shape."""
        if "timestamp" not in entry or "tokens" not in entry:
            return entry
        return {
            **entry,
            "provider": entry.get("provider"),
            "model": entry.get("model"),
            "reasoning": entry.get("reasoning"),
        }

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
