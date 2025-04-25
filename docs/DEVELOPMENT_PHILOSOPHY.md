# DEVELOPMENT PHILOSOPHY

This document outlines the development philosophy, principles, guidelines, and mandatory standards for our software projects. It serves as a comprehensive reference for our approach to software development, intended for **both human developers and AI coding agents**. Adherence to these standards is critical for building robust, maintainable, secure, and observable systems.

## Table of Contents

- [Purpose and Audience](#purpose-and-audience)
- [Core Principles](#core-principles)
- [Architecture Guidelines](#architecture-guidelines)
- [Coding Standards](#coding-standards)
- [Automation, Quality Gates, and CI/CD](#automation-quality-gates-and-cicd)
- [Semantic Versioning and Release Automation](#semantic-versioning-and-release-automation)
- [Testing Strategy](#testing-strategy)
- [Logging Strategy](#logging-strategy)
- [Security Considerations](#security-considerations)
- [Documentation Approach](#documentation-approach)
- [Observability](#observability)
- [Appendices](#appendices)

---

# Purpose and Audience

This document defines **how we build software**. Its primary audience includes:

1.  **Human Developers:** Providing a shared understanding of principles, patterns, and standards to guide design, implementation, and review.
2.  **AI Coding Agents:** Serving as a **direct instruction set** and reference for generating, modifying, and testing code according to our standards. AI agents **MUST** adhere to the mandatory requirements outlined herein.

The goal is to produce software that is simple, modular, testable, maintainable, secure, observable, and delivered efficiently through high levels of automation.

**Guiding Ethos:** In all design and implementation decisions, keep the project's core purpose and goals at the forefront. Strive for the highest standards of maintainability, extensibility, readability, and ease of change to create a delightful software experience. Balance engineering excellence with practical delivery by avoiding overengineering and unnecessary complexity. Always favor the simplest solution that meets requirements while maintaining a clear path for future evolution.

---

# Core Principles

These fundamental beliefs shape our approach to software. They guide decisions across all phases of development.

## 1. Simplicity First: Complexity is the Enemy

* **Principle:** Always seek the simplest possible solution that correctly meets the requirements. Actively resist and eliminate unnecessary complexity. Keep the program's purpose in mind when making design decisions.
* **Rationale:** Simple code is easier to understand, debug, test, modify, and maintain. Complexity is the primary source of bugs, friction, and long-term costs. We rigorously apply YAGNI (You Ain't Gonna Need It) while ensuring we're delivering high-quality, maintainable software.
* **Anti-Patterns:** Over-engineering, designing for imagined future requirements, premature abstraction, overly clever/obscure code, deep nesting (> 2-3 levels), excessively long functions/methods (signal to refactor), components violating the Single Responsibility Principle.
* **Balance:** Distinguish between essential complexity (required by the problem domain) and accidental complexity (introduced by our implementation). Ruthlessly eliminate the latter while thoughtfully managing the former.

## 2. Modularity is Mandatory: Do One Thing Well

* **Principle:** Construct software from small, well-defined, independent components (modules, packages, functions, services) with clear responsibilities and explicit interfaces. Strive for high internal cohesion and low external coupling. Embrace the Unix philosophy.
* **Rationale:** Modularity tames complexity, enables parallel development, independent testing/deployment, reuse, fault isolation, and easier evolution. It demands careful API design and boundary definition. (See [Architecture Guidelines](#architecture-guidelines)).

## 3. Design for Testability: Confidence Through Verification

* **Principle:** Testability is a fundamental, non-negotiable design constraint considered from the start. Structure code (clear interfaces, dependency inversion, separation of concerns, purity) for easy and reliable automated verification. Focus tests on *what* (public API, behavior), not *how* (internal implementation).
* **Rationale:** Automated tests build confidence, prevent regressions, enable safe refactoring, and act as executable documentation. Code difficult to test often indicates poor design (high coupling, mixed concerns). *Difficulty testing is a strong signal to refactor the code under test first.* (See [Testing Strategy](#testing-strategy)).

## 4. Maintainability Over Premature Optimization: Code for Humans First

* **Principle:** Write code primarily for human understanding and ease of future modification. Clarity, readability, and consistency are paramount. Optimize *only* after identifying *actual*, *measured* performance bottlenecks via profiling.
* **Rationale:** Most development time is spent reading/maintaining existing code. Premature optimization adds complexity, obscures intent, hinders debugging, and often targets non-critical paths, yielding negligible benefit at high maintenance cost. Prioritize clear naming and straightforward logic.

## 5. Explicit is Better than Implicit: Clarity Trumps Magic

* **Principle:** Make dependencies, data flow, control flow, contracts, and side effects clear and obvious. Avoid hidden conventions, global state, or complex implicit mechanisms. Leverage strong typing and descriptive naming.
* **Rationale:** Explicit code is easier to understand, reason about, debug, and refactor safely. Implicit behavior obscures dependencies, hinders tracing, and leads to unexpected side effects. Favor explicit dependency injection and rely heavily on static type checking.

## 6. Automate Everything: Eliminate Toil, Ensure Consistency

* **Principle:** Automate every feasible repetitive task: testing, linting, formatting, building, dependency management, vulnerability scanning, versioning, changelog generation, and deployment. If done manually more than twice, automate it.
* **Rationale:** Automation reduces manual error, ensures consistency, frees up developer time, provides faster feedback, and makes processes repeatable and reliable. Requires investment in robust tooling and CI/CD. (See [Automation, Quality Gates, and CI/CD](#automation-quality-gates-and-cicd)).

## 7. Document Decisions, Not Mechanics: Explain the *Why*

* **Principle:** Strive for self-documenting code (clear naming, structure, types) for the *how*. Reserve comments and external documentation primarily for the *why*: rationale for non-obvious choices, context, constraints, trade-offs.
* **Rationale:** Code mechanics change; comments detailing *how* quickly become outdated or redundant. The *reasoning* provides enduring value. Self-documenting code reduces the documentation synchronization burden. (See [Documentation Approach](#documentation-approach)).

---

# Architecture Guidelines

These guidelines translate Core Principles into actionable structures for maintainable, adaptable, testable, and observable applications. Language-specific implementations are detailed in the appendices.

**Balancing Quality and Pragmatism:** Keep the project's purpose and goals in mind when applying these guidelines. Strive for high-quality, maintainable architecture while avoiding overengineering. Apply these principles pragmatically, with appropriate depth for the scale and lifespan of your project.

## 1. Embrace the Unix Philosophy: Focused, Composable Units

* **Guideline:** Design components (services, libraries, modules, functions, CLIs) to "do one thing and do it well." Prefer composing smaller, specialized units over large, monolithic ones. Think inputs -> transformation -> outputs. Resist adding unrelated responsibilities.

## 2. Strict Separation of Concerns: Isolate the Core

* **Guideline:** **Ruthlessly separate** core business logic/domain knowledge from infrastructure concerns (UI, DB access, network calls, file I/O, CLI parsing, 3rd-party APIs). The core **MUST** be pure and unaware of specific I/O mechanisms.
* **Implementation:** Use patterns like Hexagonal Architecture (Ports & Adapters) or Clean Architecture. Define boundaries with interfaces defined *by the core*. Infrastructure implements these interfaces.
* **Rationale:** Paramount for *Modularity* and *Design for Testability*. Allows core logic testing in isolation and swapping infrastructure with minimal core impact.

## 3. Dependency Inversion Principle: Point Dependencies Inward

* **Guideline:** High-level policy (core logic) **MUST NOT** depend on low-level details (infrastructure). Both depend on abstractions (interfaces defined by the core). Source code dependencies point *inwards*: infrastructure -> core. Core **NEVER** imports infrastructure directly.
* **Implementation:** Use Dependency Injection (constructor injection preferred) to provide infrastructure implementations (conforming to core interfaces) to the core during application setup.
* **Rationale:** Enables *Separation of Concerns* and *Testability* by decoupling stable core logic from volatile infrastructure details.

## 4. Package/Module Structure: Organize by Feature, Not Type

* **Guideline:** Structure code primarily around business features/domains/capabilities, not technical types/layers. Prefer `src/orders/` over separate `src/controllers/`, `src/services/`, `src/repositories/`.
* **Goal:** High cohesion within feature modules, low coupling between them. This structure facilitates understanding, modification, testing, and potential future extraction into independent services if warranted.
* **Refactoring Signal:** A module becoming overly large, handling disparate concerns, or requiring excessive internal mocking is a signal to refactor or decompose it.

## 5. API Design: Define Explicit Contracts

* **Guideline:** Define clear, explicit, robust contracts for all APIs (internal module interactions, external REST/gRPC/GraphQL/CLIs). Document inputs, outputs, behavior, errors. Prioritize stability and versioning for external APIs.
* **Implementation:** Leverage type systems and interfaces internally. Use OpenAPI (Swagger) for REST, `.proto` files for gRPC as the source of truth. Provide clear CLI help messages.

## 6. Configuration Management: Externalize Environment-Specifics

* **Guideline:** **NEVER** hardcode configuration values (DB strings, API keys/endpoints, ports, feature flags) that vary between environments or are sensitive. Externalize all such configuration.
* **Implementation:** Prefer environment variables for deployment flexibility. Use config files (`.env`, YAML) for local development. Load via libraries (e.g., Viper, `dotenv`) into strongly-typed config objects/structs.

## 7. Consistent Error Handling: Fail Predictably and Informatively

* **Guideline:** Apply a consistent error handling strategy. Distinguish recoverable errors from unexpected bugs. Propagate errors clearly, adding context judiciously (without revealing sensitive info). Define explicit error handling boundaries (e.g., top-level middleware) to catch, log, and translate errors into meaningful responses (HTTP status codes, standardized error payloads, exit codes).
* **Implementation:** Use standard error types/interfaces. Avoid `panic` or uncaught exceptions for recoverable errors. Define custom error types for specific semantics where needed.

## 8. Design for Observability

* **Guideline:** Build systems that are inherently observable. Instrument code for effective logging, metrics collection, and distributed tracing from the outset. (See [Logging Strategy](#logging-strategy), [Observability](#observability)).

---

# Coding Standards

Concrete rules for writing readable, consistent, maintainable, and less defect-prone code. Adherence is **MANDATORY** and enforced via automated tooling.

## 1. Maximize Language Strictness

* **Standard:** Configure compilers and type checkers to their strictest practical settings (e.g., `strict: true` in `tsconfig.json`). Leverage static analysis fully.

## 2. Leverage Types Diligently: Express Intent Clearly

* **Standard:** Use the static type system fully and precisely. **`any` is FORBIDDEN** in TypeScript; use specific types, interfaces, unions, or `unknown`. Type all function parameters, return values, and variables. Use appropriate types and interfaces in Go.
* **Rationale:** Types are machine-checked documentation, improve clarity, reduce runtime errors, enable tooling. Supports *Explicit is Better than Implicit*.

## 3. Default to Immutability: Simplify State Management

* **Standard:** Treat data structures as immutable by default. Create new instances instead of modifying existing data in place. Mutation requires explicit justification (e.g., measured critical performance need).
* **Implementation:** Use language features (`readonly`, `const`) and immutable update patterns (spread syntax, functional array methods).
* **Rationale:** Simplifies reasoning about state, eliminates bugs from shared mutable state, makes changes predictable. Supports *Simplicity*.

## 4. Prioritize Pure Functions: Isolate Side Effects

* **Standard:** Implement core logic, transformations, and calculations as pure functions where feasible (output depends only on input, no side effects). Concentrate side effects at system edges (infrastructure adapters, command handlers).
* **Refactoring Goal:** Actively extract pure logic from functions mixing computation and side effects. Pass dependencies explicitly.
* **Rationale:** Pure functions are predictable, highly testable, reusable, easier to reason about. Supports *Simplicity*, *Modularity*, *Testability*.

## 5. Meaningful Naming: Communicate Purpose

* **Standard:** Choose clear, descriptive, unambiguous names for all identifiers (variables, functions, types, packages, etc.). Adhere strictly to language naming conventions (see Appendices). Avoid vague terms (`data`, `temp`, `handle`). Use domain terminology.
* **Rationale:** Crucial for *Maintainability* and readability. Reduces need for comments. Supports *Self-Documenting Code*.

## 6. Address Violations, Don't Suppress: Fix the Root Cause

* **Standard:** Directives to suppress linter/type errors (e.g., `// eslint-disable-line`, `@ts-ignore`, `// nolint:`, `as any`) are **STRICTLY FORBIDDEN** except in extremely rare, explicitly justified cases (requiring a comment explaining *why* it's safe and necessary, approved in review).
* **Rationale:** Suppressions hide bugs, technical debt, or poor design. Fixing the root cause leads to robust, maintainable code.

## 7. Disciplined Dependency Management: Keep It Lean and Updated

* **Standard:** Minimize third-party dependencies. Evaluate necessity, maintenance status, license, security posture, and transitive dependencies before adding. Keep essential dependencies reasonably updated via automated tools (e.g., Dependabot/Renovate Bot).
* **Implementation:** Regularly review/audit dependencies (`npm audit`, `go list -m all`, vulnerability checks). Remove unused dependencies. Address vulnerabilities promptly (see [Security Considerations](#security-considerations)).

## 8. Adhere to Length Guidelines

* **Standard:** Keep functions/methods and files/modules reasonably concise to aid readability and maintain single responsibility. Specific limits (e.g., function < 100 lines, file < 500 lines) may be enforced by linters (see Appendices). Exceeding limits is a strong signal to refactor.

---

# Automation, Quality Gates, and CI/CD

Automation is **MANDATORY** to ensure consistency, quality, and rapid feedback. Our standard workflow includes automated checks at multiple stages.

## 1. Local Development: Pre-commit Hooks

* **Standard:** **Mandatory** use of pre-commit hooks managed by a framework (e.g., `pre-commit`). Hooks **MUST** be installed and run before every commit.
* **Checks:** Typically include: Formatting (Prettier, gofmt/goimports), Linting (ESLint, golangci-lint), Basic static analysis, Secret detection, Conventional Commit message validation.
* **Policy:** **Bypassing hooks (`--no-verify`) is FORBIDDEN.** Fix issues locally before committing.

## 2. Continuous Integration (CI) Pipeline

* **Standard:** All code merged to the main branch **MUST** pass the full CI pipeline. The pipeline serves as the primary quality gate.
* **Mandatory Stages:**
    1.  **Checkout Code:** Fetch the relevant commit/branch.
    2.  **Setup Environment:** Install language runtime, dependencies.
    3.  **Lint & Format Check:** Verify code adheres to linting rules and formatting standards. **Failure is a build failure.**
    4.  **Unit Tests:** Run fast, isolated tests. **Failure is a build failure.**
    5.  **Integration Tests:** Run tests verifying component collaboration. **Failure is a build failure.**
    6.  **Test Coverage Check:** Analyze code coverage against configured minimum thresholds (e.g., 85% overall, 95% core logic). **Failure to meet or maintain thresholds is a build failure.**
    7.  **Security Vulnerability Scan:** Scan code and dependencies for known vulnerabilities (e.g., `npm audit --audit-level=high`, `govulncheck`). **Finding Critical or High severity vulnerabilities is a build failure.**
    8.  **Build:** Compile code or create build artifacts. **Failure is a build failure.**
    9.  **(Optional) Deploy:** Automated deployment to development/staging environments upon successful completion of prior stages.

## 3. Continuous Deployment (CD)

* **Goal:** Enable automated, safe deployments to production, often triggered by merges to the main branch after CI passes, potentially including additional gates like canary releases or manual approvals for critical systems.

---

# Semantic Versioning and Release Automation

We use Semantic Versioning (SemVer) 2.0.0 for all versioned artifacts (libraries, services). Versioning and release notes are automated.

## 1. Conventional Commits are Mandatory

* **Standard:** All commit messages **MUST** adhere to the [Conventional Commits specification](https://www.conventionalcommits.org/). This enables automated version determination and changelog generation.
* **Format:** `<type>[optional scope]: <description>` (e.g., `feat(api): add user profile endpoint`, `fix(parser): handle null input correctly`, `refactor!: rename core service interfaces`). Use `!` after type/scope for breaking changes.
* **Enforcement:** Pre-commit hooks and/or CI checks **MUST** validate commit message format.

## 2. Automated Version Bumping and Changelog Generation

* **Process:** CI/CD pipelines use standard tooling (e.g., `semantic-release`, `standard-version`) to analyze Conventional Commits since the last release.
* **Outcome:** Automatically determines the next SemVer version (patch, minor, major), tags the release in Git, and generates/updates a `CHANGELOG.md` file.

---

# Testing Strategy

Automated testing is non-negotiable for correctness, regression prevention, and enabling safe refactoring.

## 1. Guiding Principles

* **Verify Behavior:** Test *what* a component does via its public API, not *how*.
* **Maintainable Tests:** Test code *is* production code; keep it simple, clear, readable.
* **Testability Drives Design:** Difficulty testing **REQUIRES** refactoring the code under test.

## 2. Test Focus and Types

* **Unit Tests:** Verify small, isolated logic units (pure functions, algorithms) *without external dependencies or internal mocks*. Fast feedback.
* **Integration / Workflow Tests (High Priority):** Verify collaboration *between* multiple internal components through defined interfaces/APIs. **Provide high ROI for feature correctness.** Use real implementations of internal collaborators; mock *only* at true external system boundaries (see Mocking Policy).
* **System / End-to-End (E2E) Tests:** Validate user journeys/critical paths through the deployed system. Use sparingly due to cost/speed/flakiness.

## 3. Mocking Policy: Sparingly, At External Boundaries Only (CRITICAL)

* **Minimize Mocking:** Strive for designs requiring minimal mocking.
* **Mock ONLY True External System Boundaries:** Mocking is permissible *only* for interfaces/abstractions representing systems genuinely *external* to the service/application under test (Network I/O, Databases, Filesystem, System Clock, External Message Brokers).
* **Abstract First:** Always access external dependencies via interfaces defined *within* your codebase (Ports & Adapters). Mock *these local abstractions*.
* **NO Mocking Internal Collaborators:** **Mocking internal classes, structs, functions, or interfaces defined within the same application/service is STRICTLY FORBIDDEN.**
* **Refactor Instead of Internal Mocking:** The need for internal mocking indicates a design flaw (high coupling, poor separation). **The REQUIRED action is to refactor the code under test** (extract pure functions, introduce interfaces, use DI, break down components).

## 4. Test Coverage Enforcement

* **Standard:** Minimum test coverage targets (e.g., 85% line/branch coverage overall, 95%+ for core logic/pure functions) **MUST** be defined and **enforced** in the CI pipeline.
* **Policy:** Builds **WILL FAIL** if coverage drops below the required thresholds. Decreases must be addressed by adding tests.

## 5. Desired Test Characteristics (FIRST)

* **Fast:** Rapid feedback.
* **Independent / Isolated:** Run in any order, no shared state, self-contained setup/teardown.
* **Repeatable / Reliable:** Consistent pass/fail. Eliminate flakiness (time, concurrency, random data without seeds).
* **Self-Validating:** Explicit assertions, clear pass/fail.
* **Timely / Thorough:** Written alongside/before code. Cover happy paths, errors, edge cases.

## 6. Test Data Management

* Use clear, realistic, maintainable test data. Employ Test Data Builders or Factories. Ensure test isolation.

---

# Logging Strategy

Effective logging is crucial for observability, debugging, and monitoring. Our strategy prioritizes structured, contextual, and actionable logs.

## 1. Structured Logging is Mandatory

* **Standard:** All operational log output **MUST** be structured, preferably as JSON. Use standard structured logging libraries (see Appendices). **`fmt.Println` / `console.log` are FORBIDDEN** for operational logging.
* **Rationale:** Enables efficient parsing, filtering, and analysis by log aggregation systems.

## 2. Log Generously, Filter Aggressively

* **Philosophy:** Log sufficient detail at appropriate levels (especially DEBUG/INFO) to trace execution flow and state without needing a debugger. Rely on log aggregation tools for filtering/analysis based on level, correlation IDs, etc.

## 3. Standard Log Levels (Use Consistently)

* **DEBUG:** Detailed diagnostic information for development/troubleshooting. Disabled in production by default.
* **INFO:** Routine operational events (request received, process started/completed, significant state transitions). Default production level.
* **WARN:** Potentially harmful situations or unexpected conditions that were handled/recovered automatically but warrant attention (e.g., recoverable errors, resource limits approached, deprecated usage).
* **ERROR:** Serious errors causing an operation to fail or indicating a significant problem potentially requiring investigation/intervention (e.g., unhandled exceptions, failed external dependencies, data corruption). **MUST** include stack traces where appropriate.

## 4. Mandatory Context Fields

* All log entries **MUST** include at minimum:
    * `timestamp` (ISO 8601 format, UTC)
    * `level` (e.g., "info", "error")
    * `message` (clear description of the event)
    * `service_name` / `application_id`
    * `correlation_id` (Request ID, Trace ID - **CRITICAL**, see Context Propagation)
    * `function_name` / `module_name` (Where the log originated)
    * `error_details` (For ERROR level: type, message, stack trace)
* Include other relevant business context (e.g., User ID, Order ID) where appropriate and non-sensitive.

## 5. What to Log (Examples)

* **Entry/Exit:** Log entry/exit of key functions/methods (API handlers, service methods), including non-sensitive parameters.
* **External Calls:** Log before initiating and after completing calls (DB, APIs), including target, duration, success/failure.
* **Decision Points:** Log results of significant conditional logic.
* **State Changes:** Log key state transitions.
* **Errors:** Log all handled and unhandled errors at ERROR level with full context.
* **Background Jobs:** Log start, milestones, completion, errors.

## 6. What NOT to Log

* **Standard:** **NEVER log sensitive information:** Passwords, API keys, tokens, secrets, PII (unless explicitly required, compliant, and secured/masked), full credit card numbers, verbose internal data structures (except at DEBUG level).

## 7. Context Propagation is Mandatory

* **Standard:** For distributed systems or complex requests, a unique correlation ID (Request ID, Trace ID) **MUST** be generated at the entry point and propagated across all service boundaries (HTTP headers, message queue metadata) and asynchronous operations. This ID **MUST** be included in every log entry related to that request/transaction.
* **Implementation:** Use context propagation mechanisms provided by frameworks or libraries (e.g., Go `context.Context`, OpenTelemetry).

---

# Security Considerations

Security is integrated throughout the development lifecycle.

## 1. Core Principles

* **Input Validation:** **NEVER** trust external input. Validate type, format, length, range, allowed characters rigorously at boundaries.
* **Output Encoding:** Encode data appropriately for its context (HTML entity encoding, parameterized SQL queries) to prevent injection attacks.
* **Least Privilege:** Operate with minimum necessary permissions.
* **Defense in Depth:** Implement multiple security layers.
* **Secure Defaults:** Configure frameworks/libraries securely.

## 2. Secret Management is Critical

* **Standard:** **NEVER hardcode secrets** in source code, config files, or logs.
* **Implementation:** Use secure mechanisms: environment variables injected at runtime or dedicated secrets management systems (Vault, AWS/GCP Secret Manager).

## 3. Dependency Management Security

* **Standard:** Regularly scan dependencies for vulnerabilities using automated tools integrated into CI.
* **Policy:** CI builds **MUST FAIL** on discovery of new Critical or High severity vulnerabilities. Keep dependencies updated.

## 4. Secure Coding Practices

* Handle errors securely (no sensitive detail leakage).
* Implement proper authentication and authorization.
* Protect against common web vulnerabilities (CSRF, XSS, SQLi, etc.).
* Implement rate limiting where appropriate.

## 5. Security During Design

* Perform threat modeling for new features/services.
* Choose secure libraries and frameworks.

---

# Documentation Approach

Documentation supports understanding, usage, and maintenance, prioritizing accuracy and focusing on rationale.

## 1. Prioritize Self-Documenting Code

* **Approach:** The codebase itself (clear naming, types, structure, tests) is the primary documentation for *how* the system works. Refactor for clarity before writing explanatory comments.

## 2. README.md: The Essential Entry Point

* **Standard:** Every project/service/library **MUST** have a root `README.md`. Keep it concise and up-to-date.
* **Content:** Project Title, Description, Status Badges, Getting Started (Prerequisites, Install, Build), Running Tests, Usage/Running, Key Scripts, Architecture Overview (Link or Brief), Contribution Guide (Link), License.

## 3. Code Comments: Explaining Intent and Context (*Why*)

* **Approach:** Comments explain the *why*, not the *what* or *how*. Use for: Intent behind non-obvious code, design rationale/trade-offs, necessary context (links to issues/requirements), unavoidable workarounds.
* **Implementation:** Use standard doc formats (Go docs, TSDoc) for public APIs. **DELETE commented-out code.** Use version control history.

## 4. API Documentation: Defining Contracts

* **Internal APIs:** Primary docs are code (types, signatures) + doc comments.
* **External Service APIs:**
    * **REST:** Maintain an accurate **OpenAPI (Swagger) specification** as the definitive contract.
    * **gRPC:** The **`.proto` files** are the definitive contract. Use comments within them.

## 5. Diagrams: Visualizing Structure

* **Approach:** Use diagrams judiciously for high-level architecture or complex flows. **Prefer text-based formats** (MermaidJS, PlantUML) versioned with code. Keep diagrams focused; reference from READMEs.

## 6. Automated Changelog

* **Approach:** The `CHANGELOG.md` file is automatically generated from Conventional Commit messages during the release process. (See [Semantic Versioning and Release Automation](#semantic-versioning-and-release-automation)).

---

# Observability

Beyond logging, we strive for comprehensive observability through metrics and tracing.

## 1. Metrics

* **Goal:** Collect time-series data about system performance and behavior (e.g., request latency, error rates, resource utilization, queue depths).
* **Implementation:** Use standard metrics libraries (e.g., Prometheus client libraries, OpenTelemetry Metrics API) to instrument code. Expose metrics via standard endpoints. Focus on the RED method (Rate, Errors, Duration) for services and USE method (Utilization, Saturation, Errors) for resources.

## 2. Distributed Tracing

* **Goal:** Track requests as they propagate through distributed systems, providing visibility into call graphs, latency breakdowns, and dependencies.
* **Implementation:** Leverage context propagation (using the same correlation ID as logging) and tracing libraries (e.g., OpenTelemetry Tracing API) to generate and export trace spans.

---

# Appendices

Language-specific standards, tooling configurations, and idiomatic patterns are detailed in separate appendix documents:

* `DEVELOPMENT_PHILOSOPHY_APPENDIX_GO.md`
* `DEVELOPMENT_PHILOSOPHY_APPENDIX_TYPESCRIPT.md`
* `DEVELOPMENT_PHILOSOPHY_APPENDIX_RUST.md`
