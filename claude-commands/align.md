# ALIGN

## GOAL
Analyze the codebase against our development philosophy and generate backlog items to improve alignment.

## 1. Prepare Context
- Read `BACKLOG.md` to understand current tasks.
- Read `DEVELOPMENT_PHILOSOPHY.md` and relevant language-specific appendices.
- Identify all `glance.md` files in the codebase to gather architectural insights.

## 2. Create Prompt File
- Create `ALIGN-PROMPT.md`.
- Copy content from `docs/prompts/align.md`.
- Add current backlog context:
  ```
  ## Current Backlog
  [Copy content from BACKLOG.md]
  ```

## 3. Generate Philosophy-Aligned Backlog Items
- Make sure to maximize the timeout on the Bash tool you use to invoke `thinktank-wrapper`
- Run thinktank-wrapper for comprehensive analysis:
  ```bash
  thinktank-wrapper --model-set high_context --include-philosophy --include-glance --instructions ALIGN-PROMPT.md ./
  ```
- Copy synthesis file to create new `ALIGN_BACKLOG_ITEMS.md`
- Append items to `BACKLOG.md` after review
- Remove `ALIGN-PROMPT.md` and `thinktank_*/`

