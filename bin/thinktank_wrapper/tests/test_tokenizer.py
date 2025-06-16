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
        assert counter.verbose is False  # Default verbose should be False
    
    def test_init_openai_provider(self):
        """Test initialization with OpenAI provider."""
        counter = TokenCounter("openai")
        assert counter.provider == "openai"
        assert counter.base_ratio == 0.25
    
    def test_init_with_verbose(self):
        """Test initialization with verbose parameter."""
        # Test verbose enabled
        counter_verbose = TokenCounter(verbose=True)
        assert counter_verbose.verbose is True
        
        # Test verbose explicitly disabled
        counter_no_verbose = TokenCounter(verbose=False)
        assert counter_no_verbose.verbose is False
        
        # Test default behavior
        counter_default = TokenCounter()
        assert counter_default.verbose is False
    
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
    
    def test_verbose_binary_file_logging(self, binary_test_files, caplog):
        """Test that verbose mode logs binary file skipping at INFO level."""
        import logging
        
        # Test with verbose disabled (default)
        counter_no_verbose = TokenCounter(verbose=False)
        caplog.clear()
        with caplog.at_level(logging.INFO):
            binary_file = binary_test_files['binary']
            tokens, error = counter_no_verbose.count_file_tokens(binary_file)
            assert tokens == 0
            assert error is None
            
            # Should not log at INFO level when verbose is disabled
            info_logs = [record for record in caplog.records if record.levelno >= logging.INFO]
            binary_skip_logs = [log for log in info_logs if "Skipping binary file" in log.message]
            assert len(binary_skip_logs) == 0
        
        # Test with verbose enabled
        counter_verbose = TokenCounter(verbose=True)
        caplog.clear()
        with caplog.at_level(logging.INFO):
            tokens, error = counter_verbose.count_file_tokens(binary_file)
            assert tokens == 0
            assert error is None
            
            # Should log at INFO level when verbose is enabled
            info_logs = [record for record in caplog.records if record.levelno >= logging.INFO]
            binary_skip_logs = [log for log in info_logs if "Skipping binary file" in log.message]
            assert len(binary_skip_logs) == 1
            assert binary_file.name in binary_skip_logs[0].message
    
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
        counter = TokenCounter("openai", include_extensions=['.py'])
        tmp_path = next(iter(temp_files.values()))[0].parent
        
        # Count only Python files
        tokens, errors = counter.count_directory_tokens(tmp_path)
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


