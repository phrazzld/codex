# CONSULT

## 1. Formulate Request & Identify Task
- Identify struggling `Original Task ID: TXXX` from `TODO.md`.
- Create `CONSULT-REQUEST.md`.
- ***Think hard*** & populate with: `Original Task ID`, `Goal`, `Problem/Blocker` (Relate to `DEVELOPMENT_PHILOSOPHY.md`), `Context/History`, `Key Files`, `Errors`, `Desired Outcome`.
- Identify the ten files most relevant to the problem you're struggling with.
- Identify development philosophy files

## 2. Invoke Thinktank for Plan
- Add to `CONSULT-REQUEST.md`: "Keep the program's purpose in mind and strive for the highest quality maintainable solutions while avoiding overengineering."
- Run thinktank:
    ```bash
    thinktank --instructions CONSULT-REQUEST.md --synthesis-model gemini-2.5-pro-preview-03-25 --model gemini-2.5-flash-preview-04-17 --model gemini-2.5-pro-preview-03-25 --model gpt-4.1 --model o4-mini [development philosophy files] [ten most relevant files]
    ```
- Copy synthesis file to final destination:
    ```bash
    cp consultation-report/gemini-2.5-pro-preview-03-25-synthesis.md CONSULTANT-PLAN.md
    ```
- Handle errors (log, retry once, stop). Report success/failure.

## 3. Generate Resolution Tasks in TODO.md
- Create `CONSULT-TASKGEN-REQUEST.md`. Instruct AI (via prompt) to:
    - Analyze `CONSULTANT-PLAN.md`.
    - Decompose plan into new, atomic tasks for `TODO.md`.
    - Assign new unique Task IDs (sequential).
    - Format tasks correctly (ID, Title, Action, `Depends On:` using IDs, `AC Ref: None`).
    - Final task's `Action:` should mark `Original Task ID: TXXX` as `[x]`.
- Run thinktank for task generation with synthesis model:
    ```bash
    thinktank --instructions CONSULT-TASKGEN-REQUEST.md --synthesis-model gemini-2.5-pro-preview-03-25 --model gemini-2.5-flash-preview-04-17 --model gemini-2.5-pro-preview-03-25 --model gpt-4.1 --model o4-mini [development philosophy files] CONSULTANT-PLAN.md
    ```
- Review synthesized tasks in `thinktank_output_tasks/o4-mini-synthesis.md`
- Insert tasks into `TODO.md` (logically after `Original Task ID`), maintaining consistent formatting and ensuring proper dependency references.
- Remove `CONSULT-REQUEST.md`, `CONSULTANT-PLAN.md`, `CONSULT-TASKGEN-REQUEST.md`.
- Report: "Generated resolution tasks [New Task IDs] in TODO.md for original task [Original Task ID]. Proceed via /execute."
- **Stop** `/consult`.

