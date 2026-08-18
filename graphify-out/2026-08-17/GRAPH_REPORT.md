# Graph Report - daedalus-tui  (2026-08-17)

## Corpus Check
- 46 files · ~27,023 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 664 nodes · 1724 edges · 30 communities (27 shown, 3 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 211 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `04ee9480`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- PlanQuestion
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
- ._shutdown_coordinators
- ._set_status
- update_repository
- Daedalus TUI Coding Statistics
- ._usage_entries
- .provider_split
- CodingStatisticsScreen
- KeyboardShortcutsScreen
- PlanAnswerSelect

## God Nodes (most connected - your core abstractions)
1. `DaedalusTuiApp` - 93 edges
2. `TuiAppTests` - 60 edges
3. `TaskCoordinator` - 57 edges
4. `AgentRunner` - 52 edges
5. `DaedalusVimTextArea` - 48 edges
6. `OrchestrationSettings` - 46 edges
7. `GitWorktreeManager` - 45 edges
8. `TaskRecord` - 45 edges
9. `WorktreeContext` - 38 edges
10. `TaskMemoryStore` - 34 edges

## Surprising Connections (you probably didn't know these)
- `FakeStream` --uses--> `AgentControl`  [INFERRED]
  tests/test_agent_runner.py → tui/agent_runner.py
- `FakeProcess` --uses--> `AgentControl`  [INFERRED]
  tests/test_agent_runner.py → tui/agent_runner.py
- `InterruptibleProcess` --uses--> `AgentControl`  [INFERRED]
  tests/test_agent_runner.py → tui/agent_runner.py
- `AgentRunnerTests` --uses--> `AgentControl`  [INFERRED]
  tests/test_agent_runner.py → tui/agent_runner.py
- `FakeRunner` --uses--> `CodingStatisticsScreen`  [INFERRED]
  tests/test_app.py → tui/app.py

## Import Cycles
- None detected.

## Communities (30 total, 3 thin omitted)

### Community 0 - "PlanQuestion"
Cohesion: 0.17
Nodes (9): Textual interface for concurrent local agent tasks., copy_to_system_clipboard(), paste_from_system_clipboard(), System clipboard helpers for terminals without OSC 52 support., Read clipboard text using the native command available on the host., Selectable transcript rendering with semantic assistant-message emphasis., The Daedalus prompt's incremental Vim editing adapter., Paste Vim's register, falling back to the system clipboard. (+1 more)

### Community 1 - "DaedalusVimTextArea"
Cohesion: 0.05
Nodes (27): Any, TuiAppTests, PlanTests, build_implementation_prompt(), build_plan_followup_prompt(), parse_plan_response(), _parse_question(), _payload_text() (+19 more)

### Community 2 - "AgentRunner"
Cohesion: 0.08
Nodes (19): OutputCallback, AgentRunnerTests, FakeProcess, FakeStream, InterruptibleProcess, Thread, AgentLogEvent, AgentRequest (+11 more)

### Community 3 - "DaedalusTuiApp"
Cohesion: 0.05
Nodes (23): Changed, Log, Pressed, RowSelected, DaedalusTuiApp, Key, Path, Replace question controls after Textual has completed child removal. (+15 more)

### Community 4 - "app.py"
Cohesion: 0.07
Nodes (27): datetime, TaskMemoryStoreTests, TokenUsageTests, Path, Small local JSON stores for persistent task history., Persist task history and the most recently opened project., Return the remembered project path, if the memory contains one., Set the single project marker without losing task records. (+19 more)

### Community 5 - "TokenUsageStore"
Cohesion: 0.29
Nodes (6): Applying answers, Bridge Agent Profile, Build-loop tasking, cp_doc structure, Hard rules, Purpose

### Community 6 - "GitWorktreeManager"
Cohesion: 0.33
Nodes (4): Strip, Style, Render a line with the final-message color before selection styling., Render the native cursor without a background in visible modes.

### Community 7 - "Daedalus TUI Local Token Usage Memory"
Cohesion: 0.29
Nodes (6): Daedalus TUI Local Persistent Memory, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 8 - "update_repository"
Cohesion: 0.28
Nodes (10): ConfigTests, CodingStatisticsSettings, load_coding_statistics_settings(), load_orchestration_settings(), load_tui_settings(), ModelOption, _options(), Path (+2 more)

### Community 11 - "Key"
Cohesion: 0.07
Nodes (37): EventCallback, IntegrationGate, GraphifyTests, OrchestratorTests, PromptTests, VerificationTests, AgentControl, AgentResult (+29 more)

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
Nodes (19): TaskEventCallback, FakeOrchestrator, TaskCoordinatorTests, OrchestrationResult, OrchestrationSettings, IntegrationCoordinator, Path, Concurrent task state and serialized local integration. (+11 more)

### Community 22 - "._set_status"
Cohesion: 0.31
Nodes (4): FakeRunner, settings(), DaedalusProject, A repository recognized by the presence of a ``feature_files`` folder.

### Community 23 - "update_repository"
Cohesion: 0.07
Nodes (23): AbstractEventLoop, BaseException, Exception, Cancel active agents before ThreadPoolExecutor joins its workers.      CPython e, Stop agents before an explicit Textual exit begins., Persist Textual failures that would otherwise only flash on screen., Cover terminal and event-loop exits that bypass Textual unmount., Run before ThreadPoolExecutor's internal interpreter-exit join. (+15 more)

### Community 24 - "Daedalus TUI Coding Statistics"
Cohesion: 0.29
Nodes (6): Daedalus TUI Coding Statistics, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 25 - "._usage_entries"
Cohesion: 0.12
Nodes (10): GitWorktreeTests, GitWorktreeManager, CompletedProcess, Path, Compatibility alias for callers that used the original private helper., Stage the current worktree contents for orchestration checks or commit., Remove graphify output changes from an agent worktree.          Graphify refresh, Keep a read-only planning pass from becoming an implementation change. (+2 more)

### Community 26 - ".provider_split"
Cohesion: 0.31
Nodes (5): ProjectDiscoveryTests, discover_projects(), Path, Discovery of Daedalus-supported repositories beneath a launch root., Recursively find folders containing a direct ``feature_files`` child.      Git m

### Community 27 - "CodingStatisticsScreen"
Cohesion: 0.36
Nodes (3): CodingStatisticsScreen, _format_tokens(), Show token usage history and derived coding statistics.

### Community 28 - "KeyboardShortcutsScreen"
Cohesion: 0.33
Nodes (3): ComposeResult, KeyboardShortcutsScreen, Modal reference for the app and prompt editor keyboard shortcuts.

### Community 29 - "PlanAnswerSelect"
Cohesion: 0.33
Nodes (4): Mount, Select, PlanAnswerSelect, Initialize dynamic plan selectors after their nested children mount.

## Knowledge Gaps
- **49 isolated node(s):** `daedalus-tui`, `Execution Boundaries (CRITICAL)`, `Evidence Extraction`, `Architecture Boundaries`, `Parameter Files` (+44 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DaedalusTuiApp` connect `DaedalusTuiApp` to `PlanQuestion`, `DaedalusVimTextArea`, `AgentRunner`, `app.py`, `update_repository`, `.__init__`, `._shutdown_coordinators`, `._set_status`, `update_repository`, `CodingStatisticsScreen`, `KeyboardShortcutsScreen`?**
  _High betweenness centrality (0.227) - this node is a cross-community bridge._
- **Why does `AgentRunner` connect `AgentRunner` to `PlanQuestion`, `DaedalusTuiApp`, `update_repository`, `Key`, `.__init__`, `CodingStatisticsScreen`, `KeyboardShortcutsScreen`, `PlanAnswerSelect`?**
  _High betweenness centrality (0.137) - this node is a cross-community bridge._
- **Why does `DaedalusVimTextArea` connect `DaedalusVimTextArea` to `PlanQuestion`, `DaedalusTuiApp`, `GitWorktreeManager`, `update_repository`, `._shutdown_coordinators`, `._set_status`, `update_repository`, `CodingStatisticsScreen`, `KeyboardShortcutsScreen`, `PlanAnswerSelect`?**
  _High betweenness centrality (0.104) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `DaedalusTuiApp` (e.g. with `FakeCoordinator` and `FakeRunner`) actually correct?**
  _`DaedalusTuiApp` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `TuiAppTests` (e.g. with `CodingStatisticsScreen` and `DaedalusTuiApp`) actually correct?**
  _`TuiAppTests` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `TaskCoordinator` (e.g. with `FakeOrchestrator` and `TaskCoordinatorTests`) actually correct?**
  _`TaskCoordinator` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `AgentRunner` (e.g. with `AgentRunnerTests` and `FakeProcess`) actually correct?**
  _`AgentRunner` has 15 INFERRED edges - model-reasoned connections that need verification._