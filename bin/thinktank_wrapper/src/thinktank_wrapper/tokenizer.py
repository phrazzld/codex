"""Tokenization module for thinktank-wrapper.

This module provides functionality for counting tokens across multiple LLM providers
to enable intelligent model selection based on context size.
"""

import logging
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

try:
    import magic
    MAGIC_AVAILABLE = True
except ImportError:
    magic = None
    MAGIC_AVAILABLE = False

from .gitignore import GitignoreFilter

logger = logging.getLogger(__name__)

# Token approximation ratios based on empirical analysis
# These are conservative estimates to ensure we don't exceed context windows
TOKEN_CHAR_RATIOS = {
    "openai": 0.25,      # ~4 chars per token (GPT models)
    "anthropic": 0.24,   # Similar to OpenAI, slightly more conservative
    "google": 0.23,      # Gemini models tend to have slightly different tokenization
    "openrouter": 0.25,  # Use OpenAI ratio as default for various models
    "default": 0.27      # Conservative default for unknown providers
}

# File type specific adjustments (multipliers for base ratio)
FILE_TYPE_ADJUSTMENTS = {
    ".py": 1.15,      # Code tends to have more tokens per char
    ".js": 1.15,      # Similar to Python
    ".ts": 1.15,      # TypeScript similar to JS
    ".go": 1.12,      # Go is slightly more concise
    ".rs": 1.12,      # Rust similar to Go
    ".java": 1.18,    # Java tends to be verbose
    ".cpp": 1.15,     # C++ similar to other code
    ".c": 1.10,       # C is more concise
    ".md": 0.95,      # Markdown has less token density
    ".txt": 1.0,      # Plain text baseline
    ".json": 1.20,    # JSON structure adds tokens
    ".yaml": 1.10,    # YAML is more readable than JSON
    ".xml": 1.25,     # XML is verbose
    ".html": 1.20,    # HTML similar to XML
}

# Known binary file extensions to skip during tokenization
# These are file types that should never be processed as text
BINARY_EXTENSIONS = {
    # Executables and libraries
    '.exe', '.dll', '.so', '.dylib', '.a', '.lib', '.o', '.obj',
    # Archives and compressed files
    '.zip', '.tar', '.gz', '.bz2', '.xz', '.7z', '.rar', '.jar', '.war', '.ear',
    # Images
    '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.ico', '.svg', '.webp',
    # Audio and video
    '.mp3', '.wav', '.flac', '.aac', '.ogg', '.mp4', '.avi', '.mov', '.mkv', '.webm',
    # Documents and fonts
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.ttf', '.otf', '.woff', '.woff2', '.eot',
    # Database files
    '.db', '.sqlite', '.sqlite3', '.mdb',
    # Compiled Python
    '.pyc', '.pyo', '.pyd',
    # Java compiled
    '.class',
    # Other binary formats
    '.bin', '.dat', '.dump', '.img', '.iso', '.dmg',
}


def is_binary_by_extension(file_path: Union[str, Path]) -> bool:
    """Check if a file is likely binary based on its extension.
    
    Args:
        file_path: Path to the file to check
        
    Returns:
        True if the file extension indicates it's binary, False otherwise
    """
    path = Path(file_path)
    return path.suffix.lower() in BINARY_EXTENSIONS


def is_binary_by_mime_type(file_path: Union[str, Path]) -> Optional[bool]:
    """Check if a file is binary based on its MIME type using python-magic.
    
    This function provides content-based MIME type detection as a fallback
    when extension and null-byte detection are insufficient.
    
    Args:
        file_path: Path to the file to check
        
    Returns:
        True if MIME type indicates binary, False if text, None if undetermined or unavailable
    """
    if not MAGIC_AVAILABLE:
        logger.debug("python-magic not available, skipping MIME type detection")
        return None
    
    path = Path(file_path)
    
    if not path.exists() or not path.is_file():
        return None
    
    try:
        # Get MIME type of the file
        mime_type = magic.from_file(str(path), mime=True)
        
        if not mime_type:
            return None
        
        # Text MIME types - definitely not binary
        text_types = {
            'text/',           # text/plain, text/html, text/csv, etc.
            'application/json',
            'application/xml',
            'application/javascript',
            'application/x-yaml',
            'application/x-sh',
            'application/x-python',
            'application/x-perl',
            'application/x-ruby',
        }
        
        # Check if it's a text type
        mime_lower = mime_type.lower()
        if any(mime_lower.startswith(text_type) for text_type in text_types):
            logger.debug(f"File {path.name} detected as text via MIME type: {mime_type}")
            return False
        
        # Binary MIME types - definitely binary
        binary_types = {
            'application/octet-stream',  # Generic binary
            'application/pdf',
            'application/zip',
            'application/gzip',
            'application/x-tar',
            'application/x-executable',
            'application/x-sharedlib',
            'application/x-archive',
            'image/',                    # image/png, image/jpeg, etc.
            'audio/',                    # audio/mp3, audio/wav, etc.  
            'video/',                    # video/mp4, video/avi, etc.
            'font/',                     # font/ttf, font/woff, etc.
        }
        
        # Check if it's a binary type
        if any(mime_lower.startswith(binary_type) for binary_type in binary_types):
            logger.debug(f"File {path.name} detected as binary via MIME type: {mime_type}")
            return True
        
        # For other types, we're uncertain
        logger.debug(f"File {path.name} has uncertain MIME type: {mime_type}")
        return None
        
    except Exception as e:
        logger.debug(f"MIME type detection failed for {path.name}: {e}")
        return None


