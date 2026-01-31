# ===================================================================
# ZSH CONFIGURATION
# Modern shell configuration with enhanced productivity features
# ===================================================================

# --- CORE PLUGINS ---
# Essential plugins for enhanced shell experience
plugins=(
  asdf                    # Version manager for multiple languages
  zsh-autosuggestions    # Fish-like autosuggestions
  zsh-syntax-highlighting # Syntax highlighting for commands
)

# --- HOMEBREW INTEGRATION ---
# Add Homebrew's zsh completions (Apple Silicon)
if [[ -d /opt/homebrew/share/zsh/site-functions ]]; then
  fpath=(/opt/homebrew/share/zsh/site-functions $fpath)
fi

# --- CONFIGURATION SOURCING ---
# Load configurations in order: env vars → functions → aliases → secrets
source $HOME/.env                    # Environment variables and PATH
[ -f $HOME/.fun ] && source $HOME/.fun  # Utility functions  
source $HOME/.aliases               # Command aliases and git helpers
source $HOME/.secrets               # Machine-specific secrets

# --- HISTORY CONFIGURATION ---
# Enhanced history settings for better command recall
HISTFILE=~/.zsh_history
HISTSIZE=1024                      # Commands in memory
SAVEHIST=1024                      # Commands saved to file
setopt append_history               # Append to history file
setopt hist_ignore_all_dups        # Remove older duplicate entries
unsetopt hist_ignore_space          # Don't ignore commands starting with space
setopt hist_reduce_blanks           # Remove extra blanks
setopt hist_verify                  # Show command before executing from history
setopt inc_append_history           # Add commands immediately
setopt share_history                # Share history between sessions
setopt bang_hist                    # Enable ! history expansion

# --- EXTERNAL TOOL INTEGRATIONS ---
# Initialize various development and productivity tools

# TheFuck - correct previous command typos
if command -v thefuck >/dev/null 2>&1; then
  fuck() {
    eval "$(thefuck --alias)" && fuck
  }
fi

# Zoxide - smart directory navigation (cd replacement)
if command -v zoxide &> /dev/null; then
  eval "$(zoxide init zsh)"
fi

# ASDF - universal version manager
if [ -f "$HOME/.asdf/asdf.sh" ]; then
  source "$HOME/.asdf/asdf.sh"
fi

# Docker Desktop integration
[ -f $HOME/.docker/init-zsh.sh ] && source $HOME/.docker/init-zsh.sh || true

# FZF - fuzzy finder with ripgrep integration
if type rg &> /dev/null; then
  export FZF_DEFAULT_COMMAND='rg --files --hidden'
fi
[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh

# --- ADDITIONAL PATH EXPORTS ---
# Supplementary PATH additions (main PATH config in .env)
export PATH="$HOME/bin:$PATH"

# --- CLOUD SDK INTEGRATIONS ---
# Google Cloud SDK
if [ -f "$HOME/google-cloud-sdk/path.zsh.inc" ]; then
  source "$HOME/google-cloud-sdk/path.zsh.inc"
fi
if [ -f "$HOME/google-cloud-sdk/completion.zsh.inc" ]; then
  source "$HOME/google-cloud-sdk/completion.zsh.inc"
fi

# --- PACKAGE MANAGER INTEGRATIONS ---
# PNPM integration
export PNPM_HOME="/Users/phaedrus/Library/pnpm"
case ":$PATH:" in
  *":$PNPM_HOME:"*) ;;
  *) export PATH="$PNPM_HOME:$PATH" ;;
esac

# Deno runtime environment
. "/Users/phaedrus/.deno/env"

# --- COMPLETIONS ---
# Electron-forge tab completion (version-specific)
[[ -f $HOME/.asdf/installs/nodejs/17.9.1/lib/node_modules/electron-forge/node_modules/tabtab/.completions/electron-forge.zsh ]] && . $HOME/.asdf/installs/nodejs/17.9.1/lib/node_modules/electron-forge/node_modules/tabtab/.completions/electron-forge.zsh

# --- PROMPT INITIALIZATION ---
# Starship - modern cross-shell prompt
if command -v starship &> /dev/null; then
  eval "$(starship init zsh)"
fi

# --- PROJECT-SPECIFIC EXPORTS ---
# Codex directory for thinktank integration
export CODEX_DIR="/Users/phaedrus/Development/codex"

# opencode
export PATH=/Users/phaedrus/.opencode/bin:$PATH


# Added by Antigravity
export PATH="/Users/phaedrus/.antigravity/antigravity/bin:$PATH"

# --- PATH HYGIENE ---
# Keep asdf shims first; keep npm-global later; de-dupe entries.
typeset -U path
path=(${path:#$HOME/.asdf/shims} ${path:#$HOME/.asdf/bin} ${path:#$HOME/.npm-global/bin})
path=($HOME/.asdf/shims $HOME/.asdf/bin $path)
if [[ -d $HOME/.npm-global/bin ]]; then
  path=($path $HOME/.npm-global/bin)
fi
typeset -U path
