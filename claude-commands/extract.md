# EXTRACT

## GOAL
Generate a detailed plan for extracting reusable functionality into independent components to improve maintainability, reusability, and adherence to code principles.

## 1. Run thinktank-wrapper
- Run thinktank-wrapper with the extract template (with the maximum timeout in the bash tool used to invoke it):
    ```bash
    thinktank-wrapper --template extract --model-set high_context --include-philosophy --include-glance ./
    ```
- Review the generated output directory and use the synthesis file to create `EXTRACT_PLAN.md`