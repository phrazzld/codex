# Development Philosophy (v2)

This document consolidates the development philosophy, principles, guidelines, and standards for our projects. It serves as a comprehensive reference for our approach to software development, intended for both human developers and AI coding agents.

## Table of Contents

- [Core Principles](#core-principles)
- [Architecture Guidelines](#architecture-guidelines)
- [Coding Standards](#coding-standards)
- [Testing Strategy](#testing-strategy)
- [Logging Strategy](#logging-strategy)
- [Security Considerations](#security-considerations)
- [Documentation Approach](#documentation-approach)
- [AI Agent Action Summary](#ai-agent-action-summary)

---

# Core Principles

This section outlines the fundamental beliefs shaping our approach to software. These principles guide our decisions in architecture, coding, testing, and documentation, aiming for software that is simple, robust, maintainable, and effective.

## 1. Simplicity First: Complexity is the Enemy

* **Principle:** Always seek the simplest possible solution that correctly meets the requirements. Actively resist complexity in all forms.
* **Rationale:** Simple code is easier to understand, debug, test, modify, and maintain. Complexity is the primary source of bugs, friction, and long-term costs. We rigorously apply YAGNI (You Ain't Gonna Need It).
* **Anti-Patterns to Avoid:** Unnecessary features, premature or overly abstract designs, overly clever/obscure code, deep nesting (> 2-3 levels), functions/methods exceeding ~50-100 lines (use as a signal to refactor), classes/modules with too many responsibilities.

## 2. Modularity is Mandatory: Do One Thing Well

* **Principle:** Construct software from small, well-defined, independent components (modules, packages, functions, services) with clear responsibilities and explicit interfaces. Strive for high internal cohesion and low external coupling. Embrace the Unix philosophy.
* **Rationale:** Modularity tames complexity, enables parallel development, independent testing/deployment, reuse, fault isolation, and easier evolution. It's essential for scalable and maintainable applications. This demands careful API design and boundary definition.

## 3. Design for Testability: Confidence Through Verification

* **Principle:** Testability is a fundamental, non-negotiable design constraint considered from the start. Structure code (clear interfaces, dependency inversion, separation of concerns) for easy and reliable automated verification. Focus tests on *what* (public API, behavior), not *how* (internal implementation).
* **Rationale:** Automated tests build confidence, prevent regressions, enable safe refactoring, and act as executable documentation. Code difficult to test often indicates poor design (high coupling, mixed concerns). *Crucially, difficulty testing is a strong signal to refactor the code under test first.* (See [Testing Strategy](#testing-strategy)).

## 4. Maintainability Over Premature Optimization: Code for Humans First

* **Principle:** Write code primarily for human understanding and ease of future modification. Clarity, readability, and consistency are paramount. Optimize *only* after identifying *actual*, *measured* performance bottlenecks.
* **Rationale:** Most time is spent reading/maintaining existing code. Premature optimization adds complexity, obscures intent, hinders debugging, and often targets non-critical paths, yielding negligible benefit at high maintenance cost. Prioritize clear naming and straightforward logic.

## 5. Explicit is Better than Implicit: Clarity Trumps Magic

* **Principle:** Make dependencies, data flow, control flow, contracts, and side effects clear and obvious. Avoid hidden conventions, global state, or complex implicit mechanisms. Leverage strong typing and descriptive naming.
* **Rationale:** Explicit code is easier to understand, reason about, debug, and refactor safely. Implicit behavior obscures dependencies, hinders tracing, and leads to unexpected side effects. Favor explicit dependency injection and rely heavily on static type checking.

## 6. Automate Everything: Eliminate Toil, Ensure Consistency

* **Principle:** Automate every feasible repetitive task: testing, linting, formatting, building, dependency management, deployment. If done manually more than twice, automate it.
* **Rationale:** Automation reduces manual error, ensures consistency, frees up developer time, provides faster feedback, and makes processes repeatable and reliable. Requires investment in robust tooling and CI/CD. (See [Coding Standards](#coding-standards)).

## 7. Document Decisions, Not Mechanics: Explain the *Why*

* **Principle:** Strive for self-documenting code (clear naming, structure, types) for the *how*. Reserve comments and external documentation primarily for the *why*: rationale for non-obvious choices, context, constraints, trade-offs.
* **Rationale:** Code mechanics change; comments detailing *how* quickly become outdated. The *reasoning* provides enduring value. Self-documenting code reduces the documentation synchronization burden. (See [Documentation Approach](#documentation-approach)).

---

# Architecture Guidelines

These guidelines translate Core Principles (especially Simplicity, Modularity, Testability) into actionable structures for maintainable, adaptable, and testable applications, primarily in Go and TypeScript.

## 1. Embrace the Unix Philosophy: Focused, Composable Units

* **Guideline:** Design components (services, libraries, modules, functions, CLIs) to "do one thing and do it well." Prefer composing smaller, specialized units over large, monolithic ones.
* **Implementation:** Think inputs -> transformation -> outputs. Resist adding unrelated responsibilities; create new components instead. Define clear contracts between units. This directly supports *Simplicity* and *Modularity*.

## 2. Strict Separation of Concerns: Isolate the Core

* **Guideline:** Ruthlessly separate core business logic/domain knowledge from infrastructure concerns (UI, DB access, network calls, file I/O, CLI parsing, 3rd-party APIs). The core should be pure and unaware of specific I/O mechanisms.
* **Implementation:** Use patterns like Hexagonal Architecture (Ports & Adapters) or Clean Architecture. Define boundaries with interfaces:
    * **Go:** Core packages (`/internal/domain`, `/internal/app`) define `interface{}` types. Infrastructure packages (`/internal/platform/database`) implement them.
    * **TypeScript:** Core modules (`src/core/`, `src/domain/`) define `interface` types. Infrastructure modules (`src/infrastructure/`) provide implementing classes.
* **Rationale:** Paramount for *Modularity* and *Design for Testability*. Allows core logic testing in isolation and swapping infrastructure with minimal core impact.

## 3. Dependency Inversion Principle: Point Dependencies Inward

* **Guideline:** High-level policy (core logic) must not depend on low-level details (infrastructure). Both depend on abstractions (interfaces defined by the core). Source code dependencies point *inwards*: infrastructure -> core.
* **Implementation:**
    * **Go:** Core defines `interface{}`. Infrastructure imports core *only* to implement interfaces or use types. Core *never* imports infrastructure. Inject dependencies (interface values) during initialization (`main.go`).
    * **TypeScript:** Core defines `interface` / `abstract class`. Use Dependency Injection (constructor injection preferred) to provide infrastructure implementations to the core. Avoid `new DatabaseClient()` inside core logic.
* **Rationale:** Enables *Separation of Concerns* and *Testability* by decoupling stable core logic from volatile infrastructure details.

## 4. Package/Module Structure: Organize by Feature, Not Type

* **Guideline:** Structure code primarily around business features/domains/capabilities, not technical types/layers. Prefer `src/orders/` over separate `src/controllers/`, `src/services/`, `src/repositories/`.
* **Heuristic:** When adding functionality, if it clearly belongs to an existing feature (e.g., updating order status -> `src/orders/`), add it there. If it represents a distinct new capability (e.g., processing payments -> `src/payments/`), create a new feature module.
* **Implementation:**
    * **Go:** Use feature-oriented packages in `/internal/` or `/pkg/`. `/cmd/` for executables. Example: `/internal/inventory/`, `/internal/checkout/`. Cross-cutting platform code: `/internal/platform/auth/`.
    * **TypeScript:** Use feature directories in `src/`. Example: `src/catalog/`, `src/userProfile/`. Shared code: `src/shared/`. Infrastructure: `src/platform/` or `src/infrastructure/`.
* **Rationale:** Enhances *Modularity* and *Maintainability*. Co-locating feature code simplifies understanding, modification, and removal. Improves cohesion, reduces coupling.

## 5. API Design: Define Explicit Contracts

* **Guideline:** Define clear, explicit, robust contracts for all APIs (internal module interactions, external REST/gRPC/GraphQL/CLIs). Document inputs, outputs, behavior, errors. Prioritize stability and versioning for external APIs.
* **Implementation:**
    * **Internal:** Leverage the type system (Go interfaces, TS `interface`/`type`), clear function signatures.
    * **External REST:** Use OpenAPI (Swagger) specification as the source of truth. Keep it accurate and versioned.
    * **External gRPC:** Define services/messages rigorously in `.proto` files. Use semantic versioning for package names.
    * **CLIs:** Provide clear help messages (`--help`), document args/flags, use consistent exit codes.
* **Rationale:** Supports *Modularity* and *Explicit is Better than Implicit*. Enables independent development/testing, reduces integration friction.

## 6. Configuration Management: Externalize Environment-Specifics

* **Guideline:** Never hardcode configuration values (DB strings, API keys/endpoints, ports, feature flags) that vary between environments or are sensitive. Externalize all such configuration.
* **Implementation:** Prefer environment variables for deployment flexibility (containers). Use config files (`.env`, YAML) for local development. Use libraries (Go: Viper; TS: `dotenv`) to load/parse/validate. Define strongly-typed config objects/structs.
* **Rationale:** Crucial for *Maintainability*, deployment flexibility, and security. Allows same artifact across environments, keeps secrets out of source control.

## 7. Consistent Error Handling: Fail Predictably and Informatively

* **Guideline:** Apply a consistent error handling strategy. Distinguish recoverable errors (invalid input, not found) from unexpected bugs (nil pointer). Propagate errors clearly, adding context judiciously. Define explicit error handling boundaries (e.g., top-level HTTP middleware) to catch, log, and translate errors into meaningful responses (HTTP status codes, standardized error payloads, exit codes).
* **Implementation:**
    * **Go:** Use standard `error` interface. Return errors explicitly. Use `errors.Is`/`errors.As`. Avoid `panic` for recoverable errors. Define custom error types or use sentinel errors (`errors.New`, `fmt.Errorf` with `%w`) for specific semantics.
    * **TypeScript:** Use `Error` object, potentially custom subclasses (`ValidationError extends Error`). Handle Promise rejections consistently (`async/await` with `try...catch`). Document potential exceptions (`@throws`). Implement error handling middleware at boundaries.
* **Rationale:** Supports *Maintainability*, robustness, operational clarity. Simplifies debugging, makes behavior predictable, helps consumers understand failures.

---

# Coding Standards

These are concrete rules for writing readable, consistent, maintainable, and less defect-prone code, directly supporting our Core Principles. Adherence is enforced through automated tooling wherever possible.

## 1. Maximize Language Strictness & Tooling Enforcement

* **Standard:** Configure compilers, linters, and formatters to their strictest practical settings. Leverage static analysis fully.
* **Tooling is Mandatory:**
    * **Formatting:** Code *must* be formatted using the standard tool (**Prettier** for TS, **gofmt/goimports** for Go) via automated checks (pre-commit hook, CI). Style is non-negotiable.
    * **Linting:** Code *must* pass the standard linter (**ESLint** for TS, **golangci-lint** for Go) with a strict, shared configuration, run via automated checks.
    * **Automation:** Pre-commit hooks and CI checks *must* run these tools. **Bypassing hooks (e.g., `git commit --no-verify`) is strictly forbidden.** Address violations properly.
    * **Custom Checks:** Tooling may include custom checks (e.g., via pre-commit hooks) to enforce specific standards like file length (e.g., warn > 500 lines, fail > 1000 lines - requiring refactoring).
* **Rationale:** Catches errors early, enforces consistency, improves readability, reduces debate, ensures diffs show logic changes. Supports *Automation* and *Explicit is Better than Implicit*.

## 2. Leverage Types Diligently: Express Intent Clearly

* **Standard:** Use the static type system fully and precisely to model data, define signatures, and establish contracts.
* **Implementation:**
    * **TypeScript:** **Strictly forbid `any`**. Use specific types, `interface`, `type`, discriminated unions, utility types (`Partial`, `Readonly`), and `unknown` appropriately. Type all function parameters, return values, variables. Enable `strict: true` in `tsconfig.json`.
    * **Go:** Use appropriate built-in types, clear `struct` types, and `interface{}` judiciously for behavior contracts (prefer small, focused interfaces).
* **Rationale:** Types are machine-checked documentation, improve clarity, reduce runtime errors, enable tooling. Supports *Explicit is Better than Implicit*.

## 3. Prefer Immutability: Simplify State Management

* **Standard:** Treat data structures as immutable whenever practical. Create new instances instead of modifying existing data in place.
* **Implementation:**
    * **TypeScript:** Use `readonly`, `ReadonlyArray<T>`. Use immutable update patterns (spread `{...obj}`, array `map`/`filter`/`reduce`). Consider libraries like Immer for complex state.
    * **Go:** Be mindful of reference types (slices, maps); copy explicitly if callers need originals unchanged. Favor value types or returning new structs over modifying receiver pointers where semantics allow.
* **Rationale:** Simplifies reasoning about state, eliminates bugs related to shared mutable state, makes changes predictable. Supports *Simplicity*.

## 4. Favor Pure Functions: Isolate Side Effects

* **Standard:** Implement core logic, transformations, and calculations as pure functions where feasible (output depends only on input, no side effects). Concentrate side effects at system edges (infrastructure adapters, command handlers).
* **Implementation:** Actively extract pure logic from functions mixing computation and side effects. Pass dependencies explicitly.
* **Rationale:** Pure functions are predictable, testable, reusable, easier to reason about. Supports *Simplicity*, *Modularity*, *Testability*.

## 5. Meaningful Naming: Communicate Purpose

* **Standard:** Choose clear, descriptive, unambiguous names for all identifiers (variables, functions, types, packages, etc.). Adhere strictly to language naming conventions.
* **Implementation:**
    * **TypeScript:** `camelCase` variables/functions, `PascalCase` types/classes/interfaces/enums.
    * **Go:** `camelCase` unexported, `PascalCase` exported. Short, lowercase package names, avoid stutter.
    * Avoid vague terms (`data`, `temp`, `handle`). Use domain terminology.
* **Rationale:** Crucial for *Maintainability* and readability. Reduces need for comments. Supports *Self-Documenting Code*.

## 6. Address Violations, Don't Suppress: Fix the Root Cause

* **Standard:** Directives to suppress linter/type errors (e.g., `// eslint-disable-line`, `@ts-ignore`, `// nolint:`, `as any`) are **forbidden** except in extremely rare, explicitly justified cases (requiring a comment explaining *why* it's safe and necessary).
* **Rationale:** Suppressions hide bugs, debt, or poor design. Fixing the root cause leads to robust, maintainable code. Supports *Maintainability* and *Explicit is Better than Implicit*.

## 7. Disciplined Dependency Management: Keep It Lean and Updated

* **Standard:** Minimize third-party dependencies. Evaluate necessity, maintenance status, license, and transitive dependencies before adding. Keep essential dependencies reasonably updated.
* **Implementation:** Regularly review/audit dependencies (`npm audit`, `go list -m all`, vulnerability checks). Remove unused dependencies (`npm prune`, `go mod tidy`). Use tools like Dependabot/Renovate Bot.
* **Rationale:** Reduces attack surface, build times, version conflicts, maintenance overhead. Supports *Simplicity* and *Maintainability*.

---

# Testing Strategy

Effective automated testing is critical for correctness, preventing regressions, enabling refactoring, providing living documentation, and driving better design, aligning with *Design for Testability* and *Modularity*.

## 1. Guiding Principles

* **Purpose:** Verify requirements, prevent regressions, enable confident, frequent deployments.
* **Clarity:** Test code *is* production code: keep it simple, clear, maintainable. Complex tests often signal complex code.
* **Behavior Focus:** Test *what* a component does via its public API, not *how* it does it internally. Resilient to refactoring.
* **Testability Drives Design:** Difficulty testing indicates the *code under test* needs refactoring first.

## 2. Test Focus and Types

* **Unit Tests:** Verify small, isolated logic units (algorithms, calculations, pure functions) *without mocking internal collaborators*. Fast feedback on logical correctness.
* **Integration / Workflow Tests (High Priority):** Verify collaboration *between* multiple internal components through defined interfaces/APIs. **Often provide the highest ROI for feature correctness.** Use real implementations of internal collaborators; mock *only* at true external system boundaries (see Mocking Policy).
* **System / End-to-End (E2E) Tests:** Validate user journeys through the deployed system (UI, public API). Use sparingly due to cost, speed, and flakiness.

## 3. Mocking Policy: Sparingly, At External Boundaries Only (CRITICAL)

Our stance on mocking is conservative to ensure tests are effective and designs are sound.

* **Minimize Mocking:** Strive for designs/tests requiring minimal mocking.
* **Mock ONLY True External System Boundaries:** Mocking is permissible *only* for interfaces/abstractions representing systems genuinely *external* to the service/application under test, where direct use is impractical/undesirable. Examples:
    * Network I/O (Third-party APIs, other microservices)
    * Databases / External Data Stores (unless using test containers/in-memory fakes)
    * Filesystem Operations
    * System Clock (use injectable abstractions)
    * External Message Brokers / Caches
* **Abstract External Dependencies First:** Always access external dependencies via interfaces defined *within* your codebase (Ports & Adapters / Dependency Inversion). Mock *these local abstractions*, not external library clients directly.
* **NO Mocking Internal Collaborators:** **It is an anti-pattern to mock classes, structs, functions, or interfaces defined *within* the same application/service solely to isolate another internal component.**
* **Refactor Instead of Internal Mocking:** Feeling the need for internal mocking signals a design flaw (high coupling, poor separation, violated DI). **The correct action is to refactor the code under test to improve its design and testability.** Techniques include:
    * Extracting pure functions from mixed-concern code.
    * Introducing interfaces at logical boundaries and using Dependency Injection.
    * Breaking down large components into smaller, focused, independently testable units.
* **Rationale:** Ensures tests verify realistic interactions, remain robust to refactoring, provide genuine confidence, and accurately indicate design health. Over-mocking hides problems and tests the mocks, not integrated behavior.

## 4. Desired Test Characteristics (FIRST)

* **Fast:** Run quickly for rapid feedback.
* **Independent / Isolated:** Run in any order, no shared state, self-contained setup/teardown.
* **Repeatable / Reliable:** Consistent pass/fail results. Eliminate non-determinism (time, concurrency, random data without seeds). No flaky tests.
* **Self-Validating:** Explicit assertions, clear pass/fail reporting.
* **Timely / Thorough:** Written alongside/before code (TDD ideal). Cover happy paths, errors, edge cases relevant to the component's responsibility.

## 5. Test Data Management

* **Clarity:** Setup reveals the scenario. Descriptive names, obvious input/output relationship.
* **Realism:** Approximate real-world data characteristics, especially for integration tests.
* **Maintainability:** Avoid duplicating setup logic. Use Test Data Builders, Factories, or helper functions.
* **Isolation:** Ensure data from one test doesn't affect others. Clean up state between tests.

---

# Logging Strategy

Consistent and effective logging is crucial for observability, debugging, and monitoring system health.

## 1. Structured Logging is Mandatory

* **Standard:** All log output *must* be structured, preferably as JSON. This enables easier parsing, filtering, and analysis by log aggregation systems.
* **Implementation:** Use standard structured logging libraries (e.g., Go: `slog`, `zerolog`, `zap`; TS: `pino`, `winston` configured for JSON). Avoid `fmt.Println` or `console.log` for operational logging.

## 2. Standard Log Levels

* **Standard:** Use standard severity levels consistently:
    * **DEBUG:** Detailed information for diagnosing specific issues during development/troubleshooting. Should be disabled in production by default.
    * **INFO:** Routine information about normal operation (e.g., request received, process started/completed, configuration loaded).
    * **WARN:** Potentially harmful situations or unexpected conditions that do not necessarily stop execution but warrant attention (e.g., recoverable errors, deprecated API usage, resource limits approached).
    * **ERROR:** Serious errors that caused an operation to fail or indicate a significant problem requiring investigation (e.g., unhandled exceptions, failed external dependencies, data corruption). Includes stack traces where appropriate.
* **Default Production Level:** Typically `INFO`.

## 3. Essential Context Fields

* **Standard:** Include relevant context in log entries to aid correlation and analysis. Minimum required fields often include:
    * Timestamp (ISO 8601 format, UTC)
    * Log Level (e.g., "info", "error")
    * Message (clear, concise description of the event)
    * Service Name / Application ID
    * Request ID / Correlation ID (See Context Propagation)
    * Error Details (for ERROR level: type, message, stack trace)
* **Optional but Useful:** User ID, Session ID, relevant business identifiers (e.g., Order ID).

## 4. What NOT to Log

* **Standard:** **Never log sensitive information**, including but not limited to:
    * Passwords, API keys, tokens, secrets
    * Personally Identifiable Information (PII) unless strictly necessary, compliant with regulations, and appropriately secured/masked.
    * Full credit card numbers, bank details.
    * Verbose internal data structures unless specifically for DEBUG level.

## 5. Context Propagation

* **Standard:** For distributed systems or complex request flows, propagate a unique correlation ID (e.g., Request ID, Trace ID) across service boundaries and asynchronous operations (e.g., via HTTP headers, message queue metadata). Include this ID in all related log entries.
* **Implementation:** Use context propagation mechanisms provided by frameworks or libraries (e.g., Go `context.Context`, OpenTelemetry).

---

# Security Considerations

Security is not an afterthought; it must be integrated throughout the development lifecycle.

## 1. Core Principles

* **Input Validation:** Never trust external input (API requests, user input, file uploads, data from other services). Validate type, format, length, range, and allowed characters rigorously at the boundary.
* **Output Encoding:** Encode data appropriately for the context where it is rendered or used (e.g., HTML entity encoding for web output, parameterized queries for SQL) to prevent injection attacks (XSS, SQLi).
* **Principle of Least Privilege:** Services, processes, and users should operate with the minimum permissions necessary to perform their function. Limit access to data, resources, and system capabilities.
* **Defense in Depth:** Implement multiple layers of security controls, assuming that any single layer might fail.
* **Secure Defaults:** Configure frameworks and libraries with secure settings by default.

## 2. Secret Management

* **Standard:** **Never hardcode secrets** (API keys, passwords, certificates, tokens) in source code, configuration files, or log output.
* **Implementation:** Use secure mechanisms like environment variables injected at runtime or dedicated secrets management systems (e.g., HashiCorp Vault, AWS Secrets Manager, GCP Secret Manager).

## 3. Dependency Management Security

* **Standard:** Regularly scan dependencies for known vulnerabilities.
* **Implementation:** Integrate automated vulnerability scanning tools (`npm audit`, `yarn audit`, `govulncheck`, Snyk, Dependabot security alerts) into the CI/CD pipeline. Treat critical vulnerabilities as build failures. Keep dependencies updated.

## 4. Secure Coding Practices

* Handle errors securely (avoid leaking sensitive details).
* Implement proper authentication and authorization checks.
* Protect against common web vulnerabilities (CSRF, insecure redirects, etc.) if applicable.
* Consider rate limiting and resource usage limits.
* Be mindful of potential denial-of-service vectors.

## 5. Security During Design

* Consider potential threats and abuse cases during the design phase (threat modeling).
* Choose secure libraries and frameworks.
* Design APIs with security in mind (proper authentication, authorization, input validation).

---

# Documentation Approach

Effective communication and knowledge sharing through documentation that is accurate, maintainable, and focused on rationale. Aligns with *Explicit is Better than Implicit* and *Document Decisions, Not Mechanics*.

## 1. Prioritize Self-Documenting Code

* **Approach:** The codebase itself is the primary documentation for *how* the system works. Achieved via:
    * **Clear Naming** ([Coding Standards](#coding-standards))
    * **Strong Typing** ([Coding Standards](#coding-standards))
    * **Logical Structure / Modularity** ([Architecture Guidelines](#architecture-guidelines))
    * **Readability** (Formatting, Linting - [Coding Standards](#coding-standards))
    * **Well-Written Tests** ([Testing Strategy](#testing-strategy))
* **Rationale:** Code is the source of truth. External docs for mechanics drift easily. Refactor code for clarity before writing extensive explanatory comments.

## 2. README.md: The Essential Entry Point

* **Approach:** Every project/service/library *must* have a root `README.md`. Keep it concise and up-to-date.
* **Standard Structure:** Project Title, Brief Description, Status (Optional Badges), Getting Started (Prerequisites, Install, Build), Running Tests, Usage/Running the App, Key Scripts/Commands, Architecture Overview (Optional Brief/Link), How to Contribute (Optional Link), License.
* **Rationale:** Lowers barrier to entry for understanding, setup, running, testing, and contributing.

## 3. Code Comments: Explaining Intent and Context (*Why*)

* **Approach:** Comments explain the *why*, not the *what* or *how*. Use them for:
    * Intent behind non-obvious code.
    * Rationale for specific design choices/trade-offs.
    * Necessary context not apparent from code (links to requirements, issues).
    * Unavoidable workarounds or known limitations.
* **Implementation:**
    * Refactor unclear code before commenting on its mechanics.
    * Use standard doc formats (`//` Go docs, `/** */` TSDoc) for public APIs.
    * **Delete commented-out code.** Use version control.
* **Rationale:** Good code explains itself mechanically. Good comments provide insight into reasoning. Redundant/outdated comments mislead.

## 4. API Documentation: Defining Contracts and Usage

* **Approach:** Public APIs (internal or external) must be clearly documented. Leverage automated tooling where possible.
* **Internal Module/Package APIs:** Primary docs are code (types, signatures) supplemented by doc comments (Go docs, TSDoc) on exported identifiers (purpose, params, returns, errors/panics/throws).
* **External Service APIs:**
    * **REST APIs:** Maintain an accurate **OpenAPI (Swagger) specification** (`openapi.yaml`) as the definitive contract.
    * **gRPC APIs:** The **`.proto` files** are the definitive contract. Use comments within them.
* **Rationale:** Essential for reliable integration. Automated generation reduces drift. Supports *Explicit is Better than Implicit*.

## 5. Diagrams: Visualizing Structure and Complex Flows

* **Approach:** Use diagrams judiciously for high-level architecture, component interactions, complex flows. Prioritize easy-to-maintain formats versioned with code.
* **Tools & Storage:**
    * **Preferred:** Text-based tools embeddable in Markdown (**MermaidJS**, PlantUML).
* **Rationale:** Quickly convey structure. Maintainable formats prevent outdated burdens. Keep diagrams focused; reference them from READMEs.

---

# AI Agent Action Summary

This is a concise summary of critical, non-negotiable instructions for AI coding agents:

1.  **Format Code:** Always format code using the project's configured formatter (Prettier for TS, gofmt/goimports for Go) before finalizing output.
2.  **Pass Linter:** Ensure generated code passes all checks from the project's configured linter (ESLint for TS, golangci-lint for Go) without suppression directives.
3.  **Strict Types:** Use specific types. **`any` is forbidden in TypeScript.** Enable and adhere to strict type checking (`strict: true` in `tsconfig.json`).
4.  **No Linter/Type Suppressions:** Do not use `@ts-ignore`, `eslint-disable`, `// nolint:`, or similar directives. Fix the underlying code issue.
5.  **Follow Package Structure:** Adhere strictly to the "Package by Feature" guideline. Place code in the correct feature module/package.
6.  **Mocking Policy:** Mock *only* true external system boundaries defined by local interfaces. **Never mock internal collaborators.** If internal mocking seems needed, flag the code for refactoring.
7.  **Immutability:** Prefer immutable data structures and update patterns.
8.  **Meaningful Naming:** Use clear, descriptive names following language conventions.
9.  **Externalize Config:** Do not hardcode configuration values or secrets.
10. **Structured Logging:** Use the configured structured logging library. Do not use `console.log` or `fmt.Println` for operational logs. Never log secrets.
11. **Security:** Validate all external input. Encode output appropriately. Do not hardcode secrets.
12. **File Length:** Adhere to file length guidelines (e.g., aim for < 500 lines, flag > 1000 lines for mandatory refactoring).
