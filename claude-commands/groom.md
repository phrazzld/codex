# GROOM

## GOAL
Create an organized, expanded, and prioritized backlog based on comprehensive codebase insights.

## 1. Prepare Context
- Read `BACKLOG.md` to understand current tasks and direction.
- Identify all `glance.md` files in the codebase to gather architectural insights.
- Read `DEVELOPMENT_PHILOSOPHY.md` to anchor new backlog items in project principles.

## 2. Create Prompt File
- Create `GROOM-PROMPT.md`.
- Copy content from `docs/prompts/groom.md`.
- Add current backlog context:
  ```
  ## Current Backlog
  [Copy content from BACKLOG.md]
  ```

## 3. Generate Enhanced Backlog with Thinktank
- Run thinktank with multiple models for diverse perspectives:
  ```bash
  thinktank --instructions GROOM-PROMPT.md "${THINKTANK_ALL_MODELS[@]}" "${THINKTANK_SYNTHESIS_MODEL[@]}" BACKLOG.md $(find_philosophy_files) $(find_glance_files)
  ```
- Copy synthesis file to create new `BACKLOG.md`
- Remove `GROOM-PROMPT.md` and `thinktank_*/`

