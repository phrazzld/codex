#!/bin/bash
# Script to add CONTEXT sections to all template files in the source directory

TEMPLATES_DIR="/Users/phaedrus/Development/codex/bin/thinktank_wrapper/src/thinktank_wrapper/templates"
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
      # Find the first line with ## or the first blank line after the introduction
      intro_line=$(awk 'NR>1 && /^$/ {print NR; exit}' "$template_file")
      
      # If no blank line found, look for the first heading
      if [ -z "$intro_line" ]; then
        intro_line=$(awk '/^##/ {print NR-1; exit}' "$template_file")
      fi
      
      # If still no intro line found, just use line 7 (after the typical intro)
      if [ -z "$intro_line" ]; then
        intro_line=7
      fi
      
      # Create a temporary file
      tmp_file=$(mktemp)
      
      # Copy the first part of the file
      head -n "$intro_line" "$template_file" > "$tmp_file"
      
      # Add a blank line and the CONTEXT block
      echo "" >> "$tmp_file"
      echo "$CONTEXT_BLOCK" >> "$tmp_file"
      echo "" >> "$tmp_file"
      
      # Copy the rest of the file
      tail -n +$((intro_line+1)) "$template_file" >> "$tmp_file"
      
      # Replace the original file
      mv "$tmp_file" "$template_file"
      
      echo "✅ Added CONTEXT section to $template_name"
    fi
  fi
done

echo "Done updating template files!"