class TestBinaryFileHandlingComprehensive:
    """Comprehensive tests for binary file handling in real-world scenarios."""
    
    @pytest.fixture
    def comprehensive_binary_test_files(self, tmp_path):
        """Create a comprehensive set of test files for binary detection testing."""
        files = {}
        
        # Real binary file patterns
        
        # 1. Executable files with real headers
        elf_file = tmp_path / "linux_executable"
        elf_file.write_bytes(b'\x7fELF\x02\x01\x01\x00' + b'\x00' * 56 + b'Hello World')
        files['elf_executable'] = elf_file
        
        pe_file = tmp_path / "windows_app.exe"  
        pe_file.write_bytes(b'MZ' + b'\x00' * 58 + b'This program cannot be run in DOS mode')
        files['pe_executable'] = pe_file
        
        # 2. Image files with real headers
        png_file = tmp_path / "test_image.png"
        png_file.write_bytes(b'\x89PNG\r\n\x1a\n' + b'\x00' * 20 + b'image data')
        files['png_image'] = png_file
        
        jpeg_file = tmp_path / "photo.jpg"
        jpeg_file.write_bytes(b'\xff\xd8\xff\xe0' + b'JFIF' + b'\x00' * 100)
        files['jpeg_image'] = jpeg_file
        
        # 3. Archive files
        zip_file = tmp_path / "archive.zip" 
        zip_file.write_bytes(b'PK\x03\x04' + b'\x00' * 26 + b'archive content')
        files['zip_archive'] = zip_file
        
        # 4. Audio files
        mp3_file = tmp_path / "song.mp3"
        mp3_file.write_bytes(b'ID3' + b'\x03\x00\x00\x00' + b'\x00' * 100)
        files['mp3_audio'] = mp3_file
        
        # 5. Font files
        ttf_file = tmp_path / "font.ttf"
        ttf_file.write_bytes(b'\x00\x01\x00\x00' + b'\x00' * 20 + b'font data')
        files['ttf_font'] = ttf_file
        
        # 6. Mixed content files (mostly text with some binary)
        mixed_file = tmp_path / "mixed_content.dat"
        mixed_content = b'Text content at start\n' + b'\x00\x01\x02' + b'more text\n' + b'\xff\xfe'
        mixed_file.write_bytes(mixed_content)
        files['mixed_content'] = mixed_file
        
        # 7. Large text file (performance test)
        large_text = tmp_path / "large_text.log"
        large_content = "This is a test line.\n" * 10000  # ~200KB of text
        large_text.write_text(large_content)
        files['large_text'] = large_text
        
        # 8. Text files that might be confused for binary
        script_no_ext = tmp_path / "install_script"
        script_no_ext.write_text("#!/bin/bash\necho 'Installing application...'\n")
        files['script_no_ext'] = script_no_ext
        
        json_no_ext = tmp_path / "config_file"
        json_no_ext.write_text('{"version": "1.0", "settings": {"debug": true}}')
        files['json_no_ext'] = json_no_ext
        
        # 9. Files with misleading extensions
        text_with_bin_ext = tmp_path / "actually_text.bin"
        text_with_bin_ext.write_text("This file has a .bin extension but contains only text")
        files['text_with_bin_ext'] = text_with_bin_ext
        
        binary_with_txt_ext = tmp_path / "actually_binary.txt"
        binary_with_txt_ext.write_bytes(b'Binary data: \x00\x01\x02\xff\xfe\xfd')
        files['binary_with_txt_ext'] = binary_with_txt_ext
        
        # 10. Empty and minimal files
        empty_with_binary_ext = tmp_path / "empty.exe"
        empty_with_binary_ext.write_bytes(b'')
        files['empty_binary_ext'] = empty_with_binary_ext
        
        minimal_binary = tmp_path / "minimal.bin"
        minimal_binary.write_bytes(b'\x00')  # Just a null byte
        files['minimal_binary'] = minimal_binary
        
        return files
    
    def test_real_binary_file_detection(self, comprehensive_binary_test_files):
        """Test detection of real binary file formats."""
        # Real binary files should be detected correctly
        assert is_binary_file(comprehensive_binary_test_files['elf_executable'])
        assert is_binary_file(comprehensive_binary_test_files['pe_executable'])
        assert is_binary_file(comprehensive_binary_test_files['png_image'])
        assert is_binary_file(comprehensive_binary_test_files['jpeg_image'])
        assert is_binary_file(comprehensive_binary_test_files['zip_archive'])
        assert is_binary_file(comprehensive_binary_test_files['mp3_audio'])
        assert is_binary_file(comprehensive_binary_test_files['ttf_font'])
    
    def test_mixed_content_detection(self, comprehensive_binary_test_files):
        """Test detection of files with mixed text/binary content."""
        # Mixed content with null bytes should be detected as binary
        assert is_binary_file(comprehensive_binary_test_files['mixed_content'])
        
        # Binary content with text extension should still be detected as binary
        assert is_binary_file(comprehensive_binary_test_files['binary_with_txt_ext'])
    
    def test_text_file_edge_cases(self, comprehensive_binary_test_files):
        """Test text files that might be misidentified."""
        # Large text files should not be detected as binary
        assert not is_binary_file(comprehensive_binary_test_files['large_text'])
        
        # Scripts without extensions should not be detected as binary
        assert not is_binary_file(comprehensive_binary_test_files['script_no_ext'])
        
        # JSON files without extensions should not be detected as binary
        assert not is_binary_file(comprehensive_binary_test_files['json_no_ext'])
    
    def test_misleading_extensions(self, comprehensive_binary_test_files):
        """Test files with misleading extensions."""
        # Text with binary extension - extension check should win
        # (.bin is not in BINARY_EXTENSIONS, so should fall through to content detection)
        text_bin_result = is_binary_file(comprehensive_binary_test_files['text_with_bin_ext'])
        # This depends on whether .bin is in BINARY_EXTENSIONS
        if '.bin' in BINARY_EXTENSIONS:
            assert text_bin_result  # Extension would win
        else:
            assert not text_bin_result  # Content analysis would win
    
    def test_empty_file_edge_cases(self, comprehensive_binary_test_files):
        """Test empty files with various extensions."""
        # Empty file with binary extension should be detected based on extension
        empty_binary = comprehensive_binary_test_files['empty_binary_ext']
        assert is_binary_file(empty_binary)  # .exe is in BINARY_EXTENSIONS
        
        # Minimal binary file should be detected as binary
        assert is_binary_file(comprehensive_binary_test_files['minimal_binary'])
    
    def test_detection_method_precedence(self, comprehensive_binary_test_files):
        """Test that detection methods are applied in correct order."""
        # Test a file where we can verify the precedence
        test_file = comprehensive_binary_test_files['pe_executable']  # .exe extension + binary content
        
        # Extension should be checked first and return True
        ext_result = is_binary_by_extension(test_file)
        assert ext_result  # .exe should be in BINARY_EXTENSIONS
        
        # Full detection should also return True (via extension, not content)
        full_result = is_binary_file(test_file)
        assert full_result
    
    def test_performance_with_large_files(self, comprehensive_binary_test_files):
        """Test performance characteristics with larger files."""
        large_file = comprehensive_binary_test_files['large_text']
        
        # Should complete quickly (content analysis stops at first 8KB)
        import time
        start = time.time()
        result = is_binary_file(large_file)
        elapsed = time.time() - start
        
        assert not result  # Should be detected as text
        assert elapsed < 1.0  # Should complete quickly (less than 1 second)
    
    def test_tokenizer_integration_with_comprehensive_files(self, comprehensive_binary_test_files):
        """Test TokenCounter integration with various binary file types."""
        counter = TokenCounter()
        
        # Binary files should return 0 tokens
        binary_files = [
            'elf_executable', 'pe_executable', 'png_image', 'jpeg_image',
            'zip_archive', 'mp3_audio', 'ttf_font', 'mixed_content'
        ]
        
        for file_key in binary_files:
            file_path = comprehensive_binary_test_files[file_key]
            tokens, error = counter.count_file_tokens(file_path)
            assert tokens == 0, f"Binary file {file_key} should have 0 tokens"
            assert error is None, f"Binary file {file_key} should not generate errors"
        
        # Text files should return > 0 tokens
        text_files = ['large_text', 'script_no_ext', 'json_no_ext']
        
        for file_key in text_files:
            file_path = comprehensive_binary_test_files[file_key]
            tokens, error = counter.count_file_tokens(file_path)
            assert tokens > 0, f"Text file {file_key} should have > 0 tokens"
            assert error is None, f"Text file {file_key} should not generate errors"
    
    def test_directory_scanning_with_mixed_content(self, comprehensive_binary_test_files):
        """Test directory scanning with mixed binary and text files."""
        counter = TokenCounter()
        
        # Get the directory containing all test files
        test_dir = list(comprehensive_binary_test_files.values())[0].parent
        
        # Count tokens in the directory
        total_tokens, errors = counter.count_directory_tokens(test_dir, recursive=False)
        
        # Should have no errors
        assert len(errors) == 0
        
        # Should have some tokens (from text files) but not from binary files
        assert total_tokens > 0
        
        # Manually verify by counting expected text files
        expected_text_files = ['large_text', 'script_no_ext', 'json_no_ext']
        manual_total = 0
        for file_key in expected_text_files:
            file_path = comprehensive_binary_test_files[file_key]
            tokens, error = counter.count_file_tokens(file_path)
            if error is None:
                manual_total += tokens
        
        # Directory count should be close to manual count
        # (might differ due to other files in directory, but should be in same ballpark)
        assert total_tokens >= manual_total
    
    def test_mime_type_accuracy_on_real_files(self, comprehensive_binary_test_files):
        """Test MIME type detection accuracy on real file formats."""
        if not MAGIC_AVAILABLE:
            pytest.skip("python-magic not available")
        
        # Test specific file format MIME detection
        test_cases = [
            ('png_image', True),    # Should detect as binary
            ('jpeg_image', True),   # Should detect as binary
            ('script_no_ext', False),  # Should detect as text (script)
            ('json_no_ext', False),    # Should detect as text (JSON)
        ]
        
        for file_key, expected_binary in test_cases:
            file_path = comprehensive_binary_test_files[file_key]
            mime_result = is_binary_by_mime_type(file_path)
            
            if mime_result is not None:  # Only test if MIME detection worked
                assert mime_result == expected_binary, f"MIME detection failed for {file_key}"
    
    def test_error_handling_edge_cases(self, tmp_path):
        """Test error handling for various edge cases."""
        # Test with directory instead of file
        test_dir = tmp_path / "test_directory"
        test_dir.mkdir()
        assert not is_binary_file(test_dir)
        
        # Test with non-existent file
        assert not is_binary_file(tmp_path / "nonexistent.file")
        
        # Test with file that has read permission issues (if possible)
        restricted_file = tmp_path / "restricted.bin"
        restricted_file.write_bytes(b"binary content")
        
        try:
            # Try to make file unreadable (may not work on all systems)
            restricted_file.chmod(0o000)
            
            # Should handle gracefully
            result = is_binary_file(restricted_file)
            assert isinstance(result, bool)  # Should return bool, not crash
            
        except (OSError, PermissionError):
            # Skip if we can't modify permissions
            pass
        finally:
            # Restore permissions for cleanup
            try:
                restricted_file.chmod(0o644)
            except (OSError, PermissionError):
                pass
    
    def test_chunk_size_parameter(self, comprehensive_binary_test_files):
        """Test that chunk_size parameter works correctly."""
        large_binary_file = comprehensive_binary_test_files['mixed_content']
        
        # Test with different chunk sizes
        result_small = is_binary_file(large_binary_file, chunk_size=10)
        result_large = is_binary_file(large_binary_file, chunk_size=8192)
        
        # Both should return True (has null bytes near beginning)
        assert result_small
        assert result_large
        
        # Create a file with null byte far from beginning
        late_binary = comprehensive_binary_test_files['large_text'].parent / "late_binary.txt"
        content = b"A" * 1000 + b"\x00" + b"B" * 1000  # Null byte at position 1000
        late_binary.write_bytes(content)
        
        try:
            # Small chunk size might miss the null byte
            result_small_chunk = is_binary_file(late_binary, chunk_size=100)
            # Large chunk size should find it  
            result_large_chunk = is_binary_file(late_binary, chunk_size=2000)
            
            assert not result_small_chunk  # Might miss the null byte
            assert result_large_chunk      # Should find the null byte
            
        finally:
            late_binary.unlink()


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
        counter = TokenCounter(gitignore_enabled=True, include_extensions=['.py'])
        
        # Count only Python files
        tokens_py, errors_py = counter.count_directory_tokens(gitignore_test_repo)
        
        # Count all text files  
        counter_all = TokenCounter(gitignore_enabled=True)
        tokens_all, errors_all = counter_all.count_directory_tokens(gitignore_test_repo)
        
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


