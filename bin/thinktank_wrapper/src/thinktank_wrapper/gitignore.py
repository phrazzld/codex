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
        
        This implements Git's algorithm: check patterns from all applicable .gitignore files,
        applying them in order from root to deepest, with later patterns overriding earlier ones.
        
        Args:
            file_path: Path to check (can be absolute or relative to root_path)
            
        Returns:
            True if the file should be ignored, False otherwise
        """
        if not self._enabled:
            return False
        
        path = Path(file_path)
        
        # Convert to absolute path if needed and resolve to handle symlinks
        if not path.is_absolute():
            path = self.root_path / path
        
        # Resolve both paths to handle symlinks (e.g., /var -> /private/var on macOS)
        path = path.resolve()
        root_path = self.root_path.resolve()
        
        try:
            # Get relative path from root for pattern matching
            rel_path = path.relative_to(root_path)
        except ValueError:
            # Path is outside root directory - don't ignore
            return False
        
        # Build list of directories to check, from root to file's parent directory
        dirs_to_check = []
        current_dir = root_path
        dirs_to_check.append(current_dir)
        
        # Add each subdirectory in the path
        for part in rel_path.parts[:-1]:  # Exclude the filename itself
            current_dir = current_dir / part
            dirs_to_check.append(current_dir)
        
        # Collect all applicable patterns in order from root to deepest
        all_patterns = []
        
        for dir_path in dirs_to_check:
            gitignore_path = dir_path / ".gitignore"
            if not gitignore_path.exists() or not gitignore_path.is_file():
                continue
            
            try:
                with open(gitignore_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.read().splitlines()
                
                for line in lines:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    all_patterns.append((dir_path, line))
                        
            except Exception as e:
                logger.warning(f"Failed to read .gitignore file {gitignore_path}: {e}")
                continue
        
        # Separate directory patterns from file patterns and apply them properly
        # First determine if the file's directory path is ignored
        directory_ignored = False
        file_ignored = False
        
        # Get the directory part of the path (empty string if file is in root)
        if len(rel_path.parts) > 1:
            dir_parts = rel_path.parts[:-1]
        else:
            dir_parts = ()
        
        for dir_path, line in all_patterns:
            is_negation = line.startswith('!')
            pattern = line[1:] if is_negation else line
            is_dir_only_pattern = pattern.endswith('/')
            
            # Remove trailing slash for matching but remember it was a directory pattern
            if is_dir_only_pattern:
                pattern = pattern[:-1]
            
            # Compute path relative to this directory's .gitignore file
            if dir_path == root_path:
                # Root directory - use full relative path
                relative_match_path = str(rel_path)
                relative_dir_path = '/'.join(dir_parts) if dir_parts else ''
            else:
                # Subdirectory - use path relative to this directory
                try:
                    relative_match_path = str(path.relative_to(dir_path))
                    rel_to_dir = path.relative_to(dir_path)
                    if len(rel_to_dir.parts) > 1:
                        relative_dir_path = '/'.join(rel_to_dir.parts[:-1])
                    else:
                        relative_dir_path = ''
                except ValueError:
                    # Shouldn't happen, but skip if it does
                    continue
            
            try:
                # Test this specific pattern
                test_spec = pathspec.PathSpec.from_lines('gitwildmatch', [pattern])
                
                if is_dir_only_pattern:
                    # Directory-only pattern - check if it affects the directory containing this file
                    # Check all parent directories
                    path_parts = relative_match_path.split('/')
                    for i in range(len(path_parts)):
                        parent_path = '/'.join(path_parts[:i+1])
                        if test_spec.match_file(parent_path + "/"):
                            directory_ignored = not is_negation
                            logger.debug(f"Dir pattern '{line}' in {dir_path} matched parent {parent_path}/, dir_ignored={directory_ignored}")
                            break
                else:
                    # Regular file pattern - check if it matches this specific file
                    matches_file = test_spec.match_file(relative_match_path)
                    matches_dir = path.is_dir() and test_spec.match_file(relative_match_path + "/")
                    
                    if matches_file or matches_dir:
                        file_ignored = not is_negation
                        logger.debug(f"File pattern '{line}' in {dir_path} matched {relative_match_path}, file_ignored={file_ignored}")
                    
            except Exception as e:
                logger.debug(f"Failed to test pattern '{line}': {e}")
                continue
        
        # A file is ignored if:
        # 1. Its containing directory is ignored by directory patterns, OR
        # 2. It matches file ignore patterns (regardless of directory status)
        should_ignore = directory_ignored or file_ignored
        
        logger.debug(f"Final decision for {rel_path}: directory_ignored={directory_ignored}, file_ignored={file_ignored}, should_ignore={should_ignore}")
        
        return should_ignore
    
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