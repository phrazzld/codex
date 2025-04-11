# Documentation Approach

This document outlines our philosophy and practices for project documentation. Our goal is effective communication and knowledge sharing—whether with team members, future contributors, or our future selves—achieved with minimal friction and maximum clarity. We prioritize documentation methods that are closely tied to the code and reflect the rationale behind our decisions, aligning with the Core Principles of *Explicit is Better than Implicit* and *Document Decisions, Not Mechanics*.

---

## 1. Prioritize Self-Documenting Code

**Approach:** The codebase itself is the primary and most accurate source of documentation regarding *how* the system works. We achieve this through:
* **Clear Naming:** Adhering strictly to meaningful naming conventions (see `CODING_STANDARDS.md`).
* **Strong Typing:** Leveraging static types (TypeScript, Go types) to define data structures and contracts explicitly.
* **Logical Structure:** Organizing code into small, focused modules/packages with clear responsibilities (see `ARCHITECTURE_GUIDELINES.md`).
* **Readability:** Following consistent formatting and linting rules, and writing straightforward logic.
* **Well-Written Tests:** Tests often serve as executable examples of how components are intended to be used (see `TESTING_STRATEGY.md`).

**Rationale:** Code is the ultimate source of truth. Relying heavily on external documentation for low-level mechanics creates a significant synchronization burden and inevitably leads to outdated information. Well-factored, clearly written code minimizes the need for supplementary explanation of *what* it does.

**Implementation:** Before writing extensive comments or external documents explaining code mechanics, always ask: "Can I refactor the code itself to make its purpose and operation clearer?"

---

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

---

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

---

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

---

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

---

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