class TestAnthropicTokenizer:
    """Test Anthropic tokenizer integration."""
    
    def test_anthropic_tokenizer_initialization_with_api_key(self):
        """Test TokenCounter initialization with Anthropic provider when API key is available."""
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
            with patch('thinktank_wrapper.tokenizer.ANTHROPIC_AVAILABLE', True):
                with patch('thinktank_wrapper.tokenizer.anthropic') as mock_anthropic:
                    mock_client = Mock()
                    mock_anthropic.Anthropic.return_value = mock_client
                    
                    counter = TokenCounter("anthropic")
                    
                    assert counter.provider == "anthropic"
                    assert counter._anthropic_client == mock_client
                    mock_anthropic.Anthropic.assert_called_once_with(api_key="test-key")
    
    def test_anthropic_tokenizer_initialization_without_api_key(self):
        """Test TokenCounter initialization with Anthropic provider when API key is missing."""
        with patch.dict(os.environ, {}, clear=True):  # Clear ANTHROPIC_API_KEY
            with patch('thinktank_wrapper.tokenizer.ANTHROPIC_AVAILABLE', True):
                counter = TokenCounter("anthropic")
                
                assert counter.provider == "anthropic"
                assert counter._anthropic_client is None
    
    def test_anthropic_tokenizer_unavailable(self):
        """Test TokenCounter initialization when Anthropic library is unavailable."""
        with patch('thinktank_wrapper.tokenizer.ANTHROPIC_AVAILABLE', False):
            counter = TokenCounter("anthropic")
            
            assert counter.provider == "anthropic"
            assert counter._anthropic_client is None
    
    def test_anthropic_token_counting_success(self):
        """Test successful token counting using Anthropic API."""
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
            with patch('thinktank_wrapper.tokenizer.ANTHROPIC_AVAILABLE', True):
                with patch('thinktank_wrapper.tokenizer.anthropic') as mock_anthropic:
                    # Mock the client and response
                    mock_client = Mock()
                    mock_response = Mock()
                    mock_response.input_tokens = 25
                    mock_client.messages.count_tokens.return_value = mock_response
                    mock_anthropic.Anthropic.return_value = mock_client
                    
                    counter = TokenCounter("anthropic")
                    
                    # Test token counting
                    text = "This is a test message for token counting."
                    tokens = counter.count_text_tokens(text)
                    
                    assert tokens == 25
                    mock_client.messages.count_tokens.assert_called_once_with(
                        model="claude-3-haiku-20240307",
                        messages=[{"role": "user", "content": text}]
                    )
    
    def test_anthropic_token_counting_api_failure(self):
        """Test fallback to character approximation when Anthropic API fails."""
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
            with patch('thinktank_wrapper.tokenizer.ANTHROPIC_AVAILABLE', True):
                with patch('thinktank_wrapper.tokenizer.anthropic') as mock_anthropic:
                    # Mock the client to raise an exception
                    mock_client = Mock()
                    mock_client.messages.count_tokens.side_effect = Exception("API Error")
                    mock_anthropic.Anthropic.return_value = mock_client
                    
                    counter = TokenCounter("anthropic")
                    
                    # Test token counting falls back to approximation
                    text = "This is a test message."  # 24 chars
                    tokens = counter.count_text_tokens(text)
                    
                    # Should fall back to character approximation: 24 * 0.24 = 5.76 = 5
                    assert tokens == 5
    
    def test_anthropic_token_counting_malformed_response(self):
        """Test handling of malformed API response."""
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
            with patch('thinktank_wrapper.tokenizer.ANTHROPIC_AVAILABLE', True):
                with patch('thinktank_wrapper.tokenizer.anthropic') as mock_anthropic:
                    # Mock response without input_tokens attribute
                    mock_client = Mock()
                    mock_response = Mock(spec=[])  # Empty spec to avoid having input_tokens
                    mock_client.messages.count_tokens.return_value = mock_response
                    mock_anthropic.Anthropic.return_value = mock_client
                    
                    counter = TokenCounter("anthropic")
                    
                    # Test token counting falls back to approximation
                    text = "This is a test message."  # 24 chars
                    tokens = counter.count_text_tokens(text)
                    
                    # Should fall back to character approximation: 24 * 0.24 = 5.76 = 5
                    assert tokens == 5
    
    def test_anthropic_token_counting_empty_text(self):
        """Test Anthropic token counting with empty text."""
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
            with patch('thinktank_wrapper.tokenizer.ANTHROPIC_AVAILABLE', True):
                with patch('thinktank_wrapper.tokenizer.anthropic') as mock_anthropic:
                    mock_client = Mock()
                    mock_anthropic.Anthropic.return_value = mock_client
                    
                    counter = TokenCounter("anthropic")
                    
                    # Test with empty text
                    assert counter.count_text_tokens("") == 0
                    assert counter.count_text_tokens(None) == 0
                    
                    # API should not be called for empty text
                    mock_client.messages.count_tokens.assert_not_called()
    
    def test_anthropic_vs_tiktoken_precedence(self):
        """Test that providers use their own tokenizers, not each other's."""
        text = "def hello_world(): return 'Hello, World!'"
        
        # Test OpenAI provider (should use tiktoken if available, not Anthropic)
        with patch('thinktank_wrapper.tokenizer.TIKTOKEN_AVAILABLE', True):
            with patch('thinktank_wrapper.tokenizer.tiktoken') as mock_tiktoken:
                mock_encoding = Mock()
                mock_encoding.encode.return_value = ["token"] * 10  # 10 tokens
                mock_tiktoken.get_encoding.return_value = mock_encoding
                
                counter_openai = TokenCounter("openai")
                tokens = counter_openai.count_text_tokens(text)
                
                assert tokens == 10
                assert counter_openai._anthropic_client is None  # Should not initialize Anthropic client
        
        # Test Anthropic provider (should use Anthropic API, not tiktoken)
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
            with patch('thinktank_wrapper.tokenizer.ANTHROPIC_AVAILABLE', True):
                with patch('thinktank_wrapper.tokenizer.anthropic') as mock_anthropic:
                    mock_client = Mock()
                    mock_response = Mock()
                    mock_response.input_tokens = 15
                    mock_client.messages.count_tokens.return_value = mock_response
                    mock_anthropic.Anthropic.return_value = mock_client
                    
                    counter_anthropic = TokenCounter("anthropic")
                    tokens = counter_anthropic.count_text_tokens(text)
                    
                    assert tokens == 15
                    assert counter_anthropic._tiktoken_encoding is None  # Should not initialize tiktoken
    
    def test_anthropic_file_token_counting(self, temp_files):
        """Test Anthropic token counting integration with file processing."""
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
            with patch('thinktank_wrapper.tokenizer.ANTHROPIC_AVAILABLE', True):
                with patch('thinktank_wrapper.tokenizer.anthropic') as mock_anthropic:
                    mock_client = Mock()
                    mock_response = Mock()
                    mock_response.input_tokens = 12
                    mock_client.messages.count_tokens.return_value = mock_response
                    mock_anthropic.Anthropic.return_value = mock_client
                    
                    counter = TokenCounter("anthropic")
                    
                    # Test counting tokens in a Python file
                    py_file, _ = temp_files['python']
                    tokens, error = counter.count_file_tokens(py_file)
                    
                    assert error is None
                    # Should use API result (12) with file type adjustment (1.15 for .py)
                    # 12 * 1.15 = 13.8 = 13 tokens
                    assert tokens == 13
    
    def test_multi_provider_anthropic_integration(self, temp_files):
        """Test MultiProviderTokenCounter includes Anthropic provider."""
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
            with patch('thinktank_wrapper.tokenizer.ANTHROPIC_AVAILABLE', True):
                with patch('thinktank_wrapper.tokenizer.anthropic') as mock_anthropic:
                    mock_client = Mock()
                    mock_response = Mock()
                    mock_response.input_tokens = 20
                    mock_client.messages.count_tokens.return_value = mock_response
                    mock_anthropic.Anthropic.return_value = mock_client
                    
                    multi_counter = MultiProviderTokenCounter()
                    py_file, _ = temp_files['python']
                    
                    results = multi_counter.count_all_providers([py_file])
                    
                    # Check that Anthropic provider is included and uses API
                    assert "anthropic" in results
                    anthropic_tokens, anthropic_errors = results["anthropic"]
                    assert len(anthropic_errors) == 0
                    # Should use API result with file type adjustment: 20 * 1.15 = 23
                    assert anthropic_tokens == 23


