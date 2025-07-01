# CLAUDE.md

Repository-specific operational guidance for Claude Code.

## Repository Purpose
Configuration repository with AI prompt templates, Claude Code slash commands, and productivity tools for software development workflows.

## Build Commands
* No build process - collection of templates and configuration files
* No testing or linting commands defined

## Repository-Specific Structure
* `/claude-commands/` - Custom Claude CLI slash commands (structured workflows)
* `/docs/` - Development philosophy, prompt templates, professional docs
* `/dotfiles/` - Shell configurations (.zshrc, .aliases, .env)
* `/bin/` - Helper utilities (thinktank-wrapper)

## Command Templates
When creating new slash commands in `/claude-commands/`:
* Follow existing command structure and format
* Include clear GOAL, ANALYZE, and EXECUTE sections
* Reference DEVELOPMENT_PHILOSOPHY.md principles
* Maintain consistency with workflow patterns

## Thinktank Integration
* Use `thinktank` CLI directly for analysis
* Pre-configured with model sets and context files
* Run: `thinktank --instructions temp_instructions.txt <paths>`
* API keys configured locally

## Commit Standards
* NEVER sign commit messages
* Follow Conventional Commits specification strictly
* Use meaningful multiline descriptions
* All commits must pass pre-commit hooks

## Code Standards (when adding code)
* TypeScript: strict typing, no `any`, immutable patterns, Prettier
* Go: golangci-lint, gofmt formatting
* Follow DEVELOPMENT_PHILOSOPHY.md core principles
* Document "why" not "how"

## Git Hooks
* Custom hooks in `.githooks/` directory
* `post-commit` runs `glance ./` asynchronously
* Never bypass with `--no-verify`