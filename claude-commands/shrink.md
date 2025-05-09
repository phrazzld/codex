# SHRINK

## GOAL
Analyze the codebase and generate backlog items for code size optimization while preserving functionality.

## 1. Prepare Context
- Read `BACKLOG.md` to understand current tasks.
- Read `DEVELOPMENT_PHILOSOPHY.md` and relevant language-specific appendices.
- Identify all `glance.md` files in the codebase to gather architectural insights.

## 2. Create Context File
- Create `SHRINK-CONTEXT.md` with the following content:
  ```markdown
  # Code Size Optimization Context

  ## Current Backlog
  [Copy content from BACKLOG.md]

  ## Request
  Analyze the codebase and generate backlog items for code size optimization while preserving functionality.
  Focus on reducing file sizes, eliminating duplicated code, and simplifying complex implementations.
  ```

## 3. Generate Size Optimization Backlog Items
- Run thinktank-wrapper with shrink template (with the maximum timeout in the bash tool used to invoke it):
  ```bash
  thinktank-wrapper --template shrink --inject SHRINK-CONTEXT.md --model-set high_context --include-philosophy --include-glance ./
  ```
- Copy synthesis file to create temporary `SHRINK_BACKLOG_ITEMS.md`
- Append items to `BACKLOG.md` after review
- Remove `SHRINK-PROMPT.md` and temporary files
