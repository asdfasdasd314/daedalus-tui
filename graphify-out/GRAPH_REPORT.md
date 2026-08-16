# Graph Report - daedalus-tui  (2026-08-16)

## Corpus Check
- 30 files · ~11,366 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 344 nodes · 923 edges · 15 communities (13 shown, 2 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 131 edges (avg confidence: 0.53)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ed21dddb`
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

## God Nodes (most connected - your core abstractions)
1. `DaedalusTuiApp` - 52 edges
2. `GitWorktreeManager` - 41 edges
3. `AgentRunner` - 39 edges
4. `WorktreeContext` - 34 edges
5. `TaskCoordinator` - 34 edges
6. `OrchestrationSettings` - 33 edges
7. `AgentControl` - 32 edges
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

## Communities (15 total, 2 thin omitted)

### Community 0 - "WorktreeContext"
Cohesion: 0.11
Nodes (24): EventCallback, IntegrationGate, OrchestratorTests, FakeOrchestrator, TaskCoordinatorTests, AgentControl, AgentResult, Cooperative stop signals shared by a task and its active subprocess. (+16 more)

### Community 1 - "DaedalusVimTextArea"
Cohesion: 0.07
Nodes (15): FakeCoordinator, TuiAppTests, DaedalusVimTextArea, Key, VimTextArea with multiline prompt behavior and system clipboard sync., Return to Insert mode after programmatic prompt operations., Keep Enter as a newline; Ctrl+Enter remains the app submit key., Route visual-line mode and mirror new yanks to the host clipboard. (+7 more)

### Community 2 - "AgentRunner"
Cohesion: 0.10
Nodes (18): OutputCallback, AgentRunnerTests, FakeProcess, FakeStream, InterruptibleProcess, Thread, AgentLogEvent, AgentRequest (+10 more)

### Community 3 - "DaedalusTuiApp"
Cohesion: 0.11
Nodes (8): Changed, ComposeResult, Pressed, DaedalusTuiApp, Key, Path, Add Vim-like navigation without changing TextArea insert behavior., Return a TextArea selection or the active screen selection.

### Community 4 - "app.py"
Cohesion: 0.09
Nodes (24): FakeRunner, settings(), ConfigTests, ProjectDiscoveryTests, Textual interface for concurrent local agent tasks., Use Textual's OSC 52 path and a native clipboard fallback., copy_to_system_clipboard(), paste_from_system_clipboard() (+16 more)

### Community 5 - "AgentControl"
Cohesion: 0.29
Nodes (8): VerificationTests, discover_commands(), format_process_result(), package_has_test_script(), CompletedProcess, Path, Local verification discovery and execution., run_verification()

### Community 6 - "GitWorktreeManager"
Cohesion: 0.14
Nodes (8): GitWorktreeTests, GitWorktreeManager, CompletedProcess, Path, Compatibility alias for callers that used the original private helper., Remove graphify output changes from an agent worktree.          Graphify refresh, Commit only the generated graph after a successful primary update., Remove a cancelled task even when its branch was never integrated.

### Community 7 - "build_task_prompt"
Cohesion: 0.33
Nodes (5): PromptTests, build_repair_prompt(), build_resolver_prompt(), build_task_prompt(), Prompt wrappers used by task and resolver agents.

### Community 8 - "update_repository"
Cohesion: 0.23
Nodes (6): GraphifyTests, Path, Best-effort graph refresh owned by the local orchestration layer., Refresh the primary repository graph without affecting task success., update_repository(), Refresh graph metadata after promotion without blocking the task.

### Community 11 - "Key"
Cohesion: 0.26
Nodes (5): TaskEventCallback, Path, Submit independent prompts while sharing a serialized integration gate., TaskCoordinator, TaskRecord

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

- **Why does `DaedalusTuiApp` connect `DaedalusTuiApp` to `DaedalusVimTextArea`, `AgentRunner`, `Key`, `app.py`?**
  _High betweenness centrality (0.249) - this node is a cross-community bridge._
- **Why does `AgentRunner` connect `AgentRunner` to `WorktreeContext`, `Key`, `DaedalusTuiApp`, `app.py`?**
  _High betweenness centrality (0.188) - this node is a cross-community bridge._
- **Why does `TaskRecord` connect `Key` to `WorktreeContext`, `DaedalusVimTextArea`, `AgentRunner`, `DaedalusTuiApp`, `app.py`, `GitWorktreeManager`?**
  _High betweenness centrality (0.135) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `DaedalusTuiApp` (e.g. with `FakeCoordinator` and `FakeRunner`) actually correct?**
  _`DaedalusTuiApp` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `GitWorktreeManager` (e.g. with `GitWorktreeTests` and `AgentStopped`) actually correct?**
  _`GitWorktreeManager` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `AgentRunner` (e.g. with `AgentRunnerTests` and `FakeProcess`) actually correct?**
  _`AgentRunner` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `WorktreeContext` (e.g. with `GitWorktreeTests` and `OrchestratorTests`) actually correct?**
  _`WorktreeContext` has 11 INFERRED edges - model-reasoned connections that need verification._