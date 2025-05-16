# EXECUTE

**OBJECTIVE:** Systematically acquire, classify, plan, execute, and commit the next unblocked ticket from `TODO.md`. Minimize overhead; maximize adherence to standards.

## 1. Acquire Next Unblocked Ticket
    a. Scan `TODO.md` sequentially from top to bottom.
    b. Select the FIRST `[ ]` (unstarted) ticket for which ALL `depends-on:` tasks are marked `[x]` (completed), or for which no dependencies exist.
    c. If no such ticket exists, halt.
    d. Update the selected ticket's status to `[~]` (in progress).
    e. Record the ticket's **ID** and **Title** for use in subsequent steps.

## 2. Analyze & Classify Task
    a. **Think & Evaluate:** Carefully review the ticket's requirements, acceptance criteria, and any associated context. Consider potential complexities, scope, and required design decisions.
    b. **Classification Criteria:**
        * **`Simple`**: Likely a single-file change, involves straightforward logic, requires no significant design decisions, and has low risk.
        * **`Complex`**: Likely involves multi-file changes, intricate logic, requires design decisions, carries non-trivial risk, or presents any ambiguity.
    c. **Classify:** Based on your evaluation, designate the task as `Simple` or `Complex`.

## 3. Consult Guiding Principles
    a. Before planning or implementation, identify and thoroughly review ALL sections of `DEVELOPMENT_PHILOSOPHY.md` and any language-specific appendices (e.g., `_GO.md`, `_TYPESCRIPT.md`) that are pertinent to the current task.
    b. Ensure these principles are actively considered throughout the planning and execution phases.

## 4. Process: `Simple` Task Protocol
    a. **Plan:**
        i. Create a new file named `<task-id>-plan.md`.
        ii. Briefly document your intended implementation approach, focusing on clarity and adherence to the principles identified in Step 3.
    b. **Implement:** Write code to fulfill the ticket requirements, strictly adhering to `DEVELOPMENT_PHILOSOPHY.md` and your plan.
    c. **Validate:**
        i. Run the code formatter.
        ii. Run the linter.
        iii. Execute all relevant tests (unit, integration).
        iv. Resolve ALL errors and warnings reported by these tools. Code MUST be clean.
    d. **Finalize:**
        i. Update the ticket's status to `[x]` in `TODO.md`.
        ii. Commit changes using a compliant **Conventional Commits** message. The commit MUST pass all pre-commit hooks.
        iii. Push the commit.
        iv. Delete `<task-id>-plan.md`.

## 5. Process: `Complex` Task Protocol
    a. **Prepare for Advanced Analysis:**
        i. Create a new file named `<task-id>-task.md`.
        ii. Populate this file with the following sections:
            1.  **Task ID:** (from Step 1.e)
            2.  **Title:** (from Step 1.e)
            3.  **Original Ticket Text:** (verbatim copy)
            4.  **Implementation Approach Analysis Prompt:** (full content of the standard prompt, typically found in a separate template file)
    b. **Generate & Refine Plan (via `thinktank-wrapper`):**
        i. **Context Preparation:**
            * Sanitize the **Task Title** (from Step 1.e) to create a valid filename component (e.g., `sanitized-task-title`). The input file for `thinktank-wrapper` will be `<sanitized-task-title>-TASK.md` (which is the file created in 5.a.i, ensuring its name aligns if different from `<task-id>-task.md` or using task ID as primary). *Ensure filename consistency.* Let's assume `<task-id>-task.md` is the correct name for injection.
            * Identify up to ten additional relevant files from the codebase (e.g., related modules, data structure definitions, key `glance.md` files) that provide essential context for the `thinktank-wrapper`.
        ii. **Execute Analysis (maximize the timeout of your Bash tool when you invoke thinktank-wrapper):**
            ```bash
            thinktank-wrapper --template execute --inject <task-id>-task.md --model-set all --include-philosophy --include-glance [COMMA_SEPARATED_LIST_OF_UP_TO_10_RELEVANT_FILES]
            ```
        iii. **Synthesize Plan:** Critically review all files in the `thinktank-wrapper` output directory. Use the synthesis file and other generated artifacts to create a comprehensive, actionable plan in a new file named `<task-id>-plan.md`.
    c. **Develop (Test-First Methodology):**
        i.  **Write Tests:** Before writing implementation code, develop a comprehensive suite of failing tests. These tests MUST cover the primary success path (happy path) and all critical edge cases and foreseeable failure modes.
        ii. **Mocking Strategy:** Mock **only** true external dependencies (e.g., network services, databases, system I/O not under direct control). Internal collaborators or modules within the project MUST NOT be mocked; refactor for testability if needed.
        iii. **Implement Code:** Write the minimum amount of clean, maintainable code necessary to make all tests pass. Continuously ensure adherence to `DEVELOPMENT_PHILOSOPHY.md` and the agreed plan in `<task-id>-plan.md`.
        iv. **Refactor:** With all tests passing, refactor the new code and related existing code. Focus on improving clarity (names, structure), reducing complexity, eliminating redundancy, and ensuring adherence to design principles. All tests MUST remain green throughout refactoring.
    d. **Validate Rigorously:**
        i. Execute the full test suite.
        ii. Run the code formatter.
        iii. Run the linter.
        iv. Perform a full project build (if applicable).
        v. Confirm ALL checks pass without any errors or warnings.
    e. **Finalize:**
        i. Update the ticket's status to `[x]` in `TODO.md`.
        ii. Commit changes using a compliant **Conventional Commits** message. The commit MUST pass all pre-commit hooks.
        iii. Push the commit(s).
        iv. Delete `<task-id>-task.md` and `<task-id>-plan.md`.

## 6. Universal Execution Mandates
    a. **Acyclic Dependencies:** All code changes MUST maintain an acyclic project dependency graph.
    b. **CI Integrity:** Every commit pushed to the remote repository MUST successfully pass all stages of the Continuous Integration (CI) pipeline. Pushing known failing commits or bypassing CI checks is FORBIDDEN.
    c. **Philosophy Adherence:** All development activity MUST conform to `DEVELOPMENT_PHILOSOPHY.md` and its relevant appendices.
