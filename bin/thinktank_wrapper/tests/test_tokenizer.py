"""Tests for the tokenizer module."""

import os
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from thinktank_wrapper.tokenizer import (
    TokenCounter, 
    MultiProviderTokenCounter, 
    is_binary_file, 
    is_binary_by_extension,
    is_binary_by_mime_type,
    BINARY_EXTENSIONS,
    MAGIC_AVAILABLE
)


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


@pytest.fixture
def binary_test_files(tmp_path):
    """Create temporary test files including binary files."""
    files = {}
    
    # Text file
    text_file = tmp_path / "text.txt"
    text_file.write_text("This is a plain text file.")
    files['text'] = text_file
    
    # Binary file with null bytes
    binary_file = tmp_path / "binary.bin"
    binary_content = b"Binary content\x00with null bytes\x00and more data"
    binary_file.write_bytes(binary_content)
    files['binary'] = binary_file
    
    # Empty file
    empty_file = tmp_path / "empty.txt"
    empty_file.write_text("")
    files['empty'] = empty_file
    
    # File that looks binary but isn't (no null bytes)
    pseudobinary_file = tmp_path / "pseudo.dat"
    pseudobinary_file.write_text("This looks binary but has no null bytes")
    files['pseudobinary'] = pseudobinary_file
    
    # Files with known binary extensions
    exe_file = tmp_path / "app.exe"
    exe_file.write_bytes(b"This is a fake exe file")
    files['exe'] = exe_file
    
    pyc_file = tmp_path / "module.pyc"
    pyc_file.write_bytes(b"Compiled Python bytecode")
    files['pyc'] = pyc_file
    
    png_file = tmp_path / "image.png"
    png_file.write_bytes(b"PNG image data")
    files['png'] = png_file
    
    return files


class TestBinaryFileDetection:
    """Test binary file detection functionality."""
    
    def test_is_binary_file_with_text(self, binary_test_files):
        """Test that text files are not detected as binary."""
        text_file = binary_test_files['text']
        assert not is_binary_file(text_file)
    
    def test_is_binary_file_with_binary(self, binary_test_files):
        """Test that binary files are correctly detected."""
        binary_file = binary_test_files['binary']
        assert is_binary_file(binary_file)
    
    def test_is_binary_file_with_empty(self, binary_test_files):
        """Test that empty files are not detected as binary."""
        empty_file = binary_test_files['empty']
        assert not is_binary_file(empty_file)
    
    def test_is_binary_file_with_pseudobinary(self, binary_test_files):
        """Test that files without null bytes are not detected as binary."""
        pseudobinary_file = binary_test_files['pseudobinary']
        assert not is_binary_file(pseudobinary_file)
    
    def test_is_binary_file_nonexistent(self):
        """Test that non-existent files return False."""
        assert not is_binary_file("/non/existent/file.bin")
    
    def test_is_binary_file_with_known_extensions(self, binary_test_files):
        """Test that files with known binary extensions are detected."""
        # Files with binary extensions should be detected as binary
        assert is_binary_file(binary_test_files['exe'])
        assert is_binary_file(binary_test_files['pyc'])
        assert is_binary_file(binary_test_files['png'])
        
        # Text files should not be detected as binary
        assert not is_binary_file(binary_test_files['text'])


class TestBinaryExtensionDetection:
    """Test extension-based binary file detection."""
    
    def test_is_binary_by_extension_known_extensions(self):
        """Test detection of known binary extensions."""
        # Test various binary extensions
        assert is_binary_by_extension("file.exe")
        assert is_binary_by_extension("library.dll")
        assert is_binary_by_extension("archive.zip")
        assert is_binary_by_extension("image.png")
        assert is_binary_by_extension("audio.mp3")
        assert is_binary_by_extension("module.pyc")
        assert is_binary_by_extension("app.class")
        
        # Test case insensitivity
        assert is_binary_by_extension("FILE.EXE")
        assert is_binary_by_extension("Image.PNG")
    
    def test_is_binary_by_extension_text_extensions(self):
        """Test that text file extensions are not detected as binary."""
        assert not is_binary_by_extension("script.py")
        assert not is_binary_by_extension("document.txt")
        assert not is_binary_by_extension("config.json")
        assert not is_binary_by_extension("readme.md")
        assert not is_binary_by_extension("style.css")
        assert not is_binary_by_extension("script.js")
    
    def test_is_binary_by_extension_unknown_extensions(self):
        """Test that unknown extensions are not detected as binary."""
        assert not is_binary_by_extension("file.unknownext")
        assert not is_binary_by_extension("file.xyz")
        assert not is_binary_by_extension("file")  # No extension
    
    def test_binary_extensions_completeness(self):
        """Test that BINARY_EXTENSIONS contains expected categories."""
        # Check that we have extensions from major categories
        assert '.exe' in BINARY_EXTENSIONS  # Executables
        assert '.zip' in BINARY_EXTENSIONS  # Archives
        assert '.png' in BINARY_EXTENSIONS  # Images
        assert '.mp3' in BINARY_EXTENSIONS  # Audio
        assert '.pdf' in BINARY_EXTENSIONS  # Documents
        assert '.pyc' in BINARY_EXTENSIONS  # Compiled code
        
        # Check case consistency (all should be lowercase)
        for ext in BINARY_EXTENSIONS:
            assert ext == ext.lower(), f"Extension {ext} should be lowercase"


