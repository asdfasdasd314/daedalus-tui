# Graph Report - daedalus-tui  (2026-09-01)

## Corpus Check
- 75 files · ~52,456 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1131 nodes · 2949 edges · 56 communities (47 shown, 9 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 314 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ee944572`
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
- ._shutdown_coordinators
- ._set_status
- update_repository
- Daedalus TUI Coding Statistics
- DaedalusVimTextArea
- .provider_split
- .on_mount
- log_exception
- CodingStatisticsScreen
- calculate_token_usage
- PlanAnswerSelect
- discover_projects
- .on_button_pressed
- ._render_line_strip
- agent_runner.py
- architecture.md
- integrating.md
- ._set_status
- Daedalus Project Instructions
- README.md
- KeyboardShortcutsScreen
- CodingStatisticsScreen
- ._rebuild_plan_questions
- KeyboardShortcutsScreen
- .emit
- ._start_new_task
- .on_data_table_row_selected
- PlanQuestion
- CreateTopicScreen
- Daedalus TUI Call Graph Visualization
- b.py
- .action_view_topic
- conftest.py
- cycle_a.py
- ._render_selected_task
- __init__.py

## God Nodes (most connected - your core abstractions)
1. `DaedalusTuiApp` - 131 edges
2. `TuiAppTests` - 83 edges
3. `TaskCoordinator` - 72 edges
4. `OrchestrationSettings` - 64 edges
5. `GitWorktreeManager` - 61 edges
6. `WorktreeContext` - 60 edges
7. `AgentRunner` - 57 edges
8. `TaskRecord` - 56 edges
9. `TaskMemoryStore` - 54 edges
10. `DaedalusVimTextArea` - 54 edges

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

## Communities (56 total, 9 thin omitted)

### Community 0 - "PlanQuestion"
Cohesion: 0.11
Nodes (7): ComposeResult, Mount, Select, KeyboardShortcutsScreen, PlanAnswerSelect, Initialize dynamic plan selectors after their nested children mount., Modal reference for the app and prompt editor keyboard shortcuts.

### Community 2 - "AgentRunner"
Cohesion: 0.07
Nodes (21): OutputCallback, AgentRunnerTests, FakeProcess, FakeStream, InterruptibleProcess, Thread, AgentLogEvent, AgentRequest (+13 more)

### Community 3 - "DaedalusTuiApp"
Cohesion: 0.10
Nodes (14): DaedalusVimTextArea, Key, Keep Enter as a newline; Ctrl+Enter remains the app submit key., Route visual-line mode and mirror new yanks to the host clipboard., Add Daedalus prompt commands that the dependency does not provide., VimTextArea with multiline prompt behavior and system clipboard sync., Select the current line and enter Vim visual-line mode., Select every character in the lines between the start and cursor. (+6 more)

### Community 4 - "app.py"
Cohesion: 0.13
Nodes (8): Path, Queue a coding task that writes and expands the requested topic file., Memory override for the project, else the parameter-file default., Update the project's coordinator so later submits use ``branch``., Refresh Branch Select options for the active project and sync coordinator., Render actionable history and tasks created during this session., Keep failures, active work, and all tasks submitted in this launch., Switch the project context and focus a row selected in the inbox.

### Community 5 - "TokenUsageStore"
Cohesion: 0.29
Nodes (6): Applying answers, Bridge Agent Profile, Build-loop tasking, cp_doc structure, Hard rules, Purpose

### Community 6 - "GitWorktreeManager"
Cohesion: 0.08
Nodes (19): Log, Resize, Strip, Style, Selectable transcript rendering with semantic assistant-message emphasis., Return the width available for transcript text inside the Log., Wrap one logical line at word boundaries when the width permits., A selectable log that can emphasize a task's final assistant message.      ``Log (+11 more)

### Community 7 - "Daedalus TUI Local Token Usage Memory"
Cohesion: 0.29
Nodes (6): Daedalus TUI Local Persistent Memory, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 8 - "update_repository"
Cohesion: 0.08
Nodes (23): GraphifyTests, PromptTests, SupabaseMigrationsTests, Path, Best-effort graph refresh owned by the local orchestration layer., Refresh the primary repository graph without affecting task success., update_repository(), Single-run local agent orchestration without daemon or database dependencies. (+15 more)

### Community 11 - "Key"
Cohesion: 0.05
Nodes (31): GitWorktreeTests, ProjectConfigTests, GitWorktreeError, GitWorktreeManager, list_local_branches(), push_branch(), CompletedProcess, Path (+23 more)

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

### Community 21 - "._shutdown_coordinators"
Cohesion: 0.17
Nodes (5): Changed, DaedalusTuiApp, Remember the selected topic as the default for the active project., Prefer mounted selector values so clarification refreshes keep choices., Replace question controls after Textual has completed child removal.

### Community 22 - "._set_status"
Cohesion: 0.16
Nodes (9): Textual interface for concurrent local agent tasks., _unregister_app_for_thread_exit(), paste_from_system_clipboard(), System clipboard helpers for terminals without OSC 52 support., Read clipboard text using the native command available on the host., close_fault_handler(), The Daedalus prompt's incremental Vim editing adapter., Paste Vim's register, falling back to the system clipboard. (+1 more)

### Community 24 - "Daedalus TUI Coding Statistics"
Cohesion: 0.29
Nodes (6): Daedalus TUI Coding Statistics, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 25 - "DaedalusVimTextArea"
Cohesion: 0.14
Nodes (19): TopicsTests, build_topic_instructions(), build_topic_template(), embed_topic(), list_topic_slugs(), load_topic_text(), Path, Topic file discovery, creation, loading, and prompt embedding. (+11 more)

### Community 26 - ".provider_split"
Cohesion: 0.11
Nodes (20): ProgressCallback, Submitted, ProjectInitializerTests, ProjectInitializerScreen, Collect a project slug and create a Daedalus-compatible directory., find_github_url(), initialize_project(), load_initializer_settings() (+12 more)

### Community 27 - ".on_mount"
Cohesion: 0.08
Nodes (41): CallGraphVisitor, load_config(), main(), Path, CallGraphTreeTests, build_tree(), CallGraphConfig, _collapse_inner_safe() (+33 more)

### Community 28 - "log_exception"
Cohesion: 0.29
Nodes (6): Daedalus TUI Topics, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 29 - "CodingStatisticsScreen"
Cohesion: 0.09
Nodes (13): FakeCoordinator, FakeRunner, settings(), PlanClarificationScreen, Collect a clarification about one plan question., Display a topic markdown file without allowing edits., TopicViewerScreen, ModelOption (+5 more)

### Community 30 - "calculate_token_usage"
Cohesion: 0.05
Nodes (34): TaskMemoryStoreTests, TokenUsageTests, Path, Small local JSON stores for persistent task history., Remove one project's operating-branch override (absent = use default)., Return the remembered default topic for a project, if any., Remember one project's default topic without losing other entries., Remove one project's topic override (absent = no default topic). (+26 more)

### Community 31 - "PlanAnswerSelect"
Cohesion: 0.29
Nodes (6): Daedalus TUI Project Initialization, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 32 - "discover_projects"
Cohesion: 0.25
Nodes (7): 4-Stage Development Lifecycle, Alignment, Debugging, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization, Topics (when tagged)

### Community 33 - ".on_button_pressed"
Cohesion: 0.27
Nodes (4): CodingStatisticsScreen, _format_count(), _format_tokens(), Show token or task usage history and derived coding statistics.

### Community 34 - "._render_line_strip"
Cohesion: 0.25
Nodes (7): 4-Stage Development Lifecycle, Alignment, Debugging, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization, Topics (when tagged)

### Community 35 - "agent_runner.py"
Cohesion: 0.13
Nodes (9): Pressed, CreateTopicScreen, Collect the context needed to initialize and populate a topic file., load_topic_settings(), Load tunable limits for topic creation from the paired parameter file., Return a display name suitable for an H1 and a filesystem slug., Convert a validated topic name to the filename stem used by the TUI., topic_slug_from_name() (+1 more)

### Community 36 - "architecture.md"
Cohesion: 0.33
Nodes (5): 4-Stage Development Lifecycle, Evidence Extraction, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization

### Community 37 - "integrating.md"
Cohesion: 0.40
Nodes (4): 4-Stage Development Lifecycle, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization

### Community 38 - "._set_status"
Cohesion: 0.18
Nodes (5): Key, Return a TextArea selection or the active screen selection., Use Textual's OSC 52 path and a native clipboard fallback., Add Vim-like navigation without changing TextArea insert behavior., copy_to_system_clipboard()

### Community 39 - "Daedalus Project Instructions"
Cohesion: 0.40
Nodes (4): Daedalus Project Instructions, graphify, Task mode, Topics

### Community 41 - "KeyboardShortcutsScreen"
Cohesion: 0.09
Nodes (26): EventCallback, IntegrationGate, OrchestratorTests, VerificationTests, AgentControl, AgentResult, Cooperative stop signals shared by a task and its active subprocess., WorktreeContext (+18 more)

### Community 42 - "CodingStatisticsScreen"
Cohesion: 0.31
Nodes (5): ProjectDiscoveryTests, discover_projects(), Path, Discovery of Daedalus-supported repositories beneath a launch root., Recursively find folders containing a direct ``feature_files`` child.      Git m

### Community 43 - "._rebuild_plan_questions"
Cohesion: 0.17
Nodes (6): AbstractEventLoop, BaseException, Promote only events that need the user's attention in the inbox., Keep one bad dynamic widget update from closing the entire TUI., log_exception(), main()

### Community 45 - "KeyboardShortcutsScreen"
Cohesion: 0.20
Nodes (9): Constraints and Design Principles, Desired End State, Intended Import Workflow, Open Questions, Project Imports to the Daedalus Format, Scope and Durable Context, State Log, Topic Goal (+1 more)

### Community 46 - ".emit"
Cohesion: 0.24
Nodes (8): Cover terminal and event-loop exits that bypass Textual unmount., configure_debug_logging(), install_fault_handler(), _install_thread_exception_logging(), Path, Persistent diagnostics for failures that occur after the Textual screen closes., Write detailed runtime diagnostics to a rotating local log file., Capture fatal faults and ``SIGUSR1`` thread dumps in the debug log.

### Community 49 - "PlanQuestion"
Cohesion: 0.05
Nodes (50): TaskEventCallback, PlanTests, FakeOrchestrator, TaskCoordinatorTests, OrchestrationResult, OrchestrationSettings, build_implementation_prompt(), build_plan_clarification_prompt() (+42 more)

### Community 51 - "CreateTopicScreen"
Cohesion: 0.23
Nodes (8): ConfigTests, CodingStatisticsSettings, load_coding_statistics_settings(), load_orchestration_settings(), load_tui_settings(), _options(), Path, Read-only configuration for the standalone TUI.

### Community 52 - "Daedalus TUI Call Graph Visualization"
Cohesion: 0.29
Nodes (6): Daedalus TUI Call Graph Visualization, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 53 - "b.py"
Cohesion: 0.36
Nodes (4): alpha(), beta(), gamma(), make_runner()

### Community 54 - ".action_view_topic"
Cohesion: 0.18
Nodes (5): Refresh topics and restore the active project's remembered default., Return the selected topic slug, or None for the blank option., Enable topic viewing only when the selector has a real topic., Clear the selected task and unlock a fresh prompt editor., Open the selected project topic in a read-only modal.

### Community 55 - "conftest.py"
Cohesion: 0.50
Nodes (3): pytest_configure(), Pytest hooks shared across the test suite., Install pyan3 when call-graph tests run in an environment missing it.

### Community 57 - "._render_selected_task"
Cohesion: 0.14
Nodes (9): Exception, Pause active agents before ThreadPoolExecutor joins its workers.      CPython ex, Stop agents before an explicit Textual exit begins., Persist Textual failures that would otherwise only flash on screen., Run before ThreadPoolExecutor's internal interpreter-exit join., Clean up if Textual's run loop returns without its unmount hook., Idempotently detach task callbacks and request child-process shutdown., _register_app_for_thread_exit() (+1 more)

## Knowledge Gaps
- **101 isolated node(s):** `daedalus-tui`, `Execution Boundaries (CRITICAL)`, `Evidence Extraction`, `Architecture Boundaries`, `Parameter Files` (+96 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DaedalusTuiApp` connect `._shutdown_coordinators` to `PlanQuestion`, `DaedalusVimTextArea`, `AgentRunner`, `DaedalusTuiApp`, `app.py`, `GitWorktreeManager`, `Key`, `._set_status`, `update_repository`, `CodingStatisticsScreen`, `calculate_token_usage`, `.on_button_pressed`, `._set_status`, `._rebuild_plan_questions`, `.emit`, `._start_new_task`, `.on_data_table_row_selected`, `PlanQuestion`, `CreateTopicScreen`, `.action_view_topic`, `._render_selected_task`?**
  _High betweenness centrality (0.220) - this node is a cross-community bridge._
- **Why does `GitWorktreeError` connect `Key` to `PlanQuestion`, `DaedalusVimTextArea`, `.on_button_pressed`, `agent_runner.py`, `update_repository`, `KeyboardShortcutsScreen`, `PlanQuestion`, `._shutdown_coordinators`, `._set_status`, `.provider_split`, `CodingStatisticsScreen`?**
  _High betweenness centrality (0.086) - this node is a cross-community bridge._
- **Why does `TaskMemoryStore` connect `calculate_token_usage` to `PlanQuestion`, `.on_button_pressed`, `agent_runner.py`, `PlanQuestion`, `CreateTopicScreen`, `._shutdown_coordinators`, `._set_status`, `.provider_split`, `CodingStatisticsScreen`?**
  _High betweenness centrality (0.071) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `DaedalusTuiApp` (e.g. with `FakeCoordinator` and `FakeRunner`) actually correct?**
  _`DaedalusTuiApp` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `TuiAppTests` (e.g. with `CodingStatisticsScreen` and `DaedalusTuiApp`) actually correct?**
  _`TuiAppTests` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 21 inferred relationships involving `TaskCoordinator` (e.g. with `FakeOrchestrator` and `TaskCoordinatorTests`) actually correct?**
  _`TaskCoordinator` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `OrchestrationSettings` (e.g. with `OrchestratorTests` and `FakeOrchestrator`) actually correct?**
  _`OrchestrationSettings` has 16 INFERRED edges - model-reasoned connections that need verification._