# TICKET

## 1. Create Ticket Task File
- Create `ticket-task.md`.
- Copy content from `docs/prompts/ticket.md`.
- Append full content of `PLAN.md` under `## Implementation Plan`.

## 2. Generate Task Breakdown
- Find relevant development philosophy files
- Run thinktank:
    ```bash
    thinktank --instructions ticket-task.md "${THINKTANK_ALL_MODELS[@]}" "${THINKTANK_SYNTHESIS_MODEL[@]}" PLAN.md $(find_philosophy_files) $(find_glance_files)
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