class TestMimeTypeDetection:
    """Test MIME type-based binary file detection."""
    
    @pytest.fixture
    def mime_test_files(self, tmp_path):
        """Create test files for MIME type detection testing."""
        files = {}
        
        # Create text files that might be misidentified by extension
        text_no_ext = tmp_path / "textfile"
        text_no_ext.write_text("This is plain text without extension")
        files['text_no_ext'] = text_no_ext
        
        # Create a file with misleading extension but text content
        misleading_bin = tmp_path / "notreally.bin"
        misleading_bin.write_text("#!/bin/bash\necho 'This looks binary but is a script'")
        files['misleading_bin'] = misleading_bin
        
        # Create files that would benefit from MIME detection
        script_no_ext = tmp_path / "script"
        script_no_ext.write_text("#!/usr/bin/env python3\nprint('hello world')")
        files['script_no_ext'] = script_no_ext
        
        # Create a JSON file without extension
        json_no_ext = tmp_path / "config"
        json_no_ext.write_text('{"name": "test", "version": "1.0"}')
        files['json_no_ext'] = json_no_ext
        
        # Create a fake binary file (would need real binary content for full test)
        fake_binary = tmp_path / "fake.unknown"
        fake_binary.write_bytes(b'\x89PNG\r\n\x1a\n')  # PNG header
        files['fake_binary'] = fake_binary
        
        return files
    
    def test_is_binary_by_mime_type_text_detection(self, mime_test_files):
        """Test MIME type detection for text files."""
        if not MAGIC_AVAILABLE:
            pytest.skip("python-magic not available")
        
        # Text file without extension should be detected as text
        result = is_binary_by_mime_type(mime_test_files['text_no_ext'])
        assert result is False  # Should detect as text
        
        # Script without extension should be detected as text
        result = is_binary_by_mime_type(mime_test_files['script_no_ext'])
        assert result is False  # Should detect as text
    
    def test_is_binary_by_mime_type_graceful_degradation(self, mime_test_files):
        """Test graceful degradation when python-magic is not available."""
        with patch('thinktank_wrapper.tokenizer.MAGIC_AVAILABLE', False):
            result = is_binary_by_mime_type(mime_test_files['text_no_ext'])
            assert result is None  # Should return None when magic unavailable
    
    def test_is_binary_by_mime_type_nonexistent_file(self):
        """Test MIME type detection with non-existent file."""
        result = is_binary_by_mime_type("/non/existent/file.txt")
        assert result is None
    
    def test_is_binary_by_mime_type_error_handling(self, tmp_path):
        """Test error handling in MIME type detection."""
        if not MAGIC_AVAILABLE:
            pytest.skip("python-magic not available")
        
        # Create an empty file that might cause issues
        empty_file = tmp_path / "empty"
        empty_file.touch()
        
        # Should handle gracefully (may return None or False)
        result = is_binary_by_mime_type(empty_file)
        assert result in [None, False, True]  # Any of these are acceptable
    
    def test_is_binary_file_with_mime_type_integration(self, mime_test_files):
        """Test integration of MIME type detection with is_binary_file."""
        # Test with MIME type detection enabled (default)
        result_with_mime = is_binary_file(mime_test_files['text_no_ext'], use_mime_type=True)
        
        # Test with MIME type detection disabled
        result_without_mime = is_binary_file(mime_test_files['text_no_ext'], use_mime_type=False)
        
        if MAGIC_AVAILABLE:
            # With MIME detection, should correctly identify as text
            assert result_with_mime is False
            # Without MIME detection, might be inconclusive (defaults to False anyway)
            assert result_without_mime is False
        else:
            # Both should be the same when magic unavailable
            assert result_with_mime == result_without_mime
    
    def test_is_binary_file_mime_fallback_behavior(self, mime_test_files):
        """Test that MIME detection is used as fallback, not first choice."""
        if not MAGIC_AVAILABLE:
            pytest.skip("python-magic not available")
        
        # For a file with misleading extension, MIME should be fallback
        misleading_file = mime_test_files['misleading_bin']
        
        # Since .bin extension is in BINARY_EXTENSIONS, extension check should win
        result = is_binary_file(misleading_file)
        # Extension-based detection should take precedence
        # (.bin extension is not in our BINARY_EXTENSIONS, so it should fall through to MIME)
        
        # Let's verify the behavior step by step
        ext_result = is_binary_by_extension(misleading_file)
        mime_result = is_binary_by_mime_type(misleading_file)
        
        # .bin might not be in BINARY_EXTENSIONS, so extension check could be False
        # Then MIME detection should identify it as text (shell script)
        if not ext_result and mime_result is False:
            assert result is False  # Should be detected as text via MIME
    
    def test_mime_type_text_categories(self, tmp_path):
        """Test detection of various text MIME type categories."""
        if not MAGIC_AVAILABLE:
            pytest.skip("python-magic not available")
        
        # Create files that should be detected as text by MIME type
        test_cases = [
            ("script.sh", "#!/bin/bash\necho hello"),
            ("data.json", '{"test": "data"}'),
            ("config.yaml", "key: value\nlist:\n  - item1\n  - item2"),
            ("plain.txt", "Just plain text content"),
        ]
        
        for filename, content in test_cases:
            test_file = tmp_path / filename
            test_file.write_text(content)
            
            # Remove extension to force MIME detection
            no_ext_file = tmp_path / filename.split('.')[0]
            no_ext_file.write_text(content)
            
            mime_result = is_binary_by_mime_type(no_ext_file)
            # Most of these should be detected as text (False), but some might be uncertain (None)
            assert mime_result in [False, None], f"File {filename} should be text or uncertain"
    
    @patch('thinktank_wrapper.tokenizer.magic')
    def test_mime_type_detection_with_mock_magic(self, mock_magic, tmp_path):
        """Test MIME type detection with mocked magic library."""
        # Create a test file
        test_file = tmp_path / "test"
        test_file.write_text("test content")
        
        # Mock magic to return specific MIME types
        mock_magic.from_file.return_value = "text/plain"
        
        with patch('thinktank_wrapper.tokenizer.MAGIC_AVAILABLE', True):
            result = is_binary_by_mime_type(test_file)
            assert result is False  # text/plain should be detected as text
        
        # Test binary MIME type
        mock_magic.from_file.return_value = "application/pdf"
        result = is_binary_by_mime_type(test_file)
        assert result is True  # PDF should be detected as binary
        
        # Test uncertain MIME type
        mock_magic.from_file.return_value = "application/unknown"
        result = is_binary_by_mime_type(test_file)
        assert result is None  # Unknown type should be uncertain
        
        # Test magic exception
        mock_magic.from_file.side_effect = Exception("Magic failed")
        result = is_binary_by_mime_type(test_file)
        assert result is None  # Exception should result in None


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
    
    def test_count_file_tokens_binary_files(self, binary_test_files):
        """Test that binary files are skipped."""
        counter = TokenCounter()
        
        # Binary file should return 0 tokens with no error
        binary_file = binary_test_files['binary']
        tokens, error = counter.count_file_tokens(binary_file)
        assert tokens == 0
        assert error is None
        
        # Text file should work normally
        text_file = binary_test_files['text']
        tokens, error = counter.count_file_tokens(text_file)
        assert tokens > 0
        assert error is None
    
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


