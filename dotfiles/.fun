#!/bin/bash
# .fun - Collection of useful shell functions

# Find glance.md files in current directory and immediate subdirectories only
find_glance_files() {
  # Get current directory's absolute path
  local current_dir="$(pwd)"
  
  # Check if glance.md exists in current directory
  if [ -f "$current_dir/glance.md" ]; then
    echo "$current_dir/glance.md"
  fi
  
  # Check immediate subdirectories only
  for dir in "$current_dir"/*/; do
    # Skip if not a directory
    if [ ! -d "$dir" ]; then
      continue
    fi
    
    if [ -f "$dir/glance.md" ]; then
      echo "$dir/glance.md"
    fi
  done
}

# Find all development philosophy files in the current directory or any subdirectory
find_philosophy_files() {
  # Get current directory's absolute path
  local current_dir="$(pwd)"
  
  # Use find to locate all development philosophy files
  find "$current_dir" -type f -name "DEVELOPMENT_PHILOSOPHY*.md" | sort
}

# Usage examples:
# glance_files=$(find_glance_files)
# philosophy_files=$(find_philosophy_files)
# thinktank $THINKTANK_HIGH_CONTEXT_MODELS $THINKTANK_SYNTHESIS_MODEL $glance_files $philosophy_files