#!/bin/bash
# Script to add CONTEXT sections to all template files

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
      # Insert the CONTEXT block after the introduction
      # We'll look for the first ## heading and insert before it
      if grep -q "^##" "$template_file"; then
        # Find the line number of the first ## heading
        line_num=$(grep -n "^##" "$template_file" | head -1 | cut -d: -f1)
        
        # Create a temporary file with the CONTEXT block inserted before that line
        sed "${line_num}i\\
$CONTEXT_BLOCK
" "$template_file" > "${template_file}.new"
        
        # Move the new file over the old one
        mv "${template_file}.new" "$template_file"
        echo "✅ Added CONTEXT section to $template_name"
      else
        # If no ## heading found, append to the end of the file
        echo -e "\n$CONTEXT_BLOCK" >> "$template_file"
        echo "✅ Added CONTEXT section to end of $template_name"
      fi
    fi
  fi
done

echo "Done updating template files!"