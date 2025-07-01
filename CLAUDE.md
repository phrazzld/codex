# CLAUDE.md

Repository-specific guidance for Claude Code.

## Purpose
Configuration repository with AI templates, slash commands, and productivity tools.

## Structure
* `/bin/` - Thinktank scripts and utilities
* `/docs/` - Development philosophy and templates  
* `/dotfiles/` - Shell configs (.zshrc, .aliases, .env)
* `/scripts/` - System maintenance

## Thinktank Integration
* Use `thinktank` CLI directly
* Run: `thinktank --instructions temp_instructions.txt <paths>`
* API keys configured locally

## Standards
* Conventional commits, multiline descriptions
* TypeScript: strict typing, no `any`, immutable patterns
* Go: golangci-lint, gofmt formatting
* Document "why" not "how"
* Never bypass git hooks with `--no-verify`