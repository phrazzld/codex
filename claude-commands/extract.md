# EXTRACT

## GOAL
Generate a detailed plan for extracting reusable functionality into independent components to improve maintainability, reusability, and adherence to code principles.

## 1. Prepare Context & Run thinktank-wrapper
- Create `EXTRACT-CONTEXT.md` with information about the component to extract:
  ```markdown
  # Component Extraction Context
  
  ## Target Component
  [Identify the component or functionality to be extracted]
  
  ## Current Implementation
  [Describe how the functionality is currently implemented]
  
  ## Extraction Goal
  [Explain the goal of the extraction (e.g., reusability, maintainability)]
  ```
- Run thinktank-wrapper with the extract template (with the maximum timeout in the bash tool used to invoke it):
    ```bash
    thinktank-wrapper --template extract --inject EXTRACT-CONTEXT.md --model-set high_context --include-philosophy --include-glance ./
    ```
- Review the generated output directory and use the synthesis file to create `EXTRACT_PLAN.md`