# Codex Bin Directory

This directory contains utility scripts and tools used within the codex repository.

## Installation

The installation script automatically adds this directory to your PATH. If you need to manually add it:

```bash
# Add this line to your ~/.zshrc or ~/.bashrc to add local bin to PATH
export PATH="$PATH:$HOME/Development/codex/bin"
```

## Utilities

### thinktank-wrapper

A configurable wrapper around the thinktank CLI that centralizes model configuration and file finding logic.

**Usage:**
```bash
thinktank-wrapper [OPTIONS] [FILE_PATHS...]
```

**Common Options:**
- `--model-set <set_name>` - Use predefined model set (all, high_context)
- `--include-glance` - Include glance.md files automatically
- `--include-philosophy` - Include DEVELOPMENT_PHILOSOPHY*.md files automatically
- `--dry-run` - Display the command that would be executed without running it
- `-h, --help` - Show help message

**Examples:**
```bash
# Basic usage with explicit files
thinktank-wrapper --model-set all file1.md file2.md

# Include glance.md files automatically
thinktank-wrapper --include-glance --model-set high_context

# Include both glance and philosophy files
thinktank-wrapper --include-glance --include-philosophy

# Show command without executing (dry run)
thinktank-wrapper --dry-run --include-philosophy file.md
```
