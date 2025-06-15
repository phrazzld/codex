"""Template loader module for thinktank-wrapper.

This module provides functionality for discovering and loading prompt templates
that are bundled as package resources with the thinktank_wrapper package.
"""

import importlib.resources
import os
import pathlib
import re
from pathlib import Path
from typing import List, Optional, Union

from thinktank_wrapper import config
from thinktank_wrapper.tokenizer import get_file_access_error_message, get_encoding_error_message


class TemplateNotFoundError(Exception):
    """Raised when a requested template cannot be found."""

    def __init__(self, template_name: str, available_templates: List[str]):
        """Initialize the exception with the template name and available templates.
        
        Args:
            template_name: The name of the template that was not found.
            available_templates: A list of available template names.
        """
        self.template_name = template_name
        self.available_templates = available_templates
        message = (
            f"Template '{template_name}' not found. "
            f"Available templates: {', '.join(sorted(available_templates))}"
        )
        super().__init__(message)


def list_templates() -> List[str]:
    """List all available prompt templates.
    
    Returns:
        A list of template names (without the .md extension).
    """
    templates = []
    try:
        # Get the template directory resource
        templates_dir = importlib.resources.files("thinktank_wrapper.templates")
        
        # Iterate through all files in the templates directory
        for path in templates_dir.iterdir():
            if path.is_file() and path.name.endswith(".md") and path.name != "__init__.py":
                # Add the template name without the .md extension
                templates.append(path.stem)
    except (ImportError, FileNotFoundError):
        # Handle cases where the templates directory might not exist
        pass
    
    return templates


def load_template(name: str) -> str:
    """Load a template by name.
    
    Args:
        name: The name of the template to load (without the .md extension).
        
    Returns:
        The content of the template as a string.
        
    Raises:
        TemplateNotFoundError: If the template cannot be found.
    """
    # Normalize the template name by removing any .md extension if present
    if name.endswith(".md"):
        name = name[:-3]
    
    # Get the list of available templates
    available_templates = list_templates()
    
    # Check if the requested template exists
    if name not in available_templates:
        raise TemplateNotFoundError(name, available_templates)
    
    try:
        # Construct the path to the template
        template_path = f"{name}.md"
        
        # Read the template content
        template_content = importlib.resources.files("thinktank_wrapper.templates").joinpath(template_path).read_text(encoding="utf-8")
        
        return template_content
    except (ImportError, FileNotFoundError) as e:
        # This should not happen if we've already validated the template exists,
        # but handle it just in case
        raise TemplateNotFoundError(name, available_templates) from e


def inject_context(template_content: str, context_file_path: Optional[str]) -> str:
    """Inject context from a file into a template's CONTEXT section.
    
    Args:
        template_content: The template content as a string.
        context_file_path: The path to the file containing the context to inject.
                          If None, the template is returned unchanged.
    
    Returns:
        The template content with the injected context.
        
    Raises:
        ValueError: If the template doesn't contain the CONTEXT markers.
    """
    if not context_file_path:
        return template_content
    
    # Check if the template has the CONTEXT section
    if (config.CONTEXT_BEGIN_MARKER not in template_content or 
        config.CONTEXT_END_MARKER not in template_content):
        raise ValueError(
            f"Template does not contain required markers for context injection: "
            f"{config.CONTEXT_BEGIN_MARKER} and {config.CONTEXT_END_MARKER}"
        )
    
    try:
        # Read the context content
        with open(context_file_path, "r", encoding="utf-8") as f:
            context_content = f.read()
        
        # Instead of using regex, use string operations for replacement
        # Find the positions of the markers
        begin_pos = template_content.find(config.CONTEXT_BEGIN_MARKER)
        end_pos = template_content.find(config.CONTEXT_END_MARKER, begin_pos) + len(config.CONTEXT_END_MARKER)
        
        # Replace the content between markers
        replaced_content = (
            template_content[:begin_pos] + 
            config.CONTEXT_BEGIN_MARKER + 
            "\n" + context_content + "\n" + 
            config.CONTEXT_END_MARKER + 
            template_content[end_pos:]
        )
        
        return replaced_content
    except (PermissionError, FileNotFoundError, IsADirectoryError, OSError, IOError) as e:
        error_message = get_file_access_error_message(context_file_path, e)
        raise ValueError(f"Failed to read context file: {error_message}") from e
    except UnicodeDecodeError as e:
        error_message = get_encoding_error_message(context_file_path, e)
        raise ValueError(f"Failed to read context file: {error_message}") from e