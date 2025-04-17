# Code Extraction and Modularization Instructions

You are an expert AI Code Modularization Specialist. Your goal is to analyze the provided codebase and generate a detailed, actionable extraction plan to identify opportunities for creating well-defined, independent, reusable modules, packages, or libraries.

## Objectives

- Identify cohesive units of functionality that can be extracted into independent modules
- Improve separation of concerns and reduce coupling between components
- Create opportunities for code reuse across the codebase and potential external projects
- Enhance maintainability by establishing clear module boundaries and interfaces
- Support the "Do One Thing Well" Unix philosophy principle
- Ensure that 100% of the existing functionality is maintained during extraction

## Instructions

Generate a detailed extraction plan (`EXTRACT_PLAN.md`) that includes:

1. **Module Candidates:** Identify specific functionality, components, or subsystems that are suitable for extraction into independent modules, with justification for each recommendation.

2. **Module Boundaries:** For each candidate, define clear boundaries, including:
   - Public interfaces and contracts
   - Dependencies (both internal and external)
   - Responsibility scope (what the module should and should not do)

3. **Implementation Strategy:** For each extraction, provide:
   - Files and code sections to be extracted
   - Required refactoring to separate concerns
   - Approach for maintaining existing functionality during extraction
   - Suggested testing strategy to verify correct extraction

4. **Prioritization:** Rank extraction candidates based on:
   - Potential for reuse
   - Current coupling and complexity reduction
   - Implementation difficulty
   - Impact on overall codebase maintainability

5. **Risks & Mitigation:** Identify potential challenges (e.g., circular dependencies, shared state, tight coupling) and suggest mitigation strategies.

6. **Architecture Impact:** Describe how the proposed extractions align with and enhance the overall architecture, particularly regarding modularity, testability, and maintainability.

## Output

Provide the detailed extraction plan in Markdown format, suitable for saving as `EXTRACT_PLAN.md`, addressing all sections listed in the instructions.