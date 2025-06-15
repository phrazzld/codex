# TICKET

## GOAL
Generate a detailed task breakdown from a high-level implementation plan into a series of atomic, actionable tasks with proper dependencies.

## 1. Review Plan
- Ensure PLAN.md exists and contains sufficient implementation details.
- Find relevant development philosophy and leyline documents.

## 2. Generate Task Breakdown
- **Leyline Pre-Processing**: Query principles for task decomposition:
  - Tenets related to modularity, incremental delivery, and testability
  - Bindings for task organization and dependency management
  - Synthesize guidelines for creating atomic, well-structured tasks
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
- **Think very hard** about decomposing the plan into implementable tasks:
    - Break down each major component into atomic, testable units
    - Identify logical dependencies and order tasks appropriately
    - Consider parallel work streams where possible
    - Include tasks for writing tests before implementation (TDD approach)
    - Add verification tasks to ensure each component works correctly
    - Think about integration points and add tasks for testing them
    - Consider documentation tasks for significant changes
    - Ensure no task is too large to complete in a reasonable time
    - Include tasks for code review preparation
- Create `TODO.md` with well-structured tasks that:
    - Follow the project's task ID conventions
    - Have clear, actionable descriptions
    - Include acceptance criteria where appropriate
    - Map dependencies correctly

## 3. Review Tasks
- Verify `TODO.md`:
    - Completeness (all features/ACs covered or clarified).
    - Correct Task ID usage and dependency mapping (no cycles).
    - Appropriate inclusion of verification steps for UI/UX changes and user-facing features.