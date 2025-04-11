# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands
- `zsh -c "source ~/.zshrc"` - Reload shell configuration
- `./install.sh` - Install configuration files by creating symlinks
- `shellcheck filename.sh` - Validate shell scripts

## Code Style Guidelines
- **Shell**: POSIX-compatible syntax with `if [[ -n "$var" ]]; then` style conditionals
- **Error Handling**: Check file existence (`-f`), command availability, and use descriptive error messages
- **Functions**: Document with inline comments and use descriptive names
- **Formatting**: 2-space indentation for YAML/JSON; consistent structure in config files
- **Git**: Use conventional commits (`feat:`, `fix:`, `docs:`, `style:`, `refactor:`)
- **Types**: Prefer strong typing when applicable (TypeScript strict mode)

## Repository Structure
- Root: Documentation and installation script
- `/dotfiles/`: Configuration files (.zshrc, .aliases, .env)
- `/claude-commands/`: Custom Claude Code slash commands
- `/docs/`: Documentation on best practices and testing philosophy
- `/professional/`: Professional documents like CV and resume

## Machine Configuration
Configuration files are structured for a single machine environment.

## Best Practices
- Use single responsibility principle for scripts
- Implement consistent error handling
- Check dependencies before command execution
- Maintain well-organized configurations
- Follow TDD when writing new scripts
- Prioritize simplicity and readability over clever implementations