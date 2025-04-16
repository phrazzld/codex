# codex

A comprehensive configuration repository with adaptive configurations, AI prompt templates, and productivity tools that streamline software development workflows.

## Overview

This repository serves as a single source of truth for shell configurations, development standards, AI assistant prompts, and Claude Code slash commands. It establishes consistent practices across development activities.

## Features

- **Structured Configuration**
  - Organized `.zshrc` with clean organization and environment detection
  - Streamlined `.aliases` for common commands
  - Comprehensive `.env` file with environment variables

- **AI Tools & Templates**
  - Claude Code custom slash commands for structured development workflows
  - Comprehensive prompt templates for AI interactions
  - Standardized development processes codified in commands

- **Development Standards**
  - Detailed development philosophy with architecture guidelines
  - Documented coding standards and shell scripting patterns
  - Conventional commit formatting and structured git workflows
  - Comprehensive testing, logging, and security guidelines

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
- **`/dotfiles/`**: Configuration files (`.zshrc`, `.aliases`, `.env`)
- **`/claude-commands/`**: Structured workflow commands for Claude Code CLI
- **`/docs/`**: Documentation on development philosophy, best practices, and prompt templates
  - **`/docs/prompts/`**: Templates that power Claude Code commands
  - **`/docs/professional/`**: Professional document templates (CV, resume)
- **`BACKLOG.md`**: Planned enhancements and features

## Claude Code Commands

The repository includes a suite of slash commands for Claude Code that enable structured software development workflows:

- `/audit` - Create security audit documentation for codebases
- `/breathe` - Promote reflection and mindfulness during development
- `/chill` - Reduce development stress and maintain perspective
- `/consult` - Document problems and request architectural assistance
- `/debug` - Structured approach to diagnosing and fixing bugs
- `/execute` - Implement tasks from TODO lists with best practices
- `/ideate` - Generate and explore creative solution alternatives
- `/plan` - Create detailed technical plans for backlog items
- `/prime` - Gather context from key repository files
- `/push` - Quality assurance steps before committing code
- `/refactor` - Create structured plans for improving code quality
- `/resolve` - Troubleshoot and fix specific issues
- `/review` - Establish code review processes and documentation
- `/ticket` - Convert plans into prioritized task tickets

## Development Philosophy

The repository includes a comprehensive development philosophy document that establishes standards for:

- Core development principles
- Architecture guidelines
- Coding standards
- Testing strategy
- Logging strategy
- Security considerations
- Documentation approach

## License

MIT
