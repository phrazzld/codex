"""Command-line interface module for thinktank-wrapper.

This module handles command-line argument parsing using argparse. It defines all flags,
positional arguments, and template selection logic.
"""

import argparse
import sys
from typing import List, Optional, Tuple

from thinktank_wrapper import config, template_loader


def parse_args(args: Optional[List[str]] = None) -> Tuple[argparse.Namespace, List[str]]:
    """Parse command-line arguments for thinktank-wrapper.
    
    Args:
        args: Command-line arguments to parse. If None, sys.argv[1:] is used.
        
    Returns:
        A tuple containing:
            - The parsed arguments as a Namespace object
            - A list of unknown arguments to pass through to thinktank
    """
    parser = argparse.ArgumentParser(
        description="A wrapper for the thinktank tool that manages prompt templates.",
        epilog=(
            "Any unknown options are passed directly to the thinktank command. "
            "Any paths provided are included with automatically found context files."
        ),
    )
    
    # Template selection options
    template_group = parser.add_argument_group("Template Options")
    template_group.add_argument(
        config.TEMPLATE_ARG,
        help="The name of the prompt template to use (without .md extension)",
        metavar="<template_name>",
    )
    template_group.add_argument(
        config.LIST_TEMPLATES_ARG,
        action="store_true",
        help="List available embedded templates and exit",
    )
    
    # Model selection options
    model_group = parser.add_argument_group("Model Options")
    model_group.add_argument(
        config.MODEL_SET_ARG,
        choices=list(config.MODEL_SETS.keys()),
        default=config.DEFAULT_MODEL_SET,
        help=f"Select model set (default: {config.DEFAULT_MODEL_SET})",
        metavar="<set_name>",
    )
    
    # Context file finding options
    context_group = parser.add_argument_group("Context Options")
    context_group.add_argument(
        config.INCLUDE_GLANCE_ARG,
        action="store_true",
        help="Include glance.md files automatically",
    )
    context_group.add_argument(
        config.INCLUDE_PHILOSOPHY_ARG,
        action="store_true",
        help="Include DEVELOPMENT_PHILOSOPHY*.md files automatically",
    )
    
    # Execution options
    execution_group = parser.add_argument_group("Execution Options")
    execution_group.add_argument(
        config.DRY_RUN_ARG,
        action="store_true",
        help="Print the final thinktank command instead of executing it",
    )
    
    # Backward compatibility
    compat_group = parser.add_argument_group("Backward Compatibility")
    compat_group.add_argument(
        config.INSTRUCTIONS_ARG,
        help="Explicitly provide an instructions file path (overrides --template)",
        metavar="<file_path>",
    )
    
    # Context paths (positional arguments at the end)
    parser.add_argument(
        "context_paths",
        nargs="*",
        help="Explicit file/directory paths to include as context",
        metavar="CONTEXT_PATHS",
    )
    
    # Use parse_known_args to allow for pass-through arguments to thinktank
    return parser.parse_known_args(args)


def handle_list_templates() -> None:
    """Handle the --list-templates flag by listing available templates and exiting.
    
    This function prints the available templates and exits with a success code.
    """
    templates = template_loader.list_templates()
    if templates:
        print("Available templates:")
        for template in sorted(templates):
            print(f"  - {template}")
    else:
        print("No templates found.")
    sys.exit(0)


def validate_args(args: argparse.Namespace) -> None:
    """Validate the parsed arguments.
    
    Args:
        args: The parsed arguments to validate.
        
    Raises:
        ValueError: If the arguments are invalid.
    """
    # If --list-templates is provided, no validation needed as it will exit early
    if args.list_templates:
        return
    
    # If neither --template nor --instructions is provided, raise an error
    if not args.template and not args.instructions:
        raise ValueError(
            f"Either {config.TEMPLATE_ARG} or {config.INSTRUCTIONS_ARG} must be provided. "
            f"Use {config.LIST_TEMPLATES_ARG} to see available templates."
        )
    
    # If --template is provided, validate that it exists
    if args.template:
        try:
            # Just check if the template can be loaded, but don't actually need the content here
            template_loader.load_template(args.template)
        except template_loader.TemplateNotFoundError as e:
            # Re-raise as ValueError for consistent error handling in __main__
            raise ValueError(str(e)) from e