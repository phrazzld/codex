# DOCUMENT

## GOAL
Audit, critique, evaluate, consolidate, expand, and improve the documentation in the current repository.

## PROCESS
1. Analyze the repository's markdown documentation files
2. Evaluate structure, completeness, clarity, consistency, and organization
3. Generate a comprehensive TODO list with specific improvement tasks

## 1. Prepare Context
- Gather all the markdown documentation files in the project
- Review `BACKLOG.md` to understand current documentation-related tasks
- Read `DEVELOPMENT_PHILOSOPHY.md` for documentation standards and expectations

## 2. Create Context File
- Create `DOCUMENT-CONTEXT.md` with project-specific documentation context:
  ```markdown
  # Documentation Context

  ## Project Structure
  [Brief description of project layout and documentation organization]

  ## Documentation Priorities
  [List specific areas where documentation improvements are most needed]

  ## Current Documentation Issues
  [Known documentation problems or gaps]
  ```

## 3. Execute Documentation Audit
- Run thinktank-wrapper with the document template and context file (with the maximum timeout in the bash tool used to invoke it):
  ```bash
  thinktank-wrapper --model-set all --template document --inject DOCUMENT-CONTEXT.md --include-philosophy --include-glance
  ```
- Review the generated output directory and copy synthesis file to create `DOCUMENTATION_IMPROVEMENT_PLAN.md`

## 4. Create Detailed TODO List
- Extract actionable tasks from the improvement plan
- Format as specific, detailed TODO items that can be implemented
- Include current issues, improvement recommendations, and priority levels

## 5. Present Results
- Summarize key findings and highest priority recommendations
- Provide the detailed TODO list for implementation