def is_binary_file(file_path: Union[str, Path], chunk_size: int = 8192, use_mime_type: bool = True) -> bool:
    """Check if a file is binary using a three-stage approach for accuracy.
    
    This function uses a three-stage approach for efficiency and accuracy:
    1. Fast extension-based check for known binary types
    2. Content analysis (null byte detection) for unknown extensions  
    3. MIME type detection as fallback (optional, requires python-magic)
    
    Args:
        file_path: Path to the file to check
        chunk_size: Number of bytes to read for content detection (default 8KB)
        use_mime_type: Whether to use MIME type detection as fallback (default True)
        
    Returns:
        True if the file appears to be binary, False otherwise
    """
    # Stage 1: Fast path - check extension first
    if is_binary_by_extension(file_path):
        return True
    
    # Stage 2: Content analysis - analyze file content for unknown extensions
    path = Path(file_path)
    
    try:
        with open(path, 'rb') as f:
            chunk = f.read(chunk_size)
            # Check for null bytes which are common in binary files
            if b'\x00' in chunk:
                return True
    except (OSError, IOError):
        # If we can't read the file, assume it's not binary
        # This will let the normal file reading logic handle the error
        return False
    
    # Stage 3: MIME type detection fallback (optional)
    if use_mime_type:
        mime_result = is_binary_by_mime_type(file_path)
        if mime_result is not None:
            return mime_result
    
    # If all detection methods are inconclusive, assume it's text
    return False


