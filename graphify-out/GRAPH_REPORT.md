# Graph Report - daedalus-tui  (2026-08-17)

## Corpus Check
- 39 files · ~16,183 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 440 nodes · 1118 edges · 21 communities (19 shown, 2 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 152 edges (avg confidence: 0.53)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `af6afcd4`
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
- TokenUsageStore

## God Nodes (most connected - your core abstractions)
1. `DaedalusTuiApp` - 60 edges
2. `AgentRunner` - 46 edges
3. `GitWorktreeManager` - 41 edges
4. `TaskCoordinator` - 39 edges
5. `TuiAppTests` - 35 edges
6. `OrchestrationSettings` - 35 edges
7. `WorktreeContext` - 34 edges
8. `AgentControl` - 32 edges
9. `TaskRecord` - 32 edges
10. `LocalOrchestrator` - 31 edges

## Surprising Connections (you probably didn't know these)
- `FakeRunner` --uses--> `DaedalusTuiApp`  [INFERRED]
  tests/test_app.py → tui/app.py
- `FakeRunner` --uses--> `ModelOption`  [INFERRED]
  tests/test_app.py → tui/config.py
- `FakeRunner` --uses--> `TuiSettings`  [INFERRED]
  tests/test_app.py → tui/config.py
- `FakeRunner` --uses--> `TaskRecord`  [INFERRED]
  tests/test_app.py → tui/task_coordinator.py
- `FakeCoordinator` --uses--> `DaedalusTuiApp`  [INFERRED]
  tests/test_app.py → tui/app.py

## Import Cycles
- None detected.

## Communities (21 total, 2 thin omitted)

### Community 0 - "update_repository"
Cohesion: 0.29
Nodes (5): GraphifyTests, Path, Best-effort graph refresh owned by the local orchestration layer., Refresh the primary repository graph without affecting task success., update_repository()

### Community 1 - "DaedalusVimTextArea"
Cohesion: 0.07
Nodes (19): FakeCoordinator, FakeRunner, settings(), TuiAppTests, KeyboardShortcutsScreen, Modal reference for the app and prompt editor keyboard shortcuts., DaedalusProject, A repository recognized by the presence of a ``feature_files`` folder. (+11 more)

### Community 2 - "AgentRunner"
Cohesion: 0.08
Nodes (20): OutputCallback, AgentRunnerTests, FakeProcess, FakeStream, InterruptibleProcess, Thread, AgentControl, AgentLogEvent (+12 more)

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
Cohesion: 0.11
Nodes (21): EventCallback, IntegrationGate, PromptTests, VerificationTests, AgentStopped, LocalOrchestrator, Path, RuntimeError (+13 more)

### Community 11 - "Key"
Cohesion: 0.11
Nodes (21): TaskEventCallback, OrchestratorTests, FakeOrchestrator, TaskCoordinatorTests, AgentResult, GitWorktreeError, RuntimeError, Local Git worktree lifecycle used by the standalone orchestrator. (+13 more)

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

### Community 21 - "TokenUsageStore"
Cohesion: 0.15
Nodes (9): TaskMemoryStoreTests, Path, Small local JSON stores for persistent task history., Persist task history and the most recently opened project., Return the remembered project path, if the memory contains one., Set the single project marker without losing task records., Backward-compatible alias for :meth:`set_last_opened_project`., Upsert a task snapshot keyed by the task worktree's directory name. (+1 more)

## Knowledge Gaps
- **44 isolated node(s):** `daedalus-tui`, `Execution Boundaries (CRITICAL)`, `Evidence Extraction`, `Architecture Boundaries`, `Parameter Files` (+39 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DaedalusTuiApp` connect `DaedalusTuiApp` to `DaedalusVimTextArea`, `AgentRunner`, `app.py`, `Key`, `TokenUsageStore`?**
  _High betweenness centrality (0.197) - this node is a cross-community bridge._
- **Why does `AgentRunner` connect `AgentRunner` to `DaedalusVimTextArea`, `DaedalusTuiApp`, `app.py`, `update_repository`, `Key`?**
  _High betweenness centrality (0.165) - this node is a cross-community bridge._
- **Why does `TaskRecord` connect `Key` to `DaedalusVimTextArea`, `AgentRunner`, `DaedalusTuiApp`, `app.py`, `GitWorktreeManager`, `update_repository`, `TokenUsageStore`?**
  _High betweenness centrality (0.107) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `DaedalusTuiApp` (e.g. with `FakeCoordinator` and `FakeRunner`) actually correct?**
  _`DaedalusTuiApp` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `AgentRunner` (e.g. with `AgentRunnerTests` and `FakeProcess`) actually correct?**
  _`AgentRunner` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `GitWorktreeManager` (e.g. with `GitWorktreeTests` and `AgentStopped`) actually correct?**
  _`GitWorktreeManager` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `TaskCoordinator` (e.g. with `FakeOrchestrator` and `TaskCoordinatorTests`) actually correct?**
  _`TaskCoordinator` has 13 INFERRED edges - model-reasoned connections that need verification._