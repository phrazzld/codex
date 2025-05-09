# ADDRESS

## GOAL
Generate a structured plan to address findings from a code review, with concrete code changes and implementation steps.

## 1. Verify Code Review File
- Confirm existence of `CODE_REVIEW.md`.
- Review for standard format (issues, recommendations, priorities).

## 2. Create Context File
- Create `ADDRESS-CONTEXT.md` with the content from the code review:
  ```markdown
  # Code Review Details

  ## Code Review Content
  [Content of CODE_REVIEW.md]

  ## Task
  Create a comprehensive plan to address the issues identified in the code review.
  ```

## 3. Generate Plan with Thinktank
- Identify the most relevant source code files mentioned in the code review
- Run thinktank-wrapper (with the maximum timeout in the bash tool used to invoke it):
  ```bash
  thinktank-wrapper --template address --inject ADDRESS-CONTEXT.md --model-set all --include-philosophy --include-glance [relevant source files]
  ```
- Review the generated output directory and use the synthesis file to create `REMEDIATION_PLAN.md`