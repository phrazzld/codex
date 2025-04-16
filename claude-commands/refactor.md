# REFACTOR

## 1. Create task.md
- Create `task.md`.
- Copy content from `$DEVELOPMENT/codex/docs/prompts/refactor.md`.

## 2. Run architect
- Run:
    ```bash
    # Find relevant context files if needed
    architect --instructions task.md --output-dir architect_output --model gemini-2.5-pro-exp-03-25 --model gemini-2.0-flash ./
    ```
- **Review & Synthesize:**
    1. Review `architect_output` files.
    2. ***Think hard*** & synthesize into `REFACTOR_PLAN.md`.
- Handle errors (log, retry).

## 3. Read Plan
- Review `REFACTOR_PLAN.md` for proposed steps.

