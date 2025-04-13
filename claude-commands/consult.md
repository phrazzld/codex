# CONSULT
## 1. FORMULATE CONSULTATION REQUEST FOR CURRENT TASK
- **Goal:** Clearly articulate the problem or need for guidance on the current task you're struggling with.
- **Actions:**
    - **Current Task Focus:** This command addresses the task you are actively working on and having difficulties with. Do not select a new task.
    - Create a new file named `CONSULT-REQUEST.md`.
    - ***Think hard*** and populate this file with:
        - **`Goal:`** Original objective (Reference task/plan).
        - **`Problem/Blocker:`** Specific issue. Relate it to our standards documents if applicable:
          - **Design issues:** Explain how it violates principles in `CORE_PRINCIPLES.md` (e.g., "Creates unnecessary complexity," "Violates modularity")
          - **Architecture issues:** Describe conflicts with `ARCHITECTURE_GUIDELINES.md` (e.g., "Mixes concerns," "Creates circular dependencies")
          - **Code quality issues:** Note violations of `CODING_STANDARDS.md` (e.g., "Uses unsafe type assertions," "Creates mutable shared state")
          - **Testing issues:** Explain conflicts with `TESTING_STRATEGY.md` (e.g., "Requires extensive mocking of internal components," "Cannot test behavior without fragile implementation coupling")
          - **Documentation issues:** Indicate problems related to `DOCUMENTATION_APPROACH.md` (e.g., "Cannot document rationale clearly," "Creates unintuitive interfaces")
        - **`Context/History:`** Steps taken, attempts made (Reference `*-PLAN.md`, `BUGFIXPLAN.md`, etc.).
        - **`Key Files/Code Sections:`** Specific code areas involved.
        - **`Error Messages (if any):`** Relevant output.
        - **`Desired Outcome:`** What would success look like? (e.g., "A simpler testing strategy," "A refactoring suggestion to improve testability," "A way to achieve goal X without violating Y").

## 2. Identify Context Files/Directories
- **Goal:** Determine necessary project context for `architect`.
- **Actions:
    - Review `CONSULT-REQUEST.md` and identify mentioned files/directories.
    - Include relevant code paths, potentially parent directories.
    - **Include all relevant standards documents:**
      - Always include `CORE_PRINCIPLES.md` as foundational guidance
      - Include `ARCHITECTURE_GUIDELINES.md` for structural questions
      - Include `CODING_STANDARDS.md` for implementation-specific issues
      - Include `TESTING_STRATEGY.md` for testing-related concerns
      - Include `DOCUMENTATION_APPROACH.md` for documentation questions
    - ***Think carefully*** to select sufficient context. Create a list of paths.

## 3. Invoke Architect CLI
- **Goal:** Request assistance via `architect`.
- **Actions:**
    - **Construct Command:**
        ```bash
        architect --instructions CONSULT-REQUEST.md --output-dir architect_output --model gemini-2.5-pro-preview-03-25 --model gemini-2.5-pro-exp-03-25 --model gemini-2.0-flash docs/philosophy/ <specific-context-files>
        ```
        - **Review and Synthesize:**
            1. Review all files in the architect_output directory
            2. ***Think hard*** about the different model outputs and create a single synthesized file that combines the best elements and insights from all outputs: `CONSULTANT-PLAN.md`
        (Replace specific-context-files with relevant code paths from Step 2).
    - **Execute Command:** Run it.
    - **Handle Errors:** Report errors. Write any errors you encounter to a persistent log file. Attempt **one** retry if fixable, report failure and stop if unresolvable.
    - **Identify Output Directory:** Report success and output path.

## 4. Review Architect's Response
- **Goal:** Understand and review the implementation plan from architect.
- **Actions:**
    - Read the architect-generated plan in `CONSULTANT-PLAN.md`.
    - **Verify Standards Alignment:** Confirm the plan aligns with our complete standards framework:
      - Promotes simplicity and minimizes complexity (`CORE_PRINCIPLES.md`)
      - Maintains strong separation of concerns (`ARCHITECTURE_GUIDELINES.md`)
      - Follows established coding conventions (`CODING_STANDARDS.md`)
      - Enables straightforward testing with minimal mocking (`TESTING_STRATEGY.md`)
      - Supports clear documentation of rationale (`DOCUMENTATION_APPROACH.md`)

## 5. Execute Plan
- **Goal:** Execute the plan to resolve the original issue.
- **Actions:**
    - **Execute Plan:** Treat `CONSULTANT-PLAN.md` as the primary plan for this issue. Use standard `EXECUTE.MD` process for tasks within it if structured similarly. This supersedes previous plans *for this issue*.
    - Continue until resolved or plan completed.
    - **Update Task Status:** If the task is resolved, change the task status in `TODO.MD` from `[~]` (in progress) to `[x]` (complete).
    - Remove `CONSULT-REQUEST.md` and `CONSULTANT-PLAN.md`
