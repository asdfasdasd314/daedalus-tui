"""Standalone Textual interface and local agent orchestration."""

from .agent_runner import AgentControl, AgentLogEvent, AgentRequest, AgentResult, AgentRunner
from .orchestrator import LocalOrchestrator, OrchestrationResult
from .projects import DaedalusProject, discover_projects
from .task_coordinator import TASK_STATUSES, TaskCoordinator, TaskRecord

__all__ = [
    "AgentRequest",
    "AgentControl",
    "AgentResult",
    "AgentRunner",
    "AgentLogEvent",
    "DaedalusTuiApp",
    "LocalOrchestrator",
    "OrchestrationResult",
    "DaedalusProject",
    "discover_projects",
    "TaskCoordinator",
    "TaskRecord",
    "TASK_STATUSES",
]


def __getattr__(name: str):
    if name == "DaedalusTuiApp":
        from .app import DaedalusTuiApp

        return DaedalusTuiApp
    raise AttributeError(name)
