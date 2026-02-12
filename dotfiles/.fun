#!/bin/bash
# ===================================================================
# SHELL UTILITY FUNCTIONS
# Collection of useful functions for development and system management
# ===================================================================

# --- PROJECT DISCOVERY ---
# Find development philosophy files in current directory tree
find_philosophy_files() {
  find -L "$(pwd)" -type f -name "DEVELOPMENT_PHILOSOPHY*.md" | sort
}


# Font switching for Alacritty
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
  
  # Update the font import line in the config file (preserve theme imports)
  sed "s|/Users/phaedrus/Development/codex/dotfiles/\.alacritty-font-.*\.toml|$font_import|g" "$config_file" > "$temp_file"
  mv "$temp_file" "$config_file"
  
  # Touch the config file to trigger live reload
  touch "$config_file"
  
  echo "Switched to $font_name font (live reload)."
}

# Get current font
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

# --- GIT WORKTREE MANAGEMENT ---
# Create git worktree with new branch in ../<repo>__<branch>
gwtn() {
  local branch_name="$1"
  local base_branch="${2:-$(git rev-parse --abbrev-ref HEAD 2>/dev/null)}"
  
  # Check if branch name is provided
  if [[ -z "$branch_name" ]]; then
    echo "Usage: gwtn <branch_name> [base_branch]"
    echo "Creates a new git worktree with a new branch in ../<repo>__<branch_name>"
    echo ""
    echo "Examples:"
    echo "  gwtn feature/auth       # Creates worktree from current branch"
    echo "  gwtn hotfix main        # Creates worktree from main branch"
    return 1
  fi
  
  # Check if we're in a git repository
  if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Error: Not in a git repository"
    return 1
  fi
  
  # Get repository name
  local repo_name=$(basename $(git rev-parse --show-toplevel))
  if [[ $? -ne 0 ]]; then
    echo "❌ Error: Could not determine repository name"
    return 1
  fi
  
  # Set up paths - replace / with - for filesystem compatibility
  local clean_branch_name=$(echo "$branch_name" | sed 's/\//-/g')
  local worktree_dir="../${repo_name}__${clean_branch_name}"
  
  # Check if directory already exists
  if [[ -d "$worktree_dir" ]]; then
    echo "❌ Error: Directory $worktree_dir already exists"
    return 1
  fi
  
  # Verify base branch exists
  if ! git rev-parse --verify "$base_branch" > /dev/null 2>&1; then
    echo "❌ Error: Base branch '$base_branch' does not exist"
    return 1
  fi
  
  # Create the worktree with new branch
  echo "🌳 Creating git worktree..."
  echo "📁 Directory: $worktree_dir"
  echo "🌿 New branch: $branch_name"
  echo "🔗 Base branch: $base_branch"
  echo ""
  
  if git worktree add -b "$branch_name" "$worktree_dir" "$base_branch"; then
    echo "✅ Worktree created successfully!"
    echo ""
    echo "To switch to your new worktree:"
    echo "  cd $worktree_dir"
    echo ""
    echo "To view all worktrees:"
    echo "  gwte"
  else
    echo "❌ Failed to create worktree"
    return 1
  fi
}

# Convenience aliases
alias font='switch_font'
alias fonthelp='switch_font help'

# --- JOURNAL MANAGEMENT ---
# Quick access to daily journal entries in Obsidian vault (daybook)

# Primary journal command - creates entry with frontmatter and timestamp
p() {
  local vault=~/Documents/daybook
  local file=$vault/journal/$(date +%Y/%m/%d).md
  mkdir -p "$(dirname "$file")"

  # Create with frontmatter if new file
  if [[ ! -f "$file" ]]; then
    cat > "$file" << EOF
---
type: journal
created: $(date -Iseconds)
tags: [journal]
---

# $(date "+%B %d, %Y: %A")

EOF
  fi

  # Append timestamp section
  echo -e "\n## $(date +%H:%M:%S)\n" >> "$file"

  # Open in nvim at end of file
  nvim "+normal G" "$file"
}

# Open journal for specific date: jd 2024-01-15
jd() {
  local d="${1:-$(date +%Y-%m-%d)}"
  local file=~/Documents/daybook/journal/${d:0:4}/${d:5:2}/${d:8:2}.md
  mkdir -p "$(dirname "$file")"
  nvim "$file"
}

# Open yesterday's journal
jy() {
  local d=$(date -v-1d +%Y-%m-%d)
  jd "$d"
}

# List recent journal entries
jl() {
  local count="${1:-10}"
  find ~/Documents/daybook/journal -name "*.md" -type f | sort -r | head -n "$count"
}

# --- RALPH LOOP ---
# Autonomous issue-to-merged-PR loop
# Named after Ralph Wiggum: clueless yet relentlessly persistent

ralph() {
  if [ -z "$1" ]; then
    echo "Usage: ralph <issue-number>"
    echo ""
    echo "Runs full autopilot flow (spec → arch → build → refactor → docs → PR)"
    echo "Then monitors for CI failures and review feedback until merged."
    echo ""
    echo "Environment variables:"
    echo "  RALPH_MAX_ITERATIONS  - Max loop iterations (default: 100)"
    echo "  RALPH_CIRCUIT_BREAKER - No-progress loops before stopping (default: 5)"
    return 1
  fi
  ~/bin/ralph "$@"
}