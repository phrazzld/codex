# SHRINK

## 1. Create task.md
- Create `task.md`.
- Copy content from `docs/prompts/shrink.md`.

## 2. Run thinktank
- Run:
    ```bash
    # Find relevant context files if needed
    thinktank --instructions task.md --synthesis-model gemini-2.5-pro-preview-03-25 --model gemini-2.5-flash-preview-04-17 --model gemini-2.5-pro-preview-03-25 --model gpt-4.1 ./
    ```
- Copy synthesis file to create plan:
    ```bash
    cp thinktank_output/gemini-2.5-pro-preview-03-25-synthesis.md SHRINK_PLAN.md
    ```
- Handle errors (log, retry).

## 3. Read Plan
- Review `SHRINK_PLAN.md` for proposed optimization steps.
