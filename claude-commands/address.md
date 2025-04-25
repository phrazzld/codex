# ADDRESS

## 1. Verify Code Review File
- Confirm existence of `CODE_REVIEW.md`.
- Review for standard format (issues, recommendations, priorities).

## 2. Prepare Address Instructions
- Create `ADDRESS-PROMPT.md`.
- Copy content from `docs/prompts/address.md`.
- Add code review context: `## Code Review Content\n[Content of CODE_REVIEW.md]` at the top.

## 3. Generate Plan with Thinktank
- Identify key files to include:
    - All development philosophy files
    - Top-level glance.md file (ALWAYS include this)
    - Additional relevant glance.md files in affected directories
    - The most relevant source code files mentioned in the code review
- Run thinktank:
    ```bash
    thinktank --instructions ADDRESS-PROMPT.md --output-dir thinktank_output --synthesis-model o4-mini --model gemini-2.5-flash-preview-04-17 --model gemini-2.5-pro-preview-03-25 --model gpt-4.1 --model o4-mini [development philosophy files] [glance.md files] [relevant source files]
    ```
- Copy synthesis file to create plan:
    ```bash
    cp thinktank_output/o4-mini-synthesis.md PLAN.md
    ```
- Handle errors (report, log, retry once, stop). Report success.

## 4. Review Remediation Plan
- Read `PLAN.MD`.
- Verify it addresses all significant issues from the code review.
- Ensure solutions align with `DEVELOPMENT_PHILOSOPHY.md`.
- Remove `ADDRESS-PROMPT.md`.

