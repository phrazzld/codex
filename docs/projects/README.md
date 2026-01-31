# Project Detail Files

This directory contains detailed documentation for projects that need more than a one-line description.

## When to Create a Detail File

Create a `<project-name>.md` file here when:
- Moving from idea to active development
- Need to track architecture decisions
- Brainstorming names, features, or technical approaches
- Recording todos and implementation notes
- Documenting why certain choices were made

## Template Structure

Use this template for new project files:

```markdown
# Project Name

> One-line tagline

**Status:** 💡 idea | 🔨 active | ⏸️ paused | ✅ shipped | 📦 archived
**Repo:** `github.com/username/repo`
**Tech Stack:** Language, Framework, etc.

## Overview

Brief description of what this project is and why it exists.

## Names Under Consideration

- primary-name ⭐ (current favorite)
- alternative-name
- another-option

## Architecture

Key technical decisions, frameworks, dependencies, deployment strategy.

## Features

### Core (MVP)
- [ ] Feature 1
- [ ] Feature 2

### Future
- [ ] Nice-to-have feature
- [ ] Stretch goal

## Notes

Random thoughts, links, references, things to research.

## Todo

- [ ] Next concrete step
- [ ] Another actionable item
```

## Maintenance

- Keep in sync with main `docs/projects.md` registry
- Archive detail files when project status → archived
- Delete detail files for abandoned ideas
