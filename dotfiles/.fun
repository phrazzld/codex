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

# Alacritty Font Switching Functions
switch_font() {
  local font_name="${1:-help}"
  local config_file="$HOME/Development/codex/dotfiles/.alacritty.toml"
  local temp_file=$(mktemp)
  
  case "$font_name" in
    "firacode"|"fira")
      local font_import="/Users/phaedrus/Development/codex/dotfiles/.alacritty-font-firacode.toml"
      ;;
    "jetbrains"|"jb")
      local font_import="/Users/phaedrus/Development/codex/dotfiles/.alacritty-font-jetbrains.toml"
      ;;
    "sourcecodepro"|"scp")
      local font_import="/Users/phaedrus/Development/codex/dotfiles/.alacritty-font-source-code-pro.toml"
      ;;
    "cascadia"|"cc")
      local font_import="/Users/phaedrus/Development/codex/dotfiles/.alacritty-font-cascadia.toml"
      ;;
    "victormono"|"vm")
      local font_import="/Users/phaedrus/Development/codex/dotfiles/.alacritty-font-victor-mono.toml"
      ;;
    "hack"|"hk")
      local font_import="/Users/phaedrus/Development/codex/dotfiles/.alacritty-font-hack.toml"
      ;;
    "help"|*)
      echo "Usage: switch_font [font_name]"
      echo "Available fonts (all with Nerd Font icons):"
      echo "  firacode, fira      - FiraCode Nerd Font Mono"
      echo "  jetbrains, jb       - JetBrainsMono Nerd Font"
      echo "  sourcecodepro, scp  - SauceCodePro Nerd Font"
      echo "  cascadia, cc        - Cascadia Code NF (Microsoft)"
      echo "  victormono, vm      - VictorMono Nerd Font (cursive italics)"
      echo "  hack, hk            - Hack Nerd Font (eye-strain optimized)"
      echo ""
      echo "Current font: $(get_current_font)"
      return 0
      ;;
  esac
  
  # Update the import line in the config file
  sed "s|/Users/phaedrus/Development/codex/dotfiles/\.alacritty-font-.*\.toml|$font_import|g" "$config_file" > "$temp_file"
  mv "$temp_file" "$config_file"
  
  echo "Switched to $font_name font. Restart Alacritty to see changes."
}

# Get current font from config
get_current_font() {
  local config_file="$HOME/Development/codex/dotfiles/.alacritty.toml"
  local font_line=$(grep "\.alacritty-font-.*\.toml" "$config_file")
  
  if [[ $font_line == *"firacode"* ]]; then
    echo "FiraCode Nerd Font Mono"
  elif [[ $font_line == *"jetbrains"* ]]; then
    echo "JetBrainsMono Nerd Font"
  elif [[ $font_line == *"source-code-pro"* ]]; then
    echo "SauceCodePro Nerd Font"
  elif [[ $font_line == *"cascadia"* ]]; then
    echo "Cascadia Code NF"
  elif [[ $font_line == *"victor-mono"* ]]; then
    echo "VictorMono Nerd Font"
  elif [[ $font_line == *"hack"* ]]; then
    echo "Hack Nerd Font"
  else
    echo "Unknown"
  fi
}

# Aliases for convenience
alias font='switch_font'
alias fonthelp='switch_font help'