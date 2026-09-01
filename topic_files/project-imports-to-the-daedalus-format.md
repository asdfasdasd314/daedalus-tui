# Project Imports to the Daedalus Format

## Topic Goal
I want Daedalus to be able to interface with projects that weren't initialized at the start with Daedalus. There are two parts to this: initializing all of the infrastructure and then creating all of the feature and parameter files. Technically speaking there would be no parameter files in a project that doesn't use the daedalus format, so we do not need to initialize parameter files. This is something i use for my personal projects. Initializing the feature files is the hard part, and to do that we need to track the call graph in order to identify potential features and have ai agents pass over the results to verify the feature files generated are valid. The end result should be being able to take a program of arbitrary complexity and convert it to the Daedalus format with all of the necessary semantic information put into the feature files to allow an agent to start interacting with the codebase as if the feature files were always there (in reality the state log can realistically not be replicated, but that's probably not the most important and in the future could be replicated from git commits or something)

## Topic Status
open

## Scope and Durable Context
- The import flow targets an existing project that was not initialized with Daedalus and must leave that project independently usable in the Daedalus workflow.
- Infrastructure initialization and semantic feature-file generation are separate concerns. The first establishes the Daedalus structure; the second reconstructs the project context needed by agents.
- A non-Daedalus source project is not expected to contain parameter files. Importing it should therefore not invent parameter files unless a later design identifies a genuine tunable configuration owned by a feature.
- Feature files are the durable semantic layer: they should explain why code exists, identify the behavior a feature owns, and point to relevant implementation files without duplicating dependency internals.
- The historical state log is not expected to be reconstructed perfectly. Reconstructing useful current context is more important initially; deriving history from Git commits can remain a future extension.

## Intended Import Workflow
1. Inspect the target project and initialize the Daedalus infrastructure that is appropriate for an existing repository.
2. Analyze the project call graph and related structural information to identify candidate features, boundaries, dependencies, and entry points.
3. Have AI agents generate feature files from that evidence, with explicit uncertainty where the analysis cannot establish intent.
4. Run an independent verification pass over the generated feature files for coverage, ownership, references, consistency, and validity.
5. Present or persist the verified feature context so a Daedalus agent can begin working with the project as though the feature files had existed from project initialization.

## Constraints and Design Principles
- The process should accommodate projects of arbitrary complexity, including incomplete, multi-language, or dynamically connected call graphs where analysis is necessarily partial.
- Static call-graph results are evidence, not a complete statement of product intent. Generation and verification must preserve that distinction.
- Candidate features should be organized around cohesive behavior and ownership rather than one feature per file, function, or call-graph node.
- Imported context must distinguish direct implementation files from dependencies that are merely called, launched, imported, orchestrated, or referenced.
- Verification should detect missing coverage, duplicated ownership, unsupported assumptions, stale paths, malformed feature-file structure, and cross-feature descriptions that accidentally duplicate dependency details.
- Import tooling must not overwrite unrelated project files or fabricate historical state. Any destructive or ambiguous operation should require an explicit decision in the eventual workflow.

## Desired End State
- A user can point Daedalus at an arbitrary existing project and initialize the required infrastructure without needing to retrofit the project manually.
- The resulting feature files contain sufficient, verified semantic information for an agent to discover capabilities, understand ownership and dependencies, and safely begin interacting with the codebase.
- The import process reports analysis gaps and verification findings instead of presenting uncertain generated context as authoritative.
- The design leaves room for later improvements, including richer language-aware call-graph analysis and reconstructing portions of state history from Git commits.

## Open Questions
- Which infrastructure files and directories are mandatory for an imported project, and which should be omitted or generated lazily?
- Which call-graph and repository signals best identify feature boundaries across languages, frameworks, generated code, and dynamic dispatch?
- Should agents generate and verify feature files in one pipeline or through independently reviewable stages?
- What coverage and confidence criteria are sufficient to consider an import complete for a given project?
- How should users review, correct, and feed intent back into generated feature files when static evidence is ambiguous?

## State Log
- Topic initialized: existing non-Daedalus projects need infrastructure initialization plus call-graph-assisted, AI-verified feature-file generation; parameter files are not required by default, historical state need not be replicated initially, and the intended end state is an arbitrary-project import that provides reliable semantic context for Daedalus agents.
