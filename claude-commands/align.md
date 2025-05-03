# ALIGN

## GOAL
Analyze the codebase against our development philosophy and generate backlog items to improve alignment.

## 1. Prepare Context
- Read `BACKLOG.md` to understand current tasks.
- Read `DEVELOPMENT_PHILOSOPHY.md` and relevant language-specific appendices.
- Identify all `glance.md` files in the codebase to gather architectural insights.

## 2. Create ALIGN-PROMPT File
- Create `ALIGN-PROMPT.md` with the following content:
  ```markdown
  # Philosophy Alignment Analysis

  ## Current Backlog
  [Copy content from BACKLOG.md]

  [Template content from align.md would be included here]
  ```
- Add the current backlog content to the prompt file

## 3. Generate Philosophy-Aligned Backlog Items
- Run thinktank-wrapper (with the maximum timeout in the bash tool used to invoke it):
  ```bash
  thinktank-wrapper --instructions ALIGN-PROMPT.md --model-set high_context --include-philosophy --include-glance ./
  ```
- Review the generated output directory and use the synthesis file to create `ALIGN_BACKLOG_ITEMS.md`
- Append items to `BACKLOG.md` after review
- Remove `ALIGN-PROMPT.md`