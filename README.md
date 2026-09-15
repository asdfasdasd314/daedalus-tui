# Daedalus TUI

This directory is an independently exportable project. It contains the
Textual interface and all local agent orchestration code; it does not import
the Daedalus daemon, use a database, or communicate with Supabase.

Install it into the Python environment used from the target repository:

```bash
python3 -m pip install -e /path/to/tui
```

The standalone call-graph visualizer can inspect an arbitrary Python checkout
without adding Daedalus files first. Edit
`parameter_files/daedalus-tui-call-graph-visualization.toml` and set
`analysis_project` to the checkout directory name. `current` analyzes the
working directory; any other name resolves automatically under `projects_root`
(default `~/Projects`). For a checkout elsewhere, add an optional
`[projects."name"]` table with a `root` path and any project-specific analysis
overrides. The generic project defaults discover Python files recursively, and
a target-local call-graph parameter file takes precedence when available.

Launch it from a directory containing one or more Daedalus-supported
projects:

```bash
python3 -m tui
```

The launch directory is treated as a project workspace. The TUI discovers its
immediate child directories; nested descendants are not traversed or listed.
Folders with a `feature_files/` directory are listed first as Daedalus
projects, and plain Git checkouts are listed after them marked
`(unformatted)` so the TUI is not limited to projects you have already
converted. Set `include_all_directories = true` in the `[projects]` table of
`parameter_files/daedalus-tui.toml` to list every child directory, or
`include_git_repositories = false` to show Daedalus projects only. If no
eligible child project exists, the launch directory remains available as a
usability fallback. Each project
has its own task coordinator, task numbering, Git worktrees, and transcripts;
switching the sidebar does not interrupt tasks running in another project.

The layout adapts to terminal size. Below the configured compact-width safety
guard, or whenever a wide task/settings control is actually clipped, the task
inbox becomes a short full-width panel, the main workspace stacks vertically,
and the task toolbar's project and action controls remain available without
clipping. The wide settings row is replaced by a category and value picker
covering provider, model, reasoning, mode, topic, and operating branch. Short
terminals also use a smaller prompt and reduced vertical chrome. Tune these
defaults in the `[layout]` table of
`parameter_files/daedalus-tui.toml` (`compact_width`, `short_height`,
`compact_task_sidebar_height`, and `compact_prompt_height`).

## Providers and sign-in

Three providers are available: Codex (`codex`), Claude Code (`claude`), and
Cursor CLI (`agent`). Each provider's models and effort levels live in
`parameter_files/daedalus-tui.toml`; Claude Code has its own effort scale that
adds `max`, and Cursor is a provider-only choice with model and reasoning
disabled. Claude Code runs with `--permission-mode acceptEdits`, so it edits
files without prompting while orchestration still runs verification itself. Set
`[claude] permission_mode = "bypassPermissions"` if you want it to run commands
too; that grants autonomy comparable to Codex but without Codex's sandbox.

