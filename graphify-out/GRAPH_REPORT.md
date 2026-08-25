# Graph Report - daedalus-tui  (2026-08-24)

## Corpus Check
- 60 files · ~44,595 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 943 nodes · 2476 edges · 48 communities (41 shown, 7 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 266 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `19747fe7`
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
- CodingStatisticsScreen
- orchestrator.py
- discover_projects
- ._usage_entries
- TokenUsageStats

## God Nodes (most connected - your core abstractions)
1. `DaedalusTuiApp` - 117 edges
2. `TuiAppTests` - 74 edges
3. `TaskCoordinator` - 70 edges
4. `GitWorktreeManager` - 60 edges
5. `OrchestrationSettings` - 58 edges
6. `AgentRunner` - 55 edges
7. `TaskRecord` - 54 edges
8. `WorktreeContext` - 53 edges
9. `DaedalusVimTextArea` - 52 edges
10. `TaskMemoryStore` - 47 edges

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

## Communities (48 total, 7 thin omitted)

### Community 0 - "PlanQuestion"
Cohesion: 0.21
Nodes (7): GraphifyTests, GraphifyResult, Path, Best-effort graph refresh owned by the local orchestration layer., Refresh the primary repository graph without affecting task success., update_repository(), Refresh graph metadata after promotion without blocking the task.

### Community 2 - "AgentRunner"
Cohesion: 0.07
Nodes (19): OutputCallback, AgentRunnerTests, FakeProcess, FakeStream, InterruptibleProcess, Thread, AgentLogEvent, AgentRequest (+11 more)

### Community 3 - "DaedalusTuiApp"
Cohesion: 0.10
Nodes (12): GitWorktreeManager, CompletedProcess, Path, Remove graphify output changes from an agent worktree.          Graphify refresh, Keep a read-only planning pass from becoming an implementation change., Commit only the generated graph after a successful primary update., Return a directory whose HEAD matches the target branch tip.          When the r, Remove a short-lived primary checkout created for post-promotion work. (+4 more)

### Community 4 - "app.py"
Cohesion: 0.25
Nodes (9): VerificationTests, Single-run local agent orchestration without daemon or database dependencies., discover_commands(), format_process_result(), package_has_test_script(), CompletedProcess, Path, Local verification discovery and execution. (+1 more)

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
Cohesion: 0.21
Nodes (8): Textual interface for concurrent local agent tasks., copy_to_system_clipboard(), paste_from_system_clipboard(), System clipboard helpers for terminals without OSC 52 support., Read clipboard text using the native command available on the host., The Daedalus prompt's incremental Vim editing adapter., Paste Vim's register, falling back to the system clipboard., Paste before the cursor, including from the system clipboard.

### Community 11 - "Key"
Cohesion: 0.21
Nodes (6): OrchestratorTests, AgentResult, Standalone Textual interface and local agent orchestration., LocalOrchestrator, Expose usage only after the whole task reaches completion., VerificationResult

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
Cohesion: 0.29
Nodes (6): 4-Stage Development Lifecycle, Debugging, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization, Topics (when tagged)

### Community 17 - "planning.md"
Cohesion: 0.29
Nodes (6): Execution Boundaries (CRITICAL), Feature File Context, Graphify, Parameter Files, Planning Boundaries, Topics (when tagged)

### Community 18 - "Daedalus TUI Project Instructions"
Cohesion: 0.40
Nodes (4): Daedalus TUI Project Instructions, graphify, Project boundaries, Task mode

### Community 19 - "integrating.md"
Cohesion: 0.40
Nodes (4): Development Lifecycle, Execution Boundaries (CRITICAL), Integration Boundaries, Parameter Files

### Community 20 - ".__init__"
Cohesion: 0.05
Nodes (50): Any, TaskEventCallback, PlanTests, FakeOrchestrator, TaskCoordinatorTests, Replace question controls after Textual has completed child removal., OrchestrationSettings, build_implementation_prompt() (+42 more)

### Community 21 - "._shutdown_coordinators"
Cohesion: 0.05
Nodes (24): Changed, RowSelected, DaedalusTuiApp, Key, Path, Update the project's coordinator so later submits use ``branch``., Refresh Branch Select options for the active project and sync coordinator., Refresh Topic Select options for the active project; default remains (None). (+16 more)

### Community 22 - "._set_status"
Cohesion: 0.29
Nodes (6): Daedalus TUI Topics, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 23 - "update_repository"
Cohesion: 0.19
Nodes (11): AbstractEventLoop, BaseException, configure_debug_logging(), install_fault_handler(), _install_thread_exception_logging(), log_exception(), Path, Persistent diagnostics for failures that occur after the Textual screen closes. (+3 more)

### Community 24 - "Daedalus TUI Coding Statistics"
Cohesion: 0.29
Nodes (6): Daedalus TUI Coding Statistics, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 25 - "DaedalusVimTextArea"
Cohesion: 0.17
Nodes (10): GitWorktreeTests, GitWorktreeError, list_local_branches(), RuntimeError, Local Git worktree lifecycle used by the standalone orchestrator., Return local branch names under ``refs/heads`` without checking anything out., Install project resources and link declared shared read-only paths., WorktreeContext (+2 more)

### Community 26 - ".provider_split"
Cohesion: 0.11
Nodes (23): ProgressCallback, ProjectConfigTests, ProjectInitializerTests, load_project_worktree_settings(), Path, Configuration supplied by a target project to prepare task worktrees., Load optional worktree provisioning settings from a target repository., _string_array() (+15 more)

### Community 27 - "test_app.py"
Cohesion: 0.10
Nodes (24): PromptTests, TopicsTests, build_repair_prompt(), build_resolver_prompt(), build_task_prompt(), _embedded_profile(), _embedded_topic(), Prompt wrappers used by task and resolver agents. (+16 more)

### Community 29 - "CodingStatisticsScreen"
Cohesion: 0.11
Nodes (11): FakeCoordinator, FakeRunner, settings(), PlanClarificationScreen, Collect a clarification about one plan question., ModelOption, TuiSettings, PlanClarification (+3 more)

### Community 30 - "calculate_token_usage"
Cohesion: 0.11
Nodes (12): TaskMemoryStoreTests, Path, Remove one project's operating-branch override (absent = use default)., Return persisted task snapshots keyed by their stable task ID., Upsert a task snapshot keyed by the task worktree's directory name., Persist task history, last project, and per-project target branches., Return the remembered project path, if the memory contains one., Set the single project marker without losing task records. (+4 more)

### Community 31 - "PlanAnswerSelect"
Cohesion: 0.29
Nodes (6): Daedalus TUI Project Initialization, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 32 - "discover_projects"
Cohesion: 0.25
Nodes (7): 4-Stage Development Lifecycle, Alignment, Debugging, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization, Topics (when tagged)

### Community 33 - "CodingStatisticsScreen"
Cohesion: 0.07
Nodes (14): DaedalusVimTextArea, Key, Keep Enter as a newline; Ctrl+Enter remains the app submit key., Route visual-line mode and mirror new yanks to the host clipboard., Add Daedalus prompt commands that the dependency does not provide., VimTextArea with multiline prompt behavior and system clipboard sync., Select the current line and enter Vim visual-line mode., Select every character in the lines between the start and cursor. (+6 more)

### Community 34 - "._render_line_strip"
Cohesion: 0.25
Nodes (7): 4-Stage Development Lifecycle, Alignment, Debugging, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization, Topics (when tagged)

### Community 35 - ".on_data_table_row_selected"
Cohesion: 0.14
Nodes (17): datetime, TokenUsageTests, Small local JSON stores for persistent task history., calculate_token_usage(), merge_usage_entries(), _parse_timestamp(), Token usage records and derived coding statistics., The token usage attributed to one submitted task. (+9 more)

### Community 36 - "architecture.md"
Cohesion: 0.33
Nodes (5): 4-Stage Development Lifecycle, Evidence Extraction, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization

### Community 37 - "integrating.md"
Cohesion: 0.40
Nodes (4): 4-Stage Development Lifecycle, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization

### Community 38 - "._start_new_task"
Cohesion: 0.08
Nodes (17): ComposeResult, Mount, Pressed, Select, Submitted, ConfigTests, PlanAnswerSelect, ProjectInitializerScreen (+9 more)

### Community 39 - "Daedalus Project Instructions"
Cohesion: 0.40
Nodes (4): Daedalus Project Instructions, graphify, Task mode, Topics

### Community 41 - "KeyboardShortcutsScreen"
Cohesion: 0.16
Nodes (10): EventCallback, IntegrationGate, AgentControl, Cooperative stop signals shared by a task and its active subprocess., AgentStopped, OrchestrationResult, Path, RuntimeError (+2 more)

### Community 42 - "CodingStatisticsScreen"
Cohesion: 0.31
Nodes (4): CodingStatisticsScreen, _format_count(), _format_tokens(), Show token or task usage history and derived coding statistics.

### Community 47 - "discover_projects"
Cohesion: 0.31
Nodes (5): ProjectDiscoveryTests, discover_projects(), Path, Discovery of Daedalus-supported repositories beneath a launch root., Recursively find folders containing a direct ``feature_files`` child.      Git m

### Community 48 - "._usage_entries"
Cohesion: 0.12
Nodes (10): Exception, Pause active agents before ThreadPoolExecutor joins its workers.      CPython ex, Stop agents before an explicit Textual exit begins., Persist Textual failures that would otherwise only flash on screen., Run before ThreadPoolExecutor's internal interpreter-exit join., Clean up if Textual's run loop returns without its unmount hook., Idempotently detach task callbacks and request child-process shutdown., _shutdown_apps_before_thread_join() (+2 more)

## Knowledge Gaps
- **88 isolated node(s):** `daedalus-tui`, `Execution Boundaries (CRITICAL)`, `Evidence Extraction`, `Architecture Boundaries`, `Parameter Files` (+83 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DaedalusTuiApp` connect `._shutdown_coordinators` to `DaedalusVimTextArea`, `AgentRunner`, `.on_data_table_row_selected`, `CodingStatisticsScreen`, `._start_new_task`, `GitWorktreeManager`, `update_repository`, `Key`, `._usage_entries`, `.__init__`, `update_repository`, `log_exception`, `CodingStatisticsScreen`, `calculate_token_usage`?**
  _High betweenness centrality (0.184) - this node is a cross-community bridge._
- **Why does `AgentRunner` connect `AgentRunner` to `app.py`, `._start_new_task`, `update_repository`, `KeyboardShortcutsScreen`, `CodingStatisticsScreen`, `Key`, `.__init__`, `._shutdown_coordinators`, `log_exception`, `CodingStatisticsScreen`?**
  _High betweenness centrality (0.104) - this node is a cross-community bridge._
- **Why does `TaskCoordinator` connect `.__init__` to `AgentRunner`, `DaedalusTuiApp`, `._start_new_task`, `update_repository`, `KeyboardShortcutsScreen`, `CodingStatisticsScreen`, `Key`, `._shutdown_coordinators`, `DaedalusVimTextArea`, `log_exception`, `CodingStatisticsScreen`, `calculate_token_usage`?**
  _High betweenness centrality (0.087) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `DaedalusTuiApp` (e.g. with `FakeCoordinator` and `FakeRunner`) actually correct?**
  _`DaedalusTuiApp` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `TuiAppTests` (e.g. with `CodingStatisticsScreen` and `DaedalusTuiApp`) actually correct?**
  _`TuiAppTests` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `TaskCoordinator` (e.g. with `FakeOrchestrator` and `TaskCoordinatorTests`) actually correct?**
  _`TaskCoordinator` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `GitWorktreeManager` (e.g. with `GitWorktreeTests` and `ProjectWorktreeSettings`) actually correct?**
  _`GitWorktreeManager` has 9 INFERRED edges - model-reasoned connections that need verification._