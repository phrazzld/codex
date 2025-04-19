# DEVELOPMENT PHILOSOPHY - APPENDIX GO

## Introduction

This document specifies the Go language-specific standards, tooling requirements, and idiomatic practices required for our projects. It serves as a mandatory extension to the main **Development Philosophy (v3)** document. All Go code written for our projects **MUST** adhere to the guidelines herein, in addition to the core philosophy.

**Reference:** Always refer back to the main [Development Philosophy](DEVELOPMENT_PHILOSOPHY.md) for overarching principles.

## Table of Contents

- [1. Tooling and Environment](#1-tooling-and-environment)
- [2. Formatting (`gofmt`/`goimports`)](#2-formatting-gofmtgoimports)
- [3. Linting (`golangci-lint`)](#3-linting-golangci-lint)
- [4. Package Design and Project Structure](#4-package-design-and-project-structure)
- [5. Naming Conventions](#5-naming-conventions)
- [6. Types, Structs, and Initialization](#6-types-structs-and-initialization)
- [7. Interfaces (Usage and Design)](#7-interfaces-usage-and-design)
- [8. Error Handling (The Go Way)](#8-error-handling-the-go-way)
- [9. Concurrency (Goroutines, Channels, Context)](#9-concurrency-goroutines-channels-context)
- [10. Testing](#10-testing)
- [11. Logging (`log/slog`)](#11-logging-logslog)
- [12. Dependency Management (Go Modules)](#12-dependency-management-go-modules)
- [13. Builds and Deployment Artifacts](#13-builds-and-deployment-artifacts)

---

## 1. Tooling and Environment

* **Go Version:** Projects **MUST** use the latest stable Go release specified in the project's `go.mod` file (e.g., `go 1.21`). Updates to newer stable versions should be managed proactively.
* **Mandatory Tools:**
    * `go`: The standard Go toolchain is required for building, testing, running, and module management.
    * `gofmt` / `goimports`: For code formatting (see Section 2).
    * `golangci-lint`: For static analysis and linting (see Section 3).
* **Dependency Management:** Go Modules (`go.mod`, `go.sum`) are **MANDATORY**. Ensure `go.mod` and `go.sum` are checked into version control. Vendoring (`vendor/` directory) may be used if specific project requirements necessitate it, but Go Modules remain the source of truth.
* **Environment:** Developers should configure their editors/IDEs for seamless integration with Go tools, including format-on-save (`goimports`), real-time linting feedback (`golangci-lint`), and debugging support.

---

## 2. Formatting (`gofmt`/`goimports`)

* **Standard:** Code formatting using `gofmt` is **ABSOLUTELY NON-NEGOTIABLE**. `goimports` (which includes `gofmt`) is the preferred tool as it also manages import statements.
* **Enforcement:** Formatting **MUST** be automatically checked and enforced by pre-commit hooks and verified in the CI pipeline. There will be no discussion or deviation regarding Go code style; `gofmt` is the standard.

---

## 3. Linting (`golangci-lint`)

* **Mandatory Use:** Static analysis using `golangci-lint` **MUST** be performed on all Go code.
* **Shared Configuration:** A `.golangci.yml` configuration file **MUST** exist in the project root, be version-controlled, and define a strict set of enabled linters and their settings. This ensures consistency across all developers and CI environments.
* **Recommended Linters (Baseline):** The configuration should enable a comprehensive set including (but not limited to): `errcheck`, `govet`, `staticcheck`, `unused`, `ineffassign`, `gocritic`, `stylecheck`, `gofmt`, `goimports`, `nolintlint`, `gocyclo` (with a reasonably low complexity limit, e.g., 15), `bodyclose`, `durationcheck`, `exportloopref`, `makezero`, `sqlclosecheck`, `unconvert`, `unparam`.
* **No Suppressions:** As stated in the core philosophy, directives like `//nolint:` are **STRICTLY FORBIDDEN** except in extremely rare cases. Any such exception requires a detailed comment explaining the justification and explicit approval during code review. Use `nolintlint` to detect unneeded or unexplained suppressions.

---

## 4. Package Design and Project Structure

* **Standard Layout:** Adhere to standard Go project layout conventions. A common structure includes:
    * `/cmd/{appname}/main.go`: Main application(s) entry points.
    * `/internal/`: Private application and library code. Code here cannot be imported by external projects. Organize by feature/domain within `/internal`.
    * `/pkg/`: Library code intended to be potentially used by external applications (use with caution; prefer `/internal` unless reuse is a definite requirement).
* **Package by Feature:** Reinforce this principle. Group related types, functions, and interfaces by business feature or domain capability within `/internal` (e.g., `/internal/user`, `/internal/order`). Avoid utility packages (`/internal/utils`) where possible; prefer co-location or well-defined domain packages.
* **Package Naming:** Packages **MUST** have short, concise, lowercase names. Avoid underscores and camelCase. The name should be descriptive of its contents. Avoid stutter (e.g., `package user` should contain `type Profile` not `type UserProfile`).
* **Cohesion & Coupling:** Packages must exhibit high internal cohesion and low external coupling.
* **No Circular Dependencies:** Circular package dependencies are **FORBIDDEN** and will break the build. Design package interactions to form a Directed Acyclic Graph (DAG).

---

## 5. Naming Conventions

* **Visibility:** `PascalCase` for exported identifiers (accessible outside the package); `camelCase` for unexported identifiers (package-private).
* **Clarity:** Names should be clear and descriptive. Prefer shorter names for variables with smaller scopes (e.g., `i` for loop index, `ctx` for context).
* **Acronyms:** Treat acronyms consistently. Generally, capitalize them if at the start or entirely forming the name (e.g., `ServeHTTP`, `ID`, `API`), otherwise use standard casing (e.g., `userID`, `parseURL`). Follow `stylecheck` linter guidance (ST1003).
* **Receivers:** Use short (often 1-2 letters derived from the type), consistent names for method receivers (e.g., `u` for `User`, `or` for `orderRepo`).
* **Package Names:** See Section 4.

---

## 6. Types, Structs, and Initialization

* **Structs:** Use `struct` for grouping data. Keep them focused on a single concept. Use embedding for composition (`is-a` or `has-a` relationships where appropriate).
* **Zero Value:** Strive to make the zero value of a type useful. Initialize structs using field names for clarity (e.g., `user.Profile{ID: id, Name: name}`).
* **Constructors:** Provide constructor functions (e.g., `func NewThing(...) (*Thing, error)`) for types requiring initialization logic, validation, or dependency setup. Return errors if construction can fail. Avoid exporting struct types directly if controlled initialization is necessary.
* **Pointers vs. Values:**
    * Use value receivers if the method doesn't need to mutate the receiver.
    * Use pointer receivers (`*T`) if the method needs to mutate the receiver's state.
    * Pass structs by value if they are small and inherently immutable or if you want to ensure the function receives a copy.
    * Pass structs by pointer (`*T`) if they are large, if nil is a valid representation, or if mutation is intended. Be mindful of nil pointer dereferences.

---

## 7. Interfaces (Usage and Design)

* **Consumer-Defined:** Interfaces are typically defined in the package that *consumes* the behavior, not the package that implements it. This aligns with Dependency Inversion.
* **Small & Focused:** Interfaces **MUST** be small, usually containing only 1-3 methods. Prefer single-method interfaces where possible (e.g., `io.Reader`, `http.Handler`). This adheres to the Interface Segregation Principle.
* **Naming:** Interface names often describe the behavior, frequently ending with `-er` (e.g., `Reader`, `Writer`, `Logger`).
* **Guideline:** "Accept interfaces, return structs." This promotes flexibility in dependencies while providing concrete return types.

---

## 8. Error Handling (The Go Way)

* **Explicit Checks:** Errors **MUST** be handled explicitly using `if err != nil { ... }`. Ignoring errors (assigning to `_`) requires justification if not immediately obvious (e.g., closing a resource where the error is non-critical). `errcheck` linter helps enforce this.
* **Error Wrapping:** **MUST** use `fmt.Errorf` with the `%w` verb (requires Go 1.13+) to wrap errors when adding context. This allows inspection of the error chain using `errors.Is` and `errors.As`.
    ```go
    // DO:
    if err != nil {
        return fmt.Errorf("processing order %d: %w", orderID, err)
    }
    ```
* **`errors.Is` / `errors.As`:** Use `errors.Is` for checking against sentinel error values (see below) and `errors.As` for checking if an error in the chain matches a specific custom type.
* **Sentinel Errors:** Define sentinel errors using `errors.New` for simple, fixed error conditions that callers might need to check for specifically. Export them if they are part of a package's public API.
    ```go
    var ErrNotFound = errors.New("resource not found")
    // Check: errors.Is(err, ErrNotFound)
    ```
* **Custom Error Types:** Define custom `struct` types implementing the `error` interface when errors need to carry additional structured data.
    ```go
    type ValidationError struct {
        Field   string
        Message string
    }

    func (e *ValidationError) Error() string {
        return fmt.Sprintf("validation failed for field '%s': %s", e.Field, e.Message)
    }
    // Check: var valErr *ValidationError; if errors.As(err, &valErr) { ... }
    ```
* **`panic`/`recover`:** **FORBIDDEN** for normal control flow or expected error conditions. Use `panic` only for truly exceptional, unrecoverable situations (e.g., programmer errors like nil dereferences in contexts where recovery is impossible, fatal initialization issues).

---

## 9. Concurrency (Goroutines, Channels, Context)

* **Necessity:** Use goroutines and channels only when concurrency genuinely simplifies the design or is required for performance/responsiveness. Avoid unnecessary complexity.
* **Race Detection:** Always run tests with the `-race` flag enabled in CI (`go test -race ./...`). Fix any reported race conditions immediately.
* **Synchronization:** Use standard `sync` package primitives (`Mutex`, `RWMutex`, `WaitGroup`, `Once`, `Cond`) correctly when sharing memory between goroutines. Prefer channels for communication where it simplifies the design.
* **`context.Context`:** **MANDATORY** for managing cancellation, deadlines, and passing request-scoped data (like correlation IDs, authenticated user info) across API boundaries and asynchronous operations.
    * Pass `ctx` as the first argument to functions that may block, perform I/O, or need request-scoped information.
    * Propagate `ctx` explicitly through call chains.
    * Check for context cancellation (`<-ctx.Done()`) in long-running operations.

---

## 10. Testing

* **Standard Library:** The built-in `testing` package is the primary tool for writing tests. External assertion libraries (e.g., `testify/assert`, `testify/require`) may be used if standardized for the project, but are not required.
* **Structure:**
    * Test files: `*_test.go`.
    * Test functions: `func TestXxx(t *testing.T)`.
    * Benchmarks: `func BenchmarkXxx(b *testing.B)`.
    * Examples: `func ExampleXxx()`.
    * Table-Driven Tests: **Strongly preferred** for testing functions with multiple input/output scenarios. Use `struct` slices for test cases.
    * Subtests: Use `t.Run("subtest_name", func(t *testing.T) { ... })` to group related assertions and improve test output clarity. `t.Parallel()` may be used within subtests where appropriate.
* **Coverage:** Test coverage **MUST** meet the thresholds defined in the core philosophy, enforced by CI using `go test -coverprofile=coverage.out ./...` and coverage reporting tools.
* **Integration Tests:**
    * Use build tags (e.g., `//go:build integration`) to separate slow integration tests from fast unit tests.
    * Run integration tests separately in CI (`go test -tags=integration ./...`).
    * Consider tools like `testcontainers-go` for managing external dependencies (databases, queues) within integration tests.
* **Mocking Policy:**
    * Reiterate: **NO MOCKING INTERNAL COLLABORATORS.**
    * Mock external dependencies (DBs, APIs) by defining interfaces *in the consuming package* and providing test doubles (fakes, stubs) in the tests.
    * Standard library interfaces (`io.Reader`, `http.ResponseWriter`) can often be faked easily (e.g., `bytes.Buffer`, `httptest.ResponseRecorder`).

---

## 11. Logging (`log/slog`)

* **Standard Library:** `log/slog` (available since Go 1.21) **MUST** be used as the standard structured logging library, unless a specific third-party library (e.g., `zerolog`, `zap`) has been explicitly approved and standardized for the project.
* **JSON Output:** Configure `slog` (or the approved alternative) to output logs in **JSON format** for production and CI environments using `slog.NewJSONHandler`.
* **Configuration:** Set the appropriate minimum log level via configuration (environment variables preferred). Default to `INFO` in production.
* **Contextual Logging:**
    * Pass logger instances (potentially with pre-set attributes like `service_name`) via dependency injection or retrieve them from `context.Context`.
    * Always include the mandatory context fields specified in the core philosophy's Logging Strategy, especially the `correlation_id`. Use `slog.HandlerOptions` or custom handlers/middleware to automatically inject common fields.

---

## 12. Dependency Management (Go Modules)

* **`go.mod`:** Maintain a clean `go.mod` file. Specify the minimum Go version.
* **`go mod tidy`:** Run `go mod tidy` regularly (e.g., in pre-commit hooks, CI) to ensure `go.mod` and `go.sum` are consistent and minimal.
* **Updates:** Keep dependencies reasonably updated. Use `go list -m -u all` to check for updates. Leverage automated tools like Dependabot/Renovate Bot.
* **Vulnerability Scanning:** Integrate `govulncheck` into the CI pipeline to scan for known vulnerabilities in dependencies. Builds **MUST** fail on critical/high severity issues.

---

## 13. Builds and Deployment Artifacts

* **Static Binaries:** Leverage Go's capability to produce statically linked binaries (`CGO_ENABLED=0 GOOS=linux go build ...`) for easy deployment, especially within containers.
* **Dockerfiles:** Utilize multi-stage Docker builds. Start with a `golang` base image for building, then copy the compiled static binary into a minimal runtime image (e.g., `gcr.io/distroless/static-debian11`, `scratch`, or `alpine` if necessary). This minimizes the final image size and attack surface.
* **Build Flags:** Consider using `-ldflags="-s -w"` during the final build stage to strip debug symbols and reduce binary size for production artifacts.

