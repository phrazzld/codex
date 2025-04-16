# PLAN

## 1. Select & Scope Task
- Identify top item in `BACKLOG.md`.
- Verify task is an atomic epic (single responsibility, testable, reviewable).

## 2. Decompose Task (If Needed)
- If task is greater in scope than one focused epic:
    1. Break into multiple atomic units.
    2. Sequence by dependency.
    3. Update `BACKLOG.md`: Remove original, add first unit top, add rest below.
    4. Document dependencies.

## 3. Prepare Task File
- Create `TASK-PROMPT.md`.
- Copy content from `docs/prompts/plan.md`.
- Add `## Task Description\n[Scoped task description]` at the top.

## 4. Generate Plan with Architect
- Run architect:
    ```bash
    architect --instructions TASK-PROMPT.md --output-dir architect_output --model gemini-2.5-pro-exp-03-25 --model gemini-2.0-flash --model gemini-2.5-pro-preview-03-25 ./
    ```
- **Review & Synthesize:**
    1. Review `architect_output` files.
    2. ***Think hard*** & synthesize into `PLAN.md`.
- Handle errors (report, log, retry once, stop). Report success.

## 5. Review Plan
- Read `PLAN.MD`.
- Verify content (steps, approaches, testability), scope (atomic unit), and alignment with `DEVELOPMENT_PHILOSOPHY.md`.
- (Optional Cleanup): Remove `TASK-PROMPT.md`.

## 6. Checkout Branch
- Check out a branch for completing all of the work in the generated `PLAN.md`.

