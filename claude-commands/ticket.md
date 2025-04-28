# TICKET

## 1. Create Ticket Task File
- Create `ticket-task.md`.
- Copy content from `docs/prompts/ticket.md`.
- Append full content of `PLAN.md` under `## Implementation Plan`.

## 2. Generate Task Breakdown
- Find relevant development philosophy files
- Run thinktank:
    ```bash
    thinktank --instructions ticket-task.md --synthesis-model gemini-2.5-pro-preview-03-25 --model gemini-2.5-pro-preview-03-25 --model o4-mini PLAN.md [relevant development philosophy files]
    ```
- Copy synthesis file to create TODO.md

## 3. Review Tasks
- Verify `TODO.md`:
    - Completeness (all features/ACs covered or clarified).
    - Correct Task ID usage and dependency mapping (no cycles).
    - Appropriate inclusion of verification steps for UI/UX changes and user-facing features.

## 4. Clean Up
- Remove `ticket-task.md`
- Remove `thinktank_output/`