By default the TUI runs agents on your **signed-in account** rather than an API
key, so work bills your plan. In this mode it removes each provider's API-key
variables (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`,
`CURSOR_API_KEY`) from the agent subprocess environment, and a local `.env`
cannot put them back. Sign in once from your own terminal:

```bash
claude auth login
codex login
agent login
```

The task bar's **Sign In** control reports the selected provider's status and
repeats the exact command to run. The TUI does not host the login itself,
because an interactive CLI that takes over the terminal would hide the
interface.

To go back to key-based execution, set `mode = "api-key"` in the `[auth]` table
of `parameter_files/daedalus-tui.toml`. Cursor then reads `CURSOR_API_KEY` from
the process environment or a local `.env`:

```bash
cp .env.example .env
# edit .env and set CURSOR_API_KEY=...
```

API keys never belong in a parameter file; those tables list variable names
only.

## Project backends

New Project and the task bar's **Register Backend** control scaffold a backend
into a project: **Firebase** (`firebase.json`, deny-by-default
`firestore.rules`, `firestore.indexes.json`, `storage.rules`) or a **personal
Supabase** schema. Firebase is the default for new projects; change
`default_backend` in
`parameter_files/daedalus-tui-project-initialization.toml` to pick another.

Registration writes files only. After verification passes, orchestration
deploys changed Firestore rules and indexes with
`firebase deploy --only firestore:rules,firestore:indexes --non-interactive`,
and pushes pending Supabase migrations, repairing failures with the coding
agent before integration proceeds. Agents never run either command themselves.
Tune the deploy in `parameter_files/daedalus-tui-firebase.toml` and disable it
with `firebase_deploy_enabled = false` in the orchestration parameter file.

Each prompt creates an independent local Git worktree based on the configured
`target_branch` (default `main`; `primary_branch` remains accepted as an
alias), runs the selected agent (Codex, Claude Code, or Cursor) there, verifies
the result, resolves integration
failures with the selected agent, and fast-forwards that target branch after
successful checks. The operator does not need the target branch checked out.
Up to four prompts can run concurrently; integration and promotion remain
serialized. Automated orchestration never pushes remotes; use the settings-bar
Push control when you want to publish the selected operating branch to
`origin`. Failed worktrees are preserved
for inspection. After a successful promotion, the orchestrator refreshes and
commits `graphify-out` onto the target branch when the target repository has
graphify configured; graph refresh failures are reported as warnings and never
trigger resolver attempts.

Target projects may add an optional `.daedalus` TOML file to prepare each task
worktree before the agent starts. The `[worktree]` table accepts one argv-style
`install_command` and repository-relative `readonly_paths`; the command runs in
the task worktree, then each declared path is symlinked from the primary
worktree. For example:

```toml
[worktree]
install_command = ["npm", "ci"]
readonly_paths = ["food-data"]
```

Symlinked paths are shared local resources and are not OS-enforced read-only;
agents and setup commands must treat them as immutable.

The launch root stores task history in `.daedalus-memory.json`. Its `tasks`
entry maps each task worktree directory name to the submission timestamp,
prompt, provider/model/reasoning/mode selection, current state, assistant
outputs, token usage, resolved project path, and any error so failed, paused,
and cancelled work can be reopened for analysis. Failed tasks and tasks
interrupted by a TUI restart are rehydrated into the task inbox; failed tasks
can be retried and interrupted tasks can be resumed when their worktrees still
exist. The memory file also keeps a single `last_opened_project` entry.
Plan tasks with submitted answers additionally retain generated review requests
in an optional `prompt_history` list on the same worktree record.
Runtime diagnostics are written to `.daedalus-debug.log` next to that memory
file (rotated at 2 MB). It records UI exceptions, task/agent lifecycle events,
and shutdown state. During Python exit it cancels active agent process groups
before the executor can block on their worker threads. If the process is
stuck, run `kill -USR1 <pid>` to append all Python thread stacks to the same
log before terminating it; this command writes only to the log by design.
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

Use the mode selector for Coding, Ask, or Plan, or press `Tab` on the main
prompting screen to toggle between Coding and Plan. Ask runs are read-only and do
not promote file changes. Plan runs are read-only and remain selectable in the
task list through their `planning`, `questioning`, and answer-review states.
They return a structured implementation plan and multiple-choice questions;
submit selected answers for another review round, or use the follow-up
controls to continue planning. The Implement button remains unavailable until
the agent confirms that no questions remain, then creates a separate coding
task from the approved plan. Pause preserves the task worktree and allows
resume later; Cancel stops the agent and removes that task's worktree and
branch.

Optional Topics group closely related tasks under shared markdown in
`topic_files/` (Topic Goal, Topic Status, State Log). Create or edit those
files outside the TUI; the wide settings row and compact settings picker both
list existing stems and default to `(None)`. When tagged, coding/plan/ask
prompts embed the topic
plus usage instructions; coding tasks may append the topic State Log the same
way they update feature files.

When resuming, the optional notes field is sent to the agent only when it has
content. The resume prompt tells the agent to preserve existing work, inspect
`git status` and `git diff`, and continue from the current worktree.
