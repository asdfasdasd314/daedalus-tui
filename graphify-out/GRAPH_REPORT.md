# Graph Report - daedalus-tui  (2026-08-17)

## Corpus Check
- 40 files · ~17,169 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 469 nodes · 1171 edges · 22 communities (20 shown, 2 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 158 edges (avg confidence: 0.54)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5217f700`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- update_repository
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
- .__init__
- TokenUsageStore

## God Nodes (most connected - your core abstractions)
1. `DaedalusTuiApp` - 61 edges
2. `AgentRunner` - 46 edges
3. `GitWorktreeManager` - 43 edges
4. `TuiAppTests` - 39 edges
5. `TaskCoordinator` - 39 edges
6. `DaedalusVimTextArea` - 36 edges
7. `OrchestrationSettings` - 35 edges
8. `WorktreeContext` - 34 edges
9. `AgentControl` - 32 edges
10. `TaskRecord` - 32 edges

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

### Community 0 - "update_repository"
Cohesion: 0.15
Nodes (11): GraphifyTests, PromptTests, Path, Best-effort graph refresh owned by the local orchestration layer., Refresh the primary repository graph without affecting task success., update_repository(), Single-run local agent orchestration without daemon or database dependencies., build_repair_prompt() (+3 more)

### Community 1 - "DaedalusVimTextArea"
Cohesion: 0.06
Nodes (20): FakeCoordinator, FakeRunner, settings(), TuiAppTests, KeyboardShortcutsScreen, Modal reference for the app and prompt editor keyboard shortcuts., DaedalusProject, A repository recognized by the presence of a ``feature_files`` folder. (+12 more)

### Community 2 - "AgentRunner"
Cohesion: 0.08
Nodes (18): OutputCallback, AgentRunnerTests, FakeProcess, FakeStream, InterruptibleProcess, Thread, AgentLogEvent, AgentRequest (+10 more)

### Community 3 - "DaedalusTuiApp"
Cohesion: 0.09
Nodes (11): Changed, ComposeResult, Pressed, DaedalusTuiApp, Key, Path, Add Vim-like navigation without changing TextArea insert behavior., Clear the selected task and unlock a fresh prompt editor. (+3 more)

### Community 4 - "app.py"
Cohesion: 0.10
Nodes (21): ConfigTests, ProjectDiscoveryTests, Textual interface for concurrent local agent tasks., copy_to_system_clipboard(), paste_from_system_clipboard(), System clipboard helpers for terminals without OSC 52 support., Read clipboard text using the native command available on the host., load_orchestration_settings() (+13 more)

### Community 5 - "TokenUsageStore"
Cohesion: 0.29
Nodes (6): Applying answers, Bridge Agent Profile, Build-loop tasking, cp_doc structure, Hard rules, Purpose

### Community 6 - "GitWorktreeManager"
Cohesion: 0.12
Nodes (11): Log, Strip, Style, Selectable transcript rendering with semantic assistant-message emphasis., A selectable log that can emphasize a task's final assistant message.      ``Log, Return the tone assigned to each rendered transcript line., Use the prompt's normal text color for the final transcript tone., Re-render lines after a surrounding widget's color state changes. (+3 more)

### Community 7 - "Daedalus TUI Local Token Usage Memory"
Cohesion: 0.29
Nodes (6): Daedalus TUI Local Persistent Memory, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 8 - "update_repository"
Cohesion: 0.07
Nodes (31): GitWorktreeTests, OrchestratorTests, VerificationTests, AgentControl, AgentResult, Cooperative stop signals shared by a task and its active subprocess., GitWorktreeError, GitWorktreeManager (+23 more)

### Community 11 - "Key"
Cohesion: 0.14
Nodes (13): TaskEventCallback, FakeOrchestrator, TaskCoordinatorTests, OrchestrationResult, OrchestrationSettings, IntegrationCoordinator, Path, Concurrent task state and serialized local integration. (+5 more)

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

### Community 20 - ".__init__"
Cohesion: 0.40
Nodes (3): EventCallback, IntegrationGate, Path

### Community 21 - "TokenUsageStore"
Cohesion: 0.15
Nodes (9): TaskMemoryStoreTests, Path, Small local JSON stores for persistent task history., Persist task history and the most recently opened project., Return the remembered project path, if the memory contains one., Set the single project marker without losing task records., Backward-compatible alias for :meth:`set_last_opened_project`., Upsert a task snapshot keyed by the task worktree's directory name. (+1 more)

## Knowledge Gaps
- **44 isolated node(s):** `daedalus-tui`, `Execution Boundaries (CRITICAL)`, `Evidence Extraction`, `Architecture Boundaries`, `Parameter Files` (+39 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DaedalusTuiApp` connect `DaedalusTuiApp` to `DaedalusVimTextArea`, `AgentRunner`, `app.py`, `GitWorktreeManager`, `Key`, `TokenUsageStore`?**
  _High betweenness centrality (0.203) - this node is a cross-community bridge._
- **Why does `AgentRunner` connect `AgentRunner` to `update_repository`, `DaedalusVimTextArea`, `DaedalusTuiApp`, `app.py`, `update_repository`, `Key`, `.__init__`?**
  _High betweenness centrality (0.161) - this node is a cross-community bridge._
- **Why does `TaskRecord` connect `Key` to `DaedalusVimTextArea`, `AgentRunner`, `DaedalusTuiApp`, `app.py`, `update_repository`, `TokenUsageStore`?**
  _High betweenness centrality (0.108) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `DaedalusTuiApp` (e.g. with `FakeCoordinator` and `FakeRunner`) actually correct?**
  _`DaedalusTuiApp` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `AgentRunner` (e.g. with `AgentRunnerTests` and `FakeProcess`) actually correct?**
  _`AgentRunner` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `GitWorktreeManager` (e.g. with `GitWorktreeTests` and `AgentStopped`) actually correct?**
  _`GitWorktreeManager` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `TuiAppTests` (e.g. with `DaedalusTuiApp` and `KeyboardShortcutsScreen`) actually correct?**
  _`TuiAppTests` has 7 INFERRED edges - model-reasoned connections that need verification._