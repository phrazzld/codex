# REVIEW

## 1. Create diff.md
- Create `diff.md`.
- Copy content from `docs/prompts/review.md`.
- Add `## Diff` section at the end.

## 2. Generate Diff
- Run `git diff master` (or relevant base branch). Append output to `diff.md`.

## 3. Run Thinktank Review
- Run:
    ```bash
    thinktank-wrapper --model-set high_context --include-philosophy --include-glance --instructions diff.md ./
    ```
- Copy synthesis file to create `CODE_REVIEW.md`

