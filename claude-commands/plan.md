# PLAN

## 1. SELECT AND SCOPE TASK
- Read `BACKLOG.md` and identify the top item as the task description string.
- Evaluate if the task represents a single atomic unit of functionality:
  - A single, well-defined responsibility
  - One logical change that can be understood in isolation
  - Independently testable
  - Completes a discrete, meaningful step toward a larger goal
  - Can be reviewed thoroughly in a single sitting

## 2. TASK DECOMPOSITION (IF NEEDED)
- If the task exceeds an atomic unit of functionality:
  1. Break the task into multiple atomic units (as many as needed)
  2. Sequence them in dependency order
  3. Update `BACKLOG.md` to:
     - Remove the original task
     - Add the first atomic unit at the top (current task)
     - Add remaining atomic units as separate backlog items below
  4. Document relationships and dependencies between units
  5. Ensure each atomic unit delivers testable value on its own

## 3. PREPARE TASK FILE
- Create a file named `TASK-PROMPT.md`.
- Copy the content from `prompts/plan.md` as the base for your task prompt.
- Add the following to the top of the file, before the existing content:
    ```markdown
    ## Task Description
    [Insert properly scoped task description from Steps 1-2]
    ```

## 4. GENERATE PLAN WITH ARCHITECT
- **Goal:** Use `architect` to generate potential implementation plans based on the properly scoped task description and project context.
- **Actions:**
    - **Find Task Context:**
        1. Find the top ten most relevant files for task-specific context
    - **Run Architect:**
        1. Run the following command:
        ```bash
        architect --instructions TASK-PROMPT.md --output-dir architect_output --model gemini-2.5-pro-preview-03-25 --model gemini-2.5-pro-exp-03-25 --model gemini-2.0-flash docs/DEVELOPMENT_PHILOSOPHY.md [top-ten-relevant-files]
        ```
        - **Review and Synthesize:**
            1. Review all files in the architect_output directory
            2. ***Think hard*** about the different model outputs and create a single synthesized file that combines the best elements and insights from all outputs: `PLAN.md`
    - **Handle Errors:** If `architect` fails:
        - Report the specific error message.
        - Write the error to a persistent log file.
        - Analyze the error. Attempt to fix and retry **once** if feasible.
        - If unresolvable, report "Architect CLI invocation failed. See error above. Manual assistance required." and **stop**.
    - **Output:** If the command completes successfully, report "Architect CLI invocation successful. Plan saved to PLAN.md."

## 5. REVIEW PLAN
- **Goal:** Review the generated plan in `PLAN.MD`, ensuring it prioritizes testability and maintains proper scope.
- **Actions:**
    - Read the generated `PLAN.MD`.
    - **Verify Content:** Ensure the plan contains detailed steps, approaches, considerations (especially testability evaluations), and potential challenges.
    - **Verify Scope:** Ensure the plan represents a single atomic unit of functionality that can be implemented in one pull request.
    - **Verify Standards Alignment:** Confirm the plan aligns with our standards hierarchy:
      1. First, prioritizes simplicity and clarity (`CORE_PRINCIPLES.md`)
      2. Second, ensures strong separation of concerns (`ARCHITECTURE_GUIDELINES.md`)
      3. Third, maximizes testability with minimal mocking (`TESTING_STRATEGY.md`)
      4. Fourth, follows idiomatic coding patterns (`CODING_STANDARDS.md`)
      5. Fifth, supports clear documentation of design decisions (`DOCUMENTATION_APPROACH.md`)
    - (Optional Cleanup): Remove the temporary `TASK-PROMPT.md` file.

## 6. CHECKOUT BRANCH
- Switch to a new git branch for implementing the work described in the `PLAN.MD`.
