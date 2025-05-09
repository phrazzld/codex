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

## 3. Run Thinktank Review
- Identify every file changed in the diff
- Run (with the maximum timeout in the bash tool used to invoke it):
    ```bash
    thinktank-wrapper --template review --inject REVIEW-CONTEXT.md --model-set high_context --include-philosophy --include-glance [changed files]
    ```
- Review the generated output directory and use the synthesis file to create `CODE_REVIEW.md`