# Backlog Grooming: Comprehensive Organization & Expansion


<!-- BEGIN:CONTEXT -->
This section will be replaced with the injected context when using the --inject parameter.
If no context is injected, this default message will remain.
<!-- END:CONTEXT -->

You are a strategic product thinktank tasked with transforming a basic backlog into a comprehensive, well-organized roadmap that balances immediate needs with long-term vision. Your assignment is to analyze the current backlog and codebase architecture (from glance.md files) to produce a thoughtfully structured, prioritized, and expanded BACKLOG.md.

Keep the program's purpose in mind throughout this process. Strive for the highest quality maintainable solutions while avoiding overengineering. Balance technical excellence with practical delivery, ensuring the backlog focuses on real value without unnecessary complexity.

## 1. Analyze Current Backlog

Review the existing BACKLOG.md to understand:
- Current priorities and focus areas
- Technical debt items
- Feature development plans
- Missing dimensions that should be addressed

## 2. Study Codebase Architecture

Examine all provided glance.md files to:
- Understand the system's purpose, components, and architecture
- Identify architectural strengths to leverage and weaknesses to address
- Discover potential areas for enhancement not captured in current backlog
- Understand technical constraints and dependencies

Examine all provided development philosophy files to understand the ideal structure and architecture of the system.

## 3. Craft a Multi-Dimensional Backlog

Create a comprehensive backlog that considers ALL of these perspectives:

**Business & Value Delivery:**
- Features that drive user adoption or satisfaction
- Capabilities that create competitive advantage
- Work that directly impacts revenue or cost savings
- Market-responsive improvements

**Technical Excellence:**
- Code quality improvements
- Architecture evolution
- Performance optimizations
- Security hardening
- Technical debt reduction
- Developer experience enhancements

**Innovation & Exploration:**
- Research spikes for emerging technologies
- Proof-of-concept experiments
- Creative feature ideas
- Novel approaches to existing problems

**Operational Excellence:**
- Monitoring and observability improvements
- Deployment and reliability enhancements
- Error handling and resilience
- Scalability improvements

## 4. Apply Meaningful Organization

Structure the backlog with:

1. **Clear Priority Tiers:**
   - High: Critical for immediate development cycles
   - Medium: Important but can follow high-priority items
   - Low: Valuable but can wait for future consideration

2. **Logical Grouping:**
   - Group related items by domain, subsystem, or theme
   - Create categories that make the backlog navigable

3. **Item Metadata:**
   - Type: Feature, Enhancement, Refactor, Research, Fix
   - Complexity: Simple, Medium, Complex
   - Expected Outcome: Clear success criteria or benefit
   - Dependencies: Relationships between items (when applicable)

## 5. Format Requirements

Present the backlog in Markdown with consistent formatting:

```markdown
# BACKLOG

## High Priority

### [Category/Group Name]

- **[Feature/Enhancement/Fix/Research]**: Clear, actionable item description
  - **Complexity**: Simple/Medium/Complex
  - **Rationale**: Why this item matters (business value, technical need, etc.)
  - **Expected Outcome**: Specific success criteria or benefit
  - **Dependencies**: Related items (if applicable)

### [Another Category]
...

## Medium Priority
...

## Low Priority
...

## Future Considerations
...
```

## 6. Synthesis Guidelines

- **Retain valuable ideas** from the original backlog
- **Expand scope** where the codebase analysis reveals new opportunities
- **Add specificity** to vague items
- **Split** overly broad items into focused, actionable tasks
- **Combine** closely related or redundant items
- **Balance** immediate technical needs with long-term strategic vision
- **Prioritize ruthlessly** based on impact vs. effort
- **Consider interdependencies** between items when sequencing

## Output Requirements

- Provide ONLY the complete, formatted BACKLOG.md content—no other commentary
- Ensure every item has clear rationale tied to business value, technical excellence, or strategic advancement
- Maintain a healthy balance across all dimensions (business value, technical excellence, innovation, operations)
- Items must be specific enough to be actionable but not prescriptive about implementation details
