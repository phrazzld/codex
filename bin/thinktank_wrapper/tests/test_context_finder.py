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
        include_philosophy=True,
        explicit_paths=[str(test_file)]
    )
    
    # Assert the result contains the glance files, philosophy files, and explicit path
    expected_files = [
        str(test_file.absolute()),
    ]
    
    # Add the mock glance files
    for glance_file in mock_glance_files:
        expected_files.append(str(glance_file.absolute()))
    
    # Add the mock philosophy files
    expected_files.append(str((mock_codex_dir / "docs" / "DEVELOPMENT_PHILOSOPHY.md").absolute()))
    expected_files.append(
        str((mock_codex_dir / "docs" / "DEVELOPMENT_PHILOSOPHY_APPENDIX_TYPESCRIPT.md").absolute())
    )
    
    # Sort both lists for comparison
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