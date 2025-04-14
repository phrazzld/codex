# Coding Standards

This document defines the concrete rules, conventions, and best practices for writing code day-to-day in our projects. Adherence to these standards is essential for creating code that is readable, consistent, predictable, maintainable, and less prone to defects. These standards directly support our Core Principles, particularly aiming for Simplicity, Maintainability, and Explicit code.

---

## 1. Maximize Language Strictness: Catch Errors Early

**Standard:** Configure language compilers, interpreters, and static analysis tools to their strictest practical settings to leverage the full power of static analysis and type checking.

**Rationale:** This allows us to catch potential errors, inconsistencies, and questionable patterns at compile-time or lint-time, long before they manifest as runtime bugs. It supports the *Explicit is Better than Implicit* principle by making assumptions visible and verifiable.

**Implementation:**
* **TypeScript:** Set `strict: true` in `tsconfig.json`. This enables a suite of essential checks (`noImplicitAny`, `strictNullChecks`, etc.). Consider enabling further strictness flags like `noUnusedLocals`, `noUnusedParameters`, `noImplicitReturns` based on project needs.
* **Go:** Rely on the standard Go compiler checks (`go build`), `go vet` for identifying suspicious constructs, and a comprehensive suite of linters configured via `golangci-lint`.
* Standardize these configurations (`tsconfig.json`, `.golangci.yml`) across projects and include them in version control.

---

## 2. Leverage Types Diligently: Express Intent Clearly

**Standard:** Utilize the static type system fully and precisely to model data structures, define function signatures, and establish clear contracts between different parts of the code.

**Rationale:** Types serve as invaluable, machine-checked documentation. They improve code clarity, significantly reduce entire classes of runtime errors (e.g., type mismatches, null pointer exceptions), and enable powerful tooling like autocompletion and safe refactoring. This directly supports *Explicit is Better than Implicit*.

**Implementation:**
* **TypeScript:** **Strictly forbid the use of `any`**. Employ specific built-in types, custom `interface` definitions, `type` aliases, discriminated unions, utility types (`Partial`, `Readonly`, etc.), and `unknown` where type information is genuinely absent initially. Type all function parameters, return values, and variable declarations.
* **Go:** Use appropriate built-in types. Define clear `struct` types for data aggregation. Use `interface{}` types judiciously to define behavior contracts, adhering to the Interface Segregation Principle (preferring smaller, focused interfaces).

---

## 3. Prefer Immutability: Simplify State Management

**Standard:** Whenever practical, treat data structures and objects as immutable. Instead of modifying existing data in place, create and return new instances with the updated state.

**Rationale:** Immutability significantly simplifies reasoning about program state, as data doesn't change unexpectedly out from underfoot. It eliminates a large category of bugs related to shared mutable state, especially in concurrent or asynchronous scenarios, and makes state changes predictable. Supports *Simplicity*.

**Implementation:**
* **TypeScript:** Use the `readonly` modifier for properties and `ReadonlyArray<T>` for arrays. Employ immutable update patterns (e.g., object spread `{...obj, prop: newValue}`, array methods like `map`, `filter`, `reduce` which return new arrays). Consider libraries like Immer for managing complex immutable state updates ergonomically.
* **Go:** Be conscious that slices and maps are reference types. When passing them to functions, understand that modifications within the function will affect the original data; copy them explicitly if the caller requires the original to remain unchanged. Favor value types or return new struct instances instead of modifying receiver pointers when the type's semantics allow for immutability.

---

## 4. Favor Pure Functions: Isolate Side Effects

**Standard:** Strive to implement core logic, data transformations, and calculations as pure functions whenever feasible. A pure function's output depends *only* on its input arguments, and it produces *no* observable side effects (no I/O, no mutation of external state). Concentrate necessary side effects at the edges of the system (e.g., in infrastructure adapters, command handlers).

**Rationale:** Pure functions are the simplest building blocks. They are inherently predictable, deterministic, easy to test in isolation (no setup or mocking required), highly reusable, and make code much easier to reason about. Supports *Simplicity*, *Modularity*, and *Testability*.

**Implementation:** Actively identify opportunities to extract pure computational logic from functions that currently mix calculations with side effects. Pass dependencies explicitly rather than relying on global state.

---

## 5. Meaningful Naming: Communicate Purpose

**Standard:** Choose clear, descriptive, and unambiguous names for all identifiers (variables, constants, functions, methods, classes, interfaces, types, modules, packages, files). Names should effectively communicate the entity's purpose and usage within its context. Adhere strictly to the established naming conventions of the language.

**Rationale:** Code is read far more often than it's written. Meaningful names are arguably the most crucial factor in code *Maintainability* and readability, reducing the need for explanatory comments and lowering cognitive load. Supports *Self-Documenting Code*.

**Implementation:**
* **TypeScript:** `camelCase` for variables, parameters, functions. `PascalCase` for classes, interfaces, type aliases, enums.
* **Go:** `camelCase` for unexported identifiers (internal to package). `PascalCase` for exported identifiers (visible outside package). Package names should be short, lowercase, and meaningful, avoiding underscores or camelCase. Avoid stutter (e.g., prefer `package user; type Profile struct{}` over `package user; type UserProfile struct{}`).
* Avoid vague terms like `data`, `info`, `temp`, `handle`, `process` unless the scope is extremely limited and context makes the meaning obvious. Use domain-specific terminology where appropriate.

