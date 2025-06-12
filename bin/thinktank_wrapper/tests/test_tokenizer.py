"""Tests for the tokenizer module."""

import os
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from thinktank_wrapper.tokenizer import TokenCounter, MultiProviderTokenCounter


@pytest.fixture
def temp_files(tmp_path):
    """Create temporary test files with known content."""
    files = {}
    
    # Python file
    py_file = tmp_path / "test.py"
    py_content = "def hello():\n    return 'world'"  # 31 chars
    py_file.write_text(py_content)
    files['python'] = (py_file, py_content)
    
    # Markdown file
    md_file = tmp_path / "test.md"
    md_content = "# Test\n\nThis is a test document."  # 33 chars
    md_file.write_text(md_content)
    files['markdown'] = (md_file, md_content)
    
    # JSON file
    json_file = tmp_path / "test.json"
    json_content = '{"key": "value", "number": 42}'  # 31 chars
    json_file.write_text(json_content)
    files['json'] = (json_file, json_content)
    
    return files


class TestTokenCounter:
    """Test the TokenCounter class."""
    
    def test_init_default_provider(self):
        """Test initialization with default provider."""
        counter = TokenCounter()
        assert counter.provider == "default"
        assert counter.base_ratio == 0.27
    
    def test_init_openai_provider(self):
        """Test initialization with OpenAI provider."""
        counter = TokenCounter("openai")
        assert counter.provider == "openai"
        assert counter.base_ratio == 0.25
    
    def test_count_text_tokens_empty(self):
        """Test counting tokens in empty text."""
        counter = TokenCounter()
        assert counter.count_text_tokens("") == 0
        assert counter.count_text_tokens(None) == 0
    
    def test_count_text_tokens_approximation(self):
        """Test character-based token approximation."""
        counter = TokenCounter("openai")
        # 100 chars * 0.25 = 25 tokens
        text = "a" * 100
        assert counter.count_text_tokens(text) == 25
    
    def test_count_file_tokens(self, temp_files):
        """Test counting tokens in files."""
        counter = TokenCounter("openai")
        
        # Test Python file (31 chars * 0.25 * 1.15 adjustment = ~8.9 = 8 tokens)
        py_file, _ = temp_files['python']
        tokens, error = counter.count_file_tokens(py_file)
        assert error is None
        assert tokens == 8
        
        # Test Markdown file (33 chars * 0.25 * 0.95 adjustment = ~7.8 = 7 tokens)
        md_file, _ = temp_files['markdown']
        tokens, error = counter.count_file_tokens(md_file)
        assert error is None
        assert tokens == 7
        
        # Test JSON file (31 chars * 0.25 * 1.20 adjustment = ~9.3 = 9 tokens)
        json_file, _ = temp_files['json']
        tokens, error = counter.count_file_tokens(json_file)
        assert error is None
        assert tokens == 9
    
    def test_count_file_tokens_not_found(self):
        """Test counting tokens in non-existent file."""
        counter = TokenCounter()
        tokens, error = counter.count_file_tokens("/non/existent/file.txt")
        assert tokens == 0
        assert "File not found" in error
    
    def test_count_directory_tokens(self, temp_files):
        """Test counting tokens in directory."""
        counter = TokenCounter("openai")
        tmp_path = next(iter(temp_files.values()))[0].parent
        
        # Count all files
        tokens, errors = counter.count_directory_tokens(tmp_path)
        assert len(errors) == 0
        # Total should be sum of all files: 8 + 7 + 9 = 24
        assert tokens == 24
    
    def test_count_directory_tokens_with_extension_filter(self, temp_files):
        """Test counting tokens with extension filter."""
        counter = TokenCounter("openai")
        tmp_path = next(iter(temp_files.values()))[0].parent
        
        # Count only Python files
        tokens, errors = counter.count_directory_tokens(tmp_path, extensions=['.py'])
        assert len(errors) == 0
        assert tokens == 8  # Only the Python file
    
    def test_estimate_model_tokens_mixed_paths(self, temp_files):
        """Test estimating tokens for mixed file and directory paths."""
        counter = TokenCounter("openai")
        py_file, _ = temp_files['python']
        tmp_path = py_file.parent
        
        # Create a subdirectory with another file
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        sub_file = subdir / "sub.txt"
        sub_file.write_text("test content")  # 12 chars * 0.25 = 3 tokens
        
        # Estimate tokens for file + directory
        paths = [str(py_file), str(subdir)]
        tokens, errors = counter.estimate_model_tokens(paths)
        assert len(errors) == 0
        assert tokens == 8 + 3  # py_file + sub_file


class TestMultiProviderTokenCounter:
    """Test the MultiProviderTokenCounter class."""
    
    def test_init(self):
        """Test initialization."""
        multi_counter = MultiProviderTokenCounter()
        assert len(multi_counter.counters) == 4
        assert "openai" in multi_counter.counters
        assert "anthropic" in multi_counter.counters
        assert "google" in multi_counter.counters
        assert "openrouter" in multi_counter.counters
    
    def test_count_all_providers(self, temp_files):
        """Test counting tokens for all providers."""
        multi_counter = MultiProviderTokenCounter()
        py_file, _ = temp_files['python']
        
        results = multi_counter.count_all_providers([py_file])
        
        # Check results structure
        assert len(results) == 4
        for provider, (tokens, errors) in results.items():
            assert isinstance(tokens, int)
            assert isinstance(errors, list)
            assert len(errors) == 0
        
        # OpenAI should have specific token count
        assert results["openai"][0] == 8
        
        # Google should have slightly different count due to different ratio
        # 31 chars * 0.23 * 1.15 = ~8.2 = 8 tokens (same due to rounding)
        assert results["google"][0] == 8
    
    def test_get_max_tokens(self, temp_files):
        """Test getting maximum token count across providers."""
        multi_counter = MultiProviderTokenCounter()
        py_file, _ = temp_files['python']
        
        max_tokens = multi_counter.get_max_tokens([py_file])
        assert max_tokens == 8  # All providers should be close


@patch.dict(os.environ, {"ENABLE_TOKEN_COUNTING": "false"})
def test_token_counting_disabled_by_env():
    """Test that token counting can be disabled by environment variable."""
    from thinktank_wrapper import config
    # Need to reload to pick up env change
    import importlib
    importlib.reload(config)
    assert config.ENABLE_TOKEN_COUNTING is False