"""Tests for the gitignore module."""

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from thinktank_wrapper.gitignore import GitignoreFilter, create_gitignore_filter, is_gitignore_available


@pytest.fixture
def temp_repo(tmp_path):
    """Create a temporary repository structure with .gitignore files."""
    repo = tmp_path / "test_repo"
    repo.mkdir()
    
    # Root .gitignore
    root_gitignore = repo / ".gitignore"
    root_gitignore.write_text("""
# Root gitignore
*.log
*.tmp
node_modules/
build/
.env
""")
    
    # Create directory structure
    (repo / "src").mkdir()
    (repo / "src" / "main.py").write_text("print('hello')")
    (repo / "src" / "test.log").write_text("log content")
    
    (repo / "docs").mkdir()
    (repo / "docs" / "readme.md").write_text("# README")
    
    # Subdirectory with its own .gitignore
    subdir = repo / "subproject"
    subdir.mkdir()
    sub_gitignore = subdir / ".gitignore"
    sub_gitignore.write_text("""
# Subproject gitignore
*.pyc
temp/
""")
    (subdir / "app.py").write_text("app code")
    (subdir / "module.pyc").write_text("compiled")
    
    # Nested ignored directory
    (repo / "node_modules").mkdir()
    (repo / "node_modules" / "package.json").write_text("{}")
    
    (repo / "build").mkdir()
    (repo / "build" / "output.bin").write_text("binary")
    
    # Files that should not be ignored
    (repo / "config.yaml").write_text("config")
    (repo / ".env.example").write_text("example")
    
    return repo


@pytest.fixture
def gitignore_filter(temp_repo):
    """Create a GitignoreFilter for the test repository."""
    return GitignoreFilter(temp_repo)


class TestGitignoreFilter:
    """Test the GitignoreFilter class."""
    
    def test_init(self, temp_repo):
        """Test GitignoreFilter initialization."""
        filter_obj = GitignoreFilter(temp_repo)
        assert filter_obj.root_path == temp_repo.resolve()
        assert isinstance(filter_obj._spec_cache, dict)
    
    def test_is_enabled(self, gitignore_filter):
        """Test that gitignore filtering is enabled when pathspec is available."""
        # This test assumes pathspec is available during testing
        assert gitignore_filter.is_enabled()
    
    def test_should_ignore_root_patterns(self, gitignore_filter, temp_repo):
        """Test that files matching root .gitignore patterns are ignored."""
        # Files that should be ignored
        assert gitignore_filter.should_ignore("test.log")
        assert gitignore_filter.should_ignore("src/test.log")
        assert gitignore_filter.should_ignore("node_modules/package.json")
        assert gitignore_filter.should_ignore("build/output.bin")
        assert gitignore_filter.should_ignore(".env")
        
        # Files that should not be ignored
        assert not gitignore_filter.should_ignore("src/main.py")
        assert not gitignore_filter.should_ignore("docs/readme.md")
        assert not gitignore_filter.should_ignore("config.yaml")
        assert not gitignore_filter.should_ignore(".env.example")
    
    def test_should_ignore_subdirectory_patterns(self, gitignore_filter, temp_repo):
        """Test that files matching subdirectory .gitignore patterns are ignored."""
        # Files that should be ignored by subproject .gitignore
        assert gitignore_filter.should_ignore("subproject/module.pyc")
        
        # Files that should not be ignored
        assert not gitignore_filter.should_ignore("subproject/app.py")
    
    def test_should_ignore_absolute_paths(self, gitignore_filter, temp_repo):
        """Test gitignore matching with absolute paths."""
        log_file = temp_repo / "src" / "test.log"
        py_file = temp_repo / "src" / "main.py"
        
        assert gitignore_filter.should_ignore(log_file)
        assert not gitignore_filter.should_ignore(py_file)
    
    def test_should_ignore_outside_root(self, gitignore_filter, tmp_path):
        """Test that files outside root directory are not ignored."""
        outside_file = tmp_path / "outside.log"
        outside_file.write_text("content")
        
        assert not gitignore_filter.should_ignore(outside_file)
    
    def test_filter_paths(self, gitignore_filter, temp_repo):
        """Test filtering a list of paths."""
        paths = [
            "src/main.py",
            "src/test.log",
            "docs/readme.md", 
            "node_modules/package.json",
            "config.yaml",
            "subproject/app.py",
            "subproject/module.pyc"
        ]
        
        filtered = gitignore_filter.filter_paths(paths)
        filtered_strs = [str(p) for p in filtered]
        
        # Should keep these files
        assert "src/main.py" in filtered_strs
        assert "docs/readme.md" in filtered_strs
        assert "config.yaml" in filtered_strs
        assert "subproject/app.py" in filtered_strs
        
        # Should filter out these files
        assert "src/test.log" not in filtered_strs
        assert "node_modules/package.json" not in filtered_strs
        assert "subproject/module.pyc" not in filtered_strs
    
    def test_clear_cache(self, gitignore_filter, temp_repo):
        """Test clearing the gitignore spec cache."""
        # Trigger cache loading
        gitignore_filter.should_ignore("test.log")
        assert len(gitignore_filter._spec_cache) > 0
        
        # Clear cache
        gitignore_filter.clear_cache()
        assert len(gitignore_filter._spec_cache) == 0
    
    def test_empty_gitignore(self, tmp_path):
        """Test handling of empty .gitignore files."""
        repo = tmp_path / "empty_repo"
        repo.mkdir()
        
        # Create empty .gitignore
        (repo / ".gitignore").write_text("")
        (repo / "test.txt").write_text("content")
        
        filter_obj = GitignoreFilter(repo)
        assert not filter_obj.should_ignore("test.txt")
    
    def test_comments_and_empty_lines(self, tmp_path):
        """Test that comments and empty lines in .gitignore are handled correctly."""
        repo = tmp_path / "comment_repo"
        repo.mkdir()
        
        gitignore_content = """
# This is a comment
*.log

# Another comment
temp/

# Empty line above should be ignored
"""
        (repo / ".gitignore").write_text(gitignore_content)
        (repo / "test.log").write_text("log")
        (repo / "normal.txt").write_text("text")
        
        filter_obj = GitignoreFilter(repo)
        assert filter_obj.should_ignore("test.log")
        assert not filter_obj.should_ignore("normal.txt")
    
    def test_invalid_gitignore(self, tmp_path, caplog):
        """Test handling of invalid .gitignore files."""
        repo = tmp_path / "invalid_repo"
        repo.mkdir()
        
        # Create .gitignore with binary content (should be handled gracefully)
        gitignore_path = repo / ".gitignore"
        gitignore_path.write_bytes(b'\x00\x01\x02binary content')
        
        filter_obj = GitignoreFilter(repo)
        # Should not crash and should not ignore files when gitignore is invalid
        assert not filter_obj.should_ignore("test.txt")


