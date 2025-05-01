#!/bin/bash
# .fun - Collection of useful shell functions

# Find glance.md files in current directory and subdirectories up to specified depth
find_glance_files() {
  # Get current directory's absolute path
  local current_dir="$(pwd)"
  local max_depth="${1:-2}"  # Default to 2 levels deep if not specified
  
  # Use find to locate all glance.md files efficiently
  # +1 to max_depth because maxdepth counts from 0 (current directory)
  find "$current_dir" -maxdepth $((max_depth + 1)) -type f -name "glance.md" | sort
}

# Find all development philosophy files in the current directory or any subdirectory
find_philosophy_files() {
  # Get current directory's absolute path
  local current_dir="$(pwd)"
  
  # Use find with -L option to follow symbolic links
  find -L "$current_dir" -type f -name "DEVELOPMENT_PHILOSOPHY*.md" | sort
}

# Usage examples:
# glance_files=$(find_glance_files)
# philosophy_files=$(find_philosophy_files)
# thinktank $THINKTANK_HIGH_CONTEXT_MODELS $THINKTANK_SYNTHESIS_MODEL $glance_files $philosophy_files