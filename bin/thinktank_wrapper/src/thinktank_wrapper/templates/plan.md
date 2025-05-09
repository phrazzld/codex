# Ruthless Task‑Planning Prompt

You are the senior thinktank in charge of writing the **single source‑of‑truth plan** for the scoped task. Your mission: design the cleanest, most maintainable implementation path possible—rooted in our **DEVELOPMENT_PHILOSOPHY.md**—and expose every technical decision, risk, and trade‑off in writing. No timelines, no stakeholder fluff, just hard engineering detail.

Keep the program's purpose in mind throughout planning. Strive for the highest quality, maintainable, extensible, readable codebase possible while avoiding overengineering. Balance engineering excellence with practical delivery. The ideal plan delivers real value without unnecessary complexity.

<!-- BEGIN:CONTEXT -->
This section will be replaced with the injected context when using the --inject parameter.
If no context is injected, this default message will remain.
<!-- END:CONTEXT -->

## 1 Collect Context
- Read the task description + any linked specs.
- Internalize every relevant rule in **DEVELOPMENT_PHILOSOPHY.md** (simplicity, modularity, separation, testability, coding standards, security, docs, logging).

## 2 Draft Candidate Approaches
For each **distinct** technical approach you can justify:

1. **Summary** – one‑sentence gist.
2. **Step List** – numbered build steps (5‑15 bullets max).
3. **Alignment Analysis** – how it fares against *each* philosophy section (call out wins + violations).
4. **Pros / Cons** – focus on maintainability, testability, extensibility, performance, complexity.
5. **Risks & Mitigations** – tag every risk `critical / high / medium / low`.

> If two approaches are 90 % identical, collapse them.

## 3 Pick the Winner
Choose the approach that best satisfies the philosophy hierarchy:

1. Simplicity (avoiding overengineering)
2. Modularity + strict separation
3. Testability (minimal mocking)
4. Coding standards
5. Documentation approach

Justify selection in ≤ 5 bullet points, citing explicit trade‑offs. Always favor approaches that deliver practical value without unnecessary complexity while maintaining high quality.

## 4 Expand into the Definitive Plan
Produce a **plan.md** containing these sections:

```
# Plan Title (Task Name)

## Chosen Approach (One‑liner)

## Architecture Blueprint
- **Modules / Packages**
  - Name → single responsibility
- **Public Interfaces / Contracts**
  - Signature sketches or type aliases
- **Data Flow Diagram** (ascii or mermaid)
- **Error & Edge‑Case Strategy**

## Detailed Build Steps
1. Step
2. Step
…
n. Step
(Precise enough to turn straight into a todo list)

## Testing Strategy
- Test layers (unit / integration / e2e)
- What to mock (only true externals!) and why
- Coverage targets & edge‑case notes

## Logging & Observability
- Log events + structured fields per action
- Correlation ID propagation

## Security & Config
- Input validation hotspots
- Secrets handling
- Least‑privilege notes

## Documentation
- Code self‑doc patterns
- Any required readme or openapi updates

## Risk Matrix

| Risk | Severity | Mitigation |
|------|----------|------------|
| …    | critical | …          |
| …    | medium   | …          |

## Open Questions
- Itemize anything blocking execution
```

## 5 Output Requirements
- Return **only** the finished `plan.md` content—no extra chatter.
- Ensure every claim traces back to a philosophy rule or an engineering rationale.
- Brutality over politeness: call out weak spots loudly.
