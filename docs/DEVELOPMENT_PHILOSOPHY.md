# Development Philosophy

This document consolidates all development philosophy principles, guidelines, and standards from the project. It provides a comprehensive reference for our approach to software development.

## Table of Contents

- [Core Principles](#core-principles)
- [Architecture Guidelines](#architecture-guidelines)
- [Coding Standards](#coding-standards)
- [Testing Strategy](#testing-strategy)
- [Documentation Approach](#documentation-approach)

---

# Core Principles

This section outlines the fundamental beliefs and guiding principles that shape our approach to software design, development, and maintenance. These principles are the bedrock upon which our more specific guidelines for architecture, coding, testing, and documentation are built. Adhering to these principles helps us create software that is simple, robust, maintainable, and effective.

## 1. Simplicity First: Complexity is the Enemy

**Principle:** Always seek the simplest possible solution that correctly meets the requirements. Actively resist complexity in all its forms – unnecessary features, premature abstractions, overly clever code, or convoluted layers of indirection.

**Rationale:** Simplicity is the ultimate sophistication. Simple code is drastically easier to understand, reason about, debug, test, modify, and maintain. Complexity is the primary source of bugs, development friction, and long-term maintenance costs.

**Implications:** We rigorously apply principles like YAGNI (You Ain't Gonna Need It). We question the value proposition of every added feature or abstraction. We favor straightforward, readable code over compact but obscure implementations. Simplicity is a constant goal, not an occasional optimization.

## 2. Modularity is Mandatory: Do One Thing Well

**Principle:** Construct software from small, well-defined, independent components (modules, packages, functions, services) with clear responsibilities and explicit interfaces. Strive for high internal cohesion (logic within a component is strongly related) and low external coupling (components have minimal dependencies on the internals of others). Embrace the Unix philosophy: build focused components that perform a single task well, and compose them to create larger systems.

**Rationale:** Modularity tames complexity. It enables parallel development, allows for independent testing and deployment, facilitates code reuse, improves fault isolation, and makes the overall system easier to understand and evolve. It is essential for building scalable and maintainable applications.

**Implications:** This demands careful attention to API design and boundary definition between components. It enforces a strong separation of concerns and promotes composability. Our architectural guidelines are heavily influenced by this principle.

## 3. Design for Testability: Confidence Through Verification

**Principle:** Testability is not an optional add-on or a phase that happens "later"; it is a fundamental, non-negotiable design constraint considered from the very beginning. Structure code—using techniques like clear interfaces, dependency inversion, and separation of concerns—so that its behavior can be easily and reliably verified through automated tests. Focus tests on *what* the code achieves (its public API, its behavior, its contracts), not *how* it achieves it (internal implementation details).

**Rationale:** Automated tests are crucial for building confidence, preventing regressions, enabling safe refactoring, and acting as precise, executable documentation. Code that is inherently difficult to test without elaborate mocking or complex setup is often a sign of poor design (e.g., high coupling, mixed concerns).

**Implications:** Testability requirements directly influence architectural choices. We prefer integration or workflow tests that verify component interactions through public APIs over unit tests that require mocking internal collaborators. Difficulty in testing is a strong signal to refactor the *code under test* first.

## 4. Maintainability Over Premature Optimization: Code for Humans First

**Principle:** Write code primarily for human understanding and ease of future modification. Clarity, readability, and consistency are paramount. Aggressively resist the urge to optimize code for performance before identifying *actual*, *measured* performance bottlenecks in realistic scenarios.

**Rationale:** The vast majority of software development time is spent reading and maintaining existing code, not writing new code from scratch. Premature optimization often introduces significant complexity, obscures the original intent, makes the code harder to debug and modify, and frequently targets non-critical performance paths, yielding negligible real-world benefit while incurring high maintenance costs.

**Implications:** We prioritize clear, descriptive naming. We enforce consistent code style through automated tools. We favor straightforward algorithms and data structures unless profiling proves a more complex approach is necessary. Optimization is a targeted activity driven by data, not speculation.

## 5. Explicit is Better than Implicit: Clarity Trumps Magic

**Principle:** Make dependencies, data flow, control flow, contracts, and side effects as clear and obvious as possible within the code. Avoid "magic" behavior that relies on hidden conventions, global state modifications, or complex implicit mechanisms. Leverage the power of strong typing systems and descriptive naming.

**Rationale:** Explicit code is easier to understand, reason about, debug, and refactor safely. Implicit behavior obscures dependencies, makes tracing execution paths difficult, and often leads to unexpected side effects or coupling.

**Implications:** We favor techniques like explicit dependency injection over global singletons or service locators. We rely heavily on static type checking (TypeScript, Go types) to define and enforce contracts. Function signatures should accurately reflect dependencies and potential side effects where possible.

## 6. Automate Everything: Eliminate Toil, Ensure Consistency

**Principle:** Automate every feasible repetitive task in the development lifecycle. This includes, but is not limited to: running tests, linting code for style and potential errors, formatting code for consistency, building artifacts, managing dependencies, and deploying applications. If a task is performed manually more than a couple of times, it's a candidate for automation.

**Rationale:** Automation drastically reduces the potential for manual error, ensures consistency across different developers and environments, frees up valuable developer time for creative problem-solving, provides faster feedback loops, and makes processes repeatable and reliable.

**Implications:** This requires an upfront and ongoing investment in robust build scripts, CI/CD pipelines, testing infrastructure, and standardized development environment configurations. The goal is to make the correct way the easy way.

## 7. Document Decisions, Not Mechanics: Explain the *Why*

**Principle:** Strive for code that is largely self-documenting through clear naming, logical structure, and effective use of the type system – this covers the *how*. Reserve comments and external documentation primarily for explaining the *why*: the rationale behind a non-obvious design choice, the context surrounding complex logic, critical constraints, or the trade-offs considered.

**Rationale:** The mechanics of code change frequently, causing comments detailing the "how" to become quickly outdated and misleading. The *reasoning* behind a design, however, provides enduring value for maintainers trying to understand the system's evolution and constraints. Self-documenting code reduces the burden of keeping separate documentation synchronized.

**Implications:** We prioritize writing clean, expressive code. Comments should add value by explaining intent or context. When important, document key design decisions to track the evolution of the project's design and justifications for significant choices.

---

# Architecture Guidelines

This section translates our Core Principles—particularly Simplicity, Modularity, and Testability—into actionable guidelines for structuring our software applications. Architecture is not about rigid dogma, but about making conscious design choices that lead to systems that are maintainable, adaptable, testable, and easy to reason about. These guidelines provide a default approach optimized for building focused, composable, and robust applications primarily in Go and TypeScript.

## 1. Embrace the Unix Philosophy: Build Focused, Composable Units

**Guideline:** Design components (services, libraries, modules, functions, CLIs) to "do one thing and do it well." Aim for minimal, well-defined responsibilities, clear inputs, and predictable outputs for each unit. Prefer building larger systems by composing these smaller, specialized units rather than creating expansive, monolithic entities that attempt to do too much.

**Rationale:** Directly embodies *Simplicity* and *Modularity*. Focused components are significantly easier to understand, develop, test independently, deploy, scale, and even replace entirely. Composition provides flexibility and encourages reuse, leading to more resilient and adaptable systems.

**Implementation:** Think in terms of clear data flows: inputs -> transformation -> outputs. Resist the temptation to add unrelated responsibilities to an existing component; create a new, focused one instead. Define clear boundaries and contracts between composed units.

## 2. Strict Separation of Concerns: Isolate the Core

**Guideline:** Ruthlessly separate the application's core business logic and domain knowledge from its infrastructure concerns. Infrastructure includes anything related to external interactions: UI, database access, network calls (HTTP clients/servers), file system operations, CLI argument parsing, third-party API integrations, etc. The core logic should remain "pure," unaware of the specific mechanisms used for I/O or external communication.

**Rationale:** This is paramount for *Modularity* and *Design for Testability*. The core business rules—the most valuable part of the application—can be developed and tested in complete isolation, without needing slow or complex setups (like databases or web servers). It allows infrastructure details to be changed or replaced (e.g., swapping a REST API for gRPC, changing database vendors) with minimal impact on the stable core logic.

**Implementation:** Employ architectural patterns that enforce this separation, such as Hexagonal Architecture (Ports & Adapters), Clean Architecture, or even a well-defined Layered Architecture. The key is defining clear boundaries, typically using interfaces:
* **Go:** Core logic packages (e.g., `/internal/domain`, `/internal/app`) define `interface{}` types representing necessary collaborations (e.g., `UserRepository`, `OrderNotifier`). Infrastructure packages (e.g., `/internal/platform/database`, `/internal/platform/httpadapter`) implement these interfaces.
* **TypeScript:** Core logic modules (`src/core/`, `src/domain/`) define `interface` types or rely on constructor parameters typed with interfaces. Infrastructure modules (`src/infrastructure/`, `src/platform/`) provide concrete classes that implement these interfaces.

## 3. Dependency Inversion Principle: Point Dependencies Inward

**Guideline:** Ensure that high-level policy (core application/business logic) does not depend directly on low-level details (infrastructure). Instead, both should depend on abstractions (interfaces defined by the core). Consequently, source code dependencies must always point *inwards*, from outer layers (infrastructure) towards the central core logic. Infrastructure code implements interfaces defined *in* the core.

**Rationale:** This principle is the mechanism that enables effective *Separation of Concerns* and *Testability*. It decouples the stable, high-value core logic from volatile, low-level implementation details. This makes the system more flexible, maintainable, and robust against changes in external technologies or libraries.

**Implementation:**
* **Go:** Core packages define `interface{}` types. Infrastructure packages `import` core packages solely to implement those interfaces or use core data types. Crucially, core packages **never** import infrastructure packages. Dependencies are typically "injected" (passed as interface values) into core components during application initialization (e.g., in `main.go` or a setup function).
* **TypeScript:** Core modules define `interface` or `abstract class` contracts. Use Dependency Injection (constructor injection is preferred for its explicitness) to provide concrete infrastructure implementations (classes implementing the core interfaces) to the core logic components. Avoid `new DatabaseClient()` or similar infrastructure instantiation *within* core business logic files.

## 4. Package/Module Structure: Organize by Feature, Not Type

**Guideline:** Structure your codebase primarily around business features, domains, or capabilities, rather than grouping files by their technical type or layer. For instance, prefer `src/orders/` (containing order-related domain logic, data access, handlers, etc.) over separate `src/controllers/`, `src/services/`, `src/repositories/` directories containing fragments from many different features.

**Rationale:** Enhances *Modularity* and *Maintainability*. Co-locating all code related to a specific feature makes it significantly easier to find, understand, and modify that feature's functionality. It improves cohesion within feature modules and reduces coupling between unrelated features. This structure also simplifies tasks like refactoring or even removing a feature entirely.

**Implementation:**
* **Go:** Use clear, feature-oriented package names within `/internal/` (for application-specific code) or `/pkg/` (for reusable library code). The `/cmd/` directory contains the `main` packages for executables. Example: `/internal/inventory/`, `/internal/checkout/`, `/internal/platform/auth/` (for cross-cutting platform concerns).
* **TypeScript:** Use directories within `src/` to delineate features or domains. Example: `src/catalog/`, `src/userProfile/`, `src/shared/` (for truly cross-cutting code). Infrastructure code might live in a dedicated `src/platform/` or `src/infrastructure/` directory, organized internally as needed.

## 5. API Design: Define Explicit Contracts

**Guideline:** Whether designing internal APIs between software modules or external APIs exposed by services (REST, gRPC, GraphQL, CLIs), define clear, explicit, and robust contracts. Precisely document expected inputs, outputs, behavior, invariants, and potential error conditions. For external APIs, prioritize stability, adopt a clear versioning strategy early, and consider operational aspects like idempotency for state-changing operations.

**Rationale:** Supports *Modularity* and *Explicit is Better than Implicit*. Well-defined contracts are essential for enabling independent development, testing, and evolution of different system components or services. They reduce integration friction and serve as crucial documentation.

**Implementation:**
* **Internal APIs:** Leverage the type system. Use Go interfaces or TypeScript `interface`/`type` definitions and clear function signatures.
* **External REST APIs:** Use the OpenAPI (Swagger) specification as the source of truth. Keep the specification accurate and versioned. Consider tools for generating server/client code or documentation from the spec.
* **External gRPC APIs:** Define services and messages rigorously using `.proto` files. Use semantic versioning for Protobuf package names.
* **CLIs:** Provide clear help messages (`--help` flag), document arguments and flags, and ensure consistent exit codes.

## 6. Configuration Management: Externalize Environment-Specifics

**Guideline:** Never hardcode configuration values—especially those that vary between environments (development, testing, production) or contain sensitive information—directly within the source code. This includes database connection strings, external API endpoints, API keys, ports, feature flags, etc. Externalize all such configuration.

**Rationale:** Crucial for *Maintainability*, deployment flexibility, and security. Externalized configuration allows the same compiled artifact or codebase to run correctly in different environments without modification. It keeps secrets out of version control and simplifies configuration updates.

**Implementation:** Prefer environment variables for deployment flexibility (especially in containerized environments). Use configuration files (e.g., `.env`, YAML, TOML) for local development convenience. Employ libraries (e.g., Viper, koanf in Go; `dotenv`, node-config in TypeScript) to load, parse, and validate configuration from multiple sources. Define strongly-typed configuration objects/structs within the application.

## 7. Consistent Error Handling: Fail Predictably and Informatively

**Guideline:** Establish and consistently apply a clear error handling strategy throughout the application. Distinguish between expected, recoverable errors (e.g., invalid user input, resource not found) and unexpected, potentially fatal bugs (e.g., nil pointer dereference, unhandled exceptions). Propagate errors clearly, adding contextual information when helpful, but avoid excessive nesting that obscures the root cause. Define explicit error handling boundaries (e.g., top-level HTTP middleware, message queue consumers, main function) where errors are caught, logged appropriately, and translated into meaningful responses or operational signals (e.g., HTTP status codes, standardized error JSON payloads, process exit codes).

**Rationale:** Supports *Maintainability*, robustness, and operational clarity. Consistent error handling makes debugging significantly easier and application behavior more predictable. Informative error reporting helps consumers (API clients, users, operators) understand failures. Prevents unexpected crashes due to unhandled errors.

**Implementation:**
* **Go:** Embrace the standard `error` interface. Return errors explicitly from functions that can fail. Use `errors.Is` and `errors.As` (introduced in Go 1.13) for inspecting error chains. Avoid `panic` for recoverable error conditions; reserve it for truly exceptional, unrecoverable situations. Define custom error types or use sentinel errors (via `errors.New` or `fmt.Errorf` with `%w`) when specific error semantics need to be communicated programmatically.
* **TypeScript:** Utilize the standard `Error` object and potentially create custom error subclasses (e.g., `ValidationError extends Error`, `NotFoundError extends Error`) for specific failure modes. Handle Promise rejections consistently, typically using `async/await` with `try...catch` blocks. Clearly document potential exceptions or rejections in function/method signatures (e.g., using TSDoc `@throws`). Implement error handling middleware or wrappers at application boundaries to catch unhandled errors, log them, and return appropriate responses.

---

# Coding Standards

This section defines the concrete rules, conventions, and best practices for writing code day-to-day in our projects. Adherence to these standards is essential for creating code that is readable, consistent, predictable, maintainable, and less prone to defects. These standards directly support our Core Principles, particularly aiming for Simplicity, Maintainability, and Explicit code.

## 1. Maximize Language Strictness: Catch Errors Early

**Standard:** Configure language compilers, interpreters, and static analysis tools to their strictest practical settings to leverage the full power of static analysis and type checking.

**Rationale:** This allows us to catch potential errors, inconsistencies, and questionable patterns at compile-time or lint-time, long before they manifest as runtime bugs. It supports the *Explicit is Better than Implicit* principle by making assumptions visible and verifiable.

**Implementation:**
* **TypeScript:** Set `strict: true` in `tsconfig.json`. This enables a suite of essential checks (`noImplicitAny`, `strictNullChecks`, etc.). Consider enabling further strictness flags like `noUnusedLocals`, `noUnusedParameters`, `noImplicitReturns` based on project needs.
* **Go:** Rely on the standard Go compiler checks (`go build`), `go vet` for identifying suspicious constructs, and a comprehensive suite of linters configured via `golangci-lint`.
* Standardize these configurations (`tsconfig.json`, `.golangci.yml`) across projects and include them in version control.

## 2. Leverage Types Diligently: Express Intent Clearly

**Standard:** Utilize the static type system fully and precisely to model data structures, define function signatures, and establish clear contracts between different parts of the code.

**Rationale:** Types serve as invaluable, machine-checked documentation. They improve code clarity, significantly reduce entire classes of runtime errors (e.g., type mismatches, null pointer exceptions), and enable powerful tooling like autocompletion and safe refactoring. This directly supports *Explicit is Better than Implicit*.

**Implementation:**
* **TypeScript:** **Strictly forbid the use of `any`**. Employ specific built-in types, custom `interface` definitions, `type` aliases, discriminated unions, utility types (`Partial`, `Readonly`, etc.), and `unknown` where type information is genuinely absent initially. Type all function parameters, return values, and variable declarations.
* **Go:** Use appropriate built-in types. Define clear `struct` types for data aggregation. Use `interface{}` types judiciously to define behavior contracts, adhering to the Interface Segregation Principle (preferring smaller, focused interfaces).

## 3. Prefer Immutability: Simplify State Management

**Standard:** Whenever practical, treat data structures and objects as immutable. Instead of modifying existing data in place, create and return new instances with the updated state.

**Rationale:** Immutability significantly simplifies reasoning about program state, as data doesn't change unexpectedly out from underfoot. It eliminates a large category of bugs related to shared mutable state, especially in concurrent or asynchronous scenarios, and makes state changes predictable. Supports *Simplicity*.

**Implementation:**
* **TypeScript:** Use the `readonly` modifier for properties and `ReadonlyArray<T>` for arrays. Employ immutable update patterns (e.g., object spread `{...obj, prop: newValue}`, array methods like `map`, `filter`, `reduce` which return new arrays). Consider libraries like Immer for managing complex immutable state updates ergonomically.
* **Go:** Be conscious that slices and maps are reference types. When passing them to functions, understand that modifications within the function will affect the original data; copy them explicitly if the caller requires the original to remain unchanged. Favor value types or return new struct instances instead of modifying receiver pointers when the type's semantics allow for immutability.

## 4. Favor Pure Functions: Isolate Side Effects

**Standard:** Strive to implement core logic, data transformations, and calculations as pure functions whenever feasible. A pure function's output depends *only* on its input arguments, and it produces *no* observable side effects (no I/O, no mutation of external state). Concentrate necessary side effects at the edges of the system (e.g., in infrastructure adapters, command handlers).

**Rationale:** Pure functions are the simplest building blocks. They are inherently predictable, deterministic, easy to test in isolation (no setup or mocking required), highly reusable, and make code much easier to reason about. Supports *Simplicity*, *Modularity*, and *Testability*.

**Implementation:** Actively identify opportunities to extract pure computational logic from functions that currently mix calculations with side effects. Pass dependencies explicitly rather than relying on global state.

## 5. Meaningful Naming: Communicate Purpose

**Standard:** Choose clear, descriptive, and unambiguous names for all identifiers (variables, constants, functions, methods, classes, interfaces, types, modules, packages, files). Names should effectively communicate the entity's purpose and usage within its context. Adhere strictly to the established naming conventions of the language.

**Rationale:** Code is read far more often than it's written. Meaningful names are arguably the most crucial factor in code *Maintainability* and readability, reducing the need for explanatory comments and lowering cognitive load. Supports *Self-Documenting Code*.

**Implementation:**
* **TypeScript:** `camelCase` for variables, parameters, functions. `PascalCase` for classes, interfaces, type aliases, enums.
* **Go:** `camelCase` for unexported identifiers (internal to package). `PascalCase` for exported identifiers (visible outside package). Package names should be short, lowercase, and meaningful, avoiding underscores or camelCase. Avoid stutter (e.g., prefer `package user; type Profile struct{}` over `package user; type UserProfile struct{}`).
* Avoid vague terms like `data`, `info`, `temp`, `handle`, `process` unless the scope is extremely limited and context makes the meaning obvious. Use domain-specific terminology where appropriate.

## 6. Mandatory Code Formatting: Ensure Consistency

**Standard:** All code committed to the repository *must* be automatically formatted using the designated standard tool for the language. Formatting style is not subject to individual preference or debate.

**Rationale:** Enforces a consistent visual style across the entire codebase, drastically improving readability and reducing cognitive friction when switching between files or authors. Eliminates time wasted on style debates in code reviews. Ensures code diffs only show substantive logical changes. Supports *Maintainability* and *Automation*.

**Implementation:**
* **TypeScript:** **Prettier** is mandatory. Configure it via a `.prettierrc.js` (or similar) file checked into the repository.
* **Go:** **`gofmt`** or **`goimports`** (preferred, as it includes `gofmt` and manages imports) is mandatory and non-negotiable.
* Integrate formatters into pre-commit hooks and CI pipeline checks to enforce compliance automatically.

## 7. Mandatory Linting: Catch Problems Proactively

**Standard:** All code committed to the repository *must* pass analysis by the designated standard linter(s) using a strict, shared configuration. Pre-commit hooks must **never** be bypassed with `--no-verify`.

**Rationale:** Linters act as automated code reviewers, identifying potential bugs, anti-patterns, stylistic inconsistencies, performance issues, and deviations from best practices *before* they are manually reviewed or merged. This improves overall code quality, consistency, and *Maintainability*. Supports *Automation*.

**Implementation:**
* **TypeScript:** **ESLint** is mandatory, configured with relevant plugins (e.g., `@typescript-eslint/eslint-plugin`, framework-specific plugins, accessibility plugins). A shared `.eslintrc.js` (or similar) configuration file must be checked into the repository.
* **Go:** **`golangci-lint`** is mandatory. A shared `.golangci.yml` configuration file specifying the enabled linters and their settings must be checked into the repository. Aim for a comprehensive and strict set of enabled linters.
* Integrate linting into pre-commit hooks and CI pipeline checks, treating violations as build failures.
* **IMPORTANT:** It is *strictly forbidden* to bypass pre-commit hooks with `git commit --no-verify`. Address issues properly rather than circumventing checks.

## 8. Address Violations, Don't Suppress: Fix the Root Cause

**Standard:** Directives to suppress linter warnings or type checker errors (e.g., `// eslint-disable-line`, `@ts-ignore`, `// nolint:`, type assertions like `as any` or unsafe conversions) should be avoided at all costs. Investigate the underlying issue and refactor the code to satisfy the check correctly.

**Rationale:** Suppression mechanisms often hide genuine bugs, technical debt, or poor design choices. Bypassing these checks defeats their purpose and degrades code quality and safety over time. Fixing the root cause leads to more robust, maintainable, and understandable code. Supports *Maintainability* and *Explicit is Better than Implicit*.

**Implementation:** Legitimate exceptions are extremely rare and require explicit justification via a code comment explaining *why* the suppression is necessary and safe. Significant or recurring patterns requiring suppression should be discussed and documented where appropriate. Treat suppressions as code smells requiring scrutiny.

## 9. Purposeful Comments: Explain the *Why*

**Standard:** Write comments primarily to explain the *intent*, *rationale*, or *context* behind code that might otherwise be non-obvious. Focus on the "why," not the "what" or "how"—the code itself should clearly express the mechanics. Avoid comments that simply paraphrase the code. Use standard documentation comment formats for public APIs.

**Rationale:** Well-written code minimizes the need for comments. Valuable comments provide context that cannot be directly inferred from the code, such as reasoning behind specific design choices, trade-offs made, or links to external requirements or issues. Supports *Self-Documenting Code* and *Maintainability*.

**Implementation:**
* Before writing a comment to explain *how* code works, try to refactor the code to make its mechanics clearer.
* Delete commented-out code; rely on version control history instead.
* **TypeScript:** Use TSDoc (`/** ... */`) for exported functions, classes, types, etc., to enable documentation generation and editor tooling.
* **Go:** Use standard Go doc comments (`// ...`) preceding exported identifiers for discoverability via `godoc`.

## 10. Disciplined Dependency Management: Keep It Lean and Updated

**Standard:** Minimize the number of third-party dependencies introduced into a project. Each external dependency represents a trade-off, adding potential complexity, security risks, maintenance overhead, and licensing considerations. Keep essential dependencies reasonably up-to-date.

**Rationale:** Fewer dependencies result in a smaller attack surface, faster build times, less potential for version conflicts or "dependency hell," and generally easier long-term maintenance and upgrades. Supports *Simplicity* and *Maintainability*.

**Implementation:**
* Thoroughly evaluate the necessity and value proposition before adding any new dependency. Can the functionality be achieved reasonably with the standard library or existing dependencies?
* Prefer dependencies that are well-maintained, widely used, have compatible licenses, and minimal transitive dependencies.
* Regularly review and audit dependencies (`npm audit`, `yarn audit`, `go list -m all`, checking for vulnerabilities).
* Keep `package.json` / `go.mod` files tidy and remove unused dependencies (`npm prune`, `go mod tidy`).
* Utilize tools like Dependabot or Renovate Bot to help manage dependency updates systematically.

---

# Testing Strategy

This section outlines our philosophy and strategy for automated testing. Effective testing is critical for ensuring software correctness, preventing regressions, enabling confident refactoring, providing living documentation, and ultimately driving better software design. Our approach aligns directly with our Core Principles, especially *Design for Testability* and *Modularity*.

## 1. Guiding Principles: Why and How We Test

Our testing efforts are guided by the following fundamental principles:

* **Purpose:** Tests exist primarily to verify that the software meets its functional requirements reliably, to prevent regressions as the codebase evolves, and to increase our confidence in deploying changes frequently and safely.
* **Simplicity & Clarity:** Test code *is* production code. It must be simple, clear, concise, and maintainable. Overly complex test setups or convoluted assertions often indicate complexity or poor design in the code under test itself.
* **Behavior Over Implementation:** Tests should primarily validate the observable *behavior* of a component through its public interface or API, not its internal implementation details. Testing behavior makes tests more resilient to refactoring and less brittle.
* **Testability is a Design Constraint:** We do not write code and *then* figure out how to test it. Testability is a primary consideration *during* design and implementation. **Crucially: If code proves difficult to test without resorting to extensive mocking of internal collaborators, this is a strong signal that the *code under test* likely needs refactoring (e.g., to improve separation of concerns, clarify interfaces, or reduce coupling) *before* attempting to write complex tests.**

## 2. Test Focus and Types: The Testing Landscape

We employ different types of automated tests, strategically focusing our efforts where they provide the most value and confidence relative to their cost (in terms of writing, execution time, and maintenance).

* **Unit Tests:** Highly focused tests verifying small, isolated pieces of logic. (See Section 3).
* **Integration / Workflow Tests:** Verify the collaboration *between* multiple components or modules through their defined interfaces. **These often provide the highest return on investment for ensuring application features work correctly.** (See Section 4).
* **End-to-End (E2E) Tests:** Validate complete user journeys or critical paths through the entire deployed system (e.g., via UI automation or public API calls). Used sparingly due to their higher cost, slower execution, and potential for flakiness.

While the "Testing Pyramid" is a common model, we prioritize *effectiveness*. We favor integration/workflow tests over heavily mocked unit tests when verifying component interactions.

## 3. Unit Testing Approach: Verifying Isolated Logic

Unit tests are most valuable for verifying the correctness of specific algorithms, complex calculations, data transformations, or other logic units that can be tested in relative isolation.

* **Scope:** Test a single function, method, or a small, cohesive set of functions/methods (e.g., a small utility class or struct) in isolation from its *internal* collaborators.
* **Dependencies:** **Crucially, do not mock internal collaborators** (other components, classes, structs, functions defined *within* the same application or service). If a piece of code requires extensive internal mocking to be tested, it's a design smell – refactor the code (see Principle 1d and Section 5). Abstracted *external* dependencies may be mocked according to the Mocking Policy (Section 5).
* **Goal:** Verify the logical correctness of the unit under test, including its handling of various inputs, outputs, edge cases, and boundary conditions. Ideal candidates are pure functions.
* **Rationale:** Unit tests provide fast, precise feedback on the correctness of isolated logic blocks. Keeping them truly "unit" (without internal mocks) ensures they are robust and don't hinder refactoring.
* **Implementation:**
    * **Go:** Use the standard `testing` package. Table-driven tests are excellent for covering multiple input/output scenarios concisely. Use standard assertions or libraries like `testify/assert` for clarity.
    * **TypeScript:** Use test runners like Jest or Vitest. Test function inputs/outputs directly. Utilize the framework's assertion matchers for clear and expressive checks.

## 4. Integration / Workflow Testing Approach (High Priority): Verifying Collaboration

These tests ensure that distinct parts of our application work together correctly to fulfill a feature requirement or use case. They operate at a higher level than unit tests, focusing on the interactions and contracts *between* components.

* **Scope:** Test the collaboration between two or more components/modules/layers through their public APIs or interfaces. Examples: Testing an HTTP handler's interaction with its underlying service; testing a service's interaction with its repository abstraction; testing a workflow involving multiple services.
* **Dependencies:** Use *real* implementations of internal collaborators whenever practical. Mocking should *only* occur at true external system boundaries as defined by our Mocking Policy (Section 5). For example, when testing `HTTP Handler -> Service -> Repository` flow, use the real `Service` implementation. Mock the `Repository` interface *only if* it represents an external database or API call.
* **Goal:** Verify that components integrate correctly, data flows accurately between them, contracts are honored, side effects occur as expected, and key user/system workflows produce the correct outcomes (including error handling).
* **Rationale:** Provides high confidence that the system works cohesively. Tests behavior closer to real-world usage. Less brittle to internal refactoring compared to heavily mocked unit tests. Directly validates the *Modularity* and *Interface* design.
* **Implementation:**
    * **Go:** Utilize `net/http/httptest` for in-process HTTP handler testing. Invoke exported functions/methods of packages directly to test their integration. For tests requiring external dependencies like databases, prefer using real instances managed via Docker containers (e.g., using `testcontainers-go`) over extensive mocking where feasible.
    * **TypeScript:** Use libraries like `supertest` for testing HTTP endpoints against running application instances (or in-process equivalents). Test service methods directly, providing mock implementations *only* for external dependencies injected via DI. Consider test containers for managing real database instances during tests.

## 5. Mocking Policy: Use Sparingly, At Boundaries Only (Crucial)

Our stance on mocking is conservative and critical for maintaining effective tests and good design.

* **Minimize Mocking:** Actively strive to design code and tests that require minimal mocking. Test complexity often reflects code complexity.
* **Mock Only True External System Boundaries:** Mocking is permissible *only* for interfaces/abstractions that represent systems or concerns genuinely *external* to the service/application being tested, and which are impractical or undesirable to use directly in automated tests. These typically include:
    * Network I/O (Third-party APIs, other distinct microservices)
    * Databases / External Data Stores (when not using test containers/in-memory fakes)
    * Filesystem Operations
    * System Clock (use injectable clock abstractions)
    * External Message Brokers / Caches
* **Abstract External Dependencies First:** Ensure external dependencies are *always* accessed through interfaces or abstractions defined *within* your own codebase (following the Ports & Adapters / Dependency Inversion principle). Tests should mock *these local abstractions*, not concrete external library clients directly.
* **NO Mocking Internal Collaborators:** **It is an anti-pattern to mock classes, structs, functions, or interfaces that are defined and owned *within* the same application/service solely for the purpose of isolating another internal component.** Feeling the need to do this indicates a design flaw (likely high coupling, poor separation of concerns, or violation of dependency inversion). **The correct action is to refactor the code under test to improve its design and testability.**

**Rationale:** This strict policy ensures tests verify realistic interactions, remain robust against internal refactoring, provide genuine confidence, and act as accurate indicators of design health. Over-mocking hides design problems and leads to tests that verify the mocks, not the actual integrated behavior.

**Implementation:**
* **Go:** Define `interface{}` types for external dependencies in your core logic. Use standard mocking libraries (`gomock`, `testify/mock`) or simple hand-rolled fakes to implement these interfaces in your tests.
* **TypeScript:** Define `interface` or `abstract class` contracts for external dependencies. Use the mocking features of your test framework (e.g., Jest's `jest.fn()`, `jest.spyOn()`, `jest.mock()`) or libraries like Sinon.JS to mock these abstractions, typically provided via Dependency Injection.

## 6. Desired Test Characteristics: The FIRST Properties

We aim for tests that embody the FIRST principles, making our test suite trustworthy and effective:

* **Fast:** Tests must run quickly to provide rapid feedback during development and in CI. Slow tests reduce productivity and are run less frequently.
* **Independent / Isolated:** Each test must be runnable independently of others, in any order. Tests should set up their own preconditions and clean up afterward, not relying on shared mutable state or the side effects of other tests.
* **Repeatable / Reliable:** Tests must consistently produce the same pass/fail result each time they are run in the same environment. Eliminate sources of non-determinism (uncontrolled concurrency, reliance on real time/dates, random data without seeding). Flaky tests undermine confidence in the entire suite.
* **Self-Validating:** Tests must explicitly assert their expected outcomes and clearly report pass or fail without requiring manual inspection of output logs.
* **Timely / Thorough:** Tests should ideally be written alongside or slightly before the production code (TDD). They need to provide *thorough* coverage of the intended functionality, including happy paths, error conditions, edge cases, and boundary values relevant to the component's responsibility.

## 7. Test Data Management: Realistic and Maintainable

Effective management of test data is crucial for readable and robust tests.

* **Clarity & Intent:** Test data setup should clearly reveal the specific scenario being tested. Use descriptive variable names instead of "magic" values. Make the relationship between inputs and expected outputs obvious.
* **Realism:** Use test data that reasonably approximates real-world data characteristics, especially for integration tests, to uncover issues that might not appear with overly simplistic data.
* **Maintainability:** Avoid duplicating complex object creation logic in multiple tests. Employ patterns like Test Data Builders, Object Mothers, Factories, or simple helper functions to create test fixtures consistently and reduce boilerplate.
* **Isolation:** Ensure data used or created by one test does not persist and interfere with subsequent tests. Clean up database records, reset state, etc., between test executions (test framework hooks or helper functions are useful here).

---

# Documentation Approach

This section outlines our philosophy and practices for project documentation. Our goal is effective communication and knowledge sharing—whether with team members, future contributors, or our future selves—achieved with minimal friction and maximum clarity. We prioritize documentation methods that are closely tied to the code and reflect the rationale behind our decisions, aligning with the Core Principles of *Explicit is Better than Implicit* and *Document Decisions, Not Mechanics*.

## 1. Prioritize Self-Documenting Code

**Approach:** The codebase itself is the primary and most accurate source of documentation regarding *how* the system works. We achieve this through:
* **Clear Naming:** Adhering strictly to meaningful naming conventions (see `CODING_STANDARDS.md`).
* **Strong Typing:** Leveraging static types (TypeScript, Go types) to define data structures and contracts explicitly.
* **Logical Structure:** Organizing code into small, focused modules/packages with clear responsibilities (see `ARCHITECTURE_GUIDELINES.md`).
* **Readability:** Following consistent formatting and linting rules, and writing straightforward logic.
* **Well-Written Tests:** Tests often serve as executable examples of how components are intended to be used (see `TESTING_STRATEGY.md`).

**Rationale:** Code is the ultimate source of truth. Relying heavily on external documentation for low-level mechanics creates a significant synchronization burden and inevitably leads to outdated information. Well-factored, clearly written code minimizes the need for supplementary explanation of *what* it does.

**Implementation:** Before writing extensive comments or external documents explaining code mechanics, always ask: "Can I refactor the code itself to make its purpose and operation clearer?"

## 2. README.md: The Essential Entry Point

**Approach:** Every project, service, or significant library *must* have a `README.md` file at its root directory. This file is the front door, providing essential context and practical instructions for anyone encountering the project. It must be kept concise and up-to-date.

**Standard Structure:**
* **Project Title:** Clear and prominent.
* **Brief Description:** Concisely explain the project's purpose and what problem it solves (1-3 sentences).
* **Status:** (Optional but recommended) Badges for build status, test coverage, latest version, etc.
* **Getting Started / Setup:**
    * Minimum prerequisites (e.g., Go 1.x, Node.js vX.Y, Docker).
    * Step-by-step instructions for cloning, installing dependencies (`go mod download`, `npm install`), and any necessary environment setup (e.g., required environment variables, `.env` file setup).
    * Instructions for building the project (`go build`, `npm run build`).
* **Running Tests:** Clear command(s) to execute the full automated test suite (`go test ./...`, `npm test`).
* **Usage / Running the Application:** How to run the primary application or execute key functions (e.g., `go run ./cmd/server/`, `npm start`, example CLI usage with flags). Include pointers to key configurations or examples if relevant.
* **Key Scripts / Commands:** Reference common `Makefile` targets or `package.json` scripts for linting, formatting, etc.
* **Architecture Overview (Optional):** A very brief description or link to key architectural documents (like ADRs or diagrams) if helpful for orientation.
* **How to Contribute:** (Especially for team projects) Link to contribution guidelines, code of conduct, and the expected Pull Request process.
* **License:** Specify the project's software license.

**Rationale:** A well-structured README significantly lowers the barrier to entry, enabling others (and future you) to quickly understand, set up, run, test, and contribute to the project.

## 3. Code Comments: Explaining Intent and Context

**Approach:** Adhere strictly to the commenting philosophy outlined in `CODING_STANDARDS.md`: comments explain the *why*, not the *what* or the *how*. Use comments to:
* Clarify the *intent* behind non-obvious code sections.
* Explain the *rationale* for specific design choices, especially when trade-offs were involved.
* Provide necessary *context* that isn't apparent from the code itself (e.g., links to specific requirements, bug reports, or external specifications).
* Document unavoidable workarounds or known limitations.

**Rationale:** Good code explains itself mechanically. Good comments provide valuable insight into the reasoning and context, aiding future understanding and maintenance. Redundant or outdated comments create noise and mislead readers.

**Implementation:**
* Avoid comments that merely paraphrase the code line-by-line.
* If code requires extensive comments to explain its mechanics, it's a strong signal that it should be refactored for clarity.
* Use standard language documentation formats (`//` Go docs, `/** */` TSDoc) for public APIs to integrate with documentation generation tools.
* **Delete commented-out code.** Use version control history instead.

## 4. API Documentation: Defining Contracts and Usage

**Approach:** Public APIs—whether internal APIs between modules/packages or external APIs exposed by services—must be clearly documented to define their contracts and guide usage. Leverage automated tooling derived from code where possible.

* **Internal Module/Package APIs:**
    * The primary documentation is the code itself: clear type definitions (Go `struct`/`interface{}`, TypeScript `interface`/`type`) and function/method signatures.
    * Supplement with doc comments (Go docs, TSDoc) on all exported identifiers, explaining purpose, parameters, return values, error conditions, panics (Go), or thrown exceptions (TS).
* **External Service APIs:**
    * **REST APIs:** Maintain an accurate and up-to-date **OpenAPI (Swagger) specification**. This serves as the definitive contract and can drive documentation generation, client/server code generation, and conformance testing. Store the spec file (e.g., `openapi.yaml`) in the repository, often in `/docs/api` or a similar location.
    * **gRPC APIs:** The **`.proto` files** are the definitive contract. Use comments within the `.proto` files to clearly document services, RPC methods, messages, and fields.

**Rationale:** Clear API contracts are essential for reliable integration. Automating documentation generation from code or specifications (like OpenAPI, Protobuf) reduces manual effort and minimizes the risk of documentation drift. Supports *Explicit is Better than Implicit*.

**Implementation:**
* **Go:** Write comprehensive `godoc` comments. Use tools to serve or generate HTML documentation.
* **TypeScript:** Write comprehensive TSDoc comments. Use tools like TypeDoc to generate HTML documentation.
* Ensure OpenAPI/Protobuf definitions are versioned alongside the code they describe.

## 5. Design Decision Documentation: Capturing Rationale

**Approach:** It's useful to document significant design decisions, particularly those that affect structure, cross-cutting concerns, dependencies, interfaces, or major technology choices. These documents help capture the *context*, the *decision*, and its *consequences*, preserving rationale over time.

**Format & Storage:**
* Use simple Markdown files stored in a relevant documentation directory within the repository.
* Focus on capturing just the essential information needed to understand the decision.

**Key Sections to Consider:**
* **Title:** Short, descriptive summary of the decision.
* **Context:** What problem or situation prompted this decision?
* **Decision:** Clearly state the decision that was made.
* **Consequences:** What are the results of this decision, including any trade-offs?

**Rationale:** Documenting design decisions provides context about *why* the system evolved the way it did. This historical context can be helpful for understanding constraints and making informed future decisions. Implements *Document Decisions, Not Mechanics*.

## 6. Diagrams: Visualizing Structure and Complex Flows

**Approach:** Use diagrams judiciously when a visual representation significantly clarifies high-level architecture, component interactions, complex workflows, state machines, or data models. Prioritize diagrams that are easy to create, update, and version alongside the code.

**Tools & Storage:**
* **Preferred:** Text-based diagramming tools embeddable in Markdown (e.g., **MermaidJS**, PlantUML) as they are easily versioned and diffed.
* **Acceptable:** Simple vector drawing tools (e.g., **Excalidraw**, diagrams.net/draw.io) where the source file (e.g., `.excalidraw`, `.drawio.svg`) can be committed to the repository. Avoid opaque binary formats if possible.
* Store diagram source files and/or exported images (e.g., SVG, PNG) in a dedicated `/docs/diagrams/` directory.
* Whiteboard photos are useful for brainstorming but should be converted to a more durable format if they represent stable architectural concepts.

**Rationale:** Diagrams can quickly convey relationships and structures that are difficult to describe solely with text. Keeping them simple and using maintainable formats prevents them from becoming outdated burdens.

**Implementation:**
* Keep diagrams focused on a specific aspect or level of abstraction. Avoid overly cluttered "grand unified" diagrams.
* Ensure diagrams have clear titles and legends.
* Reference relevant diagrams from READMEs or ADRs where appropriate.
* Periodically review diagrams for accuracy during refactoring or feature development.