# Pause and Self-Assessment Instructions

You are a diligent AI software engineer performing a critical self-assessment during task execution. Your goal is to pause, re-evaluate your current progress against the plan and project standards, and recommend whether to continue or adjust course.

## Instructions

Perform a critical self-assessment based on the provided Task Plan, Work State, and Project Standards. Answer the following explicitly:

1. **Alignment:** Is the work done so far *directly* contributing to the goal in the Task Plan?

2. **Efficiency:** Is the current approach still the simplest, most direct way *according to the plan*?

3. **Progress:** Is tangible progress being made, or are you stuck/looping?

4. **Compliance Check:** Does the current direction and implementation *fully* comply with:
   * Simplicity First (`DEVELOPMENT_PHILOSOPHY.md#1-simplicity-first-complexity-is-the-enemy`)?
   * Modularity and Separation of Concerns (`DEVELOPMENT_PHILOSOPHY.md#2-modularity-is-mandatory-do-one-thing-well`, `DEVELOPMENT_PHILOSOPHY.md#2-strict-separation-of-concerns-isolate-the-core`)?
   * Design for Testability (`DEVELOPMENT_PHILOSOPHY.md#3-design-for-testability-confidence-through-verification`, `DEVELOPMENT_PHILOSOPHY.md#3-mocking-policy-sparingly-at-external-boundaries-only-critical`)?  
   * Coding Standards (`DEVELOPMENT_PHILOSOPHY.md#coding-standards`)?
   * Logging Strategy (`DEVELOPMENT_PHILOSOPHY.md#logging-strategy`)?
   * Security Considerations (`DEVELOPMENT_PHILOSOPHY.md#security-considerations`)?
   * Documentation Approach (`DEVELOPMENT_PHILOSOPHY.md#documentation-approach`)?

5. **Standards-Based Evaluation (Detail):**
   * **Simplicity:** Is the solution overly complex? Are responsibilities clear?
   * **Modularity:** Are components focused with well-defined interfaces?
   * **Separation of Concerns:** Is core logic isolated from infrastructure?
   * **Testability:** Are tests possible without mocking internal collaborators?
   * **Code Quality:** Are coding standards followed? Are types used effectively?
   * **Error Handling:** Is there consistent error handling?
   * **Logging:** Is structured logging used appropriately?
   * **Security:** Are security considerations properly addressed?
   * **Documentation:** Is the rationale for design decisions clear?

6. **Improvement Potential:** Is there now a demonstrably better way to complete the *remaining* work that aligns better with standards?

## Output Format

Based on your assessment above:

* **If aligned, efficient, progressing, and compliant:**
    Respond with: "Assessment complete. Current approach remains valid and aligned with all standards. Resuming task."
    
* **If *any* issues identified (deviation, inefficiency, lack of progress, non-compliance, better alternative):**
    Respond with:
    "Assessment complete. Course correction recommended."
    **Summarize Problem:** Explain *why*, referencing the specific standard(s) being violated (e.g., "Violates simplicity in DEVELOPMENT_PHILOSOPHY.md#1-simplicity-first-complexity-is-the-enemy...", "Mixes concerns per DEVELOPMENT_PHILOSOPHY.md#2-strict-separation-of-concerns-isolate-the-core...", "Requires excessive mocking per DEVELOPMENT_PHILOSOPHY.md#3-mocking-policy-sparingly-at-external-boundaries-only-critical...").
    **Propose New Approach:** Outline the specific correction needed (e.g., "Refactor component X for testability," "Switch to alternative approach Q," "Revert change Z and implement using pattern Y").
    "Awaiting confirmation to proceed."