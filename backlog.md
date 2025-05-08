# BACKLOG

## High Priority

### Product Identity & Branding

- **[Enhancement]**: Rename "codex" to a unique, meaningful project name
  - **Complexity**: Medium
  - **Rationale**: The current name "codex" does not reflect the system's evolving role as the engineering base of operations; a distinctive, resonant name will improve team cohesion, documentation clarity, and external perception.
  - **Expected Outcome**: All references to "codex" (code, configs, docs, CI/CD, scripts, repo, branding) are updated consistently to the new name. Internal/external docs and onboarding material reflect the change.
  - **Potential Names**: fortress of solitude, cloud nine, the lanes, necronomicon, cloaca maxima, grimoire, thinktank, architect, blueprint

### Automation & AI Integration

- **[Enhancement]**: Centralize thinktank invocation logic
  - **Complexity**: Medium
  - **Rationale**: Hardcoded thinktank calls are scattered across multiple files, causing duplication and increasing maintenance overhead; centralizing this logic enables easier updates and reduces risk of inconsistencies.
  - **Expected Outcome**: All AI agent/thinktank invocations are defined in a single, reusable module, with all commands referencing this abstraction.

- **[Feature]**: Enhance AI-driven code activity monitoring and auto-intervention
  - **Complexity**: Complex
  - **Rationale**: Current AI code execution can get stuck, loop, or become redundant without detection or recovery. Automated monitoring and self-healing (e.g., triggering `/consult` if stuck) will boost reliability and user trust.
  - **Expected Outcome**: System logs AI activity periodically, detects inactivity or loops (e.g., based on time or repeated output), and triggers appropriate interventions or alerts automatically.

### Developer Experience & Workflow

- **[Feature]**: Implement a robust "get relevant files for context" tool
  - **Complexity**: Complex
  - **Rationale**: Providing AI and developers with the most relevant code/context increases the quality of code generation, reviews, and automated assistance, especially given context window constraints.
  - **Expected Outcome**: Utility efficiently selects and ranks relevant files based on the current task, user query, or code location, and integrates with AI/command workflows.

- **[Enhancement]**: Modify "resolve" action to leverage thinktank
  - **Complexity**: Medium
  - **Rationale**: The current "resolve" action is not sufficiently leveraging strategic AI insights; integrating thinktank guidance will improve resolution quality and user confidence.
  - **Expected Outcome**: "Resolve" workflows systematically consult thinktank before suggesting or applying changes.
  - **Dependencies**: Centralized thinktank invocation

- **[Enhancement]**: Modify "audit" action to have thinktank conduct audits
  - **Complexity**: Medium
  - **Rationale**: Delegating audit logic to the thinktank (not just remediation drafting) will yield more thorough and context-aware analysis, catching issues earlier.
  - **Expected Outcome**: Audit workflows invoke thinktank for end-to-end review and recommendations.
  - **Dependencies**: Centralized thinktank invocation

- **[Feature]**: Pre-commit integration to transmit diff and dev philosophy to flash (AI agent)
  - **Complexity**: Medium
  - **Rationale**: Sending code diffs and philosophy to flash before commits can enable automated reviews, enforce standards, and catch issues preemptively, improving code quality and compliance.
  - **Expected Outcome**: Pre-commit hook reliably sends diffs and philosophy doc to flash for automated review, with actionable feedback surfaced to user.

## Medium Priority

### Observability & Monitoring

- **[Enhancement]**: Support 1M+ context window models for full-codebase AI operations
  - **Complexity**: Medium
  - **Rationale**: Larger context windows allow more holistic AI analysis and code generation, reducing the need for aggressive pre-filtering of files and improving quality of automated suggestions.
  - **Expected Outcome**: AI workflows can process and reason over the entire codebase where supported, falling back gracefully on smaller models otherwise.

- **[Enhancement]**: Expand structured logging for all AI and user actions
  - **Complexity**: Medium
  - **Rationale**: Consistent, structured logs are critical for debugging, auditing, and observability, as mandated by development philosophy; current coverage may be incomplete.
  - **Expected Outcome**: All significant actions and errors are logged in structured (JSON) format with required context fields; logs are easily queryable and integrated with aggregation tools.

- **[Feature]**: Implement metrics and health endpoints for core services and AI actions
  - **Complexity**: Medium
  - **Rationale**: Monitoring system health, latency, error rates, and AI/automation performance enables proactive issue detection and SLO/SLA enforcement.
  - **Expected Outcome**: Metrics endpoints expose RED/USE metrics; health endpoints reflect system/component/AIs operational status.

### Technical Excellence

- **[Enhancement]**: Implement mandatory pre-commit hooks (Formatting, Linting, Secrets Scan, Commit Message Lint)
  - **Complexity**: Medium
  - **Rationale**: Enforces coding standards locally, ensuring consistency and catching issues before CI. Directly implements mandatory standards from Dev Philosophy.
  - **Expected Outcome**: Pre-commit hooks installed via a framework automatically run checks on staged files. Commits fail if checks do not pass.

- **[Refactor]**: Standardize error handling across services/modules (Go/Rust/TS)
  - **Complexity**: Medium
  - **Rationale**: Ensures consistent, informative, and actionable error reporting, crucial for debugging and observability.
  - **Expected Outcome**: Error handling follows language-specific best practices. Errors are wrapped with context. Consistent logging of errors.

- **[Refactor]**: Audit and refactor configuration management (Externalize secrets/config)
  - **Complexity**: Medium
  - **Rationale**: Enhances security and deployment flexibility by ensuring no sensitive data or environment-specific settings are hardcoded, adhering to Dev Philosophy security principles.
  - **Expected Outcome**: Audit confirms no secrets (API keys, passwords) are in code/config files. Environment-specific settings are loaded via environment variables or dedicated config loading libraries.

## Low Priority

### Research & Innovation

- **[Research]**: Explore advanced AI self-diagnosis and meta-reasoning for stuck/looped processes
  - **Complexity**: Complex
  - **Rationale**: Pushing the boundary of AI autonomy to detect and recover from novel failure modes would create a competitive differentiator.
  - **Expected Outcome**: Prototype or research summary on meta-reasoning techniques for autonomous recovery.
  - **Dependencies**: AI activity monitoring

- **[Research]**: Evaluate alternative architectures for context extraction (semantic search, embeddings, etc.)
  - **Complexity**: Medium
  - **Rationale**: More intelligent relevance filtering could outperform simple heuristics, especially as codebase grows.
  - **Expected Outcome**: Report and/or prototype comparing relevance extraction approaches.

### Documentation & Architecture

- **[Enhancement]**: Add architecture diagrams (Mermaid/PlantUML) to documentation
  - **Complexity**: Simple
  - **Rationale**: Visual diagrams accelerate understanding and knowledge sharing, especially for new contributors.
  - **Expected Outcome**: High-level system/component diagrams in docs, referenced from README.

- **[Enhancement]**: Document rationale for major design decisions and trade-offs
  - **Complexity**: Simple
  - **Rationale**: Recording "why" aids future maintainers and supports transparent, informed evolution.
  - **Expected Outcome**: Major decisions documented in architecture/RFC docs.

