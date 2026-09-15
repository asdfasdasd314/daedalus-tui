"""Read-only configuration for the standalone TUI."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import tomllib

from .agent_runner import ProviderAuthPolicy
from .orchestrator import OrchestrationSettings


AUTH_MODES = frozenset({"account", "api-key"})
CLAUDE_PERMISSION_MODES = frozenset(
    {"acceptEdits", "auto", "bypassPermissions", "manual", "dontAsk", "plan"}
)

PARAMETER_DIRECTORY = "parameter_files"
TUI_PARAMETER_FILE = "daedalus-tui.toml"
ORCHESTRATION_PARAMETER_FILE = "daedalus-tui-orchestration.toml"
CODING_STATISTICS_PARAMETER_FILE = "daedalus-tui-coding-statistics.toml"


@dataclass(frozen=True)
class ModelOption:
    label: str
    value: str


@dataclass(frozen=True)
class ClaudeSettings:
    """Non-interactive execution settings for the Claude Code provider."""

    permission_mode: str = "acceptEdits"


@dataclass(frozen=True)
class ProviderAuthSettings:
    """Sign-in metadata for one provider CLI.

    ``api_key_variables`` names the environment variables that make the CLI bill
    API credit instead of the operator's plan; account mode removes them from the
    agent subprocess environment. Only variable names live here, never keys.
    """

    label: str
    api_key_variables: tuple[str, ...] = ()
    status_command: tuple[str, ...] = ()
    sign_in_command: tuple[str, ...] = ()


@dataclass(frozen=True)
class AuthSettings:
    """Whether agents run from a signed-in account or from API keys."""

    mode: str = "account"
    providers: dict[str, ProviderAuthSettings] = field(default_factory=dict)

    @property
    def uses_account_login(self) -> bool:
        return self.mode == "account"

    def for_provider(self, provider: str) -> ProviderAuthSettings:
        return self.providers.get(provider, ProviderAuthSettings(provider))

    def runner_policy(self) -> ProviderAuthPolicy:
        """Return the API-key stripping policy the agent runner applies."""
        return ProviderAuthPolicy(
            account_login=self.uses_account_login,
            api_key_variables={
                name: settings.api_key_variables for name, settings in self.providers.items()
            },
        )


@dataclass(frozen=True)
class ProjectDiscoverySettings:
    """Which immediate launch-root children appear in the project selector."""

    include_git_repositories: bool = True
    include_all_directories: bool = False
    skipped_directory_names: frozenset[str] = frozenset(
        {".git", ".daedalus-worktrees", ".venv", "__pycache__", "node_modules"}
    )


@dataclass(frozen=True)
class LayoutSettings:
    """Safety guard and dimensions used by the responsive TUI.

    The wide controls are measured against their laid-out regions above this
    width; the guard keeps very narrow terminals in compact mode while those
    regions are not usable yet. Settings selectors below ``wide_control_min_width``
    use the compact category/value picker instead of shrinking into unreadable
    controls.
    """

    compact_width: int = 100
    short_height: int = 32
    compact_task_sidebar_height: int = 8
    compact_prompt_height: int = 4
    wide_control_min_width: int = 13


@dataclass(frozen=True)
class TuiSettings:
    default_provider: str
    default_model: str
    default_reasoning: str
    providers: tuple[ModelOption, ...]
    codex_models: tuple[ModelOption, ...]
    codex_reasoning: tuple[ModelOption, ...]
    cursor_model: ModelOption
    claude_models: tuple[ModelOption, ...] = ()
    claude_reasoning: tuple[ModelOption, ...] = ()
    modes: tuple[ModelOption, ...] = (
        ModelOption("Coding", "coding"),
        ModelOption("Ask", "ask"),
        ModelOption("Plan", "plan"),
    )
    output_width: str = "95%"
    # Content widths for the four task-inbox columns, excluding DataTable
    # cell padding. The defaults leave a cell for the sidebar scrollbar.
    task_inbox_widths: tuple[int, int, int, int] = (1, 9, 14, 7)
    layout: LayoutSettings = LayoutSettings()
    claude: ClaudeSettings = ClaudeSettings()
    auth: AuthSettings = AuthSettings()
    project_discovery: ProjectDiscoverySettings = ProjectDiscoverySettings()

    def models_for(self, provider: str) -> tuple[ModelOption, ...]:
        """Return the model choices a provider exposes in the settings bar."""
        if provider == "cursor":
            return (self.cursor_model,)
        if provider == "claude":
            return self.claude_models
        return self.codex_models

    def reasoning_for(self, provider: str) -> tuple[ModelOption, ...]:
        """Return the reasoning/effort choices a provider exposes, if any."""
        if provider == "cursor":
            return ()
        if provider == "claude":
            return self.claude_reasoning
        return self.codex_reasoning

    def default_model_for(self, provider: str) -> str:
        """Return the model preselected when switching to ``provider``."""
        options = self.models_for(provider)
        if any(option.value == self.default_model for option in options):
            return self.default_model
        return options[0].value if options else ""

    def default_reasoning_for(self, provider: str) -> str:
        """Return the reasoning preselected when switching to ``provider``."""
        options = self.reasoning_for(provider)
        if any(option.value == self.default_reasoning for option in options):
            return self.default_reasoning
        return options[0].value if options else ""


@dataclass(frozen=True)
class CodingStatisticsSettings:
    recent_window_hours: int = 1
    forecast_days: int = 7
    thirty_day_forecast_days: int = 30


def load_tui_settings(parameter_path: Path | None = None) -> TuiSettings:
    path = parameter_path or (Path(__file__).resolve().parents[1] / PARAMETER_DIRECTORY / TUI_PARAMETER_FILE)
    with path.open("rb") as source:
        values = tomllib.load(source)

    defaults = values.get("defaults", {})
    providers = tuple(_options(values.get("providers", []), "provider"))
    codex_models = tuple(_options(values.get("codex_models", []), "model"))
    codex_reasoning = tuple(_options(values.get("codex_reasoning", []), "reasoning"))
    cursor_values = values.get("cursor", {})
    cursor_model = ModelOption(str(cursor_values.get("label", "Cursor CLI")), str(cursor_values.get("value", "cursor")))
    claude_models = tuple(_options(values.get("claude_models", []), "model"))
    claude_reasoning = tuple(_options(values.get("claude_reasoning", []), "reasoning"))
    modes = tuple(_options(values.get("modes", []), "mode")) or TuiSettings.modes
    output = values.get("output", {})
    output_width = str(output.get("width", "95%"))
    task_inbox = values.get("task_inbox", {})
    task_inbox_widths = tuple(
        int(task_inbox.get(name, default))
        for name, default in (
            ("marker_width", 1),
            ("project_width", 9),
            ("task_width", 14),
            ("status_width", 7),
        )
    )
    if any(width < 1 for width in task_inbox_widths):
        raise ValueError(f"{path} task_inbox widths must be positive.")

    layout_values = values.get("layout", {})
    layout = LayoutSettings(
        compact_width=int(layout_values.get("compact_width", 100)),
        short_height=int(layout_values.get("short_height", 32)),
        compact_task_sidebar_height=int(layout_values.get("compact_task_sidebar_height", 8)),
        compact_prompt_height=int(layout_values.get("compact_prompt_height", 4)),
        wide_control_min_width=int(layout_values.get("wide_control_min_width", 14)),
    )
    if any(value < 1 for value in (
        layout.compact_width,
        layout.wide_control_min_width,
        layout.short_height,
        layout.compact_task_sidebar_height,
        layout.compact_prompt_height,
    )):
        raise ValueError(f"{path} layout values must be positive.")

    default_provider = str(defaults.get("provider", "codex"))
    default_model = str(defaults.get("model", "gpt-5.6-luna"))
    default_reasoning = str(defaults.get("reasoning", "high"))
    if not providers or not codex_models or not codex_reasoning:
        raise ValueError(f"{path} must define providers, codex_models, and codex_reasoning.")
    if any(option.value == "claude" for option in providers) and not claude_models:
        raise ValueError(f"{path} lists the claude provider but defines no claude_models.")

    claude_values = values.get("claude", {})
    claude = ClaudeSettings(permission_mode=str(claude_values.get("permission_mode", "acceptEdits")))
    if claude.permission_mode not in CLAUDE_PERMISSION_MODES:
        raise ValueError(
            f"{path} claude.permission_mode must be one of {sorted(CLAUDE_PERMISSION_MODES)}."
        )

    auth = _auth_settings(values.get("auth", {}), path)
    project_discovery = _project_discovery_settings(values.get("projects", {}), path)
    return TuiSettings(
        default_provider,
        default_model,
        default_reasoning,
        providers,
        codex_models,
        codex_reasoning,
        cursor_model,
        claude_models,
        claude_reasoning,
        modes,
        output_width,
        task_inbox_widths,
        layout,
        claude,
        auth,
        project_discovery,
    )


def _auth_settings(values: object, path: Path) -> AuthSettings:
    """Build provider sign-in settings, rejecting literal keys in the file."""
    if not isinstance(values, dict):
        raise ValueError(f"{path} auth must be a table.")
    mode = str(values.get("mode", "account"))
    if mode not in AUTH_MODES:
        raise ValueError(f"{path} auth.mode must be one of {sorted(AUTH_MODES)}.")

    providers: dict[str, ProviderAuthSettings] = {}
    for name, table in values.items():
        if name == "mode":
            continue
        if not isinstance(table, dict):
            raise ValueError(f"{path} auth.{name} must be a table.")
        variables = _string_tuple(table.get("api_key_variables", []), path, f"auth.{name}.api_key_variables")
        for variable in variables:
            # The parameter file names variables; a value here would be a key.
            if "=" in variable or len(variable) > 64:
                raise ValueError(
                    f"{path} auth.{name}.api_key_variables must contain variable names, not values."
                )
        providers[name] = ProviderAuthSettings(
            label=str(table.get("label", name)),
            api_key_variables=variables,
            status_command=_string_tuple(table.get("status_command", []), path, f"auth.{name}.status_command"),
            sign_in_command=_string_tuple(table.get("sign_in_command", []), path, f"auth.{name}.sign_in_command"),
        )
    return AuthSettings(mode=mode, providers=providers)


def _project_discovery_settings(values: object, path: Path) -> ProjectDiscoverySettings:
    if not isinstance(values, dict):
        raise ValueError(f"{path} projects must be a table.")
    skipped = _string_tuple(
        values.get("skipped_directory_names", list(ProjectDiscoverySettings().skipped_directory_names)),
        path,
        "projects.skipped_directory_names",
    )
    return ProjectDiscoverySettings(
        include_git_repositories=bool(values.get("include_git_repositories", True)),
        include_all_directories=bool(values.get("include_all_directories", False)),
        skipped_directory_names=frozenset(skipped),
    )


def _string_tuple(value: object, path: Path, key: str) -> tuple[str, ...]:
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        raise ValueError(f"{path} {key} must be an array of non-empty strings.")
    return tuple(value)


def load_orchestration_settings(parameter_path: Path | None = None) -> OrchestrationSettings:
    path = parameter_path or (Path(__file__).resolve().parents[1] / PARAMETER_DIRECTORY / ORCHESTRATION_PARAMETER_FILE)
    with path.open("rb") as source:
        values = tomllib.load(source)
    commands = values.get("verification_commands", [])
    if not isinstance(commands, list):
        raise ValueError(f"{path} verification_commands must be an array.")
    normalized = []
    for command in commands:
        if not isinstance(command, list) or not command or any(not isinstance(item, str) for item in command):
            raise ValueError(f"{path} verification_commands must contain non-empty string arrays.")
        normalized.append(tuple(command))
    max_concurrent_tasks = int(values.get("max_concurrent_tasks", 4))
    if max_concurrent_tasks < 1:
        raise ValueError(f"{path} max_concurrent_tasks must be positive.")
    agent_timeout_seconds = float(values.get("agent_timeout_seconds", 450))
    if agent_timeout_seconds <= 0:
        raise ValueError(f"{path} agent_timeout_seconds must be positive.")
    shutdown_grace_seconds = float(values.get("shutdown_grace_seconds", 8))
    if shutdown_grace_seconds <= 0:
        raise ValueError(f"{path} shutdown_grace_seconds must be positive.")
    # target_branch is preferred; primary_branch remains as a compatibility alias.
    target_branch = values.get("target_branch", values.get("primary_branch", "main"))
    return OrchestrationSettings(
        primary_branch=str(target_branch),
        worktree_root=str(values.get("worktree_root", ".daedalus-worktrees")),

        verification_commands=tuple(normalized),
        task_verification_attempt_limit=int(values.get("task_verification_attempt_limit", 3)),
        resolver_attempt_limit=int(values.get("resolver_attempt_limit", 3)),
        max_concurrent_tasks=max_concurrent_tasks,
        agent_timeout_seconds=agent_timeout_seconds,
        graphify_update_enabled=bool(values.get("graphify_update_enabled", True)),
        graphify_executable=str(values.get("graphify_executable", "graphify")),
        supabase_db_push_enabled=bool(values.get("supabase_db_push_enabled", True)),
        supabase_executable=str(values.get("supabase_executable", "supabase")),
        firebase_deploy_enabled=bool(values.get("firebase_deploy_enabled", True)),
        firebase_executable=str(values.get("firebase_executable", "firebase")),
        shutdown_grace_seconds=shutdown_grace_seconds,
        debug_log_filename=str(values.get("debug_log_filename", ".daedalus-debug.log")),
    )


def load_coding_statistics_settings(parameter_path: Path | None = None) -> CodingStatisticsSettings:
    path = parameter_path or (
        Path(__file__).resolve().parents[1] / PARAMETER_DIRECTORY / CODING_STATISTICS_PARAMETER_FILE
    )
    with path.open("rb") as source:
        values = tomllib.load(source)
    recent_window_hours = int(values.get("recent_window_hours", 1))
    forecast_days = int(values.get("forecast_days", 7))
    thirty_day_forecast_days = int(values.get("thirty_day_forecast_days", 30))
    if recent_window_hours < 1 or forecast_days < 1 or thirty_day_forecast_days < 1:
        raise ValueError(
            f"{path} recent_window_hours, forecast_days, and thirty_day_forecast_days must be positive."
        )
    return CodingStatisticsSettings(recent_window_hours, forecast_days, thirty_day_forecast_days)


def _options(items, kind: str) -> list[ModelOption]:
    options = []
    for item in items:
        if not isinstance(item, dict):
            continue
        options.append(ModelOption(str(item.get("label", item.get("value", ""))), str(item.get("value", ""))))
    return [option for option in options if option.value]
