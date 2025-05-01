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
- Run thinktank:
  ```bash
  thinktank --instructions IDEATE-PROMPT.md $THINKTANK_ALL_MODELS $THINKTANK_SYNTHESIS_MODEL $(find_glance_files) $(find_philosophy_files)
  ```
- Copy synthesis file to create `IDEAS.md`
- Remove `IDEATE-PROMPT.md`
