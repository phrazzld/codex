# ADDRESS

## GOAL
Generate a structured plan to address findings from a code review, with concrete code changes and implementation steps.

## 1. Verify Code Review File
- Confirm existence of `CODE_REVIEW.md`.
- Review for standard format (issues, recommendations, priorities).

## 2. Create Custom Prompt File
- Create `ADDRESS-PROMPT.md` with the following content:
  ```markdown
  # Code Review Remediation Plan

  ## Code Review Content
  [Content of CODE_REVIEW.md]

  ## Task
  Create a comprehensive plan to address the issues identified in the code review.
  
  [Template content from address.md would be included here]
  ```

## 3. Generate Plan with Thinktank
- Identify the most relevant source code files mentioned in the code review
- Run thinktank-wrapper:
  ```bash
  thinktank-wrapper --instructions ADDRESS-PROMPT.md --model-set all --include-philosophy --include-glance [relevant source files]
  ```
- Review the generated output directory and use the synthesis file to create `REMEDIATION_PLAN.md`