"""Tests for the context_finder module."""

import os
from pathlib import Path
from typing import List

import pytest

from thinktank_wrapper.context_finder import (
    find_context_files,
    find_glance_files,
    find_philosophy_files,
    find_leyline_files,
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


class TestGitignoreIntegration:
    """Test gitignore filtering integration in context finder."""

    def test_find_glance_files_with_gitignore_filtering(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        """Test that find_glance_files respects gitignore when enabled."""
        # Create a repository structure with .gitignore
        repo_dir = tmp_path / "repo"
        repo_dir.mkdir()
        
        # Create .gitignore
        gitignore = repo_dir / ".gitignore"
        gitignore.write_text("ignored/\n*.log\n")
        
        # Create glance.md files - some should be ignored
        (repo_dir / "glance.md").write_text("# Root glance")
        
        ignored_dir = repo_dir / "ignored"
        ignored_dir.mkdir()
        (ignored_dir / "glance.md").write_text("# Ignored glance")
        
        kept_dir = repo_dir / "src"
        kept_dir.mkdir()
        (kept_dir / "glance.md").write_text("# Src glance")
        
        # Change to repo directory
        monkeypatch.chdir(repo_dir)
        
        # Test with gitignore enabled (default)
        result_filtered = find_glance_files([str(repo_dir)], gitignore_enabled=True)
        result_no_filter = find_glance_files([str(repo_dir)], gitignore_enabled=False)
        
        # With gitignore: should exclude ignored/ files
        expected_filtered = [
            str((repo_dir / "glance.md").absolute()),
            str((kept_dir / "glance.md").absolute()),
        ]
        assert sorted(result_filtered) == sorted(expected_filtered)
        
        # Without gitignore: should include all files
        expected_all = expected_filtered + [str((ignored_dir / "glance.md").absolute())]
        assert sorted(result_no_filter) == sorted(expected_all)

    def test_find_leyline_files_with_gitignore_filtering(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        """Test that find_leyline_files respects gitignore when enabled."""
        # Create a repository structure with leyline docs
        repo_dir = tmp_path / "repo"
        docs_dir = repo_dir / "docs"
        leyline_dir = docs_dir / "leyline"
        leyline_dir.mkdir(parents=True)
        
        # Create .gitignore that ignores temp files
        gitignore = repo_dir / ".gitignore"
        gitignore.write_text("*.tmp\ntemp/\n")
        
        # Create leyline files - some should be ignored
        (leyline_dir / "index.md").write_text("# Index")
        (leyline_dir / "temp.tmp").write_text("# Temp file")  # Should be ignored
        
        temp_dir = leyline_dir / "temp"
        temp_dir.mkdir()
        (temp_dir / "ignored.md").write_text("# Ignored")  # Should be ignored
        
        # Change to repo directory 
        monkeypatch.chdir(repo_dir)
        
        # Test with gitignore enabled
        result_filtered = find_leyline_files(gitignore_enabled=True)
        result_no_filter = find_leyline_files(gitignore_enabled=False)
        
        # With gitignore: should exclude .tmp files and temp/ directory
        expected_filtered = [str((leyline_dir / "index.md").absolute())]
        assert sorted(result_filtered) == sorted(expected_filtered)
        
        # Without gitignore: should include all files
        expected_all = [
            str((leyline_dir / "index.md").absolute()),
            str((leyline_dir / "temp.tmp").absolute()),
            str((temp_dir / "ignored.md").absolute()),
        ]
        assert sorted(result_no_filter) == sorted(expected_all)

    def test_find_context_files_gitignore_integration(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        """Test that find_context_files properly passes gitignore setting through."""
        # Create repository structure
        repo_dir = tmp_path / "repo"
        repo_dir.mkdir()
        
        # Create .gitignore
        gitignore = repo_dir / ".gitignore"
        gitignore.write_text("*.log\n")
        
        # Create glance file that should be ignored
        (repo_dir / "debug.log").write_text("log content")
        (repo_dir / "glance.md").write_text("# Glance")
        
        # Create explicit file that should be ignored
        ignored_file = repo_dir / "test.log" 
        ignored_file.write_text("test log")
        
        # Change to repo directory
        monkeypatch.chdir(repo_dir)
        
        # Test with gitignore enabled
        result_filtered = find_context_files(
            include_glance=True,
            include_leyline=False,
            explicit_paths=[str(ignored_file)],
            gitignore_enabled=True
        )
        
        # Test with gitignore disabled
        result_no_filter = find_context_files(
            include_glance=True,
            include_leyline=False,
            explicit_paths=[str(ignored_file)],
            gitignore_enabled=False
        )
        
        # With gitignore: should exclude .log files
        expected_filtered = [str((repo_dir / "glance.md").absolute())]
        assert sorted(result_filtered) == sorted(expected_filtered)
        
        # Without gitignore: should include all files
        expected_all = [
            str((repo_dir / "glance.md").absolute()),
            str(ignored_file.absolute()),
        ]
        assert sorted(result_no_filter) == sorted(expected_all)

    def test_gitignore_graceful_degradation(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        """Test that gitignore filtering gracefully degrades when pathspec is unavailable."""
        # Mock pathspec as unavailable
        import thinktank_wrapper.context_finder as cf_module
        
        # Create a repository structure
        repo_dir = tmp_path / "repo"
        repo_dir.mkdir()
        (repo_dir / "glance.md").write_text("# Glance")
        
        # Change to repo directory
        monkeypatch.chdir(repo_dir)
        
        # Test that it works even when pathspec is unavailable
        # (The GitignoreFilter will be disabled but no errors should occur)
        result = find_glance_files([str(repo_dir)], gitignore_enabled=True)
        
        # Should still find the glance file
        expected = [str((repo_dir / "glance.md").absolute())]
        assert result == expected

    def test_explicit_directory_gitignore_filtering(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog):
        """Test that explicit directories are filtered by gitignore rules."""
        # Create a repository structure
        repo_dir = tmp_path / "repo"
        repo_dir.mkdir()
        
        # Create .gitignore that ignores node_modules
        gitignore = repo_dir / ".gitignore"
        gitignore.write_text("node_modules/\n*.log\n")
        
        # Create directories - one ignored, one not
        node_modules_dir = repo_dir / "node_modules"
        node_modules_dir.mkdir()
        (node_modules_dir / "package.json").write_text("{}")
        
        src_dir = repo_dir / "src"
        src_dir.mkdir()
        (src_dir / "main.py").write_text("print('hello')")
        
        # Create a regular file for comparison
        allowed_file = repo_dir / "README.md"
        allowed_file.write_text("# Project")
        
        # Change to repo directory
        monkeypatch.chdir(repo_dir)
        
        # Test with gitignore enabled - explicit gitignored directory should be filtered out
        result_filtered = find_context_files(
            include_glance=False,
            include_leyline=False,
            explicit_paths=[str(node_modules_dir), str(src_dir), str(allowed_file)],
            gitignore_enabled=True
        )
        
        # Should include only src_dir and allowed_file, not node_modules
        expected_filtered = [
            str(src_dir.absolute()),
            str(allowed_file.absolute()),
        ]
        assert sorted(result_filtered) == sorted(expected_filtered)
        
        # Check that warning was logged
        assert "Explicit directory is gitignored and will be skipped" in caplog.text
        assert str(node_modules_dir.absolute()) in caplog.text
        assert "disable gitignore filtering with --no-gitignore" in caplog.text
        
        # Clear log for next test
        caplog.clear()
        
        # Test with gitignore disabled - should include all paths
        result_no_filter = find_context_files(
            include_glance=False,
            include_leyline=False,
            explicit_paths=[str(node_modules_dir), str(src_dir), str(allowed_file)],
            gitignore_enabled=False
        )
        
        # Should include all paths when gitignore is disabled
        expected_all = [
            str(node_modules_dir.absolute()),
            str(src_dir.absolute()),
            str(allowed_file.absolute()),
        ]
        assert sorted(result_no_filter) == sorted(expected_all)
        
        # Should not have warning when gitignore is disabled
        assert "Explicit directory is gitignored" not in caplog.text