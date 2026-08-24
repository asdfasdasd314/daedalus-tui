# Graph Report - daedalus-tui  (2026-08-23)

## Corpus Check
- 57 files · ~39,994 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 867 nodes · 2251 edges · 47 communities (41 shown, 6 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 239 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f3e0d9d9`
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
- KeyboardShortcutsScreen
- orchestrator.py
- DaedalusProject
- orchestrator.py
- discover_projects
- update_repository

## God Nodes (most connected - your core abstractions)
1. `DaedalusTuiApp` - 109 edges
2. `TuiAppTests` - 69 edges
3. `TaskCoordinator` - 62 edges
4. `GitWorktreeManager` - 60 edges
5. `AgentRunner` - 54 edges
6. `OrchestrationSettings` - 53 edges
7. `WorktreeContext` - 51 edges
8. `DaedalusVimTextArea` - 51 edges
9. `TaskRecord` - 50 edges
10. `TaskMemoryStore` - 45 edges

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

## Communities (47 total, 6 thin omitted)

### Community 0 - "PlanQuestion"
Cohesion: 0.21
Nodes (5): Path, Render actionable history and tasks created during this session., Keep failures, active work, and all tasks submitted in this launch., Switch the project context and focus a row selected in the inbox., Memory override for the project, else the parameter-file default.

### Community 2 - "AgentRunner"
Cohesion: 0.07
Nodes (18): OutputCallback, AgentRunnerTests, FakeProcess, FakeStream, InterruptibleProcess, Thread, AgentLogEvent, AgentRequest (+10 more)

### Community 3 - "DaedalusTuiApp"
Cohesion: 0.06
Nodes (28): GitWorktreeTests, ProjectConfigTests, GitWorktreeError, GitWorktreeManager, list_local_branches(), CompletedProcess, Path, RuntimeError (+20 more)

### Community 4 - "app.py"
Cohesion: 0.06
Nodes (16): DaedalusVimTextArea, Key, Keep Enter as a newline; Ctrl+Enter remains the app submit key., Route visual-line mode and mirror new yanks to the host clipboard., Paste Vim's register, falling back to the system clipboard., Paste before the cursor, including from the system clipboard., Add Daedalus prompt commands that the dependency does not provide., VimTextArea with multiline prompt behavior and system clipboard sync. (+8 more)

### Community 5 - "TokenUsageStore"
Cohesion: 0.29
Nodes (6): Applying answers, Bridge Agent Profile, Build-loop tasking, cp_doc structure, Hard rules, Purpose

### Community 6 - "GitWorktreeManager"
Cohesion: 0.05
Nodes (26): Log, Mount, Resize, Select, Strip, Style, CodingStatisticsScreen, _format_count() (+18 more)

### Community 7 - "Daedalus TUI Local Token Usage Memory"
Cohesion: 0.29
Nodes (6): Daedalus TUI Local Persistent Memory, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 8 - "update_repository"
Cohesion: 0.15
Nodes (12): ConfigTests, ProjectDiscoveryTests, CodingStatisticsSettings, load_coding_statistics_settings(), load_orchestration_settings(), load_tui_settings(), _options(), Path (+4 more)

### Community 11 - "Key"
Cohesion: 0.25
Nodes (6): OrchestratorTests, AgentResult, GraphifyResult, Best-effort graph refresh owned by the local orchestration layer., LocalOrchestrator, VerificationResult

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
Nodes (21): TaskEventCallback, TaskCoordinatorTests, OrchestrationSettings, _nonnegative_int(), _phase_for_status(), Path, Submit independent prompts while sharing a serialized integration gate., Send selected plan answers back to the planning agent for confirmation. (+13 more)

### Community 22 - "._set_status"
Cohesion: 0.18
Nodes (6): Exception, Stop agents before an explicit Textual exit begins., Persist Textual failures that would otherwise only flash on screen., Run before ThreadPoolExecutor's internal interpreter-exit join., Clean up if Textual's run loop returns without its unmount hook., Idempotently detach task callbacks and request child-process shutdown.

### Community 23 - "update_repository"
Cohesion: 0.10
Nodes (23): BaseException, Provider-specific subprocess execution with normalized agent messages., Textual interface for concurrent local agent tasks., Pause active agents before ThreadPoolExecutor joins its workers.      CPython ex, _shutdown_apps_before_thread_join(), _unregister_app_for_thread_exit(), copy_to_system_clipboard(), paste_from_system_clipboard() (+15 more)

### Community 24 - "Daedalus TUI Coding Statistics"
Cohesion: 0.29
Nodes (6): Daedalus TUI Coding Statistics, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 25 - "DaedalusVimTextArea"
Cohesion: 0.28
Nodes (4): FakeOrchestrator, OrchestrationResult, IntegrationCoordinator, Run ready integration operations one at a time in ready order.

### Community 26 - ".provider_split"
Cohesion: 0.10
Nodes (22): ComposeResult, Pressed, ProgressCallback, Submitted, ProjectInitializerTests, ProjectInitializerScreen, Collect a project slug and create a Daedalus-compatible directory., find_github_url() (+14 more)

### Community 27 - "test_app.py"
Cohesion: 0.29
Nodes (6): PromptTests, build_repair_prompt(), build_resolver_prompt(), build_task_prompt(), _embedded_profile(), Prompt wrappers used by task and resolver agents.

### Community 28 - "log_exception"
Cohesion: 0.20
Nodes (3): Keep one bad dynamic widget update from closing the entire TUI., Clear the selected task and unlock a fresh prompt editor., Promote only events that need the user's attention in the inbox.

### Community 29 - "CodingStatisticsScreen"
Cohesion: 0.11
Nodes (9): FakeCoordinator, FakeRunner, settings(), KeyboardShortcutsScreen, Modal reference for the app and prompt editor keyboard shortcuts., ModelOption, TuiSettings, DaedalusProject (+1 more)

### Community 30 - "calculate_token_usage"
Cohesion: 0.11
Nodes (12): TaskMemoryStoreTests, Path, Remove one project's operating-branch override (absent = use default)., Return persisted task snapshots keyed by their stable task ID., Upsert a task snapshot keyed by the task worktree's directory name., Persist task history, last project, and per-project target branches., Return the remembered project path, if the memory contains one., Set the single project marker without losing task records. (+4 more)

### Community 31 - "PlanAnswerSelect"
Cohesion: 0.29
Nodes (6): Daedalus TUI Project Initialization, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 32 - "discover_projects"
Cohesion: 0.29
Nodes (6): 4-Stage Development Lifecycle, Alignment, Debugging, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization

### Community 33 - "CodingStatisticsScreen"
Cohesion: 0.14
Nodes (22): Any, PlanTests, Replace question controls after Textual has completed child removal., Small local JSON stores for persistent task history., build_implementation_prompt(), build_plan_followup_prompt(), custom_answer_text(), encode_custom_answer() (+14 more)

### Community 34 - "._render_line_strip"
Cohesion: 0.29
Nodes (6): 4-Stage Development Lifecycle, Alignment, Debugging, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization

### Community 35 - ".on_data_table_row_selected"
Cohesion: 0.13
Nodes (18): datetime, TokenUsageTests, calculate_token_usage(), merge_usage_entries(), _parse_timestamp(), Token usage records and derived coding statistics., The token usage attributed to one submitted task., Convert persisted task snapshots into usage records. (+10 more)

### Community 36 - "architecture.md"
Cohesion: 0.33
Nodes (5): 4-Stage Development Lifecycle, Evidence Extraction, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization

### Community 37 - "integrating.md"
Cohesion: 0.40
Nodes (4): 4-Stage Development Lifecycle, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization

### Community 38 - "._start_new_task"
Cohesion: 0.27
Nodes (3): Key, Return a TextArea selection or the active screen selection., Add Vim-like navigation without changing TextArea insert behavior.

### Community 39 - "Daedalus Project Instructions"
Cohesion: 0.50
Nodes (3): Daedalus Project Instructions, graphify, Task mode

### Community 41 - "KeyboardShortcutsScreen"
Cohesion: 0.16
Nodes (9): EventCallback, IntegrationGate, AgentControl, Cooperative stop signals shared by a task and its active subprocess., AgentStopped, Path, RuntimeError, Load a repository-owned profile immediately before building a prompt. (+1 more)

### Community 42 - "orchestrator.py"
Cohesion: 0.15
Nodes (5): AbstractEventLoop, Changed, DaedalusTuiApp, Use Textual's OSC 52 path and a native clipboard fallback., __getattr__()

### Community 43 - "DaedalusProject"
Cohesion: 0.22
Nodes (4): Cover terminal and event-loop exits that bypass Textual unmount., Update the project's coordinator so later submits use ``branch``., Refresh Branch Select options for the active project and sync coordinator., _register_app_for_thread_exit()

### Community 44 - "orchestrator.py"
Cohesion: 0.25
Nodes (9): VerificationTests, Single-run local agent orchestration without daemon or database dependencies., discover_commands(), format_process_result(), package_has_test_script(), CompletedProcess, Path, Local verification discovery and execution. (+1 more)

### Community 47 - "update_repository"
Cohesion: 0.27
Nodes (5): GraphifyTests, Path, Refresh the primary repository graph without affecting task success., update_repository(), Refresh graph metadata after promotion without blocking the task.

## Knowledge Gaps
- **78 isolated node(s):** `daedalus-tui`, `Execution Boundaries (CRITICAL)`, `Evidence Extraction`, `Architecture Boundaries`, `Parameter Files` (+73 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DaedalusTuiApp` connect `orchestrator.py` to `PlanQuestion`, `DaedalusVimTextArea`, `AgentRunner`, `CodingStatisticsScreen`, `.on_data_table_row_selected`, `app.py`, `._start_new_task`, `GitWorktreeManager`, `update_repository`, `DaedalusProject`, `discover_projects`, `.__init__`, `._shutdown_coordinators`, `._set_status`, `update_repository`, `log_exception`, `CodingStatisticsScreen`, `calculate_token_usage`?**
  _High betweenness centrality (0.194) - this node is a cross-community bridge._
- **Why does `AgentRunner` connect `AgentRunner` to `CodingStatisticsScreen`, `GitWorktreeManager`, `update_repository`, `KeyboardShortcutsScreen`, `orchestrator.py`, `Key`, `orchestrator.py`, `.__init__`, `update_repository`, `DaedalusVimTextArea`, `.provider_split`, `CodingStatisticsScreen`?**
  _High betweenness centrality (0.113) - this node is a cross-community bridge._
- **Why does `TaskRecord` connect `.__init__` to `PlanQuestion`, `DaedalusVimTextArea`, `CodingStatisticsScreen`, `AgentRunner`, `DaedalusTuiApp`, `GitWorktreeManager`, `KeyboardShortcutsScreen`, `orchestrator.py`, `Key`, `._shutdown_coordinators`, `update_repository`, `DaedalusVimTextArea`, `.provider_split`, `log_exception`, `CodingStatisticsScreen`, `calculate_token_usage`?**
  _High betweenness centrality (0.092) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `DaedalusTuiApp` (e.g. with `FakeCoordinator` and `FakeRunner`) actually correct?**
  _`DaedalusTuiApp` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `TuiAppTests` (e.g. with `CodingStatisticsScreen` and `DaedalusTuiApp`) actually correct?**
  _`TuiAppTests` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `TaskCoordinator` (e.g. with `FakeOrchestrator` and `TaskCoordinatorTests`) actually correct?**
  _`TaskCoordinator` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `GitWorktreeManager` (e.g. with `GitWorktreeTests` and `ProjectWorktreeSettings`) actually correct?**
  _`GitWorktreeManager` has 9 INFERRED edges - model-reasoned connections that need verification._