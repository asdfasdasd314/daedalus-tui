# Daedalus TUI

This directory is an independently exportable project. It contains the
Textual interface and all local agent orchestration code; it does not import
the Daedalus daemon, use a database, or communicate with Supabase.

Install it into the Python environment used from the target repository:

```bash
python3 -m pip install -e /path/to/tui
```

Launch it from a directory containing one or more Daedalus-supported
projects:

```bash
python3 -m tui
```

The launch directory is treated as a project-root workspace. The TUI
recursively discovers every directory containing a `feature_files/` folder
and lists those projects in the left sidebar. Each project has its own task
coordinator, task numbering, Git worktrees, and transcripts; switching the
sidebar does not interrupt tasks running in another project.

For Cursor CLI, edit the included `.env` file (or copy `.env.example` to a
new `.env`) and set your key:

```bash
cp .env.example .env
# edit .env and set CURSOR_API_KEY=...
```

The TUI passes `CURSOR_API_KEY` to Cursor only when it is not already present
in the process environment. You can also authenticate with `agent login`.

Each prompt creates an independent local Git worktree, runs Codex or Cursor
there, verifies the result, resolves integration failures with the selected
agent, and fast-forwards the local primary branch after successful checks. Up
to four prompts can run concurrently; integration and promotion remain
serialized. No remote push is performed, and failed worktrees are preserved
for inspection. After a successful promotion, the orchestrator refreshes and
commits `graphify-out` when the target repository has graphify configured;
graph refresh failures are reported as warnings and never trigger resolver
attempts.

The launch root stores task history in `.daedalus-memory.json`. Its `tasks`
entry maps each task worktree directory name to the submission timestamp,
prompt, provider/model/reasoning/mode selection, current state, assistant
outputs, token usage, resolved project path, and any error so failed, paused,
and cancelled work can be reopened for analysis. The memory file also keeps a
single `last_opened_project` entry.
The first launch initializes it to the default project, every sidebar focus
change updates it, and the next startup restores it when that project still
exists. The file is intentionally ignored by Git.

The task list keeps each prompt's provider, model, reasoning, status, branch,
worktree, and filtered assistant-message transcript separate. Raw diffs,
command telemetry, and successful process stderr are hidden. Select a task to
replay its transcript, then click-drag across any selectable label, log, or
error surface and use the Vim `y` command (or `Ctrl+C` / `Ctrl+Alt+S`) to copy
the highlighted text. Textual captures mouse input while the app is running;
if you want your terminal emulator's native selection instead, hold Option in
iTerm or Shift in Terminal.app while dragging.

Vim-style shortcuts are also available without changing normal prompt typing.
The prompt itself is a modal Vim text area: it starts in Insert mode, `Esc`
enters Normal mode, and `i`, `a`, `o`, `h/j/k/l`, `w`, `e`, `0`, `$`, `gg`, `G`,
`d`, `u`, `y`, `p`, Visual mode, and `Shift+V` visual-line mode are available.
`Enter` inserts a newline;
`Ctrl+Enter` submits the prompt. Yanks are mirrored to the system clipboard,
and `p` falls back to the system clipboard when the Vim register is empty.
The supported command subset is intentionally incremental so additional Vim
commands can be added as they become useful. Mouse clicks and standard
Textual key navigation remain available.

Use the mode selector for Coding, Ask, or Plan. Ask runs are read-only and do
not promote file changes. Plan runs are read-only and remain selectable in the
task list through their `planning`, `questioning`, and answer-review states.
They return a structured implementation plan and multiple-choice questions;
submit selected answers for another review round, or use the follow-up
controls to continue planning. The Implement button remains unavailable until
the agent confirms that no questions remain, then creates a separate coding
task from the approved plan. Pause preserves the task worktree and allows
resume later; Cancel stops the agent and removes that task's worktree and
branch.

When resuming, the optional notes field is sent to the agent only when it has
content. The resume prompt tells the agent to preserve existing work, inspect
`git status` and `git diff`, and continue from the current worktree.
