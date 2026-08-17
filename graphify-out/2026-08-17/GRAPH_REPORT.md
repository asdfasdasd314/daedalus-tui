# Graph Report - daedalus-tui  (2026-08-17)

## Corpus Check
- 46 files · ~25,163 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 637 nodes · 1635 edges · 29 communities (25 shown, 4 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 209 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `95ebd16c`
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

## God Nodes (most connected - your core abstractions)
1. `DaedalusTuiApp` - 85 edges
2. `TuiAppTests` - 57 edges
3. `AgentRunner` - 52 edges
4. `TaskCoordinator` - 52 edges
5. `DaedalusVimTextArea` - 49 edges
6. `GitWorktreeManager` - 44 edges
7. `OrchestrationSettings` - 42 edges
8. `TaskRecord` - 41 edges
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

## Communities (29 total, 4 thin omitted)

### Community 1 - "DaedalusVimTextArea"
Cohesion: 0.07
Nodes (14): DaedalusVimTextArea, Key, Keep Enter as a newline; Ctrl+Enter remains the app submit key., Route visual-line mode and mirror new yanks to the host clipboard., Add Daedalus prompt commands that the dependency does not provide., Select the current line and enter Vim visual-line mode., Select every character in the lines between the start and cursor., VimTextArea with multiline prompt behavior and system clipboard sync. (+6 more)

### Community 2 - "AgentRunner"
Cohesion: 0.07
Nodes (22): EventCallback, IntegrationGate, OutputCallback, AgentRunnerTests, FakeProcess, FakeStream, InterruptibleProcess, Thread (+14 more)

### Community 3 - "DaedalusTuiApp"
Cohesion: 0.06
Nodes (21): AbstractEventLoop, BaseException, Changed, Exception, Pressed, DaedalusTuiApp, Key, Path (+13 more)

### Community 4 - "app.py"
Cohesion: 0.05
Nodes (42): ComposeResult, datetime, Mount, Select, ConfigTests, ProjectDiscoveryTests, TokenUsageTests, CodingStatisticsScreen (+34 more)

### Community 5 - "TokenUsageStore"
Cohesion: 0.29
Nodes (6): Applying answers, Bridge Agent Profile, Build-loop tasking, cp_doc structure, Hard rules, Purpose

### Community 6 - "GitWorktreeManager"
Cohesion: 0.10
Nodes (13): Log, Style, Strip, Selectable transcript rendering with semantic assistant-message emphasis., A selectable log that can emphasize a task's final assistant message.      ``Log, Return the tone assigned to each rendered transcript line., Use the prompt's normal text color for the final transcript tone., Re-render lines after a surrounding widget's color state changes. (+5 more)

### Community 7 - "Daedalus TUI Local Token Usage Memory"
Cohesion: 0.29
Nodes (6): Daedalus TUI Local Persistent Memory, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 8 - "update_repository"
Cohesion: 0.13
Nodes (5): FakeCoordinator, FakeRunner, settings(), DaedalusProject, A repository recognized by the presence of a ``feature_files`` folder.

### Community 11 - "Key"
Cohesion: 0.06
Nodes (38): GitWorktreeTests, OrchestratorTests, VerificationTests, AgentControl, AgentResult, Cooperative stop signals shared by a task and its active subprocess., GitWorktreeError, GitWorktreeManager (+30 more)

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
Cohesion: 0.12
Nodes (14): TaskEventCallback, FakeOrchestrator, TaskCoordinatorTests, OrchestrationSettings, Path, Submit independent prompts while sharing a serialized integration gate., Send selected plan answers back to the planning agent for confirmation., Create a new coding task from a confirmed plan review. (+6 more)

### Community 21 - "TokenUsageStore"
Cohesion: 0.15
Nodes (9): TaskMemoryStoreTests, Path, Persist task history and the most recently opened project., Return the remembered project path, if the memory contains one., Set the single project marker without losing task records., Backward-compatible alias for :meth:`set_last_opened_project`., Return persisted task snapshots keyed by their stable task ID., Upsert a task snapshot keyed by the task worktree's directory name. (+1 more)

### Community 22 - "build_task_prompt"
Cohesion: 0.22
Nodes (6): paste_from_system_clipboard(), System clipboard helpers for terminals without OSC 52 support., Read clipboard text using the native command available on the host., The Daedalus prompt's incremental Vim editing adapter., Paste Vim's register, falling back to the system clipboard., Paste before the cursor, including from the system clipboard.

### Community 23 - "update_repository"
Cohesion: 0.24
Nodes (8): Cover terminal and event-loop exits that bypass Textual unmount., configure_debug_logging(), install_fault_handler(), _install_thread_exception_logging(), Path, Persistent diagnostics for failures that occur after the Textual screen closes., Write detailed runtime diagnostics to a rotating local log file., Capture fatal faults and ``SIGUSR1`` thread dumps in the debug log.

### Community 24 - "Daedalus TUI Coding Statistics"
Cohesion: 0.29
Nodes (6): Daedalus TUI Coding Statistics, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 25 - "._usage_entries"
Cohesion: 0.24
Nodes (13): Any, PlanTests, build_implementation_prompt(), build_plan_followup_prompt(), parse_plan_response(), _parse_question(), _payload_text(), PlanOption (+5 more)

### Community 26 - ".provider_split"
Cohesion: 0.33
Nodes (5): PromptTests, build_repair_prompt(), build_resolver_prompt(), build_task_prompt(), Prompt wrappers used by task and resolver agents.

### Community 27 - "update_repository"
Cohesion: 0.36
Nodes (4): GraphifyTests, Path, Refresh the primary repository graph without affecting task success., update_repository()

## Knowledge Gaps
- **49 isolated node(s):** `daedalus-tui`, `Execution Boundaries (CRITICAL)`, `Evidence Extraction`, `Architecture Boundaries`, `Parameter Files` (+44 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DaedalusTuiApp` connect `DaedalusTuiApp` to `PlanQuestion`, `DaedalusVimTextArea`, `AgentRunner`, `app.py`, `GitWorktreeManager`, `update_repository`, `.__init__`, `TokenUsageStore`, `update_repository`, `._usage_entries`, `KeyboardShortcutsScreen`?**
  _High betweenness centrality (0.209) - this node is a cross-community bridge._
- **Why does `AgentRunner` connect `AgentRunner` to `DaedalusTuiApp`, `app.py`, `Key`, `.__init__`, `._usage_entries`, `KeyboardShortcutsScreen`?**
  _High betweenness centrality (0.141) - this node is a cross-community bridge._
- **Why does `DaedalusVimTextArea` connect `DaedalusVimTextArea` to `PlanQuestion`, `DaedalusTuiApp`, `app.py`, `GitWorktreeManager`, `update_repository`, `build_task_prompt`, `update_repository`, `._usage_entries`, `KeyboardShortcutsScreen`?**
  _High betweenness centrality (0.112) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `DaedalusTuiApp` (e.g. with `FakeCoordinator` and `FakeRunner`) actually correct?**
  _`DaedalusTuiApp` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `TuiAppTests` (e.g. with `CodingStatisticsScreen` and `DaedalusTuiApp`) actually correct?**
  _`TuiAppTests` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `AgentRunner` (e.g. with `AgentRunnerTests` and `FakeProcess`) actually correct?**
  _`AgentRunner` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `TaskCoordinator` (e.g. with `FakeOrchestrator` and `TaskCoordinatorTests`) actually correct?**
  _`TaskCoordinator` has 16 INFERRED edges - model-reasoned connections that need verification._