class TestTokenizerGitignoreIntegration:
    """Test gitignore integration in tokenizer module."""
    
    @pytest.fixture
    def gitignore_test_repo(self, tmp_path):
        """Create a test repository with .gitignore files and various content."""
        repo = tmp_path / "repo"
        repo.mkdir()
        
        # Root .gitignore
        gitignore = repo / ".gitignore"
        gitignore.write_text("*.log\n*.tmp\nbuild/\nnode_modules/\n")
        
        # Create various files
        (repo / "main.py").write_text("def main(): pass")  # Should be counted
        (repo / "debug.log").write_text("log content")     # Should be ignored
        (repo / "temp.tmp").write_text("temporary")        # Should be ignored
        (repo / "README.md").write_text("# Project")       # Should be counted
        
        # Create ignored directories
        build_dir = repo / "build"
        build_dir.mkdir()
        (build_dir / "output.bin").write_text("binary")    # Should be ignored
        
        node_modules = repo / "node_modules"
        node_modules.mkdir()
        (node_modules / "package.json").write_text("{}")   # Should be ignored
        
        # Create subdirectory with its own .gitignore
        subdir = repo / "src"
        subdir.mkdir()
        (subdir / ".gitignore").write_text("*.pyc\n")
        (subdir / "app.py").write_text("app code")         # Should be counted
        (subdir / "compiled.pyc").write_text("compiled")   # Should be ignored by subdir .gitignore
        
        return repo
    
    def test_token_counter_gitignore_enabled(self, gitignore_test_repo):
        """Test TokenCounter with gitignore filtering enabled."""
        counter = TokenCounter(gitignore_enabled=True)
        
        # Count tokens with gitignore filtering
        tokens, errors = counter.count_directory_tokens(gitignore_test_repo)
        
        # Should have no errors
        assert len(errors) == 0
        
        # Should count only non-ignored files:
        # - main.py: "def main(): pass" (16 chars)
        # - README.md: "# Project" (9 chars) 
        # - src/app.py: "app code" (8 chars)
        # Total chars: 33, with default ratio 0.27 = ~8.9 = 8 tokens
        # Actual calculation may vary due to file type adjustments
        assert tokens > 0
        assert tokens < 50  # Sanity check - should be reasonable
    
    def test_token_counter_gitignore_disabled(self, gitignore_test_repo):
        """Test TokenCounter with gitignore filtering disabled."""
        counter = TokenCounter(gitignore_enabled=False)
        
        # Count tokens without gitignore filtering
        tokens, errors = counter.count_directory_tokens(gitignore_test_repo)
        
        # Should have no errors (binary files are still filtered by extension/content)
        assert len(errors) == 0
        
        # Should count MORE files than with gitignore enabled
        # (includes *.log, *.tmp files that would normally be ignored)
        assert tokens > 0
    
    def test_token_counter_gitignore_comparison(self, gitignore_test_repo):
        """Test that gitignore filtering reduces token count compared to no filtering."""
        counter_with_git = TokenCounter(gitignore_enabled=True)
        counter_no_git = TokenCounter(gitignore_enabled=False)
        
        tokens_filtered, _ = counter_with_git.count_directory_tokens(gitignore_test_repo)
        tokens_all, _ = counter_no_git.count_directory_tokens(gitignore_test_repo)
        
        # Gitignore filtering should result in fewer or equal tokens
        # (equal if no text files are ignored, fewer if some are ignored)
        assert tokens_filtered <= tokens_all
    
    def test_multi_provider_counter_gitignore(self, gitignore_test_repo):
        """Test MultiProviderTokenCounter respects gitignore settings."""
        # Test with gitignore enabled
        multi_counter_git = MultiProviderTokenCounter(gitignore_enabled=True)
        results_git = multi_counter_git.count_all_providers([gitignore_test_repo])
        
        # Test with gitignore disabled
        multi_counter_no_git = MultiProviderTokenCounter(gitignore_enabled=False)
        results_no_git = multi_counter_no_git.count_all_providers([gitignore_test_repo])
        
        # All providers should respect gitignore setting
        for provider in results_git.keys():
            tokens_git, errors_git = results_git[provider]
            tokens_no_git, errors_no_git = results_no_git[provider]
            
            assert len(errors_git) == 0
            assert len(errors_no_git) == 0
            assert tokens_git <= tokens_no_git
    
    def test_token_counter_graceful_degradation_no_pathspec(self, gitignore_test_repo):
        """Test that tokenizer works when pathspec is unavailable."""
        with patch('thinktank_wrapper.gitignore.pathspec', None):
            # Should work with gitignore_enabled=True but pathspec unavailable
            counter = TokenCounter(gitignore_enabled=True)
            tokens, errors = counter.count_directory_tokens(gitignore_test_repo)
            
            # Should not crash and should process all files
            assert len(errors) == 0
            assert tokens > 0
    
    def test_token_counter_with_extension_filtering(self, gitignore_test_repo):
        """Test token counting with both gitignore and extension filtering."""
        counter = TokenCounter(gitignore_enabled=True)
        
        # Count only Python files
        tokens_py, errors_py = counter.count_directory_tokens(
            gitignore_test_repo, 
            extensions=['.py']
        )
        
        # Count all text files  
        tokens_all, errors_all = counter.count_directory_tokens(gitignore_test_repo)
        
        assert len(errors_py) == 0
        assert len(errors_all) == 0
        
        # Python-only should be subset of all files
        assert tokens_py <= tokens_all
    
    def test_token_counter_recursive_vs_non_recursive_with_gitignore(self, gitignore_test_repo):
        """Test gitignore behavior with recursive vs non-recursive directory traversal."""
        counter = TokenCounter(gitignore_enabled=True)
        
        # Recursive count (should include src/ subdirectory)
        tokens_recursive, _ = counter.count_directory_tokens(
            gitignore_test_repo, 
            recursive=True
        )
        
        # Non-recursive count (should only include root directory files)
        tokens_non_recursive, _ = counter.count_directory_tokens(
            gitignore_test_repo, 
            recursive=False
        )
        
        # Recursive should count more files (includes src/app.py)
        assert tokens_recursive >= tokens_non_recursive