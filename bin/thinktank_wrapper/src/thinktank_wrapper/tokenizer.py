"""Tokenization module for thinktank-wrapper.

This module provides functionality for counting tokens across multiple LLM providers
to enable intelligent model selection based on context size.
"""

import logging
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

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


class TokenCounter:
    """Provides token counting functionality for multiple LLM providers."""
    
    def __init__(self, provider: str = "default"):
        """Initialize the TokenCounter with a specific provider.
        
        Args:
            provider: The LLM provider name (openai, anthropic, google, openrouter)
        """
        self.provider = provider.lower()
        self.base_ratio = TOKEN_CHAR_RATIOS.get(self.provider, TOKEN_CHAR_RATIOS["default"])
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
    
    def __init__(self):
        """Initialize counters for all supported providers."""
        self.counters = {
            provider: TokenCounter(provider)
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