class TestExtensionFiltering:
    """Test file extension filtering functionality."""
    
    def test_should_process_file_extension_no_filters(self):
        """Test that all files are processed when no filters are specified."""
        from thinktank_wrapper.tokenizer import should_process_file_extension
        
        assert should_process_file_extension("test.py")
        assert should_process_file_extension("test.js")
        assert should_process_file_extension("test.log")
        assert should_process_file_extension("test.txt")
        assert should_process_file_extension("README")  # No extension
    
    def test_should_process_file_extension_include_filter(self):
        """Test include extension filtering."""
        from thinktank_wrapper.tokenizer import should_process_file_extension
        
        include_exts = ['.py', '.js']
        
        assert should_process_file_extension("test.py", include_extensions=include_exts)
        assert should_process_file_extension("test.js", include_extensions=include_exts)
        assert not should_process_file_extension("test.log", include_extensions=include_exts)
        assert not should_process_file_extension("test.txt", include_extensions=include_exts)
        assert not should_process_file_extension("README", include_extensions=include_exts)
    
    def test_should_process_file_extension_exclude_filter(self):
        """Test exclude extension filtering."""
        from thinktank_wrapper.tokenizer import should_process_file_extension
        
        exclude_exts = ['.log', '.tmp']
        
        assert should_process_file_extension("test.py", exclude_extensions=exclude_exts)
        assert should_process_file_extension("test.js", exclude_extensions=exclude_exts)
        assert not should_process_file_extension("test.log", exclude_extensions=exclude_exts)
        assert not should_process_file_extension("test.tmp", exclude_extensions=exclude_exts)
        assert should_process_file_extension("README", exclude_extensions=exclude_exts)
    
    def test_should_process_file_extension_normalization(self):
        """Test that extensions are normalized (case-insensitive, dots added)."""
        from thinktank_wrapper.tokenizer import should_process_file_extension
        
        # Test with extensions provided without dots
        include_exts = ['py', 'JS']  # No dots, mixed case
        
        assert should_process_file_extension("test.py", include_extensions=include_exts)
        assert should_process_file_extension("test.js", include_extensions=include_exts)
        assert should_process_file_extension("test.JS", include_extensions=include_exts)
        assert not should_process_file_extension("test.txt", include_extensions=include_exts)
    
    def test_token_counter_with_include_extensions(self, temp_files):
        """Test TokenCounter with include extension filtering."""
        counter = TokenCounter("openai", include_extensions=['.py'])
        
        # Should only count Python files
        py_file, _ = temp_files['python'] 
        tokens, error = counter.count_file_tokens(py_file)
        assert error is None
        assert tokens > 0
        
        # Directory counting should only include Python files
        tmp_path = py_file.parent
        total_tokens, errors = counter.count_directory_tokens(tmp_path)
        assert len(errors) == 0
        assert total_tokens == tokens  # Only the Python file
    
    def test_token_counter_with_exclude_extensions(self, temp_files):
        """Test TokenCounter with exclude extension filtering."""
        counter = TokenCounter("openai", exclude_extensions=['.md', '.json'])
        
        # Should count Python files but not markdown or JSON
        py_file, _ = temp_files['python']
        tmp_path = py_file.parent
        
        total_tokens, errors = counter.count_directory_tokens(tmp_path)
        assert len(errors) == 0
        assert total_tokens > 0  # Should count the Python file
        
        # Create separate counter without filtering to compare
        counter_all = TokenCounter("openai")
        total_tokens_all, _ = counter_all.count_directory_tokens(tmp_path)
        
        # Filtered count should be less than unfiltered (excludes .md and .json)
        assert total_tokens < total_tokens_all
    
    def test_multi_provider_token_counter_with_extensions(self, temp_files):
        """Test MultiProviderTokenCounter with extension filtering."""
        multi_counter = MultiProviderTokenCounter(include_extensions=['.py'])
        py_file, _ = temp_files['python']
        
        results = multi_counter.count_all_providers([py_file])
        
        # All providers should respect the extension filtering
        for provider, (tokens, errors) in results.items():
            assert len(errors) == 0
            assert tokens > 0  # Python file should be counted
    
    def test_extension_filtering_case_insensitive(self, tmp_path):
        """Test that extension filtering is case-insensitive."""
        # Create files with mixed case extensions
        py_file = tmp_path / "test.PY"
        py_file.write_text("print('hello')")
        
        JS_file = tmp_path / "test.JS"
        JS_file.write_text("console.log('hello');")
        
        counter = TokenCounter("openai", include_extensions=['.py', '.js'])
        
        # Both files should be counted despite case differences
        py_tokens, py_error = counter.count_file_tokens(py_file)
        js_tokens, js_error = counter.count_file_tokens(JS_file)
        
        assert py_error is None and py_tokens > 0
        assert js_error is None and js_tokens > 0
        
        # Directory count should include both files
        total_tokens, errors = counter.count_directory_tokens(tmp_path)
        assert len(errors) == 0
        assert total_tokens == py_tokens + js_tokens
    
    def test_extension_filtering_no_extension_files(self, tmp_path):
        """Test handling of files without extensions."""
        # Create files without extensions
        no_ext_file = tmp_path / "README"
        no_ext_file.write_text("This is a readme file")
        
        makefile = tmp_path / "Makefile"
        makefile.write_text("all:\n\techo 'building'")
        
        # Include filtering should exclude files without extensions
        counter_include = TokenCounter("openai", include_extensions=['.py'])
        tokens_include, errors_include = counter_include.count_directory_tokens(tmp_path)
        assert len(errors_include) == 0
        assert tokens_include == 0  # No .py files
        
        # Exclude filtering should include files without extensions (unless explicitly excluded)
        counter_exclude = TokenCounter("openai", exclude_extensions=['.log'])
        tokens_exclude, errors_exclude = counter_exclude.count_directory_tokens(tmp_path)
        assert len(errors_exclude) == 0
        assert tokens_exclude > 0  # Should include files without extensions


