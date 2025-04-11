# codex

A comprehensive configuration repository with adaptive configurations, AI prompt templates, and productivity tools that seamlessly work across multiple environments.

## Overview

This repository contains a unified configuration system that intelligently adapts between personal (serenity) and work (zoboomafoo) environments through hostname detection. It serves as a single source of truth for shell configuration, AI prompts, and development workflows.

## Features

- **Environment-Aware Configuration**
  - Unified `.zshrc` with dynamic environment detection
  - Conditional `.aliases` that load appropriate commands per environment
  - Shared `.env` file with common environment variables
  - Utility functions in `.fun` for daily development tasks

- **AI Tools & Templates**
  - Claude Code custom slash commands for structured development workflows

- **Best Practices**
  - Documented coding standards and shell scripting patterns
  - Conventional commit formatting and structured git workflows
  - Consistent style guides across configuration files

## Installation

Clone this repository to your development directory:

```bash
git clone https://github.com/phrazzld/codex.git ~/Development/codex
```

Install configuration files and commands:

```bash
cd ~/Development/codex
./install.sh
```

This creates symbolic links from your home directory to the configuration files and sets up Claude Code slash commands.

## Repository Structure

- **Root**: Documentation and installation script
- **`/dotfiles/`**: Configuration files (`.zshrc`, `.aliases`, `.env`, `.fun`)
- **`/claude-commands/`**: Structured workflow commands for Claude Code CLI
- **`/docs/`**: Documentation on best practices and testing philosophy
- **`/professional/`**: Professional documents like CV and resume

## Development Tools and Commands

### CLI Tools

- **`architect`** - Local CLI tool for generating technical plans and architectural guidance

### Claude Code Commands

The repository includes a suite of slash commands for Claude Code that enable structured software development workflows:

- `/audit` - Create security audit documentation for codebases
- `/breathe` - Promote reflection and mindfulness during development
- `/consult` - Document problems and request architectural assistance
- `/debug` - Structured approach to diagnosing and fixing bugs
- `/execute` - Implement tasks from TODO lists with best practices
- `/hit` - Quick access to specific functionality
- `/plan` - Create detailed technical plans for backlog items
- `/prime` - Gather context from key repository files
- `/push` - Quality assurance steps before committing code
- `/refactor` - Create structured plans for improving code quality
- `/resolve` - Troubleshoot and fix specific issues
- `/review` - Establish code review processes and documentation
- `/ticket` - Convert plans into prioritized task tickets

## Environment Detection

Configuration files adapt to different environments using hostname detection:

```bash
case "$(hostname)" in
  serenity) IS_SERENITY=1 ;;
  zoboomafoo) IS_ZOBOOMAFOO=1 ;;
esac
```

## License

MIT
