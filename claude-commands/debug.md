# DEBUG
## 1. Initialize Investigation
- **Goal:** Set up the workspace and document the known problem details.
- **Actions:**
    - Read `BUG.MD` thoroughly. Ensure you understand the reported problem, reproduction steps, expected vs. actual behavior, and any mentioned components or environment details. (If `BUG.MD` is critically unclear, report this immediately and stop).
    - Create a new file named `BUGFIXPLAN.md`.
    - Populate `BUGFIXPLAN.md` with initial sections:
        - `Bug Description:` (Copied/Summarized from `BUG.MD`)
        - `Reproduction Steps:` (Copied from `BUG.MD`)
        - `Expected Behavior:` (From `BUG.MD`)
        - `Actual Behavior:` (From `BUG.MD`)
        - `Key Components/Files Mentioned:` (From `BUG.MD`)
        - `Hypotheses:` (Initially empty)
        - `Test Log:` (Initially empty)
        - `Root Cause:` (Initially empty)
        - `Fix Description:` (Initially empty)
        - `Status:` Investigating
    - Add `BUGFIXPLAN.md` to Git tracking (`git add BUGFIXPLAN.md`).

## 2. Formulate Initial Hypotheses
- **Goal:** Generate plausible explanations for the bug based on available information.
- **Actions:**
    - Analyze the bug details and involved components (`BUGFIXPLAN.md`).
    - Examine the relevant code sections identified. Consider recent changes in Git history for these files (`git log`).
    - ***Think hard*** to brainstorm a list of potential root causes (at least 2-3 if possible).
    - For each hypothesis, briefly note:
        - The potential cause.
        - Reasoning (Why this might cause the observed behavior).
        - A quick validation idea (A simple test/check).
    - Record these under the `Hypotheses:` section in `BUGFIXPLAN.md`.

## 3. Design and Execute Tests
- **Goal:** Systematically test the hypotheses to gather evidence.
- **Actions:**
    - Retrieve the debugging prompt template from `prompts/debug.md`.
    - Prioritize hypotheses (e.g., start with the most likely or easiest to test).
    - For the current hypothesis, design a specific, minimal test to validate or refute it. Define clearly in `BUGFIXPLAN.MD` under `Test Log:`:
        - `Hypothesis Tested:` (Link back to the hypothesis)
        - `Test Description:` (What action will be performed? e.g., Add logging here, run function X with input Y, check value Z).
        - `Execution Method:` (How will the test be run? e.g., Run existing unit test, execute script, use debugger, manual code execution).
        - `Expected Result (if hypothesis is true):`
        - `Expected Result (if hypothesis is false):`
    - Execute the test using the specified method.
    - Record the `Actual Result:` and `Conclusion:` (Hypothesis supported, refuted, or inconclusive?) in the `Test Log:` entry in `BUGFIXPLAN.md`.

## 4. Analyze Results and Refine
- **Goal:** Interpret test results and update understanding, iterating until the root cause is identified.
- **Actions:**
    - Create a debug request file `DEBUG-REQUEST.md` by:
        - Copying the content from `prompts/debug.md` as the base template
        - Adding current bug analysis state at the top (bug description, current hypotheses, test results)
    - Run architect with the debug request:
        ```bash
        architect --instructions DEBUG-REQUEST.md --output-dir architect_output --model gemini-2.5-pro-preview-03-25 --model gemini-2.5-pro-exp-03-25 --model gemini-2.0-flash docs/philosophy/ [relevant-files-to-bug]
        ```
        - **Review and Synthesize:**
            1. Review all files in the architect_output directory
            2. ***Think hard*** about the different model outputs and create a single synthesized file that combines the best elements and insights from all outputs: `DEBUG-ANALYSIS.md`
    - Review architect's analysis in `DEBUG-ANALYSIS.md` and:
        - Update the status of tested hypotheses in the `Hypotheses:` section of `BUGFIXPLAN.md`.
        - If the root cause is not yet clear:
            - ***Think hard*** based on the evidence gathered.
            - Refine existing hypotheses or formulate new ones based on the results. Record these in `BUGFIXPLAN.md`.
            - Return to Step 3 to test the next prioritized/refined hypothesis.
        - If a hypothesis is strongly supported and appears to explain the *entire* bug behavior described in `BUG.MD`:
            - Proceed to Step 5.

## 5. Implement and Verify Fix
- **Goal:** Correct the code based on the identified root cause and confirm the fix works.
- **Actions:**
    - Document the confirmed `Root Cause:` in `BUGFIXPLAN.md`.
    - Design the code fix. Describe the planned `Fix Description:` in `BUGFIXPLAN.md`.
    - Apply the code changes necessary to implement the fix.
    - **Add Inline Code Comments:** Near the fix, add comments explaining: `// BUGFIX: [Brief Bug Summary], CAUSE: [Root Cause], FIX: [Fix Description]`. Consider adding a `// PREVENTION:` note if an obvious way to avoid this class of bug exists.
    - **Verify Rigorously:**
        - Execute the original `Reproduction Steps:` from `BUG.MD`/`BUGFIXPLAN.md`. Confirm the `Actual Behavior:` now matches the `Expected Behavior:`.
        - Run all relevant automated tests (unit, integration). Ensure they pass. If the fix required test changes, ensure they are logical and also committed.
    - If verification fails, update `BUGFIXPLAN.md`, revert the fix attempt, and return to Step 4 to re-evaluate the root cause or fix approach.

## 6. Finalize and Commit
- **Goal:** Commit the validated fix and updated documentation.
- **Actions:**
    - Update the `Status:` in `BUGFIXPLAN.md` to `Resolved`.
    - Stage all changed code files, test files (if any), and the updated `BUGFIXPLAN.md` (`git add`).
    - Review the final diff (`git diff --staged`).
    - Commit using the **Conventional Commits** format:
        - Message: `fix: [Concise description of the fix, e.g., resolve issue causing incorrect calculation]`
        - Body: Include a reference to the bug report/plan (e.g., `Fixes issue described in BUGFIXPLAN.md (or reference BUG.md/ticket # if applicable). Root cause identified as [...].`)
    - Report "Fix committed successfully."

## (Escape Clause) Handle Blockers
- **Action:** If at any point (especially during Step 3/4/5) you are unable to make progress, cannot identify a root cause after multiple iterations, or cannot implement/verify a fix:
    - Update the `Status:` in `BUGFIXPLAN.md` to `BLOCKED`.
    - Add a detailed entry in `BUGFIXPLAN.md` under a new `Blocker Details:` section, explaining what was attempted, what failed, and why you are stuck.
    - Report clearly: "DEBUG process BLOCKED. See `BUGFIXPLAN.md` for details. Manual assistance required."
    - **Stop** the debugging process.
