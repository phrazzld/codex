# PLAN SCOPE ANALYSIS

## Purpose
Analyze implementation plans to ensure they have appropriate scope for manageable pull requests, clean todo lists, and focused development efforts.

## Context Requirements
- `PLAN.md`: The implementation plan to analyze
- Development philosophy files: For alignment with best practices 
- Codebase: To understand implementation context

## Process
1. **Analyze Plan Contents**
   - Identify the main feature or change being implemented
   - Enumerate steps, tasks, changes required
   - Identify components/modules affected
   - Estimate testing complexity
   - Evaluate review burden and deployment risk

2. **Determine Appropriate Scope**
   - A plan has appropriate scope when:
     - It represents a cohesive, focused unit of work
     - Changes are tightly related and highly cohesive
     - Testing can be thorough and focused
     - Code review can be meaningful and thorough
     - Deployment risk is manageable
     - Implementation can be completed in a reasonable timeframe

3. **Identify Splitting Boundaries (If Needed)**
   - If the plan exceeds appropriate scope:
     - Find logical boundaries between major components
     - Identify changes that can be implemented and tested independently
     - Ensure each sub-plan can be deployed without dependencies when possible
     - Preserve logical flow of implementation across sub-plans

4. **Define Clear Sub-Plans**
   - If splitting is needed:
     - Create distinct outlines for each independent plan
     - Ensure each has a clear purpose and success criteria
     - Maintain logical sequence (if applicable) 
     - Add cross-references for any dependencies between plans

## Output Format
If the plan scope is appropriate:
```markdown
# SCOPE ASSESSMENT

## Summary
The current plan has appropriate scope and granularity. It represents a cohesive unit of work that can be implemented, tested, reviewed, and deployed effectively.

## Reasoning
- [Specific factors justifying the assessment]
- [Discussion of size, cohesion, testing, and review considerations]

## Recommendation
Proceed with the current plan. No splitting is necessary.
```

If the plan should be split:
```markdown
# SCOPE ASSESSMENT

## Summary
The current plan exceeds optimal scope and should be divided into [N] separate implementation plans to improve manageability, testing, review, and deployment.

## Reasoning
- [Specific factors justifying the assessment]
- [Discussion of size, cohesion, testing, and review considerations]

## Recommended Split Points
- **Plan 1**: [Brief description]
  - Components: [List]
  - Key functionality: [Description]
  
- **Plan 2**: [Brief description]
  - Components: [List]
  - Key functionality: [Description]
  
[Additional plans as needed]

## Implementation Sequence
[Recommended order of implementation if applicable]

## Cross-Plan Dependencies
[Any critical dependencies between the plans]
```

## Sub-Plan Format (When Splitting Required)
Each sub-plan should follow this structure:

```markdown
# IMPLEMENTATION PLAN: [SPECIFIC FOCUS]

## Overview
[Brief description of this specific sub-plan's purpose]

## Context
[Relevant project context]

## Approach
[Implementation approach specific to this sub-plan]

## Implementation Steps
1. [Detailed step]
2. [Detailed step]
...

## Dependency Notes
[Any dependencies on other sub-plans, if applicable]
```

## Priority Considerations
- **Balance**: Strike the right balance between too granular (inefficient) and too broad (unwieldy)
- **Independence**: Prioritize clean boundaries between sub-plans
- **Testability**: Each plan should result in a testable increment
- **Review Clarity**: Keep reviews focused and manageable
- **Deployment Safety**: Consider safe, incremental deployment
- **Developer Experience**: Plans should feel like natural units of work