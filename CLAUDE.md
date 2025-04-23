# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build, Test, Lint Commands

* Project is primarily a collection of prompt templates and configuration files
* No specific build process required
* No testing commands defined
* No linting commands defined

## Style Guidelines

* Follow core principles from `DEVELOPMENT_PHILOSOPHY.md`
* Prefer simplicity and maintainability over complexity
* Ensure commit messages follow Conventional Commits specification
* NEVER sign your commit messages. Your commits should ALWAYS and ONLY contain meaningful detailed multiline conventional commits about the work done.
* Document "why" not "how" in comments
* Adhere to strict configuration for any code added to the repository:
  * TypeScript: strict typing with no `any`, use immutable patterns, Prettier formatting
  * Go: strict linting with golangci-lint, gofmt formatting

## Project Structure

* Organize by feature/domain not technical type
* Use `/claude-commands/` for custom Claude CLI slash commands
* Use `/docs/` for all documentation, organized by purpose
* Keep file and function sizes reasonable

## Error Handling & Quality Gates

* Never suppress errors/warnings - fix root causes
* Never hardcode secrets - use environment variables
* All code must pass pre-commit hooks and CI checks
* Ensure consistent, explicit error handling
* Follow Test-Driven Development when applicable

## Thinktank Tool

* Use `thinktank` CLI for deeper analysis when needed
* Run with: `thinktank --instructions temp_instructions.txt <relevant_paths...>`
* API keys are pre-configured locally