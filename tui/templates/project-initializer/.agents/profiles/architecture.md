# Execution Boundaries (CRITICAL)
- NEVER EXECUTE SOURCE CODE (python, bash, node, script tasks) without explicit standalone user permission in the current turn. **Scrapers, tests, skill plugins (e.g. graphify), research and directory listing are permitted.**
- NEVER implement CLI/Command Line Arguments (`--input`, `--mode`). Hardcode configurations directly into variables for manual tweaking.

# Evidence Extraction
- You can use variations of `git diff` in order to obtain the relevant file changes
- Use graphify and the feature file system in order to obtain semantic and relational understanding of features and objects in code

# Feature File Automation
- Feature files are used to track feature context (important bugs fixed, design philosophies, etc.)
- Feature files and graphify are designed to co-exist; graphify describes *where* things exist and feature files should describe *why* things exist
- Feature files define a feature's ownership boundary. A feature owns only the logic, configuration, and behavior it directly implements.
    - Files, scripts, modules, or features that are merely called, launched, imported, orchestrated, or referenced are dependencies, not part of the feature itself.
    - Do not absorb dependency-specific details into a feature file simply because the feature interacts with them.
    - Cross-feature references should describe the interface or relationship, not duplicate the dependency's internal configuration.

- *Don't update the feature files in architecture mode, they are read-only to you*

# Parameter File Centralization
Parameter files are used to centralize feature-level configuration values that may need to be tuned, experimented with, or adjusted without modifying source code. Features should load these values from their parameter file rather than defining them directly in the implementation.

Parameter files act as a read-only source of truth during execution. Source code may read and use parameter values, but must not modify parameter files or persist runtime state back to them.

A parameter belongs in the parameter file of the feature that owns the behavior being configured, not necessarily the feature that references, imports, starts, or coordinates that behavior.

*Similar to feature files, do not edit these*

# 4-Stage Development Lifecycle
There are 4 stages we adhere to in development:

1. HACKING: Prototype phase. Omit error-handling, validation boundaries, typing setups, and algorithmic optimization. Maximize readability; write logic a high school CS student can completely parse line-by-line.
2. TESTING: Incremental hardening. Introduce structured unit tests, catch-blocks, and condition validations.
3. PRODUCTION-READY: Enterprise optimization. Implement full validation layers, robust documentation strings, edge-case coverage, and clean structural syntax (dataclasses, slots, performance optimizations).
4. DEBUGGING: Deep diagnostics. Strip defensive abstractions. Maximize structured event logging, granular print statements, and cross-feature execution tracking.
