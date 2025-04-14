# BREATHE

## 1. PAUSE & RESET
- **Action:** Clear any short-term assumptions about the immediate next action.

## 2. RE-GROUND IN CONTEXT
- **Goal:** Re-establish verifiable context for the current task.
- **Actions:**
    - Identify the **exact** Task Title you are currently working on from `TODO.MD`.
    - Locate and carefully re-read the corresponding `<task-title>-PLAN.md` file.
    - Re-read relevant section(s) and AC Ref in `TODO.MD`.
    - **Review our standards documents relevant to the current issue:**
      - `CORE_PRINCIPLES.md` for fundamental design principles
      - `ARCHITECTURE_GUIDELINES.md` for structural patterns
      - `CODING_STANDARDS.md` for implementation practices
      - `TESTING_STRATEGY.md` for testing approaches
      - `DOCUMENTATION_APPROACH.md` for documentation practices
    - If necessary, briefly review the original `PLAN.MD` section.

## 3. CRITICAL SELF-ASSESSMENT
- **Goal:** Evaluate the *current state* of your work against the grounded context.
- **Actions:**
    - Create a file called `breathe-assessment.md`.
    - Copy the content from `prompts/breathe.md` to the file.
    - Add the current task context at the top:
        ```markdown
        ## Task Context
        - **Task:** [Current task title]
        - **Work State:** [Brief summary of current progress, approaches tried, and ongoing challenges]
        ```
    - Run the assessment through architect:
        ```bash
        architect --instructions breathe-assessment.md --output-dir architect_output --model gemini-2.5-pro-exp-03-25 --model gemini-2.0-flash docs/DEVELOPMENT_PHILOSOPHY.md [relevant-files-to-task]
        ```
        - **Review and Synthesize:**
            1. Review all files in the architect_output directory
            2. ***Think hard*** about the different model outputs and create a single synthesized file that combines the best elements and insights from all outputs: `BREATHE_RESULT.md`
    - Review the `BREATHE_RESULT.md` file.

## 4. REPORT FINDINGS & RECOMMENDATION
- **Goal:** Communicate the assessment results clearly and propose the next step.
- **Actions:** Based *only* on the answers from Step 3:
    - **Scenario A: Stay the Course.** If the work is aligned with plan, progressing efficiently, and compliant with all our standards:
        - State: "Assessment complete. Current approach remains valid and aligned with all standards. Resuming task."
        - (Proceed to resume).
    - **Scenario B: Course Correction Needed.** If there are issues with any of the following:
        - Deviation from plan
        - Inefficiency or complexity
        - Lack of progress
        - Non-compliance with any of our standards
        - Design flaws revealed through implementation
        - A demonstrably better alternative exists

        Then:
        - State: "Assessment complete. Course correction recommended."
        - **Summarize Problem:** Explain *why*, referencing the specific standard being violated (e.g., "Current approach violates simplicity principle in CORE_PRINCIPLES.md by introducing unnecessary abstraction," "Implementation mixes concerns contrary to ARCHITECTURE_GUIDELINES.md," "Current approach requires excessive mocking violating TESTING_STRATEGY.md," "Code doesn't follow type usage recommendations in CODING_STANDARDS.md").
        - **Propose New Approach:** Outline the proposed fix or alternative (e.g., "Propose refactoring component X for better testability before proceeding," "Suggest switching to alternative approach Q."). Consider invoking `propose-testable-refactor` or `consult` if appropriate.
        - State: "Awaiting confirmation to proceed."
        - (Do **not** proceed until confirmation).
