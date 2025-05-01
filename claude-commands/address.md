# ADDRESS

## 1. Verify Code Review File
- Confirm existence of `CODE_REVIEW.md`.
- Review for standard format (issues, recommendations, priorities).

## 2. Prepare Address Instructions
- Create `ADDRESS-PROMPT.md`.
- Copy content from `docs/prompts/address.md`.
- Add code review context: `## Code Review Content\n[Content of CODE_REVIEW.md]` at the top.

## 3. Generate Plan with Thinktank
- Identify the most relevant source code files mentioned in the code review
- Make sure to maximize the timeout on the Bash tool you use to invoke `thinktank-wrapper`
- Run thinktank-wrapper:
    ```bash
    thinktank-wrapper --model-set all --include-philosophy --include-glance --instructions ADDRESS-PROMPT.md [relevant source files]
    ```
- Copy synthesis file to create a `REMEDIATION_PLAN.md` file

