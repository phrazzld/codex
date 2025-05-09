#!/bin/bash
# Script to add CONTEXT sections to all template files - macOS compatible version

TEMPLATES_DIR="/Users/phaedrus/Development/codex/bin/thinktank-venv/lib/python3.13/site-packages/thinktank_wrapper/templates"
CONTEXT_BLOCK="<!-- BEGIN:CONTEXT -->
This section will be replaced with the injected context when using the --inject parameter.
If no context is injected, this default message will remain.
<!-- END:CONTEXT -->"

# Check if templates directory exists
if [ ! -d "$TEMPLATES_DIR" ]; then
  echo "Templates directory not found: $TEMPLATES_DIR"
  exit 1
fi

# Find all markdown files
for template_file in "$TEMPLATES_DIR"/*.md; do
  if [ -f "$template_file" ]; then
    template_name=$(basename "$template_file")
    
    # Skip files that already have the CONTEXT markers
    if grep -q "BEGIN:CONTEXT" "$template_file"; then
      echo "✓ $template_name already has CONTEXT section"
    else
      # Read the file content
      content=$(cat "$template_file")
      
      # Check if there's a second-level heading
      if grep -q "^##" "$template_file"; then
        # Get first paragraph before any ## heading
        intro=$(awk '/^##/{exit} {print}' "$template_file")
        
        # Get everything after the intro
        remainder=$(awk 'seen{print} /^##/{seen=1}' "$template_file")
        
        # Combine with CONTEXT block in the middle
        echo "$intro" > "$template_file"
        echo -e "\n$CONTEXT_BLOCK\n" >> "$template_file"
        echo "$remainder" >> "$template_file"
        
        echo "✅ Added CONTEXT section to $template_name"
      else
        # If no ## heading, just append to the end
        echo -e "\n$CONTEXT_BLOCK" >> "$template_file"
        echo "✅ Added CONTEXT section to end of $template_name"
      fi
    fi
  fi
done

echo "Done updating template files!"