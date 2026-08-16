# Graph Report - daedalus-tui  (2026-08-16)

## Corpus Check
- 32 files · ~11,980 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 358 nodes · 947 edges · 14 communities (12 shown, 2 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 135 edges (avg confidence: 0.53)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a2e40ca9`
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
- update_repository
- daedalus-tui
- Key
- Path
- Path
- Path

## God Nodes (most connected - your core abstractions)
1. `DaedalusTuiApp` - 48 edges
2. `AgentRunner` - 43 edges
3. `GitWorktreeManager` - 41 edges
4. `TaskCoordinator` - 36 edges
5. `WorktreeContext` - 34 edges
6. `OrchestrationSettings` - 34 edges
7. `AgentControl` - 32 edges
8. `LocalOrchestrator` - 31 edges
9. `TaskRecord` - 30 edges
10. `DaedalusVimTextArea` - 26 edges

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

## Communities (14 total, 2 thin omitted)

### Community 0 - "WorktreeContext"
Cohesion: 0.10
Nodes (18): PromptTests, VerificationTests, AgentControl, Cooperative stop signals shared by a task and its active subprocess., AgentStopped, RuntimeError, Refresh graph metadata after promotion without blocking the task., build_repair_prompt() (+10 more)

### Community 1 - "DaedalusVimTextArea"
Cohesion: 0.07
Nodes (15): FakeCoordinator, TuiAppTests, DaedalusVimTextArea, Key, VimTextArea with multiline prompt behavior and system clipboard sync., Return to Insert mode after programmatic prompt operations., Keep Enter as a newline; Ctrl+Enter remains the app submit key., Route visual-line mode and mirror new yanks to the host clipboard. (+7 more)

### Community 2 - "AgentRunner"
Cohesion: 0.10
Nodes (15): OutputCallback, AgentRunnerTests, FakeProcess, FakeStream, InterruptibleProcess, Thread, AgentLogEvent, AgentRequest (+7 more)

### Community 3 - "DaedalusTuiApp"
Cohesion: 0.10
Nodes (10): Changed, ComposeResult, Pressed, DaedalusTuiApp, Key, Path, Add Vim-like navigation without changing TextArea insert behavior., Return a TextArea selection or the active screen selection. (+2 more)

### Community 4 - "app.py"
Cohesion: 0.10
Nodes (23): FakeRunner, settings(), ConfigTests, ProjectDiscoveryTests, Textual interface for concurrent local agent tasks., copy_to_system_clipboard(), paste_from_system_clipboard(), System clipboard helpers for terminals without OSC 52 support. (+15 more)

### Community 5 - "TokenUsageStore"
Cohesion: 0.24
Nodes (5): TokenUsageStoreTests, Path, Small local JSON stores for persistent task telemetry., Append completed-task token usage to a local JSON list., TokenUsageStore

### Community 6 - "GitWorktreeManager"
Cohesion: 0.15
Nodes (9): GitWorktreeTests, GitWorktreeManager, CompletedProcess, Path, Compatibility alias for callers that used the original private helper., Remove graphify output changes from an agent worktree.          Graphify refresh, Commit only the generated graph after a successful primary update., Remove a cancelled task even when its branch was never integrated. (+1 more)

### Community 8 - "update_repository"
Cohesion: 0.12
Nodes (21): EventCallback, IntegrationGate, GraphifyTests, OrchestratorTests, AgentResult, Provider-specific subprocess execution with normalized agent messages., GitWorktreeError, RuntimeError (+13 more)

### Community 11 - "Key"
Cohesion: 0.13
Nodes (10): TaskEventCallback, FakeOrchestrator, TaskCoordinatorTests, OrchestrationResult, IntegrationCoordinator, Path, Run ready integration operations one at a time in ready order., Submit independent prompts while sharing a serialized integration gate. (+2 more)

### Community 12 - "Path"
Cohesion: 0.29
Nodes (6): Daedalus Textual TUI, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 13 - "Path"
Cohesion: 0.29
Nodes (6): Daedalus TUI Local Orchestration, Dev Mode, Key Points, Relevant Files, State Log, Summary

## Knowledge Gaps
- **12 isolated node(s):** `daedalus-tui`, `Daedalus TUI`, `Summary`, `Key Points`, `Relevant Files` (+7 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DaedalusTuiApp` connect `DaedalusTuiApp` to `DaedalusVimTextArea`, `AgentRunner`, `app.py`, `update_repository`, `Key`?**
  _High betweenness centrality (0.223) - this node is a cross-community bridge._
- **Why does `AgentRunner` connect `AgentRunner` to `WorktreeContext`, `DaedalusTuiApp`, `app.py`, `update_repository`, `Key`?**
  _High betweenness centrality (0.196) - this node is a cross-community bridge._
- **Why does `TaskRecord` connect `Key` to `WorktreeContext`, `DaedalusVimTextArea`, `AgentRunner`, `DaedalusTuiApp`, `app.py`, `TokenUsageStore`, `GitWorktreeManager`, `update_repository`?**
  _High betweenness centrality (0.144) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `DaedalusTuiApp` (e.g. with `FakeCoordinator` and `FakeRunner`) actually correct?**
  _`DaedalusTuiApp` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `AgentRunner` (e.g. with `AgentRunnerTests` and `FakeProcess`) actually correct?**
  _`AgentRunner` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `GitWorktreeManager` (e.g. with `GitWorktreeTests` and `AgentStopped`) actually correct?**
  _`GitWorktreeManager` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `TaskCoordinator` (e.g. with `FakeOrchestrator` and `TaskCoordinatorTests`) actually correct?**
  _`TaskCoordinator` has 12 INFERRED edges - model-reasoned connections that need verification._