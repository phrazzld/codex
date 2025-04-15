# TICKET

## 1. Create Ticket Task File

- **Goal:** Create a dedicated prompt file for `architect` to generate task tickets.
- **Actions:**
    - Create a new file called `ticket-task.md`.
    - Copy the content from `$DEVELOPMENT/codex/docs/prompts/ticket.md` into `ticket-task.md`.
    - Read the full content of `PLAN.md` and append it to `ticket-task.md` under a section titled "## Implementation Plan".

## 2. Generate Task Breakdown with Architect

- **Goal:** Use `architect` to generate a detailed, actionable list of tasks required to implement the plan.
- **Actions:**
    - **Run Architect:**
        ```bash
        architect --instructions ticket-task.md --output-dir architect_output --model gemini-2.5-pro-exp-03-25 --model gemini-2.0-flash ./
        ```
        - **Review and Synthesize:**
            1. Review all files in the architect_output directory
            2. ***Think hard*** about the different model outputs and create a single synthesized file that combines the best elements and insights from all outputs: `TODO.md`
    - **Handle Errors:** If `architect` fails:
        - Report the specific error message.
        - Write the error to a persistent log file.
        - Attempt to fix and retry **once** if feasible.
        - If unresolvable, report "Architect CLI invocation failed. See error above. Manual assistance required." and **stop**.
    - **Output:** If the command completes successfully, report "Architect CLI invocation successful. Tasks saved to TODO.md."

## 3. Review Generated Tasks

- **Goal:** Ensure the generated `TODO.md` accurately reflects the plan and task relationships.
- **Actions:**
    - **Completeness Check:** Confirm that every Feature and Acceptance Criterion from `PLAN.md` is addressed by at least one task or is noted in the Clarifications section.
    - **Dependency Check:** Review the `Depends On:` fields to ensure the listed dependencies make logical sense and that there are no circular dependencies.
    - Remove the temporary `ticket-task.md` file.
