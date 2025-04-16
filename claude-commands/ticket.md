# TICKET

## 1. Create Ticket Task File
- Create `ticket-task.md`.
- Copy content from `docs/prompts/ticket.md`.
- Append full content of `PLAN.md` under `## Implementation Plan`.

## 2. Generate Task Breakdown
- Run architect:
    ```bash
    architect --instructions ticket-task.md --output-dir architect_output --model gemini-2.5-pro-exp-03-25 --model gemini-2.0-flash ./
    ```
- **Review & Synthesize:**
    1. Review `architect_output` files.
    2. ***Think hard*** & synthesize into `TODO.md`. Ensure unique sequential Task IDs (e.g., T001) and `Depends On:` uses these IDs.
- Handle errors (log, retry once, stop). Report success.

## 3. Review Tasks
- Verify `TODO.md`:
    - Completeness (all features/ACs covered or clarified).
    - Correct Task ID usage and dependency mapping (no cycles).
- Remove `ticket-task.md`.

