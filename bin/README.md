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

A Python-based wrapper around the thinktank CLI that centralizes model configuration, manages prompt templates, and simplifies context file discovery.

**Key Features:**
- Embedded prompt templates (no need for symlinking across repositories)
- Template selection by name with `--template`
- Context injection into templates with `--inject`
- Automatic context file discovery
- Structured logging with correlation IDs
- Backward compatibility with the original Bash implementation

**Usage:**
```bash
thinktank-wrapper [OPTIONS] [CONTEXT_PATHS...]
```

**Common Options:**
- `--template <name>` - Use a named template from the embedded templates
- `--inject <file>` - Inject context from a file into the template's CONTEXT section
- `--list-templates` - List all available templates and exit
- `--model-set <set_name>` - Use predefined model set (all, high_context)
- `--include-glance` - Include glance.md files automatically
- `--include-philosophy` - Include DEVELOPMENT_PHILOSOPHY*.md files automatically
- `--dry-run` - Display the command that would be executed without running it
- `--instructions <file>` - Use an explicit instructions file (overrides --template)
- `-h, --help` - Show help message

**Examples:**
```bash
# Use a template by name
thinktank-wrapper --template plan ./src

# Use a template with injected context
thinktank-wrapper --template debug --inject bug-details.md ./src

# List available templates
thinktank-wrapper --list-templates

# Include glance.md files automatically with a specific template
thinktank-wrapper --template debug --include-glance --model-set high_context

# Include both glance and philosophy files with context injection
thinktank-wrapper --template ideate --inject context.md --include-glance --include-philosophy

# Show command without executing (dry run)
thinktank-wrapper --template review --dry-run file.md

# Backward compatibility with explicit instructions file
thinktank-wrapper --instructions custom-prompt.md --include-philosophy
```

For more detailed documentation, see the [thinktank_wrapper README](./thinktank_wrapper/README.md).

### code-review

Automated script for generating comprehensive code reviews using thinktank analysis.

**Usage:**
```bash
code-review [base_branch]
```

**Parameters:**
- `base_branch` - Branch to compare against (default: master)

**Features:**
- Automatically generates diff against base branch
- Identifies all changed files
- Runs thinktank-wrapper with review template
- Creates CODE_REVIEW.md from synthesis output
- Handles errors gracefully
- Cleans up temporary files

**Examples:**
```bash
# Review changes against master
code-review

# Review changes against specific branch
code-review feature/new-feature
```

**Output:**
- Creates `CODE_REVIEW.md` with comprehensive review analysis
- Temporarily creates `REVIEW-CONTEXT.md` (cleaned up on success)