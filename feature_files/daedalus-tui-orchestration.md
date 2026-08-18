# Daedalus TUI Local Orchestration

## Summary
The standalone TUI orchestration layer creates isolated Git worktrees, runs a selected local agent, verifies its changes, resolves integration failures, and promotes successful task branches into the local primary branch.

## Key Points
- **Worktree isolation**: Each task receives an `agent/task-<id>` branch and a sibling `.daedalus-worktrees` directory.
- **Verification repair**: Failed task checks launch repair attempts in the same worktree up to the configured limit.
- **Resolver fallback**: Merge conflicts and post-merge verification failures launch the selected provider as a resolver with the latest failure details.
- **Safe promotion**: The primary branch must remain clean, checked out, and unchanged before fast-forward promotion; failed worktrees remain available for inspection.
- **Concurrent integration**: Up to four task agents and their verification runs execute concurrently, then ready tasks pass through a first-ready serialized integration gate before promotion.
- **Connectivity recovery**: Agent subprocesses have a bounded timeout, report actionable offline/service diagnostics, and failed requests can be retried without losing their task context.
- **Agent Git boundary**: Task, repair, and resolver agents edit files only; the orchestration layer owns staging, commits, merges, and cleanup.
- **Graph refresh boundary**: Graphify runs only after successful primary promotion, and a failed refresh is cleaned up and reported without starting a resolver.
- **Local-only boundary**: No persistence, daemon communications, Supabase deployment, migration handling, or remote Git push is included.
- **Project-scoped execution**: The TUI creates one coordinator per discovered `feature_files` project, so task numbering, worktrees, branches, and integration gates stay scoped to the selected repository.
- **Shutdown diagnostics**: A rotating project-local debug log records agent process IDs, task transitions, Textual exceptions, worker shutdown, and on-demand all-thread stack dumps.

## Relevant Files
- `tui/orchestrator.py`: Single-task lifecycle, verification repair, integration, and resolver loops.
- `tui/task_coordinator.py`: Concurrent task records, executor limit, and serialized integration gate.
- `tui/git_worktree.py`: Git validation, worktree, branch, merge, and cleanup operations.
- `tui/verification.py`: Configured and convention-based verification execution.
- `parameter_files/daedalus-tui-orchestration.toml`: Local branch, worktree, verification, and retry settings.

## Dev Mode
HACKING

## State Log
- 2026-08-14: Added independent worktree, verification, merge, and resolver orchestration without daemon or cloud communication dependencies.
- 2026-08-14: Added bounded multi-task execution with first-ready serialized promotion and explicit orchestration ownership of all Git operations.
- 2026-08-14: Hardened successful worktree removal so committed tasks clean up even when agent tooling leaves untracked artifacts behind.
- 2026-08-14: Passed target-repository environment files into isolated Cursor tasks while preserving process-level credential precedence.
- 2026-08-14: Added cooperative subprocess stopping with preserved paused worktrees and force-cleaned cancelled task branches.
- 2026-08-14: Passed accumulated resume notes into continued task runs without changing the independent worktree lifecycle.
- 2026-08-14: Kept orchestration transcripts available for Vim selection yanks without changing task execution or integration behavior.
- 2026-08-17: Staged resolver worktree changes before checking for unmerged paths so file-only conflict resolutions are recognized by the orchestration layer.
- 2026-08-14: Moved graph refreshes into a best-effort post-promotion hook and discarded accidental task-worktree graph output before orchestration commits.
- 2026-08-14: Connected orchestration to recursively discovered project roots while preserving independent task state when the sidebar changes projects.
- 2026-08-17: Added bounded agent execution timeouts and retryable failed tasks so network outages do not leave executor threads hanging or discard the plan context.
- 2026-08-17: Made shutdown detach callbacks, wait for cancellable executor work, and bound subprocess pipe-reader joins so closed TUI sessions do not linger in Python thread shutdown.
- 2026-08-17: Terminated complete agent process groups on cancellation, bounded the app shutdown grace period, and added persistent debug logging plus `SIGUSR1` all-thread dumps for stuck workers.
- 2026-08-17: Isolated non-interactive agent stdin from the Textual terminal and added an idempotent atexit shutdown guard plus asyncio failure logging for UI exits that bypass normal unmount.
- 2026-08-17: Preserved mounted plan-answer selectors while answer confirmation is queued, and moved unexpected-exit cleanup ahead of Python's executor-thread join.
- 2026-08-17: Persisted queued task snapshots before worker submission so fast completions cannot be overwritten by stale queued state, including retries.
- 2026-08-17: Hardened plan-confirmation handoff against invalid or revised agent payloads, retained recoverable answers, and removed the clean planning worktree once implementation is queued.
- 2026-08-17: Extended agent inactivity timeouts to 450 seconds and refreshed them for every stdout update so long-running tasks remain connected while the agent is making progress.
