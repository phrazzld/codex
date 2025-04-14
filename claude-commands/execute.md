# EXECUTE

## 1. SELECT AND ASSESS TASK

- **Goal:** Choose and assess the next appropriate task from `TODO.MD`.
- **Actions:**
    - Scan `TODO.MD` for tasks marked `[ ]` (incomplete). Select the first task whose prerequisites (`Depends On:`) are already marked `[x]` (complete) or are 'None'.
    - Record the exact Task Title.
    - Mark the task as in-progress by changing `[ ]` to `[~]` in `TODO.MD`.
    - **Assess Complexity:** Analyze the task requirements, determining if it's:
        - **Simple:** Small change, single file, clear requirements, no architecture changes
        - **Complex:** Multiple files, complex logic, architectural considerations, or any uncertainty
    - **Route Accordingly:**
        - For **Simple** tasks, follow Section 2 (Fast Track)
        - For **Complex** tasks, follow Section 3 (Comprehensive Track)

## 2. FAST TRACK (SIMPLE TASKS)

### 2.1. CREATE MINIMAL PLAN

- **Goal:** Document a straightforward implementation approach.
- **Actions:**
    - **Analyze:** Review the task details from `TODO.MD`.
    - **Document:** Create `<sanitized-task-title>-PLAN.md` with:
        - Task title
        - Brief implementation approach (1-2 sentences)

### 2.2. WRITE MINIMAL TESTS (IF APPLICABLE)

- **Goal:** Define happy path tests only.
- **Actions:**
    - Write minimal tests for the core happy path
    - Skip if task isn't directly testable

### 2.3. IMPLEMENT FUNCTIONALITY

- **Goal:** Write clean, simple code to satisfy requirements.
- **Actions:**
    - Consult project standards documents as needed
    - Implement the functionality directly

### 2.4. FINALIZE & COMMIT

- **Goal:** Ensure work passes checks and is recorded.
- **Actions:**
    - Run checks (linting, tests) and fix any issues
    - Update task status in `TODO.MD` to `[x]` (complete)
    - Commit with conventional commit format

## 3. COMPREHENSIVE TRACK (COMPLEX TASKS)

### 3.1. PREPARE TASK PROMPT

- **Goal:** Create a detailed prompt for implementation planning.
- **Actions:**
    - **Filename:** Sanitize Task Title -> `<sanitized-task-title>-TASK.md`.
    - **Analyze:** Re-read task details (Action, AC Ref, Depends On) from `TODO.MD` and the relevant section in `PLAN.MD`.
    - **Retrieve Base Prompt:** Copy the content from `prompts/execute.md` to use as the base for your task prompt.
    - **Customize Prompt:** Create `<sanitized-task-title>-TASK.md` by adding task-specific details to the base prompt:
        - Add task title, description, and acceptance criteria at the top.
        - Keep all the original instructions from the base prompt.
        - Ensure the prompt maintains the focus on standards alignment.

### 3.2. GENERATE IMPLEMENTATION PLAN WITH ARCHITECT

- **Goal:** Use `architect` to generate an implementation plan based on the task prompt and project context.
- **Actions:**
    - **Find Task Context:**
        1. Find the top ten most relevant files for task-specific context
    - **Run Architect:**
        1. Run `architect --instructions <sanitized-task-title>-TASK.md --output-dir architect_output --model gemini-2.5-pro-exp-03-25 --model gemini-2.0-flash docs/DEVELOPMENT_PHILOSOPHY.md [top-ten-relevant-files]`
        2. After architect finishes, review all files in the architect_output directory (typically gemini-2.5-pro-exp-03-25.md and gemini-2.0-flash.md).
        3. ***Think hard*** about the different model outputs and create a single synthesized file that combines the best elements and insights from all outputs: `<sanitized-task-title>-PLAN.md`
    - If you encounter an error, write it to a persistent logfile and try again.
    - Report success/failure. Stop on unresolvable errors.
    - **Review Plan:** Verify the implementation plan aligns with our standards hierarchy:
        1. Simplicity and clarity over cleverness (`CORE_PRINCIPLES.md`)
        2. Clean separation of concerns (`ARCHITECTURE_GUIDELINES.md`)
        3. Straightforward testability with minimal mocking (`TESTING_STRATEGY.md`)
        4. Adherence to coding conventions (`CODING_STANDARDS.md`)
        5. Support for clear documentation (`DOCUMENTATION_APPROACH.md`)
    - Remove `<sanitized-task-title>-TASK.md`.

### 3.3. WRITE FAILING TESTS