class TestGitignoreDisabled:
    """Test GitignoreFilter behavior when pathspec is not available."""
    
    @patch('thinktank_wrapper.gitignore.pathspec', None)
    def test_disabled_filter(self, tmp_path):
        """Test that GitignoreFilter works when pathspec is not available."""
        repo = tmp_path / "test_repo"
        repo.mkdir()
        (repo / ".gitignore").write_text("*.log")
        (repo / "test.log").write_text("log")
        
        filter_obj = GitignoreFilter(repo)
        assert not filter_obj.is_enabled()
        assert not filter_obj.should_ignore("test.log")  # Should not ignore anything
        
        paths = ["test.log", "main.py"]
        filtered = filter_obj.filter_paths(paths)
        assert len(filtered) == 2  # Should return all paths


class TestModuleFunctions:
    """Test module-level utility functions."""
    
    def test_create_gitignore_filter(self, temp_repo):
        """Test creating a GitignoreFilter through the factory function."""
        filter_obj = create_gitignore_filter(temp_repo)
        assert isinstance(filter_obj, GitignoreFilter)
        assert filter_obj.root_path == temp_repo.resolve()
    
    def test_is_gitignore_available(self):
        """Test checking if gitignore functionality is available."""
        # This assumes pathspec is available during testing
        assert is_gitignore_available()
    
    @patch('thinktank_wrapper.gitignore.pathspec', None)
    def test_is_gitignore_available_disabled(self):
        """Test gitignore availability check when pathspec is not available."""
        from thinktank_wrapper.gitignore import is_gitignore_available
        assert not is_gitignore_available()


class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_nonexistent_directory(self):
        """Test GitignoreFilter with non-existent directory."""
        filter_obj = GitignoreFilter("/non/existent/path")
        # Should not crash
        assert not filter_obj.should_ignore("any/file.txt")
    
    def test_file_as_root(self, tmp_path):
        """Test GitignoreFilter when root path is a file, not directory."""
        file_path = tmp_path / "not_a_dir.txt"
        file_path.write_text("content")
        
        # Should handle gracefully
        filter_obj = GitignoreFilter(file_path)
        assert not filter_obj.should_ignore("test.txt")
    
    def test_symlink_gitignore(self, tmp_path):
        """Test handling of .gitignore that is a symlink."""
        repo = tmp_path / "symlink_repo"
        repo.mkdir()
        
        # Create actual gitignore file
        actual_gitignore = tmp_path / "actual_gitignore"
        actual_gitignore.write_text("*.log")
        
        # Create symlink
        symlink_gitignore = repo / ".gitignore"
        try:
            symlink_gitignore.symlink_to(actual_gitignore)
            
            filter_obj = GitignoreFilter(repo)
            assert filter_obj.should_ignore("test.log")
        except OSError:
            # Skip test if symlinks are not supported (e.g., Windows without admin rights)
            pytest.skip("Symlinks not supported on this system")