# TICKET

## 1. Create Ticket Task File
- Create `ticket-task.md`.
- Copy content from `docs/prompts/ticket.md`.
- Append full content of `PLAN.md` under `## Implementation Plan`.

## 2. Generate Task Breakdown
- Run thinktank:
    ```bash
    thinktank --instructions ticket-task.md --output-dir thinktank_output --model gemini-2.5-pro-preview-03-25 --model o4-mini --model openrouter/x-ai/grok-3-mini-beta --model openrouter/deepseek/deepseek-r1 DEVELOPMENT_PHILOSOPHY.md PLAN.md
    ```
- **Review & Synthesize:**
    1. Review `thinktank_output` files.
    2. ***Think hard*** & synthesize into `TODO.md`. Ensure unique sequential Task IDs (e.g., T001) and `Depends On:` uses these IDs.
- Handle errors (log, retry once, stop). Report success.

## 3. Review Tasks
- Verify `TODO.md`:
    - Completeness (all features/ACs covered or clarified).
    - Correct Task ID usage and dependency mapping (no cycles).
- Remove `ticket-task.md`.

