# Daedalus TUI Coding Statistics

## Summary
The coding statistics tracker presents local task token usage and derived provider and time-window statistics from the TUI's persisted task history.

## Key Points
- `Ctrl+T` opens a modal coding statistics view and is listed in the keyboard shortcuts menu.
- The left panel lists each task timestamp, provider, and recorded token total.
- The top metrics show cumulative usage, current-local-day usage, and a 30-day projection based on recorded average daily usage.
- The view toggles between token and task units; task counts use the same completed-task records as token accounting.
- The right panel shows average usage per prompt, recent-hour usage, seven- and 30-day projections, and provider percentages in the selected unit.
- The tracker reads the existing local task memory and overlays live task snapshots so current-session totals stay accurate.
- Only completed tasks contribute to token usage; this applies equally to completed plan and coding tasks.

## Relevant Files
- `tui/token_usage.py`: Usage records, aggregation utilities, and memory/live-record conversion.
- `tui/memory.py`: Read access to persisted task snapshots.
- `tui/app.py`: Shortcut binding and statistics modal.
- `tui/app.tcss`: Statistics modal layout and styling.
- `parameter_files/daedalus-tui-coding-statistics.toml`: Projection and recent-window settings.

## Dev Mode
HACKING

## State Log
- 2026-08-17: Added persisted and live token usage aggregation with a `Ctrl+T` coding statistics modal.
- 2026-08-17: Restricted token accounting to tasks that complete successfully, including plan tasks.
- 2026-08-17: Added task-unit statistics, a token/task toggle, and a configurable 30-day projection.
