# Graph Report - daedalus-tui  (2026-09-07)

## Corpus Check
- 86 files · ~64,720 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1390 nodes · 3601 edges · 69 communities (60 shown, 9 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 338 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4b391b7b`
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
- ._render_line_strip
- __init__.py
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

## Communities (69 total, 9 thin omitted)

### Community 0 - "PlanQuestion"
Cohesion: 0.15
Nodes (27): CandidateFeatureGroup, A deterministic connected component of qualifying similarity relations., Return the stable identifier using the concise ``id`` spelling., Compatibility alias for callers that refer to group relations directly., score_band(), _canonical_tree_name(), _feature_ids_by_member(), _histogram_bars() (+19 more)

### Community 1 - "DaedalusVimTextArea"
Cohesion: 0.11
Nodes (7): TuiAppTests, DaedalusVimTextArea, VimTextArea with multiline prompt behavior and system clipboard sync., Return bar, underline, or block for the current Vim state., Return to Insert mode after programmatic prompt operations., Move to the end of the current word, or the next word when needed., VimTextArea

### Community 2 - "AgentRunner"
Cohesion: 0.10
Nodes (11): OutputCallback, AgentRunnerTests, FakeProcess, FakeStream, InterruptibleProcess, Thread, AgentLogEvent, AgentRequest (+3 more)

### Community 3 - "DaedalusTuiApp"
Cohesion: 0.06
Nodes (49): AnnAssign, Assign, AsyncFunctionDef, Attribute, AugAssign, Call, ClassDef, comprehension (+41 more)

### Community 4 - "app.py"
Cohesion: 0.26
Nodes (7): OrchestratorTests, AgentResult, WorktreeContext, GraphifyResult, LocalOrchestrator, PushResult, VerificationResult

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
Cohesion: 0.07
Nodes (35): PromptTests, TopicsTests, build_migration_repair_prompt(), build_repair_prompt(), build_resolver_prompt(), build_task_prompt(), build_topic_population_prompt(), _embedded_profile() (+27 more)

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
Cohesion: 0.09
Nodes (14): RowSelected, Path, Queue a coding task that writes and expands the requested topic file., Focus a task from the cross-project update inbox., Memory override for the project, else the parameter-file default., Update the project's coordinator so later submits use ``branch``., Return only direct-child projects, or the empty-root fallback., Render actionable history and tasks created during this session. (+6 more)

### Community 21 - "._shutdown_coordinators"
Cohesion: 0.09
Nodes (9): Changed, DaedalusTuiApp, Open the selected project topic in a read-only modal., Remember the selected topic as the default for the active project., Return the selected topic slug, or None for the blank option., Enable topic viewing only when the selector has a real topic., Keep a task visible after user activity during this launch., Prefer mounted selector values so clarification refreshes keep choices. (+1 more)

### Community 22 - "._set_status"
Cohesion: 0.14
Nodes (10): Provider-specific subprocess execution with normalized agent messages., Track an inactivity deadline that agent stdout can refresh., _TimeoutTracker, cursor_environment(), Path, Small, dependency-free environment-file loading for local CLI providers., Return the process environment plus local Cursor credentials.      Explicit proc, read_env_file() (+2 more)

### Community 23 - "update_repository"
Cohesion: 0.15
Nodes (21): build_symbol_contexts(), candidate_feature_id(), _doc_for_definition(), extract_docs_for_symbols(), invert_edges(), _leading_comments(), _module_path_candidates(), _percentile() (+13 more)

### Community 24 - "Daedalus TUI Coding Statistics"
Cohesion: 0.29
Nodes (6): Daedalus TUI Coding Statistics, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 25 - "._set_status"
Cohesion: 0.17
Nodes (4): Key, Return a TextArea selection or the active screen selection., Use Textual's OSC 52 path and a native clipboard fallback., Add Vim-like navigation without changing TextArea insert behavior.

### Community 26 - ".provider_split"
Cohesion: 0.07
Nodes (25): ComposeResult, Pressed, ProgressCallback, Select, Submitted, ProjectInitializerTests, CreateTopicScreen, ProjectInitializerScreen (+17 more)

### Community 27 - ".on_mount"
Cohesion: 0.16
Nodes (16): CallGraphTreeTests, format_descriptor(), _format_name_list(), group_candidate_features(), Any, Format a stable descriptor using terminal names for graph peers., Group symbols connected by inclusive-threshold relations.      Parent/child dire, Score every unique parent→child edge and capped sibling pairs. (+8 more)

### Community 28 - "log_exception"
Cohesion: 0.29
Nodes (6): Daedalus TUI Topics, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 29 - "CodingStatisticsScreen"
Cohesion: 0.12
Nodes (6): FakeCoordinator, FakeRunner, settings(), ModelOption, DaedalusProject, A repository recognized by the presence of a ``feature_files`` folder.

### Community 30 - "calculate_token_usage"
Cohesion: 0.05
Nodes (33): TaskMemoryStoreTests, TokenUsageTests, Path, Remove one project's operating-branch override (absent = use default)., Return the remembered default topic for a project, if any., Remember one project's default topic without losing other entries., Remove one project's topic override (absent = no default topic)., Return persisted task snapshots keyed by their stable task ID. (+25 more)

### Community 31 - "PlanAnswerSelect"
Cohesion: 0.29
Nodes (6): Daedalus TUI Project Initialization, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 32 - "discover_projects"
Cohesion: 0.25
Nodes (7): 4-Stage Development Lifecycle, Alignment, Debugging, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization, Topics (when tagged)

### Community 33 - ".on_button_pressed"
Cohesion: 0.06
Nodes (45): ConfigTests, PlanTests, CodingStatisticsScreen, _format_count(), _format_tokens(), Textual interface for concurrent local agent tasks., Resolve a Select value that is legal for the current question options., Show token or task usage history and derived coding statistics. (+37 more)

### Community 34 - "._render_line_strip"
Cohesion: 0.25
Nodes (7): 4-Stage Development Lifecycle, Alignment, Debugging, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization, Topics (when tagged)

### Community 35 - "agent_runner.py"
Cohesion: 0.17
Nodes (3): Path, _sample_files(), VariableLineageTests

### Community 36 - "architecture.md"
Cohesion: 0.33
Nodes (5): 4-Stage Development Lifecycle, Evidence Extraction, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization

### Community 37 - "integrating.md"
Cohesion: 0.40
Nodes (4): 4-Stage Development Lifecycle, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization

### Community 38 - "._set_status"
Cohesion: 0.13
Nodes (11): Refresh Branch Select options for the active project and sync coordinator., Enable Push only when an origin remote and operating branch are available., Push the Branch Select value for the active project to origin., Cover terminal and event-loop exits that bypass Textual unmount., configure_debug_logging(), install_fault_handler(), _install_thread_exception_logging(), Path (+3 more)

### Community 39 - "Daedalus Project Instructions"
Cohesion: 0.40
Nodes (4): Daedalus Project Instructions, graphify, Task mode, Topics

### Community 41 - "KeyboardShortcutsScreen"
Cohesion: 0.14
Nodes (12): EventCallback, IntegrationGate, AgentControl, Cooperative stop signals shared by a task and its active subprocess., AgentStopped, OrchestrationResult, Path, RuntimeError (+4 more)

### Community 42 - "debug_log.py"
Cohesion: 0.22
Nodes (7): Strip, Style, Text, _literal_select_options(), Build Select prompts that Rich will not parse as markup., Render a line with the final-message color before selection styling., Render the native cursor without a background in visible modes.

### Community 43 - "._rebuild_plan_questions"
Cohesion: 0.15
Nodes (10): parent_child_score_map(), build_tree(), datetime, Build a call tree from *root* with cycle and depth limits., Render candidate features independently from the similarity panel., Render a self-contained HTML page for the call trees., _render_candidate_features_panel(), render_html() (+2 more)

### Community 44 - "task_coordinator.py"
Cohesion: 0.07
Nodes (27): TaskEventCallback, FakeOrchestrator, TaskCoordinatorTests, OrchestrationSettings, IntegrationCoordinator, _nonnegative_int(), _phase_for_status(), Path (+19 more)

### Community 45 - "KeyboardShortcutsScreen"
Cohesion: 0.20
Nodes (9): Constraints and Design Principles, Desired End State, Intended Import Workflow, Open Questions, Project Imports to the Daedalus Format, Scope and Durable Context, State Log, Topic Goal (+1 more)

### Community 46 - "._handle_visual_line_mode"
Cohesion: 0.14
Nodes (8): Key, Keep Enter as a newline; Ctrl+Enter remains the app submit key., Route visual-line mode and mirror new yanks to the host clipboard., Add Daedalus prompt commands that the dependency does not provide., Select the current line and enter Vim visual-line mode., Select every character in the lines between the start and cursor., Handle movement and operators while whole lines are selected., Expose operator-pending so the caret can become an underline.

### Community 47 - "._start_new_task"
Cohesion: 0.07
Nodes (17): AbstractEventLoop, BaseException, Exception, Promote only events that need the user's attention in the inbox., Finish Select setup without allowing a stale value to exit the TUI.          Pla, Pause active agents before ThreadPoolExecutor joins its workers.      CPython ex, Stop agents before an explicit Textual exit begins., Persist Textual failures that would otherwise only flash on screen. (+9 more)

### Community 48 - "discover_projects"
Cohesion: 0.29
Nodes (5): ProjectDiscoveryTests, discover_projects(), Path, Discovery of Daedalus-supported repositories beneath a launch root., Find immediate child folders containing a direct ``feature_files`` child.      G

### Community 49 - "._render_line_strip"
Cohesion: 0.23
Nodes (7): SupabaseMigrationsTests, migrations_pending(), push_migrations(), Path, Orchestration-owned Supabase migration push for target project worktrees., Return True when the worktree differs from base under supabase/migrations/., Run non-interactive `supabase db push --yes` in the target worktree.

### Community 50 - ".test_plan_review_renders_literal_markup_like_agent_text"
Cohesion: 0.09
Nodes (5): Agent plan text must not be parsed as Textual/Rich markup., Follow-up questions must not crash when old option ids linger on widgets., Deferred Select init must not fatal-exit on a leftover option id., Clearing questions after confirmation must keep the TUI alive., PlanOption

### Community 51 - "CreateTopicScreen"
Cohesion: 0.25
Nodes (9): VerificationTests, Single-run local agent orchestration without daemon or database dependencies., discover_commands(), format_process_result(), package_has_test_script(), CompletedProcess, Path, Local verification discovery and execution. (+1 more)

### Community 52 - "Daedalus TUI Call Graph Visualization"
Cohesion: 0.29
Nodes (6): Daedalus TUI Call Graph Visualization, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 53 - "b.py"
Cohesion: 0.10
Nodes (21): alpha(), Entry helper that fans out into order and UI branches., beta(), Continue the sample call chain toward gamma., gamma(), Leaf helper in the sample call chain., make_runner(), create_order() (+13 more)

### Community 54 - "update_repository"
Cohesion: 0.29
Nodes (5): GraphifyTests, Path, Best-effort graph refresh owned by the local orchestration layer., Refresh the primary repository graph without affecting task success., update_repository()

### Community 55 - "conftest.py"
Cohesion: 0.50
Nodes (3): pytest_configure(), Pytest hooks shared across the test suite., Install pyan3 when call-graph tests run in an environment missing it.

### Community 57 - "DescriptorEmbedder"
Cohesion: 0.25
Nodes (5): _descriptor_hash(), DescriptorEmbedder, Lowercase and split identifiers on `.` / `_` while keeping word tokens., Fit TF-IDF over symbol descriptors and score cosine similarity., tokenize_descriptor()

### Community 59 - "render_call_graph_tree"
Cohesion: 0.27
Nodes (9): load_config(), main(), Path, Unit tests for AST variable-lineage analysis., CallGraphConfig, Analyze the project at *project_root* and write the HTML call tree., render_call_graph_tree(), VariableLineageResult (+1 more)

### Community 60 - "trading.py"
Cohesion: 0.32
Nodes (5): calculate(), execute_trade(), Portfolio, Assignment lineage, augassign, attribute mutate, and unique call mapping., run_pipeline()

### Community 62 - "ambiguous_a.py"
Cohesion: 0.67
Nodes (3): helper(), Ambiguous same-named callees should not emit PASSED_TO edges., run_local()

### Community 63 - "ambiguous_b.py"
Cohesion: 0.67
Nodes (3): helper(), Second helper with the same simple name as ambiguous_a.helper., run_other()

### Community 66 - "._render_line_strip"
Cohesion: 0.14
Nodes (12): Mount, KeyboardShortcutsScreen, PlanAnswerSelect, PlanClarificationScreen, Initialize dynamic plan selectors after their nested children mount., Collect a clarification about one plan question., Modal reference for the app and prompt editor keyboard shortcuts., Display a topic markdown file without allowing edits. (+4 more)

### Community 71 - "_collapse_inner_safe"
Cohesion: 0.15
Nodes (12): CallGraphVisitor, _collapse_inner_safe(), _collect_node_names(), discover_source_files(), extract_uses_edges(), Any, Path, Run pyan's collapse_inner while skipping anonymous nodes pyan cannot parent-reso (+4 more)

## Knowledge Gaps
- **101 isolated node(s):** `daedalus-tui`, `Execution Boundaries (CRITICAL)`, `Evidence Extraction`, `Architecture Boundaries`, `Parameter Files` (+96 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DaedalusTuiApp` connect `._shutdown_coordinators` to `DaedalusVimTextArea`, `._render_line_strip`, `.on_button_pressed`, `AgentRunner`, `._set_status`, `GitWorktreeManager`, `Key`, `task_coordinator.py`, `._start_new_task`, `.test_plan_review_renders_literal_markup_like_agent_text`, `CodingStatisticsScreen`, `TaskRecord`, `._set_status`, `._set_status`, `CodingStatisticsScreen`, `calculate_token_usage`?**
  _High betweenness centrality (0.112) - this node is a cross-community bridge._
- **Why does `AgentRunner` connect `AgentRunner` to `.on_button_pressed`, `._render_line_strip`, `app.py`, `KeyboardShortcutsScreen`, `task_coordinator.py`, `CreateTopicScreen`, `TaskRecord`, `._shutdown_coordinators`, `._set_status`, `.provider_split`?**
  _High betweenness centrality (0.071) - this node is a cross-community bridge._
- **Why does `TuiAppTests` connect `DaedalusVimTextArea` to `.on_button_pressed`, `._render_line_strip`, `Key`, `task_coordinator.py`, `.test_plan_review_renders_literal_markup_like_agent_text`, `._shutdown_coordinators`, `CodingStatisticsScreen`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `DaedalusTuiApp` (e.g. with `FakeCoordinator` and `FakeRunner`) actually correct?**
  _`DaedalusTuiApp` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `TuiAppTests` (e.g. with `CodingStatisticsScreen` and `DaedalusTuiApp`) actually correct?**
  _`TuiAppTests` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 21 inferred relationships involving `TaskCoordinator` (e.g. with `FakeOrchestrator` and `TaskCoordinatorTests`) actually correct?**
  _`TaskCoordinator` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `OrchestrationSettings` (e.g. with `OrchestratorTests` and `FakeOrchestrator`) actually correct?**
  _`OrchestrationSettings` has 16 INFERRED edges - model-reasoned connections that need verification._