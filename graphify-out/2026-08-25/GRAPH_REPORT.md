# Graph Report - daedalus-tui  (2026-08-25)

## Corpus Check
- 60 files · ~46,338 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 975 nodes · 2566 edges · 48 communities (44 shown, 4 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 280 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3dfa0e2a`
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
- log_exception
- CodingStatisticsScreen
- calculate_token_usage
- PlanAnswerSelect
- discover_projects
- ._render_line_strip
- architecture.md
- integrating.md
- Daedalus Project Instructions
- README.md
- KeyboardShortcutsScreen
- CodingStatisticsScreen
- ._rebuild_plan_questions
- orchestrator.py
- orchestrator.py
- .emit
- discover_projects
- update_repository
- load_project_worktree_settings
- ._shutdown_coordinators
- CreateTopicScreen

## God Nodes (most connected - your core abstractions)
1. `DaedalusTuiApp` - 120 edges
2. `TuiAppTests` - 76 edges
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

## Communities (48 total, 4 thin omitted)

### Community 0 - "PlanQuestion"
Cohesion: 0.15
Nodes (6): Changed, Log, Path, Memory override for the project, else the parameter-file default., Update the project's coordinator so later submits use ``branch``., Refresh Branch Select options for the active project and sync coordinator.

### Community 1 - "DaedalusVimTextArea"
Cohesion: 0.06
Nodes (18): Agent plan text must not be parsed as Textual/Rich markup., TuiAppTests, DaedalusVimTextArea, Key, Keep Enter as a newline; Ctrl+Enter remains the app submit key., Route visual-line mode and mirror new yanks to the host clipboard., Paste Vim's register, falling back to the system clipboard., Paste before the cursor, including from the system clipboard. (+10 more)

### Community 2 - "AgentRunner"
Cohesion: 0.07
Nodes (21): OutputCallback, AgentRunnerTests, FakeProcess, FakeStream, InterruptibleProcess, Thread, AgentLogEvent, AgentRequest (+13 more)

### Community 3 - "DaedalusTuiApp"
Cohesion: 0.10
Nodes (11): CompletedProcess, Path, Remove graphify output changes from an agent worktree.          Graphify refresh, Keep a read-only planning pass from becoming an implementation change., Commit only the generated graph after a successful primary update., Return a directory whose HEAD matches the target branch tip.          When the r, Remove a short-lived primary checkout created for post-promotion work., Remove a cancelled task even when its branch was never integrated. (+3 more)

### Community 4 - "app.py"
Cohesion: 0.14
Nodes (8): Queue a coding task that writes and expands the requested topic file., Promote only events that need the user's attention in the inbox., Refresh Topic Select options for the active project; default remains (None)., Render actionable history and tasks created during this session., Keep failures, active work, and all tasks submitted in this launch., Switch the project context and focus a row selected in the inbox., Keep one bad dynamic widget update from closing the entire TUI., Clear the selected task and unlock a fresh prompt editor.

### Community 5 - "TokenUsageStore"
Cohesion: 0.29
Nodes (6): Applying answers, Bridge Agent Profile, Build-loop tasking, cp_doc structure, Hard rules, Purpose

### Community 6 - "GitWorktreeManager"
Cohesion: 0.07
Nodes (19): Resize, Strip, Style, Show either the full-size transcript or the full-size diagnostics log., Selectable transcript rendering with semantic assistant-message emphasis., Return the width available for transcript text inside the Log., Wrap one logical line at word boundaries when the width permits., A selectable log that can emphasize a task's final assistant message.      ``Log (+11 more)

### Community 7 - "Daedalus TUI Local Token Usage Memory"
Cohesion: 0.29
Nodes (6): Daedalus TUI Local Persistent Memory, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 8 - "update_repository"
Cohesion: 0.33
Nodes (6): Textual interface for concurrent local agent tasks., copy_to_system_clipboard(), paste_from_system_clipboard(), System clipboard helpers for terminals without OSC 52 support., Read clipboard text using the native command available on the host., The Daedalus prompt's incremental Vim editing adapter.

### Community 11 - "Key"
Cohesion: 0.14
Nodes (10): GitWorktreeTests, GitWorktreeError, GitWorktreeManager, list_local_branches(), RuntimeError, Local Git worktree lifecycle used by the standalone orchestrator., Return local branch names under ``refs/heads`` without checking anything out., Install project resources and link declared shared read-only paths. (+2 more)

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
Nodes (49): Any, TaskEventCallback, PlanTests, FakeOrchestrator, TaskCoordinatorTests, OrchestrationSettings, build_implementation_prompt(), build_plan_clarification_prompt() (+41 more)

### Community 21 - "._shutdown_coordinators"
Cohesion: 0.09
Nodes (8): DaedalusTuiApp, Key, Keep a task visible after user activity during this launch., Prefer mounted selector values so clarification refreshes keep choices., Replace question controls after Textual has completed child removal., Return a TextArea selection or the active screen selection., Use Textual's OSC 52 path and a native clipboard fallback., Add Vim-like navigation without changing TextArea insert behavior.

### Community 22 - "._set_status"
Cohesion: 0.22
Nodes (3): ComposeResult, KeyboardShortcutsScreen, Modal reference for the app and prompt editor keyboard shortcuts.

### Community 24 - "Daedalus TUI Coding Statistics"
Cohesion: 0.29
Nodes (6): Daedalus TUI Coding Statistics, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 25 - "DaedalusVimTextArea"
Cohesion: 0.07
Nodes (34): PromptTests, TopicsTests, build_repair_prompt(), build_resolver_prompt(), build_task_prompt(), build_topic_population_prompt(), _embedded_profile(), _embedded_topic() (+26 more)

### Community 26 - ".provider_split"
Cohesion: 0.17
Nodes (17): ProgressCallback, ProjectInitializerTests, find_github_url(), initialize_project(), load_initializer_settings(), matching_request_marker(), materialize_templates(), normalize_github_url() (+9 more)

### Community 28 - "log_exception"
Cohesion: 0.29
Nodes (6): Daedalus TUI Topics, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 29 - "CodingStatisticsScreen"
Cohesion: 0.13
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

### Community 36 - "architecture.md"
Cohesion: 0.33
Nodes (5): 4-Stage Development Lifecycle, Evidence Extraction, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization

### Community 37 - "integrating.md"
Cohesion: 0.40
Nodes (4): 4-Stage Development Lifecycle, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization

### Community 39 - "Daedalus Project Instructions"
Cohesion: 0.40
Nodes (4): Daedalus Project Instructions, graphify, Task mode, Topics

### Community 41 - "KeyboardShortcutsScreen"
Cohesion: 0.15
Nodes (11): EventCallback, IntegrationGate, AgentControl, Cooperative stop signals shared by a task and its active subprocess., AgentStopped, OrchestrationResult, Path, RuntimeError (+3 more)

### Community 42 - "CodingStatisticsScreen"
Cohesion: 0.31
Nodes (4): CodingStatisticsScreen, _format_count(), _format_tokens(), Show token or task usage history and derived coding statistics.

### Community 43 - "._rebuild_plan_questions"
Cohesion: 0.31
Nodes (6): OrchestratorTests, AgentResult, WorktreeContext, GraphifyResult, LocalOrchestrator, VerificationResult

### Community 44 - "orchestrator.py"
Cohesion: 0.25
Nodes (10): ConfigTests, CodingStatisticsSettings, load_coding_statistics_settings(), load_orchestration_settings(), load_tui_settings(), ModelOption, _options(), Path (+2 more)

### Community 45 - "orchestrator.py"
Cohesion: 0.25
Nodes (9): VerificationTests, Single-run local agent orchestration without daemon or database dependencies., discover_commands(), format_process_result(), package_has_test_script(), CompletedProcess, Path, Local verification discovery and execution. (+1 more)

### Community 46 - ".emit"
Cohesion: 0.29
Nodes (4): Mount, Select, PlanAnswerSelect, Initialize dynamic plan selectors after their nested children mount.

### Community 47 - "discover_projects"
Cohesion: 0.31
Nodes (5): ProjectDiscoveryTests, discover_projects(), Path, Discovery of Daedalus-supported repositories beneath a launch root., Recursively find folders containing a direct ``feature_files`` child.      Git m

### Community 49 - "update_repository"
Cohesion: 0.23
Nodes (6): GraphifyTests, Path, Best-effort graph refresh owned by the local orchestration layer., Refresh the primary repository graph without affecting task success., update_repository(), Refresh graph metadata after promotion without blocking the task.

### Community 50 - "load_project_worktree_settings"
Cohesion: 0.29
Nodes (6): ProjectConfigTests, load_project_worktree_settings(), Path, Configuration supplied by a target project to prepare task worktrees., Load optional worktree provisioning settings from a target repository., _string_array()

### Community 51 - "._shutdown_coordinators"
Cohesion: 0.07
Nodes (23): AbstractEventLoop, BaseException, Exception, Pause active agents before ThreadPoolExecutor joins its workers.      CPython ex, Stop agents before an explicit Textual exit begins., Persist Textual failures that would otherwise only flash on screen., Cover terminal and event-loop exits that bypass Textual unmount., Run before ThreadPoolExecutor's internal interpreter-exit join. (+15 more)

### Community 52 - "CreateTopicScreen"
Cohesion: 0.09
Nodes (10): Pressed, Submitted, CreateTopicScreen, PlanClarificationScreen, ProjectInitializerScreen, Collect a clarification about one plan question., Collect a project slug and create a Daedalus-compatible directory., Collect the context needed to initialize and populate a topic file. (+2 more)

## Knowledge Gaps
- **88 isolated node(s):** `daedalus-tui`, `Execution Boundaries (CRITICAL)`, `Evidence Extraction`, `Architecture Boundaries`, `Parameter Files` (+83 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DaedalusTuiApp` connect `._shutdown_coordinators` to `PlanQuestion`, `DaedalusVimTextArea`, `AgentRunner`, `app.py`, `GitWorktreeManager`, `update_repository`, `orchestrator.py`, `._shutdown_coordinators`, `CreateTopicScreen`, `.__init__`, `._set_status`, `update_repository`, `CodingStatisticsScreen`, `calculate_token_usage`?**
  _High betweenness centrality (0.183) - this node is a cross-community bridge._
- **Why does `AgentRunner` connect `AgentRunner` to `update_repository`, `KeyboardShortcutsScreen`, `CodingStatisticsScreen`, `._rebuild_plan_questions`, `orchestrator.py`, `orchestrator.py`, `.emit`, `CreateTopicScreen`, `._shutdown_coordinators`, `._set_status`, `.__init__`?**
  _High betweenness centrality (0.100) - this node is a cross-community bridge._
- **Why does `TaskCoordinator` connect `.__init__` to `PlanQuestion`, `AgentRunner`, `update_repository`, `KeyboardShortcutsScreen`, `CodingStatisticsScreen`, `Key`, `orchestrator.py`, `._rebuild_plan_questions`, `.emit`, `CreateTopicScreen`, `._shutdown_coordinators`, `._set_status`, `calculate_token_usage`?**
  _High betweenness centrality (0.086) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `DaedalusTuiApp` (e.g. with `FakeCoordinator` and `FakeRunner`) actually correct?**
  _`DaedalusTuiApp` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `TuiAppTests` (e.g. with `CodingStatisticsScreen` and `DaedalusTuiApp`) actually correct?**
  _`TuiAppTests` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `TaskCoordinator` (e.g. with `FakeOrchestrator` and `TaskCoordinatorTests`) actually correct?**
  _`TaskCoordinator` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `GitWorktreeManager` (e.g. with `GitWorktreeTests` and `ProjectWorktreeSettings`) actually correct?**
  _`GitWorktreeManager` has 9 INFERRED edges - model-reasoned connections that need verification._