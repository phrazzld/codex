# ALIGN

## GOAL
Analyze the codebase against our development philosophy and generate GitHub issues to improve alignment.

## 1. Create Context File
- Fetch current GitHub issues to understand existing tasks:
  ```bash
  gh issue list --state open --json number,title,body,labels --limit 100
  ```
- Create `ALIGN-CONTEXT.md` with the following content:
  ```markdown
  # Philosophy Alignment Context

  ## Current Issues
  [Include output from GitHub issues list]

  ## Request
  Analyze the codebase against our development philosophy and generate items to improve alignment.
  ```

## 2. Generate Philosophy-Aligned Improvement Items
- Run thinktank-wrapper with the align template (with the maximum timeout in the bash tool used to invoke it):
  ```bash
  thinktank-wrapper --template align --inject ALIGN-CONTEXT.md --model-set high_context --include-philosophy --include-glance ./
  ```
- Thoroughly review all files in the generated output directory, not just the synthesis file
- If the synthesis file appears truncated or incomplete, manually analyze all output files and synthesize the information
- Create GitHub issues for each alignment item identified, with appropriate labels and priorities based on your assessment of each item
