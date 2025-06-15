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
        # Gitignore is enabled by default, disabled by --no-gitignore flag
        gitignore_enabled = not getattr(parsed_args, 'no_gitignore', False)
        
        # Get extension filtering parameters
        include_extensions = getattr(parsed_args, 'include_ext', None)
        exclude_extensions = getattr(parsed_args, 'exclude_ext', None)
        
        context_files = context_finder.find_context_files(
            include_glance=parsed_args.include_glance,
            include_leyline=parsed_args.include_leyline,
            explicit_paths=parsed_args.context_paths,
            gitignore_enabled=gitignore_enabled,
            include_extensions=include_extensions,
            exclude_extensions=exclude_extensions,
        )
        parsed_args.context_files = context_files
        logger.info(f"Found {len(context_files)} context files", extra={
            "include_glance": parsed_args.include_glance,
            "include_leyline": parsed_args.include_leyline,
            "explicit_paths_count": len(parsed_args.context_paths),
        })
        
        # Perform token counting and dynamic model selection if enabled
        disable_counting = getattr(parsed_args, "disable_token_counting", False)
        if config.ENABLE_TOKEN_COUNTING and not disable_counting:
            try:
                # Lazy import tokenizer to avoid breaking when optional deps missing
                from thinktank_wrapper import tokenizer
                
                # Initialize token counter with gitignore, verbose, and extension filtering settings
                verbose_enabled = getattr(parsed_args, 'verbose', False)
                token_counter = tokenizer.TokenCounter(
                    provider=config.TOKEN_COUNT_PROVIDER,
                    gitignore_enabled=gitignore_enabled,
                    verbose=verbose_enabled,
                    include_extensions=include_extensions,
                    exclude_extensions=exclude_extensions
                )
                
                # Count tokens in all context files
                total_tokens, errors = token_counter.estimate_model_tokens(context_files)
                
                # Output token count to stderr to avoid polluting stdout
                print(f"TOKEN_COUNT: {total_tokens}", file=sys.stderr)
                
                # Log any errors
                if errors:
                    for error in errors:
                        logger.warning(f"Token counting error: {error}")
                
                # Dynamic model selection based on threshold
                threshold = getattr(parsed_args, "token_threshold", config.LLM_CONTEXT_THRESHOLD)
                original_model_set = parsed_args.model_set
                
                # Only perform dynamic selection if user didn't explicitly set model-set
                if original_model_set is None:
                    if total_tokens <= threshold:
                        parsed_args.model_set = "all"
                        logger.info(f"Selected model set 'all' (tokens: {total_tokens} <= threshold: {threshold})")
                    else:
                        parsed_args.model_set = "high_context"
                        logger.info(f"Selected model set 'high_context' (tokens: {total_tokens} > threshold: {threshold})")
                    
                    # Output model selection info to stderr
                    print(f"Using model set: {parsed_args.model_set} (threshold: {threshold})", file=sys.stderr)
                else:
                    # User explicitly set model-set, respect their choice
                    logger.info(f"Using explicitly set model set: {original_model_set}")
                
                # Set default if still None
                if parsed_args.model_set is None:
                    parsed_args.model_set = config.DEFAULT_MODEL_SET
                    
            except ImportError as e:
                logger.warning(f"Token counting module not available: {e}")
                # Continue without token counting
            except (ValueError, TypeError, AttributeError) as e:
                logger.error(f"Token counting configuration error: {e}", exc_info=True)
                # Continue with original model set selection
            except Exception as e:
                logger.error(f"Unexpected error during token counting: {e}", exc_info=True)
                # Continue with original model set selection
        
        # Ensure model_set has a value (use default if still None)
        if parsed_args.model_set is None:
            parsed_args.model_set = config.DEFAULT_MODEL_SET
        
        # Load template content if --template is provided
        template_content = None
        if parsed_args.template:
            template_content = template_loader.load_template(parsed_args.template)
            logger.info(f"Loaded template: {parsed_args.template}", extra={
                "template_name": parsed_args.template,
                "template_size": len(template_content),
            })
            
            # Inject context if --inject is provided
            if parsed_args.inject:
                try:
                    template_content = template_loader.inject_context(template_content, parsed_args.inject)
                    logger.info(f"Injected context from: {parsed_args.inject}", extra={
                        "inject_file": parsed_args.inject,
                        "template_size_after_injection": len(template_content),
                    })
                except ValueError as e:
                    logger.error(f"Failed to inject context: {e}")
                    print(f"Error: {e}", file=sys.stderr)
                    return 1
        
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