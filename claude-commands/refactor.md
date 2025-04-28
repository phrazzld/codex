# REFACTOR

## 1. Create task.md
- Create `task.md`.
- Copy content from `docs/prompts/refactor.md`.
- Add note: "Keep the program's purpose in mind and strive for the highest quality maintainable code while avoiding overengineering. Focus on practical improvements that provide real value."

## 2. Run thinktank
- Run:
    ```bash
    # Find relevant context files if needed
    thinktank --instructions task.md --synthesis-model gemini-2.5-pro-preview-03-25 --model gemini-2.5-flash-preview-04-17 --model gpt-4.1 --model gemini-2.5-pro-preview-03-25 ./
    ```
- Copy synthesis file to create plan:
    ```bash
    cp thinktank_output/gemini-2.5-pro-preview-03-25-synthesis.md REFACTOR_PLAN.md
    ```
- Review to ensure plan balances code quality with pragmatic implementation.
- Handle errors (log, retry).

## 3. Read Plan
- Review `REFACTOR_PLAN.md` for proposed steps.
- Validate that refactoring suggestions improve maintainability without unnecessary complexity.

