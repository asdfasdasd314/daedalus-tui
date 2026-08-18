# Graph Report - daedalus-tui  (2026-08-17)

## Corpus Check
- 46 files · ~27,188 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 671 nodes · 1738 edges · 29 communities (27 shown, 2 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 211 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `cad6092f`
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

## God Nodes (most connected - your core abstractions)
1. `DaedalusTuiApp` - 93 edges
2. `TuiAppTests` - 60 edges
3. `TaskCoordinator` - 57 edges
4. `AgentRunner` - 53 edges
5. `DaedalusVimTextArea` - 48 edges
6. `OrchestrationSettings` - 46 edges
7. `GitWorktreeManager` - 45 edges
8. `TaskRecord` - 45 edges
9. `WorktreeContext` - 38 edges
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
- `FakeRunner` --uses--> `DaedalusTuiApp`  [INFERRED]
  tests/test_app.py → tui/app.py

## Import Cycles
- None detected.

## Communities (29 total, 2 thin omitted)

### Community 0 - "PlanQuestion"
Cohesion: 0.23
Nodes (13): Any, PlanTests, build_implementation_prompt(), build_plan_followup_prompt(), parse_plan_response(), _parse_question(), _payload_text(), PlanOption (+5 more)

### Community 1 - "DaedalusVimTextArea"
Cohesion: 0.07
Nodes (15): TuiAppTests, DaedalusVimTextArea, Key, Keep Enter as a newline; Ctrl+Enter remains the app submit key., Route visual-line mode and mirror new yanks to the host clipboard., Add Daedalus prompt commands that the dependency does not provide., VimTextArea with multiline prompt behavior and system clipboard sync., Select the current line and enter Vim visual-line mode. (+7 more)

### Community 2 - "AgentRunner"
Cohesion: 0.07
Nodes (19): OutputCallback, AgentRunnerTests, FakeProcess, FakeStream, InterruptibleProcess, Thread, AgentLogEvent, AgentRequest (+11 more)

### Community 3 - "DaedalusTuiApp"
Cohesion: 0.11
Nodes (4): Pressed, Key, Return a TextArea selection or the active screen selection., Add Vim-like navigation without changing TextArea insert behavior.

### Community 4 - "app.py"
Cohesion: 0.05
Nodes (38): datetime, TaskMemoryStoreTests, TokenUsageTests, Textual interface for concurrent local agent tasks., _unregister_app_for_thread_exit(), copy_to_system_clipboard(), paste_from_system_clipboard(), System clipboard helpers for terminals without OSC 52 support. (+30 more)

### Community 5 - "TokenUsageStore"
Cohesion: 0.29
Nodes (6): Applying answers, Bridge Agent Profile, Build-loop tasking, cp_doc structure, Hard rules, Purpose

### Community 6 - "GitWorktreeManager"
Cohesion: 0.33
Nodes (4): Strip, Style, Render a line with the final-message color before selection styling., Render the native cursor without a background in visible modes.

### Community 7 - "Daedalus TUI Local Token Usage Memory"
Cohesion: 0.29
Nodes (6): Daedalus TUI Local Persistent Memory, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 8 - "update_repository"
Cohesion: 0.06
Nodes (26): ComposeResult, FakeCoordinator, FakeRunner, settings(), ConfigTests, ProjectDiscoveryTests, CodingStatisticsScreen, _format_tokens() (+18 more)

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
Cohesion: 0.08
Nodes (22): Mount, Select, TaskEventCallback, FakeOrchestrator, TaskCoordinatorTests, PlanAnswerSelect, Replace question controls after Textual has completed child removal., Initialize dynamic plan selectors after their nested children mount. (+14 more)

### Community 21 - "._shutdown_coordinators"
Cohesion: 0.23
Nodes (4): Changed, DaedalusTuiApp, Path, Use Textual's OSC 52 path and a native clipboard fallback.

### Community 22 - "._set_status"
Cohesion: 0.16
Nodes (6): RowSelected, Clear the selected task and unlock a fresh prompt editor., Focus a task from the cross-project update inbox., Render every known task, promoting rows with unseen updates., Switch the project context and focus a row selected in the inbox., Keep one bad dynamic widget update from closing the entire TUI.

### Community 23 - "update_repository"
Cohesion: 0.14
Nodes (9): Exception, Cancel active agents before ThreadPoolExecutor joins its workers.      CPython e, Stop agents before an explicit Textual exit begins., Persist Textual failures that would otherwise only flash on screen., Run before ThreadPoolExecutor's internal interpreter-exit join., Clean up if Textual's run loop returns without its unmount hook., Idempotently detach task callbacks and request child-process shutdown., _register_app_for_thread_exit() (+1 more)

### Community 24 - "Daedalus TUI Coding Statistics"
Cohesion: 0.29
Nodes (6): Daedalus TUI Coding Statistics, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 25 - "._usage_entries"
Cohesion: 0.17
Nodes (7): Log, A selectable log that can emphasize a task's final assistant message.      ``Log, Return the tone assigned to each rendered transcript line., Use the prompt's normal text color for the final transcript tone., Re-render lines after a surrounding widget's color state changes., Append one assistant message and assign its semantic tone., TranscriptLog

### Community 26 - ".provider_split"
Cohesion: 0.20
Nodes (5): AbstractEventLoop, BaseException, Promote only events that need the user's attention in the inbox., log_exception(), main()

### Community 27 - "CodingStatisticsScreen"
Cohesion: 0.33
Nodes (5): PromptTests, build_repair_prompt(), build_resolver_prompt(), build_task_prompt(), Prompt wrappers used by task and resolver agents.

### Community 28 - "KeyboardShortcutsScreen"
Cohesion: 0.24
Nodes (8): Cover terminal and event-loop exits that bypass Textual unmount., configure_debug_logging(), install_fault_handler(), _install_thread_exception_logging(), Path, Persistent diagnostics for failures that occur after the Textual screen closes., Write detailed runtime diagnostics to a rotating local log file., Capture fatal faults and ``SIGUSR1`` thread dumps in the debug log.

## Knowledge Gaps
- **49 isolated node(s):** `daedalus-tui`, `Execution Boundaries (CRITICAL)`, `Evidence Extraction`, `Architecture Boundaries`, `Parameter Files` (+44 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DaedalusTuiApp` connect `._shutdown_coordinators` to `PlanQuestion`, `DaedalusVimTextArea`, `AgentRunner`, `DaedalusTuiApp`, `app.py`, `update_repository`, `Key`, `.__init__`, `._set_status`, `update_repository`, `._usage_entries`, `.provider_split`, `KeyboardShortcutsScreen`?**
  _High betweenness centrality (0.225) - this node is a cross-community bridge._
- **Why does `AgentRunner` connect `AgentRunner` to `PlanQuestion`, `app.py`, `update_repository`, `Key`, `.__init__`, `._shutdown_coordinators`?**
  _High betweenness centrality (0.142) - this node is a cross-community bridge._
- **Why does `DaedalusVimTextArea` connect `DaedalusVimTextArea` to `PlanQuestion`, `DaedalusTuiApp`, `app.py`, `GitWorktreeManager`, `update_repository`, `.__init__`, `._shutdown_coordinators`, `._usage_entries`, `KeyboardShortcutsScreen`?**
  _High betweenness centrality (0.103) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `DaedalusTuiApp` (e.g. with `FakeCoordinator` and `FakeRunner`) actually correct?**
  _`DaedalusTuiApp` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `TuiAppTests` (e.g. with `CodingStatisticsScreen` and `DaedalusTuiApp`) actually correct?**
  _`TuiAppTests` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `TaskCoordinator` (e.g. with `FakeOrchestrator` and `TaskCoordinatorTests`) actually correct?**
  _`TaskCoordinator` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `AgentRunner` (e.g. with `AgentRunnerTests` and `FakeProcess`) actually correct?**
  _`AgentRunner` has 15 INFERRED edges - model-reasoned connections that need verification._