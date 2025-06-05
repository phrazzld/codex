# ALIGN

## GOAL
Analyze the codebase against our development philosophy and leyline documents and generate GitHub issues to improve alignment.

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
  Analyze the codebase against our development philosophy and leyline documents and generate items to improve alignment.
  ```

## 2. Generate Philosophy-Aligned Improvement Items
- **Think very hard** about the codebase alignment with our development philosophy and leyline documents:
  - Read and internalize `DEVELOPMENT_PHILOSOPHY.md`, all language-specific appendices, and leyline documents
  - Systematically analyze each major component/module against our core principles:
    * Simplicity and modularity
    * Testability and explicit contracts
    * Maintainability and clarity
    * Automation and tooling adherence
  - Consider the context from `ALIGN-CONTEXT.md` and existing GitHub issues
  - Identify specific misalignments, anti-patterns, or areas for improvement
  - For each finding, determine:
    * The specific principle being violated
    * The impact on the codebase
    * A concrete improvement strategy
    * Priority level (high/medium/low)
- Create GitHub issues for each alignment item identified, with appropriate labels and priorities based on your assessment of each item
