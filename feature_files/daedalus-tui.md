# Daedalus Textual TUI

## Summary
The standalone Daedalus TUI is an installable Textual application that runs from a target repository and submits independent local, orchestrated coding tasks concurrently.

## Key Points
- **Independent project boundary**: The exported `tui` project owns its UI, provider execution, configuration, tests, and local orchestration modules without importing `local-daemon`.
- **Provider controls**: Codex exposes Luna, Terra, and Sol with light, medium,
  high, and extra-high reasoning; Cursor CLI is a provider-only choice with
  model and reasoning disabled. The settings bar also exposes a per-project
  Branch Select for the operating branch used by new task worktrees.
- **Local execution**: Prompts run in isolated Git worktrees and never use Supabase, daemon RPC, a database, or a remote push.
- **Concurrent task inbox**: Up to four independent prompts can run at once, each with its own configuration snapshot, branch, worktree, status, and transcript; the left-side inbox promotes tasks with unseen updates.
- **Plan-first task route**: Plan tasks remain selectable through `planning` and `questioning` states, support follow-up planning passes, and can promote their preserved context into the normal coding, verification, and integration route.
- **Plan custom answers**: Plan review renders a software-owned custom-answer choice alongside the agent's reasonable options and collects free text only when that choice is selected; the agent protocol remains unchanged.
- **Filtered logs and copying**: The output pane uses Textual's selectable `Log` widget for completed assistant messages; Vim yank commands copy selected transcript or diagnostic text to the system clipboard.
- **Readable streamed output**: Assistant messages are separated by a blank line, and transcript lines are reflowed to the output pane width so long responses remain visible.
- **Incremental Vim input**: The prompt uses a modal VimTextArea with a practical command subset; additional Vim commands can be added as they become useful instead of implementing the entire Vim language up front.
- **Project selection**: Launching from a root directory recursively discovers supported projects by their `feature_files` folders; the task toolbar selects the project for new submissions, editable prompt drafts survive project switches, and focusing an inbox row synchronizes the active project without mixing transcripts or worktrees. Each project's remembered operating branch is restored independently when focus returns.
- **Project initialization**: New Project materializes bundled Daedalus templates under the launch root, runs Graphify/Git setup, optionally creates a private GitHub repo, then refreshes discovery onto the new project.
- **Actionable task history**: The task inbox keeps every failed task, active or paused work, and all tasks from the current TUI session while hiding older completed, blocked, and cancelled tasks.
- **Retryable failures**: Failed agent tasks expose their diagnostics and a Retry action so transient connectivity or service failures can be recovered in place.

## Relevant Files
- `tui/app.py`: Textual layout, selectors, task list, transcript replay, and task controls.
- `tui/plan.py`: Agent plan parsing plus UI-owned custom-answer encoding and prompt formatting.
- `tui/vim_text_area.py`: Incremental modal Vim prompt adapter and system clipboard integration.
- `tui/agent_runner.py`: Independent Codex and Cursor subprocess adapter.
- `tui/task_coordinator.py`: Concurrent task executor and serialized integration gate.
- `parameter_files/daedalus-tui.toml`: Provider, model, reasoning, and default UI settings.
- `feature_files/daedalus-tui-orchestration.md`: Local orchestration ownership boundary.
- `feature_files/daedalus-tui-project-initialization.md`: Launch-root project scaffolding.
- `tests/test_plan.py`, `tests/test_app.py`, `tests/test_task_coordinator.py`: Coverage for custom-answer rendering, validation, and follow-up handoff.

## Dev Mode
HACKING

