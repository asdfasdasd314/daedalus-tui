# Graph Report - /Users/jameshollingsworth/Projects/daedalus/tui  (2026-08-16)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 328 nodes · 869 edges · 26 communities (10 shown, 16 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 131 edges (avg confidence: 0.53)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `df481b1a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- WorktreeContext
- DaedalusVimTextArea
- AgentRunner
- DaedalusTuiApp
- app.py
- AgentControl
- GitWorktreeManager
- build_task_prompt
- update_repository
- daedalus-tui
- Key
- Path
- Path
- Path
- CompletedProcess
- Path
- RuntimeError
- Path
- Path
- RuntimeError
- Path
- Path
- CompletedProcess
- Path
- Key

## God Nodes (most connected - your core abstractions)
1. `DaedalusTuiApp` - 52 edges
2. `GitWorktreeManager` - 41 edges
3. `AgentRunner` - 36 edges
4. `WorktreeContext` - 34 edges
5. `TaskCoordinator` - 34 edges
6. `AgentControl` - 32 edges
7. `OrchestrationSettings` - 32 edges
8. `LocalOrchestrator` - 31 edges
9. `TaskRecord` - 29 edges
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

## Communities (26 total, 16 thin omitted)

### Community 0 - "WorktreeContext"
Cohesion: 0.12
Nodes (20): TaskEventCallback, OrchestratorTests, FakeOrchestrator, TaskCoordinatorTests, AgentResult, GitWorktreeError, Local Git worktree lifecycle used by the standalone orchestrator., WorktreeContext (+12 more)

### Community 1 - "DaedalusVimTextArea"
Cohesion: 0.07
Nodes (14): FakeCoordinator, TuiAppTests, DaedalusVimTextArea, VimTextArea with multiline prompt behavior and system clipboard sync., Return to Insert mode after programmatic prompt operations., Keep Enter as a newline; Ctrl+Enter remains the app submit key., Route visual-line mode and mirror new yanks to the host clipboard., Paste Vim's register, falling back to the system clipboard. (+6 more)

### Community 2 - "AgentRunner"
Cohesion: 0.10
Nodes (17): OutputCallback, AgentRunnerTests, FakeProcess, FakeStream, InterruptibleProcess, Thread, AgentLogEvent, AgentRequest (+9 more)

### Community 3 - "DaedalusTuiApp"
Cohesion: 0.11
Nodes (7): Changed, ComposeResult, Pressed, DaedalusTuiApp, Add Vim-like navigation without changing TextArea insert behavior., Return a TextArea selection or the active screen selection., Use Textual's OSC 52 path and a native clipboard fallback.

### Community 4 - "app.py"
Cohesion: 0.11
Nodes (21): FakeRunner, settings(), ConfigTests, ProjectDiscoveryTests, Textual interface for concurrent local agent tasks., copy_to_system_clipboard(), paste_from_system_clipboard(), System clipboard helpers for terminals without OSC 52 support. (+13 more)

### Community 5 - "AgentControl"
Cohesion: 0.13
Nodes (12): EventCallback, IntegrationGate, VerificationTests, AgentControl, Cooperative stop signals shared by a task and its active subprocess., AgentStopped, Refresh graph metadata after promotion without blocking the task., discover_commands() (+4 more)

### Community 6 - "GitWorktreeManager"
Cohesion: 0.14
Nodes (6): GitWorktreeTests, GitWorktreeManager, Compatibility alias for callers that used the original private helper., Remove graphify output changes from an agent worktree.          Graphify refresh, Commit only the generated graph after a successful primary update., Remove a cancelled task even when its branch was never integrated.

### Community 7 - "build_task_prompt"
Cohesion: 0.33
Nodes (5): PromptTests, build_repair_prompt(), build_resolver_prompt(), build_task_prompt(), Prompt wrappers used by task and resolver agents.

### Community 8 - "update_repository"
Cohesion: 0.33
Nodes (4): GraphifyTests, Best-effort graph refresh owned by the local orchestration layer., Refresh the primary repository graph without affecting task success., update_repository()

## Knowledge Gaps
- **1 isolated node(s):** `daedalus-tui`
  These have ≤1 connection - possible missing edges or undocumented components.
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DaedalusTuiApp` connect `DaedalusTuiApp` to `WorktreeContext`, `DaedalusVimTextArea`, `AgentRunner`, `app.py`?**
  _High betweenness centrality (0.255) - this node is a cross-community bridge._
- **Why does `AgentRunner` connect `AgentRunner` to `WorktreeContext`, `DaedalusTuiApp`, `app.py`, `AgentControl`?**
  _High betweenness centrality (0.178) - this node is a cross-community bridge._
- **Why does `TaskRecord` connect `WorktreeContext` to `DaedalusVimTextArea`, `AgentRunner`, `DaedalusTuiApp`, `app.py`, `AgentControl`, `GitWorktreeManager`?**
  _High betweenness centrality (0.139) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `DaedalusTuiApp` (e.g. with `FakeCoordinator` and `FakeRunner`) actually correct?**
  _`DaedalusTuiApp` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `GitWorktreeManager` (e.g. with `GitWorktreeTests` and `AgentStopped`) actually correct?**
  _`GitWorktreeManager` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `AgentRunner` (e.g. with `AgentRunnerTests` and `FakeProcess`) actually correct?**
  _`AgentRunner` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `WorktreeContext` (e.g. with `GitWorktreeTests` and `OrchestratorTests`) actually correct?**
  _`WorktreeContext` has 11 INFERRED edges - model-reasoned connections that need verification._