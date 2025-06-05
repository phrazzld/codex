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

## 3. Generate Remediation Plan
- Identify the most relevant source code files mentioned in the code review
- ***Think very hard*** about addressing the code review findings:
  - Analyze each issue and its root cause
  - Develop specific code changes to fix identified problems
  - Consider the impact of changes on existing functionality
  - Plan implementation order based on dependencies and risk
  - Include refactoring opportunities that align with best practices
  - Ensure fixes follow DEVELOPMENT_PHILOSOPHY.md and leyline document principles
  - Consider test coverage for all changes
  - Plan for code review of the fixes themselves
- Create `REMEDIATION_PLAN.md` with:
  - Summary of issues being addressed
  - Detailed implementation steps for each fix
  - Specific code changes with before/after examples
  - Testing strategy for validating fixes
  - Risk assessment and mitigation strategies
  - Implementation timeline and priorities