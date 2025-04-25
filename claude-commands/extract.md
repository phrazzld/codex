# EXTRACT

## 1. Create task.md
- Create `task.md`.
- Copy content from `docs/prompts/extract.md`.
- Add note: "Keep the program's purpose in mind and strive for the highest quality maintainable code while avoiding overengineering. Balance modularity with avoiding unnecessary complexity."

## 2. Run thinktank
- Run:
    ```bash
    # Find relevant context files if needed
    thinktank --instructions task.md --output-dir thinktank_output --synthesis-model o4-mini --model gemini-2.5-flash-preview-04-17 --model gemini-2.5-pro-preview-03-25 --model gpt-4.1 ./
    ```
- Copy synthesis file to create plan:
    ```bash
    cp thinktank_output/o4-mini-synthesis.md EXTRACT_PLAN.md
    ```
- Review to ensure plan maintains a proper balance between modularity and simplicity.
- Handle errors (log, retry).

## 3. Read Plan
- Review `EXTRACT_PLAN.md` for proposed modularization steps.
- Validate that extraction suggestions improve maintainability without unnecessary complexity.
