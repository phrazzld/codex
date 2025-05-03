# SHRINK

## GOAL
Analyze the codebase and generate backlog items for code size optimization while preserving functionality.

## 1. Prepare Context
- Read `BACKLOG.md` to understand current tasks.
- Read `DEVELOPMENT_PHILOSOPHY.md` and relevant language-specific appendices.
- Identify all `glance.md` files in the codebase to gather architectural insights.

## 2. Create Prompt File
- Create `SHRINK-PROMPT.md`.
- Copy content from `docs/prompts/shrink.md`.
- Add current backlog context:
  ```
  ## Current Backlog
  [Copy content from BACKLOG.md]
  ```

## 3. Generate Size Optimization Backlog Items
- Run thinktank-wrapper for comprehensive analysis:
  ```bash
  thinktank-wrapper --model-set high_context --include-philosophy --include-glance --instructions SHRINK-PROMPT.md ./
  ```
- Copy synthesis file to create temporary `SHRINK_BACKLOG_ITEMS.md`
- Append items to `BACKLOG.md` after review
- Remove `SHRINK-PROMPT.md` and temporary files