- **Goal:** Define expected behavior via tests, adhering strictly to the testing philosophy.
- **Actions:**
    - **Consult All Standards:** Review task requirements (`AC Ref:`, `<sanitized-task-title>-PLAN.md`) and adhere to all standards, with particular focus on testing:
        - Ensure tests reflect the simplicity principle (`CORE_PRINCIPLES.md`)
        - Test through public interfaces as defined in the architecture (`ARCHITECTURE_GUIDELINES.md`)
        - Follow coding standards in test code too (`CODING_STANDARDS.md`)
        - **Strictly adhere to testing principles, avoiding mocks of internal components** (`TESTING_STRATEGY.md`)
        - Document test rationale where needed (`DOCUMENTATION_APPROACH.md`)
    - **Write Happy Path Tests:** Write the minimum tests needed to verify the core *behavior* for the happy path, focusing on the public interface. **Prioritize tests that avoid mocking internal components.**
    - **Write Critical Edge Case Tests:** Add tests for important error conditions or edge cases identified.
    - **Verify Test Simplicity:** ***Think hard*** - "Are these tests simple? Do they avoid complex setup? Do they rely on mocking internal code? If yes, reconsider the test approach itself."
    - Ensure tests currently fail (as appropriate for TDD/BDD style).
- **Guidance:** Test *behavior*, not implementation. **Aggressively avoid unnecessary mocks.** If mocking seems unavoidable for internal logic, it's a signal to improve the design.

### 3.4. IMPLEMENT FUNCTIONALITY

- **Goal:** Write the minimal code needed to make tests pass (green).
- **Actions:**
    - **Consult Standards:** Review `CONTRIBUTING.MD`, `CODING_STANDARDS.md`, `ARCHITECTURE_GUIDELINES.md`, etc.
    - **Write Code:** Implement the functionality based on `<sanitized-task-title>-PLAN.md` that satisfies the failing tests.
    - **Focus on Passing Tests:** Initially implement just enough code to make tests pass, deferring optimization.
    - **Adhere Strictly:** Follow project standards and the chosen plan.
- **Guidance:** Focus on making tests pass first, then improve the implementation in the refactoring phase.

### 3.5. REFACTOR FOR STANDARDS COMPLIANCE

- **Goal:** Improve code quality while maintaining passing tests.
- **Actions:**
    - **Review Code:** Analyze the code files just implemented to ensure they pass tests.
    - **Assess Standards Compliance:** ***Think hard*** and evaluate against all standards:
        - **Core Principles:** "Does this implementation embrace simplicity? Does it have clear responsibilities? Is it explicit rather than implicit?" (`CORE_PRINCIPLES.md`)
        - **Architecture:** "Is there clean separation between core logic and infrastructure? Are dependencies pointing inward?" (`ARCHITECTURE_GUIDELINES.md`)
        - **Code Quality:** "Does it follow our coding conventions? Does it leverage types effectively? Does it prefer immutability?" (`CODING_STANDARDS.md`)
        - **Testability:** "Can this code be tested simply? Does it require complex setup or extensive mocking of internal components?" (`TESTING_STRATEGY.md`)
        - **Documentation:** "Are design decisions clear? Would comments explain the 'why' not just the 'what'?" (`DOCUMENTATION_APPROACH.md`)
    - **Identify Refactors:** If any standard is not met, identify the **minimal necessary refactoring** to address the issues:
        - For simplicity issues: Extract responsibilities, reduce complexity
        - For architectural issues: Improve separation of concerns, realign dependencies
        - For code quality issues: Apply coding conventions, use types more effectively
        - For testability issues: Reduce coupling, extract pure functions, improve interfaces
        - For documentation issues: Clarify design decisions with appropriate comments
    - **Perform Refactor:** Apply the identified refactoring changes while ensuring tests continue to pass.

### 3.6. VERIFY ALL TESTS PASS

- **Goal:** Ensure all tests pass with the refactored implementation.
- **Actions:**
    - Run the code and all tests.
    - Verify that all tests pass, including the original failing tests and any additional tests added.
    - If any tests fail after refactoring, fix the implementation while maintaining standards compliance.
    - **Do NOT modify tests to make them pass unless the test itself was fundamentally flawed.**

### 3.7. FINALIZE & COMMIT

- **Goal:** Ensure work is complete, passes all checks, and is recorded.
- **Actions:**
    - **Run Checks & Fix:** Execute linting, building, and the **full test suite**. Fix *any* code issues causing failures.
    - **Update Task Status:** Change the task status in `TODO.MD` from `[~]` (in progress) to `[x]` (complete).
    - **Remove Task-Specific Reference Files:** Delete <sanitized-task-title>-PLAN.md
    - **Add, Commit, and Push Changes**
