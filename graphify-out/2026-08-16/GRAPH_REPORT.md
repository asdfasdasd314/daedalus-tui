# Graph Report - daedalus-tui  (2026-08-16)

## Corpus Check
- 39 files · ~14,305 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 413 nodes · 1027 edges · 21 communities (19 shown, 2 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 149 edges (avg confidence: 0.53)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e7cf071d`
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

## God Nodes (most connected - your core abstractions)
1. `DaedalusTuiApp` - 52 edges
2. `AgentRunner` - 44 edges
3. `GitWorktreeManager` - 41 edges
4. `TaskCoordinator` - 37 edges
5. `WorktreeContext` - 34 edges
6. `OrchestrationSettings` - 34 edges
7. `AgentControl` - 32 edges
8. `LocalOrchestrator` - 31 edges
9. `TaskRecord` - 31 edges
10. `DaedalusVimTextArea` - 31 edges

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

## Communities (21 total, 2 thin omitted)

### Community 0 - "WorktreeContext"
Cohesion: 0.15
Nodes (11): GraphifyTests, PromptTests, Path, Best-effort graph refresh owned by the local orchestration layer., Refresh the primary repository graph without affecting task success., update_repository(), Single-run local agent orchestration without daemon or database dependencies., build_repair_prompt() (+3 more)

### Community 1 - "DaedalusVimTextArea"
Cohesion: 0.07
Nodes (15): FakeCoordinator, TuiAppTests, DaedalusVimTextArea, Key, VimTextArea with multiline prompt behavior and system clipboard sync., Return to Insert mode after programmatic prompt operations., Keep Enter as a newline; Ctrl+Enter remains the app submit key., Route visual-line mode and mirror new yanks to the host clipboard. (+7 more)

### Community 2 - "AgentRunner"
Cohesion: 0.09
Nodes (17): OutputCallback, AgentRunnerTests, FakeProcess, FakeStream, InterruptibleProcess, Thread, AgentLogEvent, AgentRequest (+9 more)

### Community 3 - "DaedalusTuiApp"
Cohesion: 0.09
Nodes (11): Changed, ComposeResult, Pressed, DaedalusTuiApp, Key, Path, Add Vim-like navigation without changing TextArea insert behavior., Clear the selected task and unlock a fresh prompt editor. (+3 more)

### Community 4 - "app.py"
Cohesion: 0.10
Nodes (25): FakeRunner, settings(), ConfigTests, ProjectDiscoveryTests, KeyboardShortcutsScreen, Textual interface for concurrent local agent tasks., Modal reference for the app and prompt editor keyboard shortcuts., copy_to_system_clipboard() (+17 more)

### Community 5 - "TokenUsageStore"
Cohesion: 0.29
Nodes (6): Applying answers, Bridge Agent Profile, Build-loop tasking, cp_doc structure, Hard rules, Purpose

### Community 6 - "GitWorktreeManager"
Cohesion: 0.14
Nodes (8): GitWorktreeTests, GitWorktreeManager, CompletedProcess, Path, Compatibility alias for callers that used the original private helper., Remove graphify output changes from an agent worktree.          Graphify refresh, Commit only the generated graph after a successful primary update., Remove a cancelled task even when its branch was never integrated.

### Community 7 - "Daedalus TUI Local Token Usage Memory"
Cohesion: 0.29
Nodes (6): Daedalus TUI Local Token Usage Memory, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 8 - "update_repository"
Cohesion: 0.12
Nodes (17): EventCallback, IntegrationGate, VerificationTests, AgentControl, Cooperative stop signals shared by a task and its active subprocess., AgentStopped, LocalOrchestrator, Path (+9 more)

### Community 11 - "Key"
Cohesion: 0.11
Nodes (20): TaskEventCallback, OrchestratorTests, FakeOrchestrator, TaskCoordinatorTests, AgentResult, GitWorktreeError, RuntimeError, Local Git worktree lifecycle used by the standalone orchestrator. (+12 more)

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
Cohesion: 0.24
Nodes (5): TokenUsageStoreTests, Path, Small local JSON stores for persistent task telemetry., Append completed-task token usage to a local JSON list., TokenUsageStore

## Knowledge Gaps
- **44 isolated node(s):** `daedalus-tui`, `Execution Boundaries (CRITICAL)`, `Evidence Extraction`, `Architecture Boundaries`, `Parameter Files` (+39 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DaedalusTuiApp` connect `DaedalusTuiApp` to `DaedalusVimTextArea`, `AgentRunner`, `Key`, `app.py`?**
  _High betweenness centrality (0.182) - this node is a cross-community bridge._
- **Why does `AgentRunner` connect `AgentRunner` to `WorktreeContext`, `DaedalusTuiApp`, `app.py`, `update_repository`, `Key`?**
  _High betweenness centrality (0.162) - this node is a cross-community bridge._
- **Why does `TaskRecord` connect `Key` to `DaedalusVimTextArea`, `AgentRunner`, `DaedalusTuiApp`, `app.py`, `GitWorktreeManager`, `update_repository`, `TokenUsageStore`?**
  _High betweenness centrality (0.114) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `DaedalusTuiApp` (e.g. with `FakeCoordinator` and `FakeRunner`) actually correct?**
  _`DaedalusTuiApp` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `AgentRunner` (e.g. with `AgentRunnerTests` and `FakeProcess`) actually correct?**
  _`AgentRunner` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `GitWorktreeManager` (e.g. with `GitWorktreeTests` and `AgentStopped`) actually correct?**
  _`GitWorktreeManager` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `TaskCoordinator` (e.g. with `FakeOrchestrator` and `TaskCoordinatorTests`) actually correct?**
  _`TaskCoordinator` has 13 INFERRED edges - model-reasoned connections that need verification._