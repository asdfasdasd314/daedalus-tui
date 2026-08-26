# Graph Report - daedalus-tui  (2026-08-25)

## Corpus Check
- 62 files · ~48,647 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1018 nodes · 2729 edges · 47 communities (41 shown, 6 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 295 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ef4ab3ba`
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
- orchestrator.py
- .emit
- ._shutdown_coordinators

## God Nodes (most connected - your core abstractions)
1. `DaedalusTuiApp` - 125 edges
2. `TuiAppTests` - 80 edges
3. `TaskCoordinator` - 71 edges
4. `OrchestrationSettings` - 64 edges
5. `GitWorktreeManager` - 61 edges
6. `WorktreeContext` - 60 edges
7. `AgentRunner` - 56 edges
8. `TaskRecord` - 55 edges
9. `DaedalusVimTextArea` - 53 edges
10. `LocalOrchestrator` - 50 edges

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
Cohesion: 0.19
Nodes (4): Path, Memory override for the project, else the parameter-file default., Update the project's coordinator so later submits use ``branch``., Refresh Branch Select options for the active project and sync coordinator.

### Community 2 - "AgentRunner"
Cohesion: 0.07
Nodes (21): OutputCallback, AgentRunnerTests, FakeProcess, FakeStream, InterruptibleProcess, Thread, AgentLogEvent, AgentRequest (+13 more)

### Community 3 - "DaedalusTuiApp"
Cohesion: 0.06
Nodes (14): DaedalusVimTextArea, Key, Keep Enter as a newline; Ctrl+Enter remains the app submit key., Route visual-line mode and mirror new yanks to the host clipboard., Add Daedalus prompt commands that the dependency does not provide., VimTextArea with multiline prompt behavior and system clipboard sync., Select the current line and enter Vim visual-line mode., Select every character in the lines between the start and cursor. (+6 more)

### Community 4 - "app.py"
Cohesion: 0.16
Nodes (7): RowSelected, Queue a coding task that writes and expands the requested topic file., Focus a task from the cross-project update inbox., Render actionable history and tasks created during this session., Keep failures, active work, and all tasks submitted in this launch., Switch the project context and focus a row selected in the inbox., Keep one bad dynamic widget update from closing the entire TUI.

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
Cohesion: 0.21
Nodes (10): PromptTests, build_migration_repair_prompt(), build_repair_prompt(), build_resolver_prompt(), build_task_prompt(), build_topic_population_prompt(), _embedded_profile(), _embedded_topic() (+2 more)

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

### Community 20 - ".__init__"
Cohesion: 0.05
Nodes (50): Any, TaskEventCallback, PlanTests, FakeOrchestrator, TaskCoordinatorTests, OrchestrationResult, OrchestrationSettings, build_implementation_prompt() (+42 more)

### Community 21 - "._shutdown_coordinators"
Cohesion: 0.20
Nodes (4): Changed, DaedalusTuiApp, Prefer mounted selector values so clarification refreshes keep choices., Replace question controls after Textual has completed child removal.

### Community 22 - "._set_status"
Cohesion: 0.15
Nodes (10): Textual interface for concurrent local agent tasks., _unregister_app_for_thread_exit(), copy_to_system_clipboard(), paste_from_system_clipboard(), System clipboard helpers for terminals without OSC 52 support., Read clipboard text using the native command available on the host., close_fault_handler(), The Daedalus prompt's incremental Vim editing adapter. (+2 more)

### Community 23 - "update_repository"
Cohesion: 0.26
Nodes (8): ConfigTests, CodingStatisticsSettings, load_coding_statistics_settings(), load_orchestration_settings(), load_tui_settings(), _options(), Path, Read-only configuration for the standalone TUI.

### Community 24 - "Daedalus TUI Coding Statistics"
Cohesion: 0.29
Nodes (6): Daedalus TUI Coding Statistics, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 25 - "DaedalusVimTextArea"
Cohesion: 0.14
Nodes (16): TopicsTests, build_topic_instructions(), build_topic_template(), embed_topic(), load_topic_settings(), Topic file discovery, creation, loading, and prompt embedding., Return missing required headings; empty list means structurally complete., Mode-specific rules for using an embedded topic file. (+8 more)

### Community 26 - ".provider_split"
Cohesion: 0.08
Nodes (24): ComposeResult, Pressed, ProgressCallback, Submitted, ProjectInitializerTests, CreateTopicScreen, ProjectInitializerScreen, Collect a project slug and create a Daedalus-compatible directory. (+16 more)

### Community 27 - ".on_mount"
Cohesion: 0.15
Nodes (7): Enable Push only when an origin remote and operating branch are available., Push the Branch Select value for the active project to origin., Pause active agents before ThreadPoolExecutor joins its workers.      CPython ex, Cover terminal and event-loop exits that bypass Textual unmount., Run before ThreadPoolExecutor's internal interpreter-exit join., _register_app_for_thread_exit(), _shutdown_apps_before_thread_join()

### Community 28 - "log_exception"
Cohesion: 0.29
Nodes (6): Daedalus TUI Topics, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 29 - "CodingStatisticsScreen"
Cohesion: 0.09
Nodes (13): FakeCoordinator, FakeRunner, settings(), KeyboardShortcutsScreen, PlanClarificationScreen, Collect a clarification about one plan question., Modal reference for the app and prompt editor keyboard shortcuts., ModelOption (+5 more)

### Community 30 - "calculate_token_usage"
Cohesion: 0.06
Nodes (31): datetime, TaskMemoryStoreTests, TokenUsageTests, Path, Small local JSON stores for persistent task history., Remove one project's operating-branch override (absent = use default)., Return persisted task snapshots keyed by their stable task ID., Upsert a task snapshot keyed by the task worktree's directory name. (+23 more)

### Community 31 - "PlanAnswerSelect"
Cohesion: 0.29
Nodes (6): Daedalus TUI Project Initialization, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 32 - "discover_projects"
Cohesion: 0.25
Nodes (7): 4-Stage Development Lifecycle, Alignment, Debugging, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization, Topics (when tagged)

### Community 34 - "._render_line_strip"
Cohesion: 0.25
Nodes (7): 4-Stage Development Lifecycle, Alignment, Debugging, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization, Topics (when tagged)

### Community 35 - "agent_runner.py"
Cohesion: 0.27
Nodes (9): list_topic_slugs(), load_topic_text(), Path, Return sorted topic filename stems from ``topic_files/*.md``., Resolve ``topic_files/{slug}.md`` under the project checkout., Load topic markdown for ``slug``, or ``None`` when missing/unreadable., Build Select options: ``(None)`` plus each discovered topic slug., topic_path() (+1 more)

### Community 36 - "architecture.md"
Cohesion: 0.33
Nodes (5): 4-Stage Development Lifecycle, Evidence Extraction, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization

### Community 37 - "integrating.md"
Cohesion: 0.40
Nodes (4): 4-Stage Development Lifecycle, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization

### Community 38 - "._set_status"
Cohesion: 0.20
Nodes (4): Key, Return a TextArea selection or the active screen selection., Use Textual's OSC 52 path and a native clipboard fallback., Add Vim-like navigation without changing TextArea insert behavior.

### Community 39 - "Daedalus Project Instructions"
Cohesion: 0.40
Nodes (4): Daedalus Project Instructions, graphify, Task mode, Topics

### Community 41 - "KeyboardShortcutsScreen"
Cohesion: 0.06
Nodes (39): EventCallback, IntegrationGate, GraphifyTests, OrchestratorTests, SupabaseMigrationsTests, VerificationTests, AgentControl, AgentResult (+31 more)

### Community 42 - "CodingStatisticsScreen"
Cohesion: 0.31
Nodes (5): ProjectDiscoveryTests, discover_projects(), Path, Discovery of Daedalus-supported repositories beneath a launch root., Recursively find folders containing a direct ``feature_files`` child.      Git m

### Community 44 - "orchestrator.py"
Cohesion: 0.14
Nodes (8): Mount, Select, CodingStatisticsScreen, _format_count(), _format_tokens(), PlanAnswerSelect, Initialize dynamic plan selectors after their nested children mount., Show token or task usage history and derived coding statistics.

### Community 46 - ".emit"
Cohesion: 0.12
Nodes (10): AbstractEventLoop, BaseException, Exception, Promote only events that need the user's attention in the inbox., Stop agents before an explicit Textual exit begins., Persist Textual failures that would otherwise only flash on screen., Clean up if Textual's run loop returns without its unmount hook., Idempotently detach task callbacks and request child-process shutdown. (+2 more)

### Community 51 - "._shutdown_coordinators"
Cohesion: 0.32
Nodes (7): configure_debug_logging(), install_fault_handler(), _install_thread_exception_logging(), Path, Persistent diagnostics for failures that occur after the Textual screen closes., Write detailed runtime diagnostics to a rotating local log file., Capture fatal faults and ``SIGUSR1`` thread dumps in the debug log.

## Knowledge Gaps
- **88 isolated node(s):** `daedalus-tui`, `Execution Boundaries (CRITICAL)`, `Evidence Extraction`, `Architecture Boundaries`, `Parameter Files` (+83 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DaedalusTuiApp` connect `._shutdown_coordinators` to `PlanQuestion`, `DaedalusVimTextArea`, `AgentRunner`, `.on_button_pressed`, `app.py`, `DaedalusTuiApp`, `._set_status`, `GitWorktreeManager`, `._rebuild_plan_questions`, `Key`, `.emit`, `.__init__`, `._set_status`, `update_repository`, `.on_mount`, `CodingStatisticsScreen`, `calculate_token_usage`?**
  _High betweenness centrality (0.156) - this node is a cross-community bridge._
- **Why does `TaskMemoryStore` connect `calculate_token_usage` to `PlanQuestion`, `orchestrator.py`, `.__init__`, `._shutdown_coordinators`, `._set_status`, `.provider_split`, `CodingStatisticsScreen`?**
  _High betweenness centrality (0.103) - this node is a cross-community bridge._
- **Why does `AgentRunner` connect `AgentRunner` to `PlanQuestion`, `KeyboardShortcutsScreen`, `orchestrator.py`, `.__init__`, `._shutdown_coordinators`, `._set_status`, `.provider_split`, `CodingStatisticsScreen`?**
  _High betweenness centrality (0.089) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `DaedalusTuiApp` (e.g. with `FakeCoordinator` and `FakeRunner`) actually correct?**
  _`DaedalusTuiApp` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `TuiAppTests` (e.g. with `CodingStatisticsScreen` and `DaedalusTuiApp`) actually correct?**
  _`TuiAppTests` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `TaskCoordinator` (e.g. with `FakeOrchestrator` and `TaskCoordinatorTests`) actually correct?**
  _`TaskCoordinator` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `OrchestrationSettings` (e.g. with `OrchestratorTests` and `FakeOrchestrator`) actually correct?**
  _`OrchestrationSettings` has 16 INFERRED edges - model-reasoned connections that need verification._