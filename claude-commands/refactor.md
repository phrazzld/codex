# REFACTOR

## 1. Create task.md
- Create `task.md`.
- Copy content from `docs/prompts/refactor.md`.
- Add note: "Keep the program's purpose in mind and strive for the highest quality maintainable code while avoiding overengineering. Focus on practical improvements that provide real value."

## 2. Run thinktank-wrapper
- Make sure to maximize the timeout on the Bash tool you use to invoke `thinktank-wrapper`
- Run:
    ```bash
    thinktank-wrapper --model-set high_context --include-philosophy --include-glance --instructions task.md ./
    ```
- Copy synthesis file to create `REFACTOR_PLAN.md`

