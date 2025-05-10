# REFACTOR

## GOAL
Analyze the codebase and generate backlog items for code refactoring while preserving functionality.

## 1. Prepare Context
- Read `BACKLOG.md` to understand current tasks.
- Read `DEVELOPMENT_PHILOSOPHY.md` and relevant language-specific appendices.
- Identify all `glance.md` files in the codebase to gather architectural insights.

## 2. Create Context File
- Create `REFACTOR-CONTEXT.md` with the following content:
  ```markdown
  # Refactoring Analysis Context

  ## Current Backlog
  [Copy content from BACKLOG.md]

  ## Request
  Analyze the codebase and generate backlog items for code refactoring while preserving functionality.
  Focus on improving maintainability, readability, and reducing technical debt.
  ```

## 3. Generate Refactoring Backlog Items
- Run thinktank-wrapper with refactor template (with the maximum timeout in the bash tool used to invoke it):
  ```bash
  thinktank-wrapper --template refactor --inject REFACTOR-CONTEXT.md --model-set high_context --include-philosophy --include-glance ./
  ```
- Copy synthesis file to create temporary `REFACTOR_BACKLOG_ITEMS.md`
- Append items to `BACKLOG.md` after review
- Remove `REFACTOR-PROMPT.md` and temporary files
