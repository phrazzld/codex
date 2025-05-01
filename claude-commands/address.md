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
    thinktank --instructions ADDRESS-PROMPT.md $THINKTANK_ALL_MODELS $THINKTANK_SYNTHESIS_MODEL $(find_philosophy_files) $(find_glance_files) [relevant source files]
    ```
- Copy synthesis file to create a PLAN.md file.
- Handle errors (report, log, retry once, stop). Report success.

## 4. Review Remediation Plan
- Read `PLAN.md`.
- Verify it addresses all significant issues from the code review.
- Ensure solutions align with `DEVELOPMENT_PHILOSOPHY.md`.
- Remove `ADDRESS-PROMPT.md`.

