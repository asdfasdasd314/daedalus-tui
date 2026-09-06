# Graph Report - daedalus-tui  (2026-09-05)

## Corpus Check
- 78 files · ~57,388 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1220 nodes · 3173 edges · 72 communities (62 shown, 10 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 327 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `71863ee6`
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
- TaskRecord
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
- task_coordinator.py
- KeyboardShortcutsScreen
- ._handle_visual_line_mode
- ._start_new_task
- .on_data_table_row_selected
- PlanQuestion
- ._render_line_strip
- CreateTopicScreen
- Daedalus TUI Call Graph Visualization
- b.py
- .action_view_topic
- conftest.py
- cycle_a.py
- ._render_selected_task
- __init__.py
- orchestrator.py
- update_repository
- CodingStatisticsScreen
- load_project_worktree_settings
- .action_view_topic
- PlanClarification
- ._render_selected_task
- ._render_line_strip
- CreateTopicScreen
- _TimeoutTracker
- FakeStream
- tokenize_descriptor
- _collapse_inner_safe

## God Nodes (most connected - your core abstractions)
1. `DaedalusTuiApp` - 134 edges
2. `TuiAppTests` - 89 edges
3. `TaskCoordinator` - 74 edges
4. `OrchestrationSettings` - 65 edges
5. `GitWorktreeManager` - 61 edges
6. `WorktreeContext` - 60 edges
7. `AgentRunner` - 57 edges
8. `TaskRecord` - 57 edges
9. `TaskMemoryStore` - 55 edges
10. `DaedalusVimTextArea` - 54 edges

## Surprising Connections (you probably didn't know these)
- `FakeStream` --uses--> `AgentControl`  [INFERRED]
  tests/test_agent_runner.py → tui/agent_runner.py
- `FakeStream` --uses--> `AgentLogEvent`  [INFERRED]
  tests/test_agent_runner.py → tui/agent_runner.py
- `FakeStream` --uses--> `AgentRequest`  [INFERRED]
  tests/test_agent_runner.py → tui/agent_runner.py
- `FakeStream` --uses--> `AgentRunner`  [INFERRED]
  tests/test_agent_runner.py → tui/agent_runner.py
- `FakeProcess` --uses--> `AgentControl`  [INFERRED]
  tests/test_agent_runner.py → tui/agent_runner.py

## Import Cycles
- None detected.

## Communities (72 total, 10 thin omitted)

### Community 0 - "PlanQuestion"
Cohesion: 0.18
Nodes (27): score_band(), SimilarityResult, _canonical_tree_name(), _histogram_bars(), _layout_extent_y(), _layout_subtree(), _layout_trees(), _LayoutNode (+19 more)

### Community 1 - "DaedalusVimTextArea"
Cohesion: 0.09
Nodes (6): TuiAppTests, DaedalusVimTextArea, VimTextArea with multiline prompt behavior and system clipboard sync., Return to Insert mode after programmatic prompt operations., Move to the end of the current word, or the next word when needed., VimTextArea

### Community 2 - "AgentRunner"
Cohesion: 0.20
Nodes (4): AgentRunnerTests, FakeProcess, InterruptibleProcess, AgentRequest

### Community 4 - "app.py"
Cohesion: 0.12
Nodes (9): Changed, RowSelected, Path, Focus a task from the cross-project update inbox., Memory override for the project, else the parameter-file default., Update the project's coordinator so later submits use ``branch``., Remember the selected topic as the default for the active project., Refresh Branch Select options for the active project and sync coordinator. (+1 more)

### Community 5 - "TokenUsageStore"
Cohesion: 0.29
Nodes (6): Applying answers, Bridge Agent Profile, Build-loop tasking, cp_doc structure, Hard rules, Purpose

### Community 6 - "GitWorktreeManager"
Cohesion: 0.09
Nodes (15): Log, Resize, Show either the full-size transcript or the full-size diagnostics log., Return the width available for transcript text inside the Log., Wrap one logical line at word boundaries when the width permits., A selectable log that can emphasize a task's final assistant message.      ``Log, Split an overlong word with visible hyphens at cell boundaries., Return the tone assigned to each rendered transcript line. (+7 more)

### Community 7 - "Daedalus TUI Local Token Usage Memory"
Cohesion: 0.29
Nodes (6): Daedalus TUI Local Persistent Memory, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 8 - "update_repository"
Cohesion: 0.16
Nodes (14): PromptTests, build_migration_repair_prompt(), build_repair_prompt(), build_resolver_prompt(), build_task_prompt(), build_topic_population_prompt(), _embedded_profile(), _embedded_topic() (+6 more)

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

### Community 20 - "TaskRecord"
Cohesion: 0.14
Nodes (6): Queue a coding task that writes and expands the requested topic file., Promote only events that need the user's attention in the inbox., Render actionable history and tasks created during this session., Keep failures, active work, and all tasks submitted in this launch., Keep one bad dynamic widget update from closing the entire TUI., Clear the selected task and unlock a fresh prompt editor.

### Community 21 - "._shutdown_coordinators"
Cohesion: 0.10
Nodes (5): DaedalusTuiApp, Keep a task visible after user activity during this launch., Prefer mounted selector values so clarification refreshes keep choices., Replace question controls after Textual has completed child removal., Return a TextArea selection or the active screen selection.

### Community 22 - "._set_status"
Cohesion: 0.12
Nodes (11): Textual interface for concurrent local agent tasks., Use Textual's OSC 52 path and a native clipboard fallback., _unregister_app_for_thread_exit(), copy_to_system_clipboard(), paste_from_system_clipboard(), System clipboard helpers for terminals without OSC 52 support., Read clipboard text using the native command available on the host., close_fault_handler() (+3 more)

### Community 23 - "update_repository"
Cohesion: 0.14
Nodes (21): AST, _descriptor_hash(), DescriptorEmbedder, _doc_for_definition(), format_descriptor(), _format_name_list(), invert_edges(), _leading_comments() (+13 more)

### Community 24 - "Daedalus TUI Coding Statistics"
Cohesion: 0.29
Nodes (6): Daedalus TUI Coding Statistics, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 25 - "DaedalusVimTextArea"
Cohesion: 0.14
Nodes (19): TopicsTests, build_topic_template(), list_topic_slugs(), load_topic_text(), Path, Topic file discovery, creation, loading, and prompt embedding., Return missing required headings; empty list means structurally complete., Return a display name suitable for an H1 and a filesystem slug. (+11 more)

### Community 26 - ".provider_split"
Cohesion: 0.18
Nodes (16): ProgressCallback, ProjectInitializerTests, find_github_url(), initialize_project(), matching_request_marker(), materialize_templates(), normalize_github_url(), publish() (+8 more)

### Community 27 - ".on_mount"
Cohesion: 0.13
Nodes (17): CallGraphVisitor, load_config(), main(), Path, CallGraphTreeTests, build_tree(), CallGraphConfig, discover_source_files() (+9 more)

### Community 28 - "log_exception"
Cohesion: 0.29
Nodes (6): Daedalus TUI Topics, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 29 - "CodingStatisticsScreen"
Cohesion: 0.08
Nodes (19): Mount, FakeCoordinator, FakeRunner, settings(), KeyboardShortcutsScreen, PlanAnswerSelect, PlanClarificationScreen, Initialize dynamic plan selectors after their nested children mount. (+11 more)

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
Cohesion: 0.09
Nodes (27): Agent plan text must not be parsed as Textual/Rich markup., Follow-up questions must not crash when old option ids linger on widgets., Deferred Select init must not fatal-exit on a leftover option id., Clearing questions after confirmation must keep the TUI alive., PlanTests, Resolve a Select value that is legal for the current question options., build_implementation_prompt(), build_plan_clarification_prompt() (+19 more)

### Community 34 - "._render_line_strip"
Cohesion: 0.25
Nodes (7): 4-Stage Development Lifecycle, Alignment, Debugging, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization, Topics (when tagged)

### Community 35 - "agent_runner.py"
Cohesion: 0.16
Nodes (5): Pressed, Submitted, ProjectInitializerScreen, Collect a project slug and create a Daedalus-compatible directory., load_initializer_settings()

### Community 36 - "architecture.md"
Cohesion: 0.33
Nodes (5): 4-Stage Development Lifecycle, Evidence Extraction, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization

### Community 37 - "integrating.md"
Cohesion: 0.40
Nodes (4): 4-Stage Development Lifecycle, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization

### Community 38 - "._set_status"
Cohesion: 0.20
Nodes (4): Key, Enable Push only when an origin remote and operating branch are available., Push the Branch Select value for the active project to origin., Add Vim-like navigation without changing TextArea insert behavior.

### Community 39 - "Daedalus Project Instructions"
Cohesion: 0.40
Nodes (4): Daedalus Project Instructions, graphify, Task mode, Topics

### Community 41 - "KeyboardShortcutsScreen"
Cohesion: 0.26
Nodes (7): OrchestratorTests, AgentResult, WorktreeContext, GraphifyResult, LocalOrchestrator, PushResult, VerificationResult

### Community 42 - "CodingStatisticsScreen"
Cohesion: 0.23
Nodes (7): ProjectDiscoveryTests, __getattr__(), Standalone Textual interface and local agent orchestration., discover_projects(), Path, Discovery of Daedalus-supported repositories beneath a launch root., Recursively find folders containing a direct ``feature_files`` child.      Git m

### Community 44 - "task_coordinator.py"
Cohesion: 0.18
Nodes (6): FakeOrchestrator, TaskCoordinatorTests, OrchestrationResult, OrchestrationSettings, Submit independent prompts while sharing a serialized integration gate., TaskCoordinator

### Community 45 - "KeyboardShortcutsScreen"
Cohesion: 0.20
Nodes (9): Constraints and Design Principles, Desired End State, Intended Import Workflow, Open Questions, Project Imports to the Daedalus Format, Scope and Durable Context, State Log, Topic Goal (+1 more)

### Community 46 - "._handle_visual_line_mode"
Cohesion: 0.14
Nodes (8): Key, Keep Enter as a newline; Ctrl+Enter remains the app submit key., Route visual-line mode and mirror new yanks to the host clipboard., Add Daedalus prompt commands that the dependency does not provide., Select the current line and enter Vim visual-line mode., Select every character in the lines between the start and cursor., Handle movement and operators while whole lines are selected., Expose operator-pending so the caret can become an underline.

### Community 47 - "._start_new_task"
Cohesion: 0.15
Nodes (12): AbstractEventLoop, BaseException, Finish Select setup without allowing a stale value to exit the TUI.          Pla, configure_debug_logging(), install_fault_handler(), _install_thread_exception_logging(), log_exception(), Path (+4 more)

### Community 48 - ".on_data_table_row_selected"
Cohesion: 0.15
Nodes (11): EventCallback, IntegrationGate, AgentControl, Cooperative stop signals shared by a task and its active subprocess., AgentStopped, Path, RuntimeError, Load a repository-owned profile immediately before building a prompt. (+3 more)

### Community 49 - "PlanQuestion"
Cohesion: 0.15
Nodes (10): Send selected plan answers back to the planning agent for confirmation., Ask a side-channel clarification about one plan question without plan follow-up., Create a new coding task from a confirmed plan review., Run another planning pass while keeping the task in questioning., Promote a reviewed plan into the normal coding and verification route., Retry a failed agent request after connectivity or service recovery., Run an ask-mode clarification that does not mutate plan conversation state., Remove the clean, read-only planning worktree after coding is queued. (+2 more)

### Community 50 - "._render_line_strip"
Cohesion: 0.12
Nodes (13): TaskEventCallback, IntegrationCoordinator, _nonnegative_int(), _phase_for_status(), Path, Concurrent task state and serialized local integration., Recover review questions from the last persisted plan response., Run ready integration operations one at a time in ready order. (+5 more)

### Community 51 - "CreateTopicScreen"
Cohesion: 0.23
Nodes (8): ConfigTests, CodingStatisticsSettings, load_coding_statistics_settings(), load_orchestration_settings(), load_tui_settings(), _options(), Path, Read-only configuration for the standalone TUI.

### Community 52 - "Daedalus TUI Call Graph Visualization"
Cohesion: 0.29
Nodes (6): Daedalus TUI Call Graph Visualization, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 53 - "b.py"
Cohesion: 0.10
Nodes (21): alpha(), Entry helper that fans out into order and UI branches., beta(), Continue the sample call chain toward gamma., gamma(), Leaf helper in the sample call chain., make_runner(), create_order() (+13 more)

### Community 54 - ".action_view_topic"
Cohesion: 0.23
Nodes (7): SupabaseMigrationsTests, migrations_pending(), push_migrations(), Path, Orchestration-owned Supabase migration push for target project worktrees., Return True when the worktree differs from base under supabase/migrations/., Run non-interactive `supabase db push --yes` in the target worktree.

### Community 55 - "conftest.py"
Cohesion: 0.50
Nodes (3): pytest_configure(), Pytest hooks shared across the test suite., Install pyan3 when call-graph tests run in an environment missing it.

### Community 57 - "._render_selected_task"
Cohesion: 0.14
Nodes (9): Exception, Pause active agents before ThreadPoolExecutor joins its workers.      CPython ex, Stop agents before an explicit Textual exit begins., Persist Textual failures that would otherwise only flash on screen., Run before ThreadPoolExecutor's internal interpreter-exit join., Clean up if Textual's run loop returns without its unmount hook., Idempotently detach task callbacks and request child-process shutdown., _register_app_for_thread_exit() (+1 more)

### Community 59 - "orchestrator.py"
Cohesion: 0.29
Nodes (8): VerificationTests, discover_commands(), format_process_result(), package_has_test_script(), CompletedProcess, Path, Local verification discovery and execution., run_verification()

### Community 60 - "update_repository"
Cohesion: 0.29
Nodes (5): GraphifyTests, Path, Best-effort graph refresh owned by the local orchestration layer., Refresh the primary repository graph without affecting task success., update_repository()

### Community 61 - "CodingStatisticsScreen"
Cohesion: 0.27
Nodes (4): CodingStatisticsScreen, _format_count(), _format_tokens(), Show token or task usage history and derived coding statistics.

### Community 62 - "load_project_worktree_settings"
Cohesion: 0.21
Nodes (5): OutputCallback, Thread, AgentRunner, Run Codex or Cursor directly and emit only assistant-facing messages., Return assistant text deltas from Cursor's stream-json events.

### Community 63 - ".action_view_topic"
Cohesion: 0.20
Nodes (5): Refresh topics and restore the active project's remembered default., Return the selected topic slug, or None for the blank option., Enable topic viewing only when the selector has a real topic., Cover terminal and event-loop exits that bypass Textual unmount., Open the selected project topic in a read-only modal.

### Community 64 - "PlanClarification"
Cohesion: 0.26
Nodes (8): AgentLogEvent, Provider-specific subprocess execution with normalized agent messages., cursor_environment(), Path, Small, dependency-free environment-file loading for local CLI providers., Return the process environment plus local Cursor credentials.      Explicit proc, read_env_file(), Single-run local agent orchestration without daemon or database dependencies.

### Community 65 - "._render_selected_task"
Cohesion: 0.21
Nodes (12): build_symbol_contexts(), extract_docs_for_symbols(), _module_path_candidates(), Path, Extract docstring + leading comments for symbols when source is available., Build per-symbol semantic context from uses-edges and source docs., Symbols that share at least one common caller (excluding self)., Best-effort map from FQN prefixes to Python module paths. (+4 more)

### Community 66 - "._render_line_strip"
Cohesion: 0.22
Nodes (7): Strip, Style, Text, _literal_select_options(), Build Select prompts that Rich will not parse as markup., Render a line with the final-message color before selection styling., Render the native cursor without a background in visible modes.

### Community 67 - "CreateTopicScreen"
Cohesion: 0.25
Nodes (4): CreateTopicScreen, Collect the context needed to initialize and populate a topic file., load_topic_settings(), Load tunable limits for topic creation from the paired parameter file.

### Community 71 - "_collapse_inner_safe"
Cohesion: 0.50
Nodes (4): _collapse_inner_safe(), _collect_node_names(), Any, Run pyan's collapse_inner while skipping anonymous nodes pyan cannot parent-reso

## Knowledge Gaps
- **101 isolated node(s):** `daedalus-tui`, `Execution Boundaries (CRITICAL)`, `Evidence Extraction`, `Architecture Boundaries`, `Parameter Files` (+96 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DaedalusTuiApp` connect `._shutdown_coordinators` to `DaedalusVimTextArea`, `app.py`, `GitWorktreeManager`, `Key`, `TaskRecord`, `._set_status`, `CodingStatisticsScreen`, `calculate_token_usage`, `.on_button_pressed`, `._set_status`, `CodingStatisticsScreen`, `task_coordinator.py`, `._start_new_task`, `PlanQuestion`, `CreateTopicScreen`, `._render_selected_task`, `CodingStatisticsScreen`, `load_project_worktree_settings`, `.action_view_topic`?**
  _High betweenness centrality (0.156) - this node is a cross-community bridge._
- **Why does `TaskCoordinator` connect `task_coordinator.py` to `.on_button_pressed`, `CreateTopicScreen`, `app.py`, `agent_runner.py`, `KeyboardShortcutsScreen`, `CodingStatisticsScreen`, `Key`, `.on_data_table_row_selected`, `PlanQuestion`, `CodingStatisticsScreen`, `CreateTopicScreen`, `._render_line_strip`, `._shutdown_coordinators`, `._set_status`, `calculate_token_usage`, `CodingStatisticsScreen`, `load_project_worktree_settings`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **Why does `GitWorktreeError` connect `Key` to `PlanClarification`, `DaedalusVimTextArea`, `CreateTopicScreen`, `agent_runner.py`, `KeyboardShortcutsScreen`, `task_coordinator.py`, `.on_data_table_row_selected`, `PlanQuestion`, `CodingStatisticsScreen`, `._render_line_strip`, `._shutdown_coordinators`, `._set_status`, `CodingStatisticsScreen`?**
  _High betweenness centrality (0.068) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `DaedalusTuiApp` (e.g. with `FakeCoordinator` and `FakeRunner`) actually correct?**
  _`DaedalusTuiApp` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `TuiAppTests` (e.g. with `CodingStatisticsScreen` and `DaedalusTuiApp`) actually correct?**
  _`TuiAppTests` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 21 inferred relationships involving `TaskCoordinator` (e.g. with `FakeOrchestrator` and `TaskCoordinatorTests`) actually correct?**
  _`TaskCoordinator` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `OrchestrationSettings` (e.g. with `OrchestratorTests` and `FakeOrchestrator`) actually correct?**
  _`OrchestrationSettings` has 16 INFERRED edges - model-reasoned connections that need verification._