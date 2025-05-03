# Core plugin definitions
plugins=(
  asdf
  zsh-autosuggestions
  zsh-syntax-highlighting
)

# Add Homebrew's zsh site-functions to fpath (for Apple Silicon)
if [[ -d /opt/homebrew/share/zsh/site-functions ]]; then
  fpath=(/opt/homebrew/share/zsh/site-functions $fpath)
fi

# Source environment, functions, and aliases
source $HOME/.env
[ -f $HOME/.fun ] && source $HOME/.fun
source $HOME/.aliases

# Load machine-specific configuration
source $HOME/.secrets

# History settings
HISTFILE=~/.zsh_history
HISTSIZE=1024
SAVEHIST=1024
setopt append_history
setopt hist_ignore_all_dups
unsetopt hist_ignore_space
setopt hist_reduce_blanks
setopt hist_verify
setopt inc_append_history
setopt share_history
setopt bang_hist

# thefuck alias if available
if command -v thefuck >/dev/null 2>&1; then
  fuck() {
    eval "$(thefuck --alias)" && fuck
  }
fi

# Zoxide (directory jumper)
if command -v zoxide &> /dev/null; then
  eval "$(zoxide init zsh)"
fi

# ASDF version manager
if [ -f "$HOME/.asdf/asdf.sh" ]; then
  source "$HOME/.asdf/asdf.sh"
fi

# Docker Desktop if available
[ -f $HOME/.docker/init-zsh.sh ] && source $HOME/.docker/init-zsh.sh || true

# FZF integration
# Use ripgrep if available
if type rg &> /dev/null; then
  export FZF_DEFAULT_COMMAND='rg --files --hidden'
fi
[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh

# Add yarn bin to PATH if needed
export PATH="$HOME/.yarn/bin:$HOME/.config/yarn/global/node_modules/.bin:$PATH"

# Google Cloud SDK (if available)
if [ -f "$HOME/google-cloud-sdk/path.zsh.inc" ]; then
  source "$HOME/google-cloud-sdk/path.zsh.inc"
fi

# Google Cloud SDK completions (if available)
if [ -f "$HOME/google-cloud-sdk/completion.zsh.inc" ]; then
  source "$HOME/google-cloud-sdk/completion.zsh.inc"
fi

# Electron-forge tab completion
[[ -f $HOME/.asdf/installs/nodejs/17.9.1/lib/node_modules/electron-forge/node_modules/tabtab/.completions/electron-forge.zsh ]] && . $HOME/.asdf/installs/nodejs/17.9.1/lib/node_modules/electron-forge/node_modules/tabtab/.completions/electron-forge.zsh

# Initialize starship prompt
if command -v starship &> /dev/null; then
  eval "$(starship init zsh)"
fi
. "/Users/phaedrus/.deno/env"
# pnpm
export PNPM_HOME="/Users/phaedrus/Library/pnpm"
case ":$PATH:" in
  *":$PNPM_HOME:"*) ;;
  *) export PATH="$PNPM_HOME:$PATH" ;;
esac
# pnpm end

# Codex directory path for thinktank-wrapper
export CODEX_DIR="/Users/phaedrus/Development/codex"
