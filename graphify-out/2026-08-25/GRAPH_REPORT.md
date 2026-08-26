# Graph Report - daedalus-tui  (2026-08-25)

## Corpus Check
- 60 files · ~47,186 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 994 nodes · 2637 edges · 51 communities (41 shown, 10 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 293 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4f2c564a`
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
- orchestrator.py
- .emit
- discover_projects
- ._should_promote_task_update
- update_repository
- ._shutdown_coordinators

## God Nodes (most connected - your core abstractions)
1. `DaedalusTuiApp` - 125 edges
2. `TuiAppTests` - 80 edges
3. `TaskCoordinator` - 71 edges
4. `GitWorktreeManager` - 60 edges
5. `OrchestrationSettings` - 58 edges
6. `AgentRunner` - 56 edges
7. `TaskRecord` - 55 edges
8. `WorktreeContext` - 53 edges
9. `DaedalusVimTextArea` - 53 edges
10. `TaskMemoryStore` - 48 edges

## Surprising Connections (you probably didn't know these)
- `FakeStream` --uses--> `AgentControl`  [INFERRED]
  tests/test_agent_runner.py → tui/agent_runner.py
- `FakeStream` --uses--> `AgentRequest`  [INFERRED]
  tests/test_agent_runner.py → tui/agent_runner.py
- `FakeStream` --uses--> `AgentRunner`  [INFERRED]
  tests/test_agent_runner.py → tui/agent_runner.py
- `FakeProcess` --uses--> `AgentControl`  [INFERRED]
  tests/test_agent_runner.py → tui/agent_runner.py
- `FakeProcess` --uses--> `AgentLogEvent`  [INFERRED]
  tests/test_agent_runner.py → tui/agent_runner.py

## Import Cycles
- None detected.

## Communities (51 total, 10 thin omitted)

### Community 2 - "AgentRunner"
Cohesion: 0.13
Nodes (7): AgentRunnerTests, FakeProcess, InterruptibleProcess, AgentRequest, AgentRunner, Run Codex or Cursor directly and emit only assistant-facing messages., Return assistant text deltas from Cursor's stream-json events.

### Community 3 - "DaedalusTuiApp"
Cohesion: 0.06
Nodes (14): DaedalusVimTextArea, Key, Keep Enter as a newline; Ctrl+Enter remains the app submit key., Route visual-line mode and mirror new yanks to the host clipboard., Add Daedalus prompt commands that the dependency does not provide., VimTextArea with multiline prompt behavior and system clipboard sync., Select the current line and enter Vim visual-line mode., Select every character in the lines between the start and cursor. (+6 more)

### Community 4 - "app.py"
Cohesion: 0.16
Nodes (7): Path, Queue a coding task that writes and expands the requested topic file., Memory override for the project, else the parameter-file default., Render actionable history and tasks created during this session., Keep failures, active work, and all tasks submitted in this launch., Switch the project context and focus a row selected in the inbox., Keep one bad dynamic widget update from closing the entire TUI.

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
Cohesion: 0.22
Nodes (9): PromptTests, build_repair_prompt(), build_resolver_prompt(), build_task_prompt(), build_topic_population_prompt(), _embedded_profile(), _embedded_topic(), Prompt wrappers used by task and resolver agents. (+1 more)

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
Nodes (51): Any, TaskEventCallback, PlanTests, FakeOrchestrator, TaskCoordinatorTests, OrchestrationSettings, build_implementation_prompt(), build_plan_clarification_prompt() (+43 more)

### Community 21 - "._shutdown_coordinators"
Cohesion: 0.16
Nodes (5): AbstractEventLoop, Changed, DaedalusTuiApp, Prefer mounted selector values so clarification refreshes keep choices., Replace question controls after Textual has completed child removal.

### Community 24 - "Daedalus TUI Coding Statistics"
Cohesion: 0.29
Nodes (6): Daedalus TUI Coding Statistics, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 25 - "DaedalusVimTextArea"
Cohesion: 0.05
Nodes (46): ProjectDiscoveryTests, TopicsTests, Textual interface for concurrent local agent tasks., _unregister_app_for_thread_exit(), copy_to_system_clipboard(), paste_from_system_clipboard(), System clipboard helpers for terminals without OSC 52 support., Read clipboard text using the native command available on the host. (+38 more)

### Community 26 - ".provider_split"
Cohesion: 0.10
Nodes (21): Pressed, ProgressCallback, Submitted, ProjectInitializerTests, ProjectInitializerScreen, Collect a project slug and create a Daedalus-compatible directory., find_github_url(), initialize_project() (+13 more)

### Community 27 - ".on_mount"
Cohesion: 0.12
Nodes (9): Update the project's coordinator so later submits use ``branch``., Refresh Branch Select options for the active project and sync coordinator., Enable Push only when an origin remote and operating branch are available., Push the Branch Select value for the active project to origin., Refresh Topic Select options for the active project; default remains (None)., Pause active agents before ThreadPoolExecutor joins its workers.      CPython ex, Cover terminal and event-loop exits that bypass Textual unmount., _register_app_for_thread_exit() (+1 more)

### Community 28 - "log_exception"
Cohesion: 0.29
Nodes (6): Daedalus TUI Topics, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 29 - "CodingStatisticsScreen"
Cohesion: 0.11
Nodes (5): FakeCoordinator, FakeRunner, settings(), DaedalusProject, A repository recognized by the presence of a ``feature_files`` folder.

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
Cohesion: 0.18
Nodes (8): FakeStream, AgentLogEvent, Provider-specific subprocess execution with normalized agent messages., cursor_environment(), Path, Small, dependency-free environment-file loading for local CLI providers., Return the process environment plus local Cursor credentials.      Explicit proc, read_env_file()

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
Cohesion: 0.16
Nodes (10): EventCallback, IntegrationGate, AgentControl, Cooperative stop signals shared by a task and its active subprocess., AgentStopped, Path, RuntimeError, Load a repository-owned profile immediately before building a prompt. (+2 more)

### Community 42 - "CodingStatisticsScreen"
Cohesion: 0.21
Nodes (4): OutputCallback, Thread, Track an inactivity deadline that agent stdout can refresh., _TimeoutTracker

### Community 43 - "._rebuild_plan_questions"
Cohesion: 0.31
Nodes (6): OrchestratorTests, AgentResult, WorktreeContext, GraphifyResult, LocalOrchestrator, VerificationResult

### Community 44 - "orchestrator.py"
Cohesion: 0.07
Nodes (23): ComposeResult, Mount, Select, ConfigTests, CodingStatisticsScreen, CreateTopicScreen, _format_count(), _format_tokens() (+15 more)

### Community 45 - "orchestrator.py"
Cohesion: 0.29
Nodes (8): VerificationTests, discover_commands(), format_process_result(), package_has_test_script(), CompletedProcess, Path, Local verification discovery and execution., run_verification()

### Community 46 - ".emit"
Cohesion: 0.18
Nodes (6): Exception, Stop agents before an explicit Textual exit begins., Persist Textual failures that would otherwise only flash on screen., Run before ThreadPoolExecutor's internal interpreter-exit join., Clean up if Textual's run loop returns without its unmount hook., Idempotently detach task callbacks and request child-process shutdown.

### Community 49 - "update_repository"
Cohesion: 0.23
Nodes (6): GraphifyTests, Path, Best-effort graph refresh owned by the local orchestration layer., Refresh the primary repository graph without affecting task success., update_repository(), Refresh graph metadata after promotion without blocking the task.

### Community 51 - "._shutdown_coordinators"
Cohesion: 0.21
Nodes (8): BaseException, log_exception(), Persistent diagnostics for failures that occur after the Textual screen closes., __getattr__(), Standalone Textual interface and local agent orchestration., main(), OrchestrationResult, Single-run local agent orchestration without daemon or database dependencies.

## Knowledge Gaps
- **88 isolated node(s):** `daedalus-tui`, `Execution Boundaries (CRITICAL)`, `Evidence Extraction`, `Architecture Boundaries`, `Parameter Files` (+83 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DaedalusTuiApp` connect `._shutdown_coordinators` to `PlanQuestion`, `DaedalusVimTextArea`, `AgentRunner`, `DaedalusTuiApp`, `app.py`, `GitWorktreeManager`, `Key`, `.__init__`, `._set_status`, `update_repository`, `DaedalusVimTextArea`, `.on_mount`, `CodingStatisticsScreen`, `calculate_token_usage`, `.on_button_pressed`, `._set_status`, `orchestrator.py`, `.emit`, `discover_projects`, `._should_promote_task_update`, `._shutdown_coordinators`?**
  _High betweenness centrality (0.190) - this node is a cross-community bridge._
- **Why does `AgentRunner` connect `AgentRunner` to `agent_runner.py`, `app.py`, `KeyboardShortcutsScreen`, `CodingStatisticsScreen`, `._rebuild_plan_questions`, `orchestrator.py`, `._shutdown_coordinators`, `.__init__`, `._shutdown_coordinators`, `._set_status`, `DaedalusVimTextArea`, `.provider_split`?**
  _High betweenness centrality (0.091) - this node is a cross-community bridge._
- **Why does `TaskCoordinator` connect `.__init__` to `AgentRunner`, `app.py`, `KeyboardShortcutsScreen`, `Key`, `orchestrator.py`, `._rebuild_plan_questions`, `._shutdown_coordinators`, `._shutdown_coordinators`, `._set_status`, `DaedalusVimTextArea`, `.provider_split`, `calculate_token_usage`?**
  _High betweenness centrality (0.076) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `DaedalusTuiApp` (e.g. with `FakeCoordinator` and `FakeRunner`) actually correct?**
  _`DaedalusTuiApp` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `TuiAppTests` (e.g. with `CodingStatisticsScreen` and `DaedalusTuiApp`) actually correct?**
  _`TuiAppTests` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `TaskCoordinator` (e.g. with `FakeOrchestrator` and `TaskCoordinatorTests`) actually correct?**
  _`TaskCoordinator` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `GitWorktreeManager` (e.g. with `GitWorktreeTests` and `ProjectWorktreeSettings`) actually correct?**
  _`GitWorktreeManager` has 9 INFERRED edges - model-reasoned connections that need verification._