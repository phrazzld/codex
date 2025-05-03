# IDEATE

## GOAL
Generate innovative ideas for the project backlog by analyzing existing tasks and codebase context.

## 1. Prepare Context
- Read `BACKLOG.md` to understand current tasks and direction.
- Read `DEVELOPMENT_PHILOSOPHY.md` to understand the ideal general principles of the project's structure and implementation.
- Analyze codebase structure to identify areas for enhancement.

## 2. Generate Ideas with Thinktank
- Run thinktank-wrapper with the ideate template (with the maximum timeout in the bash tool used to invoke it):
  ```bash
  thinktank-wrapper --template ideate --model-set all --include-philosophy --include-glance ./
  ```
- Review the generated output directory and use the synthesis file to create `IDEAS.md`