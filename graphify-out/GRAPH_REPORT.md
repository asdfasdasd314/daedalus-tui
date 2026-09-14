# Graph Report - daedalus-tui  (2026-09-13)

## Corpus Check
- 87 files · ~68,795 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1466 nodes · 3797 edges · 81 communities (68 shown, 13 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 364 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1393247c`
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
- CompactSettingsSelect
- Daedalus TUI Call Graph Visualization
- b.py
- update_repository
- conftest.py
- cycle_a.py
- DescriptorEmbedder
- __init__.py
- render_call_graph_tree
- trading.py
- CodingStatisticsScreen
- ambiguous_a.py
- ambiguous_b.py
- module_resource.py
- scopes.py
- task_coordinator.py
- __init__.py
- PlanQuestion
- ._set_status
- debug_log.py
- _collapse_inner_safe
- render_call_graph_tree.py
- CandidateFeatureGroup
- __init__.py
- CallGraphRunnerTests
- .action_view_topic
- .cursor_shape
- .enter_insert_mode
- .nav_word_end
- .edit_paste_after

## God Nodes (most connected - your core abstractions)
1. `DaedalusTuiApp` - 153 edges
2. `TuiAppTests` - 98 edges
3. `TaskCoordinator` - 75 edges
4. `OrchestrationSettings` - 66 edges
5. `GitWorktreeManager` - 61 edges
6. `WorktreeContext` - 60 edges
7. `TaskRecord` - 59 edges
8. `DaedalusVimTextArea` - 59 edges
9. `AgentRunner` - 58 edges
10. `TaskMemoryStore` - 56 edges

## Surprising Connections (you probably didn't know these)
- `FakeRunner` --uses--> `CodingStatisticsScreen`  [INFERRED]
  tests/test_app.py → tui/app.py
- `FakeRunner` --uses--> `DaedalusTuiApp`  [INFERRED]
  tests/test_app.py → tui/app.py
- `FakeRunner` --uses--> `PlanClarificationScreen`  [INFERRED]
  tests/test_app.py → tui/app.py
- `FakeRunner` --uses--> `LayoutSettings`  [INFERRED]
  tests/test_app.py → tui/config.py
- `FakeRunner` --uses--> `ModelOption`  [INFERRED]
  tests/test_app.py → tui/config.py

## Import Cycles
- None detected.

## Communities (81 total, 13 thin omitted)

### Community 0 - "PlanQuestion"
Cohesion: 0.18
Nodes (25): score_band(), _canonical_tree_name(), _collapse_inner_safe(), _collect_node_names(), _histogram_bars(), _layout_extent_y(), _layout_subtree(), _layout_trees() (+17 more)

### Community 1 - "DaedalusVimTextArea"
Cohesion: 0.06
Nodes (30): TaskEventCallback, FakeOrchestrator, TaskCoordinatorTests, OrchestrationResult, OrchestrationSettings, is_valid_plan_answer(), Validate agent option ids and the software-owned custom answer format., IntegrationCoordinator (+22 more)

### Community 2 - "AgentRunner"
Cohesion: 0.06
Nodes (24): OutputCallback, AgentRunnerTests, FakeProcess, FakeStream, InterruptibleProcess, Thread, AgentControl, AgentLogEvent (+16 more)

### Community 3 - "DaedalusTuiApp"
Cohesion: 0.06
Nodes (48): AnnAssign, Assign, AsyncFunctionDef, Attribute, AugAssign, Call, ClassDef, comprehension (+40 more)

### Community 4 - "app.py"
Cohesion: 0.26
Nodes (7): OrchestratorTests, AgentResult, WorktreeContext, GraphifyResult, LocalOrchestrator, PushResult, VerificationResult

### Community 5 - "TokenUsageStore"
Cohesion: 0.29
Nodes (6): Applying answers, Bridge Agent Profile, Build-loop tasking, cp_doc structure, Hard rules, Purpose

### Community 6 - "GitWorktreeManager"
Cohesion: 0.08
Nodes (14): Strip, Style, Resize, Return the width available for transcript text inside the Log., Wrap one logical line at word boundaries when the width permits., Split an overlong word with visible hyphens at cell boundaries., Render a line with the final-message color before selection styling., Reflow stored messages when the output box changes width. (+6 more)

### Community 7 - "Daedalus TUI Local Token Usage Memory"
Cohesion: 0.29
Nodes (6): Daedalus TUI Local Persistent Memory, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 8 - "update_repository"
Cohesion: 0.07
Nodes (35): PromptTests, TopicsTests, build_migration_repair_prompt(), build_repair_prompt(), build_resolver_prompt(), build_task_prompt(), build_topic_population_prompt(), _embedded_profile() (+27 more)

### Community 11 - "Key"
Cohesion: 0.10
Nodes (14): GitWorktreeTests, GitWorktreeError, GitWorktreeManager, list_local_branches(), push_branch(), RuntimeError, Local Git worktree lifecycle used by the standalone orchestrator., Install project resources and link declared shared read-only paths. (+6 more)

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
Cohesion: 0.12
Nodes (10): RowSelected, Focus a task from the cross-project update inbox., Apply only the newest event per task to keep the UI responsive., Promote only events that need the user's attention in the inbox., Render actionable history and tasks created during this session., Keep failures, active work, and all tasks submitted in this launch., Keep inbox cells within their fixed width with a visible ellipsis., Switch the project context and focus a row selected in the inbox. (+2 more)

### Community 21 - "._shutdown_coordinators"
Cohesion: 0.07
Nodes (15): DaedalusTuiApp, Key, Return provider metadata from the shared controls for a new task., Queue a coding task that writes and expands the requested topic file., Remember the selected topic as the default for the active project., Push the Branch Select value for the active project to origin., Return only direct-child projects, or the empty-root fallback., Keep a task visible after user activity during this launch. (+7 more)

### Community 22 - "._set_status"
Cohesion: 0.25
Nodes (6): AbstractEventLoop, BaseException, Exception, Persist Textual failures that would otherwise only flash on screen., log_exception(), main()

### Community 23 - "update_repository"
Cohesion: 0.09
Nodes (32): build_symbol_contexts(), _descriptor_hash(), DescriptorEmbedder, _doc_for_definition(), extract_docs_for_symbols(), format_descriptor(), _format_name_list(), invert_edges() (+24 more)

### Community 24 - "Daedalus TUI Coding Statistics"
Cohesion: 0.29
Nodes (6): Daedalus TUI Coding Statistics, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 25 - "._set_status"
Cohesion: 0.14
Nodes (20): PlanTests, build_implementation_prompt(), build_plan_clarification_prompt(), build_plan_followup_prompt(), custom_answer_text(), encode_custom_answer(), parse_plan_response(), _parse_question() (+12 more)

### Community 26 - ".provider_split"
Cohesion: 0.14
Nodes (18): ProgressCallback, Submitted, ProjectInitializerTests, find_github_url(), initialize_project(), load_initializer_settings(), matching_request_marker(), materialize_templates() (+10 more)

### Community 27 - ".on_mount"
Cohesion: 0.14
Nodes (17): Popen, Protocol, VerificationTests, discover_commands(), format_process_result(), package_has_test_script(), CompletedProcess, Path (+9 more)

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
Cohesion: 0.23
Nodes (7): SupabaseMigrationsTests, migrations_pending(), push_migrations(), Path, Orchestration-owned Supabase migration push for target project worktrees., Return True when the worktree differs from base under supabase/migrations/., Run non-interactive `supabase db push --yes` in the target worktree.

### Community 34 - "._render_line_strip"
Cohesion: 0.25
Nodes (7): 4-Stage Development Lifecycle, Alignment, Debugging, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization, Topics (when tagged)

### Community 35 - "agent_runner.py"
Cohesion: 0.13
Nodes (9): Path, Unit tests for AST variable-lineage analysis., _sample_files(), VariableLineageTests, CallGraphConfig, Analyze the project at *project_root* and write the HTML call tree., render_call_graph_tree(), VariableLineageResult (+1 more)

### Community 36 - "architecture.md"
Cohesion: 0.33
Nodes (5): 4-Stage Development Lifecycle, Evidence Extraction, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization

### Community 37 - "integrating.md"
Cohesion: 0.40
Nodes (4): 4-Stage Development Lifecycle, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization

### Community 38 - "._set_status"
Cohesion: 0.09
Nodes (14): Cover terminal and event-loop exits that bypass Textual unmount., Open the selected project topic in a read-only modal., Apply provider-specific model and reasoning choices to all controls., Avoid posting Select.Changed events when the options are unchanged., Return labels and values for one compact settings category., Read the current value from the same selectors used for submission., Populate the compact value Select while retaining its active category., Apply a compact value through the existing wide-control state. (+6 more)

### Community 39 - "Daedalus Project Instructions"
Cohesion: 0.40
Nodes (4): Daedalus Project Instructions, graphify, Task mode, Topics

### Community 41 - "KeyboardShortcutsScreen"
Cohesion: 0.15
Nodes (6): Text, _literal_select_options(), Finish Select setup without allowing a stale value to exit the TUI.          Pla, Resolve a Select value that is legal for the current question options., Replace question controls after Textual has completed child removal., Build Select prompts that Rich will not parse as markup.

### Community 42 - "debug_log.py"
Cohesion: 0.23
Nodes (6): GraphifyTests, Path, Best-effort graph refresh owned by the local orchestration layer., Refresh the primary repository graph without affecting task success., update_repository(), Refresh graph metadata after promotion without blocking the task.

### Community 43 - "._rebuild_plan_questions"
Cohesion: 0.22
Nodes (10): CallGraphTreeTests, candidate_feature_id(), group_candidate_features(), Return a stable ID derived solely from a group's sorted member symbols., Group symbols connected by inclusive-threshold relations.      Parent/child dire, ScoredRelation, SimilarityResult, write_similarity_json() (+2 more)

### Community 44 - "task_coordinator.py"
Cohesion: 0.09
Nodes (10): Pressed, CreateTopicScreen, PlanClarificationScreen, ProjectInitializerScreen, Path, Memory override for the project, else the parameter-file default., Collect a clarification about one plan question., Collect a project slug and create a Daedalus-compatible directory. (+2 more)

### Community 45 - "KeyboardShortcutsScreen"
Cohesion: 0.20
Nodes (9): Constraints and Design Principles, Desired End State, Intended Import Workflow, Open Questions, Project Imports to the Daedalus Format, Scope and Durable Context, State Log, Topic Goal (+1 more)

### Community 46 - "._handle_visual_line_mode"
Cohesion: 0.14
Nodes (8): Key, Keep Enter as a newline; Ctrl+Enter remains the app submit key., Route visual-line mode and mirror new yanks to the host clipboard., Add Daedalus prompt commands that the dependency does not provide., Select the current line and enter Vim visual-line mode., Select every character in the lines between the start and cursor., Handle movement and operators while whole lines are selected., Expose operator-pending so the caret can become an underline.

### Community 47 - "._start_new_task"
Cohesion: 0.12
Nodes (10): Log, Resize, Apply the viewport-aware layout whenever the terminal changes size., Toggle responsive classes and dimensions after a viewport change.          ``com, Measure wide controls after their current layout pass completes., Switch to compact mode when wide controls extend past their bars., Return whether wide-layout controls are clipped or too narrow., A selectable log that can emphasize a task's final assistant message.      ``Log (+2 more)

### Community 48 - "discover_projects"
Cohesion: 0.26
Nodes (7): ProjectDiscoveryTests, discover_projects(), is_direct_child_project(), Path, Discovery of Daedalus-supported repositories beneath a launch root., Return whether ``path`` is an immediate child of ``launch_root``., Find immediate child folders containing a direct ``feature_files`` child.      G

### Community 49 - "._render_line_strip"
Cohesion: 0.10
Nodes (11): CompletedProcess, Path, Stage the current worktree contents for orchestration checks or commit., Remove graphify output changes from an agent worktree.          Graphify refresh, Keep a read-only planning pass from becoming an implementation change., Commit only the generated graph after a successful primary update., Return a directory whose HEAD matches the target branch tip.          When the r, Remove a short-lived primary checkout created for post-promotion work. (+3 more)

### Community 50 - ".test_plan_review_renders_literal_markup_like_agent_text"
Cohesion: 0.10
Nodes (4): TuiAppTests, DaedalusVimTextArea, VimTextArea with multiline prompt behavior and system clipboard sync., VimTextArea

### Community 51 - "CompactSettingsSelect"
Cohesion: 0.17
Nodes (4): ComposeResult, Select, CompactSettingsSelect, Keep only the latest value-change event for rebuilt compact controls.

### Community 52 - "Daedalus TUI Call Graph Visualization"
Cohesion: 0.29
Nodes (6): Daedalus TUI Call Graph Visualization, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 53 - "b.py"
Cohesion: 0.10
Nodes (21): alpha(), Entry helper that fans out into order and UI branches., beta(), Continue the sample call chain toward gamma., gamma(), Leaf helper in the sample call chain., make_runner(), create_order() (+13 more)

### Community 54 - "update_repository"
Cohesion: 0.27
Nodes (4): CodingStatisticsScreen, _format_count(), _format_tokens(), Show token or task usage history and derived coding statistics.

### Community 55 - "conftest.py"
Cohesion: 0.50
Nodes (3): pytest_configure(), Pytest hooks shared across the test suite., Install pyan3 when call-graph tests run in an environment missing it.

### Community 57 - "DescriptorEmbedder"
Cohesion: 0.26
Nodes (10): ConfigTests, LayoutSettings, load_coding_statistics_settings(), load_orchestration_settings(), load_tui_settings(), ModelOption, _options(), Path (+2 more)

### Community 59 - "render_call_graph_tree"
Cohesion: 0.14
Nodes (11): parent_child_score_map(), build_tree(), datetime, Build a call tree from *root* with cycle and depth limits., Render candidate features independently from the similarity panel., Render a self-contained HTML page for the call trees., _render_candidate_features_panel(), render_html() (+3 more)

### Community 60 - "trading.py"
Cohesion: 0.32
Nodes (5): calculate(), execute_trade(), Portfolio, Assignment lineage, augassign, attribute mutate, and unique call mapping., run_pipeline()

### Community 61 - "CodingStatisticsScreen"
Cohesion: 0.22
Nodes (8): EventCallback, IntegrationGate, AgentStopped, Path, RuntimeError, Load a repository-owned profile immediately before building a prompt., Load a tagged topic from the task worktree immediately before a prompt., Expose usage only after the whole task reaches completion.

### Community 62 - "ambiguous_a.py"
Cohesion: 0.67
Nodes (3): helper(), Ambiguous same-named callees should not emit PASSED_TO edges., run_local()

### Community 63 - "ambiguous_b.py"
Cohesion: 0.67
Nodes (3): helper(), Second helper with the same simple name as ambiguous_a.helper., run_other()

### Community 66 - "task_coordinator.py"
Cohesion: 0.29
Nodes (6): ProjectConfigTests, load_project_worktree_settings(), Path, Configuration supplied by a target project to prepare task worktrees., Load optional worktree provisioning settings from a target repository., _string_array()

### Community 68 - "PlanQuestion"
Cohesion: 0.11
Nodes (4): Agent plan text must not be parsed as Textual/Rich markup., Follow-up questions must not crash when old option ids linger on widgets., Deferred Select init must not fatal-exit on a leftover option id., Clearing questions after confirmation must keep the TUI alive.

### Community 69 - "._set_status"
Cohesion: 0.20
Nodes (5): Stop agents before an explicit Textual exit begins., Clean up if Textual's run loop returns without its unmount hook., Idempotently detach task callbacks and request child-process shutdown., _unregister_app_for_thread_exit(), close_fault_handler()

### Community 70 - "debug_log.py"
Cohesion: 0.32
Nodes (7): configure_debug_logging(), install_fault_handler(), _install_thread_exception_logging(), Path, Persistent diagnostics for failures that occur after the Textual screen closes., Write detailed runtime diagnostics to a rotating local log file., Capture fatal faults and ``SIGUSR1`` thread dumps in the debug log.

### Community 71 - "_collapse_inner_safe"
Cohesion: 0.21
Nodes (8): CallGraphVisitor, discover_source_files(), extract_uses_edges(), Path, CallGraphVisitor with a collapse_inner guard for namespace-less anonymous nodes., Run pyan analysis and return caller→callees edges plus all node names., Collect Python source files matching *source_globs* and not *exclude*., _SafeCallGraphVisitor

### Community 72 - "render_call_graph_tree.py"
Cohesion: 0.24
Nodes (14): _flat_parameter_values(), load_config(), _load_parameter_values(), load_runner_parameters(), main(), _project_root_setting(), _project_table(), Path (+6 more)

### Community 73 - "CandidateFeatureGroup"
Cohesion: 0.25
Nodes (6): CandidateFeatureGroup, A deterministic connected component of qualifying similarity relations., Return the stable identifier using the concise ``id`` spelling., Compatibility alias for callers that refer to group relations directly., _feature_ids_by_member(), Map each grouped symbol to its stable candidate-feature ID.

### Community 76 - ".action_view_topic"
Cohesion: 0.40
Nodes (4): Run before ThreadPoolExecutor's internal interpreter-exit join., Pause active agents before ThreadPoolExecutor joins its workers.      CPython ex, _register_app_for_thread_exit(), _shutdown_apps_before_thread_join()

### Community 80 - ".edit_paste_after"
Cohesion: 0.17
Nodes (9): Textual interface for concurrent local agent tasks., copy_to_system_clipboard(), paste_from_system_clipboard(), System clipboard helpers for terminals without OSC 52 support., Read clipboard text using the native command available on the host., Selectable transcript rendering with semantic assistant-message emphasis., The Daedalus prompt's incremental Vim editing adapter., Paste Vim's register, falling back to the system clipboard. (+1 more)

## Knowledge Gaps
- **101 isolated node(s):** `daedalus-tui`, `Execution Boundaries (CRITICAL)`, `Evidence Extraction`, `Architecture Boundaries`, `Parameter Files` (+96 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DaedalusTuiApp` connect `._shutdown_coordinators` to `DaedalusVimTextArea`, `AgentRunner`, `._set_status`, `._set_status`, `KeyboardShortcutsScreen`, `__init__.py`, `Key`, `task_coordinator.py`, `.action_view_topic`, `._start_new_task`, `.edit_paste_after`, `.test_plan_review_renders_literal_markup_like_agent_text`, `TaskRecord`, `update_repository`, `._set_status`, `._set_status`, `CodingStatisticsScreen`, `calculate_token_usage`?**
  _High betweenness centrality (0.140) - this node is a cross-community bridge._
- **Why does `DaedalusVimTextArea` connect `.test_plan_review_renders_literal_markup_like_agent_text` to `._set_status`, `GitWorktreeManager`, `task_coordinator.py`, `.cursor_shape`, `._handle_visual_line_mode`, `._start_new_task`, `.edit_paste_after`, `.enter_insert_mode`, `.nav_word_end`, `CompactSettingsSelect`, `._shutdown_coordinators`, `update_repository`, `CodingStatisticsScreen`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Why does `TuiAppTests` connect `.test_plan_review_renders_literal_markup_like_agent_text` to `PlanQuestion`, `Key`, `task_coordinator.py`, `TaskRecord`, `._shutdown_coordinators`, `update_repository`, `._set_status`, `CodingStatisticsScreen`, `DescriptorEmbedder`?**
  _High betweenness centrality (0.060) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `DaedalusTuiApp` (e.g. with `FakeCoordinator` and `FakeRunner`) actually correct?**
  _`DaedalusTuiApp` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `TuiAppTests` (e.g. with `CodingStatisticsScreen` and `DaedalusTuiApp`) actually correct?**
  _`TuiAppTests` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `TaskCoordinator` (e.g. with `FakeOrchestrator` and `TaskCoordinatorTests`) actually correct?**
  _`TaskCoordinator` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `OrchestrationSettings` (e.g. with `OrchestratorTests` and `FakeOrchestrator`) actually correct?**
  _`OrchestrationSettings` has 17 INFERRED edges - model-reasoned connections that need verification._