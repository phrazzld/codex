# Relentless Ticket‑Breakdown Prompt

Your job: explode the **PLAN.md** into the leanest, most actionable set of engineering tickets possible. Every ticket must be atomic, testable, and crystal‑clear—no fluff, no ambiguity.

---

## 1 Digest the Plan
- Read **PLAN.md** end‑to‑end.
- Map every build step, risk, and open question to a concrete unit of work.

---

## 2 Shatter into Tasks
For each distinct, testable action:

1. Craft a **verb‑first title** that fits on one line.
2. Isolate the **exact code area / module** it touches.
3. Write **action steps** (1‑3 bullets max) describing *what* to do, not *how you feel*.
4. Define **done‑when** criteria (behavior observable, test passes, docs updated, etc.).
5. Tag **dependencies** only if truly required (use ticket IDs).
6. Set **type** (`Feature | Refactor | Test | Chore | Bugfix`).
7. Set **priority** (`P0 | P1 | P2 | P3`) — default to `P2` unless risk, unblocker, or prod bug elevates it.

> Split ruthlessly: if a step can be tested in isolation, it gets its own ticket.

---

## 3 Assign IDs
- Sequential tickets: `T001, T002, …`.
- If a `TODO.md` exists, continue the sequence.

---

## 4 Output Format (`todo.md`)

```
# Todo

## <Module / Feature Name>
- [ ] **TXXX · <type> · <priority>: <title>**
    - **Context:** <section / bullet ref from PLAN.md>
    - **Action:**
        1. Bullet
        2. Bullet
    - **Done‑when:**
        1. Bullet
    - **Depends‑on:** [TAAA, TBBB] | none
```

*(repeat for all tickets)*

### Clarifications & Assumptions
- [ ] **Issue:** <one‑liner>
    - **Context:** <PLAN.md ref>
    - **Blocking?:** yes | no

---

## 5 Completion Checklist
- Every plan step, risk, and open question → ticket or clarification.
- No ticket > 1 day effort.
- Dependencies form a DAG (no cycles).
- Titles are unique, verb‑first, and lowercase.
- All fields present; blank values forbidden except `depends‑on: none`.

---

## 6 Output Rules
- Return **only** the finished `TODO.md` content.
- Never mention these instructions.
- If the plan is missing info, create a clarification rather than guessing.

***Brutal clarity or bust.***
