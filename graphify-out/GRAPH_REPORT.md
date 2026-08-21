# Graph Report - daedalus-tui  (2026-08-20)

## Corpus Check
- 48 files · ~30,967 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 732 nodes · 1955 edges · 36 communities (32 shown, 4 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 225 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `77a46711`
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

## God Nodes (most connected - your core abstractions)
1. `DaedalusTuiApp` - 99 edges
2. `TuiAppTests` - 62 edges
3. `TaskCoordinator` - 60 edges
4. `AgentRunner` - 53 edges
5. `GitWorktreeManager` - 51 edges
6. `OrchestrationSettings` - 50 edges
7. `TaskRecord` - 49 edges
8. `DaedalusVimTextArea` - 48 edges
9. `WorktreeContext` - 47 edges
10. `TaskMemoryStore` - 38 edges

## Surprising Connections (you probably didn't know these)
- `FakeRunner` --uses--> `DaedalusTuiApp`  [INFERRED]
  tests/test_app.py → tui/app.py
- `FakeRunner` --uses--> `PlanOption`  [INFERRED]
  tests/test_app.py → tui/plan.py
- `FakeRunner` --uses--> `PlanQuestion`  [INFERRED]
  tests/test_app.py → tui/plan.py
- `FakeRunner` --uses--> `TaskRecord`  [INFERRED]
  tests/test_app.py → tui/task_coordinator.py
- `FakeRunner` --uses--> `DaedalusVimTextArea`  [INFERRED]
  tests/test_app.py → tui/vim_text_area.py

## Import Cycles
- None detected.

## Communities (36 total, 4 thin omitted)

### Community 0 - "PlanQuestion"
Cohesion: 0.26
Nodes (4): Path, Render actionable history and tasks created during this session., Keep failures, active work, and all tasks submitted in this launch., Switch the project context and focus a row selected in the inbox.

### Community 1 - "DaedalusVimTextArea"
Cohesion: 0.05
Nodes (16): FakeCoordinator, TuiAppTests, DaedalusVimTextArea, Key, Keep Enter as a newline; Ctrl+Enter remains the app submit key., Route visual-line mode and mirror new yanks to the host clipboard., Add Daedalus prompt commands that the dependency does not provide., VimTextArea with multiline prompt behavior and system clipboard sync. (+8 more)

### Community 2 - "AgentRunner"
Cohesion: 0.06
Nodes (23): OutputCallback, AgentRunnerTests, FakeProcess, FakeStream, InterruptibleProcess, Thread, AgentControl, AgentLogEvent (+15 more)

### Community 3 - "DaedalusTuiApp"
Cohesion: 0.12
Nodes (5): Pressed, DaedalusTuiApp, Clear the selected task and unlock a fresh prompt editor., Use Textual's OSC 52 path and a native clipboard fallback., Keep a task visible after user activity during this launch.

### Community 4 - "app.py"
Cohesion: 0.12
Nodes (8): CompletedProcess, Path, Commit only the generated graph after a successful primary update., Remove a cancelled task even when its branch was never integrated., Compatibility alias for callers that used the original private helper., Stage the current worktree contents for orchestration checks or commit., Remove graphify output changes from an agent worktree.          Graphify refresh, Keep a read-only planning pass from becoming an implementation change.

### Community 5 - "TokenUsageStore"
Cohesion: 0.29
Nodes (6): Applying answers, Bridge Agent Profile, Build-loop tasking, cp_doc structure, Hard rules, Purpose

### Community 6 - "GitWorktreeManager"
Cohesion: 0.11
Nodes (12): Log, Strip, Style, Selectable transcript rendering with semantic assistant-message emphasis., A selectable log that can emphasize a task's final assistant message.      ``Log, Return the tone assigned to each rendered transcript line., Use the prompt's normal text color for the final transcript tone., Re-render lines after a surrounding widget's color state changes. (+4 more)

### Community 7 - "Daedalus TUI Local Token Usage Memory"
Cohesion: 0.29
Nodes (6): Daedalus TUI Local Persistent Memory, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 8 - "update_repository"
Cohesion: 0.06
Nodes (38): ComposeResult, Mount, Select, FakeRunner, settings(), ConfigTests, ProjectDiscoveryTests, CodingStatisticsScreen (+30 more)

### Community 11 - "Key"
Cohesion: 0.22
Nodes (7): EventCallback, IntegrationGate, AgentStopped, Path, RuntimeError, Load a repository-owned profile immediately before building a prompt., Expose usage only after the whole task reaches completion.

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
Nodes (26): TaskEventCallback, FakeOrchestrator, TaskCoordinatorTests, OrchestrationResult, OrchestrationSettings, IntegrationCoordinator, _nonnegative_int(), _phase_for_status() (+18 more)

### Community 21 - "._shutdown_coordinators"
Cohesion: 0.16
Nodes (21): Any, PlanTests, Replace question controls after Textual has completed child removal., build_implementation_prompt(), build_plan_followup_prompt(), custom_answer_text(), encode_custom_answer(), is_valid_plan_answer() (+13 more)

### Community 22 - "._set_status"
Cohesion: 0.15
Nodes (7): Exception, Stop agents before an explicit Textual exit begins., Persist Textual failures that would otherwise only flash on screen., Clean up if Textual's run loop returns without its unmount hook., Idempotently detach task callbacks and request child-process shutdown., _unregister_app_for_thread_exit(), close_fault_handler()

### Community 23 - "update_repository"
Cohesion: 0.15
Nodes (12): Pause active agents before ThreadPoolExecutor joins its workers.      CPython ex, Cover terminal and event-loop exits that bypass Textual unmount., Run before ThreadPoolExecutor's internal interpreter-exit join., _register_app_for_thread_exit(), _shutdown_apps_before_thread_join(), configure_debug_logging(), install_fault_handler(), _install_thread_exception_logging() (+4 more)

### Community 24 - "Daedalus TUI Coding Statistics"
Cohesion: 0.29
Nodes (6): Daedalus TUI Coding Statistics, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 25 - "DaedalusVimTextArea"
Cohesion: 0.20
Nodes (8): GitWorktreeTests, GitWorktreeError, GitWorktreeManager, RuntimeError, Local Git worktree lifecycle used by the standalone orchestrator., Install project resources and link declared shared read-only paths., ProjectWorktreeSettings, Install and shared-path settings from a target project's .daedalus file.

### Community 26 - ".provider_split"
Cohesion: 0.35
Nodes (6): OrchestratorTests, AgentResult, WorktreeContext, GraphifyResult, LocalOrchestrator, VerificationResult

### Community 27 - "test_app.py"
Cohesion: 0.29
Nodes (6): PromptTests, build_repair_prompt(), build_resolver_prompt(), build_task_prompt(), _embedded_profile(), Prompt wrappers used by task and resolver agents.

### Community 28 - "log_exception"
Cohesion: 0.17
Nodes (6): AbstractEventLoop, BaseException, Promote only events that need the user's attention in the inbox., Keep one bad dynamic widget update from closing the entire TUI., log_exception(), main()

### Community 29 - "CodingStatisticsScreen"
Cohesion: 0.25
Nodes (9): VerificationTests, Single-run local agent orchestration without daemon or database dependencies., discover_commands(), format_process_result(), package_has_test_script(), CompletedProcess, Path, Local verification discovery and execution. (+1 more)

### Community 30 - "calculate_token_usage"
Cohesion: 0.07
Nodes (27): datetime, TaskMemoryStoreTests, TokenUsageTests, Path, Small local JSON stores for persistent task history., Upsert a task snapshot keyed by the task worktree's directory name., Persist task history and the most recently opened project., Return the remembered project path, if the memory contains one. (+19 more)

### Community 31 - "PlanAnswerSelect"
Cohesion: 0.23
Nodes (6): GraphifyTests, Path, Best-effort graph refresh owned by the local orchestration layer., Refresh the primary repository graph without affecting task success., update_repository(), Refresh graph metadata after promotion without blocking the task.

### Community 32 - "discover_projects"
Cohesion: 0.29
Nodes (6): ProjectConfigTests, load_project_worktree_settings(), Path, Configuration supplied by a target project to prepare task worktrees., Load optional worktree provisioning settings from a target repository., _string_array()

### Community 34 - "._render_line_strip"
Cohesion: 0.27
Nodes (3): Key, Return a TextArea selection or the active screen selection., Add Vim-like navigation without changing TextArea insert behavior.

## Knowledge Gaps
- **49 isolated node(s):** `daedalus-tui`, `Execution Boundaries (CRITICAL)`, `Evidence Extraction`, `Architecture Boundaries`, `Parameter Files` (+44 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DaedalusTuiApp` connect `DaedalusTuiApp` to `PlanQuestion`, `DaedalusVimTextArea`, `AgentRunner`, `._render_line_strip`, `CodingStatisticsScreen`, `.on_data_table_row_selected`, `GitWorktreeManager`, `update_repository`, `.__init__`, `._shutdown_coordinators`, `._set_status`, `update_repository`, `log_exception`, `calculate_token_usage`?**
  _High betweenness centrality (0.215) - this node is a cross-community bridge._
- **Why does `AgentRunner` connect `AgentRunner` to `DaedalusTuiApp`, `update_repository`, `Key`, `.__init__`, `.provider_split`, `CodingStatisticsScreen`?**
  _High betweenness centrality (0.134) - this node is a cross-community bridge._
- **Why does `TaskRecord` connect `.__init__` to `PlanQuestion`, `DaedalusVimTextArea`, `CodingStatisticsScreen`, `DaedalusTuiApp`, `AgentRunner`, `update_repository`, `._shutdown_coordinators`, `DaedalusVimTextArea`, `.provider_split`, `log_exception`, `calculate_token_usage`?**
  _High betweenness centrality (0.106) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `DaedalusTuiApp` (e.g. with `FakeCoordinator` and `FakeRunner`) actually correct?**
  _`DaedalusTuiApp` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `TuiAppTests` (e.g. with `CodingStatisticsScreen` and `DaedalusTuiApp`) actually correct?**
  _`TuiAppTests` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `TaskCoordinator` (e.g. with `FakeOrchestrator` and `TaskCoordinatorTests`) actually correct?**
  _`TaskCoordinator` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `AgentRunner` (e.g. with `AgentRunnerTests` and `FakeProcess`) actually correct?**
  _`AgentRunner` has 15 INFERRED edges - model-reasoned connections that need verification._