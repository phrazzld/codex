# claude‑command.md – ruthless execute loop

your only goal: grab the next unblocked ticket, finish it, commit. no ceremony.

---

## 0 prep
- open `todo.md`, `development_philosophy.md`, full codebase.
- ticket state markers: `[ ]` untouched · `[~]` in‑progress · `[x]` done.

---

## 1 pick a ticket
1. scan `todo.md` top → bottom.
2. select the first `[ ]` ticket whose `depends‑on:` list is empty or all `[x]`.
3. flip its box to `[~]` and note **id** + **title**.

---

## 2 classify
- **simple** → single‑file change, clear logic, no design calls.
- **complex** → multi‑file, tricky logic, risk ≥ high, or any ambiguity.

---

## 3 simple path
1. create `<task‑id>-plan.md`. think about the best approach, and document it.
2. *(optional)* write minimal happy‑path test.
3. implement per **development_philosophy.md**.
4. run formatter, linter, tests; fix everything.
5. mark ticket `[x]`, commit, push, delete plan file.

---

## 4 complex path
1. create `<task‑id>-task.md` containing:
   - task id + title
   - original ticket text
   - full **implementation approach analysis prompt** (see separate file)

2. **generate approaches & plan**
   - run the exact architect command:

     ```
     architect --instructions <sanitized-task-title>-TASK.md \
               --output-dir architect_output \
               --model gemini-2.5-flash-preview-04-17 \
               --model gemini-2.5-pro-preview-03-25 \
               --model o4-mini \
               --model gpt-4.1 \
               DEVELOPMENT_PHILOSOPHY.md [top-ten-relevant-files]
     ```

   - read outputs, **think hard**, keep the strongest ideas only.
   - synthesize the chosen path into `<task‑id>-plan.md`; delete the `*-task.md`.

3. **tests first**
   - write failing tests covering happy path + critical edges.
   - mock **only** true externals.

4. **code**
   - implement just enough to make tests pass, staying inside philosophy guard‑rails.

5. **refactor**
   - tighten names, remove cruft, enforce simplicity—tests must stay green.

6. **verify & finalize**
   - full test suite, linter, build must all pass.
   - mark ticket `[x]`, commit, push, delete plan file.

---

## 5 execution rules
- no ticket remains `[~]` > 24 h—split or re‑queue.
- dependency graph must stay acyclic.
- every commit passes CI; failing commits are outlawed.

***brutal clarity or bust.***
