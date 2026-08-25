# Graph Report - daedalus-tui  (2026-08-24)

## Corpus Check
- 60 files · ~44,865 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 946 nodes · 2484 edges · 43 communities (40 shown, 3 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 267 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b0cec45e`
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
- architecture.md
- integrating.md
- Daedalus Project Instructions
- README.md
- KeyboardShortcutsScreen
- CodingStatisticsScreen
- ._rebuild_plan_questions
- orchestrator.py

## God Nodes (most connected - your core abstractions)
1. `DaedalusTuiApp` - 118 edges
2. `TuiAppTests` - 75 edges
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

## Communities (43 total, 3 thin omitted)

### Community 0 - "PlanQuestion"
Cohesion: 0.11
Nodes (14): Log, RowSelected, DaedalusTuiApp, Path, Memory override for the project, else the parameter-file default., Update the project's coordinator so later submits use ``branch``., Refresh Branch Select options for the active project and sync coordinator., Refresh Topic Select options for the active project; default remains (None). (+6 more)

### Community 1 - "DaedalusVimTextArea"
Cohesion: 0.06
Nodes (18): Agent plan text must not be parsed as Textual/Rich markup., TuiAppTests, DaedalusVimTextArea, Key, Keep Enter as a newline; Ctrl+Enter remains the app submit key., Route visual-line mode and mirror new yanks to the host clipboard., Paste Vim's register, falling back to the system clipboard., Paste before the cursor, including from the system clipboard. (+10 more)

### Community 2 - "AgentRunner"
Cohesion: 0.07
Nodes (21): OutputCallback, AgentRunnerTests, FakeProcess, FakeStream, InterruptibleProcess, Thread, AgentLogEvent, AgentRequest (+13 more)

### Community 3 - "DaedalusTuiApp"
Cohesion: 0.09
Nodes (13): GitWorktreeTests, GitWorktreeManager, CompletedProcess, Path, Remove graphify output changes from an agent worktree.          Graphify refresh, Keep a read-only planning pass from becoming an implementation change., Commit only the generated graph after a successful primary update., Return a directory whose HEAD matches the target branch tip.          When the r (+5 more)

### Community 4 - "app.py"
Cohesion: 0.25
Nodes (9): VerificationTests, Single-run local agent orchestration without daemon or database dependencies., discover_commands(), format_process_result(), package_has_test_script(), CompletedProcess, Path, Local verification discovery and execution. (+1 more)

### Community 5 - "TokenUsageStore"
Cohesion: 0.29
Nodes (6): Applying answers, Bridge Agent Profile, Build-loop tasking, cp_doc structure, Hard rules, Purpose

### Community 6 - "GitWorktreeManager"
Cohesion: 0.08
Nodes (18): Resize, Strip, Style, Show either the full-size transcript or the full-size diagnostics log., Selectable transcript rendering with semantic assistant-message emphasis., Return the width available for transcript text inside the Log., Wrap one logical line without changing its selectable text., Render a line with the final-message color before selection styling. (+10 more)

### Community 7 - "Daedalus TUI Local Token Usage Memory"
Cohesion: 0.29
Nodes (6): Daedalus TUI Local Persistent Memory, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 8 - "update_repository"
Cohesion: 0.12
Nodes (14): ProjectDiscoveryTests, Textual interface for concurrent local agent tasks., Use Textual's OSC 52 path and a native clipboard fallback., _unregister_app_for_thread_exit(), copy_to_system_clipboard(), paste_from_system_clipboard(), System clipboard helpers for terminals without OSC 52 support., Read clipboard text using the native command available on the host. (+6 more)

### Community 11 - "Key"
Cohesion: 0.31
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
Cohesion: 0.06
Nodes (28): TaskEventCallback, FakeOrchestrator, TaskCoordinatorTests, Promote only events that need the user's attention in the inbox., OrchestrationResult, OrchestrationSettings, IntegrationCoordinator, _nonnegative_int() (+20 more)

### Community 21 - "._shutdown_coordinators"
Cohesion: 0.10
Nodes (4): Key, Keep a task visible after user activity during this launch., Return a TextArea selection or the active screen selection., Add Vim-like navigation without changing TextArea insert behavior.

### Community 22 - "._set_status"
Cohesion: 0.12
Nodes (24): Any, PlanTests, Prefer mounted selector values so clarification refreshes keep choices., build_implementation_prompt(), build_plan_clarification_prompt(), build_plan_followup_prompt(), custom_answer_text(), encode_custom_answer() (+16 more)

### Community 23 - "update_repository"
Cohesion: 0.08
Nodes (21): AbstractEventLoop, BaseException, Exception, Pause active agents before ThreadPoolExecutor joins its workers.      CPython ex, Stop agents before an explicit Textual exit begins., Persist Textual failures that would otherwise only flash on screen., Cover terminal and event-loop exits that bypass Textual unmount., Run before ThreadPoolExecutor's internal interpreter-exit join. (+13 more)

### Community 24 - "Daedalus TUI Coding Statistics"
Cohesion: 0.29
Nodes (6): Daedalus TUI Coding Statistics, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 25 - "DaedalusVimTextArea"
Cohesion: 0.23
Nodes (6): GraphifyTests, Path, Best-effort graph refresh owned by the local orchestration layer., Refresh the primary repository graph without affecting task success., update_repository(), Refresh graph metadata after promotion without blocking the task.

### Community 26 - ".provider_split"
Cohesion: 0.15
Nodes (18): ProgressCallback, Submitted, ProjectInitializerTests, find_github_url(), initialize_project(), load_initializer_settings(), matching_request_marker(), materialize_templates() (+10 more)

### Community 27 - "test_app.py"
Cohesion: 0.10
Nodes (24): PromptTests, TopicsTests, build_repair_prompt(), build_resolver_prompt(), build_task_prompt(), _embedded_profile(), _embedded_topic(), Prompt wrappers used by task and resolver agents. (+16 more)

### Community 28 - "log_exception"
Cohesion: 0.13
Nodes (14): ProjectConfigTests, GitWorktreeError, list_local_branches(), RuntimeError, Local Git worktree lifecycle used by the standalone orchestrator., Return local branch names under ``refs/heads`` without checking anything out., Install project resources and link declared shared read-only paths., load_project_worktree_settings() (+6 more)

### Community 29 - "CodingStatisticsScreen"
Cohesion: 0.14
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

### Community 33 - "CodingStatisticsScreen"
Cohesion: 0.29
Nodes (6): Daedalus TUI Topics, Dev Mode, Key Points, Relevant Files, State Log, Summary

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
Cohesion: 0.16
Nodes (10): EventCallback, IntegrationGate, AgentControl, Cooperative stop signals shared by a task and its active subprocess., AgentStopped, Path, RuntimeError, Load a repository-owned profile immediately before building a prompt. (+2 more)

### Community 42 - "CodingStatisticsScreen"
Cohesion: 0.22
Nodes (5): Changed, CodingStatisticsScreen, _format_count(), _format_tokens(), Show token or task usage history and derived coding statistics.

### Community 43 - "._rebuild_plan_questions"
Cohesion: 0.10
Nodes (10): ComposeResult, Mount, Select, KeyboardShortcutsScreen, PlanAnswerSelect, Initialize dynamic plan selectors after their nested children mount., Replace question controls after Textual has completed child removal., Modal reference for the app and prompt editor keyboard shortcuts. (+2 more)

### Community 44 - "orchestrator.py"
Cohesion: 0.12
Nodes (15): Pressed, ConfigTests, PlanClarificationScreen, ProjectInitializerScreen, Collect a clarification about one plan question., Collect a project slug and create a Daedalus-compatible directory., CodingStatisticsSettings, load_coding_statistics_settings() (+7 more)

## Knowledge Gaps
- **88 isolated node(s):** `daedalus-tui`, `Execution Boundaries (CRITICAL)`, `Evidence Extraction`, `Architecture Boundaries`, `Parameter Files` (+83 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DaedalusTuiApp` connect `PlanQuestion` to `DaedalusVimTextArea`, `AgentRunner`, `GitWorktreeManager`, `update_repository`, `CodingStatisticsScreen`, `._rebuild_plan_questions`, `orchestrator.py`, `.__init__`, `._shutdown_coordinators`, `._set_status`, `update_repository`, `CodingStatisticsScreen`, `calculate_token_usage`?**
  _High betweenness centrality (0.186) - this node is a cross-community bridge._
- **Why does `AgentRunner` connect `AgentRunner` to `PlanQuestion`, `app.py`, `update_repository`, `KeyboardShortcutsScreen`, `CodingStatisticsScreen`, `._rebuild_plan_questions`, `orchestrator.py`, `Key`, `.__init__`?**
  _High betweenness centrality (0.104) - this node is a cross-community bridge._
- **Why does `TaskCoordinator` connect `.__init__` to `PlanQuestion`, `AgentRunner`, `DaedalusTuiApp`, `update_repository`, `KeyboardShortcutsScreen`, `CodingStatisticsScreen`, `._rebuild_plan_questions`, `orchestrator.py`, `Key`, `._set_status`, `log_exception`, `calculate_token_usage`?**
  _High betweenness centrality (0.086) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `DaedalusTuiApp` (e.g. with `FakeCoordinator` and `FakeRunner`) actually correct?**
  _`DaedalusTuiApp` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `TuiAppTests` (e.g. with `CodingStatisticsScreen` and `DaedalusTuiApp`) actually correct?**
  _`TuiAppTests` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `TaskCoordinator` (e.g. with `FakeOrchestrator` and `TaskCoordinatorTests`) actually correct?**
  _`TaskCoordinator` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `GitWorktreeManager` (e.g. with `GitWorktreeTests` and `ProjectWorktreeSettings`) actually correct?**
  _`GitWorktreeManager` has 9 INFERRED edges - model-reasoned connections that need verification._