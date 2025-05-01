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

## 4. Generate Plan with Thinktank
- Run thinktank-wrapper:
    ```bash
    thinktank-wrapper --model-set high_context --include-philosophy --include-glance --instructions TASK-PROMPT.md ./
    ```
- Copy synthesis file to create `PLAN.md`
- Remove `TASK-PROMPT.md`.

## 5. Checkout Branch
- Check out a branch for completing all of the work in the generated `PLAN.md`.

