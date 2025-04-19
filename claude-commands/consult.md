# CONSULT

## 1. Formulate Request & Identify Task
- Identify struggling `Original Task ID: TXXX` from `TODO.md`.
- Create `CONSULT-REQUEST.md`.
- ***Think hard*** & populate with: `Original Task ID`, `Goal`, `Problem/Blocker` (Relate to `DEVELOPMENT_PHILOSOPHY.md`), `Context/History`, `Key Files`, `Errors`, `Desired Outcome`.

## 2. Invoke Architect for Plan
- Run architect:
    ```bash
    architect --instructions CONSULT-REQUEST.md --output-dir architect_output --model gemini-2.5-flash-preview-04-17 --model gemini-2.5-pro-preview-03-25 --model o4-mini --model gpt-4.1 DEVELOPMENT_PHILOSOPHY.md ./
    ```
- **Review & Synthesize Plan:**
    1. Review `architect_output` files.
    2. ***Think hard*** & synthesize into `CONSULTANT-PLAN.md`.
- Handle errors (log, retry once, stop). Report success/failure.

## 3. Generate Resolution Tasks in TODO.md
- Create `CONSULT-TASKGEN-REQUEST.md`. Instruct AI (via prompt) to:
    - Analyze `CONSULTANT-PLAN.md`.
    - Decompose plan into new, atomic tasks for `TODO.md`.
    - Assign new unique Task IDs (sequential).
    - Format tasks correctly (ID, Title, Action, `Depends On:` using IDs, `AC Ref: None`).
    - Final task's `Action:` should mark `Original Task ID: TXXX` as `[x]`.
- Run architect for task generation:
    ```bash
    architect --instructions CONSULT-TASKGEN-REQUEST.md --output-dir architect_output_tasks --model gemini-2.5-flash-preview-04-17 --model gemini-2.5-pro-preview-03-25 --model o4-mini --model gpt-4.1 DEVELOPMENT_PHILOSOPHY.md CONSULTANT-PLAN.md
    ```
- **Synthesize & Insert Tasks:**
    - Review generated tasks.
    - ***Think hard*** & synthesize best breakdown.
    - Insert new tasks into `TODO.md` (logically after `Original Task ID`).
- Remove `CONSULT-REQUEST.md`, `CONSULTANT-PLAN.md`, `CONSULT-TASKGEN-REQUEST.md`.
- Report: "Generated resolution tasks [New Task IDs] in TODO.md for original task [Original Task ID]. Proceed via /execute."
- **Stop** `/consult`.

