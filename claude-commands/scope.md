# SCOPE

## GOAL
Analyze and right-size PLAN.md, breaking it into manageable pieces if needed to avoid oversized tasks, excessive TODO files, and unwieldy pull requests.

## USAGE
```
/scope
```

## FLOW

### 1. Gather Context
- Read PLAN.md
- Find relevant development philosophy files

### 2. Analyze Plan Scope
- Create SCOPE-ANALYSIS.md with pattern:
  ```markdown
  # SCOPE ANALYSIS
  
  Analyze the complexity and scope of PLAN.md and determine if it should be broken into multiple smaller plans.
  
  ## Context
  - PLAN.md contains [feature/task description]
  
  ## Scope Criteria
  - Size: total steps, tasks, or changes required
  - Cohesion: how tightly coupled the changes are
  - Dependencies: number of interrelated components changed together
  - Testing complexity: scope of testing required
  - Review burden: how difficult this would be to meaningfully review
  - Deployment risk: potential for regression or issues
  
  ## Analysis Instructions
  1. Determine if PLAN.md should be split based on the scope criteria above
  2. If splitting is recommended, identify logical boundaries for separation
  3. Define clear, focused sub-plans with minimal interdependencies
  4. Ensure each sub-plan is independently implementable and testable
  ```

### 3. Generate Scope Analysis with Thinktank
- Run thinktank:
  ```bash
  thinktank --instructions SCOPE-ANALYSIS.md --synthesis-model gemini-2.5-pro-preview-03-25 --model gemini-2.5-pro-preview-03-25 --model gpt-4.1 --model o4-mini PLAN.md [relevant development philosophy files]
  ```
- Copy synthesis file to create analysis:
  ```bash
  cp thinktank_output/gemini-2.5-pro-preview-03-25-synthesis.md SCOPE-RESULT.md
  ```
- Handle errors (log, retry once, stop). Report success.

### 4. Execute Plan Splitting (If Needed)
- If SCOPE-RESULT.md recommends splitting:
  - Create SCOPE-SPLIT.md prompt with:
    ```markdown
    # SCOPE SPLITTING
    
    Based on the scope analysis, split PLAN.md into multiple focused plan files.
    
    ## Source Plan
    [Include PLAN.md content]
    
    ## Scope Analysis Results
    [Include SCOPE-RESULT.md content]
    
    ## Output Requirements
    1. Create separate plan files (PLAN-1.md, PLAN-2.md, etc.)
    2. Each plan file must be independently implementable
    3. Each must include a complete plan structure (introduction, context, approach, steps)
    4. Each must maintain proper markdown formatting
    5. Ensure all original content is preserved across the split plans
    6. Add a "Dependency Notes" section to each plan if there are cross-dependencies
    ```
  - Run thinktank for splitting:
    ```bash
    thinktank --instructions SCOPE-SPLIT.md --synthesis-model gemini-2.5-pro-preview-03-25 --model gemini-2.5-pro-preview-03-25 --model gpt-4.1 --model o4-mini PLAN.md SCOPE-RESULT.md
    ```
  - Parse thinktank output to extract plan files
  - Write each plan to PLAN-{n}.md files
  - Rename original to PLAN-ORIGINAL.md
  - Create PLAN-INDEX.md listing all generated plans

### 5. Review & Clean Up
- Present results to user
  - If not split: "Plan scope is appropriate - proceed with ticket command"
  - If split: "Plan split into N parts: [list file names]. Run ticket command on each plan separately."
- Remove temporary files (SCOPE-ANALYSIS.md, SCOPE-SPLIT.md, thinktank_output/)