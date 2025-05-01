# EXTRACT

## 1. Create task.md
- Create `task.md`.
- Copy content from `docs/prompts/extract.md`.
- Add note: "Keep the program's purpose in mind and strive for the highest quality maintainable code while avoiding overengineering. Balance modularity with avoiding unnecessary complexity."

## 2. Run thinktank-wrapper
- Run:
    ```bash
    thinktank-wrapper --model-set high_context --include-philosophy --include-glance --instructions task.md ./
    ```
- Copy synthesis file to create `EXTRACT_PLAN.md`

