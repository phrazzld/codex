# Bin Directory

Utility scripts and thinktank automation tools.

## Installation

Installation script adds this directory to PATH:
```bash
export PATH="$PATH:$HOME/Development/codex/bin"
```

## TT Scripts

Direct thinktank CLI automation using shared library (`tt-common.sh`):

- `tt-review-diff` - Diff-focused code review (bugs, functional issues)
- `tt-review` - General code review automation  
- `tt-address` - Generate remediation plans from reviews
- `tt-ticket` - Break plans into atomic tasks (TODO.md)
- `tt-plan` - Create implementation plans from context
- `tt-groom` - Organize and prioritize backlog
- `tt-ideate` - Generate innovative backlog ideas
- `tt-refactor` - Identify refactoring opportunities  
- `tt-shrink` - Find code size optimization opportunities
- `tt-security` - Security audit with OWASP focus
- `tt-gordian` - Radical simplification analysis
- `tt-align` - Philosophy alignment review

## Other Utilities

- `alacritty-theme` - Theme switching for Alacritty
- `toggle-theme`, `light-mode`, `dark-mode` - System theme control
- `tmux-startup` - Development session startup
- `adminifi` - Admin privilege escalation
- `todo-stats` - TODO analysis