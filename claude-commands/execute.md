# Claude‑Command.md – Ruthless Execute Loop

Your only goal: grab the next unblocked ticket, finish it, commit. No ceremony.

---

## 1 Pick a Ticket
1. Scan `TODO.md` top → bottom.
2. Select the first `[ ]` ticket whose `depends‑on:` list is empty or all `[x]`.
3. Flip its box to `[~]` and note **ID** + **Title**.

---

## 2 Classify
- **Simple** → single‑file change, clear logic, no design calls.
- **Complex** → multi‑file, tricky logic, risk ≥ high, or any ambiguity.
- **Think** about the details of this task, then classify it appropriately.

---

## 3 Simple Path
1. Create `<task‑id>-plan.md`. Think about the best approach, and document it.
3. Implement per **DEVELOPMENT_PHILOSOPHY.md**.
4. Run formatter, linter, tests; fix everything.
5. Mark ticket `[x]`, commit, push, delete plan file.

---

## 4 Complex Path
1. Create `<task‑id>-task.md` containing:
   - Task ID + title
   - Original ticket text
   - Full **Implementation Approach Analysis prompt** (see separate file)

2. **Generate Approaches & Plan**
   - Identify relevant development philosophy files
   - Run the exact thinktank command:

     ```bash
     thinktank --instructions <sanitized-task-title>-TASK.md --synthesis-model gemini-2.5-pro-preview-03-25 --model gemini-2.5-pro-preview-03-25 --model o4-mini [relevant development philosophy files] [top-ten-other-relevant-files]
     ```

   - Copy synthesis file: `cp thinktank_output/gemini-2.5-pro-preview-03-25-synthesis.md <task‑id>-plan.md`; delete the `*-task.md`.

3. **Tests First**
   - Write failing tests covering happy path + critical edges.
   - Mock **only** true externals.

4. **Code**
   - Implement just enough to make tests pass, staying inside philosophy guard‑rails.

5. **Refactor**
   - Tighten names, remove cruft, enforce simplicity—tests must stay green.

6. **Verify & Finalize**
   - Full test suite, linter, build must all pass.
   - Mark ticket `[x]`, commit, push, delete plan file.

---

## 5 Execution Rules
- Dependency graph must stay acyclic.
- Every commit passes CI; failing commits are outlawed.

