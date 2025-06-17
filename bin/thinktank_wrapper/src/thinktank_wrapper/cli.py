"""Command-line interface module for thinktank-wrapper.

This module handles command-line argument parsing using argparse. It defines all flags,
positional arguments, and template selection logic.
"""

import argparse
import os
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
    template_group.add_argument(
        config.INJECT_ARG,
        help="Path to file containing context to inject into the template's CONTEXT section",
        metavar="<file_path>",
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
        config.INCLUDE_LEYLINE_ARG,
        action="store_true",
        help="Include leyline documents from docs/leyline/; if not found, falls back to DEVELOPMENT_PHILOSOPHY*.md files in docs/",
    )
    context_group.add_argument(
        "--no-gitignore",
        action="store_true", 
        help="Disable gitignore filtering when finding context files",
    )
    
    # File extension filtering
    extension_group = context_group.add_mutually_exclusive_group()
    extension_group.add_argument(
        "--include-ext",
        action="append",
        metavar="EXT",
        help="Only process files with these extensions (use multiple times: --include-ext .py --include-ext .js)",
    )
    extension_group.add_argument(
        "--exclude-ext", 
        action="append",
        metavar="EXT",
        help="Skip files with these extensions (use multiple times: --exclude-ext .log --exclude-ext .tmp)",
    )
    
    # Execution options
    execution_group = parser.add_argument_group("Execution Options")
    execution_group.add_argument(
        config.DRY_RUN_ARG,
        action="store_true",
        help="Print the final thinktank command instead of executing it",
    )
    execution_group.add_argument(
        "--token-threshold",
        type=int,
        default=config.LLM_CONTEXT_THRESHOLD,
        help=f"Token count threshold for model selection (default: {config.LLM_CONTEXT_THRESHOLD})",
        metavar="<tokens>",
    )
    execution_group.add_argument(
        "--disable-token-counting",
        action="store_true",
        help="Disable automatic token counting and model selection",
    )
    execution_group.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging, including details about skipped files",
    )
    execution_group.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode with structured JSON logging",
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
    
    # If --inject is provided, validate that:
    # 1. --template is also provided (can't inject into --instructions)
    # 2. The inject file exists and is readable
    if args.inject:
        if not args.template:
            raise ValueError(
                f"{config.INJECT_ARG} can only be used with {config.TEMPLATE_ARG}, "
                f"not with {config.INSTRUCTIONS_ARG}."
            )
        
        if not os.path.isfile(args.inject):
            raise ValueError(f"Inject file not found: {args.inject}")
        
        if not os.access(args.inject, os.R_OK):
            from pathlib import Path
            inject_path = Path(args.inject)
            raise ValueError(
                f"Permission denied reading inject file '{inject_path.name}'. "
                f"Check that you have read access to this file. "
                f"Try: chmod +r \"{inject_path}\" or run with appropriate permissions."
            )