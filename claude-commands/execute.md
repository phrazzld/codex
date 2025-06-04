# EXECUTE

Pick the next unblocked ticket from `TODO.md` and complete it following our development philosophy.

## Workflow

**1. Select Task**
- Find first `[ ]` ticket where all `depends-on:` tasks are `[x]` completed
- Mark as `[~]` in progress

**2. Assess Complexity & Allocate Thinking**
- **Analyze** the ticket's scope, risk, architectural impact, and design decisions required
- **Scale thinking budget** based on complexity:
  - **Minimal**: Trivial fixes, typos, obvious changes → just execute
  - **Low**: Single-file changes, clear requirements → **think** briefly about approach
  - **Medium**: Multi-file changes, some ambiguity → **think hard** about design and plan thoroughly
  - **High**: Architectural changes, cross-cutting concerns → **ultrathink** - brainstorm multiple solutions, evaluate tradeoffs, risk analysis, comprehensive planning

**3. Plan & Implement**
- Follow `DEVELOPMENT_PHILOSOPHY.md` and relevant language appendices
- For medium+ complexity: write failing tests first, implement to make them pass
- Never mock internal collaborators - refactor for testability instead
- Create planning artifacts proportional to complexity

**4. Validate**
- Format, lint, test - resolve all issues
- Ensure clean conventional commit that passes pre-commit hooks

**5. Finalize**
- Mark ticket `[x]` complete
- Push clean commit
- Clean up any planning files

## Key Principles
- Maintain acyclic dependencies
- All commits must pass CI
- Test-driven development for non-trivial work
- Mock only true external dependencies