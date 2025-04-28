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
  thinktank --instructions GROOM-PROMPT.md --synthesis-model gemini-2.5-pro-preview-03-25 --model gemini-2.5-flash-preview-04-17 --model gemini-2.5-pro-preview-03-25 --model o4-mini --model gpt-4.1 BACKLOG.md $(find . -name "glance.md")
  ```
- Copy synthesis file to create new backlog:
  ```bash
  cp thinktank_output/gemini-2.5-pro-preview-03-25-synthesis.md BACKLOG.md
  ```
- Review to ensure backlog maintains balance between:
  - Innovation and practicality
  - Technical excellence and business value
  - Short-term improvements and long-term vision
- Handle errors (report, log, retry once). Report success.

## 4. Review Enhanced Backlog
- Read the synthesized `BACKLOG.md`.
- Verify content is well-structured, prioritized, and covers all dimensions:
  - Feature development
  - Technical improvements
  - Performance optimizations
  - Research and experimentation
  - Developer experience
  - Business value
- Ensure items are specific, actionable, and aligned with development philosophy.
- Remove `GROOM-PROMPT.md` and `thinktank_output/`.

## 5. Commit Updated Backlog
- Create commit with enhanced `BACKLOG.md`.
- Use conventional commit format: `feat: enhance and prioritize project backlog`
