# thinktank-wrapper

A Python wrapper for the thinktank tool that manages prompt templates directly and eliminates the need for symlinking prompt files across repositories.

## Features

- Embedded prompt templates as package resources
- Template selection by name
- Automatic context file discovery
- Model set configuration
- Pass-through arguments to thinktank

## Installation

```
pip install .
```

## Usage

```
thinktank-wrapper --template <template_name> [CONTEXT_FILES...]
```

For more options:

```
thinktank-wrapper --help
```