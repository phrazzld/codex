# GORDIAN

## GOAL
Identify opportunities for radical simplification and creative destruction in the codebase through outside-the-box thinking, and create GitHub issues for the most promising opportunities.

## 1. Prepare Context
- Fetch current GitHub issues to understand existing tasks:
  ```bash
  gh issue list --state open --json number,title,body,labels --limit 100
  ```
- Create `GORDIAN-CONTEXT.md` with the following content:
  ```markdown
  # Radical Simplification Context

  ## Current Issues
  [Include output from GitHub issues list]

  ## Request
  Identify components in the codebase that could benefit from radical simplification or creative destruction.
  ```

## 2. Generate Gordian Opportunities
- Run the following command with the maximum timeout in the bash tool:
  ```bash
  thinktank-wrapper --template gordian --inject GORDIAN-CONTEXT.md --model-set high_context --include-philosophy --include-glance ./
  ```
- Thoroughly review all files in the generated output directory, not just the synthesis file
- If the synthesis file appears truncated or incomplete, manually analyze all output files and synthesize the information

## 3. Create GitHub Issues
- For each radical simplification opportunity, create a GitHub issue with appropriate details and labels

## DESCRIPTION
Inspired by Elon Musk's observation that "the number one mistake great engineers make is optimizing something that shouldn't exist" and the legend of Alexander cutting the Gordian Knot instead of untangling it. This command identifies components that:

1. Should be eliminated rather than optimized
2. Could be radically simplified with unconventional approaches
3. Are unnecessarily complex, tightly coupled, or difficult to maintain
4. Present opportunities to "cut the knot" rather than wrestling with its complexity

The output will provide specific, actionable recommendations for simplification and creative destruction.
