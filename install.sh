#!/bin/bash

# Codex installation script
# This script creates symlinks from the home directory to the configuration files in this directory

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
RESET='\033[0m'

# Codex directory (assumes script is run from the codex directory)
CODEX_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CONFIG_SUBDIR="$CODEX_DIR/dotfiles"

echo -e "${BLUE}Installing configuration files from $CODEX_DIR${RESET}"

# Create symlinks for core configuration files
echo -e "${YELLOW}Creating symlinks for core configuration files...${RESET}"
ln -sf "$CONFIG_SUBDIR/.zshrc" "$HOME/.zshrc" && echo -e "${GREEN}✓ .zshrc${RESET}" || echo -e "${RED}✗ .zshrc${RESET}"
ln -sf "$CONFIG_SUBDIR/.aliases" "$HOME/.aliases" && echo -e "${GREEN}✓ .aliases${RESET}" || echo -e "${RED}✗ .aliases${RESET}"
ln -sf "$CONFIG_SUBDIR/.env" "$HOME/.env" && echo -e "${GREEN}✓ .env${RESET}" || echo -e "${RED}✗ .env${RESET}"

# Create backup of existing configurations if they exist
backup_if_exists() {
  if [ -e "$1" ] && [ ! -L "$1" ]; then
    local backup="$1.bak.$(date +%Y%m%d%H%M%S)"
    echo -e "${YELLOW}Backing up $1 to $backup${RESET}"
    mv "$1" "$backup"
  fi
}

# Setup Claude Code custom slash commands directory
echo -e "${YELLOW}Setting up Claude Code custom slash commands...${RESET}"
# Backup existing claude commands if it's not a symlink
if [ -d "$HOME/.claude/commands" ] && [ ! -L "$HOME/.claude/commands" ]; then
  backup_dir="$HOME/.claude/commands.bak.$(date +%Y%m%d%H%M%S)"
  echo -e "${YELLOW}Backing up $HOME/.claude/commands to $backup_dir${RESET}"
  mv "$HOME/.claude/commands" "$backup_dir"
fi

# Ensure parent directory exists
mkdir -p "$HOME/.claude"
# Create symlink to the entire directory
if [ -L "$HOME/.claude/commands" ]; then
  # Remove existing symlink first to prevent recursive symlinks
  rm "$HOME/.claude/commands"
fi
ln -sf "$CODEX_DIR/claude-commands" "$HOME/.claude/commands" && echo -e "${GREEN}✓ Claude commands directory${RESET}" || echo -e "${RED}✗ Claude commands directory${RESET}"

# Setup Thinktank configuration
echo -e "${YELLOW}Setting up Thinktank configuration...${RESET}"
# Ensure thinktank config directory exists
mkdir -p "$HOME/.config/thinktank"
# Create symlink for models.yaml
if [ -e "$HOME/.config/thinktank/models.yaml" ] && [ ! -L "$HOME/.config/thinktank/models.yaml" ]; then
  backup_file="$HOME/.config/thinktank/models.yaml.bak.$(date +%Y%m%d%H%M%S)"
  echo -e "${YELLOW}Backing up $HOME/.config/thinktank/models.yaml to $backup_file${RESET}"
  mv "$HOME/.config/thinktank/models.yaml" "$backup_file"
elif [ -L "$HOME/.config/thinktank/models.yaml" ]; then
  # Remove existing symlink
  rm "$HOME/.config/thinktank/models.yaml"
fi
ln -sf "$CODEX_DIR/models.yaml" "$HOME/.config/thinktank/models.yaml" && echo -e "${GREEN}✓ Thinktank models.yaml${RESET}" || echo -e "${RED}✗ Thinktank models.yaml${RESET}"

# Setup Git hooks
echo -e "${YELLOW}Setting up Git hooks...${RESET}"
git config core.hooksPath .githooks
chmod +x .githooks/*
echo -e "${GREEN}✓ Git hooks${RESET}"

# Reload shell
echo -e "${GREEN}Installation complete!${RESET}"
echo -e "${YELLOW}To apply changes immediately, run:${RESET}"
echo -e "${BLUE}zsh -c \"source ~/.zshrc\"${RESET}"