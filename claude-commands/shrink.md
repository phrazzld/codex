# SHRINK

## 1. Create task.md
- Create `task.md`.
- Copy content from `docs/prompts/shrink.md`.

## 2. Run thinktank-wrapper
- Run:
    ```bash
    thinktank-wrapper --model-set high_context --include-philosophy --include-glance --instructions task.md ./
    ```
- Copy synthesis file to create a `SHRINK_PLAN.md` file
- Handle errors (log, retry).

## 3. Read Plan
- Review `SHRINK_PLAN.md` for proposed optimization steps.
