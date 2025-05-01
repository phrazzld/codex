# REVIEW

## 1. Create diff.md
- Create `diff.md`.
- Copy content from `docs/prompts/review.md`.
- Add `## Diff` section at the end.

## 2. Generate Diff
- Run `git diff master` (or relevant base branch). Append output to `diff.md`.

## 3. Run Thinktank Review
- Make a list of most useful files reference files to include that relate to the work done on this branch
    - All development philosophy files
    - `glance.md` files in relevant directories
    - `PLAN.md` and `TODO.md`
- Run:
    ```bash
    thinktank --instructions diff.md $THINKTANK_HIGH_CONTEXT_MODELS $THINKTANK_SYNTHESIS_MODEL [at least 10 relevant reference files]
    ```
- Copy synthesis file to create `CODE_REVIEW.md`

