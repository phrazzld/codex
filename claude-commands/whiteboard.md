# WHITEBOARD

## GOAL
Generate creative technical brainstorming for a GitHub issue, exploring multiple approaches from conventional to innovative "cut the Gordian knot" solutions.

## 1. Select Issue
- List GitHub issues to select one for brainstorming:
  ```bash
  gh issue list --state open --json number,title,labels --limit 20
  ```
- View details of the selected issue:
  ```bash
  gh issue view [issue-number] --json number,title,body,labels
  ```

## 2. Create Context
- Create `WHITEBOARD-CONTEXT.md` containing the selected GitHub issue details

## 3. Generate Ideas
- Run the following command with the maximum timeout in the bash tool:
  ```bash
  thinktank-wrapper --template whiteboard --inject WHITEBOARD-CONTEXT.md --model-set high_context --include-philosophy --include-glance ./
  ```
- Thoroughly review all files in the generated output directory, not just the synthesis file
- If the synthesis file appears truncated or incomplete, manually analyze all output files

## 4. Update Issue
- Consider commenting on the GitHub issue with the brainstorming results:
  ```bash
  gh issue comment [issue-number] --body "[Summary of brainstorming results]"
  ```