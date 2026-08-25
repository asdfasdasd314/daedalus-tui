# Execution Boundaries (CRITICAL)

- NEVER EXECUTE SOURCE CODE (python, bash, node, script tasks) without
  explicit standalone user permission in the current turn. Scrapers, tests,
  skill plugins (including Graphify), research, and directory listing are
  permitted.
- NEVER implement CLI/Command Line Arguments (`--input`, `--mode`). Hardcode
  configurations directly into variables for manual tweaking.

# Planning Boundaries

- Use feature files and Graphify to understand the project before proposing
  work.
- Feature files and parameter files are read-only during planning.
- Keep plans within the TUI's standalone project boundary; do not assume
  access to the parent Daedalus daemon, site, database, or Supabase.
- Do not implement code in planning mode.

# Feature File Context

Feature files describe why behavior exists; Graphify describes where it exists.
Features own only the logic, configuration, and behavior they directly
implement. Cross-feature references should describe interfaces rather than
duplicate dependency internals.

Feature files use this schema: H1 title, `## Summary`, `## Key Points`,
`## Relevant Files`, `## Dev Mode`, and `## State Log`.

# Topics (when tagged)

Optional `topic_files/` markdown provides shared umbrella context (goal,
status, state log) across related features. Use an embedded topic for
planning context only; do not modify topic files in planning mode. Feature
files and parameter files remain read-only during planning as well.

# Parameter Files

Each feature file has a paired `.toml` file in `parameter_files/`. Treat these
files as read-only sources of tunable configuration. Never put API keys in
them, and do not move fixed implementation constants there without a tuning
need.

# Graphify

For broad architecture review use `graphify-out/GRAPH_REPORT.md`; for focused
questions use `graphify query`, `graphify path`, or `graphify explain` when the
graph exists. After code changes, the implementing task should run
`graphify update .`.
