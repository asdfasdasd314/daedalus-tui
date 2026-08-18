"""Token usage records and derived coding statistics."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Iterable


UTC = timezone.utc


@dataclass(frozen=True)
class TokenUsageEntry:
    """The token usage attributed to one submitted task."""

    task_id: str
    timestamp: datetime
    provider: str
    tokens: int
    prompt: str = ""
    state: str = "completed"

    def __post_init__(self) -> None:
        timestamp = self.timestamp
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=UTC)
        else:
            timestamp = timestamp.astimezone(UTC)
        object.__setattr__(self, "timestamp", timestamp)
        object.__setattr__(self, "tokens", max(0, int(self.tokens)))
        object.__setattr__(self, "provider", self.provider or "unknown")


@dataclass(frozen=True)
class TokenUsageStats:
    """Aggregates used by the coding statistics screen."""

    entries: tuple[TokenUsageEntry, ...]
    cumulative_tokens: int
    daily_tokens: int
    cumulative_tasks: int
    daily_tasks: int
    average_tokens_per_prompt: float
    average_tasks_per_prompt: float
    last_hour_tokens: int
    last_hour_tasks: int
    seven_day_expected_tokens: int
    seven_day_expected_tasks: int
    thirty_day_expected_tokens: int
    thirty_day_expected_tasks: int
    provider_tokens: tuple[tuple[str, int], ...]
    provider_tasks: tuple[tuple[str, int], ...]
    provider_percentages: tuple[tuple[str, float], ...]

    def provider_split(self, unit: str = "tokens") -> tuple[tuple[str, int, float], ...]:
        """Return provider, count, and percentage triples for the selected unit."""
        if unit not in {"tokens", "tasks"}:
            raise ValueError("unit must be 'tokens' or 'tasks'")
        totals = self.provider_tokens if unit == "tokens" else self.provider_tasks
        total = sum(count for _, count in totals)
        return tuple(
            (provider, count, (count / total * 100) if total else 0.0)
            for provider, count in totals
        )


def calculate_token_usage(
    entries: Iterable[TokenUsageEntry],
    *,
    now: datetime | None = None,
    recent_window_hours: int = 1,
    forecast_days: int = 7,
    thirty_day_forecast_days: int = 30,
) -> TokenUsageStats:
    """Calculate token and task totals, windows, and provider percentages.

    Daily usage uses the user's local calendar day. The forecast projects the
    average daily usage across the recorded history into ``forecast_days``.
    """
    if recent_window_hours < 1:
        raise ValueError("recent_window_hours must be positive")
    if forecast_days < 1:
        raise ValueError("forecast_days must be positive")
    if thirty_day_forecast_days < 1:
        raise ValueError("thirty_day_forecast_days must be positive")

    current = now or datetime.now(UTC)
    if current.tzinfo is None:
        current = current.replace(tzinfo=UTC)
    normalized = tuple(
        sorted(
            (entry for entry in entries if entry.state == "completed"),
            key=lambda entry: entry.timestamp,
            reverse=True,
        )
    )
    current_local = current.astimezone()
    today = current_local.date()
    recent_start = current - timedelta(hours=recent_window_hours)
    cumulative = sum(entry.tokens for entry in normalized)
    cumulative_tasks = len(normalized)
    daily = sum(
        entry.tokens
        for entry in normalized
        if entry.timestamp.astimezone(current_local.tzinfo).date() == today
    )
    daily_tasks = sum(
        1
        for entry in normalized
        if entry.timestamp.astimezone(current_local.tzinfo).date() == today
    )
    recent = sum(entry.tokens for entry in normalized if recent_start <= entry.timestamp <= current)
    recent_tasks = sum(1 for entry in normalized if recent_start <= entry.timestamp <= current)
    average = cumulative / len(normalized) if normalized else 0.0
    average_tasks = 1.0 if normalized else 0.0

    if normalized:
        first_day = normalized[-1].timestamp.astimezone(current_local.tzinfo).date()
        history_days = max(1, (today - first_day).days + 1)
        average_daily = cumulative / history_days
    else:
        average_daily = 0.0
    expected = round(average_daily * forecast_days)
    expected_thirty_day = round(average_daily * thirty_day_forecast_days)
    average_daily_tasks = cumulative_tasks / history_days if normalized else 0.0

    provider_totals: dict[str, int] = {}
    provider_task_totals: dict[str, int] = {}
    for entry in normalized:
        provider_totals[entry.provider] = provider_totals.get(entry.provider, 0) + entry.tokens
        provider_task_totals[entry.provider] = provider_task_totals.get(entry.provider, 0) + 1
    provider_items = tuple(sorted(provider_totals.items(), key=lambda item: (-item[1], item[0])))
    provider_task_items = tuple(
        sorted(provider_task_totals.items(), key=lambda item: (-item[1], item[0]))
    )
    provider_percentages = tuple(
        (provider, (tokens / cumulative * 100) if cumulative else 0.0)
        for provider, tokens in provider_items
    )
    return TokenUsageStats(
        entries=normalized,
        cumulative_tokens=cumulative,
        daily_tokens=daily,
        cumulative_tasks=cumulative_tasks,
        daily_tasks=daily_tasks,
        average_tokens_per_prompt=average,
        average_tasks_per_prompt=average_tasks,
        last_hour_tokens=recent,
        last_hour_tasks=recent_tasks,
        seven_day_expected_tokens=expected,
        seven_day_expected_tasks=round(average_daily_tasks * forecast_days),
        thirty_day_expected_tokens=expected_thirty_day,
        thirty_day_expected_tasks=round(average_daily_tasks * thirty_day_forecast_days),
        provider_tokens=provider_items,
        provider_tasks=provider_task_items,
        provider_percentages=provider_percentages,
    )


def usage_entries_from_memory(store) -> tuple[TokenUsageEntry, ...]:
    """Convert persisted task snapshots into usage records."""
    entries: list[TokenUsageEntry] = []
    for task_id, task in store.get_tasks().items():
        if task.get("state") != "completed":
            continue
        timestamp = _parse_timestamp(task.get("timestamp"))
        if timestamp is None:
            continue
        provider = task.get("provider")
        tokens = task.get("tokens", 0)
        if not isinstance(provider, str):
            provider = "unknown"
        if not isinstance(tokens, int) or isinstance(tokens, bool):
            tokens = 0
        entries.append(
            TokenUsageEntry(
                task_id,
                timestamp,
                provider,
                tokens,
                str(task.get("prompt", "")),
                str(task.get("state", "")),
            )
        )
    return tuple(entries)


def merge_usage_entries(*entry_groups: Iterable[TokenUsageEntry]) -> tuple[TokenUsageEntry, ...]:
    """Merge snapshots by task ID, allowing live records to replace history."""
    merged: dict[str, TokenUsageEntry] = {}
    for group in entry_groups:
        for entry in group:
            merged[entry.task_id] = entry
    return tuple(sorted(merged.values(), key=lambda entry: entry.timestamp, reverse=True))


def _parse_timestamp(value: object) -> datetime | None:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return datetime.fromtimestamp(value, UTC)
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed.replace(tzinfo=UTC) if parsed.tzinfo is None else parsed.astimezone(UTC)


def task_usage_entry(record) -> TokenUsageEntry | None:
    """Convert a live task record without coupling this module to its class."""
    if record.status != "completed":
        return None
    return TokenUsageEntry(
        record.memory_task_id or f"task-{record.task_id}",
        datetime.fromtimestamp(record.submitted_at, UTC),
        record.provider,
        record.tokens_consumed,
        record.prompt,
        record.status,
    )
