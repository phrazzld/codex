# TICKET

## 1. Create Ticket Task File
- Create `ticket-task.md`.
- Copy content from `docs/prompts/ticket.md`.
- Append full content of `PLAN.md` under `## Implementation Plan`.

## 2. Generate Task Breakdown
- Make sure to maximize the timeout on the Bash tool you use to invoke `thinktank-wrapper`
- Run thinktank-wrapper:
    ```bash
    thinktank-wrapper --model-set all --include-philosophy --include-glance --instructions ticket-task.md PLAN.md
    ```
- Copy synthesis file to create `TODO.md`

## 3. Review Tasks
- Verify `TODO.md`:
    - Completeness (all features/ACs covered or clarified).
    - Correct Task ID usage and dependency mapping (no cycles).
    - Appropriate inclusion of verification steps for UI/UX changes and user-facing features.

## 4. Clean Up
- Remove `ticket-task.md`
- Remove `thinktank_*/`

