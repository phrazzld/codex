# DEVELOPMENT PHILOSOPHY - APPENDIX RUST

## Introduction

This document specifies the Rust language-specific standards, tooling requirements, and idiomatic practices required for our projects. It serves as a mandatory extension to the main **Development Philosophy (v3)** document. All Rust code written for our projects **MUST** adhere to the guidelines herein, in addition to the core philosophy.

**Reference:** Always refer back to the main [Development Philosophy](DEVELOPMENT_PHILOSOPHY.md) for overarching principles.

## Table of Contents

- [1. Tooling and Environment](#1-tooling-and-environment)
- [2. Formatting (`rustfmt`)](#2-formatting-rustfmt)
- [3. Linting (`clippy`)](#3-linting-clippy)
- [4. Crates, Modules, and Project Structure](#4-crates-modules-and-project-structure)
- [5. Naming Conventions](#5-naming-conventions)
- [6. Types, Structs, Enums, and Traits](#6-types-structs-enums-and-traits)
- [7. Ownership, Borrowing, and Lifetimes](#7-ownership-borrowing-and-lifetimes)
- [8. Error Handling (`Result`, `panic!`, `?`)](#8-error-handling-result-panic-)
- [9. Concurrency (Fearless Concurrency)](#9-concurrency-fearless-concurrency)
- [10. Unsafe Code (`unsafe`)](#10-unsafe-code-unsafe)
- [11. Testing (`#[test]`, Integration, Doc Tests)](#11-testing-test-integration-doc-tests)
- [12. Logging (`log`, `tracing`)](#12-logging-log-tracing)
- [13. Dependency Management (Cargo)](#13-dependency-management-cargo)
- [14. Builds and Deployment Artifacts](#14-builds-and-deployment-artifacts)
- [15. Macros (`macro_rules!`, Procedural)](#15-macros-macro_rules-procedural)
- [16. Foreign Function Interface (FFI)](#16-foreign-function-interface-ffi)

---

## 1. Tooling and Environment

* **Rust Version:** Projects **MUST** specify the Rust edition and Minimum Supported Rust Version (MSRV) in `Cargo.toml`. Use the latest stable Rust release where feasible. Updates should be managed proactively. Consider using Rust toolchains (e.g., `rustup override set stable`).
* **Mandatory Tools:**
    * `rustup`: The Rust toolchain installer and manager.
    * `cargo`: The Rust package manager and build tool. **MANDATORY** for building, testing, running, dependency management, etc.
    * `rustfmt`: For code formatting (see Section 2).
    * `clippy`: For static analysis and linting (see Section 3).
* **Recommended Tools:**
    * `rust-analyzer`: Language server for IDEs/editors, providing real-time feedback, completion, and navigation. Strongly recommended for developer productivity.
    * `cargo-edit`: For managing dependencies via the command line (`cargo add`, `cargo rm`).
    * `cargo-audit`: For auditing dependencies for security vulnerabilities (see Section 13).
* **Environment:** Developers should configure their editors/IDEs for seamless integration with Rust tools, including format-on-save (`rustfmt`), real-time linting (`clippy`), type checking (`cargo check`), and debugging support (e.g., via LLDB/GDB integration).

---

## 2. Formatting (`rustfmt`)

* **Standard:** Code formatting using `rustfmt` is **ABSOLUTELY NON-NEGOTIABLE**.
* **Shared Configuration:** A `rustfmt.toml` or `.rustfmt.toml` configuration file **MAY** exist in the project root if deviations from `rustfmt` defaults are necessary and agreed upon. If present, it **MUST** be version-controlled. However, strive to adhere to defaults.
* **Enforcement:** Formatting **MUST** be automatically checked (`cargo fmt --check`) and enforced by pre-commit hooks and verified in the CI pipeline. There will be no discussion or deviation regarding Rust code style; `rustfmt` is the standard.

---

## 3. Linting (`clippy`)

* **Mandatory Use:** Static analysis using `clippy` (`cargo clippy`) **MUST** be performed on all Rust code.
* **Strictness:** Run `clippy` with a strict set of lints. Configure via `Cargo.toml` or a `clippy.toml` file if needed, ensuring it is version-controlled. Start with `#[warn(clippy::all)]` and consider promoting specific warnings to denials (`#[deny(...)]`) for critical issues. Aim for `cargo clippy -- -D warnings`.
* **No Suppressions:** As stated in the core philosophy, attributes like `#[allow(...)]` (for `clippy` or `rustc` lints) are **STRICTLY FORBIDDEN** except in extremely rare cases (e.g., FFI, specific macro usage). Any such exception requires a detailed comment (`// ALLOWANCE: Reason...`) explaining the justification and explicit approval during code review.

---

## 4. Crates, Modules, and Project Structure

* **Standard Layout:** Adhere to standard Cargo project layout:
    * `Cargo.toml`, `Cargo.lock`: Manifest and lock file.
    * `src/main.rs`: Binary crate root and entry point.
    * `src/lib.rs`: Library crate root.
    * `src/bin/`: Additional binary crates.
    * `tests/`: Integration tests.
    * `examples/`: Example usage code.
    * `benches/`: Benchmarks.
* **Package by Feature:** Reinforce this principle within `src/`. Organize code into modules (`mod`) based on business features or domains. Prefer `src/user/mod.rs`, `src/order/mod.rs` over technical layering like `src/models.rs`, `src/controllers.rs`. Use nested directories for sub-modules (e.g., `src/user/profile.rs`).
* **Visibility:** Use Rust's visibility modifiers (`pub`, `pub(crate)`, `pub(super)`, private by default) deliberately to encapsulate implementation details. Expose only the necessary public API from modules and crates.
* **Crate Design:** Distinguish between binary and library crates. Libraries should aim for broader usability and stability. Consider extracting core logic into library crates consumed by binary crates.
* **Workspaces:** Use Cargo Workspaces to manage multi-crate projects, sharing dependencies and build artifacts where appropriate.

---

## 5. Naming Conventions

* **Strict Adherence:** **MUST** follow standard Rust API guidelines naming conventions:
    * `snake_case`: Functions, methods, variables, modules, crate names (usually).
    * `PascalCase`: Types (structs, enums, traits), type aliases.
    * `SCREAMING_SNAKE_CASE`: Constants, statics.
* **Clarity:** Names should be clear and descriptive, favoring explicitness. Use domain terminology.

---

## 6. Types, Structs, Enums, and Traits

* **Leverage the Type System:** Use the strong type system extensively. Define precise `struct`s and `enum`s. Use `enum`s (especially with associated data) for modeling states, variants, or alternatives (akin to discriminated unions).
* **Traits for Abstraction:** Use `trait`s to define shared behavior (interfaces). Prefer defining traits in the module that *needs* the abstraction (consumer-defined). Implement traits for concrete types. Leverage trait bounds for generic programming. Follow the "Accept traits, return concrete types" guideline where applicable.
* **Generics:** Use generics (`<T>`) judiciously to reduce code duplication where behavior is identical across different types. Avoid premature or overly complex generic abstractions.
* **Newtype Pattern:** Use the newtype pattern (tuple struct with one element, e.g., `struct UserId(String);`) to create distinct types from primitives, enhancing type safety (e.g., preventing accidental mixing of different kinds of IDs).
* **Composition over Inheritance:** Rust does not have implementation inheritance. Use composition (structs containing other structs/types) and traits for code reuse and polymorphism.

---

## 7. Ownership, Borrowing, and Lifetimes

* **Embrace Ownership:** Understand and leverage Rust's core ownership, borrowing, and lifetime rules. This is fundamental to writing safe and correct Rust code.
* **Prefer Borrowing:** Borrow (`&`, `&mut`) data whenever possible instead of transferring ownership. This often leads to more efficient and flexible code.
* **Explicit Lifetimes:** Use explicit lifetime annotations (`'a`) only when the compiler cannot infer them. Keep lifetimes as short as possible. Complex lifetime requirements often signal a need to rethink data ownership structure.
* **Immutability by Default:** Rust enforces immutability by default (`let x = ...`). Use `mut` explicitly and sparingly when mutation is necessary. This aligns perfectly with the core philosophy's "Default to Immutability".
* **Smart Pointers:** Understand and use standard library smart pointers (`Box`, `Rc`, `Arc`, `RefCell`, `Mutex`, etc.) appropriately for different ownership and memory management scenarios (heap allocation, shared ownership, interior mutability).

---

## 8. Error Handling (`Result`, `panic!`, `?`)

* **`Result<T, E>` is Standard:** **MUST** use the `Result<T, E>` enum for all recoverable errors. Functions that can fail in expected ways **MUST** return `Result`.
* **`panic!` for Unrecoverable Errors:** **FORBIDDEN** for normal control flow or expected error conditions. Use `panic!` *only* for truly exceptional, unrecoverable situations indicating a bug (e.g., violated invariants, impossible states, assertion failures in tests).
* **`?` Operator:** **MUST** use the `?` operator for concise propagation of errors within functions returning `Result`.
* **Error Types:**
    * Define custom `enum`s or `struct`s implementing the `std::error::Error` trait for specific error types within your crate/module. This provides structure and allows callers to handle different errors distinctly.
    * Libraries like `thiserror` are **strongly recommended** for easily creating custom error types via derivation.
    * Libraries like `anyhow` **MAY** be used in *binary crates* (applications) for simpler error handling when specific error types don't need to be handled differently at the top level, but **SHOULD NOT** be used in library crates where callers need specific error information.
* **Contextual Errors:** When propagating errors, add context where appropriate, often by wrapping the underlying error in a custom error type.

---

## 9. Concurrency (Fearless Concurrency)

* **Leverage Safety:** Rust's ownership model and `Send`/`Sync` traits prevent data races at compile time. Embrace this "fearless concurrency".
* **Standard Primitives:** Use standard library concurrency primitives (`std::thread`, `std::sync::{Mutex, RwLock, Arc, mpsc}`) for thread management and synchronization when appropriate.
* **Async/Await:** For I/O-bound concurrency, **MUST** use Rust's `async`/`await` syntax.
    * **Runtime:** Choose and standardize on an async runtime (e.g., **Tokio**, **async-std**) for the project. Binary crates set up the runtime; libraries should be runtime-agnostic if possible.
    * **`Send`/`Sync` Bounds:** Pay attention to `Send`/`Sync` bounds required by async operations and ensure types used across `.await` points meet them.
* **Avoid Shared Mutable State:** Prefer message passing (channels) or immutable shared data (`Arc<T>`) over shared mutable state (`Arc<Mutex<T>>`) where possible, as it often simplifies reasoning.

---

## 10. Unsafe Code (`unsafe`)

* **Avoid `unsafe`:** **STRONGLY DISCOURAGED.** The primary benefit of Rust is safety; `unsafe` bypasses compiler guarantees.
* **Justification Required:** Use of `unsafe` blocks or functions **MUST** be minimized and **STRICTLY JUSTIFIED**. It is typically only permissible for:
    * FFI (Foreign Function Interface) calls.
    * Interacting with hardware or low-level OS features.
    * Implementing specific low-level data structures or optimizations where safety invariants are manually upheld and *proven* correct.
* **Encapsulation:** If `unsafe` is necessary, it **MUST** be encapsulated within a safe abstraction (a module or function) whose public API guarantees safety. The `unsafe` block itself **MUST** be commented with a `// SAFETY:` comment explaining exactly why the code is safe despite bypassing compiler checks.
* **Scrutiny:** Code using `unsafe` will receive the highest level of scrutiny during code reviews.

---

## 11. Testing (`#[test]`, Integration, Doc Tests)

* **Built-in Framework:** **MUST** use Rust's built-in testing framework (`#[test]`, `assert!`, `assert_eq!`, etc.). External assertion crates (e.g., `assert_matches`, `pretty_assertions`) may be used if standardized for the project.
* **Structure:**
    * Unit Tests: Place `#[test]` functions in submodules named `tests` (e.g., `mod tests { ... }`) within the same file as the code being tested (`src/my_module.rs`).
    * Integration Tests: Place in the `tests/` directory at the crate root. Each `.rs` file is compiled as a separate crate. Test the public API of your library crate.
    * Doc Tests: Write example code blocks within documentation comments (`///`) that demonstrate usage. `cargo test` automatically runs these. **Strongly encouraged** for public APIs.
* **`#[should_panic]`:** Use `#[should_panic]` to test that code panics under specific error conditions, but prefer testing for `Err` variants of `Result` where applicable.
* **Coverage:** Test coverage **MUST** meet the thresholds defined in the core philosophy, enforced by CI using tools like `cargo-tarpaulin` or `grcov`.
* **Mocking Policy:**
    * Reiterate: **NO MOCKING INTERNAL COLLABORATORS/MODULES.**
    * Leverage Rust's trait system and Dependency Injection. Define traits for external dependencies (DBs, APIs, filesystem) *in your crate*. Provide test doubles (fakes, stubs implementing the trait) in your tests.
    * Libraries like `mockall` **MAY** be used *sparingly* and *only* for mocking true external dependencies defined by traits, if simpler fakes are insufficient. Avoid complex mocking setups.

---

## 12. Logging (`log`, `tracing`)

* **Standard Facade:** Use the `log` crate as the standard logging facade API. Libraries should depend only on `log`.
* **Implementation:** Binary crates choose and configure a logging implementation that plugs into the `log` facade (e.g., `env_logger`, `fern`).
* **Structured Logging:** The chosen implementation **MUST** be configured for **JSON output** in production and CI environments.
* **`tracing` Crate:** For applications requiring more advanced observability (spans, structured events, async context), the `tracing` ecosystem **SHOULD** be preferred over `log`. Configure `tracing-subscriber` for JSON output.
* **Configuration:** Configure the minimum log level via environment variables (e.g., `RUST_LOG`). Default to `INFO` in production.
* **Contextual Logging:** Include mandatory context fields (timestamp, level, target/module, correlation_id, etc.) as specified in the core philosophy. Use `tracing`'s span context or pass contextual data explicitly.

---

## 13. Dependency Management (Cargo)

* **`Cargo.toml`:** Maintain a clean `Cargo.toml`. Specify crate metadata, dependencies, and features accurately.
* **`Cargo.lock`:** The `Cargo.lock` file **MUST** be committed to version control for binary crates and *may* be committed for library crates (depending on policy, often recommended for CI stability).
* **`cargo update`:** Keep dependencies reasonably updated. Use `cargo update` carefully. Leverage automated tools like Dependabot/Renovate Bot.
* **Features:** Use Cargo features judiciously to manage optional dependencies and conditional compilation.
* **Vulnerability Scanning:** Integrate `cargo audit` into the CI pipeline. Builds **MUST** fail on critical/high severity vulnerabilities.

---

## 14. Builds and Deployment Artifacts

* **Build Profiles:** Understand and use Cargo build profiles (`[profile.dev]`, `[profile.release]`) in `Cargo.toml` to control optimization levels, debug symbols, etc.
* **Release Builds:** Production artifacts **MUST** be built using the release profile (`cargo build --release`).
* **Static Linking:** Rust typically produces statically linked binaries by default on Linux (when using `musl` target or if C dependencies are static), simplifying deployment.
* **Cross-Compilation:** Leverage `rustup target add` and Cargo's build target options (`--target`) for cross-compilation needs.
* **Dockerfiles:** Utilize multi-stage Docker builds. Use a `rust` base image for building (`cargo build --release`), then copy the compiled binary into a minimal runtime image (e.g., `debian:slim`, `gcr.io/distroless/static-debian11`, or `scratch` if fully static).

---

## 15. Macros (`macro_rules!`, Procedural)

* **Use Judiciously:** Macros enable powerful metaprogramming but can increase complexity and hinder readability/tooling if overused or poorly written.
* **`macro_rules!`:** Prefer functions and generics over declarative macros (`macro_rules!`) unless there's a clear need for code generation based on syntax (e.g., DSLs, repetitive boilerplate). Keep them simple and well-documented.
* **Procedural Macros:** Use procedural macros (derive, attribute-like, function-like) primarily via established ecosystem crates (e.g., `serde_derive`, `thiserror`, `async_trait`). Writing custom procedural macros is complex and should only be done when the benefit clearly outweighs the significant maintenance cost and complexity.
* **Hygiene:** Be aware of macro hygiene to avoid unintended variable captures.

---

## 16. Foreign Function Interface (FFI)

* **Safety Wrappers:** When interacting with C libraries via FFI, **MUST** create safe Rust wrappers around the `unsafe` FFI calls. The public API of the wrapper module **MUST** maintain Rust's safety guarantees.
* **`unsafe` Justification:** FFI is a primary valid use case for `unsafe`. Follow the guidelines in Section 10.
* **`repr(C)`:** Use `#[repr(C)]` on structs passed across the FFI boundary to ensure predictable memory layout compatible with C.
* **Error Handling:** Carefully translate error codes or conventions from the C library into Rust `Result` types within the safe wrapper.
* **Resource Management:** Ensure resources acquired from the C library (memory, file handles) are properly managed (e.g., using RAII wrappers implementing `Drop`).


