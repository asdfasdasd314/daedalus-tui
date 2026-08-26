"""Read-only configuration for the standalone TUI."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tomllib

from .orchestrator import OrchestrationSettings


PARAMETER_DIRECTORY = "parameter_files"
TUI_PARAMETER_FILE = "daedalus-tui.toml"
ORCHESTRATION_PARAMETER_FILE = "daedalus-tui-orchestration.toml"
CODING_STATISTICS_PARAMETER_FILE = "daedalus-tui-coding-statistics.toml"


@dataclass(frozen=True)
class ModelOption:
    label: str
    value: str


@dataclass(frozen=True)
class TuiSettings:
    default_provider: str
    default_model: str
    default_reasoning: str
    providers: tuple[ModelOption, ...]
    codex_models: tuple[ModelOption, ...]
    codex_reasoning: tuple[ModelOption, ...]
    cursor_model: ModelOption
    modes: tuple[ModelOption, ...] = (
        ModelOption("Coding", "coding"),
        ModelOption("Ask", "ask"),
        ModelOption("Plan", "plan"),
    )
    output_width: str = "95%"


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
    modes = tuple(_options(values.get("modes", []), "mode")) or TuiSettings.modes
    output = values.get("output", {})
    output_width = str(output.get("width", "95%"))

    default_provider = str(defaults.get("provider", "codex"))
    default_model = str(defaults.get("model", "gpt-5.6-luna"))
    default_reasoning = str(defaults.get("reasoning", "high"))
    if not providers or not codex_models or not codex_reasoning:
        raise ValueError(f"{path} must define providers, codex_models, and codex_reasoning.")
    return TuiSettings(
        default_provider,
        default_model,
        default_reasoning,
        providers,
        codex_models,
        codex_reasoning,
        cursor_model,
        modes,
        output_width,
    )


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
