# SCOPE

## GOAL
Analyze and right-size `TODO.md`, breaking it into manageable pieces if needed to avoid unwieldy pull requests.

## FLOW

### 1. Gather Context
- Read PLAN.md
- Read TODO.md
- Find relevant development philosophy files

### 2. Generate Scope Analysis with Thinktank
- Run thinktank-wrapper with the scope template (with the maximum timeout in the bash tool used to invoke it):
  ```bash
  thinktank-wrapper --template scope --model-set all --include-philosophy --include-glance PLAN.md TODO.md
  ```
- Review the generated output directory and use the synthesis file to create `SCOPE-RESULT.md`

### 3. Execute Splitting (If Needed)
- If SCOPE-RESULT.md recommends splitting:
  - Create SCOPE-SPLIT.md prompt with:
    ```markdown
    # SCOPE SPLITTING

    Based on the scope analysis, split TODO.md into multiple focused todo files.

    ## Source Plan
    [Include PLAN.md content]

    ## Source TODO
    [Include TODO.md content]

    ## Scope Analysis Results
    [Include SCOPE-RESULT.md content]

    ## Output Requirements
    1. Create separate plan files (TODO-1.md, TODO-2.md, etc.)
    2. Each todo file must be independently implementable
    ```
  - Run thinktank-wrapper for splitting (with the maximum timeout in the bash tool used to invoke it):
    ```bash
    thinktank-wrapper --instructions SCOPE-SPLIT.md --model-set all --include-philosophy --include-glance PLAN.md TODO.md SCOPE-RESULT.md
    ```
  - Parse thinktank output to extract todo files
  - Write each plan to `TODO-{n}.md` files
  - Rename original to `TODO-ORIGINAL.md`
  - Create `TODO-INDEX.md` listing all generated plans

### 4. Review & Clean Up
- Present results to user
  - If not split: "TODO scope is appropriate - proceed with ticket command"
  - If split: "TODO split into N parts: [list file names]"
- Remove temporary files (SCOPE-SPLIT.md)