# Daedalus TUI Local Persistent Memory

## Summary
The TUI persists task history and the last opened project in one launch-root
local JSON file so failed work can be reopened for analysis and project
navigation can survive application restarts without depending on the Daedalus
daemon, a remote service, or a database server.

## Key Points
- **Local persistence**: The launch root stores all task history in one
  `.daedalus-memory.json` file. The file is intentionally ignored by Git.
- **Task history**: A single `tasks` entry maps each task worktree directory
  name to an ISO-8601 UTC submission `timestamp`, prompt, provider, model,
  reasoning, mode, current state, assistant outputs, and error. The entry is
  upserted as the task progresses, including for failed, paused, and cancelled
  tasks.
- **Upsert behavior**: A missing memory file starts as an empty list; each
  task creates or updates one worktree-keyed entry while preserving other task
  entries.
- **Project restoration**: The launch root's memory file keeps one
  `last_opened_project` entry. Startup selects it when it is still among the
  discovered projects, and otherwise selects the first discovered project and
  creates or repairs the marker.
- **Project updates**: Selecting a different project immediately replaces the
  existing `last_opened_project` entry, including when focus later switches
  back to an earlier project, without changing task-history entries.
- **Safe writes**: Updates are serialized in-process and written through a
  temporary file followed by an atomic replacement, so a completed write does
  not leave a partially written JSON document.
- **Corrupt input**: Invalid JSON or a non-list top-level value raises a
  validation error and leaves the existing file unchanged. Memory errors are
  isolated from otherwise successful task completion.
- **Legacy compatibility**: Older standalone token-usage entries are removed
  the next time the memory file is saved.

## Relevant Files
- `tui/memory.py`: `TaskMemoryStore`, the default memory filename, JSON schema,
  task-history and last-project entries, validation, locking, and atomic file
  replacement.
- `tui/app.py`: Restores the remembered project at startup and updates it on
  project selection.
- `tui/task_coordinator.py`: Records task snapshots throughout orchestration.
- `tests/test_memory.py`: Covers task-history creation and upserts, removal of
  legacy usage entries, project-marker updates, and preservation of a corrupt
  file.
- `tests/test_app.py`: Covers startup restoration and sidebar persistence of
  the last opened project.
- `tests/test_task_coordinator.py`: Covers task snapshots for successful and
  unsuccessful task results.
- `README.md`: Documents the launch-root file and its lifecycle.

## Dev Mode
HACKING

## State Log
- 2026-08-16: Documented the existing local JSON token-usage store, its completion-only recording boundary, and its atomic write and validation behavior.
- 2026-08-16: Added an updatable launch-root project marker so startup restores the last available project and falls back to the first discovered project.
- 2026-08-16: Normalized discovered project paths at app startup so memory restoration and fallback remain canonical across symlinked temporary paths.
- 2026-08-16: Seeded the ignored launch-root memory file with the canonical path of the active daedalus-tui worktree.
- 2026-08-16: Added provider, model, and reasoning metadata to token-usage entries, with nullable fields for legacy records and providers without those controls.
- 2026-08-16: Made startup initialization and every project-focus transition use an explicit single-marker update, with coverage for first launch and repeated switching.
- 2026-08-17: Centralized all prompt telemetry in the launch-root memory file and recorded the resolved project destination for each completed prompt.
- 2026-08-17: Added worktree-keyed task history snapshots so prompt metadata, lifecycle state, outputs, and failure diagnostics survive task completion or failure.
- 2026-08-17: Replaced standalone token-usage entries with timestamped task records while preserving the last-opened-project marker.
