# DEVELOPMENT PHILOSOPHY - APPENDIX SWIFT/IOS

## Introduction

This document specifies the Swift language-specific and iOS platform-specific standards, architecture patterns, tooling requirements, and idiomatic practices required for our mobile projects. It serves as a mandatory extension to the main **Development Philosophy (v3)** document. All Swift code written for our iOS projects **MUST** adhere to the guidelines herein, in addition to the core philosophy.

**Reference:** Always refer back to the main [Development Philosophy](DEVELOPMENT_PHILOSOPHY.md) for overarching principles.

## Table of Contents

- [1. Tooling and Environment](#1-tooling-and-environment)
- [2. Formatting (SwiftFormat/Xcode)](#2-formatting-swiftformatxcode)
- [3. Linting (SwiftLint)](#3-linting-swiftlint)
- [4. Project Structure and Architecture](#4-project-structure-and-architecture)
- [5. Naming Conventions](#5-naming-conventions)
- [6. Types and Data Structures (POP, Value vs. Reference)](#6-types-and-data-structures-pop-value-vs-reference)
- [7. Memory Management (ARC)](#7-memory-management-arc)
- [8. Error Handling](#8-error-handling)
- [9. Concurrency (async/await, Actors, GCD)](#9-concurrency-asyncawait-actors-gcd)
- [10. UI Development (SwiftUI / UIKit)](#10-ui-development-swiftui--uikit)
- [11. Testing (XCTest)](#11-testing-xctest)
- [12. Logging (OSLog, SwiftLog)](#12-logging-oslog-swiftlog)
- [13. Dependency Management (Swift Package Manager)](#13-dependency-management-swift-package-manager)
- [14. Builds, Deployment, and Automation (Xcode, Fastlane)](#14-builds-deployment-and-automation-xcode-fastlane)
- [15. Immutability](#15-immutability)
- [16. Accessibility (a11y)](#16-accessibility-a11y)
- [17. Persistence (Codable, Core Data, Realm, UserDefaults)](#17-persistence-codable-core-data-realm-userdefaults)
- [18. Networking (URLSession)](#18-networking-urlsession)
- [19. API Design within the App](#19-api-design-within-the-app)
- [20. Swift Language Features](#20-swift-language-features)
- [21. Security](#21-security)

---

## 1. Tooling and Environment

* **Swift Version:** Projects **MUST** use the latest stable Swift version compatible with the targeted Xcode version, specified in project documentation. The Minimum Supported Swift Version (MSRV) **MUST** be defined. Updates to newer stable versions should be managed proactively.
* **Xcode:** The latest stable version of Xcode, as approved for project use, is **MANDATORY**. Specific Xcode versions may be enforced per project via `.xcode-version` file if using tools like `xcenv`.
* **Mandatory Tools:**
    * `Xcode`: Including its build system (`xcodebuild`) and command-line tools.
    * `Swift Package Manager (SPM)`: For dependency management (see Section 13).
    * `SwiftLint`: For linting (see Section 3).
* **Recommended Tools:**
    * `SwiftFormat`: For code formatting (see Section 2), if Xcode's formatter isn't sufficient.
    * `Fastlane`: For automation of build, test, and release processes.
    * `Sourcery`: For metaprogramming, especially for generating boilerplate (e.g., mocks for protocols). Use judiciously and with team agreement.
* **Environment:** Developers **MUST** configure Xcode for seamless integration with Swift tools, including enabling warnings, static analysis, and debugging support. Ensure schemes are shared for consistent build and test configurations.

---

## 2. Formatting (SwiftFormat/Xcode)

* **Standard:** Code formatting is **ABSOLUTELY NON-NEGOTIABLE**. Either Xcode's built-in code formatter (configured consistently) or `SwiftFormat` **MUST** be used. The choice should be standardized per project.
* **Shared Configuration:** If `SwiftFormat` is used, a `.swiftformat` configuration file **MUST** exist in the project root, be version-controlled, and define the project's formatting rules. If using Xcode's formatter, settings should be documented.
* **Enforcement:** Formatting **MUST** be automatically checked (e.g., `swiftformat --lint` or a script validating Xcode settings) and enforced by pre-commit hooks and verified in the CI pipeline.

---

## 3. Linting (SwiftLint)

* **Mandatory Use:** Static analysis and linting using `SwiftLint` **MUST** be performed on all Swift code.
* **Shared Configuration:** A `.swiftlint.yml` configuration file **MUST** exist in the project root, be version-controlled, and define a strict set of enabled linters and their settings, including custom rules.
* **Strictness:** Aim for a high level of strictness (e.g., opting into more rules, setting strict thresholds for complexity).
* **No Suppressions:** As stated in the core philosophy, directives like `// swiftlint:disable` or `// swiftlint:disable:next` are **STRICTLY FORBIDDEN** except in extremely rare cases. Any such exception requires a detailed comment (`// SWIFTLINT_SUPPRESSION: Reason...`) explaining the justification and explicit approval during code review. Use `analyzer_rules` for more complex static analysis where possible.

---

## 4. Project Structure and Architecture

* **Standard Layout:** Adhere to standard Xcode project structure (`.xcodeproj` or `.xcworkspace`, groups, and folders).
* **Group by Feature:** Organize code within modules/targets primarily by business feature or domain (e.g., `Features/UserProfile`, `Features/OrderProcessing`) rather than by technical layer (e.g., `ViewModels`, `Views`, `Services`). Infrastructure components (e.g., `Networking`, `Persistence`) can be separate modules.
* **Architectural Pattern:**
    * A modern, scalable architectural pattern such as **MVVM (Model-View-ViewModel) with Coordinators (MVVM-C)**, **VIPER**, or **The Composable Architecture (TCA)** **MUST** be chosen and consistently applied. Avoid Massive View Controller (MVC) anti-patterns.
    * The chosen architecture **MUST** facilitate separation of concerns (UI, presentation logic, business logic, navigation, data management, networking).
* **Dependency Injection (DI):**
    * **MANDATORY.** Dependencies **MUST** be explicitly injected (constructor injection preferred, property injection for UIKit components lifecycle-managed by the system).
    * Avoid ambient context/singletons for dependencies; use DI containers or manual DI. This is crucial for *Testability*.
* **Modularity:** Leverage Swift Package Manager to create local packages/modules for distinct features or shared components to enforce clear boundaries and improve build times.

---

## 5. Naming Conventions

* **Swift API Design Guidelines:** **MUST** strictly adhere to the [Swift API Design Guidelines](https://www.swift.org/documentation/api-design-guidelines/).
    * `PascalCase` for types (structs, enums, protocols, classes), type aliases.
    * `camelCase` for functions, methods, properties, variables, constants, enum cases.
* **Clarity and Brevity:** Names should be clear, descriptive, and promote clarity at the point of use. Avoid abbreviations. Use domain terminology. For UI elements, include the type (e.g., `submitButton`, `userNameLabel`).

---

## 6. Types and Data Structures (POP, Value vs. Reference)

* **Protocol-Oriented Programming (POP):**
    * Embrace POP. Define abstractions using `protocol`s.
    * Use protocol extensions for default implementations.
    * Prefer composing behavior with protocols over class inheritance.
* **Value vs. Reference Types:**
    * **Prefer value types (`struct`, `enum`)** over reference types (`class`) where appropriate, especially for models and data holders. This aligns with *Immutability* and simplifies reasoning about state.
    * Use `class` when identity or shared mutable state is essential (e.g., ViewModels managing state, service clients).
* **`final` Keyword:** Classes not designed for inheritance **MUST** be marked `final` to improve performance and signal intent.
* **Enums:** Use `enum`s extensively, especially with associated values, for modeling distinct states, alternatives, or configurations in a type-safe manner.
* **Type Aliases:** Use `typealias` to improve readability for complex types or to clarify intent (e.g., `typealias UserID = String`).

---

## 7. Memory Management (ARC)

* **Automatic Reference Counting (ARC):** Understand that ARC manages memory for reference types.
* **Retain Cycles:** Developers **MUST** actively prevent and resolve retain cycles:
    * Use `weak` or `unowned` references for inverse relationships (e.g., delegate patterns). Understand the difference: `weak` for optional references, `unowned` when the reference is guaranteed to exist for the lifetime.
    * Use capture lists (`[weak self]`, `[unowned self]`) in closures that capture `self` (especially in escaping closures or when `self` owns the closure).
* **Instruments:** Use Xcode's Instruments (e.g., Leaks, Allocations) to detect memory issues.

---

## 8. Error Handling

* **Swift `Error` Protocol:** Recoverable errors **MUST** be modeled using types conforming to the `Error` protocol. Custom error `enum`s are preferred for domain-specific errors.
* **`do-try-catch`:** Use `do-try-catch` for handling synchronous throwing functions.
* **`Result<Success, Failure: Error>`:** **Strongly preferred** for asynchronous operations and for representing success or failure explicitly.
* **Propagation:** Propagate errors by re-throwing or returning them in a `Result` type. Avoid "swallowing" errors.
* **`try?` and `try!`:**
    * `try?` (optional try) should be used judiciously when `nil` is a valid outcome for a failed operation and error details are not needed.
    * `try!` (forced try) is **STRICTLY FORBIDDEN** except in cases where a failure is a programmer error and unrecoverable (e.g., loading critical bundled resources during app startup, where `fatalError` would be the alternative). Justify with a comment.
* **`fatalError(_:file:line:)`:** Use *only* for unrecoverable programmer errors or impossible states that indicate a bug.

---

## 9. Concurrency (async/await, Actors, GCD)

* **`async/await`:** **MANDATORY** for all new asynchronous code (Swift 5.5+). This improves readability and simplifies error handling.
* **Actors:** Use `actor`s to protect shared mutable state in concurrent environments.
* **`@MainActor`:** UI updates and interactions with UIKit/SwiftUI view properties **MUST** be performed on the main thread, typically by marking functions or types with `@MainActor`.
* **Grand Central Dispatch (GCD):** May be used for specific low-level tasks or in older codebases. Prefer `async/await` for new development. Understand dispatch queues (serial, concurrent, global, main).
* **Combine Framework:** If the project standardizes on Combine for reactive programming, it **MUST** be used consistently. Otherwise, prefer `async/await`.
* **Cancellation:** Support task cancellation using `Task.checkCancellation()` and structured concurrency patterns.

---

## 10. UI Development (SwiftUI / UIKit)

* **Framework Choice:**
    * **SwiftUI:** Preferred for new projects or new features where its capabilities are sufficient. Embrace its declarative, compositional nature.
    * **UIKit:** For existing projects or when SwiftUI does not meet specific requirements.
    * A project **MUST** standardize on one primary UI framework or have clear guidelines for interoperability (`UIViewRepresentable`, `UIViewControllerRepresentable`).
* **If UIKit:**
    * **Programmatic UI:** Prefer building UI programmatically for better testability, maintainability, and easier code reviews, unless Storyboards/XIBs are a strictly enforced project standard for simpler screens.
    * **Auto Layout:** Use Auto Layout for adaptive UIs. Constraints should be defined clearly and efficiently.
    * **View Controllers:** Keep View Controllers focused on view management and user interaction delegation. Logic should reside in ViewModels or other architectural components.
* **If SwiftUI:**
    * **State Management:** Use SwiftUI's state management tools (`@State`, `@StateObject`, `@ObservedObject`, `@EnvironmentObject`, `@Binding`) correctly according to their purpose.
    * **Views as Functions of State:** Design views to be a function of their state.
    * **Composition:** Build complex views by composing smaller, reusable views.
* **Separation:** Regardless of the framework, UI logic **MUST** be separated from business logic (e.g., via ViewModels).

---

## 11. Testing (XCTest)

* **XCTest Framework:** The `XCTest` framework is **MANDATORY** for all unit and UI tests.
* **Test Types:**
    * **Unit Tests:** Target individual components (ViewModels, services, utility functions, models) in isolation.
    * **UI Tests (`XCUIApplication`):** Cover critical user flows and UI interactions. Use sparingly due to their slower execution and potential flakiness; prioritize unit and integration tests.
* **Test Coverage:** **MUST** meet thresholds defined in the core philosophy (e.g., 85% overall, 95% for core logic/ViewModels), enforced by CI.
* **Mocking Policy (CRITICAL - aligned with core philosophy):**
    * **Abstract External Dependencies:** Access external dependencies (Network, Database, System Services like Location/Bluetooth) via protocols defined *within your app/module*.
    * **Mock ONLY These Abstractions:** Provide test doubles (fakes, stubs, mocks) for these protocols in your tests. Libraries like `Sourcery` can assist in generating mocks for protocols.
    * **NO Mocking Internal Collaborators:** **Mocking internal classes, structs, or protocols defined and implemented within the same application module for the purpose of isolating another internal component is STRICTLY FORBIDDEN.**
    * **Refactor Instead of Internal Mocking:** The need for internal mocking indicates a design flaw (high coupling, poor separation). **The REQUIRED action is to refactor the code under test** (extract pure logic, improve DI, use protocols for actual seams).
* **Asynchronous Testing:** Use `XCTestExpectation` or `async` tests with `await` for testing asynchronous code.
* **Test Organization:** Co-locate unit tests with components where feasible or in dedicated test targets. UI tests reside in their own target.

---

## 12. Logging (OSLog, SwiftLog)

* **`OSLog` (Unified Logging):** **Preferred** for on-device logging. It provides efficient, configurable logging with different levels and categories.
* **Structured Logging to Backend:** If logs are sent to a remote server, use a library like `SwiftLog` as a facade with a backend that supports **JSON output** (e.g., `LoggingOSLog` for local consolidation, or a custom backend for remote transmission).
* **Consistency:** Adhere to the main philosophy's [Logging Strategy](#logging-strategy):
    * Structured JSON for remote logs.
    * Standard log levels (`debug`, `info`, `warning`, `error`).
    * Mandatory context fields (timestamp, level, message, `service_name` (app name/bundle ID), `correlation_id` if applicable for API interactions, function/module).
* **`print()` is FORBIDDEN** for operational logging. Use it only for transient debugging during development.
* **Sensitive Data:** **NEVER** log PII, credentials, or other sensitive data, as per the core philosophy.

---

## 13. Dependency Management (Swift Package Manager)

* **Swift Package Manager (SPM):** **MANDATORY** for managing external dependencies.
* **CocoaPods / Carthage:** **FORBIDDEN** for new projects. Only permissible in legacy projects actively migrating to SPM or for critical dependencies not yet available via SPM.
* **`Package.swift` and `Package.resolved`:** Both files **MUST** be committed to version control. `Package.resolved` ensures reproducible builds.
* **Dependency Updates:** Keep dependencies updated. Leverage tools or manual checks (`swift package update`, `swift package show-dependencies --outdated`). Schedule regular reviews.
* **Vulnerability Scanning:** While less mature than in other ecosystems, investigate and use available tools for scanning Swift package vulnerabilities if they meet project needs.

---

## 14. Builds, Deployment, and Automation (Xcode, Fastlane)

* **Xcode Build System:** `xcodebuild` is the foundation. Manage build settings (`.xcconfig` files are recommended for consistency).
* **Configurations:** Use build configurations (e.g., Debug, Beta, Release) to manage environment-specific settings (API endpoints, logging levels, bundle identifiers for different stages).
* **Schemes:** Define and share Xcode schemes for building, testing, and running different targets and configurations.
* **Code Signing:** Proper code signing setup is **MANDATORY** for device testing and App Store distribution. Prefer automated code signing managed by Xcode where possible.
* **Deployment:**
    * Use **App Store Connect** for TestFlight beta distribution and App Store releases.
    * Adhere to App Store Review Guidelines.
* **Automation (Fastlane):** `Fastlane` is **STRONGLY RECOMMENDED** (and may be mandated per project) for automating:
    * Building and signing the app.
    * Running tests.
    * Managing provisioning profiles and certificates.
    * Taking screenshots.
    * Uploading builds to TestFlight / App Store Connect.
    * Managing app metadata.
* **CI/CD:** Integrate with CI/CD services (e.g., Xcode Cloud, GitHub Actions with macOS runners, Jenkins, GitLab CI) for automated build, test, and deployment pipelines.

---

## 15. Immutability

* **`let` by Default:** **MUST** use `let` to declare constants. Use `var` only when the value genuinely needs to mutate after initialization. This aligns with the core philosophy's "Default to Immutability".
* **Value Types:** Prefer immutable `struct`s for data models. If a `struct` needs to be modified, create a new instance with the changes.
* **Collections:** Use immutable collections (`Array`, `Dictionary`, `Set` declared with `let`) by default. Non-mutating methods (`map`, `filter`, `reduce`) are preferred over in-place mutation.
* **Classes:** For `class` instances, make properties `let` if they are not meant to change after initialization. If a class manages mutable state, ensure this is intentional and well-encapsulated.

---

## 16. Accessibility (a11y)

* **WCAG Compliance is Mandatory:** Applications **MUST** aim for [WCAG 2.1 AA](https://www.w3.org/WAI/WCAG21/quickref/) compliance as applicable to mobile.
* **Key Requirements:**
    * **Accessibility Properties:** Set appropriate accessibility labels, hints, values, and traits for all UI elements using `accessibilityLabel`, `accessibilityHint`, etc.
    * **Dynamic Type:** Support Dynamic Type to allow users to customize font sizes. Test with various font sizes.
    * **VoiceOver:** Ensure app is navigable and usable with VoiceOver. Test manually.
    * **Color Contrast:** Text and meaningful UI elements **MUST** meet minimum color contrast ratios.
    * **Tap Targets:** Ensure all interactive elements have a minimum tap target size (e.g., 44x44 points).
    * **Reduce Motion:** Respect `UIAccessibility.isReduceMotionEnabled`.
* **Testing:** Use Xcode's Accessibility Inspector. Conduct manual testing with accessibility features enabled.

---

## 17. Persistence

* **`Codable` Protocol:** **MANDATORY** for serializing and deserializing data to/from JSON, Plist, or other formats.
* **`UserDefaults`:** Use only for small pieces of data, like user preferences or simple state. **DO NOT** store large amounts of data or sensitive information.
* **Local Databases:**
    * For complex, structured local data storage, choose one primary solution and standardize: **Core Data** or **Realm**.
    * The chosen solution **MUST** be encapsulated behind a repository or service layer.
* **Keychain:** **MANDATORY** for storing all sensitive data (API tokens, passwords, cryptographic keys). Use a wrapper library (e.g., `Valet`, `KeychainAccess`) for easier and safer Keychain interaction.
* **File System:** Store larger files (images, documents) in appropriate directories (e.g., Documents, Caches). Manage storage space responsibly.

---

## 18. Networking

* **`URLSession`:** **MANDATORY** for all HTTP/HTTPS network requests.
* **Abstraction Layer:** Implement a dedicated networking layer (e.g., an API service client) that abstracts `URLSession` details and handles request creation, response parsing, and error handling. This layer should use `async/await`.
* **`Codable` for Payloads:** Use `Codable` types for request and response bodies.
* **Error Handling:** Handle network errors robustly (connectivity issues, timeouts, HTTP status codes). Map these to domain-specific errors or `Result` types.
* **Background Sessions:** Use `URLSessionConfiguration.background(withIdentifier:)` for transfers that should continue when the app is not in the foreground.
* **Security:** Always use HTTPS. Implement certificate pinning if required by security policy.

---

## 19. API Design within the App

* **Clarity and Simplicity:** Internal APIs (functions, methods, protocols) **MUST** be clear, well-documented (using standard Swift documentation comments `///`), and easy to use correctly.
* **Protocol-Oriented Design:** Use protocols to define contracts between components (e.g., between ViewModel and Service, View and ViewModel).
* **Access Control:** Use Swift's access control modifiers (`private`, `fileprivate`, `internal`, `public`, `open`) deliberately to encapsulate implementation details and expose only the necessary API from modules and types. Default to the most restrictive access level possible.

---

## 20. Swift Language Features

* **Optionals:**
    * Handle optionals gracefully using optional chaining (`?`), `if let`, `guard let`, and nil-coalescing (`??`).
    * Force unwrapping (`!`) is **STRICTLY FORBIDDEN** unless an invariant guarantees the value's presence at that point, and this invariant is documented or obvious. A crash due to unexpected `nil` from force unwrapping is a critical bug.
* **Generics:** Use generics to write flexible, reusable functions and types that can work with any type conforming to specified constraints.
* **Closures:** Understand closure syntax, escaping vs. non-escaping closures, and capture lists (see Section 7).
* **Extensions:** Use extensions to organize code by adding new functionality to existing types, conforming types to protocols, or separating concerns within a type.
* **Property Wrappers:** Use property wrappers (`@propertyWrapper`) to reduce boilerplate for common property patterns (e.g., `@AppStorage`, `@Published`, custom wrappers for dependency injection or data validation). Use judiciously.
* **Error Prone Patterns:** Avoid overly complex operator overloads or obscure language features that hinder readability.

---

## 21. Security

* **Input Validation:** Validate all data received from external sources (network, user input, files).
* **Secure Data Storage:** Use Keychain for sensitive data (see Section 17). Encrypt sensitive files if stored outside the Keychain.
* **Secure Networking:** Use HTTPS exclusively. Consider certificate pinning for high-security applications.
* **API Key Management:** **NEVER** embed API keys or secrets directly in code. Use `.xcconfig` files (not committed if containing secrets, use a template) or a build phase script to inject them from a secure location or environment variables in CI.
* **Third-Party Libraries:** Vet third-party libraries for security vulnerabilities. Keep them updated.
* **Jailbreak/Root Detection:** For high-security applications, consider implementing jailbreak/root detection mechanisms, but understand their limitations.
* **Code Obfuscation:** Consider code obfuscation for sensitive algorithms if deemed necessary, but prioritize strong architectural security.
* **Regular Security Audits:** Conduct security reviews and penetration testing as appropriate for the application's risk profile.
