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
    thinktank --instructions diff.md --synthesis-model gemini-2.5-pro-preview-03-25 --model gemini-2.5-flash-preview-04-17 --model gpt-4.1 --model gemini-2.5-pro-preview-03-25 --model o4-mini [at least 10 relevant reference files]
    ```
- Copy synthesis file to create code review:
    ```bash
    cp thinktank_output/gemini-2.5-pro-preview-03-25-synthesis.md CODE_REVIEW.md
    ```
- Handle errors (log, retry).

## 4. Review the Review
- Read `CODE_REVIEW.MD`.
- Verify feedback covers all dimensions of `DEVELOPMENT_PHILOSOPHY.md`.
- Ensure review addresses both quality and complexity - flagging both under-engineering (too simplistic, brittle) and over-engineering (unnecessary complexity, premature abstraction).
- Validate that review keeps the program's purpose in mind and evaluates code against practical value delivery.

