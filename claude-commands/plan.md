# PLAN

## GOAL
Generate a detailed implementation plan for a prioritized task, with focus on architecture, approach tradeoffs, implementation steps, testing strategy, and risk mitigation.

## 1. Select & Scope Task
- Identify top item in `BACKLOG.md`.

## 2. Generate Plan with Thinktank
- Create `PLAN-CONTEXT.md` with the task description and requirements:
  ```markdown
  # Task Description

  ## Overview
  [Brief description of the task to be implemented]

  ## Requirements
  - [Requirement 1]
  - [Requirement 2]
  - [Requirement 3]

  ## Technical Context
  [Any relevant technical details, constraints, or existing system information]

  ## Considerations
  [Special considerations, challenges, or trade-offs to be addressed]
  ```
- Run thinktank-wrapper with the plan template (with the maximum timeout in the bash tool used to invoke it):
    ```bash
    thinktank-wrapper --template plan --inject PLAN-CONTEXT.md --model-set high_context --include-philosophy --include-glance ./
    ```
- Review the generated output directory and use the synthesis file as the basis for `PLAN.md`

## 3. Checkout Branch
- Check out a branch for completing all of the work in the generated `PLAN.md`.
