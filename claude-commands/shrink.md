# SHRINK

## 1. Create task.md
- Create `task.md`.
- Copy content from `docs/prompts/shrink.md`.

## 2. Run architect
- Run:
    ```bash
    # Find relevant context files if needed
    architect --instructions task.md --output-dir architect_output --model gemini-2.5-flash-preview-04-17 --model gemini-2.5-pro-preview-03-25 --model gpt-4.1 ./
    ```
- **Review & Synthesize:**
    1. Review `architect_output` files.
    2. ***Think hard*** & synthesize into `SHRINK_PLAN.md`.
- Handle errors (log, retry).

## 3. Read Plan
- Review `SHRINK_PLAN.md` for proposed optimization steps.
