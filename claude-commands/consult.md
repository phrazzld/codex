# CONSULT

## GOAL
Generate alternative approaches and solutions for a blocked task by leveraging multiple AI models, then create specific follow-up tasks in TODO.md.

## 1. Formulate Request & Identify Task
- Identify the issue or blocked task you're struggling with (reference task ID if available).
- Create `CONSULT-REQUEST.md`.
- ***Think hard*** & populate with: `Task Description`, `Goal`, `Problem/Blocker` (Relate to `DEVELOPMENT_PHILOSOPHY.md`), `Context/History`, `Key Files`, `Errors`, `Desired Outcome`.
- Identify the ten files most relevant to the problem you're struggling with.
- Identify development philosophy files

## 2. Invoke Thinktank for Plan
- Add to `CONSULT-REQUEST.md`: "Keep the program's purpose in mind and strive for the highest quality maintainable solutions while avoiding overengineering."
- Run thinktank-wrapper with the consult template (with the maximum timeout in the bash tool used to invoke it):
    ```bash
    thinktank-wrapper --template consult --inject CONSULT-REQUEST.md --model-set high_context --include-philosophy --include-glance ./
    ```
- Review the generated output directory and use the synthesis file to create `CONSULTANT-PLAN.md`
- Handle errors (log, retry once, stop). Report success/failure.

## 3. Generate Resolution Tasks in TODO.md
- Create `CONSULT-CONTEXT.md` with task generation context:
    ```markdown
    # Consultation Task Generation

    ## Consultation Plan
    [Summary of key points from CONSULTANT-PLAN.md]

    ## Task Requirements
    - Decompose the consultant's plan into new, atomic tasks for TODO.md
    - Assign appropriate task IDs based on project conventions
    - Format tasks according to project's task format
    - Ensure final task resolves the original issue
    ```
- Run thinktank-wrapper for task generation (with the maximum timeout in the bash tool used to invoke it):
    ```bash
    thinktank-wrapper --template consult --inject CONSULT-CONTEXT.md --model-set all --include-philosophy --include-glance CONSULTANT-PLAN.md
    ```
- Review tasks in synthesis file
- Insert tasks into `TODO.md`, maintaining consistent formatting.
- Remove `CONSULT-REQUEST.md`, `CONSULTANT-PLAN.md`, `CONSULT-TASKGEN-REQUEST.md`.
- Report: "Generated resolution tasks in TODO.md for the original issue. Proceed via /execute."
- **Stop** `/consult`.