# brutal remediation‑planning prompt

your task: turn a pile of code‑review wounds into a surgical strike plan. no fluff, no ego—just the shortest path from “broken” to “bulletproof.”

---

## 1 triage the feedback
- read the `code_review.md` table line‑by‑line.
- tag every issue:

| id | type | severity | location |
|----|------|----------|----------|
| cr‑01 | arch | blocker / high / med / low | file:line |

(use the ids in all later refs.)

---

## 2 diagnose & prescribe
for each **blocker** or **high** severity item (and any medium that bundles in cheaply):

1. **problem:** one sentence.
2. **impact:** why it hurts (security hole, logic bomb, tech‑debt anchor).
3. **options:** 2‑3 ways to fix, each with 3‑5 bullets.
4. **standards check:** table ↓

| philosophy | passes? | note |
|------------|---------|------|
| simplicity | ✔ / ✖ | … |
| modularity | ✔ / ✖ | … |
| testability | ✔ / ✖ | … |
| coding std | ✔ / ✖ | … |
| security | ✔ / ✖ | … |

5. **recommendation:** pick the greenest option + ≤ 3‑bullet rationale.
6. **effort:** `xs / s / m / l / xl` (≤ 1 d, ≤ 2 d, ≤ 3 d, ≤ 1 w, > 1 w).

---

## 3 build the strike order
- sort by severity → dependency → effort.
- deliver quick wins early if they unlock others.
- produce a numbered list: `1. cr‑02, 2. cr‑01, …`

---

## 4 plan format (`plan.md`)
```
# remediation plan – sprint <n>

## executive summary
<3‑sentence overview: why these fixes, why this order>

## strike list
| seq | cr‑id | title | effort | owner? |
|-----|-------|-------|--------|--------|
| 1 | cr‑02 | seal jwt leak | s | backend |
| … | … | … | … | … |

## detailed remedies
### cr‑02 seal jwt leak
- **problem:** …
- **impact:** …
- **chosen fix:** …
- **steps:**
  1. …
  2. …
- **done‑when:** tests pass, no token in logs, zap scan clean.

*(repeat for each id)*

## standards alignment
- bullet justification referencing philosophy hierarchy.

## validation checklist
- automated tests green.
- static analyzers clear.
- manual pen‑test of <area> passes.
- no new lint or audit warnings.

```

---

## 5 output rules
- return **only** the finished `plan.md` content—nothing else.
- every fix must trace back to a code‑review id.
- if review missed a latent blocker, add it and mark `cr‑new‑x`.
- be savage: call out any reviewer under‑rating.
