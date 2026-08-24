# Graph Report - daedalus-tui  (2026-08-24)

## Corpus Check
- 57 files · ~41,755 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 895 nodes · 2360 edges · 52 communities (44 shown, 8 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 265 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `62407b1a`
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
- ._rebuild_plan_questions
- orchestrator.py
- discover_projects
- .emit
- discover_projects
- ._usage_entries
- TokenUsageStats
- .enter_insert_mode
- .nav_word_end

## God Nodes (most connected - your core abstractions)
1. `DaedalusTuiApp` - 115 edges
2. `TuiAppTests` - 73 edges
3. `TaskCoordinator` - 68 edges
4. `GitWorktreeManager` - 60 edges
5. `AgentRunner` - 55 edges
6. `OrchestrationSettings` - 54 edges
7. `TaskRecord` - 54 edges
8. `DaedalusVimTextArea` - 52 edges
9. `WorktreeContext` - 51 edges
10. `TaskMemoryStore` - 46 edges

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

## Communities (52 total, 8 thin omitted)

### Community 0 - "PlanQuestion"
Cohesion: 0.22
Nodes (4): Path, Refresh Branch Select options for the active project and sync coordinator., Memory override for the project, else the parameter-file default., Update the project's coordinator so later submits use ``branch``.

### Community 1 - "DaedalusVimTextArea"
Cohesion: 0.11
Nodes (4): TuiAppTests, DaedalusVimTextArea, VimTextArea with multiline prompt behavior and system clipboard sync., VimTextArea

### Community 2 - "AgentRunner"
Cohesion: 0.07
Nodes (21): OutputCallback, AgentRunnerTests, FakeProcess, FakeStream, InterruptibleProcess, Thread, AgentLogEvent, AgentRequest (+13 more)

### Community 3 - "DaedalusTuiApp"
Cohesion: 0.13
Nodes (12): GitWorktreeManager, CompletedProcess, Path, Remove graphify output changes from an agent worktree.          Graphify refresh, Keep a read-only planning pass from becoming an implementation change., Commit only the generated graph after a successful primary update., Return a directory whose HEAD matches the target branch tip.          When the r, Remove a short-lived primary checkout created for post-promotion work. (+4 more)

### Community 5 - "TokenUsageStore"
Cohesion: 0.29
Nodes (6): Applying answers, Bridge Agent Profile, Build-loop tasking, cp_doc structure, Hard rules, Purpose

### Community 6 - "GitWorktreeManager"
Cohesion: 0.09
Nodes (17): Resize, Strip, Style, Selectable transcript rendering with semantic assistant-message emphasis., Return the width available for transcript text inside the Log., Wrap one logical line without changing its selectable text., Render a line with the final-message color before selection styling., A selectable log that can emphasize a task's final assistant message.      ``Log (+9 more)

### Community 7 - "Daedalus TUI Local Token Usage Memory"
Cohesion: 0.29
Nodes (6): Daedalus TUI Local Persistent Memory, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 8 - "update_repository"
Cohesion: 0.13
Nodes (12): _format_tokens(), Textual interface for concurrent local agent tasks., Use Textual's OSC 52 path and a native clipboard fallback., _unregister_app_for_thread_exit(), copy_to_system_clipboard(), paste_from_system_clipboard(), System clipboard helpers for terminals without OSC 52 support., Read clipboard text using the native command available on the host. (+4 more)

### Community 11 - "Key"
Cohesion: 0.33
Nodes (6): OrchestratorTests, AgentResult, WorktreeContext, GraphifyResult, LocalOrchestrator, VerificationResult

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
Cohesion: 0.07
Nodes (27): TaskEventCallback, FakeOrchestrator, TaskCoordinatorTests, OrchestrationResult, OrchestrationSettings, IntegrationCoordinator, _nonnegative_int(), _phase_for_status() (+19 more)

### Community 21 - "._shutdown_coordinators"
Cohesion: 0.15
Nodes (5): DaedalusTuiApp, Key, Keep a task visible after user activity during this launch., Return a TextArea selection or the active screen selection., Add Vim-like navigation without changing TextArea insert behavior.

### Community 22 - "._set_status"
Cohesion: 0.13
Nodes (23): Any, PlanTests, build_implementation_prompt(), build_plan_clarification_prompt(), build_plan_followup_prompt(), custom_answer_text(), encode_custom_answer(), is_valid_plan_answer() (+15 more)

### Community 23 - "update_repository"
Cohesion: 0.08
Nodes (21): AbstractEventLoop, BaseException, Exception, Pause active agents before ThreadPoolExecutor joins its workers.      CPython ex, Stop agents before an explicit Textual exit begins., Persist Textual failures that would otherwise only flash on screen., Cover terminal and event-loop exits that bypass Textual unmount., Run before ThreadPoolExecutor's internal interpreter-exit join. (+13 more)

### Community 24 - "Daedalus TUI Coding Statistics"
Cohesion: 0.29
Nodes (6): Daedalus TUI Coding Statistics, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 25 - "DaedalusVimTextArea"
Cohesion: 0.13
Nodes (3): GitWorktreeTests, GitWorktreeError, RuntimeError

### Community 26 - ".provider_split"
Cohesion: 0.11
Nodes (21): Pressed, ProgressCallback, Submitted, ProjectInitializerTests, ProjectInitializerScreen, Collect a project slug and create a Daedalus-compatible directory., find_github_url(), initialize_project() (+13 more)

### Community 27 - "test_app.py"
Cohesion: 0.10
Nodes (20): GraphifyTests, PromptTests, VerificationTests, Path, Best-effort graph refresh owned by the local orchestration layer., Refresh the primary repository graph without affecting task success., update_repository(), Single-run local agent orchestration without daemon or database dependencies. (+12 more)

### Community 28 - "log_exception"
Cohesion: 0.14
Nodes (12): ProjectConfigTests, list_local_branches(), Local Git worktree lifecycle used by the standalone orchestrator., Return local branch names under ``refs/heads`` without checking anything out., Install project resources and link declared shared read-only paths., load_project_worktree_settings(), ProjectWorktreeSettings, Path (+4 more)

### Community 29 - "CodingStatisticsScreen"
Cohesion: 0.10
Nodes (13): FakeCoordinator, FakeRunner, settings(), KeyboardShortcutsScreen, PlanClarificationScreen, Collect a clarification about one plan question., Modal reference for the app and prompt editor keyboard shortcuts., ModelOption (+5 more)

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
Nodes (8): Key, Keep Enter as a newline; Ctrl+Enter remains the app submit key., Route visual-line mode and mirror new yanks to the host clipboard., Add Daedalus prompt commands that the dependency does not provide., Select the current line and enter Vim visual-line mode., Select every character in the lines between the start and cursor., Handle movement and operators while whole lines are selected., Expose operator-pending so the caret can become an underline.

### Community 34 - "._render_line_strip"
Cohesion: 0.29
Nodes (6): 4-Stage Development Lifecycle, Alignment, Debugging, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization

### Community 35 - ".on_data_table_row_selected"
Cohesion: 0.21
Nodes (11): datetime, TokenUsageTests, Small local JSON stores for persistent task history., calculate_token_usage(), _parse_timestamp(), Token usage records and derived coding statistics., The token usage attributed to one submitted task., Convert persisted task snapshots into usage records. (+3 more)

### Community 36 - "architecture.md"
Cohesion: 0.33
Nodes (5): 4-Stage Development Lifecycle, Evidence Extraction, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization

### Community 37 - "integrating.md"
Cohesion: 0.40
Nodes (4): 4-Stage Development Lifecycle, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization

### Community 38 - "._start_new_task"
Cohesion: 0.14
Nodes (6): ComposeResult, Log, Mount, Select, PlanAnswerSelect, Initialize dynamic plan selectors after their nested children mount.

### Community 39 - "Daedalus Project Instructions"
Cohesion: 0.50
Nodes (3): Daedalus Project Instructions, graphify, Task mode

### Community 41 - "KeyboardShortcutsScreen"
Cohesion: 0.14
Nodes (10): EventCallback, IntegrationGate, AgentControl, Cooperative stop signals shared by a task and its active subprocess., AgentStopped, Path, RuntimeError, Load a repository-owned profile immediately before building a prompt. (+2 more)

### Community 42 - "CodingStatisticsScreen"
Cohesion: 0.23
Nodes (5): Changed, CodingStatisticsScreen, _format_count(), Show token or task usage history and derived coding statistics., CodingStatisticsSettings

### Community 44 - "orchestrator.py"
Cohesion: 0.32
Nodes (7): ConfigTests, load_coding_statistics_settings(), load_orchestration_settings(), load_tui_settings(), _options(), Path, Read-only configuration for the standalone TUI.

### Community 45 - "discover_projects"
Cohesion: 0.11
Nodes (8): RowSelected, Render actionable history and tasks created during this session., Keep failures, active work, and all tasks submitted in this launch., Switch the project context and focus a row selected in the inbox., Keep one bad dynamic widget update from closing the entire TUI., Clear the selected task and unlock a fresh prompt editor., Focus a task from the cross-project update inbox., Promote only events that need the user's attention in the inbox.

### Community 47 - "discover_projects"
Cohesion: 0.31
Nodes (5): ProjectDiscoveryTests, discover_projects(), Path, Discovery of Daedalus-supported repositories beneath a launch root., Recursively find folders containing a direct ``feature_files`` child.      Git m

### Community 48 - "._usage_entries"
Cohesion: 0.33
Nodes (4): merge_usage_entries(), Merge snapshots by task ID, allowing live records to replace history., Convert a live task record without coupling this module to its class., task_usage_entry()

### Community 49 - "TokenUsageStats"
Cohesion: 0.33
Nodes (4): Aggregates used by the coding statistics screen., Return provider and absolute usage pairs for the selected unit., Return per-provider average usage per prompt for the selected unit., TokenUsageStats

## Knowledge Gaps
- **78 isolated node(s):** `daedalus-tui`, `Execution Boundaries (CRITICAL)`, `Evidence Extraction`, `Architecture Boundaries`, `Parameter Files` (+73 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DaedalusTuiApp` connect `._shutdown_coordinators` to `PlanQuestion`, `DaedalusVimTextArea`, `AgentRunner`, `._start_new_task`, `GitWorktreeManager`, `update_repository`, `CodingStatisticsScreen`, `._rebuild_plan_questions`, `discover_projects`, `._usage_entries`, `.__init__`, `._set_status`, `update_repository`, `CodingStatisticsScreen`, `calculate_token_usage`?**
  _High betweenness centrality (0.192) - this node is a cross-community bridge._
- **Why does `AgentRunner` connect `AgentRunner` to `PlanQuestion`, `._start_new_task`, `update_repository`, `KeyboardShortcutsScreen`, `CodingStatisticsScreen`, `Key`, `.__init__`, `._shutdown_coordinators`, `.provider_split`, `test_app.py`, `CodingStatisticsScreen`?**
  _High betweenness centrality (0.112) - this node is a cross-community bridge._
- **Why does `TaskRecord` connect `.__init__` to `DaedalusVimTextArea`, `AgentRunner`, `DaedalusTuiApp`, `._start_new_task`, `update_repository`, `KeyboardShortcutsScreen`, `CodingStatisticsScreen`, `._rebuild_plan_questions`, `Key`, `discover_projects`, `._shutdown_coordinators`, `._set_status`, `DaedalusVimTextArea`, `.provider_split`, `CodingStatisticsScreen`, `calculate_token_usage`?**
  _High betweenness centrality (0.090) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `DaedalusTuiApp` (e.g. with `FakeCoordinator` and `FakeRunner`) actually correct?**
  _`DaedalusTuiApp` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `TuiAppTests` (e.g. with `CodingStatisticsScreen` and `DaedalusTuiApp`) actually correct?**
  _`TuiAppTests` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `TaskCoordinator` (e.g. with `FakeOrchestrator` and `TaskCoordinatorTests`) actually correct?**
  _`TaskCoordinator` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `GitWorktreeManager` (e.g. with `GitWorktreeTests` and `ProjectWorktreeSettings`) actually correct?**
  _`GitWorktreeManager` has 9 INFERRED edges - model-reasoned connections that need verification._