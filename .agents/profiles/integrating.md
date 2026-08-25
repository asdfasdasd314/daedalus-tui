# Execution Boundaries (CRITICAL)

- NEVER EXECUTE SOURCE CODE (python, bash, node, script tasks) without
  explicit standalone user permission in the current turn. Scrapers, tests,
  skill plugins (including Graphify), research, and directory listing are
  permitted.
- NEVER implement CLI/Command Line Arguments (`--input`, `--mode`). Hardcode
  configurations directly into variables for manual tweaking.

# Integration Boundaries

- In integration mode, focus on resolving conflicts in feature and parameter
  files while preserving both relevant changes where possible.
- Keep the TUI standalone; do not pull in parent Daedalus daemon or site
  dependencies.
- The orchestration layer owns staging, commits, merges, worktree cleanup, and
  graph refreshes.
- Feature files and parameter files describe the currently integrated project
  state; do not use integration mode to invent new feature requirements.
- Concurrent topic State Log appends can race like concurrent feature-file
  edits; prefer preserving both relevant topic entries when resolving
  conflicts.

# Parameter Files

Parameter files are read-only sources of tunable configuration. Keep a
parameter with the feature that owns its behavior, and never put API keys in
one.

# Development Lifecycle

The four stages are HACKING, TESTING, PRODUCTION-READY, and DEBUGGING. In
general, prefer moving quickly and do not autonomously upgrade a feature's
stage.
