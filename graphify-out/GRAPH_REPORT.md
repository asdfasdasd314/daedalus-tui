# Graph Report - daedalus-tui  (2026-08-17)

## Corpus Check
- 46 files · ~25,574 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 644 nodes · 1659 edges · 32 communities (29 shown, 3 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 209 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d965ecd4`
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
- TokenUsageStore
- build_task_prompt
- update_repository
- Daedalus TUI Coding Statistics
- ._usage_entries
- .provider_split
- update_repository
- KeyboardShortcutsScreen
- test_app.py
- discover_projects
- .__init__

## God Nodes (most connected - your core abstractions)
1. `DaedalusTuiApp` - 90 edges
2. `TuiAppTests` - 57 edges
3. `AgentRunner` - 52 edges
4. `TaskCoordinator` - 52 edges
5. `DaedalusVimTextArea` - 48 edges
6. `GitWorktreeManager` - 44 edges
7. `OrchestrationSettings` - 42 edges
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

## Communities (32 total, 3 thin omitted)

### Community 1 - "DaedalusVimTextArea"
Cohesion: 0.07
Nodes (14): DaedalusVimTextArea, Key, Keep Enter as a newline; Ctrl+Enter remains the app submit key., Route visual-line mode and mirror new yanks to the host clipboard., Add Daedalus prompt commands that the dependency does not provide., VimTextArea with multiline prompt behavior and system clipboard sync., Select the current line and enter Vim visual-line mode., Select every character in the lines between the start and cursor. (+6 more)

### Community 2 - "AgentRunner"
Cohesion: 0.08
Nodes (20): AbstractEventLoop, BaseException, OutputCallback, AgentRunnerTests, FakeProcess, FakeStream, InterruptibleProcess, Thread (+12 more)

### Community 3 - "DaedalusTuiApp"
Cohesion: 0.05
Nodes (22): Changed, Exception, Pressed, RowSelected, DaedalusTuiApp, Key, Path, Clear the selected task and unlock a fresh prompt editor. (+14 more)

### Community 4 - "app.py"
Cohesion: 0.14
Nodes (17): datetime, TokenUsageTests, calculate_token_usage(), merge_usage_entries(), _parse_timestamp(), Token usage records and derived coding statistics., Convert persisted task snapshots into usage records., The token usage attributed to one submitted task. (+9 more)

### Community 5 - "TokenUsageStore"
Cohesion: 0.29
Nodes (6): Applying answers, Bridge Agent Profile, Build-loop tasking, cp_doc structure, Hard rules, Purpose

### Community 6 - "GitWorktreeManager"
Cohesion: 0.08
Nodes (16): Log, Mount, Select, Strip, Style, PlanAnswerSelect, Initialize dynamic plan selectors after their nested children mount., Selectable transcript rendering with semantic assistant-message emphasis. (+8 more)

### Community 7 - "Daedalus TUI Local Token Usage Memory"
Cohesion: 0.29
Nodes (6): Daedalus TUI Local Persistent Memory, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 8 - "update_repository"
Cohesion: 0.13
Nodes (5): FakeCoordinator, FakeRunner, settings(), DaedalusProject, A repository recognized by the presence of a ``feature_files`` folder.

### Community 11 - "Key"
Cohesion: 0.06
Nodes (37): GitWorktreeTests, OrchestratorTests, VerificationTests, AgentControl, AgentResult, Cooperative stop signals shared by a task and its active subprocess., GitWorktreeError, GitWorktreeManager (+29 more)

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
Cohesion: 0.10
Nodes (16): TaskEventCallback, FakeOrchestrator, TaskCoordinatorTests, OrchestrationSettings, IntegrationCoordinator, Path, Submit independent prompts while sharing a serialized integration gate., Send selected plan answers back to the planning agent for confirmation. (+8 more)

### Community 21 - "TokenUsageStore"
Cohesion: 0.13
Nodes (10): TaskMemoryStoreTests, Path, Small local JSON stores for persistent task history., Persist task history and the most recently opened project., Return the remembered project path, if the memory contains one., Set the single project marker without losing task records., Backward-compatible alias for :meth:`set_last_opened_project`., Return persisted task snapshots keyed by their stable task ID. (+2 more)

### Community 22 - "build_task_prompt"
Cohesion: 0.16
Nodes (9): Textual interface for concurrent local agent tasks., Use Textual's OSC 52 path and a native clipboard fallback., copy_to_system_clipboard(), paste_from_system_clipboard(), System clipboard helpers for terminals without OSC 52 support., Read clipboard text using the native command available on the host., The Daedalus prompt's incremental Vim editing adapter., Paste Vim's register, falling back to the system clipboard. (+1 more)

### Community 23 - "update_repository"
Cohesion: 0.32
Nodes (7): configure_debug_logging(), install_fault_handler(), _install_thread_exception_logging(), Path, Persistent diagnostics for failures that occur after the Textual screen closes., Write detailed runtime diagnostics to a rotating local log file., Capture fatal faults and ``SIGUSR1`` thread dumps in the debug log.

### Community 24 - "Daedalus TUI Coding Statistics"
Cohesion: 0.29
Nodes (6): Daedalus TUI Coding Statistics, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 25 - "._usage_entries"
Cohesion: 0.26
Nodes (12): Any, PlanTests, build_implementation_prompt(), build_plan_followup_prompt(), parse_plan_response(), _parse_question(), _payload_text(), PlanOption (+4 more)

### Community 26 - ".provider_split"
Cohesion: 0.33
Nodes (5): PromptTests, build_repair_prompt(), build_resolver_prompt(), build_task_prompt(), Prompt wrappers used by task and resolver agents.

### Community 27 - "update_repository"
Cohesion: 0.29
Nodes (5): GraphifyTests, Path, Best-effort graph refresh owned by the local orchestration layer., Refresh the primary repository graph without affecting task success., update_repository()

### Community 28 - "KeyboardShortcutsScreen"
Cohesion: 0.17
Nodes (7): ComposeResult, CodingStatisticsScreen, _format_tokens(), KeyboardShortcutsScreen, Show token usage history and derived coding statistics., Modal reference for the app and prompt editor keyboard shortcuts., CodingStatisticsSettings

### Community 29 - "test_app.py"
Cohesion: 0.31
Nodes (9): ConfigTests, load_coding_statistics_settings(), load_orchestration_settings(), load_tui_settings(), ModelOption, _options(), Path, Read-only configuration for the standalone TUI. (+1 more)

### Community 30 - "discover_projects"
Cohesion: 0.31
Nodes (5): ProjectDiscoveryTests, discover_projects(), Path, Discovery of Daedalus-supported repositories beneath a launch root., Recursively find folders containing a direct ``feature_files`` child.      Git m

### Community 31 - ".__init__"
Cohesion: 0.40
Nodes (3): EventCallback, IntegrationGate, Path

## Knowledge Gaps
- **49 isolated node(s):** `daedalus-tui`, `Execution Boundaries (CRITICAL)`, `Evidence Extraction`, `Architecture Boundaries`, `Parameter Files` (+44 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DaedalusTuiApp` connect `DaedalusTuiApp` to `PlanQuestion`, `DaedalusVimTextArea`, `AgentRunner`, `app.py`, `GitWorktreeManager`, `update_repository`, `Key`, `.__init__`, `TokenUsageStore`, `build_task_prompt`, `KeyboardShortcutsScreen`, `test_app.py`?**
  _High betweenness centrality (0.225) - this node is a cross-community bridge._
- **Why does `AgentRunner` connect `AgentRunner` to `DaedalusTuiApp`, `GitWorktreeManager`, `Key`, `.__init__`, `build_task_prompt`, `KeyboardShortcutsScreen`, `.__init__`?**
  _High betweenness centrality (0.141) - this node is a cross-community bridge._
- **Why does `DaedalusVimTextArea` connect `DaedalusVimTextArea` to `PlanQuestion`, `DaedalusTuiApp`, `GitWorktreeManager`, `update_repository`, `build_task_prompt`, `KeyboardShortcutsScreen`, `test_app.py`?**
  _High betweenness centrality (0.106) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `DaedalusTuiApp` (e.g. with `FakeCoordinator` and `FakeRunner`) actually correct?**
  _`DaedalusTuiApp` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `TuiAppTests` (e.g. with `CodingStatisticsScreen` and `DaedalusTuiApp`) actually correct?**
  _`TuiAppTests` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `AgentRunner` (e.g. with `AgentRunnerTests` and `FakeProcess`) actually correct?**
  _`AgentRunner` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `TaskCoordinator` (e.g. with `FakeOrchestrator` and `TaskCoordinatorTests`) actually correct?**
  _`TaskCoordinator` has 16 INFERRED edges - model-reasoned connections that need verification._