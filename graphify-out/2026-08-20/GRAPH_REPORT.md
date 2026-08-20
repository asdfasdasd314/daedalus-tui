# Graph Report - daedalus-tui  (2026-08-17)

## Corpus Check
- 46 files · ~28,439 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 684 nodes · 1780 edges · 37 communities (32 shown, 5 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 212 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2de26901`
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
- ._usage_entries
- .provider_split
- CodingStatisticsScreen
- KeyboardShortcutsScreen
- PlanAnswerSelect
- calculate_token_usage
- log_exception
- test_app.py
- CodingStatisticsScreen
- PlanAnswerSelect
- discover_projects
- ._render_line_strip

## God Nodes (most connected - your core abstractions)
1. `DaedalusTuiApp` - 93 edges
2. `TuiAppTests` - 60 edges
3. `TaskCoordinator` - 57 edges
4. `AgentRunner` - 53 edges
5. `OrchestrationSettings` - 48 edges
6. `DaedalusVimTextArea` - 48 edges
7. `GitWorktreeManager` - 45 edges
8. `TaskRecord` - 45 edges
9. `WorktreeContext` - 40 edges
10. `LocalOrchestrator` - 37 edges

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

## Communities (37 total, 5 thin omitted)

### Community 0 - "PlanQuestion"
Cohesion: 0.27
Nodes (3): Path, Render every known task, promoting rows with unseen updates., Switch the project context and focus a row selected in the inbox.

### Community 2 - "AgentRunner"
Cohesion: 0.07
Nodes (21): OutputCallback, AgentRunnerTests, FakeProcess, FakeStream, InterruptibleProcess, Thread, AgentLogEvent, AgentRequest (+13 more)

### Community 3 - "DaedalusTuiApp"
Cohesion: 0.12
Nodes (6): Pressed, DaedalusTuiApp, Key, Replace question controls after Textual has completed child removal., Return a TextArea selection or the active screen selection., Add Vim-like navigation without changing TextArea insert behavior.

### Community 4 - "app.py"
Cohesion: 0.15
Nodes (9): TaskMemoryStoreTests, Path, Persist task history and the most recently opened project., Return the remembered project path, if the memory contains one., Set the single project marker without losing task records., Backward-compatible alias for :meth:`set_last_opened_project`., Return persisted task snapshots keyed by their stable task ID., Upsert a task snapshot keyed by the task worktree's directory name. (+1 more)

### Community 5 - "TokenUsageStore"
Cohesion: 0.29
Nodes (6): Applying answers, Bridge Agent Profile, Build-loop tasking, cp_doc structure, Hard rules, Purpose

### Community 6 - "GitWorktreeManager"
Cohesion: 0.13
Nodes (7): Log, A selectable log that can emphasize a task's final assistant message.      ``Log, Return the tone assigned to each rendered transcript line., Use the prompt's normal text color for the final transcript tone., Re-render lines after a surrounding widget's color state changes., Append one assistant message and assign its semantic tone., TranscriptLog

### Community 7 - "Daedalus TUI Local Token Usage Memory"
Cohesion: 0.29
Nodes (6): Daedalus TUI Local Persistent Memory, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 8 - "update_repository"
Cohesion: 0.10
Nodes (7): FakeCoordinator, FakeRunner, settings(), KeyboardShortcutsScreen, Modal reference for the app and prompt editor keyboard shortcuts., DaedalusProject, A repository recognized by the presence of a ``feature_files`` folder.

### Community 11 - "Key"
Cohesion: 0.05
Nodes (45): EventCallback, IntegrationGate, GitWorktreeTests, GraphifyTests, OrchestratorTests, VerificationTests, AgentControl, AgentResult (+37 more)

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
Nodes (17): TaskEventCallback, FakeOrchestrator, TaskCoordinatorTests, OrchestrationSettings, IntegrationCoordinator, Path, Submit independent prompts while sharing a serialized integration gate., Send selected plan answers back to the planning agent for confirmation. (+9 more)

### Community 21 - "._shutdown_coordinators"
Cohesion: 0.24
Nodes (11): Any, PlanTests, build_implementation_prompt(), build_plan_followup_prompt(), parse_plan_response(), _parse_question(), _payload_text(), PlanQuestion (+3 more)

### Community 22 - "._set_status"
Cohesion: 0.12
Nodes (10): Exception, Cancel active agents before ThreadPoolExecutor joins its workers.      CPython e, Stop agents before an explicit Textual exit begins., Persist Textual failures that would otherwise only flash on screen., Cover terminal and event-loop exits that bypass Textual unmount., Run before ThreadPoolExecutor's internal interpreter-exit join., Clean up if Textual's run loop returns without its unmount hook., Idempotently detach task callbacks and request child-process shutdown. (+2 more)

### Community 23 - "update_repository"
Cohesion: 0.20
Nodes (9): _unregister_app_for_thread_exit(), close_fault_handler(), configure_debug_logging(), install_fault_handler(), _install_thread_exception_logging(), Path, Persistent diagnostics for failures that occur after the Textual screen closes., Write detailed runtime diagnostics to a rotating local log file. (+1 more)

### Community 24 - "Daedalus TUI Coding Statistics"
Cohesion: 0.29
Nodes (6): Daedalus TUI Coding Statistics, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 25 - "._usage_entries"
Cohesion: 0.07
Nodes (14): DaedalusVimTextArea, Key, Keep Enter as a newline; Ctrl+Enter remains the app submit key., Route visual-line mode and mirror new yanks to the host clipboard., Add Daedalus prompt commands that the dependency does not provide., VimTextArea with multiline prompt behavior and system clipboard sync., Select the current line and enter Vim visual-line mode., Select every character in the lines between the start and cursor. (+6 more)

### Community 26 - ".provider_split"
Cohesion: 0.29
Nodes (6): PromptTests, build_repair_prompt(), build_resolver_prompt(), build_task_prompt(), _embedded_profile(), Prompt wrappers used by task and resolver agents.

### Community 27 - "CodingStatisticsScreen"
Cohesion: 0.15
Nodes (10): Textual interface for concurrent local agent tasks., Use Textual's OSC 52 path and a native clipboard fallback., copy_to_system_clipboard(), paste_from_system_clipboard(), System clipboard helpers for terminals without OSC 52 support., Read clipboard text using the native command available on the host., Selectable transcript rendering with semantic assistant-message emphasis., The Daedalus prompt's incremental Vim editing adapter. (+2 more)

### Community 30 - "calculate_token_usage"
Cohesion: 0.13
Nodes (18): datetime, TokenUsageTests, Small local JSON stores for persistent task history., calculate_token_usage(), merge_usage_entries(), _parse_timestamp(), Token usage records and derived coding statistics., The token usage attributed to one submitted task. (+10 more)

### Community 31 - "log_exception"
Cohesion: 0.19
Nodes (6): AbstractEventLoop, BaseException, Promote only events that need the user's attention in the inbox., Keep one bad dynamic widget update from closing the entire TUI., log_exception(), main()

### Community 32 - "test_app.py"
Cohesion: 0.30
Nodes (9): ConfigTests, load_coding_statistics_settings(), load_orchestration_settings(), load_tui_settings(), ModelOption, _options(), Path, Read-only configuration for the standalone TUI. (+1 more)

### Community 33 - "CodingStatisticsScreen"
Cohesion: 0.22
Nodes (6): Changed, CodingStatisticsScreen, _format_count(), _format_tokens(), Show token or task usage history and derived coding statistics., CodingStatisticsSettings

### Community 34 - "PlanAnswerSelect"
Cohesion: 0.22
Nodes (5): ComposeResult, Mount, Select, PlanAnswerSelect, Initialize dynamic plan selectors after their nested children mount.

### Community 35 - "discover_projects"
Cohesion: 0.31
Nodes (5): ProjectDiscoveryTests, discover_projects(), Path, Discovery of Daedalus-supported repositories beneath a launch root., Recursively find folders containing a direct ``feature_files`` child.      Git m

### Community 36 - "._render_line_strip"
Cohesion: 0.33
Nodes (4): Strip, Style, Render a line with the final-message color before selection styling., Render the native cursor without a background in visible modes.

## Knowledge Gaps
- **49 isolated node(s):** `daedalus-tui`, `Execution Boundaries (CRITICAL)`, `Evidence Extraction`, `Architecture Boundaries`, `Parameter Files` (+44 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DaedalusTuiApp` connect `DaedalusTuiApp` to `test_app.py`, `DaedalusVimTextArea`, `AgentRunner`, `CodingStatisticsScreen`, `PlanQuestion`, `app.py`, `GitWorktreeManager`, `update_repository`, `.__init__`, `._set_status`, `update_repository`, `._usage_entries`, `CodingStatisticsScreen`, `KeyboardShortcutsScreen`, `PlanAnswerSelect`, `calculate_token_usage`, `log_exception`?**
  _High betweenness centrality (0.220) - this node is a cross-community bridge._
- **Why does `AgentRunner` connect `AgentRunner` to `PlanQuestion`, `CodingStatisticsScreen`, `PlanAnswerSelect`, `DaedalusTuiApp`, `update_repository`, `Key`, `.__init__`, `CodingStatisticsScreen`?**
  _High betweenness centrality (0.141) - this node is a cross-community bridge._
- **Why does `DaedalusVimTextArea` connect `._usage_entries` to `test_app.py`, `DaedalusVimTextArea`, `CodingStatisticsScreen`, `DaedalusTuiApp`, `PlanAnswerSelect`, `._render_line_strip`, `GitWorktreeManager`, `update_repository`, `._set_status`, `CodingStatisticsScreen`?**
  _High betweenness centrality (0.101) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `DaedalusTuiApp` (e.g. with `FakeCoordinator` and `FakeRunner`) actually correct?**
  _`DaedalusTuiApp` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `TuiAppTests` (e.g. with `CodingStatisticsScreen` and `DaedalusTuiApp`) actually correct?**
  _`TuiAppTests` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `TaskCoordinator` (e.g. with `FakeOrchestrator` and `TaskCoordinatorTests`) actually correct?**
  _`TaskCoordinator` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `AgentRunner` (e.g. with `AgentRunnerTests` and `FakeProcess`) actually correct?**
  _`AgentRunner` has 15 INFERRED edges - model-reasoned connections that need verification._