## State Log
- 2026-08-23: Added a settings-bar Branch Select that remembers each project's operating branch in launch-root memory and applies it to new task worktrees only.
- 2026-08-14: Moved the TUI feature ownership into the standalone project boundary and expanded provider/model/reasoning controls for local orchestration.
- 2026-08-14: Added concurrent task snapshots, assistant-message filtering, selectable transcript replay, and copy-all output for independent worktrees.
- 2026-08-14: Made failed diagnostics selectable and copyable, added Cursor failure guidance, and hardened successful worktree cleanup.
- 2026-08-14: Added ignored local Cursor credential loading and a native clipboard fallback for terminals without OSC 52 support.
- 2026-08-14: Added Coding, Ask, and Plan mode controls plus per-task pause, resume, and cancellation actions.
- 2026-08-14: Added optional per-resume notes and a continuation prompt that directs agents to inspect existing work before making updates.
- 2026-08-14: Routed Textual selection copies through the native clipboard fallback and added an explicit partial-output copy action.
- 2026-08-14: Clarified that task agents edit files only while orchestration owns Git operations and graph refreshes.
- 2026-08-14: Enabled global Textual selection copying for arbitrary UI text while preserving native TextArea selection and terminal modifier guidance.
- 2026-08-14: Added non-modal Vim-style output navigation and system clipboard y/p shortcuts without intercepting prompt editor typing.
- 2026-08-14: Added a modal VimTextArea prompt with multiline Insert mode, Normal/Visual commands, system clipboard yank/paste, and an intentionally incremental command subset for future additions.
- 2026-08-14: Removed Vim status and shortcut hints from the rendered interface and added Shift+V whole-line visual selection to the prompt editor.
- 2026-08-14: Added recursive Daedalus project discovery from the launch root and a sidebar that preserves independent task coordinators for each supported project.
- 2026-08-16: Removed copy buttons and dedicated full-output/error copy actions in favor of Vim yank commands.
- 2026-08-16: Added standalone `AGENTS.md` and task-mode profiles so the TUI retains its operating instructions when moved into its own repository.
- 2026-08-16: Preserved submitted prompts in an immutable task view and added an explicit New Task action to unlock a blank prompt editor.
- 2026-08-16: Switched the output pane from RichLog to Log so transcript text supports click-drag selection and yank without editing.
- 2026-08-16: Kept task selection user-controlled during background events and streamed Cursor assistant deltas into the live transcript.
- 2026-08-17: Matched selectable output highlighting to the prompt selection colors so selected transcript characters remain readable.
- 2026-08-17: Added prompt `yy` coverage, reliable `e` word-end progression, Escape selection clearing, and a steady underline-style insert cursor.
- 2026-08-17: Added quieter progress-message text, a brighter final assistant summary, and faded styling for immutable submitted prompts.
- 2026-08-17: Switched the insert caret to a thin white bar, used an underline while yank is pending, and mapped `$` to line-end in command mode.
- 2026-08-17: Resolved the final transcript color through Textual before passing it to Rich, avoiding invalid `auto` CSS colors during pointer rendering.
- 2026-08-17: Kept the insert caret between characters so rendering a middle-of-line prompt does not hide the text to its right.
- 2026-08-17: Fixed insert caret rendering by splitting the full Textual strip at the cursor position and drawing a visible one-cell vertical bar.
- 2026-08-17: Used a left-aligned thin block for the insert caret so it sits on the left edge of the character cell at the insertion point.
- 2026-08-17: Kept Plan tasks selectable through a planning/questioning loop with follow-up controls, structured plan/questions review, and an explicit transition into coding.
- 2026-08-17: Made asynchronous plan-question rendering generation-safe and non-fatal so streamed completion events cannot close the TUI before the review controls appear.
- 2026-08-17: Suppressed Textual's inherited Select mount handler for dynamic plan answers, preventing a race where SelectCurrent lacked its internal `#label` node during initialization.
- 2026-08-17: Added visible retry controls for failed agent requests and preserved the last request prompt for connectivity recovery.
- 2026-08-17: Included the visible AI transcript from failed attempts in retry context while relying on the existing worktree diff for file-change state.
- 2026-08-17: Deferred dynamic plan Select initialization until after Textual's nested SelectCurrent label is mounted, preventing a lifecycle race from terminating the TUI.
- 2026-08-17: Detached task callbacks before coordinator shutdown, waited for executor workers to finish, and ignored late events after Textual closes.
- 2026-08-17: Replaced the insert caret's rendered cell instead of adding one, so middle-of-line text no longer shifts while the prompt document stays unchanged.
- 2026-08-17: Let Textual underline the real insert cursor cell with no background override so the character beneath the caret remains visible without a dark box.
- 2026-08-17: Disabled Textual's dark active-line highlight for the Vim prompt because it remained underneath the transparent cursor cell.
- 2026-08-17: Replaced project-focused sidebar navigation with a cross-project task update inbox, moved project selection into the task toolbar, and made task focus synchronize the active project context.
- 2026-08-17: Validated the toolbar project at submission time so a newly selected project receives the draft even before its queued selector event is processed.
- 2026-08-17: Limited task-update inbox promotion to completed or failed tasks and plan questions, leaving streaming progress events out of the update queue.
- 2026-08-17: Made task diagnostics use the selectable output-log surface so error text supports mouse selection, Vim yanks, and Ctrl+C copying.
- 2026-08-17: Made confirmed plan implementation a one-shot action and visibly faded the Implement button after it queues coding.
- 2026-08-20: Added a UI-owned Custom answer choice to plan questions, with conditional free-text input and encoded follow-up handoff that leaves agent-generated options unchanged.
- 2026-08-20: Filtered the task inbox to failed history, active work, and tasks from the current TUI session, while preserving visibility when an older task is resumed or retried.
- 2026-08-23: Added blank-line separation between streamed assistant messages and width-aware transcript wrapping that reflows when the terminal is resized.
- 2026-08-23: Updated final-tone verification to locate the final message after width-aware wrapping rather than assuming a fixed physical line index.
- 2026-08-23: Wrapped transcript lines to the output Log's content region so border and padding remain clear, with resize coverage for reflow.
- 2026-08-23: Reflowed cached transcript lines during rendering when a style width change does not emit a resize event.
- 2026-08-23: Used an explicit cell width immediately during transcript reflow so direct output width updates are reflected before the next layout pass.
- 2026-08-23: Accounted for border-box gutters when using an explicit output width, keeping wrapped text inside the Log content area.
- 2026-08-23: Folded transcript messages by cell width so constrained output panes visibly reflow on narrow resize changes without crossing the content boundary.
- 2026-08-23: Linked New Project initialization so launch-root scaffolding refreshes the discovered project list.
- 2026-08-23: Preserved editable prompt drafts across toolbar project switches so a mis-targeted draft can be redirected instead of erased.
