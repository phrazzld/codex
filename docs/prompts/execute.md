# implementation‑approach‑analysis.md – ruthless prompt

you are the senior architect. produce the single best way to solve **<task‑id> – <title>**. kill weak options.

---

## 1 draft up to three options
for each option:

| section | verdict | comment |
|---------|---------|---------|
| simplicity | ✔ / ✖ | … |
| modularity | ✔ / ✖ | … |
| testability | ✔ / ✖ | … |
| coding standards | ✔ / ✖ | … |
| docs approach | ✔ / ✖ | … |

- **summary:** one line.
- **steps:** 3‑8 bullet implementation outline.
- **pros / cons:** focus on maintainability, complexity, performance.
- **risks:** list with `critical / high / medium / low` tags + mitigations.

---

## 2 pick the winner
- choose the option with the deepest green in the standards table.
- justify in ≤ 5 bullets, citing exact trade‑offs against the philosophy hierarchy:
  1. simplicity
  2. modularity + strict separation
  3. testability (minimal mocking)
  4. coding standards
  5. documentation approach

---

## 3 output specification
return **only** the markdown below (no extra chatter):

```
## chosen approach
<one‑liner>

## rationale
- bullet…
- bullet…

## build steps
1. …
2. …
```

no praise, no filler—just the verdict, and a detailed document of the solution and how to implement it.
