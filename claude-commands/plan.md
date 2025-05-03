# PLAN

## GOAL
Generate a detailed implementation plan for a prioritized task, with focus on architecture, approach tradeoffs, implementation steps, testing strategy, and risk mitigation.

## 1. Select & Scope Task
- Identify top item in `BACKLOG.md`.
- Verify task is an atomic epic (single responsibility, testable, reviewable).

## 2. Decompose Task (If Needed)
- If task is greater in scope than one focused epic:
    1. Break into multiple atomic units.
    2. Sequence by dependency.
    3. Update `BACKLOG.md`: Remove original, add first unit top, add rest below.
    4. Document dependencies.

## 3. Generate Plan with Thinktank
- Prepare task description for the thinktank prompt
- Run thinktank-wrapper with the plan template (with the maximum timeout in the bash tool used to invoke it):
    ```bash
    thinktank-wrapper --template plan --model-set high_context --include-philosophy --include-glance ./
    ```
- Review the generated output directory and use the synthesis file as the basis for `PLAN.md`

## 4. Checkout Branch
- Check out a branch for completing all of the work in the generated `PLAN.md`.