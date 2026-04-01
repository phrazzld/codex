# Dotfiles

Shell configuration files for consistent development environment.

## Files

- `.zshrc` - Main shell configuration
- `.aliases` - Command shortcuts  
- `.env` - Environment variables
- `.fun` - Shell utility functions

## Installation

Automatically symlinked by `install.sh`:
```bash
cd ~/Development/codex && ./install.sh
```

## Configuration

- Modular organization with clear sections
- Environment-aware setup
- POSIX-compatible syntax
- Security-conscious (no secrets in configs)

## Remote Workflow

- `ph` - SSH to `phyrexia` with GitHub identity envs wired
- `ph "<command>"` - Run a single remote command with same identity wiring
- `phf` - Jump directly into remote `factory` tmux session (`attach` default)
- `phf up|status|kill|shell` - Manage factory session lifecycle on `phyrexia`
- `pht` - Short alias for `phf`
