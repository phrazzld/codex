"""Context finder module for thinktank-wrapper.

This module provides functionality for finding context files like glance.md 
and DEVELOPMENT_PHILOSOPHY*.md based on command-line flags.
"""

import logging
import os
import pathlib
from typing import List, Set

from thinktank_wrapper import config

logger = logging.getLogger(__name__)


def find_glance_files(search_paths: List[str]) -> List[str]:
    """Find glance.md files in the provided search paths.
    
    Args:
        search_paths: List of paths to search in. If empty, the current
            working directory is used.
            
    Returns:
        A list of absolute paths to glance.md files found.
    """
    result: Set[str] = set()
    
    # If no explicit search paths are provided, use the current working directory
    if not search_paths:
        search_paths = [os.getcwd()]
    
    # Log the search paths
    logger.debug(f"Searching for glance.md files in {len(search_paths)} paths")
    
    for search_path in search_paths:
        path = pathlib.Path(search_path)
        
        # Skip non-existent paths with a warning
        if not path.exists():
            logger.warning(f"Search path does not exist: {path}")
            continue
        
        # If the path is a file (not a directory), check if it's a glance.md file
        if path.is_file() and path.name.lower() == "glance.md":
            result.add(str(path.absolute()))
            continue
        
        # Otherwise, search for glance.md files in the directory (up to MAX_GLANCE_DEPTH levels deep)
        if path.is_dir():
            # Use rglob to recursively search for glance.md files
            # The pattern "*/glance.md" will start at subdirectories, not the current level
            for glance_path in path.glob("**/glance.md"):
                # Check if the depth is within limits
                # Calculate relative path parts to determine depth
                rel_path = glance_path.relative_to(path)
                depth = len(rel_path.parts)
                
                if depth <= config.MAX_GLANCE_DEPTH:
                    result.add(str(glance_path.absolute()))
    
    # Sort the results for deterministic behavior
    return sorted(result)


def find_philosophy_files() -> List[str]:
    """Find DEVELOPMENT_PHILOSOPHY*.md files in the current working directory's docs folder.
    
    Returns:
        A list of absolute paths to philosophy files found.
    """
    result: Set[str] = set()
    
    # Look in current working directory's docs folder
    current_dir = pathlib.Path(os.getcwd())
    docs_dir = current_dir / "docs"
    if not docs_dir.exists() or not docs_dir.is_dir():
        logger.warning(f"Docs directory not found: {docs_dir}")
        return []
    
    # Search for philosophy files in the docs directory
    philosophy_pattern = "DEVELOPMENT_PHILOSOPHY*.md"
    for philosophy_path in docs_dir.glob(philosophy_pattern):
        if philosophy_path.is_file():
            result.add(str(philosophy_path.absolute()))
    
    # Log the result
    logger.debug(f"Found {len(result)} philosophy files in {docs_dir}")
    
    # Sort the results for deterministic behavior
    return sorted(result)


def find_leyline_files() -> List[str]:
    """Find leyline documents with fallback to philosophy documents.
    
    First tries to find leyline documents in docs/leyline/ in the current working directory.
    If none are found, falls back to DEVELOPMENT_PHILOSOPHY*.md files in the same docs directory.
    
    Returns:
        A list of absolute paths to leyline or philosophy .md files found.
    """
    result: Set[str] = set()
    
    # Look in current working directory
    current_dir = pathlib.Path(os.getcwd())
    leyline_dir = current_dir / "docs" / "leyline"
    
    # First try: Look for leyline documents
    if leyline_dir.exists() and leyline_dir.is_dir():
        # Search for all .md files recursively in the leyline directory
        for leyline_path in leyline_dir.rglob("*.md"):
            if leyline_path.is_file():
                result.add(str(leyline_path.absolute()))
        
        if result:
            logger.info(f"Found {len(result)} leyline files in {leyline_dir}")
            return sorted(result)
    
    # Fallback: Look for philosophy documents if no leyline files found
    logger.info("No leyline files found, falling back to philosophy documents")
    docs_dir = current_dir / "docs"
    if docs_dir.exists() and docs_dir.is_dir():
        philosophy_pattern = "DEVELOPMENT_PHILOSOPHY*.md"
        for philosophy_path in docs_dir.glob(philosophy_pattern):
            if philosophy_path.is_file():
                result.add(str(philosophy_path.absolute()))
        
        logger.info(f"Found {len(result)} philosophy files as fallback in {docs_dir}")
    else:
        logger.warning(f"Docs directory not found: {docs_dir}")
    
    # Sort the results for deterministic behavior
    return sorted(result)


def find_context_files(
    include_glance: bool, 
    include_leyline: bool,
    explicit_paths: List[str]
) -> List[str]:
    """Find all context files based on flags and explicit paths.
    
    Args:
        include_glance: Whether to include glance.md files.
        include_leyline: Whether to include leyline documents (with philosophy fallback).
        explicit_paths: Explicit file/directory paths to include as context.
        
    Returns:
        A list of absolute paths to context files.
    """
    result: Set[str] = set()
    
    # Find glance files if requested
    if include_glance:
        glance_files = find_glance_files(explicit_paths)
        result.update(glance_files)
        logger.info(f"Found {len(glance_files)} glance.md files")
    
    # Find leyline files (with philosophy fallback) if requested
    if include_leyline:
        leyline_files = find_leyline_files()
        result.update(leyline_files)
        # Note: logging is already handled in find_leyline_files()
    
    # Add explicit paths if they exist
    valid_explicit_paths = []
    for path_str in explicit_paths:
        path = pathlib.Path(path_str)
        if path.exists():
            valid_explicit_paths.append(str(path.absolute()))
        else:
            logger.warning(f"Explicit path does not exist: {path_str}")
    
    result.update(valid_explicit_paths)
    
    # Remove duplicates and sort for deterministic behavior
    return sorted(result)


def validate_paths(paths: List[str]) -> List[str]:
    """Validate that the provided paths exist.
    
    Args:
        paths: List of paths to validate.
        
    Returns:
        A list of absolute paths that exist.
    """
    valid_paths = []
    for path_str in paths:
        path = pathlib.Path(path_str)
        if path.exists():
            valid_paths.append(str(path.absolute()))
        else:
            logger.warning(f"Path does not exist: {path_str}")
    
    return valid_paths