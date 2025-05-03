#!/bin/bash

# Codex installation script
# This script creates symlinks from the home directory to the configuration files in this directory
# and installs the Python-based thinktank-wrapper

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
ln -sf "$CONFIG_SUBDIR/.fun" "$HOME/.fun" && echo -e "${GREEN}✓ .fun${RESET}" || echo -e "${RED}✗ .fun${RESET}"

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

# Install Python-based thinktank-wrapper
echo -e "${YELLOW}Installing Python-based thinktank-wrapper...${RESET}"
WRAPPER_DIR="$CODEX_DIR/bin/thinktank_wrapper"
if [ -d "$WRAPPER_DIR" ]; then
  # Check if Python 3.8+ is available
  python_version=$(python3 --version 2>&1 | awk '{print $2}')
  if [[ "$(printf '%s\n' "3.8" "$python_version" | sort -V | head -n1)" == "3.8" ]]; then
    # Python 3.8 or higher is available
    echo -e "${BLUE}Python $python_version is available, installing thinktank-wrapper...${RESET}"
    # Install the package in development mode
    (cd "$WRAPPER_DIR" && pip install -e . && echo -e "${GREEN}✓ thinktank-wrapper Python package${RESET}") || echo -e "${RED}✗ thinktank-wrapper Python package installation failed${RESET}"
    
    # Create a Bash wrapper script for backward compatibility
    THINKTANK_WRAPPER_SCRIPT="$CODEX_DIR/bin/thinktank-wrapper"
    echo -e "${BLUE}Creating thinktank-wrapper script...${RESET}"
    cat > "$THINKTANK_WRAPPER_SCRIPT" << 'EOF'
#!/bin/bash
# This script is a compatibility wrapper for the Python-based thinktank-wrapper
# It ensures that $CODEX_DIR is set correctly before invoking the Python package

# Set CODEX_DIR to the parent directory of the bin directory
export CODEX_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"

# Execute the Python package with all arguments
python3 -m thinktank_wrapper "$@"
EOF
    chmod +x "$THINKTANK_WRAPPER_SCRIPT" && echo -e "${GREEN}✓ thinktank-wrapper script${RESET}" || echo -e "${RED}✗ thinktank-wrapper script creation failed${RESET}"
  else
    echo -e "${RED}Python 3.8 or higher is required, but version $python_version is installed.${RESET}"
    echo -e "${YELLOW}Please install Python 3.8 or higher and re-run this script.${RESET}"
  fi
else
  echo -e "${RED}thinktank_wrapper directory not found at $WRAPPER_DIR${RESET}"
fi

# Setup Git hooks
echo -e "${YELLOW}Setting up Git hooks...${RESET}"
git config core.hooksPath .githooks
chmod +x .githooks/*
echo -e "${GREEN}✓ Git hooks${RESET}"

# Set CODEX_DIR in shell configuration
echo -e "${YELLOW}Setting up CODEX_DIR environment variable...${RESET}"
if [ -f "$HOME/.zshrc" ]; then
  # Check if CODEX_DIR is already in .zshrc
  if ! grep -q "export CODEX_DIR=" "$HOME/.zshrc"; then
    echo -e "\n# Codex directory path for thinktank-wrapper" >> "$HOME/.zshrc"
    echo "export CODEX_DIR=\"$CODEX_DIR\"" >> "$HOME/.zshrc"
    echo -e "${GREEN}✓ Added CODEX_DIR to .zshrc${RESET}"
  else
    echo -e "${YELLOW}CODEX_DIR already defined in .zshrc${RESET}"
  fi
fi

if [ -f "$HOME/.bashrc" ]; then
  # Check if CODEX_DIR is already in .bashrc
  if ! grep -q "export CODEX_DIR=" "$HOME/.bashrc"; then
    echo -e "\n# Codex directory path for thinktank-wrapper" >> "$HOME/.bashrc"
    echo "export CODEX_DIR=\"$CODEX_DIR\"" >> "$HOME/.bashrc"
    echo -e "${GREEN}✓ Added CODEX_DIR to .bashrc${RESET}"
  else
    echo -e "${YELLOW}CODEX_DIR already defined in .bashrc${RESET}"
  fi
fi

# Reload shell
echo -e "${GREEN}Installation complete!${RESET}"
echo -e "${YELLOW}To apply changes immediately, run:${RESET}"
echo -e "${BLUE}zsh -c \"source ~/.zshrc\"${RESET}"