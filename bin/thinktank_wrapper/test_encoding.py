#!/usr/bin/env python3
"""
Test script to verify improved encoding handling functionality.
"""

import os
import sys
import tempfile
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from thinktank_wrapper.tokenizer import TokenCounter, detect_file_encoding, get_encoding_error_message


def test_encoding_detection():
    """Test encoding detection functionality."""
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        
        print(f"Created test directory: {tmp_path}")
        
        # Test UTF-8 file
        print("\n=== Testing UTF-8 Encoding ===")
        utf8_file = tmp_path / "utf8.txt"
        utf8_file.write_text("Hello world! 🌍 Unicode test", encoding='utf-8')
        
        detected = detect_file_encoding(utf8_file)
        print(f"  UTF-8 file detection: {detected}")
        assert detected == 'utf-8', f"Expected utf-8, got {detected}"
        
        # Test file with TokenCounter
        counter = TokenCounter("openai")
        tokens, error = counter.count_file_tokens(utf8_file)
        print(f"  UTF-8 file tokens: {tokens}, error: {error}")
        assert error is None and tokens > 0, "UTF-8 file should be processed successfully"
        
        # Test Latin-1 file
        print("\n=== Testing Latin-1 Encoding ===")
        latin1_file = tmp_path / "latin1.txt"
        latin1_content = "Café résumé naïve"
        latin1_file.write_bytes(latin1_content.encode('latin1'))
        
        detected = detect_file_encoding(latin1_file)
        print(f"  Latin-1 file detection: {detected}")
        assert detected in ['latin1', 'cp1252', 'iso-8859-1'], f"Expected Latin-1 family, got {detected}"
        
        # Test file with TokenCounter (should give helpful error)
        tokens, error = counter.count_file_tokens(latin1_file)
        print(f"  Latin-1 file tokens: {tokens}, error: {error}")
        assert tokens == 0 and error is not None, "Latin-1 file should give encoding error"
        assert "encoding" in error.lower(), f"Error should mention encoding: {error}"
        assert "iconv" in error, f"Error should suggest iconv: {error}"
        
        # Test binary file with null bytes (should be caught by binary detection)
        print("\n=== Testing Binary File ===")
        binary_file = tmp_path / "binary.bin"
        # Create content with null bytes which indicates binary
        binary_content = b'Some text\x00\x01\x02\xff\xfe\x00more binary data'
        binary_file.write_bytes(binary_content)
        
        # Test with TokenCounter (should be skipped as binary)
        tokens, error = counter.count_file_tokens(binary_file)
        print(f"  Binary file tokens: {tokens}, error: {error}")
        assert tokens == 0 and error is None, "Binary file should be skipped with 0 tokens and no error"
        
        # Test UTF-8 with BOM
        print("\n=== Testing UTF-8 with BOM ===")
        utf8_bom_file = tmp_path / "utf8_bom.txt"
        content = "Hello world with BOM"
        utf8_bom_file.write_bytes(b'\xef\xbb\xbf' + content.encode('utf-8'))
        
        detected = detect_file_encoding(utf8_bom_file)
        print(f"  UTF-8 BOM file detection: {detected}")
        assert detected in ['utf-8', 'utf-8-sig'], f"Expected UTF-8 variant, got {detected}"
        
        # Test with TokenCounter
        tokens, error = counter.count_file_tokens(utf8_bom_file)
        print(f"  UTF-8 BOM file tokens: {tokens}, error: {error}")
        assert error is None and tokens > 0, "UTF-8 BOM file should be processed successfully"
        
        print("\n✅ All encoding detection tests passed!")


def test_error_messages():
    """Test encoding error message generation."""
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        
        print(f"\n=== Testing Error Message Generation ===")
        
        # Test error message for a file that encoding detection says is binary
        binary_file = tmp_path / "binary.dat"
        # Create a file that will make encoding detection return None
        binary_file.write_bytes(b'\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89')  # Invalid UTF-8 sequences
        
        fake_error = UnicodeDecodeError('utf-8', b'\x80\x81', 0, 1, 'invalid start byte')
        message = get_encoding_error_message(binary_file, fake_error)
        print(f"  Binary-like file message: {message}")
        assert "binary.dat" in message
        # The message will depend on what encoding detection finds
        assert "encoding" in message.lower() or "binary" in message.lower()
        
        # Test different encoding error message
        latin1_file = tmp_path / "latin1.txt"
        latin1_content = "Café résumé".encode('latin1')
        latin1_file.write_bytes(latin1_content)
        
        fake_error = UnicodeDecodeError('utf-8', latin1_content, 3, 4, 'invalid continuation byte')
        message = get_encoding_error_message(latin1_file, fake_error)
        print(f"  Latin-1 file message: {message}")
        assert "latin1.txt" in message
        assert "iconv" in message
        
        print("✅ Error message generation tests passed!")


def test_integration():
    """Test full integration with TokenCounter."""
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        
        print(f"\n=== Testing Full Integration ===")
        
        # Create various test files
        files = {
            "utf8.py": ("def hello(): return 'world'", 'utf-8'),
            "latin1.txt": ("Café résumé naïve", 'latin1'),
            "utf8_bom.js": ("console.log('hello');", 'utf-8-sig'),
        }
        
        counter = TokenCounter("openai")
        
        for filename, (content, encoding) in files.items():
            file_path = tmp_path / filename
            if encoding == 'utf-8-sig':
                # UTF-8 with BOM
                file_path.write_bytes(b'\xef\xbb\xbf' + content.encode('utf-8'))
            else:
                file_path.write_bytes(content.encode(encoding))
            
            tokens, error = counter.count_file_tokens(file_path)
            print(f"  {filename} ({encoding}): tokens={tokens}, error={error}")
            
            if encoding in ['utf-8', 'utf-8-sig']:
                assert error is None and tokens > 0, f"UTF-8 file {filename} should work"
            elif encoding == 'latin1':
                assert tokens == 0 and error is not None, f"Latin-1 file {filename} should give error"
                assert "encoding" in error.lower(), f"Error should mention encoding for {filename}"
        
        print("✅ Integration tests passed!")


def main():
    """Run all encoding tests."""
    print("Testing improved encoding handling...\n")
    
    try:
        test_encoding_detection()
        test_error_messages()
        test_integration()
        
        print("\n🎉 All encoding handling tests passed! Improved encoding functionality is working.")
        return 0
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())