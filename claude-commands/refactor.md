# REFACTOR

## 1. Create task.md
- Create `task.md`.
- Copy content from `docs/prompts/refactor.md`.
- Add note: "Keep the program's purpose in mind and strive for the highest quality maintainable code while avoiding overengineering. Focus on practical improvements that provide real value."

## 2. Run architect
- Run:
    ```bash
    # Find relevant context files if needed
    architect --instructions task.md --output-dir architect_output --model gemini-2.5-flash-preview-04-17 --model gpt-4.1 --model gemini-2.5-pro-preview-03-25 ./
    ```
- **Review & Synthesize:**
    1. Review `architect_output` files.
    2. ***Think hard*** & synthesize into `REFACTOR_PLAN.md`.
    3. Ensure plan balances code quality with pragmatic implementation.
- Handle errors (log, retry).

## 3. Read Plan
- Review `REFACTOR_PLAN.md` for proposed steps.
- Validate that refactoring suggestions improve maintainability without unnecessary complexity.

