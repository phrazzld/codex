# Brutal Remediation‑Planning Prompt

Your task: turn a pile of code‑review wounds into a surgical strike plan. No fluff, no ego—just the shortest path from "broken" to "bulletproof."

---

## 1 Triage the Feedback
- Read the `code_review.md` table line‑by‑line.
- Tag every issue:

| ID | Type | Severity | Location |
|----|------|----------|----------|
| cr‑01 | arch | blocker / high / med / low | file:line |

(Use the IDs in all later refs.)

---

## 2 Diagnose & Prescribe
For each **blocker** or **high** severity item (and any medium that bundles in cheaply):

1. **Problem:** one sentence.
2. **Impact:** why it hurts (security hole, logic bomb, tech‑debt anchor).
3. **Options:** 2‑3 ways to fix, each with 3‑5 bullets.
4. **Standards Check:** table ↓

| Philosophy | Passes? | Note |
|------------|---------|------|
| Simplicity | ✔ / ✖ | … |
| Modularity | ✔ / ✖ | … |
| Testability | ✔ / ✖ | … |
| Coding Std | ✔ / ✖ | … |
| Security | ✔ / ✖ | … |

5. **Recommendation:** pick the greenest option + ≤ 3‑bullet rationale.
6. **Effort:** `xs / s / m / l / xl` (≤ 1 d, ≤ 2 d, ≤ 3 d, ≤ 1 w, > 1 w).

---

## 3 Build the Strike Order
- Sort by severity → dependency → effort.
- Deliver quick wins early if they unlock others.
- Produce a numbered list: `1. cr‑02, 2. cr‑01, …`

---

## 4 Plan Format (`plan.md`)
```
# Remediation Plan – Sprint <n>

## Executive Summary
<3‑sentence overview: why these fixes, why this order>

## Strike List
| Seq | CR‑ID | Title | Effort | Owner? |
|-----|-------|-------|--------|--------|
| 1 | cr‑02 | seal jwt leak | s | backend |
| … | … | … | … | … |

## Detailed Remedies
### cr‑02 Seal JWT Leak
- **Problem:** …
- **Impact:** …
- **Chosen Fix:** …
- **Steps:**
  1. …
  2. …
- **Done‑When:** tests pass, no token in logs, zap scan clean.

*(repeat for each ID)*

## Standards Alignment
- Bullet justification referencing philosophy hierarchy.

## Validation Checklist
- Automated tests green.
- Static analyzers clear.
- Manual pen‑test of <area> passes.
- No new lint or audit warnings.

```

---

## 5 Output Rules
- Return **only** the finished `plan.md` content—nothing else.
- Every fix must trace back to a code‑review ID.
- If review missed a latent blocker, add it and mark `cr‑new‑x`.
- Be savage: call out any reviewer under‑rating.