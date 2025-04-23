# CONSULT

## 1. Formulate Request & Identify Task
- Identify struggling `Original Task ID: TXXX` from `TODO.md`.
- Create `CONSULT-REQUEST.md`.
- ***Think hard*** & populate with: `Original Task ID`, `Goal`, `Problem/Blocker` (Relate to `DEVELOPMENT_PHILOSOPHY.md`), `Context/History`, `Key Files`, `Errors`, `Desired Outcome`.
- Identify the ten files most relevant to the problem you're struggling with.

## 2. Invoke Thinktank for Plan
- Add to `CONSULT-REQUEST.md`: "Keep the program's purpose in mind and strive for the highest quality maintainable solutions while avoiding overengineering."
- Run thinktank:
    ```bash
    thinktank --instructions CONSULT-REQUEST.md --output-dir consultation-report --model gemini-2.5-pro-preview-03-25 --model gpt-4.1 --model o4-mini --model openrouter/x-ai/grok-3-mini-beta --model openrouter/deepseek/deepseek-r1 DEVELOPMENT_PHILOSOPHY.md [ten most relevant files]
    ```
- **Review & Synthesize Plan:**
    1. Review `thinktank_output` files.
    2. ***Think hard*** & synthesize into `CONSULTANT-PLAN.md`.
    3. Ensure plan balances code quality with practicality and avoids unnecessary complexity.
- Handle errors (log, retry once, stop). Report success/failure.

## 3. Generate Resolution Tasks in TODO.md
- Create `CONSULT-TASKGEN-REQUEST.md`. Instruct AI (via prompt) to:
    - Analyze `CONSULTANT-PLAN.md`.
    - Decompose plan into new, atomic tasks for `TODO.md`.
    - Assign new unique Task IDs (sequential).
    - Format tasks correctly (ID, Title, Action, `Depends On:` using IDs, `AC Ref: None`).
    - Final task's `Action:` should mark `Original Task ID: TXXX` as `[x]`.
- Run thinktank for task generation:
    ```bash
    thinktank --instructions CONSULT-TASKGEN-REQUEST.md --output-dir thinktank_output_tasks --model gemini-2.5-pro-preview-03-25 --model gpt-4.1 --model o4-mini --model openrouter/x-ai/grok-3-mini-beta --model openrouter/deepseek/deepseek-r1 DEVELOPMENT_PHILOSOPHY.md CONSULTANT-PLAN.md
    ```
- **Synthesize & Insert Tasks:**
    - Review generated tasks.
    - ***Think hard*** & synthesize best breakdown.
    - Insert new tasks into `TODO.md` (logically after `Original Task ID`).
- Remove `CONSULT-REQUEST.md`, `CONSULTANT-PLAN.md`, `CONSULT-TASKGEN-REQUEST.md`.
- Report: "Generated resolution tasks [New Task IDs] in TODO.md for original task [Original Task ID]. Proceed via /execute."
- **Stop** `/consult`.

