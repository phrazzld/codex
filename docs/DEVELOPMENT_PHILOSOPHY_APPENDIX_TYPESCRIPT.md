# Development Philosophy - Appendix: TypeScript (APPENDIX-TYPESCRIPT.md)

## Introduction

This document specifies the TypeScript language-specific standards, tooling requirements, and idiomatic practices required for our projects. It serves as a mandatory extension to the main **Development Philosophy (v3)** document. All TypeScript code written for our projects **MUST** adhere to the guidelines herein, in addition to the core philosophy.

**Reference:** Always refer back to the main [Development Philosophy](DEVELOPMENT_PHILOSOPHY.md) for overarching principles.

## Table of Contents

- [1. Tooling and Environment](#1-tooling-and-environment)
- [2. Formatting (Prettier)](#2-formatting-prettier)
- [3. Linting (ESLint + TypeScript ESLint)](#3-linting-eslint--typescript-eslint)
- [4. TypeScript Configuration (`tsconfig.json`)](#4-typescript-configuration-tsconfigjson)
- [5. Types and Interfaces (Best Practices, No `any`)](#5-types-and-interfaces-best-practices-no-any)
- [6. Modules and Structure (ES Modules, Feature Folders)](#6-modules-and-structure-es-modules-feature-folders)
- [7. Immutability (`readonly`, Patterns)](#7-immutability-readonly-patterns)
- [8. Functions and Classes (Purity, Async/Await)](#8-functions-and-classes-purity-asyncawait)
- [9. Error Handling (Errors, Promises, Middleware)](#9-error-handling-errors-promises-middleware)
- [10. Testing](#10-testing)
- [11. Logging (Standard Library, JSON, Context)](#11-logging-standard-library-json-context)
- [12. Dependency Management (npm/yarn/pnpm, Auditing)](#12-dependency-management-npmyarnpnpm-auditing)
- [13. Builds and Compilation (`tsc`, Transpilers)](#13-builds-and-compilation-tsc-transpilers)

---

## 1. Tooling and Environment

* **Node.js Version:** Projects **MUST** use a specified LTS (Long-Term Support) version of Node.js, defined in project documentation or `.nvmrc`/`package.json#engines`.
* **Package Manager:** Specify the standard package manager for the project (**npm**, **yarn**, or **pnpm**). Consistency is key.
* **Mandatory Tools:**
    * Node.js & Selected Package Manager
    * TypeScript (`typescript` package)
    * Prettier (`prettier` package) - For code formatting (see Section 2).
    * ESLint (`eslint`, `@typescript-eslint/parser`, `@typescript-eslint/eslint-plugin`) - For static analysis and linting (see Section 3).
* **Environment:** Developers should configure their editors/IDEs for seamless integration with TypeScript and the associated tooling, including format-on-save (Prettier), real-time linting and type-checking feedback (ESLint, `tsc`), and debugging support.

---

## 2. Formatting (Prettier)

* **Standard:** Code formatting using Prettier is **ABSOLUTELY NON-NEGOTIABLE**.
* **Shared Configuration:** A Prettier configuration file (`.prettierrc.js`, `.prettierrc.json`, `.prettierrc.yaml`, or `prettier` key in `package.json`) **MUST** exist in the project root, be version-controlled, and define the project's formatting rules.
* **Enforcement:** Formatting **MUST** be automatically checked and enforced by pre-commit hooks and verified in the CI pipeline. There will be no discussion or deviation regarding code style; Prettier is the standard.

---

## 3. Linting (ESLint + TypeScript ESLint)

* **Mandatory Use:** Static analysis using ESLint, configured with TypeScript support (`@typescript-eslint/parser` and `@typescript-eslint/eslint-plugin`), **MUST** be performed on all TypeScript code.
* **Shared Configuration:** An ESLint configuration file (`.eslintrc.js`, `.eslintrc.json`, etc.) **MUST** exist in the project root, be version-controlled, and define a strict set of enabled rules and parser options. It should extend recommended configurations:
    * `eslint:recommended`
    * `plugin:@typescript-eslint/recommended`
    * `plugin:@typescript-eslint/recommended-requiring-type-checking` (Requires `tsconfig.json` parserOptions)
    * Consider Prettier integration plugins (`eslint-config-prettier`) to disable ESLint rules that conflict with Prettier.
* **No Suppressions:** As stated in the core philosophy, directives like `// eslint-disable-line`, `// eslint-disable-next-line`, `@ts-ignore`, `@ts-expect-error` are **STRICTLY FORBIDDEN** except in extremely rare cases. Any such exception requires a detailed comment explaining the justification and explicit approval during code review.

---

## 4. TypeScript Configuration (`tsconfig.json`)

* **Mandatory File:** A `tsconfig.json` file **MUST** exist in the project root (or relevant sub-package roots in monorepos).
* **Strictness is Required:** The configuration **MUST** enable strict type-checking options:
    * `"strict": true` (This implicitly enables the following and more)
        * `"noImplicitAny": true`
        * `"strictNullChecks": true`
        * `"strictFunctionTypes": true`
        * `"strictBindCallApply": true`
        * `"strictPropertyInitialization": true`
        * `"noImplicitThis": true`
        * `"useUnknownInCatchVariables": true` (TS 4.4+)
        * `"alwaysStrict": true`
* **Other Essential Options (Example Baseline):**
    * `"target": "ES2020"` (or later, depending on Node.js version support)
    * `"module": "NodeNext"` (Recommended for modern Node.js) or `"ESNext"`
    * `"moduleResolution": "NodeNext"` (Recommended for modern Node.js) or `"Bundler"`
    * `"esModuleInterop": true` (For better compatibility with CommonJS modules)
    * `"forceConsistentCasingInFileNames": true`
    * `"skipLibCheck": true` (Usually speeds up compilation)
    * `"isolatedModules": true` (Ensures files can be transpiled independently)
    * `"noUnusedLocals": true`
    * `"noUnusedParameters": true`
    * `"noImplicitReturns": true`
    * `"noFallthroughCasesInSwitch": true`
    * `"resolveJsonModule": true` (If importing JSON files)
    * *(Compiler output options like `outDir`, `rootDir`, `declaration`, `sourceMap` as needed)*
* **Path Aliases:** If using path aliases (e.g., `@/*`), configure `"baseUrl"` and `"paths"`.

---

## 5. Types and Interfaces (Best Practices, No `any`)

* **`any` is FORBIDDEN:** Code **MUST NOT** use `any`. Use specific types, union types (`|`), intersection types (`&`), generics (`<T>`), or `unknown` (followed by type checking/assertion) instead.
* **`interface` vs `type`:**
    * Use `interface` primarily for defining the shape of objects or contracts for classes. Interfaces can be merged via declaration merging and implemented/extended by classes.
    * Use `type` primarily for defining aliases for union types, intersection types, primitive types, tuples, mapped types, conditional types, or complex object shapes not intended for implementation by classes.
* **Utility Types:** Leverage built-in utility types effectively (e.g., `Partial<T>`, `Readonly<T>`, `Required<T>`, `Pick<T, K>`, `Omit<T, K>`, `Record<K, T>`, `ReturnType<F>`, `Parameters<F>`) to create new types based on existing ones without redundancy.
* **Immutability:** Use the `readonly` modifier for properties in interfaces/types and classes to enforce immutability at compile time (see Section 7).
* **Discriminated Unions:** Use discriminated unions (tagged unions) with a common literal type property to model states, events, or variants in a type-safe way.
* **Specificity:** Be as specific as possible with types. Use literal types (`'success' | 'error'`) over `string` where applicable.

---

## 6. Modules and Structure (ES Modules, Feature Folders)

* **ES Modules:** **MUST** use standard ES Module syntax (`import` / `export`). Avoid `require()` unless interacting with legacy CommonJS APIs where necessary.
* **Package by Feature:** Reinforce this principle. Organize code into directories based on business features or domains (e.g., `src/user/`, `src/order/`, `src/common/`).
* **Module Boundaries:** Define clear boundaries between modules. Use `export` to expose only the intended public API of a module.
* **Barrel Files (`index.ts`):** Use `index.ts` files judiciously to re-export the public API of a feature module. Avoid overly deep nesting or complex re-export chains that can obscure dependencies, hinder tree-shaking, or create import cycles.
* **No Circular Dependencies:** Circular module dependencies are **FORBIDDEN**. Structure code to avoid them. Tools like `eslint-plugin-import` or `madge` can help detect cycles.

---

## 7. Immutability (`readonly`, Patterns)

* **Default to Immutability:** Data structures should be treated as immutable by default, aligning with the core philosophy.
* **`readonly` Modifier:** Use `readonly` extensively for properties in `interface`, `type`, and `class` definitions to prevent accidental mutation. Use `Readonly<T>` and `ReadonlyArray<T>` utility types for collections.
* **Immutable Updates:** **MUST** use immutable update patterns:
    * Objects: Use spread syntax (`{ ...obj, property: newValue }`).
    * Arrays: Use spread syntax (`[...arr, newItem]`) or non-mutating array methods (`map`, `filter`, `reduce`, `slice`, `concat`). **Avoid** mutating methods like `push`, `pop`, `splice`, `sort` directly on shared state.
* **Libraries (Optional):** Consider libraries like `immer` for simplifying complex nested immutable state updates, but only if native patterns become overly verbose or error-prone.

---

## 8. Functions and Classes (Purity, Async/Await)

* **Pure Functions:** Prioritize pure functions for logic and transformations, as per the core philosophy.
* **`class` Usage:** Use `class` for object-oriented modeling, especially when dealing with instances that have internal state and methods operating on that state, or when implementing specific patterns (e.g., Repositories, Services with dependency injection). Prefer composition over deep inheritance hierarchies.
* **`async`/`await`:** **MUST** use `async`/`await` syntax for handling asynchronous operations (Promises). Avoid raw `.then()`/`.catch()` chains where `async/await` provides better readability, except in specific cases where Promise combinators (`Promise.all`, `Promise.race`, etc.) are used directly.
* **Typing:** All function parameters and return values **MUST** be explicitly typed. Use `void` for functions that do not return a value. Use `Promise<T>` for async functions returning type `T`.

---

## 9. Error Handling (Errors, Promises, Middleware)

* **Error Objects:** Use the standard `Error` object or create custom error classes extending `Error` for specific error types that require distinct handling or additional properties.
    ```typescript
    class NetworkError extends Error {
      constructor(message: string, public statusCode?: number) {
        super(message);
        this.name = 'NetworkError';
      }
    }
    ```
* **Promise Rejections:** Handle Promise rejections consistently using `try...catch` blocks within `async` functions. Unhandled promise rejections are **FORBIDDEN**.
    ```typescript
    async function fetchData(url: string): Promise<Data> {
      try {
        const response = await fetch(url);
        if (!response.ok) {
          throw new NetworkError(`HTTP error! status: ${response.status}`, response.status);
        }
        return await response.json() as Data;
      } catch (error) {
        // Log the error appropriately
        console.error("Failed to fetch data:", error);
        // Re-throw or handle as needed
        throw error;
      }
    }
    ```
* **TSDoc `@throws`:** Document potential errors thrown by functions using the `@throws` tag in TSDoc comments.
* **Centralized Handling:** In applications (e.g., web servers), implement centralized error handling middleware (e.g., Express error middleware) to catch errors, log them consistently, and return standardized error responses to clients.

---

## 10. Testing

* **Framework:** Specify the standard testing framework (e.g., **Jest**, **Vitest**) for the project.
* **Test Files:** Use standard naming conventions (`*.test.ts`, `*.spec.ts`). Co-locate test files with source code or place them in a dedicated `__tests__` directory adjacent to the source.
* **TypeScript Tests:** Tests **MUST** be written in TypeScript to benefit from type safety during testing.
* **Coverage:** Test coverage **MUST** meet the thresholds defined in the core philosophy, enforced by CI using the tooling provided by the chosen test framework (e.g., `jest --coverage`).
* **Mocking Policy:**
    * Reiterate: **NO MOCKING INTERNAL COLLABORATORS/MODULES.** Refactor code for testability instead (DI, interfaces).
    * Use the test framework's mocking capabilities (e.g., `jest.mock`, `vi.mock`) **ONLY** for mocking true external dependencies (APIs, DBs accessed via abstractions) or environment-specific modules (e.g., `fs`).
    * Leverage Dependency Injection heavily. Define interfaces for dependencies and provide test doubles (fakes, stubs, mocks) in tests.
* **Assertions:** Use the assertion library provided by the framework (e.g., Jest's `expect`) or an approved external library (`chai` etc.).

---

## 11. Logging (Standard Library, JSON, Context)

* **Standard Library:** Specify the standard structured logging library for the project (e.g., **pino**, **winston**). Avoid `console.log` for operational logging.
* **JSON Output:** The chosen logging library **MUST** be configured to output logs in **JSON format** in production and CI environments.
* **Configuration:** Configure the minimum log level via environment variables. Default to `INFO` in production.
* **Contextual Logging:**
    * Inject logger instances (potentially with pre-set context like `service_name`) via dependency injection frameworks or manually.
    * Use context propagation mechanisms (e.g., `AsyncLocalStorage` in Node.js) where feasible to automatically include request-scoped context like `correlation_id` in all logs for a given request/transaction. Ensure mandatory context fields from the core philosophy are present.

---

## 12. Dependency Management (npm/yarn/pnpm, Auditing)

* **Package Manager & Lock Files:** Use the specified package manager (`npm`/`yarn`/`pnpm`) consistently. The corresponding lock file (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`) **MUST** be committed to version control.
* **`package.json`:** Maintain a clean `package.json`. Define `engines` for Node.js/package manager versions. Use scripts for common tasks (lint, test, build).
* **Updates:** Keep dependencies reasonably updated using tools like `npm update`, `yarn upgrade-interactive`, or `pnpm update`. Leverage automated tools like Dependabot/Renovate Bot.
* **`@types` Dependencies:** Explicitly manage `@types/*` dependencies for libraries that don't bundle their own types. Keep them aligned with the library versions.
* **Vulnerability Scanning:** Integrate dependency auditing (`npm audit --audit-level=high`, `yarn audit --level high`) into the CI pipeline. Builds **MUST** fail on new critical/high severity vulnerabilities.

---

## 13. Builds and Compilation (`tsc`, Transpilers)

* **Type Checking:** The TypeScript Compiler (`tsc`) **MUST** be used for comprehensive type checking, typically via `tsc --noEmit`, enforced in CI.
* **Compilation/Transpilation:**
    * `tsc` can be used for compiling TypeScript to JavaScript.
    * Faster transpilers (e.g., **SWC**, **esbuild**, **Babel** with `@babel/preset-typescript`) may be used for development speed or build pipelines, BUT `tsc --noEmit` must still pass in CI.
* **Configuration:** Configure build outputs (`outDir`, `rootDir`) and options (`declaration`, `sourceMap`) in `tsconfig.json` as needed for the project type (application vs. library).
* **Declaration Files:** Libraries intended for consumption by other TypeScript projects **MUST** generate declaration files (`declaration: true`, `declarationMap: true`).

