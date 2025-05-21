# GROOM

## GOAL
Create an organized, expanded, and prioritized issue backlog based on comprehensive codebase insights.

## 1. Prepare Context
- Fetch current GitHub issues to understand existing tasks and direction:
  ```bash
  gh issue list --limit 100 --json number,title,body,labels
  ```
- Identify all `glance.md` files in the codebase to gather architectural insights.
- Read `DEVELOPMENT_PHILOSOPHY.md` to anchor new backlog items in project principles.

## 2. Generate Enhanced GitHub Issues with Thinktank
- Create `GROOM-CONTEXT.md` with grooming criteria and current issues information:
  ```markdown
  # Backlog Grooming Context

  ## Current Issues
  [Include output from GitHub issues list]

  ## Grooming Goals
  - Prioritize items based on business value and technical dependencies
  - Identify missing tasks that should be added
  - Remove or modify outdated tasks
  - Ensure all tasks are clear, atomic, and actionable
  ```
- Run thinktank-wrapper with the groom template (with the maximum timeout in the bash tool used to invoke it):
  ```bash
  thinktank-wrapper --template groom --inject GROOM-CONTEXT.md --model-set high_context --include-philosophy --include-glance ./
  ```
- Review the generated output directory and use the synthesis file to update GitHub issues

## 3. Update GitHub Issues
- For each existing issue that needs modifications:
  ```bash
  gh issue edit [issue-number] --title "Updated Title" --body "Updated description" --add-label "priority:high,type:feature"
  ```
- For new issues identified during grooming:
  ```bash
  gh issue create --title "New Issue Title" --body "Detailed description" --label "priority:medium,type:feature,size:m"
  ```
- For issues that are no longer relevant:
  ```bash
  gh issue close [issue-number] --comment "Closing as no longer relevant: [explanation]"
  ```
