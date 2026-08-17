# Graph Report - daedalus-tui  (2026-08-17)

## Corpus Check
- 45 files · ~21,267 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 567 nodes · 1444 edges · 23 communities (21 shown, 2 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 199 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3aaeb294`
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
- Daedalus TUI Coding Statistics

## God Nodes (most connected - your core abstractions)
1. `DaedalusTuiApp` - 70 edges
2. `TuiAppTests` - 48 edges
3. `DaedalusVimTextArea` - 48 edges
4. `AgentRunner` - 47 edges
5. `TaskCoordinator` - 45 edges
6. `GitWorktreeManager` - 43 edges
7. `OrchestrationSettings` - 39 edges
8. `TaskRecord` - 38 edges
9. `WorktreeContext` - 36 edges
10. `LocalOrchestrator` - 34 edges

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

## Communities (23 total, 2 thin omitted)

### Community 0 - "update_repository"
Cohesion: 0.40
Nodes (3): EventCallback, IntegrationGate, Path

### Community 1 - "DaedalusVimTextArea"
Cohesion: 0.07
Nodes (17): TuiAppTests, DaedalusVimTextArea, Key, Keep Enter as a newline; Ctrl+Enter remains the app submit key., Route visual-line mode and mirror new yanks to the host clipboard., Paste Vim's register, falling back to the system clipboard., Paste before the cursor, including from the system clipboard., Add Daedalus prompt commands that the dependency does not provide. (+9 more)

### Community 2 - "AgentRunner"
Cohesion: 0.09
Nodes (16): OutputCallback, AgentRunnerTests, FakeProcess, FakeStream, InterruptibleProcess, Thread, AgentLogEvent, AgentRequest (+8 more)

### Community 3 - "DaedalusTuiApp"
Cohesion: 0.06
Nodes (18): Changed, Log, Pressed, DaedalusTuiApp, Key, Path, Add Vim-like navigation without changing TextArea insert behavior., Clear the selected task and unlock a fresh prompt editor. (+10 more)

### Community 4 - "app.py"
Cohesion: 0.06
Nodes (32): ComposeResult, FakeCoordinator, FakeRunner, settings(), ConfigTests, ProjectDiscoveryTests, CodingStatisticsScreen, _format_tokens() (+24 more)

### Community 5 - "TokenUsageStore"
Cohesion: 0.29
Nodes (6): Applying answers, Bridge Agent Profile, Build-loop tasking, cp_doc structure, Hard rules, Purpose

### Community 6 - "GitWorktreeManager"
Cohesion: 0.29
Nodes (5): Style, Strip, Render a line with the final-message color before selection styling., Strip, Paint a thin left-aligned caret at the insertion point.

### Community 7 - "Daedalus TUI Local Token Usage Memory"
Cohesion: 0.29
Nodes (6): Daedalus TUI Local Persistent Memory, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 8 - "update_repository"
Cohesion: 0.13
Nodes (9): GitWorktreeTests, GitWorktreeManager, CompletedProcess, Path, Compatibility alias for callers that used the original private helper., Stage the current worktree contents for orchestration checks or commit., Remove graphify output changes from an agent worktree.          Graphify refresh, Commit only the generated graph after a successful primary update. (+1 more)

### Community 11 - "Key"
Cohesion: 0.07
Nodes (38): GraphifyTests, OrchestratorTests, PromptTests, VerificationTests, AgentControl, AgentResult, Provider-specific subprocess execution with normalized agent messages., Cooperative stop signals shared by a task and its active subprocess. (+30 more)

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
Cohesion: 0.09
Nodes (26): Any, TaskEventCallback, PlanTests, FakeOrchestrator, TaskCoordinatorTests, Replace question controls after Textual has completed child removal., OrchestrationSettings, build_implementation_prompt() (+18 more)

### Community 21 - "TokenUsageStore"
Cohesion: 0.07
Nodes (27): datetime, TaskMemoryStoreTests, TokenUsageTests, Path, Small local JSON stores for persistent task history., Persist task history and the most recently opened project., Return the remembered project path, if the memory contains one., Set the single project marker without losing task records. (+19 more)

### Community 24 - "Daedalus TUI Coding Statistics"
Cohesion: 0.29
Nodes (6): Daedalus TUI Coding Statistics, Dev Mode, Key Points, Relevant Files, State Log, Summary

## Knowledge Gaps
- **49 isolated node(s):** `daedalus-tui`, `Execution Boundaries (CRITICAL)`, `Evidence Extraction`, `Architecture Boundaries`, `Parameter Files` (+44 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DaedalusTuiApp` connect `DaedalusTuiApp` to `DaedalusVimTextArea`, `AgentRunner`, `app.py`, `Key`, `.__init__`, `TokenUsageStore`?**
  _High betweenness centrality (0.182) - this node is a cross-community bridge._
- **Why does `AgentRunner` connect `AgentRunner` to `update_repository`, `DaedalusTuiApp`, `app.py`, `Key`, `.__init__`?**
  _High betweenness centrality (0.143) - this node is a cross-community bridge._
- **Why does `DaedalusVimTextArea` connect `DaedalusVimTextArea` to `DaedalusTuiApp`, `app.py`, `GitWorktreeManager`?**
  _High betweenness centrality (0.121) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `DaedalusTuiApp` (e.g. with `FakeCoordinator` and `FakeRunner`) actually correct?**
  _`DaedalusTuiApp` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `TuiAppTests` (e.g. with `CodingStatisticsScreen` and `DaedalusTuiApp`) actually correct?**
  _`TuiAppTests` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 24 inferred relationships involving `DaedalusVimTextArea` (e.g. with `FakeCoordinator` and `FakeRunner`) actually correct?**
  _`DaedalusVimTextArea` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `AgentRunner` (e.g. with `AgentRunnerTests` and `FakeProcess`) actually correct?**
  _`AgentRunner` has 14 INFERRED edges - model-reasoned connections that need verification._