# EXTRACT

## 1. Create task.md
- Create `task.md`.
- Copy content from `docs/prompts/extract.md`.
- Add note: "Keep the program's purpose in mind and strive for the highest quality maintainable code while avoiding overengineering. Balance modularity with avoiding unnecessary complexity."

## 2. Run thinktank
- Run:
    ```bash
    thinktank --instructions task.md $THINKTANK_HIGH_CONTEXT_MODELS $THINKTANK_SYNTHESIS_MODEL $(find_glance_files) $(find_philosophy_files) ./
    ```
- Copy synthesis file to create `EXTRACT_PLAN.md`

