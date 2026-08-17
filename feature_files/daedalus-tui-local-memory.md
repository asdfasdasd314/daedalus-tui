# Daedalus TUI Local Persistent Memory

## Summary
The TUI persists completed-task token usage and the last opened project in a
local JSON file so usage history and project navigation survive application
restarts without depending on the Daedalus daemon, a remote service, or a
database server.

## Key Points
- **Local persistence**: Each project stores usage in `.daedalus-memory.json`
  at its repository root. The file is intentionally ignored by Git.
- **Current record shape**: Each usage entry is a JSON object with an ISO-8601
  UTC `timestamp` for prompt submission, a non-negative integer `tokens` value,
  and nullable `provider`, `model`, and `reasoning` metadata. Providers without
  model or reasoning controls, such as Cursor, store `null` for those fields.
- **Append behavior**: A missing memory file starts as an empty list; each
  successful task appends one record while preserving existing entries.
- **Project restoration**: The launch root's memory file keeps one
  `last_opened_project` entry. Startup selects it when it is still among the
  discovered projects, and otherwise selects the first discovered project.
- **Project updates**: Selecting a different project replaces the existing
  `last_opened_project` entry without changing token-usage records.
- **Completion boundary**: Only successfully completed tasks are recorded.
  Failed, paused, and cancelled tasks do not contribute telemetry.
- **Safe writes**: Updates are serialized in-process and written through a
  temporary file followed by an atomic replacement, so a completed write does
  not leave a partially written JSON document.
- **Corrupt input**: Invalid JSON or a non-list top-level value raises a
  validation error and leaves the existing file unchanged. Telemetry errors
  are isolated from otherwise successful task completion.
- **Provider interface**: Provider-specific output parsing supplies the total
  input/output token count and the coordinator supplies the selected provider
  metadata; this feature owns storage, not provider parsing.
- **Legacy compatibility**: Older token entries without provider metadata are
  normalized to explicit `null` fields the next time the memory file is saved.

## Relevant Files
- `tui/memory.py`: `TokenUsageStore`, the default memory filename, JSON schema,
  last-project entry, validation, locking, and atomic file replacement.
- `tui/app.py`: Restores the remembered project at startup and updates it on
  project selection.
- `tui/task_coordinator.py`: Records usage after successful orchestration and
  injects the project-local memory path.
- `tui/agent_runner.py`: Extracts provider-reported token usage consumed by
  the memory store.
- `tests/test_memory.py`: Covers JSON record creation, project-marker updates,
  and preservation of a corrupt file.
- `tests/test_app.py`: Covers startup restoration and sidebar persistence of
  the last opened project.
- `tests/test_task_coordinator.py`: Covers recording only successful task
  results.
- `README.md`: Documents the project-local file and its lifecycle.

## Dev Mode
HACKING

## State Log
- 2026-08-16: Documented the existing local JSON token-usage store, its completion-only recording boundary, and its atomic write and validation behavior.
- 2026-08-16: Added an updatable launch-root project marker so startup restores the last available project and falls back to the first discovered project.
- 2026-08-16: Normalized discovered project paths at app startup so memory restoration and fallback remain canonical across symlinked temporary paths.
- 2026-08-16: Seeded the ignored launch-root memory file with the canonical path of the active daedalus-tui worktree.
- 2026-08-16: Added provider, model, and reasoning metadata to token-usage entries, with nullable fields for legacy records and providers without those controls.
