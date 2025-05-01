# DEBUG

## 1. Init Investigation & Identify Task
- Read `BUG.MD`. Stop if critically unclear.
- Identify related `Original Task ID: TXXX` from `TODO.md`. Note if none.
- Create `BUGFIXPLAN.md` (Sections: Bug Desc, Repro, Expected, Actual, Components, Hypotheses, Test Log, Root Cause, Fix Desc, Status: Investigating).
- Create `DEBUG-REQUEST.md` (copy prompt template, add bug details, `Original Task ID`).
- Identify relevant development philosophy files
- Run thinktank for initial analysis:
    ```bash
    thinktank --instructions DEBUG-REQUEST.md $THINKTANK_HIGH_CONTEXT_MODELS $THINKTANK_SYNTHESIS_MODEL $(find_philosophy_files) $(find_glance_files)
    ```
- Copy synthesis file to `DEBUG-ANALYSIS.md`

## 2. Formulate Initial Hypotheses
- Analyze bug details, components, `DEBUG-ANALYSIS.md`, code, git history.
- ***Think hard*** & brainstorm potential root causes.
- Keep the program's purpose in mind and strive for the highest quality maintainable solutions while avoiding overengineering.
- Record hypotheses (cause, reasoning, validation idea) in `BUGFIXPLAN.md`.

## 3. Generate Investigation Tasks in TODO.md
- Decide next logical debug step (e.g., test hypothesis, gather data).
- Create `DEBUG-TASKGEN-REQUEST.md`. Instruct AI (via prompt) to:
    - Generate new, atomic tasks for `TODO.md` for next debug steps (e.g., "Test Hypo X", "Analyze Y", "Implement Fix Z").
    - Assign new unique Task IDs (sequential).
    - Format tasks correctly (ID, Title, Action, `Depends On:` using IDs, `AC Ref: None`).
    - Final "Verify Fix" task's `Action:` should mark `Original Task ID: TXXX` as `[x]`.
- Run thinktank for task generation:
    ```bash
    thinktank --instructions DEBUG-TASKGEN-REQUEST.md $THINKTANK_ALL_MODELS $THINKTANK_SYNTHESIS_MODEL $(find_philosophy_files) BUGFIXPLAN.md DEBUG-ANALYSIS.md
    ```
- Review tasks from synthesis file
- Insert tasks into `TODO.md` (logically after `Original Task ID`), maintaining consistent formatting and proper dependency references.
- Remove `DEBUG-TASKGEN-REQUEST.md`.
- Report: "Generated debug tasks [New Task IDs] in TODO.md related to original task [Original Task ID]. Proceed via /execute."
- **Stop** `/debug`.

## (Escape Clause) Handle Blockers
- If unable to formulate hypotheses or generate tasks:
    - Update `Status: BLOCKED` in `BUGFIXPLAN.md`. Add `Blocker Details`.
    - Report: "DEBUG process BLOCKED. See `BUGFIXPLAN.md`. Manual assistance required."
    - **Stop**.

