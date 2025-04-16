# BREATHE

## 1. Pause & Reset
- Clear immediate assumptions.

## 2. Re-Ground Context
- Identify current Task Title from `TODO.MD`.
- Re-read corresponding `<task-title>-PLAN.md`.
- Re-read relevant `TODO.MD` section/AC Ref.
- Review `DEVELOPMENT_PHILOSOPHY.md` principles related to current issue.
- Briefly review original `PLAN.MD` section if needed.

## 3. Critical Self-Assessment
- Create `breathe-assessment.md`.
- Copy content from `docs/prompts/breathe.md`.
- Add context: `## Task Context\n- **Task:** [Current task title]\n- **Work State:** [Summary of progress/challenges]`
- Run architect:
    ```bash
    architect --instructions breathe-assessment.md --output-dir architect_output --model gemini-2.5-pro-exp-03-25 --model gemini-2.0-flash --model gemini-2.5-pro-preview-03-25 DEVELOPMENT_PHILOSOPHY.md [relevant-files-to-task]
    ```
- **Review & Synthesize:**
    1. Review `architect_output` files.
    2. ***Think hard*** & synthesize into `BREATHE_RESULT.md`.
- Review `BREATHE_RESULT.md`.

## 4. Report Findings & Recommendation
- Based *only* on Step 3 results:
    - **Scenario A: Stay Course.** If aligned, efficient, progressing, compliant:
        - Report: "Assessment complete. Approach valid. Resuming task."
        - (Proceed).
    - **Scenario B: Course Correction.** If issues (deviation, inefficiency, stuck, non-compliance, design flaws, better alternative):
        - Report: "Assessment complete. Course correction recommended."
        - Summarize Problem (reference specific `DEVELOPMENT_PHILOSOPHY.md` violation).
        - Propose New Approach (e.g., "Propose refactor X," "Suggest alternative Q"). Consider `/consult`.
        - Report: "Awaiting confirmation."
        - (Wait for confirmation).

