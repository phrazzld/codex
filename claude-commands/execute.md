# Claude‑Command.md – Ruthless Execute Loop

Your only goal: grab the next unblocked ticket, finish it, commit. No ceremony.

---

## 0 Prep
- Open `todo.md`, `development_philosophy.md`, full codebase.
- Ticket state markers: `[ ]` untouched · `[~]` in‑progress · `[x]` done.

---

## 1 Pick a Ticket
1. Scan `todo.md` top → bottom.
2. Select the first `[ ]` ticket whose `depends‑on:` list is empty or all `[x]`.
3. Flip its box to `[~]` and note **ID** + **Title**.

---

## 2 Classify
- **Simple** → single‑file change, clear logic, no design calls.
- **Complex** → multi‑file, tricky logic, risk ≥ high, or any ambiguity.

---

## 3 Simple Path
1. Create `<task‑id>-plan.md`. Think about the best approach, and document it.
2. *(optional)* Write minimal happy‑path test.
3. Implement per **development_philosophy.md**.
4. Run formatter, linter, tests; fix everything.
5. Mark ticket `[x]`, commit, push, delete plan file.

---

## 4 Complex Path
1. Create `<task‑id>-task.md` containing:
   - Task ID + title
   - Original ticket text
   - Full **Implementation Approach Analysis prompt** (see separate file)

2. **Generate Approaches & Plan**
   - Run the exact architect command:

     ```
     architect --instructions <sanitized-task-title>-TASK.md \
               --output-dir architect_output \
               --model gemini-2.5-flash-preview-04-17 \
               --model gemini-2.5-pro-preview-03-25 \
               --model o4-mini \
               --model gpt-4.1 \
               DEVELOPMENT_PHILOSOPHY.md [top-ten-relevant-files]
     ```

   - Read outputs, **think hard**, keep the strongest ideas only.
   - Synthesize the chosen path into `<task‑id>-plan.md`; delete the `*-task.md`.

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
- No ticket remains `[~]` > 24 h—split or re‑queue.
- Dependency graph must stay acyclic.
- Every commit passes CI; failing commits are outlawed.

***Brutal clarity or bust.***