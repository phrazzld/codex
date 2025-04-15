# RESOLVE

> Execute each step in sequence to systematically resolve git merge conflicts.

## 1. ANALYZE MERGE CONFLICT

- **Goal:** Thoroughly understand the nature and scope of the current git merge conflict.
- **Actions:**
    - **Check Status:** Run `git status` to identify conflicted files and confirm we're in a merge state.
    - **Analyze Conflict Scale:** Run `git diff --check` to get a clearer view of conflict markers in the code.
    - **Understand Context:** Run `git log --merge -p <conflicted_file>` on each conflicted file to understand the changes from both branches.
    - ***Think hard*** to identify and document the core conflict pattern:
        - **Simple Text Conflicts:** Direct text overlaps
        - **Semantic Conflicts:** Non-overlapping text but logical incompatibilities
        - **Structural Conflicts:** Moved code or refactored elements
        - **Dependency Conflicts:** Changes to related files or interfaces

## 2. PLAN CONFLICT RESOLUTION STRATEGY

- **Goal:** Determine a systematic, cautious approach to resolving each conflicted file while preserving intended functionality from both sources.
- **Actions:**
    - **Review Standards:** Locate and review project documentation for coding standards (`docs/DEVELOPMENT_PHILOSOPHY.md`) to ensure your resolution adheres to project conventions.
    - **Identify Dependencies:** Determine if conflicts span multiple files that must be resolved as a cohesive unit.
    - **Prioritize Approach:** Explicitly decide on the appropriate resolution approach for each file:
        - **Keep Ours:** When our changes should clearly take precedence
        - **Keep Theirs:** When the incoming changes should clearly take precedence
        - **Combine Changes:** When both sets of changes must be preserved (most common)
        - **Complete Rewrite:** When neither version works and a new solution is needed
    - **Document Plan:** For complex conflicts, outline a specific plan for each affected file. For simple conflicts, a general approach is sufficient.

## 3. RESOLVE CONFLICTS FILE-BY-FILE

- **Goal:** Methodically resolve each conflict, ensuring functionality, standards compliance, and intent preservation.
- **Actions:**
    - For each conflicted file:
        - **Inspect:** Open the file and review the conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) to understand the specific differences.
        - **Consider Context:** Re-examine the broader purpose of these changes from both branches.
        - **Edit Cautiously:** ***Think carefully*** and manually edit the file to resolve each conflict according to the strategy determined in Step 2.
            - Keep the version that best preserves the project's standards and intended functionality
            - When combining changes, ensure logical flow is maintained
            - Watch for subtle inconsistencies like variable name changes, indentation, or formatting
        - **Remove Markers:** Ensure all conflict markers are removed.
        - **Verify Syntax:** Check that the file is syntactically valid (no incomplete statements, matching brackets/parentheses).
    - **Document Decisions:** For significant or non-obvious resolutions, document your reasoning as a comment in the code.

## 4. VALIDATE RESOLUTION

- **Goal:** Ensure the merged code is valid, functional, and preserves the intended behavior from both branches.
- **Actions:**
    - **Syntax Check:** For each resolved file, verify that the basic syntax is correct (e.g., run linters if available).
    - **Mark Resolved:** Run `git add <file>` for each successfully resolved file.
    - **Check Remaining:** Run `git status` to confirm all conflicts have been addressed.
    - **Test Compilation/Build:** If applicable, run a build or compilation step to verify basic integrity.
    - **Run Tests:** If a test suite exists, run it to verify functionality is preserved.
    - **Manual Verification:** For critical components, manually verify the functionality works as expected.

## 5. FINALIZE MERGE

- **Goal:** Complete the merge process and document the resolution for future reference.
- **Actions:**
    - **Final Check:** Run a final `git status` to ensure all conflicts are resolved and files are staged.
    - **Commit Resolution:** Execute `git commit` to finalize the merge. If the merge was particularly complex:
        - Use a detailed commit message that explains the conflict resolution approach
        - Note any important decisions made or compromises accepted
        - Reference relevant issue numbers or pull requests
    - **Push Changes:** If appropriate, push the changes to the remote repository.
    - **Cleanup (Optional):** If temporary branches were created for the merge process, clean them up.

## 6. POST-MERGE VALIDATION

- **Goal:** Perform a final validation to ensure the codebase is stable after the merge.
- **Actions:**
    - **Comprehensive Tests:** Run the complete test suite to verify overall system integrity.
    - **Code Review:** If the merge resolution was complex, consider requesting a review from a team member familiar with both sets of changes.
    - **Documentation:** For significant merges with complex resolution strategies, consider documenting the process in a project wiki or documentation for future reference.