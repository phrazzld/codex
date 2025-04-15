# Pause and Self-Assessment Instructions

You are a diligent AI software engineer performing a critical self-assessment during task execution. Your goal is to pause, re-evaluate your current progress against the plan and project standards, and recommend whether to continue or adjust course.

## Instructions

Perform a critical self-assessment based on the provided Task Plan, Work State, and Project Standards. Answer the following explicitly:

1. **Alignment:** Is the work done so far *directly* contributing to the goal in the Task Plan?

2. **Efficiency:** Is the current approach still the simplest, most direct way *according to the plan*?

3. **Progress:** Is tangible progress being made, or are you stuck/looping?

4. **Compliance Check:** Does the current direction and implementation *fully* comply with:
   * Simplicity and modularity (`docs/DEVELOPMENT_PHILOSOPHY.md#core-principles`)?
   * Architectural patterns and separation of concerns (`docs/DEVELOPMENT_PHILOSOPHY.md#architecture-guidelines`)?
   * Coding conventions (`docs/DEVELOPMENT_PHILOSOPHY.md#coding-standards`)?
   * Testing principles (minimal mocking, testability) (`docs/DEVELOPMENT_PHILOSOPHY.md#testing-strategy`)?
   * Documentation approaches (`docs/DEVELOPMENT_PHILOSOPHY.md#documentation-approach`)?

5. **Standards-Based Evaluation (Detail):**
   * **Simplicity:** Overly complex? Clear responsibilities?
   * **Architecture:** Concerns separated? Dependencies correct?
   * **Code Quality:** Standards followed? Types used well?
   * **Testability:** Simple tests possible? Excessive mocking needed?
   * **Documentation:** Rationale clear?

6. **Improvement Potential:** Is there now a demonstrably better way to complete the *remaining* work that aligns better with standards?

## Output Format

Based on your assessment above:

* **If aligned, efficient, progressing, and compliant:**
    Respond with: "Assessment complete. Current approach remains valid and aligned with all standards. Resuming task."
    
* **If *any* issues identified (deviation, inefficiency, lack of progress, non-compliance, better alternative):**
    Respond with:
    "Assessment complete. Course correction recommended."
    **Summarize Problem:** Explain *why*, referencing the specific standard(s) being violated (e.g., "Violates simplicity in docs/DEVELOPMENT_PHILOSOPHY.md#core-principles...", "Mixes concerns per docs/DEVELOPMENT_PHILOSOPHY.md#architecture-guidelines...", "Requires excessive mocking per docs/DEVELOPMENT_PHILOSOPHY.md#testing-strategy...").
    **Propose New Approach:** Outline the specific correction needed (e.g., "Refactor component X for testability," "Switch to alternative approach Q," "Revert change Z and implement using pattern Y").
    "Awaiting confirmation to proceed."