class TokenCounter:
    """Provides token counting functionality for multiple LLM providers."""
    
    def __init__(self, provider: str = "default", gitignore_enabled: bool = True):
        """Initialize the TokenCounter with a specific provider.
        
        Args:
            provider: The LLM provider name (openai, anthropic, google, openrouter)
            gitignore_enabled: Whether to respect .gitignore rules when processing directories
        """
        self.provider = provider.lower()
        self.base_ratio = TOKEN_CHAR_RATIOS.get(self.provider, TOKEN_CHAR_RATIOS["default"])
        self.gitignore_enabled = gitignore_enabled
        self._tiktoken = None
        self._tiktoken_encoding = None
        
        # Try to load tiktoken for more accurate OpenAI counting
        if self.provider == "openai":
            try:
                import tiktoken
                self._tiktoken = tiktoken
                self._tiktoken_encoding = tiktoken.get_encoding("cl100k_base")
                logger.debug("Loaded tiktoken for accurate OpenAI token counting")
            except ImportError:
                logger.debug("tiktoken not available, using character-based approximation")
    
    def count_text_tokens(self, text: str) -> int:
        """Count tokens in a text string.
        
        Args:
            text: The text to count tokens for
            
        Returns:
            Estimated token count
        """
        if not text:
            return 0
            
        # Use tiktoken for OpenAI if available
        if self.provider == "openai" and self._tiktoken_encoding:
            try:
                return len(self._tiktoken_encoding.encode(text))
            except Exception as e:
                logger.warning(f"tiktoken encoding failed, falling back to approximation: {e}")
        
        # Character-based approximation
        return int(len(text) * self.base_ratio)
    
    def count_file_tokens(self, file_path: Union[str, Path]) -> Tuple[int, Optional[str]]:
        """Count tokens in a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Tuple of (token_count, error_message)
        """
        path = Path(file_path)
        
        if not path.exists():
            return 0, f"File not found: {file_path}"
        
        if not path.is_file():
            return 0, f"Not a file: {file_path}"
        
        # Check if file is binary before attempting to read as text
        if is_binary_file(path):
            logger.debug(f"Skipping binary file: {path.name}")
            return 0, None
        
        try:
            # Read file content
            content = path.read_text(encoding='utf-8', errors='ignore')
            
            # Get base token count
            base_tokens = self.count_text_tokens(content)
            
            # Apply file type adjustment
            suffix = path.suffix.lower()
            adjustment = FILE_TYPE_ADJUSTMENTS.get(suffix, 1.0)
            adjusted_tokens = int(base_tokens * adjustment)
            
            logger.debug(f"File {path.name}: {len(content)} chars, "
                        f"{base_tokens} base tokens, {adjusted_tokens} adjusted tokens "
                        f"(adjustment: {adjustment})")
            
            return adjusted_tokens, None
            
        except Exception as e:
            return 0, f"Error reading file {file_path}: {str(e)}"
    
    def count_directory_tokens(self, dir_path: Union[str, Path], 
                             recursive: bool = True,
                             extensions: Optional[List[str]] = None) -> Tuple[int, List[str]]:
        """Count tokens in all files in a directory.
        
        Args:
            dir_path: Path to the directory
            recursive: Whether to search recursively
            extensions: List of file extensions to include (e.g., ['.py', '.js'])
            
        Returns:
            Tuple of (total_token_count, list_of_errors)
        """
        path = Path(dir_path)
        
        if not path.exists():
            return 0, [f"Directory not found: {dir_path}"]
        
        if not path.is_dir():
            return 0, [f"Not a directory: {dir_path}"]
        
        total_tokens = 0
        errors = []
        
        # Set up gitignore filtering if enabled
        gitignore_filter: Optional[GitignoreFilter] = None
        if self.gitignore_enabled:
            try:
                # Use the directory being processed as the root for gitignore
                gitignore_filter = GitignoreFilter(path)
                if not gitignore_filter.is_enabled():
                    logger.debug("Gitignore filtering requested but pathspec not available")
                    gitignore_filter = None
            except Exception as e:
                logger.warning(f"Failed to initialize gitignore filtering: {e}")
                gitignore_filter = None
        
        # Determine file pattern
        if recursive:
            pattern = "**/*"
        else:
            pattern = "*"
        
        # Process files
        for file_path in path.glob(pattern):
            if not file_path.is_file():
                continue
                
            # Check extension filter
            if extensions and file_path.suffix.lower() not in extensions:
                continue
            
            # Apply gitignore filtering if enabled
            if gitignore_filter and gitignore_filter.should_ignore(file_path):
                logger.debug(f"Gitignore filtered out file: {file_path}")
                continue
            
            tokens, error = self.count_file_tokens(file_path)
            total_tokens += tokens
            
            if error:
                errors.append(error)
        
        return total_tokens, errors
    
    def estimate_model_tokens(self, paths: List[Union[str, Path]]) -> Tuple[int, List[str]]:
        """Estimate total tokens for a list of file/directory paths.
        
        Args:
            paths: List of file or directory paths
            
        Returns:
            Tuple of (total_token_count, list_of_errors)
        """
        total_tokens = 0
        all_errors = []
        
        for path_str in paths:
            path = Path(path_str)
            
            if path.is_file():
                tokens, error = self.count_file_tokens(path)
                total_tokens += tokens
                if error:
                    all_errors.append(error)
                    
            elif path.is_dir():
                tokens, errors = self.count_directory_tokens(path)
                total_tokens += tokens
                all_errors.extend(errors)
                
            else:
                all_errors.append(f"Invalid path: {path_str}")
        
        return total_tokens, all_errors


class MultiProviderTokenCounter:
    """Manages token counting across multiple providers for comparison."""
    
    def __init__(self, gitignore_enabled: bool = True):
        """Initialize counters for all supported providers.
        
        Args:
            gitignore_enabled: Whether to respect .gitignore rules when processing directories
        """
        self.counters = {
            provider: TokenCounter(provider, gitignore_enabled=gitignore_enabled)
            for provider in ["openai", "anthropic", "google", "openrouter"]
        }
    
    def count_all_providers(self, paths: List[Union[str, Path]]) -> Dict[str, Tuple[int, List[str]]]:
        """Count tokens for all providers.
        
        Args:
            paths: List of file or directory paths
            
        Returns:
            Dictionary mapping provider names to (token_count, errors) tuples
        """
        results = {}
        
        for provider, counter in self.counters.items():
            tokens, errors = counter.estimate_model_tokens(paths)
            results[provider] = (tokens, errors)
            
        return results
    
    def get_max_tokens(self, paths: List[Union[str, Path]]) -> int:
        """Get the maximum token count across all providers.
        
        Args:
            paths: List of file or directory paths
            
        Returns:
            Maximum token count among all providers
        """
        results = self.count_all_providers(paths)
        return max(tokens for tokens, _ in results.values())