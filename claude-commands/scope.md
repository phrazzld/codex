# SCOPE

## GOAL
Analyze and right-size `TODO.md`, breaking it into manageable pieces if needed to avoid unwieldy pull requests.

## FLOW

### 1. Gather Context
- Read PLAN.md
- Read TODO.md
- Find relevant development philosophy files

### 2. Analyze Plan Scope
- Create SCOPE-ANALYSIS.md with pattern:
  ```markdown
  # SCOPE ANALYSIS

  Analyze the complexity and scope of PLAN.md and TODO.md and determine if it should be broken into multiple smaller, more focused TODO files.

  ## Context
  - PLAN.md contains [feature/task description]
  - TODO.md contains [atomized task list to implement plan]

  ## Scope Criteria
  - Size: total steps, tasks, or changes required
  - Cohesion: how tightly coupled the changes are
  - Dependencies: number of interrelated components changed together
  - Testing complexity: scope of testing required
  - Review burden: how difficult this would be to meaningfully review
  - Deployment risk: potential for regression or issues

  ## Analysis Instructions
  1. Determine if TODO.md should be split based on the scope criteria above
  2. If splitting is recommended, identify logical boundaries for separation
  3. Define clear, focused sub-todos with minimal interdependencies
  4. Ensure each sub-todo is independently implementable and testable
  ```

### 3. Generate Scope Analysis with Thinktank
- Run thinktank-wrapper:
  ```bash
  thinktank-wrapper --model-set all --include-philosophy --include-glance --instructions SCOPE-ANALYSIS.md PLAN.md TODO.md
  ```
- Copy synthesis file to create `SCOPE-RESULT.md`

### 4. Execute Splitting (If Needed)
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
  - Run thinktank-wrapper for splitting:
    ```bash
    thinktank-wrapper --model-set all --include-philosophy --include-glance --instructions SCOPE-SPLIT.md PLAN.md TODO.md SCOPE-RESULT.md
    ```
  - Parse thinktank output to extract todo files
  - Write each plan to `TODO-{n}.md` files
  - Rename original to `TODO-ORIGINAL.md`
  - Create `TODO-INDEX.md` listing all generated plans

### 5. Review & Clean Up
- Present results to user
  - If not split: "TODO scope is appropriate - proceed with ticket command"
  - If split: "TODO split into N parts: [list file names]"
- Remove temporary files (SCOPE-ANALYSIS.md, SCOPE-SPLIT.md, thinktank_*/)

