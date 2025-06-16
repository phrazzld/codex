"""Command builder module for thinktank-wrapper.

This module provides functionality for constructing the thinktank command
based on the parsed arguments, selected template, and context files.
"""

import argparse
import logging
import os
import tempfile
from typing import Dict, List, Optional, Tuple

from thinktank_wrapper import config

logger = logging.getLogger(__name__)


class CommandBuilderError(Exception):
    """Raised when an error occurs during command building."""
    pass


def _add_model_args(cmd_args: List[str], model_set_name: str) -> None:
    """Add model arguments to the command line based on the selected model set.
    
    Args:
        cmd_args: The command line argument list to append to.
        model_set_name: The name of the model set to use.
        
    Raises:
        CommandBuilderError: If the model set name is invalid.
    """
    # Validate the model set name
    if model_set_name not in config.MODEL_SETS:
        valid_sets = ", ".join(sorted(config.MODEL_SETS.keys()))
        raise CommandBuilderError(
            f"Invalid model set: '{model_set_name}'. "
            f"Valid options are: {valid_sets}"
        )
    
    # Add the model arguments
    for model in config.MODEL_SETS[model_set_name]:
        cmd_args.extend(["--model", model])
    
    # Add the synthesis model
    cmd_args.extend(["--synthesis-model", config.SYNTHESIS_MODEL])
    
    logger.debug(
        f"Added {len(config.MODEL_SETS[model_set_name])} models from set '{model_set_name}' "
        f"and synthesis model '{config.SYNTHESIS_MODEL}'"
    )


def build_command(
    args: argparse.Namespace, 
    unknown_args: List[str],
    template_content: Optional[str] = None
) -> Tuple[List[str], Optional[str]]:
    """Build the thinktank command based on the parsed arguments.
    
    Args:
        args: The parsed arguments.
        unknown_args: Unknown arguments to pass through to thinktank.
        template_content: The content of the template if one was selected.
        
    Returns:
        A tuple containing:
            - The thinktank command as a list of strings.
            - The path to the temporary template file (if one was created), or None.
            
    Raises:
        CommandBuilderError: If an error occurs during command building.
    """
    # Initialize the command with the thinktank executable
    cmd_args: List[str] = ["thinktank"]
    
    # Keep track of any temporary file we create
    temp_file_path: Optional[str] = None
    
    # Process unknown args (pass-through to thinktank)
    # We need to handle them carefully as some may have values
    i = 0
    while i < len(unknown_args):
        arg = unknown_args[i]
        
        # If this is an option with a value, include both
        if arg.startswith("-") and i + 1 < len(unknown_args) and not unknown_args[i + 1].startswith("-"):
            cmd_args.extend([arg, unknown_args[i + 1]])
            i += 2
        # Otherwise, just include the option
        else:
            cmd_args.append(arg)
            i += 1
    
    # Handle instructions file
    # If --instructions is explicitly provided, use that
    # Otherwise, if template_content is provided, create a temporary file
    if args.instructions:
        cmd_args.extend([config.INSTRUCTIONS_ARG, args.instructions])
        logger.info(f"Using provided instructions file: {args.instructions}")
    elif template_content:
        try:
            # Create a temporary file for the template content
            fd, temp_file_path = tempfile.mkstemp(suffix=".md", prefix="thinktank-template-")
            
            # Write the template content to the temporary file
            with os.fdopen(fd, "w") as f:
                f.write(template_content)
            
            # Add the temporary file path to the command
            cmd_args.extend([config.INSTRUCTIONS_ARG, temp_file_path])
            logger.info(f"Created temporary instructions file: {temp_file_path}")
        except (IOError, OSError) as e:
            # If temp_file_path was set by mkstemp, try to clean it up
            if temp_file_path:
                try:
                    os.unlink(temp_file_path)
                except OSError:
                    # Ignore cleanup errors - the important thing is to raise the original error
                    pass
            raise CommandBuilderError(f"Failed to create temporary file: {e}") from e
    else:
        # Neither --instructions nor template_content provided
        # This should not happen due to validation in cli.py, but handle it just in case
        raise CommandBuilderError(
            "Neither instructions file nor template content provided. "
            "This is likely a bug in the program."
        )
    
    # Add model arguments
    _add_model_args(cmd_args, args.model_set)
    
    # Add context files at the end
    if hasattr(args, "context_files") and args.context_files:
        cmd_args.extend(args.context_files)
        logger.debug(f"Added {len(args.context_files)} context files")
    
    return cmd_args, temp_file_path