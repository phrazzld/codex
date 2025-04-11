# Dotfiles

This directory contains environment configuration files that adapt between different machines and provide a consistent development experience.

## Contents

- **[.zshrc](.zshrc)** - Main shell configuration file with environment detection
- **[.aliases](.aliases)** - Command aliases with environment-specific conditionals
- **[.env](.env)** - Environment variables for development setup

## Machine Configuration

These configuration files are structured with a focus on clear organization and practical utility.

## Installation

These dotfiles are automatically linked to your home directory by the main `install.sh` script at the repository root. The script creates symbolic links, ensuring that updates to the repository are immediately reflected in your environment.

## Customization

When adding new configuration or customizing existing files:

1. Follow the established formatting and organization within each file
2. Document non-obvious configurations with comments
3. Consider security implications when storing sensitive information
4. Keep configuration modular and well-organized

## Best Practices

- Use single responsibility principle for each configuration file
- Maintain consistent syntax and formatting
- Check for dependencies before configuring them
- Keep configuration settings well-organized and clearly marked