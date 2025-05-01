# IDEATE

## GOAL
Generate innovative ideas for the project backlog by analyzing existing tasks and codebase context.

## 1. Prepare Context
- Read `BACKLOG.md` to understand current tasks and direction.
- Read `DEVELOPMENT_PHILOSOPHY.md` to understand the ideal general principles of the project's structure and implementation.
- Analyze codebase structure to identify areas for enhancement.

## 2. Prepare Prompt File
- Create `IDEATE-PROMPT.md`.
- Copy content from `docs/prompts/ideate.md`.
- Add current backlog content as context:
  ```
  ## Current Backlog
  [Copy content from BACKLOG.md]
  ```

## 3. Generate Ideas with Thinktank
- Make sure to maximize the timeout on the Bash tool you use to invoke `thinktank-wrapper`
- Run thinktank-wrapper:
  ```bash
  thinktank-wrapper --model-set all --include-philosophy --include-glance --instructions IDEATE-PROMPT.md
  ```
- Copy synthesis file to create `IDEAS.md`
- Remove `IDEATE-PROMPT.md`
