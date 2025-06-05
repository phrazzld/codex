```text
## Technical Overview of /Users/phaedrus/Development/codex/bin/thinktank_wrapper/src/thinktank_wrapper/templates

**Purpose:**

This directory houses a collection of prompt templates used by the `thinktank_wrapper` application. These templates are designed to guide large language models (LLMs) in performing various software engineering tasks, such as planning, code review, task breakdown, security auditing, and documentation improvement. The templates provide a structured framework for the LLM to follow, ensuring that the generated output is focused, actionable, and aligned with specific goals and development philosophies.

**Architecture:**

The directory's architecture is flat; it contains only `.md` files and a `__init__.py` file. Each `.md` file represents a single prompt template. The `__init__.py` file serves as a simple package declaration, though it currently contains only a docstring. The templates themselves are written in Markdown, allowing for clear formatting and easy readability.  Each template follows a consistent structure, typically including:

*   A high-level instruction set defining the LLM's role and mission.
*   Context injection points (using `<!-- BEGIN:CONTEXT -->` and `<!-- END:CONTEXT -->` tags) to insert relevant information, such as task descriptions, code snippets, or development philosophy documents.
*   Detailed steps and guidelines for the LLM to follow in order to complete the assigned task.
*   Specific output format requirements, ensuring the generated content is structured and easily parsed.

**Key File Roles:**

*   **`plan.md`**:  Generates a detailed implementation plan for a given task, focusing on technical details, risks, and trade-offs.
*   **`review-diff.md`**:  Performs a diff-focused code review, identifying functional issues, bugs, and critical problems in the changed lines of code.
*   **`ticket.md`**:  Breaks down an implementation plan into a set of atomic, testable engineering tickets, formatted for a `TODO.md` file.
*   **`whiteboard.md`**:  Facilitates creative technical brainstorming, exploring various approaches to implementing a backlog item.
*   **`address.md`**:  Creates a remediation plan based on code review feedback, prioritizing and detailing steps to address identified issues.
*   **`execute.md`**:  Analyzes and selects the best implementation approach for a given task, justifying the choice and outlining build steps.
*   **`gordian.md`**:  Identifies opportunities to simplify the codebase by eliminating unnecessary complexity and finding transformative solutions.
*   **`review-philosophy.md`**:  Evaluates code changes against a defined development philosophy, focusing on maintainability, testability, and adherence to coding standards.
*   **`review.md`**:  Provides brutal code review instructions, hunting down flaws, oversights, and philosophical breaches in a code diff.
*   **`__init__.py`**:  Declares the directory as a Python package.
*   **`audit.md`**:  Performs a security audit of the codebase, generating actionable backlog items for remediation.
*   **`diagram.md`**:  Generates Mermaid diagrams to visualize system architecture, workflows, or relationships.
*   **`document.md`**:  Analyzes documentation and creates a plan for comprehensive improvements.
*   **`groom.md`**:  Transforms a basic backlog into a comprehensive, well-organized roadmap.
*   **`resolve.md`**:  Resolves Git merge conflicts, preserving functionality and maintaining code quality.
*   **`shrink.md`**:  Generates backlog items to optimize code size while preserving functionality.
*   **`align.md`**:  Generates backlog items that improve alignment with a defined development philosophy.
*   **`ci-failure.md`**:  Analyzes CI pipeline failures and creates a detailed resolution plan.
*   **`consult.md`**: Decomposes consultant advice into a detailed set of tasks.
*   **`extract.md`**:  Identifies opportunities to extract code into reusable modules.
*   **`ideate.md`**:  Generates innovative ideas for the project in the form of backlog items.
*   **`refactor.md`**:  Generates backlog items for refactoring the codebase to improve quality and maintainability.
*   **`scope.md`**: Analyzes implementation plans to ensure they have appropriate scope.
*   **`debug.md`**: Analyzes a reported bug, systematically investigates its root cause, and generates actionable debugging tasks.

**Important Dependencies or Gotchas:**

*   **LLM Dependency:** The effectiveness of these templates heavily relies on the capabilities of the underlying LLM.  The LLM must be able to understand and follow the instructions provided in the templates, as well as generate coherent and relevant code, plans, and analyses.
*   **Context Injection:** The quality of the injected context is crucial.  Insufficient or inaccurate context can lead to poor results.  The templates use `<!-- BEGIN:CONTEXT -->` and `<!-- END:CONTEXT -->` as placeholders for injected content.
*   **Development Philosophy:** Several templates reference a `DEVELOPMENT_PHILOSOPHY.md` file. The absence or inconsistency of this file can significantly impact the alignment of the generated output with the project's goals.
*   **Output Parsing:** The templates are designed to generate structured output in Markdown format.  The application using these templates must be able to reliably parse this output to extract the relevant information (e.g., task lists, code snippets, risk assessments).
*   **Task ID Management:** Several templates (e.g., `ticket.md`, `debug.md`) involve generating or referencing task IDs. Proper management of these IDs is essential to maintain consistency and avoid conflicts.  The templates generally assume a `TODO.md` file exists or is created.
*   **Security Considerations:** The `audit.md` template focuses on security auditing.  However, the generated audit findings should always be reviewed and validated by human security experts.  Relying solely on the LLM's analysis could lead to missed vulnerabilities.
*   **Markdown Interpretation**: The mermaid diagrams in `diagram.md` will only render correctly if the output is interpreted by a markdown renderer that supports the mermaid syntax.
```