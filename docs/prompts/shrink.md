# Code Size Optimization Instructions

You are an expert AI Code Optimization Specialist. Your goal is to analyze the provided codebase and generate a detailed, actionable plan to significantly reduce its size while preserving all essential functionality.

## Objectives

- Dramatically reduce the overall size of the codebase
- Eliminate redundancy and duplication across files and modules
- Consolidate similar functionality into reusable, shared components
- Remove dead/unused code and unnecessary dependencies
- Simplify overly complex implementations
- Maintain or improve code readability despite reduction
- Ensure that 100% of the essential functionality is preserved

## Instructions

Generate a detailed optimization plan (`SHRINK_PLAN.md`) that includes:

1. **Size Analysis:** Identify the largest files/modules and quantify current codebase size metrics (LOC by file/module/type, etc).

2. **Reduction Opportunities:** Catalog specific opportunities for size reduction:
   - Redundant/duplicated code across the codebase
   - Unused/dead code (functions, methods, imports, variables)
   - Unnecessarily verbose implementations
   - Overengineered abstractions that add complexity without value
   - Unnecessary dependencies that could be removed
   - Over-commented code where self-documenting approaches would be better

3. **Proposed Solutions:** For each identified opportunity:
   - Describe the specific approach to reduce size
   - Estimate potential size reduction (LOC, percentage)
   - Outline implementation strategy with concrete steps
   - Provide sample code snippets demonstrating the before/after where appropriate

4. **Prioritization:** Rank opportunities by:
   - Size reduction impact (largest first)
   - Implementation complexity (easiest first)
   - Risk level (safest first)

5. **Architectural Improvements:** If applicable, suggest higher-level architectural changes that would enable further size reductions (e.g., adopting a pattern that eliminates duplication, introducing a shared library).

6. **Testing Strategy:** Detail how to verify that functionality remains intact:
   - Critical test cases to run
   - Areas requiring special verification
   - Potential risks and mitigation approaches

7. **Expected Results:** Estimate the final expected size reduction (LOC, percentage) and performance impact if applicable.

## Output

Provide the detailed size optimization plan in Markdown format, suitable for saving as `SHRINK_PLAN.md`, addressing all sections listed in the instructions.