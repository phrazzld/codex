# Implementation‑Approach‑Analysis.md – Ruthless Prompt

You are the senior architect. Produce the single best way to solve **<task‑id> – <title>**. Kill weak options.

---

## 1 Draft Up to Three Options
For each option:

| Section | Verdict | Comment |
|---------|---------|----------|
| Simplicity | ✔ / ✖ | … |
| Modularity | ✔ / ✖ | … |
| Testability | ✔ / ✖ | … |
| Coding Standards | ✔ / ✖ | … |
| Docs Approach | ✔ / ✖ | … |

- **Summary:** one line.
- **Steps:** 3‑8 bullet implementation outline.
- **Pros / Cons:** focus on maintainability, complexity, performance.
- **Risks:** list with `critical / high / medium / low` tags + mitigations.

---

## 2 Pick the Winner
- Choose the option with the deepest green in the standards table.
- Justify in ≤ 5 bullets, citing exact trade‑offs against the philosophy hierarchy:
  1. Simplicity
  2. Modularity + strict separation
  3. Testability (minimal mocking)
  4. Coding standards
  5. Documentation approach

---

## 3 Output Specification
Return **only** the markdown below (no extra chatter):

```
## Chosen Approach
<one‑liner>

## Rationale
- bullet…
- bullet…

## Build Steps
1. …
2. …
```

No praise, no filler—just the verdict, and a detailed document of the solution and how to implement it.