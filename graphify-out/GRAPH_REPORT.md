# Graph Report - daedalus-tui  (2026-08-23)

## Corpus Check
- 57 files · ~37,712 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 836 nodes · 2153 edges · 41 communities (34 shown, 7 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 236 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `79df693f`
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
- DaedalusVimTextArea
- .provider_split
- test_app.py
- log_exception
- CodingStatisticsScreen
- calculate_token_usage
- PlanAnswerSelect
- discover_projects
- CodingStatisticsScreen
- ._render_line_strip
- .on_data_table_row_selected
- architecture.md
- integrating.md
- ._start_new_task
- Daedalus Project Instructions
- README.md

## God Nodes (most connected - your core abstractions)
1. `DaedalusTuiApp` - 102 edges
2. `TuiAppTests` - 64 edges
3. `TaskCoordinator` - 61 edges
4. `GitWorktreeManager` - 60 edges
5. `AgentRunner` - 54 edges
6. `OrchestrationSettings` - 50 edges
7. `TaskRecord` - 50 edges
8. `WorktreeContext` - 49 edges
9. `DaedalusVimTextArea` - 49 edges
10. `TaskMemoryStore` - 39 edges

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

## Communities (41 total, 7 thin omitted)

### Community 0 - "PlanQuestion"
Cohesion: 0.20
Nodes (4): Path, Render actionable history and tasks created during this session., Keep failures, active work, and all tasks submitted in this launch., Switch the project context and focus a row selected in the inbox.

### Community 2 - "AgentRunner"
Cohesion: 0.07
Nodes (18): OutputCallback, AgentRunnerTests, FakeProcess, FakeStream, InterruptibleProcess, Thread, AgentLogEvent, AgentRequest (+10 more)

### Community 3 - "DaedalusTuiApp"
Cohesion: 0.16
Nodes (5): DaedalusTuiApp, Key, Keep a task visible after user activity during this launch., Return a TextArea selection or the active screen selection., Add Vim-like navigation without changing TextArea insert behavior.

### Community 4 - "app.py"
Cohesion: 0.06
Nodes (15): DaedalusVimTextArea, Key, The Daedalus prompt's incremental Vim editing adapter., Keep Enter as a newline; Ctrl+Enter remains the app submit key., Route visual-line mode and mirror new yanks to the host clipboard., Add Daedalus prompt commands that the dependency does not provide., VimTextArea with multiline prompt behavior and system clipboard sync., Select the current line and enter Vim visual-line mode. (+7 more)

### Community 5 - "TokenUsageStore"
Cohesion: 0.29
Nodes (6): Applying answers, Bridge Agent Profile, Build-loop tasking, cp_doc structure, Hard rules, Purpose

### Community 6 - "GitWorktreeManager"
Cohesion: 0.06
Nodes (23): ComposeResult, Log, Mount, Resize, Select, Strip, Style, PlanAnswerSelect (+15 more)

### Community 7 - "Daedalus TUI Local Token Usage Memory"
Cohesion: 0.29
Nodes (6): Daedalus TUI Local Persistent Memory, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 8 - "update_repository"
Cohesion: 0.14
Nodes (13): ConfigTests, CodingStatisticsScreen, _format_count(), _format_tokens(), Show token or task usage history and derived coding statistics., CodingStatisticsSettings, load_coding_statistics_settings(), load_orchestration_settings() (+5 more)

### Community 11 - "Key"
Cohesion: 0.07
Nodes (33): EventCallback, IntegrationGate, GraphifyTests, OrchestratorTests, VerificationTests, AgentControl, AgentResult, Provider-specific subprocess execution with normalized agent messages. (+25 more)

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
Cohesion: 0.08
Nodes (25): TaskEventCallback, FakeOrchestrator, TaskCoordinatorTests, OrchestrationSettings, IntegrationCoordinator, _nonnegative_int(), _phase_for_status(), Path (+17 more)

### Community 21 - "._shutdown_coordinators"
Cohesion: 0.07
Nodes (40): Any, PlanTests, ProjectDiscoveryTests, Textual interface for concurrent local agent tasks., Use Textual's OSC 52 path and a native clipboard fallback., copy_to_system_clipboard(), paste_from_system_clipboard(), System clipboard helpers for terminals without OSC 52 support. (+32 more)

### Community 22 - "._set_status"
Cohesion: 0.15
Nodes (7): Exception, Stop agents before an explicit Textual exit begins., Persist Textual failures that would otherwise only flash on screen., Clean up if Textual's run loop returns without its unmount hook., Idempotently detach task callbacks and request child-process shutdown., _unregister_app_for_thread_exit(), close_fault_handler()

### Community 23 - "update_repository"
Cohesion: 0.25
Nodes (5): Pause active agents before ThreadPoolExecutor joins its workers.      CPython ex, Cover terminal and event-loop exits that bypass Textual unmount., Run before ThreadPoolExecutor's internal interpreter-exit join., _register_app_for_thread_exit(), _shutdown_apps_before_thread_join()

### Community 24 - "Daedalus TUI Coding Statistics"
Cohesion: 0.29
Nodes (6): Daedalus TUI Coding Statistics, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 25 - "DaedalusVimTextArea"
Cohesion: 0.07
Nodes (26): GitWorktreeTests, ProjectConfigTests, GitWorktreeError, GitWorktreeManager, CompletedProcess, Path, RuntimeError, Local Git worktree lifecycle used by the standalone orchestrator. (+18 more)

### Community 26 - ".provider_split"
Cohesion: 0.12
Nodes (21): Pressed, ProgressCallback, Submitted, ProjectInitializerTests, ProjectInitializerScreen, Collect a project slug and create a Daedalus-compatible directory., find_github_url(), initialize_project() (+13 more)

### Community 27 - "test_app.py"
Cohesion: 0.29
Nodes (6): PromptTests, build_repair_prompt(), build_resolver_prompt(), build_task_prompt(), _embedded_profile(), Prompt wrappers used by task and resolver agents.

### Community 28 - "log_exception"
Cohesion: 0.15
Nodes (6): AbstractEventLoop, BaseException, Keep one bad dynamic widget update from closing the entire TUI., Promote only events that need the user's attention in the inbox., log_exception(), main()

### Community 29 - "CodingStatisticsScreen"
Cohesion: 0.11
Nodes (8): FakeCoordinator, FakeRunner, settings(), KeyboardShortcutsScreen, Modal reference for the app and prompt editor keyboard shortcuts., TuiSettings, DaedalusProject, A repository recognized by the presence of a ``feature_files`` folder.

### Community 30 - "calculate_token_usage"
Cohesion: 0.07
Nodes (27): datetime, TaskMemoryStoreTests, TokenUsageTests, Path, Small local JSON stores for persistent task history., Upsert a task snapshot keyed by the task worktree's directory name., Persist task history and the most recently opened project., Return the remembered project path, if the memory contains one. (+19 more)

### Community 31 - "PlanAnswerSelect"
Cohesion: 0.29
Nodes (6): Daedalus TUI Project Initialization, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 32 - "discover_projects"
Cohesion: 0.29
Nodes (6): 4-Stage Development Lifecycle, Alignment, Debugging, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization

### Community 34 - "._render_line_strip"
Cohesion: 0.29
Nodes (6): 4-Stage Development Lifecycle, Alignment, Debugging, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization

### Community 36 - "architecture.md"
Cohesion: 0.33
Nodes (5): 4-Stage Development Lifecycle, Evidence Extraction, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization

### Community 37 - "integrating.md"
Cohesion: 0.40
Nodes (4): 4-Stage Development Lifecycle, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization

### Community 39 - "Daedalus Project Instructions"
Cohesion: 0.50
Nodes (3): Daedalus Project Instructions, graphify, Task mode

## Knowledge Gaps
- **78 isolated node(s):** `daedalus-tui`, `Execution Boundaries (CRITICAL)`, `Evidence Extraction`, `Architecture Boundaries`, `Parameter Files` (+73 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DaedalusTuiApp` connect `DaedalusTuiApp` to `PlanQuestion`, `DaedalusVimTextArea`, `AgentRunner`, `CodingStatisticsScreen`, `.on_data_table_row_selected`, `app.py`, `._start_new_task`, `GitWorktreeManager`, `update_repository`, `Key`, `.__init__`, `._shutdown_coordinators`, `._set_status`, `update_repository`, `log_exception`, `CodingStatisticsScreen`, `calculate_token_usage`?**
  _High betweenness centrality (0.186) - this node is a cross-community bridge._
- **Why does `AgentRunner` connect `AgentRunner` to `PlanQuestion`, `DaedalusTuiApp`, `GitWorktreeManager`, `update_repository`, `Key`, `.__init__`, `._shutdown_coordinators`, `.provider_split`, `CodingStatisticsScreen`?**
  _High betweenness centrality (0.117) - this node is a cross-community bridge._
- **Why does `TaskRecord` connect `.__init__` to `PlanQuestion`, `DaedalusVimTextArea`, `CodingStatisticsScreen`, `DaedalusTuiApp`, `AgentRunner`, `GitWorktreeManager`, `update_repository`, `Key`, `._shutdown_coordinators`, `DaedalusVimTextArea`, `.provider_split`, `log_exception`, `CodingStatisticsScreen`, `calculate_token_usage`?**
  _High betweenness centrality (0.097) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `DaedalusTuiApp` (e.g. with `FakeCoordinator` and `FakeRunner`) actually correct?**
  _`DaedalusTuiApp` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `TuiAppTests` (e.g. with `CodingStatisticsScreen` and `DaedalusTuiApp`) actually correct?**
  _`TuiAppTests` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `TaskCoordinator` (e.g. with `FakeOrchestrator` and `TaskCoordinatorTests`) actually correct?**
  _`TaskCoordinator` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `GitWorktreeManager` (e.g. with `GitWorktreeTests` and `ProjectWorktreeSettings`) actually correct?**
  _`GitWorktreeManager` has 9 INFERRED edges - model-reasoned connections that need verification._