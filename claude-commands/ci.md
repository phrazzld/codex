# CI

## GOAL
Check the CI status for the current PR and generate actionable resolution tasks for failures.

## 1. Check CI Status
- Use `gh` to check the CI status for the current PR
- If successful, celebrate and stop
- If in progress, wait thirty seconds and check again
- If failed, proceed to analyze the failure

## 2. Analyze CI Failure
- Create `CI-FAILURE-ANALYSIS.md` with comprehensive failure details
- Include build information, error logs, failed steps, and affected components
- Document initial analysis of potential causes

## 3. Generate Resolution Plan
- Run thinktank-wrapper with the high_context model set:
  ```bash
  thinktank-wrapper --template ci-failure --model-set high_context --include-philosophy --include-glance ./
  ```
- Review the generated output and create `CI-RESOLUTION-PLAN.md`
- Handle errors (log, retry once, stop). Report success/failure.

## 4. Generate Resolution Tasks
- Create `CI-TASKS-CONTEXT.md` with task generation context:
  ```markdown
  # CI Fix Task Generation

  ## Resolution Plan
  [Relevant excerpts from CI-RESOLUTION-PLAN.md]

  ## Task Requirements
  - Decompose the resolution plan into atomic, implementable tasks
  - Format tasks according to project conventions
  - Include verification steps for each task
  - Ensure tasks are sequenced properly with dependencies
  ```
- Run thinktank-wrapper with ci-failure template and context:
  ```bash
  thinktank-wrapper --template ci-failure --inject CI-TASKS-CONTEXT.md --model-set all --include-philosophy --include-glance CI-RESOLUTION-PLAN.md
  ```
- Review generated tasks and insert into `TODO.md`
- Remove temporary files
