# CONSULT
## 1. FORMULATE CONSULTATION REQUEST FOR CURRENT TASK
- **Goal:** Clearly articulate the problem or need for guidance on the current task you're struggling with.
- **Actions:**
    - **Current Task Focus:** This command addresses the task you are actively working on and having difficulties with. Do not select a new task.
    - Create a new file named `CONSULT-REQUEST.md`.
    - ***Think hard*** and populate this file with:
        - **`Goal:`** Original objective (Reference task/plan).
        - **`Problem/Blocker:`** Specific issue. Relate it to our `DEVELOPMENT_PHILOSOPHY.md` document where able.
        - **`Context/History:`** Steps taken, attempts made (Reference `*-PLAN.md`, `BUGFIXPLAN.md`, etc.).
        - **`Key Files/Code Sections:`** Specific code areas involved.
        - **`Error Messages (if any):`** Relevant output.
        - **`Desired Outcome:`** What would success look like? (e.g., "A simpler testing strategy," "A refactoring suggestion to improve testability," "A way to achieve goal X without violating Y").

## 2. Invoke Architect CLI
- **Goal:** Request assistance via `architect`.
- **Actions:**
    - **Construct Command:**
        ```bash
        architect --instructions CONSULT-REQUEST.md --output-dir architect_output --model gemini-2.5-pro-preview-03-25 --model gemini-2.5-pro-exp-03-25 --model gemini-2.0-flash docs/DEVELOPMENT_PHILOSOPHY.md ./
        ```
        - **Review and Synthesize:**
            1. Review all files in the architect_output directory
            2. ***Think hard*** about the different model outputs and create a single synthesized file that combines the best elements and insights from all outputs: `CONSULTANT-PLAN.md`
        (Replace specific-context-files with relevant code paths from Step 2).
    - **Execute Command:** Run it.
    - **Handle Errors:** Report errors. Write any errors you encounter to a persistent log file. Attempt **one** retry if fixable, report failure and stop if unresolvable.
    - **Identify Output Directory:** Report success and output path.

## 3. Review Architect's Response
- **Goal:** Understand and review the implementation plan from architect.
- **Actions:**
    - Read the architect-generated plan in `CONSULTANT-PLAN.md`.
    - **Verify Standards Alignment:** Confirm the plan aligns with our `DEVELOPMENT_PHILOSOPHY.md`.
## 4. Execute Plan
- **Goal:** Execute the plan to resolve the original issue.
- **Actions:**
    - **Execute Plan:** Treat `CONSULTANT-PLAN.md` as the primary plan for this issue. Use standard `EXECUTE.MD` process for tasks within it if structured similarly. This supersedes previous plans *for this issue*.
    - Continue until resolved or plan completed.
    - **Update Task Status:** If the task is resolved, change the task status in `TODO.MD` from `[~]` (in progress) to `[x]` (complete).
    - Remove `CONSULT-REQUEST.md` and `CONSULTANT-PLAN.md`