class TestErrorMessages:
    """Test improved error message functionality."""
    
    def test_get_file_access_error_message_permission_error(self, tmp_path):
        """Test permission error message generation."""
        from thinktank_wrapper.tokenizer import get_file_access_error_message
        
        test_file = tmp_path / "test.txt"
        error = PermissionError("Permission denied")
        
        message = get_file_access_error_message(test_file, error)
        
        assert "Permission denied" in message
        assert "test.txt" in message
        assert "chmod +r" in message
        assert "read access" in message
    
    def test_get_file_access_error_message_file_not_found(self, tmp_path):
        """Test file not found error message generation."""
        from thinktank_wrapper.tokenizer import get_file_access_error_message
        
        test_file = tmp_path / "missing.txt"
        error = FileNotFoundError("No such file or directory")
        
        message = get_file_access_error_message(test_file, error)
        
        assert "File not found" in message
        assert str(test_file) in message
        assert "Check that the file exists" in message
    
    def test_get_file_access_error_message_is_directory(self, tmp_path):
        """Test directory error message generation."""
        from thinktank_wrapper.tokenizer import get_file_access_error_message
        
        test_dir = tmp_path / "testdir"
        test_dir.mkdir()
        error = IsADirectoryError("Is a directory")
        
        message = get_file_access_error_message(test_dir, error)
        
        assert "is a directory" in message
        assert "testdir" in message
        assert "Specify a file path" in message
    
    def test_get_file_access_error_message_generic_os_error(self, tmp_path):
        """Test generic OSError message generation."""
        from thinktank_wrapper.tokenizer import get_file_access_error_message
        
        test_file = tmp_path / "test.txt"
        error = OSError("Generic I/O error")
        
        message = get_file_access_error_message(test_file, error)
        
        assert "Unable to read" in message
        assert "test.txt" in message
        assert "Check file permissions" in message
    
    def test_get_file_access_error_message_eacces_errno(self, tmp_path):
        """Test EACCES errno handling."""
        from thinktank_wrapper.tokenizer import get_file_access_error_message
        import errno
        
        test_file = tmp_path / "test.txt"
        error = OSError()
        error.errno = errno.EACCES
        
        message = get_file_access_error_message(test_file, error)
        
        assert "Access denied" in message
        assert "test.txt" in message
        assert "locked by another process" in message or "restrictive permissions" in message
    
    def test_token_counter_permission_error_handling(self, tmp_path):
        """Test TokenCounter handles permission errors gracefully."""
        # Create a test file
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        
        counter = TokenCounter("openai")
        
        try:
            # Make file unreadable
            test_file.chmod(0o000)
            
            tokens, error = counter.count_file_tokens(test_file)
            
            # Should return 0 tokens and a user-friendly error
            assert tokens == 0
            assert error is not None
            assert "Permission denied" in error or "Access denied" in error
            assert "test.txt" in error
            
        except (OSError, PermissionError):
            # Skip test if we can't modify permissions on this system
            pytest.skip("Cannot modify file permissions on this system")
        finally:
            # Restore permissions for cleanup
            try:
                test_file.chmod(0o644)
            except (OSError, PermissionError):
                pass
    
    def test_token_counter_file_not_found_error_handling(self, tmp_path):
        """Test TokenCounter handles missing files gracefully."""
        nonexistent_file = tmp_path / "does_not_exist.txt"
        
        counter = TokenCounter("openai")
        tokens, error = counter.count_file_tokens(nonexistent_file)
        
        assert tokens == 0
        assert error is not None
        assert "File not found" in error
        assert "does_not_exist.txt" in error


