# TICKET

## GOAL
Generate a detailed task breakdown from a high-level implementation plan into a series of atomic, actionable tasks with proper dependencies.

## 1. Review Plan
- Ensure PLAN.md exists and contains sufficient implementation details.
- Find relevant development philosophy files.

## 2. Generate Task Breakdown
- Create `TICKET-CONTEXT.md` with the plan details:
  ```markdown
  # Plan Details
  
  [Include content from PLAN.md]
  
  ## Task Breakdown Requirements
  - Create atomic, independent tasks
  - Ensure proper dependency mapping
  - Include verification steps
  - Follow project task ID and formatting conventions
  ```
- Run thinktank-wrapper with the ticket template (with the maximum timeout in the bash tool used to invoke it):
    ```bash
    thinktank-wrapper --template ticket --inject TICKET-CONTEXT.md --model-set all --include-philosophy --include-glance PLAN.md
    ```
- Review the generated output directory and use the synthesis file to create `TODO.md`

## 3. Review Tasks
- Verify `TODO.md`:
    - Completeness (all features/ACs covered or clarified).
    - Correct Task ID usage and dependency mapping (no cycles).
    - Appropriate inclusion of verification steps for UI/UX changes and user-facing features.