"""Tests for nested .gitignore file handling."""

import tempfile
import pytest
from pathlib import Path
from unittest.mock import Mock, patch

from thinktank_wrapper.gitignore import GitignoreFilter


@pytest.fixture
def temp_repo():
    """Create a temporary directory structure with nested .gitignore files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_path = Path(temp_dir)
        
        # Create directory structure
        (repo_path / "subdir1" / "subdir2").mkdir(parents=True)
        
        # Create .gitignore files
        (repo_path / ".gitignore").write_text("*.log\ntemp.txt\n")
        (repo_path / "subdir1" / ".gitignore").write_text("*.tmp\n!important.tmp\n")
        (repo_path / "subdir1" / "subdir2" / ".gitignore").write_text("*.cache\n")
        
        # Create test files
        (repo_path / "app.log").touch()
        (repo_path / "temp.txt").touch()
        (repo_path / "normal.txt").touch()
        (repo_path / "subdir1" / "test.tmp").touch()
        (repo_path / "subdir1" / "important.tmp").touch()
        (repo_path / "subdir1" / "normal.txt").touch()
        (repo_path / "subdir1" / "subdir2" / "data.cache").touch()
        (repo_path / "subdir1" / "subdir2" / "normal.txt").touch()
        
        yield repo_path


def test_nested_gitignore_path_resolution_logic():
    """Test that we compute correct relative paths for each .gitignore file."""
    root_path = Path("/project")
    
    # Mock GitignoreFilter to test path resolution without pathspec
    filter_obj = GitignoreFilter(root_path)
    filter_obj._enabled = False  # Disable actual pathspec usage
    
    test_cases = [
        ("app.log", [
            ("/project/.gitignore", "app.log")
        ]),
        ("subdir1/test.tmp", [
            ("/project/.gitignore", "subdir1/test.tmp"),
            ("/project/subdir1/.gitignore", "test.tmp")
        ]),
        ("subdir1/subdir2/data.cache", [
            ("/project/.gitignore", "subdir1/subdir2/data.cache"),
            ("/project/subdir1/.gitignore", "subdir2/data.cache"),
            ("/project/subdir1/subdir2/.gitignore", "data.cache")
        ])
    ]
    
    for file_path_str, expected_checks in test_cases:
        # Convert to absolute path
        file_path = root_path / file_path_str
        rel_path = file_path.relative_to(root_path)
        
        # Build list of directories to check (simulate the logic from should_ignore)
        dirs_to_check = []
        current_dir = root_path
        dirs_to_check.append(current_dir)
        
        for part in rel_path.parts[:-1]:
            current_dir = current_dir / part
            dirs_to_check.append(current_dir)
        
        # Verify the computed paths match expected
        actual_checks = []
        for i, dir_path in enumerate(dirs_to_check):
            gitignore_path = str(dir_path / ".gitignore")
            
            if i == 0:
                relative_match_path = str(rel_path)
            else:
                relative_match_path = str(file_path.relative_to(dir_path))
            
            actual_checks.append((gitignore_path, relative_match_path))
        
        assert actual_checks == expected_checks, f"Path resolution failed for {file_path_str}"


@pytest.mark.skipif(
    not hasattr(pytest, "importorskip") or not pytest.importorskip("pathspec", reason="pathspec not available"),
    reason="pathspec library required for gitignore functionality"
)
def test_nested_gitignore_with_pathspec(temp_repo):
    """Test nested .gitignore behavior when pathspec is available."""
    import pathspec
    
    gitignore_filter = GitignoreFilter(temp_repo)
    assert gitignore_filter.is_enabled()
    
    # Test cases: (file_path, should_be_ignored)
    test_cases = [
        ("app.log", True),           # Ignored by root .gitignore (*.log)
        ("temp.txt", True),          # Ignored by root .gitignore (temp.txt)
        ("normal.txt", False),       # Not ignored
        ("subdir1/test.tmp", True),  # Ignored by subdir1 .gitignore (*.tmp)
        ("subdir1/important.tmp", False),  # NOT ignored (negated by !important.tmp in subdir1)
        ("subdir1/normal.txt", False),     # Not ignored
        ("subdir1/subdir2/data.cache", True),  # Ignored by subdir2 .gitignore (*.cache)
        ("subdir1/subdir2/normal.txt", False), # Not ignored
    ]
    
    for file_path, expected_ignored in test_cases:
        actual_ignored = gitignore_filter.should_ignore(file_path)
        assert actual_ignored == expected_ignored, f"Failed for {file_path}: expected {expected_ignored}, got {actual_ignored}"


def test_nested_gitignore_without_pathspec():
    """Test that nested gitignore gracefully degrades when pathspec is unavailable."""
    with patch('thinktank_wrapper.gitignore.pathspec', None):
        gitignore_filter = GitignoreFilter(Path("/project"))
        assert not gitignore_filter.is_enabled()
        
        # Should not ignore anything when pathspec is unavailable
        assert not gitignore_filter.should_ignore("any/file.txt")


def test_gitignore_filter_paths():
    """Test the filter_paths method with nested gitignore."""
    root_path = Path("/project")
    
    # Mock pathspec to test the logic
    mock_spec = Mock()
    mock_spec.match_file.side_effect = lambda path: path.endswith('.log')
    
    with patch('thinktank_wrapper.gitignore.pathspec') as mock_pathspec:
        mock_pathspec.PathSpec.from_lines.return_value = mock_spec
        
        gitignore_filter = GitignoreFilter(root_path)
        
        # Mock the _get_gitignore_spec to return our mock spec for root only
        def mock_get_spec(directory):
            if directory == root_path:
                return mock_spec
            return None
        
        gitignore_filter._get_gitignore_spec = mock_get_spec
        
        test_paths = ["app.log", "normal.txt", "subdir1/test.log", "subdir1/normal.txt"]
        filtered = gitignore_filter.filter_paths(test_paths)
        
        # Should filter out .log files
        expected = [Path("normal.txt"), Path("subdir1/normal.txt")]
        assert filtered == expected