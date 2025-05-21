# SHRINK

## GOAL
Analyze the codebase and generate GitHub issues for code size optimization while preserving functionality.

## 1. Prepare Context
- Fetch current GitHub issues to understand existing tasks:
  ```bash
  gh issue list --state open --json number,title,body,labels --limit 100
  ```
- Read `DEVELOPMENT_PHILOSOPHY.md` and relevant language-specific appendices.
- Identify all `glance.md` files in the codebase to gather architectural insights.

## 2. Create Context File
- Create `SHRINK-CONTEXT.md` with the following content:
  ```markdown
  # Code Size Optimization Context

  ## Current Issues
  [Include output from GitHub issues list]

  ## Request
  Analyze the codebase and generate items for code size optimization while preserving functionality.
  Focus on reducing file sizes, eliminating duplicated code, and simplifying complex implementations.
  ```

## 3. Generate Size Optimization Items
- Run thinktank-wrapper with shrink template (with the maximum timeout in the bash tool used to invoke it):
  ```bash
  thinktank-wrapper --template shrink --inject SHRINK-CONTEXT.md --model-set high_context --include-philosophy --include-glance ./
  ```
- Thoroughly review all files in the generated output directory, not just the synthesis file
- If the synthesis file appears truncated or incomplete, manually analyze all output files and synthesize the information
- For each size optimization opportunity, create a GitHub issue with appropriate details and labels
