# EXECUTE

Pick the next unblocked ticket from `TODO.md` and complete it following our development philosophy and leyline documents.

## Workflow

**1. Select Task**
- Find first `[~]` ticket -- an in progress ticket -- and complete it.
- If there are no in progress tickets, find first `[ ]` ticket where all `depends-on:` tasks are `[x]` completed
- Mark as `[~]` in progress

**2. Assess Complexity & Allocate Thinking**
- **Leyline Pre-Processing**: Based on the selected ticket's domain and requirements:
  - Identify relevant tenets (e.g., Modularity for component work, Testability for new features, Simplicity for refactoring)
  - Query applicable bindings (language-specific, testing patterns, architecture guidelines)
  - Internalize how these principles will guide implementation approach
- **Analyze** the ticket's scope, risk, architectural impact, and design decisions required
- **Scale thinking budget** based on complexity:
  - **Minimal**: Trivial fixes, typos, obvious changes → just execute
  - **Low**: Single-file changes, clear requirements → **think** briefly about approach
  - **Medium**: Multi-file changes, some ambiguity → **think hard** about design and plan thoroughly
  - **High**: Architectural changes, cross-cutting concerns → **engage thinktank** for comprehensive analysis

**3. For High Complexity: Engage Thinktank**
- **Investigate context**: Thoroughly examine the codebase to identify the most relevant files and directories for the task
  - Read the ticket carefully to understand all affected areas
  - Use search tools to find related code, tests, documentation, and configuration
  - Identify key modules, interfaces, and dependencies that will be impacted
  - Locate existing patterns and architectural precedents to follow
- **Create instructions**: Generate `execute-instructions.md` with detailed context about:
  - The specific task requirements and acceptance criteria
  - Relevant architectural constraints and design principles
  - Key files and directories that need consideration
  - Expected implementation approach and testing strategy
- **Run thinktank**: Execute comprehensive analysis:
  ```bash
  thinktank-wrapper --instructions execute-instructions.md --model-set all --include-leyline --include-glance [list of relevant files and directories]
  ```
- **Synthesize results**: Review thinktank outputs and create implementation plan

**4. Plan & Implement**
- Follow `DEVELOPMENT_PHILOSOPHY.md`, leyline documents, and relevant language appendices
- For medium+ complexity: write failing tests first, implement to make them pass
- For high complexity: implement according to thinktank analysis and synthesis
- Never mock internal collaborators - refactor for testability instead
- Create planning artifacts proportional to complexity

**5. Validate**
- Format, lint, test - resolve all issues
- Ensure clean conventional commit that passes pre-commit hooks

**6. Finalize**
- Mark ticket `[x]` complete
- Push clean commit
- Clean up any planning files and thinktank outputs

## Key Principles
- Maintain acyclic dependencies
- All commits must pass CI
- Test-driven development for non-trivial work
- Mock only true external dependencies
