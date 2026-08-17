# Daedalus TUI Coding Statistics

## Summary
The coding statistics tracker presents local task token usage and derived provider and time-window statistics from the TUI's persisted task history.

## Key Points
- `Ctrl+T` opens a modal coding statistics view and is listed in the keyboard shortcuts menu.
- The left panel lists each task timestamp, provider, and recorded token total.
- The top metrics show cumulative and current-local-day token usage.
- The right panel shows average tokens per prompt, recent-hour usage, a seven-day projection based on recorded average daily usage, and provider percentages.
- The tracker reads the existing local task memory and overlays live task snapshots so current-session totals stay accurate.

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
