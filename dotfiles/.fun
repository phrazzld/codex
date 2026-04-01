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

# --- ORCHESTRATOR ---
# Autonomous issue-to-merge loop with sensible defaults
orchestrate() {
  ~/.claude/scripts/orchestrator.sh "${PWD}" \
    --max-issues 5 \
    --max-build-iter 15 \
    --max-prfix-iter 10 \
    --ci-sleep 300 \
    "$@"
}

# flywheel — Go autopilot (successor to orchestrate)
# Usage: flywheel [flags]          — run in current dir
#        flywheel -t [flags]       — run in a new tmux session named 'flywheel'
#        flywheel -t NAME [flags]  — run in tmux session NAME
flywheel() {
  local tmux_session=""
  local dir="${PWD}"

  # Parse -t [session-name]
  if [[ "$1" == "-t" ]]; then
    shift
    if [[ -n "$1" && "$1" != --* ]]; then
      tmux_session="$1"
      shift
    else
      tmux_session="flywheel"
    fi
  fi

  if [[ -n "$tmux_session" ]]; then
    tmux new-session -d -s "$tmux_session" \
      "flywheel run ${(q)dir} --max-issues 5 --max-build-iter 20 --max-prfix-iter 15 --ci-sleep 300 $*; exec zsh"
    echo "flywheel running in tmux session '${tmux_session}'"
    echo "  attach: tmux attach -t ${tmux_session}"
  else
    command flywheel run "$dir" \
      --max-issues 5 \
      --max-build-iter 20 \
      --max-prfix-iter 15 \
      --ci-sleep 300 \
      "$@"
  fi
}

# --- REMOTE SSH WITH IDENTITY FORWARDING ---
# SSH to Phyrexia with full GitHub identity (phrazzld)
# Agent forwarding handles git SSH ops; env vars handle gh CLI + commit author
_ph_identity_ssh() {
  local remote_cmd="${1:-exec zsh -l}"
  local gh_token
  local quoted_remote_cmd

  gh_token=$(gh auth token 2>/dev/null) || { echo "gh auth failed"; return 1; }
  quoted_remote_cmd=$(printf '%q' "$remote_cmd")
  ssh-add --apple-use-keychain ~/.ssh/github_phrazzld >/dev/null 2>&1 || true

  ssh -tt \
    -o ConnectTimeout=10 \
    -o ServerAliveInterval=30 \
    -o ServerAliveCountMax=3 \
    phyrexia "
    export GH_TOKEN='${gh_token}'
    export GIT_AUTHOR_NAME='phrazzld'
    export GIT_AUTHOR_EMAIL='phrazzld@pm.me'
    export GIT_COMMITTER_NAME='phrazzld'
    export GIT_COMMITTER_EMAIL='phrazzld@pm.me'
    export GIT_CONFIG_COUNT=1
    export GIT_CONFIG_KEY_0='url.git@github.com:.insteadOf'
    export GIT_CONFIG_VALUE_0='https://github.com/'
    exec zsh -lc ${quoted_remote_cmd}
  "
}

# --- CODEX NATIVE MULTI-AGENT REVIEW ---
# Uses subagent injection: parent sees all child results in context

cxreview() {
  local target="${1:-$(git diff --name-only HEAD~1 | head -20 | tr '\n' ' ')}"
  codex -q "
    You are a tech lead orchestrating a code review.

    Spawn these agents in parallel:
    1. grug agent: review for complexity demons in: $target
    2. carmack agent: review for shippability and YAGNI in: $target
    3. ousterhout agent: review for module depth and information hiding in: $target

    Wait for all results. Then synthesize:
    - Deduplicate findings across reviewers
    - Resolve conflicts (if reviewers disagree, explain your call)
    - Prioritize: critical (block merge) > important (fix in PR) > suggestion
    - Output: action plan with file:line references
  "
}

cxreview-full() {
  local target="${1:-$(git diff --name-only HEAD~1 | head -20 | tr '\n' ' ')}"
  codex -q "
    You are a tech lead orchestrating a comprehensive code review.

    Spawn ALL these agents in parallel:
    1. grug: complexity demons, premature abstraction
    2. carmack: shippability, YAGNI, focus
    3. ousterhout: module depth, information hiding
    4. torvalds: correctness, clarity, pragmatic efficiency
    5. beck: TDD discipline, test quality

    Wait for all results. Synthesize into:
    - Consensus findings (2+ reviewers agree)
    - Conflicts resolved (with reasoning)
    - Prioritized action plan: critical > important > suggestion
    - Positive observations (what was done well)
  "
}

ph() {
  if [[ $# -eq 0 ]]; then
    _ph_identity_ssh "exec zsh -l"
    return
  fi

  _ph_identity_ssh "$*"
}

# Peek at Phyrexia factory session (no identity injection).
# For authenticated work, use `ph` instead.
phf() {
  local action="${1:-attach}"

  case "$action" in
    attach|start|'')
      ssh-add --apple-use-keychain ~/.ssh/github_phrazzld 2>/dev/null || true
      ssh -tt \
        -o ConnectTimeout=10 \
        -o ServerAliveInterval=30 \
        -o ServerAliveCountMax=3 \
        phyrexia "
        if command -v factory-tmux >/dev/null 2>&1; then
          exec factory-tmux attach
        elif command -v tmux >/dev/null 2>&1; then
          exec tmux new-session -A -s factory
        fi
        echo 'tmux not found' >&2; exit 1
      "
      ;;
    status)
      ssh phyrexia "tmux list-sessions 2>/dev/null || echo 'No tmux sessions'"
      ;;
    kill)
      ssh phyrexia "tmux kill-session -t factory 2>/dev/null; echo 'killed factory session'"
      ;;
    help|-h|--help)
      cat <<'EOF'
Usage: phf [command]

Peek at Kaylee's factory session (no GitHub identity injected).
For authenticated work, use: ph

Commands:
  attach   Attach to factory session (default)
  status   Show tmux sessions on phyrexia
  kill     Kill factory session
  help     Show this help
EOF
      ;;
    *)
      echo "Unknown phf command: $action (try: phf help)"
      return 1
      ;;
  esac
}
