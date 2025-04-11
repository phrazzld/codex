# Dotfiles

This directory contains environment configuration files that adapt between different machines and provide a consistent development experience.

## Contents

- **[.zshrc](.zshrc)** - Main shell configuration file with environment detection
- **[.aliases](.aliases)** - Command aliases with environment-specific conditionals
- **[.env](.env)** - Environment variables for development setup
- **[.fun](.fun)** - Utility functions for daily development tasks

## Environment Awareness

These configuration files use hostname detection to adapt between different environments:

```bash
case "$(hostname)" in
  serenity) IS_SERENITY=1 ;;
  zoboomafoo) IS_ZOBOOMAFOO=1 ;;
esac
```

This approach allows for a unified configuration system that intelligently adapts between personal (serenity) and work (zoboomafoo) environments.

## Installation

These dotfiles are automatically linked to your home directory by the main `install.sh` script at the repository root. The script creates symbolic links, ensuring that updates to the repository are immediately reflected in your environment.

## Customization

When adding new configuration or customizing existing files:

1. Use the environment detection pattern for settings that should differ between environments
2. Follow the established formatting and organization within each file
3. Document non-obvious configurations with comments
4. Consider security implications when storing sensitive information

## Best Practices

- Use single responsibility principle for each configuration file
- Maintain consistent syntax and formatting
- Check for dependencies before configuring them
- Keep environment-specific settings well-organized and clearly marked