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
    thinktank --instructions diff.md --output-dir thinktank_output --model gemini-2.5-flash-preview-04-17 --model gpt-4.1 --model gemini-2.5-pro-preview-03-25 ./
    ```
- **Review & Synthesize:**
    1. Review `thinktank_output` files.
    2. ***Think hard*** & synthesize into `CODE_REVIEW.md`, including summary table per prompt.
- Handle errors (log, retry).

## 4. Review the Review
- Read `CODE_REVIEW.MD`.
- Verify feedback covers all dimensions of `DEVELOPMENT_PHILOSOPHY.md`.
- Ensure review addresses both quality and complexity - flagging both under-engineering (too simplistic, brittle) and over-engineering (unnecessary complexity, premature abstraction).
- Validate that review keeps the program's purpose in mind and evaluates code against practical value delivery.

