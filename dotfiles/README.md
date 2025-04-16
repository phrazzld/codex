# Dotfiles

This directory contains environment configuration files that provide a consistent development experience across environments.

## Contents

- **[.zshrc](.zshrc)** - Main shell configuration file with clean organization
- **[.aliases](.aliases)** - Command aliases for common operations
- **[.env](.env)** - Environment variables for development setup

## Configuration Philosophy

These configuration files follow the principles outlined in the Development Philosophy document:

- Simplicity First - Configurations are kept clear and straightforward
- Modularity - Each file has a distinct purpose
- Maintainability - Well-organized with clear sections and comments
- Explicit Design - Dependencies and requirements are clearly stated

## Installation

These dotfiles are automatically linked to your home directory by the main `install.sh` script at the repository root. The script creates symbolic links, ensuring that updates to the repository are immediately reflected in your environment.

```bash
cd ~/Development/codex
./install.sh
```

## Shell Configuration

The `.zshrc` file provides:

- Clean organization with logical sections
- Consistent error handling
- Efficient utility functions
- Environment-aware configuration

## Customization

When adding new configuration or customizing existing files:

1. Follow the established formatting and organization within each file
2. Document non-obvious configurations with comments
3. Consider security implications when storing sensitive information
4. Keep configuration modular and well-organized
5. Use POSIX-compatible syntax with `if [[ -n "$var" ]]; then` style conditionals

## Best Practices

- Use single responsibility principle for each configuration file
- Maintain consistent syntax and formatting
- Check for dependencies before configuring them
- Keep configuration settings well-organized and clearly marked
- Follow the 2-space indentation standard for YAML/JSON configuration