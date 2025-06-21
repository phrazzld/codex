# thinktank-wrapper

A Python wrapper for the thinktank tool that manages prompt templates directly and eliminates the need for symlinking prompt files across repositories.

## Features

- **Embedded Templates:** Prompt templates are bundled as package resources, eliminating the need for symlinking across repositories
- **Template Selection:** Choose templates by name with the `--template` option
- **Context Injection:** Inject custom context into template's designated CONTEXT section
- **Automatic Context Discovery:** Automatically find and include leyline documents from docs/leyline/
- **Flexible Configuration:** Configure model sets and easily override options
- **Structured Logging:** JSON-formatted logs with correlation IDs for traceability
- **Clean Error Handling:** Detailed error messages and proper exit codes
- **Compatibility:** Maintains backward compatibility with the original Bash wrapper

## Installation

### Prerequisites

- Python 3.8 or higher
- The `thinktank` executable in your PATH
- `$CODEX_DIR` environment variable set to the root of your codex repository

### Installing from Source

Clone the repository and install the package:

```bash
# Navigate to the directory containing the thinktank_wrapper package
cd /path/to/codex/bin/thinktank_wrapper

# Install the package in development mode
pip install -e .
```

### Installing via install.sh

The codex repository's `install.sh` script will automatically set up the thinktank-wrapper:

```bash
# Run the install script from the codex root directory
./install.sh
```

## Usage

### Basic Usage

```bash
# Use a template by name
thinktank-wrapper --template plan ./src

# Use a template with injected context
thinktank-wrapper --template debug --inject bug-details.md ./src

# List available templates
thinktank-wrapper --list-templates

# Use a specific model set
thinktank-wrapper --template debug --model-set high_context ./src

# Include automatic context files with injection
thinktank-wrapper --template ideate --inject context.md --include-philosophy ./src

# Dry run (print command without executing)
thinktank-wrapper --template review --dry-run ./src
```

### Advanced Usage

```bash
# Use an explicit instructions file (backward compatibility)
thinktank-wrapper --instructions custom-prompt.md ./src

# Pass through options to thinktank
thinktank-wrapper --template plan --timeout 600000 --output-dir ./output ./src

# Multiple context paths
thinktank-wrapper --template plan ./src ./tests ./docs
```

## Template Management

Templates are embedded as package resources in the `thinktank_wrapper/templates` directory. To add or modify templates:

1. Edit the files in the `src/thinktank_wrapper/templates` directory
2. Reinstall the package (`pip install -e .`)

### Context Injection

Templates include a standardized CONTEXT section that can be replaced with custom content using the `--inject` parameter. This section is marked with HTML comment markers:

```markdown
<!-- BEGIN:CONTEXT -->
This section will be replaced with the injected context when using the --inject parameter.
If no context is injected, this default message will remain.
<!-- END:CONTEXT -->
```

When using `--inject <file_path>`, the content between these markers will be replaced with the content of the specified file. This allows for customizing templates with specific contextual information without modifying the template itself.

## Command Reference

```
thinktank-wrapper [OPTIONS] [CONTEXT_PATHS...]
```

### Template Options

- `--template <template_name>`: Select a template by name
- `--inject <file_path>`: Inject content from a file into the template's CONTEXT section
- `--list-templates`: List available templates and exit
- `--instructions <file_path>`: Use an explicit instructions file (overrides `--template`)

### Model Options

- `--model-set <set_name>`: Select a model set (`all` or `high_context`)

### Context Options

- `--include-philosophy`: Include DEVELOPMENT_PHILOSOPHY*.md files and leyline documents automatically
- `CONTEXT_PATHS`: Explicit file/directory paths to include as context

### Execution Options

- `--dry-run`: Print the thinktank command without executing it

### Other Options

Any other options are passed directly to the thinktank command.

## Environment Variables

- `CODEX_DIR`: Path to the codex repository root (required for finding philosophy files)

## Development

### Setup

```bash
# Clone the repository
git clone <repository-url>

# Navigate to the package directory
cd bin/thinktank_wrapper

# Install development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=thinktank_wrapper

# Run specific tests
pytest tests/test_template_loader.py
```

## License

MIT
