"""Context finder module for thinktank-wrapper.

This module provides functionality for finding context files like glance.md 
and DEVELOPMENT_PHILOSOPHY*.md based on command-line flags.
"""

import logging
import os
import pathlib
from typing import List, Optional, Set

from thinktank_wrapper import config
from thinktank_wrapper.gitignore import GitignoreFilter
from thinktank_wrapper.tokenizer import should_process_file_extension

logger = logging.getLogger(__name__)


def find_glance_files(search_paths: List[str], gitignore_enabled: bool = True) -> List[str]:
    """Find glance.md files in the provided search paths.
    
    Args:
        search_paths: List of paths to search in. If empty, the current
            working directory is used.
        gitignore_enabled: Whether to respect .gitignore rules when finding files.
            
    Returns:
        A list of absolute paths to glance.md files found.
    """
    result: Set[str] = set()
    
    # If no explicit search paths are provided, use the current working directory
    if not search_paths:
        search_paths = [os.getcwd()]
    
    # Set up gitignore filtering if enabled
    gitignore_filter: Optional[GitignoreFilter] = None
    if gitignore_enabled:
        try:
            gitignore_filter = GitignoreFilter(os.getcwd())
            if not gitignore_filter.is_enabled():
                logger.debug("Gitignore filtering requested but pathspec not available")
                gitignore_filter = None
        except Exception as e:
            logger.warning(f"Failed to initialize gitignore filtering: {e}")
            gitignore_filter = None
    
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
            abs_path = str(path.absolute())
            # Apply gitignore filtering if enabled
            if gitignore_filter is None or not gitignore_filter.should_ignore(abs_path):
                result.add(abs_path)
            else:
                logger.debug(f"Gitignore filtered out glance file: {abs_path}")
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
                    abs_path = str(glance_path.absolute())
                    # Apply gitignore filtering if enabled
                    if gitignore_filter is None or not gitignore_filter.should_ignore(abs_path):
                        result.add(abs_path)
                    else:
                        logger.debug(f"Gitignore filtered out glance file: {abs_path}")
    
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


def find_leyline_files(gitignore_enabled: bool = True) -> List[str]:
    """Find leyline documents with fallback to philosophy documents.
    
    First tries to find leyline documents in docs/leyline/ in the current working directory.
    If none are found, falls back to DEVELOPMENT_PHILOSOPHY*.md files in the same docs directory.
    
    Args:
        gitignore_enabled: Whether to respect .gitignore rules when finding files.
    
    Returns:
        A list of absolute paths to leyline or philosophy .md files found.
    """
    result: Set[str] = set()
    
    # Set up gitignore filtering if enabled
    gitignore_filter: Optional[GitignoreFilter] = None
    if gitignore_enabled:
        try:
            gitignore_filter = GitignoreFilter(os.getcwd())
            if not gitignore_filter.is_enabled():
                logger.debug("Gitignore filtering requested but pathspec not available")
                gitignore_filter = None
        except Exception as e:
            logger.warning(f"Failed to initialize gitignore filtering: {e}")
            gitignore_filter = None
    
    # Look in current working directory
    current_dir = pathlib.Path(os.getcwd())
    leyline_dir = current_dir / "docs" / "leyline"
    
    # First try: Look for leyline documents
    if leyline_dir.exists() and leyline_dir.is_dir():
        # Search for all .md files recursively in the leyline directory
        for leyline_path in leyline_dir.rglob("*.md"):
            if leyline_path.is_file():
                abs_path = str(leyline_path.absolute())
                # Apply gitignore filtering if enabled
                if gitignore_filter is None or not gitignore_filter.should_ignore(abs_path):
                    result.add(abs_path)
                else:
                    logger.debug(f"Gitignore filtered out leyline file: {abs_path}")
        
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
                abs_path = str(philosophy_path.absolute())
                # Apply gitignore filtering if enabled
                if gitignore_filter is None or not gitignore_filter.should_ignore(abs_path):
                    result.add(abs_path)
                else:
                    logger.debug(f"Gitignore filtered out philosophy file: {abs_path}")
        
        logger.info(f"Found {len(result)} philosophy files as fallback in {docs_dir}")
    else:
        logger.warning(f"Docs directory not found: {docs_dir}")
    
    # Sort the results for deterministic behavior
    return sorted(result)


def find_context_files(
    include_glance: bool, 
    include_leyline: bool,
    explicit_paths: List[str],
    gitignore_enabled: bool = True,
    include_extensions: Optional[List[str]] = None,
    exclude_extensions: Optional[List[str]] = None
) -> List[str]:
    """Find all context files based on flags and explicit paths.
    
    Args:
        include_glance: Whether to include glance.md files.
        include_leyline: Whether to include leyline documents (with philosophy fallback).
        explicit_paths: Explicit file/directory paths to include as context.
        gitignore_enabled: Whether to respect .gitignore rules when finding files.
        include_extensions: If provided, only process files with these extensions.
        exclude_extensions: If provided, skip files with these extensions.
        
    Returns:
        A list of absolute paths to context files.
    """
    result: Set[str] = set()
    
    # Find glance files if requested
    if include_glance:
        glance_files = find_glance_files([], gitignore_enabled=gitignore_enabled)
        result.update(glance_files)
        logger.info(f"Found {len(glance_files)} glance.md files")
    
    # Find leyline files (with philosophy fallback) if requested
    if include_leyline:
        leyline_files = find_leyline_files(gitignore_enabled=gitignore_enabled)
        result.update(leyline_files)
        # Note: logging is already handled in find_leyline_files()
    
    # Add explicit paths if they exist
    # Set up gitignore filtering for explicit paths
    gitignore_filter: Optional[GitignoreFilter] = None
    if gitignore_enabled:
        try:
            gitignore_filter = GitignoreFilter(os.getcwd())
            if not gitignore_filter.is_enabled():
                gitignore_filter = None
        except Exception as e:
            logger.warning(f"Failed to initialize gitignore filtering for explicit paths: {e}")
            gitignore_filter = None
    
    valid_explicit_paths = []
    for path_str in explicit_paths:
        path = pathlib.Path(path_str)
        if path.exists():
            abs_path = str(path.absolute())
            # Only apply filtering to files, not directories
            if path.is_file():
                # Apply extension filtering
                if not should_process_file_extension(abs_path, include_extensions, exclude_extensions):
                    logger.debug(f"Extension filtered out explicit file: {abs_path}")
                    continue
                
                # Apply gitignore filtering  
                if gitignore_filter is None or not gitignore_filter.should_ignore(abs_path):
                    valid_explicit_paths.append(abs_path)
                else:
                    logger.debug(f"Gitignore filtered out explicit file: {abs_path}")
            else:
                # Apply gitignore filtering to directories for consistency
                if gitignore_filter is None or not gitignore_filter.should_ignore(abs_path):
                    valid_explicit_paths.append(abs_path)
                else:
                    logger.warning(f"Explicit directory is gitignored and will be skipped: {abs_path}")
                    logger.warning(f"To include gitignored directory '{path_str}', disable gitignore filtering with --no-gitignore")
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