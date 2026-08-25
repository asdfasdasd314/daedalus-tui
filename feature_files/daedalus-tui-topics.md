# Daedalus TUI Topics

## Summary
Optional Topics group closely related tasks and features under a shared
git-tracked markdown umbrella (`topic_files/{slug}.md`) so agents can carry
concise recurrent memory without replaying full conversations.

## Key Points
- **Optional attachment**: Tasks may omit a topic. The settings-bar Topic
  Select defaults to `(None)` and does not persist the last selection in
  launch-root memory; New Task and project switches reset to `(None)`.
- **External authorship**: Operators create and edit topic markdown outside
  the TUI (or via a later coding task). The TUI only lists existing
  `topic_files/*.md` stems from the active project checkout.
- **Schema**: Each topic file has an H1 name plus `## Topic Goal`,
  `## Topic Status` (`open` | `complete`), and `## State Log`.
- **Prompt embed**: When tagged, the orchestrator loads the topic from the
  task worktree and embeds it with mode-specific instructions (coding may
  append State Log / set Status; ask/plan are read-only for topic files;
  repair/resolver re-embed and only write when the umbrella outcome changes).
- **Inheritance**: Plan → Implement, retry, resume, repair, resolver, and
  plan-question clarifications keep the originating task's topic slug.
- **Boundary**: Topics are project-local and optional; project discovery still
  keys only on `feature_files/`. Concurrent State Log appends can race the
  same way concurrent feature-file edits can.

## Relevant Files
- `tui/topics.py`: Discovery, load, validation helpers, and prompt embed.
- `tui/prompts.py`: Optional topic blocks on task, repair, and resolver prompts.
- `tui/orchestrator.py`: Loads tagged topics from the task worktree before prompts.
- `tui/task_coordinator.py`: Optional `topic` on `TaskRecord` / submit and inheritance.
- `tui/memory.py`: Optional `topic` on persisted task snapshots.
- `tui/app.py`: Topic Select beside Mode / Branch.
- `parameter_files/daedalus-tui-topics.toml`: Paired parameter file (no tunables in v1).
- `tests/test_topics.py`, `tests/test_prompts.py`, `tests/test_app.py`,
  `tests/test_memory.py`, `tests/test_task_coordinator.py`: Coverage for
  discovery, embeds, UI, persistence, and inheritance.

## Dev Mode
HACKING

## State Log
- 2026-08-24: Introduced optional Topics with markdown schema, prompt embeds,
  settings-bar Select, memory persistence, and coding State Log updates.
