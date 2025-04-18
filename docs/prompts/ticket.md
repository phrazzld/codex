# relentless ticket‑breakdown prompt

your job: explode the **plan.md** into the leanest, most actionable set of engineering tickets possible. every ticket must be atomic, testable, and crystal‑clear—no fluff, no ambiguity.

---

## 1 digest the plan
- read **plan.md** end‑to‑end.
- map every build step, risk, and open question to a concrete unit of work.

---

## 2 shatter into tasks
for each distinct, testable action:

1. craft a **verb‑first title** that fits on one line.
2. isolate the **exact code area / module** it touches.
3. write **action steps** (1‑3 bullets max) describing *what* to do, not *how you feel*.
4. define **done‑when** criteria (behavior observable, test passes, docs updated, etc.).
5. tag **dependencies** only if truly required (use ticket IDs).
6. set **type** (`feature | refactor | test | chore | bugfix`).
7. set **priority** (`p0 | p1 | p2 | p3`) — default to `p2` unless risk, unblocker, or prod bug elevates it.

> split ruthlessly: if a step can be tested in isolation, it gets its own ticket.

---

## 3 assign ids
- sequential tickets: `t001, t002, …`.
- if a `todo.md` exists, continue the sequence.

---

## 4 output format (`todo.md`)

```
# todo

## <module / feature name>
- [ ] **tXXX · <type> · <priority>: <title>**
    - **context:** <section / bullet ref from plan.md>
    - **action:**
        1. bullet
        2. bullet
    - **done‑when:**
        1. bullet
    - **depends‑on:** [tAAA, tBBB] | none
```

*(repeat for all tickets)*

### clarifications & assumptions
- [ ] **issue:** <one‑liner>
    - **context:** <plan.md ref>
    - **blocking?:** yes | no

---

## 5 completion checklist
- every plan step, risk, and open question → ticket or clarification.
- no ticket > 1 day effort.
- dependencies form a DAG (no cycles).
- titles are unique, verb‑first, and lowercase.
- all fields present; blank values forbidden except `depends‑on: none`.

---

## 6 output rules
- return **only** the finished `todo.md` content.
- never mention these instructions.
- if the plan is missing info, create a clarification rather than guessing.

***brutal clarity or bust.***
