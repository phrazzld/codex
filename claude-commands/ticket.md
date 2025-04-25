# TICKET

## 1. Create Ticket Task File
- Create `ticket-task.md`.
- Copy content from `docs/prompts/ticket.md`.
- Append full content of `PLAN.md` under `## Implementation Plan`.

## 2. Generate Task Breakdown
- Find relevant development philosophy files
- Run thinktank:
    ```bash
    thinktank --instructions ticket-task.md --output-dir thinktank_output --synthesis-model o4-mini --model gemini-2.5-pro-preview-03-25 --model o4-mini --model openrouter/deepseek/deepseek-r1 PLAN.md [relevant development philosophy files]
    ```
- Copy synthesis file to create TODO.md:
    ```bash
    cp thinktank_output/o4-mini-synthesis.md TODO.md
    ```
- Handle errors (log, retry once, stop). Report success.

## 3. Review Tasks
- Verify `TODO.md`:
    - Completeness (all features/ACs covered or clarified).
    - Correct Task ID usage and dependency mapping (no cycles).
- Remove `ticket-task.md`.

