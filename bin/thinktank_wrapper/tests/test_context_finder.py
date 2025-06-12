"""Tests for the context_finder module."""

import os
from pathlib import Path
from typing import List

import pytest

from thinktank_wrapper.context_finder import (
    find_context_files,
    find_glance_files,
    find_philosophy_files,
    validate_paths,
)


def test_find_glance_files_empty():
    """Test that find_glance_files returns an empty list when no paths are provided."""
    with pytest.MonkeyPatch().context() as mp:
        # Change the working directory to a temporary directory
        mp.chdir("/tmp")
        # Call the function
        result = find_glance_files([])
        # Assert the result
        assert result == []


def test_find_glance_files(mock_glance_files: List[Path], temp_dir: Path):
    """Test that find_glance_files returns the correct glance files."""
    # Call the function with the temp directory
    result = find_glance_files([str(temp_dir)])
    
    # Assert the result contains all the mock glance files
    assert len(result) == len(mock_glance_files)
    for glance_file in mock_glance_files:
        assert str(glance_file.absolute()) in result


def test_find_philosophy_files(mock_codex_dir: Path):
    """Test that find_philosophy_files returns the correct philosophy files."""
    # Call the function
    result = find_philosophy_files()
    
    # Assert the result contains both mock philosophy files
    expected_files = [
        str((mock_codex_dir / "docs" / "DEVELOPMENT_PHILOSOPHY.md").absolute()),
        str((mock_codex_dir / "docs" / "DEVELOPMENT_PHILOSOPHY_APPENDIX_TYPESCRIPT.md").absolute()),
    ]
    
    assert sorted(result) == sorted(expected_files)


def test_find_philosophy_files_no_codex_dir(monkeypatch: pytest.MonkeyPatch):
    """Test that find_philosophy_files returns an empty list when CODEX_DIR is not set."""
    # Remove the CODEX_DIR environment variable
    monkeypatch.delenv("CODEX_DIR", raising=False)
    
    # Call the function
    result = find_philosophy_files()
    
    # Assert the result is an empty list
    assert result == []


def test_find_context_files(mock_glance_files: List[Path], mock_codex_dir: Path, temp_dir: Path):
    """Test that find_context_files returns the correct context files."""
    # Create a test file to use as an explicit path
    test_file = temp_dir / "test_file.txt"
    test_file.write_text("Test file")
    
    # Call the function
    result = find_context_files(
        include_glance=True,
        include_leyline=False,
        explicit_paths=[str(test_file)]
    )
    
    # Assert the result contains the glance files and explicit path
    expected_files = [
        str(test_file.absolute()),
    ]
    
    # Add the mock glance files
    for glance_file in mock_glance_files:
        expected_files.append(str(glance_file.absolute()))
    
    # Sort both lists for comparison
    assert sorted(result) == sorted(expected_files)


def test_find_leyline_files_fallback_to_philosophy(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    """Test that find_leyline_files falls back to philosophy files when no leyline directory exists."""
    # Create a temporary codex directory structure
    codex_dir = tmp_path / "codex"
    docs_dir = codex_dir / "docs"
    docs_dir.mkdir(parents=True)
    
    # Create philosophy files but no leyline directory
    philosophy_file1 = docs_dir / "DEVELOPMENT_PHILOSOPHY.md"
    philosophy_file1.write_text("Main philosophy")
    philosophy_file2 = docs_dir / "DEVELOPMENT_PHILOSOPHY_APPENDIX_GO.md"
    philosophy_file2.write_text("Go appendix")
    
    # Set CODEX_DIR environment variable
    monkeypatch.setenv("CODEX_DIR", str(codex_dir))
    
    # Call find_leyline_files
    result = find_leyline_files()
    
    # Assert it found the philosophy files as fallback
    expected_files = [
        str(philosophy_file1.absolute()),
        str(philosophy_file2.absolute()),
    ]
    assert sorted(result) == sorted(expected_files)


def test_find_leyline_files_with_leyline_directory(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    """Test that find_leyline_files finds leyline files when directory exists."""
    # Create a temporary codex directory structure
    codex_dir = tmp_path / "codex"
    docs_dir = codex_dir / "docs"
    leyline_dir = docs_dir / "leyline"
    leyline_dir.mkdir(parents=True)
    
    # Create leyline files
    leyline_file1 = leyline_dir / "index.md"
    leyline_file1.write_text("Leyline index")
    leyline_file2 = leyline_dir / "tenets" / "simplicity.md"
    leyline_file2.parent.mkdir()
    leyline_file2.write_text("Simplicity tenet")
    
    # Also create philosophy files (should be ignored when leyline exists)
    philosophy_file = docs_dir / "DEVELOPMENT_PHILOSOPHY.md"
    philosophy_file.write_text("Philosophy")
    
    # Set CODEX_DIR environment variable
    monkeypatch.setenv("CODEX_DIR", str(codex_dir))
    
    # Call find_leyline_files
    result = find_leyline_files()
    
    # Assert it found only the leyline files, not philosophy
    expected_files = [
        str(leyline_file1.absolute()),
        str(leyline_file2.absolute()),
    ]
    assert sorted(result) == sorted(expected_files)


def test_validate_paths(temp_dir: Path):
    """Test that validate_paths returns only the paths that exist."""
    # Create a test file
    test_file = temp_dir / "test_file.txt"
    test_file.write_text("Test file")
    
    # Call the function with one valid and one invalid path
    result = validate_paths([
        str(test_file),
        str(temp_dir / "nonexistent_file.txt"),
    ])
    
    # Assert the result contains only the valid path
    assert result == [str(test_file.absolute())]