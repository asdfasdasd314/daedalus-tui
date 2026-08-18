# Graph Report - daedalus-tui  (2026-08-17)

## Corpus Check
- 46 files · ~26,161 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 654 nodes · 1688 edges · 34 communities (31 shown, 3 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 210 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `36059a05`
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
- test_app.py
- DaedalusProject
- CodingStatisticsScreen
- ._render_selected_task_safely
- discover_projects
- KeyboardShortcutsScreen
- PlanAnswerSelect

## God Nodes (most connected - your core abstractions)
1. `DaedalusTuiApp` - 92 edges
2. `TuiAppTests` - 58 edges
3. `TaskCoordinator` - 53 edges
4. `AgentRunner` - 52 edges
5. `DaedalusVimTextArea` - 48 edges
6. `GitWorktreeManager` - 44 edges
7. `OrchestrationSettings` - 43 edges
8. `TaskRecord` - 42 edges
9. `WorktreeContext` - 37 edges
10. `TaskMemoryStore` - 34 edges

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

## Communities (34 total, 3 thin omitted)

### Community 0 - "PlanQuestion"
Cohesion: 0.15
Nodes (5): Changed, RowSelected, Path, Focus a task from the cross-project update inbox., Switch the project context and focus a row selected in the inbox.

### Community 1 - "DaedalusVimTextArea"
Cohesion: 0.07
Nodes (16): TuiAppTests, PlanOption, DaedalusVimTextArea, Key, Keep Enter as a newline; Ctrl+Enter remains the app submit key., Route visual-line mode and mirror new yanks to the host clipboard., Add Daedalus prompt commands that the dependency does not provide., VimTextArea with multiline prompt behavior and system clipboard sync. (+8 more)

### Community 2 - "AgentRunner"
Cohesion: 0.08
Nodes (19): OutputCallback, AgentRunnerTests, FakeProcess, FakeStream, InterruptibleProcess, Thread, AgentLogEvent, AgentRequest (+11 more)

### Community 3 - "DaedalusTuiApp"
Cohesion: 0.15
Nodes (3): Pressed, DaedalusTuiApp, Replace question controls after Textual has completed child removal.

### Community 4 - "app.py"
Cohesion: 0.07
Nodes (27): datetime, TaskMemoryStoreTests, TokenUsageTests, Path, Small local JSON stores for persistent task history., Persist task history and the most recently opened project., Return the remembered project path, if the memory contains one., Set the single project marker without losing task records. (+19 more)

### Community 5 - "TokenUsageStore"
Cohesion: 0.29
Nodes (6): Applying answers, Bridge Agent Profile, Build-loop tasking, cp_doc structure, Hard rules, Purpose

### Community 6 - "GitWorktreeManager"
Cohesion: 0.11
Nodes (12): Log, Strip, Style, Selectable transcript rendering with semantic assistant-message emphasis., A selectable log that can emphasize a task's final assistant message.      ``Log, Return the tone assigned to each rendered transcript line., Use the prompt's normal text color for the final transcript tone., Re-render lines after a surrounding widget's color state changes. (+4 more)

### Community 7 - "Daedalus TUI Local Token Usage Memory"
Cohesion: 0.29
Nodes (6): Daedalus TUI Local Persistent Memory, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 11 - "Key"
Cohesion: 0.05
Nodes (42): EventCallback, IntegrationGate, GitWorktreeTests, GraphifyTests, OrchestratorTests, VerificationTests, AgentControl, AgentResult (+34 more)

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
Cohesion: 0.08
Nodes (29): Any, TaskEventCallback, PlanTests, FakeOrchestrator, TaskCoordinatorTests, OrchestrationResult, OrchestrationSettings, build_implementation_prompt() (+21 more)

### Community 21 - "._shutdown_coordinators"
Cohesion: 0.13
Nodes (8): Exception, Stop agents before an explicit Textual exit begins., Persist Textual failures that would otherwise only flash on screen., Run before ThreadPoolExecutor's internal interpreter-exit join., Clean up if Textual's run loop returns without its unmount hook., Idempotently detach task callbacks and request child-process shutdown., _unregister_app_for_thread_exit(), close_fault_handler()

### Community 22 - "._set_status"
Cohesion: 0.20
Nodes (4): Key, Return a TextArea selection or the active screen selection., Use Textual's OSC 52 path and a native clipboard fallback., Add Vim-like navigation without changing TextArea insert behavior.

### Community 23 - "update_repository"
Cohesion: 0.13
Nodes (15): AbstractEventLoop, BaseException, Cancel active agents before ThreadPoolExecutor joins its workers.      CPython e, Cover terminal and event-loop exits that bypass Textual unmount., _register_app_for_thread_exit(), _shutdown_apps_before_thread_join(), configure_debug_logging(), install_fault_handler() (+7 more)

### Community 24 - "Daedalus TUI Coding Statistics"
Cohesion: 0.29
Nodes (6): Daedalus TUI Coding Statistics, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 25 - "._usage_entries"
Cohesion: 0.21
Nodes (8): Textual interface for concurrent local agent tasks., copy_to_system_clipboard(), paste_from_system_clipboard(), System clipboard helpers for terminals without OSC 52 support., Read clipboard text using the native command available on the host., The Daedalus prompt's incremental Vim editing adapter., Paste Vim's register, falling back to the system clipboard., Paste before the cursor, including from the system clipboard.

### Community 26 - ".provider_split"
Cohesion: 0.33
Nodes (5): PromptTests, build_repair_prompt(), build_resolver_prompt(), build_task_prompt(), Prompt wrappers used by task and resolver agents.

### Community 27 - "test_app.py"
Cohesion: 0.33
Nodes (8): ConfigTests, load_orchestration_settings(), load_tui_settings(), ModelOption, _options(), Path, Read-only configuration for the standalone TUI., TuiSettings

### Community 28 - "DaedalusProject"
Cohesion: 0.31
Nodes (4): FakeRunner, settings(), DaedalusProject, A repository recognized by the presence of a ``feature_files`` folder.

### Community 29 - "CodingStatisticsScreen"
Cohesion: 0.29
Nodes (5): CodingStatisticsScreen, _format_tokens(), Show token usage history and derived coding statistics., CodingStatisticsSettings, load_coding_statistics_settings()

### Community 30 - "._render_selected_task_safely"
Cohesion: 0.22
Nodes (3): Clear the selected task and unlock a fresh prompt editor., Render every known task, promoting rows with unseen updates., Keep one bad dynamic widget update from closing the entire TUI.

### Community 31 - "discover_projects"
Cohesion: 0.31
Nodes (5): ProjectDiscoveryTests, discover_projects(), Path, Discovery of Daedalus-supported repositories beneath a launch root., Recursively find folders containing a direct ``feature_files`` child.      Git m

### Community 32 - "KeyboardShortcutsScreen"
Cohesion: 0.33
Nodes (3): ComposeResult, KeyboardShortcutsScreen, Modal reference for the app and prompt editor keyboard shortcuts.

### Community 33 - "PlanAnswerSelect"
Cohesion: 0.33
Nodes (4): Mount, Select, PlanAnswerSelect, Initialize dynamic plan selectors after their nested children mount.

## Knowledge Gaps
- **49 isolated node(s):** `daedalus-tui`, `Execution Boundaries (CRITICAL)`, `Evidence Extraction`, `Architecture Boundaries`, `Parameter Files` (+44 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DaedalusTuiApp` connect `DaedalusTuiApp` to `KeyboardShortcutsScreen`, `DaedalusVimTextArea`, `AgentRunner`, `PlanQuestion`, `app.py`, `GitWorktreeManager`, `update_repository`, `.__init__`, `._shutdown_coordinators`, `._set_status`, `update_repository`, `._usage_entries`, `test_app.py`, `DaedalusProject`, `CodingStatisticsScreen`, `._render_selected_task_safely`?**
  _High betweenness centrality (0.228) - this node is a cross-community bridge._
- **Why does `AgentRunner` connect `AgentRunner` to `KeyboardShortcutsScreen`, `PlanAnswerSelect`, `DaedalusTuiApp`, `Key`, `.__init__`, `._usage_entries`, `CodingStatisticsScreen`?**
  _High betweenness centrality (0.139) - this node is a cross-community bridge._
- **Why does `DaedalusVimTextArea` connect `DaedalusVimTextArea` to `PlanQuestion`, `KeyboardShortcutsScreen`, `PlanAnswerSelect`, `DaedalusTuiApp`, `GitWorktreeManager`, `update_repository`, `._set_status`, `update_repository`, `._usage_entries`, `test_app.py`, `DaedalusProject`, `CodingStatisticsScreen`?**
  _High betweenness centrality (0.105) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `DaedalusTuiApp` (e.g. with `FakeCoordinator` and `FakeRunner`) actually correct?**
  _`DaedalusTuiApp` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `TuiAppTests` (e.g. with `CodingStatisticsScreen` and `DaedalusTuiApp`) actually correct?**
  _`TuiAppTests` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `TaskCoordinator` (e.g. with `FakeOrchestrator` and `TaskCoordinatorTests`) actually correct?**
  _`TaskCoordinator` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `AgentRunner` (e.g. with `AgentRunnerTests` and `FakeProcess`) actually correct?**
  _`AgentRunner` has 15 INFERRED edges - model-reasoned connections that need verification._