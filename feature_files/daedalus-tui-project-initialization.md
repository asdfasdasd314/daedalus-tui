# Daedalus TUI Project Initialization

## Summary
The TUI can initialize a new Daedalus-compatible project under the launch root by materializing bundled templates (AGENTS.md, agent profiles, feature/parameter directories, README, and gitignore), installing Graphify hooks, creating the initial Git commit, and optionally creating a private GitHub repository.

## Key Points
- **Launch-root destination**: The user supplies only a project slug and optional GitHub opt-in; the destination is always a direct child of the TUI launch root.
- **Template copy**: Initializer-owned files under `tui/templates/project-initializer/` are copied into an atomic temporary sibling, then renamed into place.
- **Recoverable requests**: A `.git/daedalus-initialization-request-id` marker lets retries recognize initializer-owned projects without overwriting unrelated directories.
- **Local by default**: Graphify install and Git init/commit always run; GitHub creation is optional and private.
- **Discovery refresh**: After success, the TUI rediscovers `feature_files` projects and switches to the new project.

## Relevant Files
- `tui/project_initializer.py`: Validation, template materialization, command steps, cleanup, and result construction.
- `tui/templates/project-initializer/`: Base Daedalus project assets copied into new projects.
- `tui/app.py`: New Project modal and post-init project list refresh.
- `parameter_files/daedalus-tui-project-initialization.toml`: Initializer-owned settings.
- `tests/test_project_initializer.py`: Unit coverage for validation and initialization flows.

## Dev Mode
HACKING

## State Log
- 2026-08-23: Ported daemon project initialization into the standalone TUI with bundled templates and a New Project modal under the launch root.
