# Prompts

This directory contains template prompts for use with Claude Code and other AI assistants.

## Purpose

These prompt templates provide structured frameworks for common development tasks. They help ensure consistent interactions with AI assistants and guide the AI toward providing the most helpful and relevant responses.

## Available Prompts

- **[audit.md](audit.md)** - Security audit documentation templates
- **[breathe.md](breathe.md)** - Prompts for reflective development practices
- **[consult.md](consult.md)** - Guidance for architectural consultation
- **[debug.md](debug.md)** - Structured approach to debugging problems
- **[execute.md](execute.md)** - Framework for implementing tasks and features
- **[ideate.md](ideate.md)** - Templates for creative solution exploration
- **[plan.md](plan.md)** - Templates for creating technical plans
- **[refactor.md](refactor.md)** - Guidelines for code refactoring
- **[resolve.md](resolve.md)** - Strategies for resolving specific issues
- **[review.md](review.md)** - Structured code review processes
- **[ticket.md](ticket.md)** - Templates for creating task tickets

## Prompt Structure

Each prompt generally follows a consistent format:

1. **Goal/Purpose** - Clear statement of what the prompt aims to achieve
2. **Context Requirements** - What information should be provided to the AI
3. **Process Steps** - Structured workflow for the AI to follow
4. **Output Format** - Expected deliverables from the interaction

This structure ensures that prompts produce consistent, high-quality results regardless of who uses them.

## Relationship to Claude Commands

These prompts correspond to the slash commands in the `/claude-commands` directory. They provide the content templates that are used when those commands are invoked. 

When a slash command is executed (e.g., `/prime`), the Claude Code CLI uses the corresponding prompt template from this directory to structure the interaction.

## Customization

These prompts can be customized to better fit specific project needs or personal preferences. When making modifications:

1. Maintain the structured approach that guides both the user and the AI
2. Ensure all critical aspects of each task type are covered
3. Keep language clear and actionable
4. Update the corresponding slash command in `/claude-commands/` if significant changes are made
5. Test the modified prompt to ensure it produces the desired outcome