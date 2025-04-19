# ADDRESS

## 1. Verify Code Review File
- Confirm existence of `CODE_REVIEW.md`.
- Review for standard format (issues, recommendations, priorities).

## 2. Prepare Address Instructions
- Create `ADDRESS-PROMPT.md`.
- Copy content from `docs/prompts/address.md`.
- Add code review context: `## Code Review Content\n[Content of CODE_REVIEW.md]` at the top.

## 3. Generate Plan with Architect
- Run architect:
    ```bash
    architect --instructions ADDRESS-PROMPT.md --output-dir architect_output --model gemini-2.5-flash-preview-04-17 --model gemini-2.5-pro-preview-03-25 --model o4-mini --model gpt-4.1 ./
    ```
- **Review & Synthesize:**
    1. Review `architect_output` files.
    2. ***Think hard*** & synthesize into `PLAN.md`.
- Handle errors (report, log, retry once, stop). Report success.

## 4. Review Remediation Plan
- Read `PLAN.MD`.
- Verify it addresses all significant issues from the code review.
- Ensure solutions align with `DEVELOPMENT_PHILOSOPHY.md`.
- (Optional Cleanup): Remove `ADDRESS-PROMPT.md`.

## 5. Checkout Branch
- Check out a branch named `address-code-review` for implementing the remediation plan.
