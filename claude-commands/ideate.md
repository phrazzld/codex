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

## 3. Generate Ideas with Architect
- Run architect:
  ```bash
  architect --instructions IDEATE-PROMPT.md --output-dir architect_output --model gemini-2.5-flash-preview-04-17 --model gemini-2.5-pro-preview-03-25 --model gpt-4.1 ./
  ```
- **Review & Synthesize:**
  1. Review `architect_output` files.
  2. ***Think hard*** & synthesize into `IDEAS.md`.
- Handle errors (report, log, retry once, stop). Report success.

## 4. Review Ideas
- Read `IDEAS.md`.
- Evaluate generated ideas for:
  - Adherence to or realization of development philosophy
  - Technical feasibility
  - Alignment with project goals
  - Innovation value
  - Implementation complexity
  - Balance of quality and avoiding overengineering
  - Focus on practical value delivery
- Prioritize ideas based on impact vs. effort.
- Ensure ideas maintain high quality standards while avoiding unnecessary complexity.

## 5. Update Backlog (Optional)
- Add selected ideas to `BACKLOG.md`.
- Ensure new items follow the same format as existing entries.
- (Optional Cleanup): Remove `IDEATE-PROMPT.md`.
