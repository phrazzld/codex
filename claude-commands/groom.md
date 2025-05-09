# GROOM

## GOAL
Create an organized, expanded, and prioritized backlog based on comprehensive codebase insights.

## 1. Prepare Context
- Read `BACKLOG.md` to understand current tasks and direction.
- Identify all `glance.md` files in the codebase to gather architectural insights.
- Read `DEVELOPMENT_PHILOSOPHY.md` to anchor new backlog items in project principles.

## 2. Generate Enhanced Backlog with Thinktank
- Create `GROOM-CONTEXT.md` with grooming criteria and current backlog information:
  ```markdown
  # Backlog Grooming Context
  
  ## Current Backlog
  [Include content from BACKLOG.md]
  
  ## Grooming Goals
  - Prioritize items based on business value and technical dependencies
  - Identify missing tasks that should be added
  - Remove or modify outdated tasks
  - Ensure all tasks are clear, atomic, and actionable
  ```
- Run thinktank-wrapper with the groom template (with the maximum timeout in the bash tool used to invoke it):
  ```bash
  thinktank-wrapper --template groom --inject GROOM-CONTEXT.md --model-set all --include-philosophy --include-glance BACKLOG.md
  ```
- Review the generated output directory and use the synthesis file to create a new `BACKLOG.md`