# Graph Report - daedalus-tui  (2026-09-05)

## Corpus Check
- 78 files · ~58,157 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1229 nodes · 3205 edges · 65 communities (59 shown, 6 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 327 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `efa00ec2`
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
- ._set_status
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
- debug_log.py
- ._rebuild_plan_questions
- task_coordinator.py
- KeyboardShortcutsScreen
- ._handle_visual_line_mode
- ._start_new_task
- discover_projects
- ._render_line_strip
- .test_plan_review_renders_literal_markup_like_agent_text
- CreateTopicScreen
- Daedalus TUI Call Graph Visualization
- b.py
- run_verification
- conftest.py
- cycle_a.py
- TranscriptLog
- __init__.py
- render_call_graph_tree
- ._create_topic
- CodingStatisticsScreen
- ._render_line_strip
- tokenize_descriptor
- _collapse_inner_safe

## God Nodes (most connected - your core abstractions)
1. `DaedalusTuiApp` - 137 edges
2. `TuiAppTests` - 90 edges
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

## Communities (65 total, 6 thin omitted)

### Community 0 - "PlanQuestion"
Cohesion: 0.18
Nodes (27): score_band(), SimilarityResult, _canonical_tree_name(), _histogram_bars(), _layout_extent_y(), _layout_subtree(), _layout_trees(), _LayoutNode (+19 more)

### Community 1 - "DaedalusVimTextArea"
Cohesion: 0.10
Nodes (6): TuiAppTests, DaedalusVimTextArea, VimTextArea with multiline prompt behavior and system clipboard sync., Return to Insert mode after programmatic prompt operations., Move to the end of the current word, or the next word when needed., VimTextArea

### Community 2 - "AgentRunner"
Cohesion: 0.07
Nodes (21): OutputCallback, AgentRunnerTests, FakeProcess, FakeStream, InterruptibleProcess, Thread, AgentLogEvent, AgentRequest (+13 more)

### Community 4 - "app.py"
Cohesion: 0.23
Nodes (4): Path, Memory override for the project, else the parameter-file default., Update the project's coordinator so later submits use ``branch``., Refresh Branch Select options for the active project and sync coordinator.

### Community 5 - "TokenUsageStore"
Cohesion: 0.29
Nodes (6): Applying answers, Bridge Agent Profile, Build-loop tasking, cp_doc structure, Hard rules, Purpose

### Community 6 - "GitWorktreeManager"
Cohesion: 0.07
Nodes (17): Resize, Strip, Style, Text, _literal_select_options(), Build Select prompts that Rich will not parse as markup., Return the width available for transcript text inside the Log., Wrap one logical line at word boundaries when the width permits. (+9 more)

### Community 7 - "Daedalus TUI Local Token Usage Memory"
Cohesion: 0.29
Nodes (6): Daedalus TUI Local Persistent Memory, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 8 - "update_repository"
Cohesion: 0.14
Nodes (19): TopicsTests, build_topic_instructions(), build_topic_template(), embed_topic(), list_topic_slugs(), load_topic_text(), Path, Topic file discovery, creation, loading, and prompt embedding. (+11 more)

### Community 11 - "Key"
Cohesion: 0.10
Nodes (15): GitWorktreeTests, GitWorktreeError, GitWorktreeManager, list_local_branches(), push_branch(), CompletedProcess, RuntimeError, Local Git worktree lifecycle used by the standalone orchestrator. (+7 more)

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
Cohesion: 0.10
Nodes (12): RowSelected, Queue a coding task that writes and expands the requested topic file., Focus a task from the cross-project update inbox., Promote only events that need the user's attention in the inbox., Refresh topics and restore the active project's remembered default., Render actionable history and tasks created during this session., Keep failures, active work, and all tasks submitted in this launch., Keep inbox cells within their fixed width with a visible ellipsis. (+4 more)

### Community 21 - "._shutdown_coordinators"
Cohesion: 0.08
Nodes (12): Changed, DaedalusTuiApp, Key, Open the selected project topic in a read-only modal., Remember the selected topic as the default for the active project., Return the selected topic slug, or None for the blank option., Enable topic viewing only when the selector has a real topic., Prefer mounted selector values so clarification refreshes keep choices. (+4 more)

### Community 22 - "._set_status"
Cohesion: 0.12
Nodes (14): Textual interface for concurrent local agent tasks., Pause active agents before ThreadPoolExecutor joins its workers.      CPython ex, _register_app_for_thread_exit(), _shutdown_apps_before_thread_join(), _unregister_app_for_thread_exit(), copy_to_system_clipboard(), paste_from_system_clipboard(), System clipboard helpers for terminals without OSC 52 support. (+6 more)

### Community 23 - "update_repository"
Cohesion: 0.13
Nodes (25): AST, build_symbol_contexts(), _doc_for_definition(), extract_docs_for_symbols(), _format_name_list(), invert_edges(), _leading_comments(), _module_path_candidates() (+17 more)

### Community 24 - "Daedalus TUI Coding Statistics"
Cohesion: 0.29
Nodes (6): Daedalus TUI Coding Statistics, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 25 - "._set_status"
Cohesion: 0.08
Nodes (23): GraphifyTests, PromptTests, SupabaseMigrationsTests, Path, Best-effort graph refresh owned by the local orchestration layer., Refresh the primary repository graph without affecting task success., update_repository(), Single-run local agent orchestration without daemon or database dependencies. (+15 more)

### Community 26 - ".provider_split"
Cohesion: 0.09
Nodes (26): ProgressCallback, Submitted, ProjectConfigTests, ProjectInitializerTests, ProjectInitializerScreen, Collect a project slug and create a Daedalus-compatible directory., load_project_worktree_settings(), Path (+18 more)

### Community 27 - ".on_mount"
Cohesion: 0.19
Nodes (10): CallGraphTreeTests, format_descriptor(), Format a stable descriptor using terminal names for graph peers., Score every unique parent→child edge and capped sibling pairs., score_relationships(), SymbolContext, build_tree(), Choose tree roots from configured entry points or orphan graph nodes. (+2 more)

### Community 28 - "log_exception"
Cohesion: 0.29
Nodes (6): Daedalus TUI Topics, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 29 - "CodingStatisticsScreen"
Cohesion: 0.09
Nodes (15): Mount, FakeCoordinator, FakeRunner, settings(), KeyboardShortcutsScreen, PlanAnswerSelect, Initialize dynamic plan selectors after their nested children mount., Modal reference for the app and prompt editor keyboard shortcuts. (+7 more)

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
Cohesion: 0.12
Nodes (23): PlanTests, Resolve a Select value that is legal for the current question options., build_implementation_prompt(), build_plan_clarification_prompt(), build_plan_followup_prompt(), custom_answer_text(), encode_custom_answer(), is_valid_plan_answer() (+15 more)

### Community 34 - "._render_line_strip"
Cohesion: 0.25
Nodes (7): 4-Stage Development Lifecycle, Alignment, Debugging, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization, Topics (when tagged)

### Community 35 - "agent_runner.py"
Cohesion: 0.13
Nodes (5): Pressed, CreateTopicScreen, PlanClarificationScreen, Collect a clarification about one plan question., Collect the context needed to initialize and populate a topic file.

### Community 36 - "architecture.md"
Cohesion: 0.33
Nodes (5): 4-Stage Development Lifecycle, Evidence Extraction, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization

### Community 37 - "integrating.md"
Cohesion: 0.40
Nodes (4): 4-Stage Development Lifecycle, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization

### Community 38 - "._set_status"
Cohesion: 0.25
Nodes (3): Enable Push only when an origin remote and operating branch are available., Push the Branch Select value for the active project to origin., Cover terminal and event-loop exits that bypass Textual unmount.

### Community 39 - "Daedalus Project Instructions"
Cohesion: 0.40
Nodes (4): Daedalus Project Instructions, graphify, Task mode, Topics

### Community 41 - "KeyboardShortcutsScreen"
Cohesion: 0.15
Nodes (11): EventCallback, IntegrationGate, AgentControl, Cooperative stop signals shared by a task and its active subprocess., AgentStopped, Path, RuntimeError, Load a repository-owned profile immediately before building a prompt. (+3 more)

### Community 42 - "debug_log.py"
Cohesion: 0.32
Nodes (7): configure_debug_logging(), install_fault_handler(), _install_thread_exception_logging(), Path, Persistent diagnostics for failures that occur after the Textual screen closes., Write detailed runtime diagnostics to a rotating local log file., Capture fatal faults and ``SIGUSR1`` thread dumps in the debug log.

### Community 43 - "._rebuild_plan_questions"
Cohesion: 0.10
Nodes (10): Path, Stage the current worktree contents for orchestration checks or commit., Remove graphify output changes from an agent worktree.          Graphify refresh, Keep a read-only planning pass from becoming an implementation change., Commit only the generated graph after a successful primary update., Return a directory whose HEAD matches the target branch tip.          When the r, Remove a short-lived primary checkout created for post-promotion work., Remove a cancelled task even when its branch was never integrated. (+2 more)

### Community 44 - "task_coordinator.py"
Cohesion: 0.07
Nodes (29): TaskEventCallback, FakeOrchestrator, TaskCoordinatorTests, OrchestrationResult, OrchestrationSettings, IntegrationCoordinator, _nonnegative_int(), _phase_for_status() (+21 more)

### Community 45 - "KeyboardShortcutsScreen"
Cohesion: 0.20
Nodes (9): Constraints and Design Principles, Desired End State, Intended Import Workflow, Open Questions, Project Imports to the Daedalus Format, Scope and Durable Context, State Log, Topic Goal (+1 more)

### Community 46 - "._handle_visual_line_mode"
Cohesion: 0.14
Nodes (8): Key, Keep Enter as a newline; Ctrl+Enter remains the app submit key., Route visual-line mode and mirror new yanks to the host clipboard., Add Daedalus prompt commands that the dependency does not provide., Select the current line and enter Vim visual-line mode., Select every character in the lines between the start and cursor., Handle movement and operators while whole lines are selected., Expose operator-pending so the caret can become an underline.

### Community 47 - "._start_new_task"
Cohesion: 0.11
Nodes (11): AbstractEventLoop, BaseException, Exception, Finish Select setup without allowing a stale value to exit the TUI.          Pla, Stop agents before an explicit Textual exit begins., Persist Textual failures that would otherwise only flash on screen., Run before ThreadPoolExecutor's internal interpreter-exit join., Clean up if Textual's run loop returns without its unmount hook. (+3 more)

### Community 48 - "discover_projects"
Cohesion: 0.26
Nodes (7): ProjectDiscoveryTests, discover_projects(), is_direct_child_project(), Path, Discovery of Daedalus-supported repositories beneath a launch root., Return whether ``path`` is an immediate child of ``launch_root``., Find immediate child folders containing a direct ``feature_files`` child.      G

### Community 49 - "._render_line_strip"
Cohesion: 0.26
Nodes (7): OrchestratorTests, AgentResult, WorktreeContext, GraphifyResult, LocalOrchestrator, PushResult, VerificationResult

### Community 50 - ".test_plan_review_renders_literal_markup_like_agent_text"
Cohesion: 0.11
Nodes (4): Agent plan text must not be parsed as Textual/Rich markup., Follow-up questions must not crash when old option ids linger on widgets., Deferred Select init must not fatal-exit on a leftover option id., Clearing questions after confirmation must keep the TUI alive.

### Community 51 - "CreateTopicScreen"
Cohesion: 0.31
Nodes (8): ConfigTests, load_coding_statistics_settings(), load_orchestration_settings(), load_tui_settings(), ModelOption, _options(), Path, Read-only configuration for the standalone TUI.

### Community 52 - "Daedalus TUI Call Graph Visualization"
Cohesion: 0.29
Nodes (6): Daedalus TUI Call Graph Visualization, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 53 - "b.py"
Cohesion: 0.10
Nodes (21): alpha(), Entry helper that fans out into order and UI branches., beta(), Continue the sample call chain toward gamma., gamma(), Leaf helper in the sample call chain., make_runner(), create_order() (+13 more)

### Community 54 - "run_verification"
Cohesion: 0.29
Nodes (8): VerificationTests, discover_commands(), format_process_result(), package_has_test_script(), CompletedProcess, Path, Local verification discovery and execution., run_verification()

### Community 55 - "conftest.py"
Cohesion: 0.50
Nodes (3): pytest_configure(), Pytest hooks shared across the test suite., Install pyan3 when call-graph tests run in an environment missing it.

### Community 57 - "TranscriptLog"
Cohesion: 0.24
Nodes (5): Log, Show either the full-size transcript or the full-size diagnostics log., A selectable log that can emphasize a task's final assistant message.      ``Log, Return the tone assigned to each rendered transcript line., TranscriptLog

### Community 59 - "render_call_graph_tree"
Cohesion: 0.43
Nodes (6): load_config(), main(), Path, CallGraphConfig, Analyze the project at *project_root* and write the HTML call tree., render_call_graph_tree()

### Community 60 - "._create_topic"
Cohesion: 0.29
Nodes (6): load_topic_settings(), Load tunable limits for topic creation from the paired parameter file., Return a display name suitable for an H1 and a filesystem slug., Convert a validated topic name to the filename stem used by the TUI., topic_slug_from_name(), validate_topic_name()

### Community 61 - "CodingStatisticsScreen"
Cohesion: 0.23
Nodes (5): CodingStatisticsScreen, _format_count(), _format_tokens(), Show token or task usage history and derived coding statistics., CodingStatisticsSettings

### Community 66 - "._render_line_strip"
Cohesion: 0.18
Nodes (3): ComposeResult, Select, Return only direct-child projects, or the empty-root fallback.

### Community 70 - "tokenize_descriptor"
Cohesion: 0.25
Nodes (5): _descriptor_hash(), DescriptorEmbedder, Lowercase and split identifiers on `.` / `_` while keeping word tokens., Fit TF-IDF over symbol descriptors and score cosine similarity., tokenize_descriptor()

### Community 71 - "_collapse_inner_safe"
Cohesion: 0.17
Nodes (10): CallGraphVisitor, _collapse_inner_safe(), _collect_node_names(), discover_source_files(), extract_uses_edges(), Any, Path, Run pyan's collapse_inner while skipping anonymous nodes pyan cannot parent-reso (+2 more)

## Knowledge Gaps
- **101 isolated node(s):** `daedalus-tui`, `Execution Boundaries (CRITICAL)`, `Evidence Extraction`, `Architecture Boundaries`, `Parameter Files` (+96 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DaedalusTuiApp` connect `._shutdown_coordinators` to `DaedalusVimTextArea`, `AgentRunner`, `agent_runner.py`, `app.py`, `._render_line_strip`, `._set_status`, `.on_button_pressed`, `Key`, `task_coordinator.py`, `._start_new_task`, `CodingStatisticsScreen`, `TaskRecord`, `._set_status`, `TranscriptLog`, `CodingStatisticsScreen`, `calculate_token_usage`?**
  _High betweenness centrality (0.169) - this node is a cross-community bridge._
- **Why does `AgentRunner` connect `AgentRunner` to `agent_runner.py`, `app.py`, `KeyboardShortcutsScreen`, `task_coordinator.py`, `._render_line_strip`, `CodingStatisticsScreen`, `._shutdown_coordinators`, `._set_status`, `._set_status`, `.provider_split`, `CodingStatisticsScreen`?**
  _High betweenness centrality (0.077) - this node is a cross-community bridge._
- **Why does `TaskCoordinator` connect `task_coordinator.py` to `.on_button_pressed`, `AgentRunner`, `agent_runner.py`, `app.py`, `KeyboardShortcutsScreen`, `Key`, `._render_line_strip`, `CodingStatisticsScreen`, `._shutdown_coordinators`, `._set_status`, `.provider_split`, `CodingStatisticsScreen`, `calculate_token_usage`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `DaedalusTuiApp` (e.g. with `FakeCoordinator` and `FakeRunner`) actually correct?**
  _`DaedalusTuiApp` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `TuiAppTests` (e.g. with `CodingStatisticsScreen` and `DaedalusTuiApp`) actually correct?**
  _`TuiAppTests` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 21 inferred relationships involving `TaskCoordinator` (e.g. with `FakeOrchestrator` and `TaskCoordinatorTests`) actually correct?**
  _`TaskCoordinator` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `OrchestrationSettings` (e.g. with `OrchestratorTests` and `FakeOrchestrator`) actually correct?**
  _`OrchestrationSettings` has 16 INFERRED edges - model-reasoned connections that need verification._