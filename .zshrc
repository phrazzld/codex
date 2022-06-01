autoload -U promptinit; promptinit
prompt pure

export NVM_LAZY_LOAD=true

plugins=(
  zsh-nvm
  git
  node
  fzf
  autojump
  zsh-autosuggestions
  zsh-syntax-highlighting
)

# Env first, cuz it loads OMZ
source $HOME/.env
source $HOME/.aliases
source $HOME/.fun
source $HOME/.cerego

# History
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

# thefuck
eval $(thefuck --alias)

# Autojump
[[ -s /root/.autojump/etc/profile.d/autojump.sh ]] && source /root/.autojump/etc/profile.d/autojump.sh
autoload -U compinit && compinit -u

# fzf
# use ripgrep
if type rg &> /dev/null; then
    export FZF_DEFAULT_COMMAND='rg --files --hidden'
fi
[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh
