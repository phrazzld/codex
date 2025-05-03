# GROOM

## GOAL
Create an organized, expanded, and prioritized backlog based on comprehensive codebase insights.

## 1. Prepare Context
- Read `BACKLOG.md` to understand current tasks and direction.
- Identify all `glance.md` files in the codebase to gather architectural insights.
- Read `DEVELOPMENT_PHILOSOPHY.md` to anchor new backlog items in project principles.

## 2. Generate Enhanced Backlog with Thinktank
- Run thinktank-wrapper with the groom template (with the maximum timeout in the bash tool used to invoke it):
  ```bash
  thinktank-wrapper --template groom --model-set all --include-philosophy --include-glance BACKLOG.md
  ```
- Review the generated output directory and use the synthesis file to create a new `BACKLOG.md`