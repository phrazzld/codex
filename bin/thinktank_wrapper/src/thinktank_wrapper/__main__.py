"""Main module for thinktank-wrapper.

This module provides the entry point for the thinktank-wrapper CLI application.
It orchestrates the parsing of arguments, template loading, context file finding,
command building, and execution.
"""

import logging
import os
import sys
from typing import List, Optional

from thinktank_wrapper import (
    cli,
    command_builder,
    config,
    context_finder,
    executor,
    logging_config,
    template_loader,
)


def main(args: Optional[List[str]] = None) -> int:
    """Run the thinktank-wrapper application.
    
    Args:
        args: Command-line arguments to parse. If None, sys.argv[1:] is used.
        
    Returns:
        The exit code to return to the shell.
    """
    # Set up logging with structured output and a correlation ID
    correlation_id = logging_config.setup_logging(structured=True)
    logger = logging.getLogger(__name__)
    logger.info("Starting thinktank-wrapper", extra={
        "version": "0.1.0",
    })
    
    # Initialize variable to track any temp file we create
    temp_file_path: Optional[str] = None
    
    try:
        # Parse command-line arguments
        parsed_args, unknown_args = cli.parse_args(args)
        logger.debug("Arguments parsed successfully", extra={
            "args": vars(parsed_args),
            "unknown_args_count": len(unknown_args),
        })
        
        # Handle --list-templates flag
        if parsed_args.list_templates:
            cli.handle_list_templates()
            # handle_list_templates will exit the process, so we don't need to return
        
        # Validate arguments
        cli.validate_args(parsed_args)
        
        # Find context files based on flags and explicit paths
        context_files = context_finder.find_context_files(
            include_glance=parsed_args.include_glance,
            include_philosophy=parsed_args.include_philosophy,
            explicit_paths=parsed_args.context_paths,
        )
        parsed_args.context_files = context_files
        logger.info(f"Found {len(context_files)} context files", extra={
            "include_glance": parsed_args.include_glance,
            "include_philosophy": parsed_args.include_philosophy,
            "explicit_paths_count": len(parsed_args.context_paths),
        })
        
        # Load template content if --template is provided
        template_content = None
        if parsed_args.template:
            template_content = template_loader.load_template(parsed_args.template)
            logger.info(f"Loaded template: {parsed_args.template}", extra={
                "template_name": parsed_args.template,
                "template_size": len(template_content),
            })
        
        # Build the command
        cmd_args, temp_file_path = command_builder.build_command(
            parsed_args, unknown_args, template_content
        )
        logger.debug("Command built successfully", extra={
            "cmd_args_count": len(cmd_args),
            "has_temp_file": temp_file_path is not None,
        })
        
        # Execute the command (or just print it if --dry-run)
        return_code = executor.run_command(cmd_args, parsed_args.dry_run)
        
        return return_code
    except template_loader.TemplateNotFoundError as e:
        logger.error(f"Template not found: {e}")
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except (ValueError, command_builder.CommandBuilderError) as e:
        logger.error(f"Error: {e}")
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except executor.ThinktankNotFoundError as e:
        logger.error(f"Thinktank not found: {e}")
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except executor.ThinktankExecutionError as e:
        logger.error(f"Thinktank execution error: {e}")
        print(f"Error: {e}", file=sys.stderr)
        return e.return_code if e.return_code != 0 else 1
    except KeyboardInterrupt:
        logger.warning("Interrupted by user")
        print("Interrupted by user", file=sys.stderr)
        return 130  # Standard exit code for SIGINT
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        print(f"Error: An unexpected error occurred: {e}", file=sys.stderr)
        return 1
    finally:
        # Clean up any temporary file we created
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
                logger.debug(f"Removed temporary file: {temp_file_path}")
            except OSError as e:
                logger.warning(f"Failed to remove temporary file {temp_file_path}: {e}")


if __name__ == "__main__":
    sys.exit(main())