# CI

## GOAL
Check the CI status for the current PR and generate actionable resolution tasks for failures.

## 1. Check CI Status
- Use `gh` to check the CI status for the current PR
- If successful, celebrate and stop
- If in progress, wait thirty seconds and check again
- If failed, proceed to analyze the failure

## 2. Analyze CI Failure
- Create `CI-FAILURE-SUMMARY.md` with comprehensive failure details
- Include build information, error logs, failed steps, and affected components

## 3. Generate Resolution Plan
- Run thinktank-wrapper with the high_context model set:
  ```bash
  thinktank-wrapper --template ci-failure --inject CI-FAILURE-SUMMARY.md --model-set high_context --include-philosophy --include-glance ./
  ```
- Review the generated output -- particularly the synthesis file -- and create `CI-RESOLUTION-PLAN.md`

## 4. Generate Resolution Tasks
- Run thinktank-wrapper with ci-failure template and context:
  ```bash
  thinktank-wrapper --template ticket --inject CI-RESOLUTION-PLAN.md --model-set all --include-philosophy --include-glance CI-FAILURE-SUMMARY.md
  ```
- Review thinktank output, especially the synthesis output, and insert generated tasks into `TODO.md`
- Remove temporary files
