# EXECUTE

## 1. Select & Assess Task
- Scan `TODO.MD` for `[ ]` tasks whose `Depends On:` Task IDs are `[x]`. Select first match.
- Record Task ID & Title. Mark task `[~]` in `TODO.MD`.
- Assess Complexity: Simple (small, clear, single file) vs. Complex (multi-file, complex logic, uncertainty).
- Route: Simple -> Section 2 (Fast Track), Complex -> Section 3 (Comprehensive).

## 2. FAST TRACK (Simple Tasks)
- **2.1 Plan:** Create `<sanitized-task-title>-PLAN.md` (Task ID/Title, brief approach).
- **2.2 Test (Optional):** Write minimal happy path tests only.
- **2.3 Implement:** Write code directly per standards.
- **2.4 Finalize:** Run checks (lint, test), fix issues. Update task `[x]` in `TODO.MD`. Commit.

## 3. COMPREHENSIVE TRACK (Complex Tasks)
- **3.1 Prep Prompt:** Create `<sanitized-task-title>-TASK.md` (copy `prompts/execute.md`, add Task ID/details).
- **3.2 Gen Plan:**
    - Find top 10 relevant context files.
    - Run architect: `architect --instructions <sanitized-task-title>-TASK.md --output-dir architect_output --model gemini-2.5-pro-exp-03-25 --model gemini-2.0-flash --model gemini-2.5-pro-preview-03-25 DEVELOPMENT_PHILOSOPHY.md [top-ten-relevant-files]`
    - Review outputs & ***Think hard*** to synthesize into `<sanitized-task-title>-PLAN.md`.
    - Handle errors (log, retry). Stop if unresolvable.
    - Review plan against `DEVELOPMENT_PHILOSOPHY.md`. Remove TASK file.
- **3.3 Write Tests:** Write failing tests (happy path, critical edge cases) per `DEVELOPMENT_PHILOSOPHY.md` (minimal mocking, test behavior). Ensure tests fail initially.
- **3.4 Implement:** Write minimal code per plan to make tests pass. Adhere to standards.
- **3.5 Refactor:** Ensure tests pass. ***Think hard*** & evaluate code against `DEVELOPMENT_PHILOSOPHY.md`. Apply minimal refactoring needed for compliance (simplicity, architecture, quality, testability, docs). Keep tests passing.
- **3.6 Verify Tests:** Run all tests. Ensure pass. Fix implementation if needed (don't modify tests unless flawed).
- **3.7 Finalize:** Run all checks (lint, build, full test suite), fix failures. Update task `[x]` in `TODO.MD`. Remove PLAN file. Add, Commit, Push.

