# Graph Report - daedalus-tui  (2026-08-17)

## Corpus Check
- 39 files · ~15,890 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 438 nodes · 1110 edges · 22 communities (20 shown, 2 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 151 edges (avg confidence: 0.53)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6c0c364e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- WorktreeContext
- DaedalusVimTextArea
- AgentRunner
- DaedalusTuiApp
- app.py
- TokenUsageStore
- GitWorktreeManager
- Daedalus TUI Local Token Usage Memory
- update_repository
- daedalus-tui
- Key
- Path
- Path
- Path
- architecture.md
- coding.md
- planning.md
- Daedalus TUI Project Instructions
- integrating.md
- TokenUsageStore
- TokenUsageStore

## God Nodes (most connected - your core abstractions)
1. `DaedalusTuiApp` - 60 edges
2. `AgentRunner` - 46 edges
3. `GitWorktreeManager` - 41 edges
4. `TaskCoordinator` - 38 edges
5. `OrchestrationSettings` - 35 edges
6. `TuiAppTests` - 34 edges
7. `WorktreeContext` - 34 edges
8. `AgentControl` - 32 edges
9. `LocalOrchestrator` - 31 edges
10. `TaskRecord` - 31 edges

## Surprising Connections (you probably didn't know these)
- `FakeStream` --uses--> `AgentControl`  [INFERRED]
  tests/test_agent_runner.py → tui/agent_runner.py
- `FakeProcess` --uses--> `AgentControl`  [INFERRED]
  tests/test_agent_runner.py → tui/agent_runner.py
- `InterruptibleProcess` --uses--> `AgentControl`  [INFERRED]
  tests/test_agent_runner.py → tui/agent_runner.py
- `AgentRunnerTests` --uses--> `AgentControl`  [INFERRED]
  tests/test_agent_runner.py → tui/agent_runner.py
- `FakeRunner` --uses--> `DaedalusTuiApp`  [INFERRED]
  tests/test_app.py → tui/app.py

## Import Cycles
- None detected.

## Communities (22 total, 2 thin omitted)

### Community 0 - "WorktreeContext"
Cohesion: 0.33
Nodes (5): PromptTests, build_repair_prompt(), build_resolver_prompt(), build_task_prompt(), Prompt wrappers used by task and resolver agents.

### Community 1 - "DaedalusVimTextArea"
Cohesion: 0.07
Nodes (19): FakeCoordinator, FakeRunner, settings(), TuiAppTests, KeyboardShortcutsScreen, Modal reference for the app and prompt editor keyboard shortcuts., DaedalusProject, A repository recognized by the presence of a ``feature_files`` folder. (+11 more)

### Community 2 - "AgentRunner"
Cohesion: 0.08
Nodes (18): OutputCallback, AgentRunnerTests, FakeProcess, FakeStream, InterruptibleProcess, Thread, AgentLogEvent, AgentRequest (+10 more)

### Community 3 - "DaedalusTuiApp"
Cohesion: 0.08
Nodes (11): Changed, ComposeResult, Pressed, DaedalusTuiApp, Key, Path, Add Vim-like navigation without changing TextArea insert behavior., Clear the selected task and unlock a fresh prompt editor. (+3 more)

### Community 4 - "app.py"
Cohesion: 0.10
Nodes (21): ConfigTests, ProjectDiscoveryTests, Textual interface for concurrent local agent tasks., copy_to_system_clipboard(), paste_from_system_clipboard(), System clipboard helpers for terminals without OSC 52 support., Read clipboard text using the native command available on the host., load_orchestration_settings() (+13 more)

### Community 5 - "TokenUsageStore"
Cohesion: 0.29
Nodes (6): Applying answers, Bridge Agent Profile, Build-loop tasking, cp_doc structure, Hard rules, Purpose

### Community 6 - "GitWorktreeManager"
Cohesion: 0.14
Nodes (8): GitWorktreeTests, GitWorktreeManager, CompletedProcess, Path, Compatibility alias for callers that used the original private helper., Remove graphify output changes from an agent worktree.          Graphify refresh, Commit only the generated graph after a successful primary update., Remove a cancelled task even when its branch was never integrated.

### Community 7 - "Daedalus TUI Local Token Usage Memory"
Cohesion: 0.29
Nodes (6): Daedalus TUI Local Persistent Memory, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 8 - "update_repository"
Cohesion: 0.10
Nodes (25): GraphifyTests, OrchestratorTests, VerificationTests, AgentControl, AgentResult, Cooperative stop signals shared by a task and its active subprocess., WorktreeContext, GraphifyResult (+17 more)

### Community 11 - "Key"
Cohesion: 0.12
Nodes (15): TaskEventCallback, FakeOrchestrator, TaskCoordinatorTests, GitWorktreeError, RuntimeError, Local Git worktree lifecycle used by the standalone orchestrator., OrchestrationResult, OrchestrationSettings (+7 more)

### Community 12 - "Path"
Cohesion: 0.29
Nodes (6): Daedalus Textual TUI, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 13 - "Path"
Cohesion: 0.29
Nodes (6): Daedalus TUI Local Orchestration, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 15 - "architecture.md"
Cohesion: 0.33
Nodes (5): Architecture Boundaries, Development Lifecycle, Evidence Extraction, Execution Boundaries (CRITICAL), Parameter Files

### Community 16 - "coding.md"
Cohesion: 0.33
Nodes (5): 4-Stage Development Lifecycle, Debugging, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization

### Community 17 - "planning.md"
Cohesion: 0.33
Nodes (5): Execution Boundaries (CRITICAL), Feature File Context, Graphify, Parameter Files, Planning Boundaries

### Community 18 - "Daedalus TUI Project Instructions"
Cohesion: 0.40
Nodes (4): Daedalus TUI Project Instructions, graphify, Project boundaries, Task mode

### Community 19 - "integrating.md"
Cohesion: 0.40
Nodes (4): Development Lifecycle, Execution Boundaries (CRITICAL), Integration Boundaries, Parameter Files

### Community 20 - "TokenUsageStore"
Cohesion: 0.40
Nodes (3): EventCallback, IntegrationGate, Path

### Community 21 - "TokenUsageStore"
Cohesion: 0.15
Nodes (9): TokenUsageStoreTests, Path, Small local JSON stores for persistent task telemetry., Give legacy telemetry entries the current nullable metadata shape., Persist task telemetry and the most recently opened project., Return the remembered project path, if the memory contains one., Set the single project marker without losing telemetry records., Backward-compatible alias for :meth:`set_last_opened_project`. (+1 more)

## Knowledge Gaps
- **44 isolated node(s):** `daedalus-tui`, `Execution Boundaries (CRITICAL)`, `Evidence Extraction`, `Architecture Boundaries`, `Parameter Files` (+39 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DaedalusTuiApp` connect `DaedalusTuiApp` to `DaedalusVimTextArea`, `AgentRunner`, `app.py`, `Key`, `TokenUsageStore`?**
  _High betweenness centrality (0.197) - this node is a cross-community bridge._
- **Why does `AgentRunner` connect `AgentRunner` to `DaedalusVimTextArea`, `DaedalusTuiApp`, `app.py`, `update_repository`, `Key`, `TokenUsageStore`?**
  _High betweenness centrality (0.165) - this node is a cross-community bridge._
- **Why does `TaskRecord` connect `Key` to `DaedalusVimTextArea`, `AgentRunner`, `DaedalusTuiApp`, `app.py`, `GitWorktreeManager`, `update_repository`, `TokenUsageStore`?**
  _High betweenness centrality (0.103) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `DaedalusTuiApp` (e.g. with `FakeCoordinator` and `FakeRunner`) actually correct?**
  _`DaedalusTuiApp` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `AgentRunner` (e.g. with `AgentRunnerTests` and `FakeProcess`) actually correct?**
  _`AgentRunner` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `GitWorktreeManager` (e.g. with `GitWorktreeTests` and `AgentStopped`) actually correct?**
  _`GitWorktreeManager` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `TaskCoordinator` (e.g. with `FakeOrchestrator` and `TaskCoordinatorTests`) actually correct?**
  _`TaskCoordinator` has 13 INFERRED edges - model-reasoned connections that need verification._