# Claude Code Instructions - Core Project Guide

**IMPORTANT:** You MUST adhere to the principles and mandatory standards outlined in the full `DEVELOPMENT_PHILOSOPHY.md` document provided in context. This file is a concise reminder of key operational points for working within this repository.

If this is a Go or TypeScript project, also strictly adhere to the rules in the relevant `DEVELOPMENT_PHILOSOPHY_APPENDIX_GO.md` or `DEVELOPMENT_PHILOSOPHY_APPENDIX_TYPESCRIPT.md` file.

## Core Principles Reminder

* **Simplicity First:** Seek the simplest correct solution. Eliminate unnecessary complexity.
* **Modularity:** Build small, focused components with clear interfaces. Follow package-by-feature structure.
* **Design for Testability:** Non-negotiable. Structure code for easy automated testing. **NO mocking internal collaborators.** Difficulty testing REQUIRES refactoring the code under test first.
* **Maintainability:** Code for humans first. Clarity > Premature Optimization.
* **Explicit > Implicit:** Make dependencies, control flow, and contracts obvious.
* **Automate Everything:** Especially linting, formatting, testing, versioning via established project tooling.
* **Document *Why*, Not *How*:** Code should be self-documenting. Comments explain rationale.

## Mandatory Practices

* **Strict Configuration:** Use strictest settings for linters, formatters, and type checkers defined in project configuration files.
* **NEVER Suppress Errors/Warnings:** Fix the root cause. Directives to ignore linter/type errors are FORBIDDEN without explicit, reviewed justification and explanation.
* **NEVER Hardcode Secrets:** Use environment variables or designated secret managers.
* **NEVER Trust Input:** Validate all external input rigorously at system boundaries.
* **Conventional Commits:** All commit messages MUST follow the spec for automated versioning/changelogs.
* **Structured Logging:** Use the project's standard structured logging library to output JSON logs.
* **Context Propagation:** Ensure `correlation_id` (Trace/Request ID) is generated, propagated across boundaries, and included in ALL relevant logs.
* **Quality Gates:** All code MUST pass mandatory pre-commit hooks and all CI checks (lint, format, tests, coverage, security scan). Bypassing hooks (`--no-verify`) is FORBIDDEN.

## Workflow & Tools

* **Plan First:** For non-trivial tasks, outline a plan (e.g., using "think") before coding. Confirm the plan if needed.
* **Use Checklists:** For complex tasks (migrations, large refactors), use a Markdown checklist to track progress step-by-step and ensure thoroughness.
* **Testing:** Follow the Test-Driven Development (TDD) approach where applicable (Write Test -> Fail -> Code -> Pass). Focus on robust Integration/Workflow tests that verify component collaboration.
* **Git Interaction:** You are expected to handle `git` operations, including writing Conventional Commit messages, searching history, and preparing changes.
* **`architect` CLI Tool:**
    * **Purpose:** This is a specialized local tool for deeper analysis and planning, using different models for broader perspective.
    * **When to Use:** Use `architect` if you are **struggling with a problem for too long**, feel like you are **getting off track or going in circles**, or are **getting nowhere** with the current approach. It's useful before starting complex coding or when stuck.
    * **How to Use:**
        1.  Create a temporary file (e.g., `temp_instructions.txt`) with clear, specific instructions for the `architect` tool detailing the problem, context, and desired output (e.g., "Analyze requirements X and propose 3 implementation strategies for feature Y, considering trade-offs based on `DEVELOPMENT_PHILOSOPHY.md`.").
        2.  Run the command: `architect --instructions temp_instructions.txt <relevant_paths...>` (e.g., `architect --instructions temp_instructions.txt ./src/featureY ./docs/specX`).
        3.  Analyze the output plan(s) generated by `architect`.
        4.  Proceed with the chosen plan, use the insights to get unstuck, or refine instructions and rerun if needed.
    * *(API keys are pre-configured locally; you don't need to manage them).*

**REMINDER:** This file highlights key operational points. Always refer to `DEVELOPMENT_PHILOSOPHY.md` and the relevant language-specific appendix (`DEVELOPMENT_PHILOSOPHY_APPENDIX_*.md`) for the complete standards and detailed guidelines.