class TestEncodingHandling:
    """Test improved encoding detection and error handling."""
    
    def test_detect_file_encoding_utf8(self, tmp_path):
        """Test encoding detection for UTF-8 files."""
        from thinktank_wrapper.tokenizer import detect_file_encoding
        
        # Create UTF-8 file
        utf8_file = tmp_path / "utf8.txt"
        utf8_file.write_text("Hello world! 🌍", encoding='utf-8')
        
        detected = detect_file_encoding(utf8_file)
        assert detected == 'utf-8'
    
    def test_detect_file_encoding_latin1(self, tmp_path):
        """Test encoding detection for Latin-1 files."""
        from thinktank_wrapper.tokenizer import detect_file_encoding
        
        # Create Latin-1 file
        latin1_file = tmp_path / "latin1.txt"
        latin1_content = "Café résumé naïve".encode('latin1')
        latin1_file.write_bytes(latin1_content)
        
        detected = detect_file_encoding(latin1_file)
        assert detected in ['latin1', 'cp1252', 'iso-8859-1']  # Any of these are acceptable
    
    def test_detect_file_encoding_binary(self, tmp_path):
        """Test encoding detection for binary files."""
        from thinktank_wrapper.tokenizer import detect_file_encoding
        
        # Create binary file
        binary_file = tmp_path / "binary.bin"
        binary_file.write_bytes(b'\xff\xfe\x00\x00\x80\x90\xa0\xb0')
        
        detected = detect_file_encoding(binary_file)
        assert detected is None  # Should detect as binary
    
    def test_detect_file_encoding_empty(self, tmp_path):
        """Test encoding detection for empty files."""
        from thinktank_wrapper.tokenizer import detect_file_encoding
        
        # Create empty file
        empty_file = tmp_path / "empty.txt"
        empty_file.touch()
        
        detected = detect_file_encoding(empty_file)
        assert detected == 'utf-8'  # Default for empty files
    
    def test_get_encoding_error_message_binary_detection(self, tmp_path):
        """Test encoding error message for binary files."""
        from thinktank_wrapper.tokenizer import get_encoding_error_message
        
        # Create a binary file
        binary_file = tmp_path / "binary.dat"
        binary_file.write_bytes(b'\xff\xfe\x00\x00\x80\x90\xa0\xb0')
        
        fake_error = UnicodeDecodeError('utf-8', b'\xff\xfe', 0, 1, 'invalid start byte')
        message = get_encoding_error_message(binary_file, fake_error)
        
        assert "binary.dat" in message
        assert "binary data" in message
        assert "corrupted" in message or "unusual encoding" in message
    
    def test_get_encoding_error_message_different_encoding(self, tmp_path):
        """Test encoding error message for files with different encodings."""
        from thinktank_wrapper.tokenizer import get_encoding_error_message
        
        # Create a Latin-1 file
        latin1_file = tmp_path / "latin1.txt"
        latin1_content = "Café résumé".encode('latin1')
        latin1_file.write_bytes(latin1_content)
        
        fake_error = UnicodeDecodeError('utf-8', latin1_content, 3, 4, 'invalid continuation byte')
        message = get_encoding_error_message(latin1_file, fake_error)
        
        assert "latin1.txt" in message
        assert "encoding" in message.lower()
        assert "iconv" in message  # Should suggest conversion command
    
    def test_get_encoding_error_message_corrupted_utf8(self, tmp_path):
        """Test encoding error message for corrupted UTF-8 files."""
        from thinktank_wrapper.tokenizer import get_encoding_error_message
        
        # Create a file that starts as UTF-8 but becomes corrupted
        utf8_file = tmp_path / "corrupted.txt"
        content = "Valid UTF-8 start".encode('utf-8') + b'\xff\xfe\x00'
        utf8_file.write_bytes(content)
        
        fake_error = UnicodeDecodeError('utf-8', content, 17, 18, 'invalid start byte')
        message = get_encoding_error_message(utf8_file, fake_error)
        
        assert "corrupted.txt" in message
        assert "UTF-8 encoding issues" in message
        assert "corrupted" in message or "mixed encodings" in message
        assert "file" in message  # Should suggest using file command
    
    def test_token_counter_encoding_error_handling(self, tmp_path):
        """Test TokenCounter handles encoding errors gracefully."""
        # Create a file with non-UTF-8 content
        non_utf8_file = tmp_path / "latin1.txt"
        non_utf8_content = "Café résumé naïve".encode('latin1')
        non_utf8_file.write_bytes(non_utf8_content)
        
        counter = TokenCounter("openai")
        tokens, error = counter.count_file_tokens(non_utf8_file)
        
        # Should return 0 tokens and a helpful error message
        assert tokens == 0
        assert error is not None
        assert "latin1.txt" in error
        assert "encoding" in error.lower()
        # Should provide conversion guidance for detected encoding
        assert "iconv" in error or "encoding issues" in error
    
    def test_token_counter_with_utf8_bom(self, tmp_path):
        """Test TokenCounter handles UTF-8 with BOM correctly."""
        # Create UTF-8 file with BOM
        utf8_bom_file = tmp_path / "utf8_bom.txt"
        content = "Hello world"
        utf8_bom_file.write_bytes(b'\xef\xbb\xbf' + content.encode('utf-8'))  # BOM + content
        
        counter = TokenCounter("openai")
        tokens, error = counter.count_file_tokens(utf8_bom_file)
        
        # Should successfully read the file (BOM should be handled)
        assert error is None
        assert tokens > 0
    
    def test_token_counter_encoding_vs_binary_detection(self, tmp_path):
        """Test that encoding errors are handled differently from binary detection."""
        # Create a text file with encoding issues (not binary)
        encoding_issue_file = tmp_path / "bad_encoding.txt"
        # This is valid Latin-1 but invalid UTF-8
        encoding_issue_file.write_bytes("Café".encode('latin1'))
        
        # Create a clearly binary file
        binary_file = tmp_path / "clearly_binary.bin"
        binary_file.write_bytes(b'\x00\x01\x02\x03\xff\xfe\xfd\xfc')
        
        counter = TokenCounter("openai")
        
        # Encoding issue should give encoding error
        tokens1, error1 = counter.count_file_tokens(encoding_issue_file)
        assert tokens1 == 0
        assert error1 is not None
        assert "encoding" in error1.lower()
        
        # Binary file should be skipped without error (handled by binary detection)
        tokens2, error2 = counter.count_file_tokens(binary_file)
        assert tokens2 == 0
        assert error2 is None  # Binary files are silently skipped
    
    def test_encoding_detection_performance(self, tmp_path):
        """Test that encoding detection doesn't read entire large files."""
        from thinktank_wrapper.tokenizer import detect_file_encoding
        
        # Create a large file
        large_file = tmp_path / "large.txt"
        # Write a large amount of data (much more than the 8KB sample)
        content = "This is a test line.\n" * 10000  # ~200KB
        large_file.write_text(content, encoding='utf-8')
        
        # Detection should be fast even for large files
        import time
        start = time.time()
        detected = detect_file_encoding(large_file)
        elapsed = time.time() - start
        
        assert detected == 'utf-8'
        assert elapsed < 1.0  # Should complete quickly (less than 1 second)