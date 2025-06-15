"""Gitignore handling module for thinktank-wrapper.

This module provides functionality for parsing and applying .gitignore rules
when traversing directories and collecting files for token counting.
"""

import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

try:
    import pathspec
    PathSpecType = pathspec.PathSpec
except ImportError:
    pathspec = None
    PathSpecType = Any  # Use Any when pathspec is not available

logger = logging.getLogger(__name__)


class GitignoreFilter:
    """Handles .gitignore pattern matching for file filtering."""
    
    def __init__(self, root_path: Union[str, Path]):
        """Initialize the GitignoreFilter for a given root directory.
        
        Args:
            root_path: The root directory to start searching for .gitignore files
        """
        self.root_path = Path(root_path).resolve()
        self._spec_cache: Dict[Path, Optional[PathSpecType]] = {}
        self._enabled = pathspec is not None
        
        if not self._enabled:
            logger.warning("pathspec library not available - gitignore filtering disabled")
    
    def is_enabled(self) -> bool:
        """Check if gitignore filtering is enabled (pathspec library available).
        
        Returns:
            True if gitignore filtering can be performed, False otherwise
        """
        return self._enabled
    
    def _load_gitignore_spec(self, directory: Path) -> Optional[PathSpecType]:
        """Load .gitignore patterns from a directory and return a PathSpec.
        
        Args:
            directory: Directory to look for .gitignore file
            
        Returns:
            PathSpec object if .gitignore exists and can be parsed, None otherwise
        """
        if not self._enabled:
            return None
            
        gitignore_path = directory / ".gitignore"
        
        if not gitignore_path.exists() or not gitignore_path.is_file():
            return None
        
        try:
            with open(gitignore_path, 'r', encoding='utf-8', errors='ignore') as f:
                patterns = f.read().splitlines()
            
            # Filter out empty lines and comments
            patterns = [
                line.strip() for line in patterns 
                if line.strip() and not line.strip().startswith('#')
            ]
            
            if not patterns:
                return None
                
            spec = pathspec.PathSpec.from_lines('gitwildmatch', patterns)
            logger.debug(f"Loaded {len(patterns)} gitignore patterns from {gitignore_path}")
            return spec
            
        except Exception as e:
            logger.warning(f"Failed to parse .gitignore file {gitignore_path}: {e}")
            return None
    
    def _get_gitignore_spec(self, directory: Path) -> Optional[PathSpecType]:
        """Get cached gitignore spec for a directory, loading if necessary.
        
        Args:
            directory: Directory to get gitignore spec for
            
        Returns:
            PathSpec object if available, None otherwise
        """
        if directory not in self._spec_cache:
            self._spec_cache[directory] = self._load_gitignore_spec(directory)
        
        return self._spec_cache[directory]
    
    def should_ignore(self, file_path: Union[str, Path]) -> bool:
        """Check if a file path should be ignored according to .gitignore rules.
        
        This method checks all .gitignore files in the directory hierarchy from
        the root path up to the file's directory.
        
        Args:
            file_path: Path to check (can be absolute or relative to root_path)
            
        Returns:
            True if the file should be ignored, False otherwise
        """
        if not self._enabled:
            return False
        
        path = Path(file_path)
        
        # Convert to absolute path if needed
        if not path.is_absolute():
            path = self.root_path / path
        
        try:
            # Get relative path from root for pattern matching
            rel_path = path.relative_to(self.root_path)
        except ValueError:
            # Path is outside root directory - don't ignore
            return False
        
        # Check gitignore files from root down to the file's directory
        current_dir = self.root_path
        rel_path_str = str(rel_path)
        
        # Walk up the directory hierarchy
        for part in rel_path.parts[:-1]:  # Exclude the filename itself
            current_dir = current_dir / part
            spec = self._get_gitignore_spec(current_dir)
            
            if spec and spec.match_file(rel_path_str):
                logger.debug(f"File {rel_path_str} matched gitignore pattern in {current_dir}")
                return True
        
        # Check root .gitignore
        root_spec = self._get_gitignore_spec(self.root_path)
        if root_spec and root_spec.match_file(rel_path_str):
            logger.debug(f"File {rel_path_str} matched gitignore pattern in root")
            return True
        
        return False
    
    def filter_paths(self, paths: List[Union[str, Path]]) -> List[Path]:
        """Filter a list of paths, removing those that should be ignored.
        
        Args:
            paths: List of paths to filter
            
        Returns:
            List of Path objects that should not be ignored
        """
        if not self._enabled:
            return [Path(p) for p in paths]
        
        filtered = []
        for path in paths:
            if not self.should_ignore(path):
                filtered.append(Path(path))
            else:
                logger.debug(f"Filtered out ignored path: {path}")
        
        return filtered
    
    def clear_cache(self):
        """Clear the internal cache of loaded .gitignore specs."""
        self._spec_cache.clear()


def create_gitignore_filter(root_path: Union[str, Path]) -> GitignoreFilter:
    """Create a GitignoreFilter for the given root path.
    
    Args:
        root_path: Root directory to search for .gitignore files
        
    Returns:
        GitignoreFilter instance
    """
    return GitignoreFilter(root_path)


def is_gitignore_available() -> bool:
    """Check if gitignore functionality is available.
    
    Returns:
        True if pathspec library is available, False otherwise
    """
    return pathspec is not None