# REVIEW

## 1. Create diff.md
- Create `diff.md`.
- Copy content from `docs/prompts/review.md`.
- Add `## Diff` section at the end.

## 2. Generate Diff
- Run `git diff master` (or relevant base branch). Append output to `diff.md`.

## 3. Run Architect Review
- Run:
    ```bash
    architect --instructions diff.md --output-dir architect_output --model gemini-2.5-pro-exp-03-25 --model gemini-2.0-flash ./
    ```
- **Review & Synthesize:**
    1. Review `architect_output` files.
    2. ***Think hard*** & synthesize into `CODE_REVIEW.md`, including summary table per prompt.
- Handle errors (log, retry).

## 4. Review the Review
- Read `CODE_REVIEW.MD`.
- Verify feedback covers all dimensions of `DEVELOPMENT_PHILOSOPHY.md`.

