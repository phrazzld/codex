```text
/Users/phaedrus/Development/codex/bin/thinktank_wrapper/src/thinktank_wrapper/templates

This directory contains prompt templates, written in Markdown, used by the `thinktank_wrapper` application.  The purpose of these templates is to provide structured instructions and context to a large language model (LLM), guiding it to perform specific software engineering tasks. The architecture relies on injecting relevant context (e.g., code snippets, error logs) into the templates before passing them to the LLM.  The LLM's output, based on the template and injected context, is then used to generate reports, code, or other artifacts.

Key File Roles:

*   `address.md`:  Instructions for planning remediation of code review findings. It triages feedback, diagnoses issues, proposes fixes, and builds a strike order.
*   `align.md`:  Instructions for generating backlog items that specifically address alignment with the project's development philosophy.
*   `audit.md`:  Instructions for performing a security audit and creating security remediation backlog items.
*   `ci-failure.md`:  Instructions for analyzing CI pipeline failures and creating a resolution plan.
*   `consult.md`: Instructions for translating architectural advice or troubleshooting plans into actionable development tasks.
*   `debug.md`:  Instructions for analyzing bugs and generating actionable debugging tasks for insertion into a TODO list.
*   `diagram.md`:  Instructions for generating Mermaid diagrams to visualize system architecture, workflows, etc.
*   `document.md`:  Instructions for analyzing and improving documentation quality.
*   `execute.md`:  Instructions for analyzing implementation approaches and selecting the best one.
*   `extract.md`:  Instructions for identifying opportunities for code extraction and modularization.
*   `gordian.md`:  Instructions for identifying opportunities for radical simplification of the codebase.
*   `groom.md`:  Instructions for backlog grooming, organizing, and expanding the existing backlog.
*   `ideate.md`: Instructions for generating innovative, technically sound ideas for backlog items.
*   `plan.md`:  Instructions for creating a detailed implementation plan for a given task.
*   `refactor.md`:  Instructions for generating refactoring backlog items.
*   `resolve.md`:  Instructions for resolving Git merge conflicts.
*   `review.md`:  Instructions for performing a brutal code review.
*   `scope.md`: Instructions for analyzing plan scope to ensure manageable pull requests.
*   `shrink.md`:  Instructions for generating backlog items to reduce code size.
*   `ticket.md`:  Instructions for breaking down a plan into actionable engineering tickets.
*   `whiteboard.md`:  Instructions for creative technical brainstorming.
*   `__init__.py`:  Marks the directory as a Python package.

Important Dependencies/Gotchas:

*   The effectiveness of these templates heavily relies on the quality and relevance of the injected context.  Poor context will lead to poor results from the LLM.
*   The templates are designed to be strict and opinionated, enforcing specific coding standards and architectural principles.  This might require careful customization depending on the project's specific needs.
*   The templates assume the LLM has a good understanding of software engineering principles and best practices.
*   Each template expects specific input files (e.g., `BUG.MD`, `BUGFIXPLAN.md`, `DEVELOPMENT_PHILOSOPHY.md`) to be present and correctly formatted.
*   Many templates rely on a `DEVELOPMENT_PHILOSOPHY.md` file, which is not present in this directory, but is assumed to exist elsewhere.  This file defines the project's coding standards, architectural principles, and other development guidelines.  The contents of this file are crucial for the LLM to generate appropriate and consistent output.
*   The templates often use Markdown formatting for output, including task lists and tables. The application consuming the output must be able to parse this Markdown correctly.
*   The templates follow a consistent pattern of a preamble, analysis instructions, and output format specification.
*   The templates frequently emphasize simplicity, modularity, testability, and maintainability.
```