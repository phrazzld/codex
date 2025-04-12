# REFACTOR

> Execute each task in the order given to generate a refactor plan for the codebase.

## 1. Create task.md

Create a new file called `task.md`.

Copy the content from `prompts/refactor.md` into `task.md`.

## 2. Run architect with the task file

Run the following command from the project root:

```bash
# Find the top ten most relevant files for additional context
# Run architect with all the context files
architect --instructions task.md --output-dir architect_output --model gemini-2.5-pro-exp-03-25 --model gemini-2.0-flash docs/philosophy/ [top-ten-relevant-files]

# Review and Synthesize
# 1. Review all files in the architect_output directory (typically gemini-2.5-pro-exp-03-25.md and gemini-2.0-flash.md)
# 2. ***Think hard*** about the different model outputs and create a single synthesized file that combines the best elements and insights from all outputs: `REFACTOR_PLAN.md`
```

This will analyze the codebase and generate a refactor plan in `REFACTOR_PLAN.md`.

If you encounter an error, write the error to a persistent logfile. Then try again.

## 3. Read the refactor plan

Go to the `REFACTOR_PLAN.md` file and read the generated plan to understand the proposed refactoring steps and recommendations.
