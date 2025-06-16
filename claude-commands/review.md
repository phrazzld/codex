# REVIEW

## GOAL
Generate a comprehensive code review of changes against best practices, using a diff and relevant source files as context.

## 1. Create Context File 
- Create `REVIEW-CONTEXT.md` with the following content:
  ```markdown
  # Code Review Context
  
  ## PR Details
  Branch: [current branch name]
  Files Changed: [count of changed files]
  
  ## Diff
  [Output of git diff master]
  ```

## 2. Generate Diff and Complete Context File
- Run `git diff master` (or relevant base branch) and add the output to the context file
- Update the PR Details section with current branch and files changed info

## 3. Perform Deep Code Review
- Identify every file changed in the diff
- ***Think very hard*** about the code changes:
  - Analyze the diff line-by-line for correctness, performance, security, and maintainability
  - Check for adherence to leyline document principles
  - Evaluate consistency with existing codebase patterns and conventions
  - Identify potential bugs, edge cases, or error handling issues
  - Consider architectural implications and design patterns
  - Review test coverage and testability of the changes
  - Assess documentation completeness and clarity
- Create `CODE_REVIEW.md` with structured findings including:
  - Summary of changes
  - Issues found (categorized by severity)
  - Recommendations for improvement
  - Positive aspects worth highlighting