---

## 6. Mandatory Code Formatting: Ensure Consistency

**Standard:** All code committed to the repository *must* be automatically formatted using the designated standard tool for the language. Formatting style is not subject to individual preference or debate.

**Rationale:** Enforces a consistent visual style across the entire codebase, drastically improving readability and reducing cognitive friction when switching between files or authors. Eliminates time wasted on style debates in code reviews. Ensures code diffs only show substantive logical changes. Supports *Maintainability* and *Automation*.

**Implementation:**
* **TypeScript:** **Prettier** is mandatory. Configure it via a `.prettierrc.js` (or similar) file checked into the repository.
* **Go:** **`gofmt`** or **`goimports`** (preferred, as it includes `gofmt` and manages imports) is mandatory and non-negotiable.
* Integrate formatters into pre-commit hooks and CI pipeline checks to enforce compliance automatically.

---

## 7. Mandatory Linting: Catch Problems Proactively

**Standard:** All code committed to the repository *must* pass analysis by the designated standard linter(s) using a strict, shared configuration. Pre-commit hooks must **never** be bypassed with `--no-verify`.

**Rationale:** Linters act as automated code reviewers, identifying potential bugs, anti-patterns, stylistic inconsistencies, performance issues, and deviations from best practices *before* they are manually reviewed or merged. This improves overall code quality, consistency, and *Maintainability*. Supports *Automation*.

**Implementation:**
* **TypeScript:** **ESLint** is mandatory, configured with relevant plugins (e.g., `@typescript-eslint/eslint-plugin`, framework-specific plugins, accessibility plugins). A shared `.eslintrc.js` (or similar) configuration file must be checked into the repository.
* **Go:** **`golangci-lint`** is mandatory. A shared `.golangci.yml` configuration file specifying the enabled linters and their settings must be checked into the repository. Aim for a comprehensive and strict set of enabled linters.
* Integrate linting into pre-commit hooks and CI pipeline checks, treating violations as build failures.
* **IMPORTANT:** It is *strictly forbidden* to bypass pre-commit hooks with `git commit --no-verify`. Address issues properly rather than circumventing checks.

---

## 8. Address Violations, Don't Suppress: Fix the Root Cause

**Standard:** Directives to suppress linter warnings or type checker errors (e.g., `// eslint-disable-line`, `@ts-ignore`, `// nolint:`, type assertions like `as any` or unsafe conversions) should be avoided at all costs. Investigate the underlying issue and refactor the code to satisfy the check correctly.

**Rationale:** Suppression mechanisms often hide genuine bugs, technical debt, or poor design choices. Bypassing these checks defeats their purpose and degrades code quality and safety over time. Fixing the root cause leads to more robust, maintainable, and understandable code. Supports *Maintainability* and *Explicit is Better than Implicit*.

**Implementation:** Legitimate exceptions are extremely rare and require explicit justification via a code comment explaining *why* the suppression is necessary and safe. Significant or recurring patterns requiring suppression should be discussed and documented where appropriate. Treat suppressions as code smells requiring scrutiny.

---

## 9. Purposeful Comments: Explain the *Why*

**Standard:** Write comments primarily to explain the *intent*, *rationale*, or *context* behind code that might otherwise be non-obvious. Focus on the "why," not the "what" or "how"—the code itself should clearly express the mechanics. Avoid comments that simply paraphrase the code. Use standard documentation comment formats for public APIs.

**Rationale:** Well-written code minimizes the need for comments. Valuable comments provide context that cannot be directly inferred from the code, such as reasoning behind specific design choices, trade-offs made, or links to external requirements or issues. Supports *Self-Documenting Code* and *Maintainability*.

**Implementation:**
* Before writing a comment to explain *how* code works, try to refactor the code to make its mechanics clearer.
* Delete commented-out code; rely on version control history instead.
* **TypeScript:** Use TSDoc (`/** ... */`) for exported functions, classes, types, etc., to enable documentation generation and editor tooling.
* **Go:** Use standard Go doc comments (`// ...`) preceding exported identifiers for discoverability via `godoc`.

---

## 10. Disciplined Dependency Management: Keep It Lean and Updated

**Standard:** Minimize the number of third-party dependencies introduced into a project. Each external dependency represents a trade-off, adding potential complexity, security risks, maintenance overhead, and licensing considerations. Keep essential dependencies reasonably up-to-date.

**Rationale:** Fewer dependencies result in a smaller attack surface, faster build times, less potential for version conflicts or "dependency hell," and generally easier long-term maintenance and upgrades. Supports *Simplicity* and *Maintainability*.

**Implementation:**
* Thoroughly evaluate the necessity and value proposition before adding any new dependency. Can the functionality be achieved reasonably with the standard library or existing dependencies?
* Prefer dependencies that are well-maintained, widely used, have compatible licenses, and minimal transitive dependencies.
* Regularly review and audit dependencies (`npm audit`, `yarn audit`, `go list -m all`, checking for vulnerabilities).
* Keep `package.json` / `go.mod` files tidy and remove unused dependencies (`npm prune`, `go mod tidy`).
* Utilize tools like Dependabot or Renovate Bot to help manage dependency updates systematically.
