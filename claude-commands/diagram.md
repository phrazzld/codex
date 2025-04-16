# DIAGRAM

## GOAL
Generate a Mermaid diagram of the codebase structure or workflow using the Architect CLI.

## PROCESS
1. Run architect with the diagram prompt:
   ```bash
   # Run architect to generate the diagram using the prompt file
   architect --instructions docs/prompts/diagram.md --output-dir architect_output --model gemini-2.5-pro-exp-03-25 --model gemini-2.0-flash --model gemini-2.5-pro-preview-03-25 ./

   # Display results
   cat architect_output/*.md
   ```
