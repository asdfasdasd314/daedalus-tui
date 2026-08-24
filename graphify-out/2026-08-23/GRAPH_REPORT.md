# Graph Report - daedalus-tui  (2026-08-23)

## Corpus Check
- 57 files · ~38,307 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 839 nodes · 2167 edges · 48 communities (43 shown, 5 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 236 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `154bedb9`
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
- load_project_worktree_settings
- discover_projects
- CodingStatisticsScreen
- update_repository

## God Nodes (most connected - your core abstractions)
1. `DaedalusTuiApp` - 102 edges
2. `TuiAppTests` - 64 edges
3. `TaskCoordinator` - 62 edges
4. `GitWorktreeManager` - 60 edges
5. `AgentRunner` - 54 edges
6. `OrchestrationSettings` - 53 edges
7. `WorktreeContext` - 51 edges
8. `TaskRecord` - 50 edges
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

## Communities (48 total, 5 thin omitted)

### Community 0 - "PlanQuestion"
Cohesion: 0.22
Nodes (4): Path, Render actionable history and tasks created during this session., Keep failures, active work, and all tasks submitted in this launch., Switch the project context and focus a row selected in the inbox.

### Community 1 - "DaedalusVimTextArea"
Cohesion: 0.06
Nodes (16): TuiAppTests, DaedalusVimTextArea, Key, Keep Enter as a newline; Ctrl+Enter remains the app submit key., Route visual-line mode and mirror new yanks to the host clipboard., Paste Vim's register, falling back to the system clipboard., Add Daedalus prompt commands that the dependency does not provide., VimTextArea with multiline prompt behavior and system clipboard sync. (+8 more)

### Community 2 - "AgentRunner"
Cohesion: 0.07
Nodes (18): OutputCallback, AgentRunnerTests, FakeProcess, FakeStream, InterruptibleProcess, Thread, AgentLogEvent, AgentRequest (+10 more)

### Community 3 - "DaedalusTuiApp"
Cohesion: 0.14
Nodes (4): Changed, DaedalusTuiApp, Keep a task visible after user activity during this launch., __getattr__()

### Community 4 - "app.py"
Cohesion: 0.15
Nodes (9): GitWorktreeTests, GitWorktreeError, GitWorktreeManager, RuntimeError, Local Git worktree lifecycle used by the standalone orchestrator., Install project resources and link declared shared read-only paths., ProjectWorktreeSettings, Configuration supplied by a target project to prepare task worktrees. (+1 more)

### Community 5 - "TokenUsageStore"
Cohesion: 0.29
Nodes (6): Applying answers, Bridge Agent Profile, Build-loop tasking, cp_doc structure, Hard rules, Purpose

### Community 6 - "GitWorktreeManager"
Cohesion: 0.08
Nodes (18): Log, Resize, Strip, Style, Selectable transcript rendering with semantic assistant-message emphasis., Return the width available for transcript text inside the Log., Wrap one logical line without changing its selectable text., Render a line with the final-message color before selection styling. (+10 more)

### Community 7 - "Daedalus TUI Local Token Usage Memory"
Cohesion: 0.29
Nodes (6): Daedalus TUI Local Persistent Memory, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 8 - "update_repository"
Cohesion: 0.25
Nodes (10): ConfigTests, CodingStatisticsSettings, load_coding_statistics_settings(), load_orchestration_settings(), load_tui_settings(), ModelOption, _options(), Path (+2 more)

### Community 11 - "Key"
Cohesion: 0.13
Nodes (11): EventCallback, IntegrationGate, AgentControl, Cooperative stop signals shared by a task and its active subprocess., AgentStopped, OrchestrationResult, Path, RuntimeError (+3 more)

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
Cohesion: 0.05
Nodes (49): Any, Mount, TaskEventCallback, PlanTests, FakeOrchestrator, TaskCoordinatorTests, PlanAnswerSelect, Replace question controls after Textual has completed child removal. (+41 more)

### Community 21 - "._shutdown_coordinators"
Cohesion: 0.25
Nodes (7): Textual interface for concurrent local agent tasks., copy_to_system_clipboard(), paste_from_system_clipboard(), System clipboard helpers for terminals without OSC 52 support., Read clipboard text using the native command available on the host., The Daedalus prompt's incremental Vim editing adapter., Paste before the cursor, including from the system clipboard.

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
Cohesion: 0.10
Nodes (11): CompletedProcess, Path, Keep a read-only planning pass from becoming an implementation change., Commit only the generated graph after a successful primary update., Return a directory whose HEAD matches the target branch tip.          When the r, Remove a short-lived primary checkout created for post-promotion work., Remove a cancelled task even when its branch was never integrated., Ensure the configured target branch exists and is safe to integrate into. (+3 more)

### Community 26 - ".provider_split"
Cohesion: 0.14
Nodes (19): Pressed, ProgressCallback, Submitted, ProjectInitializerTests, find_github_url(), initialize_project(), load_initializer_settings(), matching_request_marker() (+11 more)

### Community 27 - "test_app.py"
Cohesion: 0.29
Nodes (6): PromptTests, build_repair_prompt(), build_resolver_prompt(), build_task_prompt(), _embedded_profile(), Prompt wrappers used by task and resolver agents.

### Community 28 - "log_exception"
Cohesion: 0.15
Nodes (6): AbstractEventLoop, BaseException, Keep one bad dynamic widget update from closing the entire TUI., Promote only events that need the user's attention in the inbox., log_exception(), main()

### Community 30 - "calculate_token_usage"
Cohesion: 0.07
Nodes (27): datetime, TaskMemoryStoreTests, TokenUsageTests, Path, Small local JSON stores for persistent task history., Upsert a task snapshot keyed by the task worktree's directory name., Persist task history and the most recently opened project., Return the remembered project path, if the memory contains one. (+19 more)

### Community 31 - "PlanAnswerSelect"
Cohesion: 0.29
Nodes (6): Daedalus TUI Project Initialization, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 32 - "discover_projects"
Cohesion: 0.29
Nodes (6): 4-Stage Development Lifecycle, Alignment, Debugging, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization

### Community 33 - "CodingStatisticsScreen"
Cohesion: 0.22
Nodes (9): OrchestratorTests, AgentResult, Provider-specific subprocess execution with normalized agent messages., WorktreeContext, GraphifyResult, Best-effort graph refresh owned by the local orchestration layer., Standalone Textual interface and local agent orchestration., LocalOrchestrator (+1 more)

### Community 34 - "._render_line_strip"
Cohesion: 0.29
Nodes (6): 4-Stage Development Lifecycle, Alignment, Debugging, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization

### Community 36 - "architecture.md"
Cohesion: 0.33
Nodes (5): 4-Stage Development Lifecycle, Evidence Extraction, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization

### Community 37 - "integrating.md"
Cohesion: 0.40
Nodes (4): 4-Stage Development Lifecycle, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization

### Community 38 - "._start_new_task"
Cohesion: 0.15
Nodes (5): Key, Clear the selected task and unlock a fresh prompt editor., Return a TextArea selection or the active screen selection., Use Textual's OSC 52 path and a native clipboard fallback., Add Vim-like navigation without changing TextArea insert behavior.

### Community 39 - "Daedalus Project Instructions"
Cohesion: 0.50
Nodes (3): Daedalus Project Instructions, graphify, Task mode

### Community 41 - "KeyboardShortcutsScreen"
Cohesion: 0.14
Nodes (6): ComposeResult, Select, KeyboardShortcutsScreen, ProjectInitializerScreen, Modal reference for the app and prompt editor keyboard shortcuts., Collect a project slug and create a Daedalus-compatible directory.

### Community 42 - "orchestrator.py"
Cohesion: 0.25
Nodes (9): VerificationTests, Single-run local agent orchestration without daemon or database dependencies., discover_commands(), format_process_result(), package_has_test_script(), CompletedProcess, Path, Local verification discovery and execution. (+1 more)

### Community 43 - "DaedalusProject"
Cohesion: 0.31
Nodes (4): FakeRunner, settings(), DaedalusProject, A repository recognized by the presence of a ``feature_files`` folder.

### Community 44 - "load_project_worktree_settings"
Cohesion: 0.33
Nodes (5): ProjectConfigTests, load_project_worktree_settings(), Path, Load optional worktree provisioning settings from a target repository., _string_array()

### Community 45 - "discover_projects"
Cohesion: 0.31
Nodes (5): ProjectDiscoveryTests, discover_projects(), Path, Discovery of Daedalus-supported repositories beneath a launch root., Recursively find folders containing a direct ``feature_files`` child.      Git m

### Community 46 - "CodingStatisticsScreen"
Cohesion: 0.33
Nodes (4): CodingStatisticsScreen, _format_count(), _format_tokens(), Show token or task usage history and derived coding statistics.

### Community 47 - "update_repository"
Cohesion: 0.36
Nodes (4): GraphifyTests, Path, Refresh the primary repository graph without affecting task success., update_repository()

## Knowledge Gaps
- **78 isolated node(s):** `daedalus-tui`, `Execution Boundaries (CRITICAL)`, `Evidence Extraction`, `Architecture Boundaries`, `Parameter Files` (+73 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DaedalusTuiApp` connect `DaedalusTuiApp` to `PlanQuestion`, `DaedalusVimTextArea`, `AgentRunner`, `.on_data_table_row_selected`, `CodingStatisticsScreen`, `._start_new_task`, `GitWorktreeManager`, `update_repository`, `KeyboardShortcutsScreen`, `DaedalusProject`, `.__init__`, `._shutdown_coordinators`, `._set_status`, `update_repository`, `log_exception`, `CodingStatisticsScreen`, `calculate_token_usage`?**
  _High betweenness centrality (0.185) - this node is a cross-community bridge._
- **Why does `AgentRunner` connect `AgentRunner` to `CodingStatisticsScreen`, `DaedalusTuiApp`, `update_repository`, `KeyboardShortcutsScreen`, `orchestrator.py`, `Key`, `CodingStatisticsScreen`, `.__init__`, `._shutdown_coordinators`?**
  _High betweenness centrality (0.117) - this node is a cross-community bridge._
- **Why does `TaskRecord` connect `.__init__` to `PlanQuestion`, `DaedalusVimTextArea`, `CodingStatisticsScreen`, `DaedalusTuiApp`, `AgentRunner`, `app.py`, `update_repository`, `KeyboardShortcutsScreen`, `DaedalusProject`, `Key`, `CodingStatisticsScreen`, `._shutdown_coordinators`, `log_exception`, `CodingStatisticsScreen`, `calculate_token_usage`?**
  _High betweenness centrality (0.097) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `DaedalusTuiApp` (e.g. with `FakeCoordinator` and `FakeRunner`) actually correct?**
  _`DaedalusTuiApp` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `TuiAppTests` (e.g. with `CodingStatisticsScreen` and `DaedalusTuiApp`) actually correct?**
  _`TuiAppTests` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `TaskCoordinator` (e.g. with `FakeOrchestrator` and `TaskCoordinatorTests`) actually correct?**
  _`TaskCoordinator` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `GitWorktreeManager` (e.g. with `GitWorktreeTests` and `ProjectWorktreeSettings`) actually correct?**
  _`GitWorktreeManager` has 9 INFERRED edges - model-reasoned connections that need verification._