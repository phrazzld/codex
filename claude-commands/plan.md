# PLAN

## GOAL
Generate a detailed implementation plan for a prioritized task, with focus on architecture, approach tradeoffs, implementation steps, testing strategy, and risk mitigation.

## 1. Select & Scope Task
- Fetch all open GitHub issues and examine their details:
  ```bash
  # Get all open issues
  gh issue list --state open --json number,title,labels,assignees --limit 100
  
  # After selecting an issue number, view its complete details
  gh issue view [issue-number] --json number,title,body,labels,assignees,milestone
  ```
- Select an important issue ready for implementation, prioritizing those with higher priority labels if available.

## 2. Generate Plan with Thinktank
- Create `PLAN-CONTEXT.md` with the selected GitHub issue details:
  ```markdown
  # Task Description

  ## Issue Details
  [Issue title, number and URL]

  ## Overview
  [Brief description of the issue from body]

  ## Requirements
  [Extract requirements from issue description and/or labels]

  ## Technical Context
  [Any relevant technical details, constraints, or existing system information from the issue]

  ## Related Issues
  [Any linked or referenced issues]
  ```
- Run thinktank-wrapper with the plan template (with the maximum timeout in the bash tool used to invoke it):
    ```bash
    thinktank-wrapper --template plan --inject PLAN-CONTEXT.md --model-set high_context --include-philosophy --include-glance ./
    ```
- Review the generated output directory and use the synthesis file as the basis for `PLAN.md`

## 3. Checkout Branch
- Create and check out a branch for implementing the selected GitHub issue, following the repository's branch naming conventions.
