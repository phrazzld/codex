# IDEATE

## GOAL
Generate innovative ideas for the project backlog by analyzing existing tasks and codebase context.

## 1. Prepare Context
- Read `BACKLOG.md` to understand current tasks and direction.
- Analyze codebase structure to identify areas for enhancement.

## 2. Prepare Prompt File
- Create `IDEATE-PROMPT.md`.
- Copy content from `$DEVELOPMENT/codex/docs/prompts/ideate.md`.
- Add current backlog content as context:
  ```
  ## Current Backlog
  [Copy content from BACKLOG.md]
  ```

## 3. Generate Ideas with Architect
- Run architect:
  ```bash
  architect --instructions IDEATE-PROMPT.md --output-dir architect_output --model gemini-2.5-pro-exp-03-25 --model gemini-2.0-flash ./
  ```
- **Review & Synthesize:**
  1. Review `architect_output` files.
  2. ***Think hard*** & synthesize into `IDEAS.md`.
- Handle errors (report, log, retry once, stop). Report success.

## 4. Review Ideas
- Read `IDEAS.md`.
- Evaluate generated ideas for:
  - Technical feasibility
  - Alignment with project goals
  - Innovation value
  - Implementation complexity
- Prioritize ideas based on impact vs. effort.

## 5. Update Backlog (Optional)
- Add selected ideas to `BACKLOG.md`.
- Ensure new items follow the same format as existing entries.
- (Optional Cleanup): Remove `IDEATE-PROMPT.md`.