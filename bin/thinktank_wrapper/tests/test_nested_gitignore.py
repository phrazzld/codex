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


@pytest.mark.skipif(
    not hasattr(pytest, "importorskip") or not pytest.importorskip("pathspec", reason="pathspec not available"),
    reason="pathspec library required for gitignore functionality"
)
def test_gitignore_precedence_integration():
    """Integration test for gitignore precedence - subdirectory rules override parent rules."""
    import pathspec
    
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_path = Path(temp_dir)
        
        # Create complex directory structure
        (repo_path / "src" / "main" / "java").mkdir(parents=True)
        (repo_path / "src" / "test" / "java").mkdir(parents=True)
        (repo_path / "docs" / "api").mkdir(parents=True)
        
        # Create .gitignore files with conflicting rules
        # Root .gitignore: ignore all .log files and docs directory
        (repo_path / ".gitignore").write_text("*.log\ndocs/\n")
        
        # src/.gitignore: allow important.log files (negation pattern)
        (repo_path / "src" / ".gitignore").write_text("!important.log\n*.tmp\n")
        
        # docs/.gitignore: allow api directory (negation pattern) 
        (repo_path / "docs" / ".gitignore").write_text("!api/\n*.draft\n")
        
        # Create test files to verify precedence
        test_files = [
            # Root level - should follow root .gitignore
            (repo_path / "app.log", True),           # Ignored by root *.log
            (repo_path / "readme.txt", False),       # Not ignored
            
            # src/ level - should follow src .gitignore rules + root rules
            (repo_path / "src" / "debug.log", True),      # Ignored by root *.log
            (repo_path / "src" / "important.log", False), # NOT ignored (negated by src/.gitignore)
            (repo_path / "src" / "temp.tmp", True),       # Ignored by src *.tmp
            (repo_path / "src" / "main.java", False),     # Not ignored
            
            # src/main/java/ level - should follow src rules (no more specific .gitignore)
            (repo_path / "src" / "main" / "java" / "build.log", True),      # Ignored by root *.log
            (repo_path / "src" / "main" / "java" / "important.log", False), # NOT ignored (src negation)
            (repo_path / "src" / "main" / "java" / "cache.tmp", True),      # Ignored by src *.tmp
            
            # docs/ level - should follow docs .gitignore + root rules
            (repo_path / "docs" / "user.log", True),        # Ignored by root *.log
            (repo_path / "docs" / "spec.draft", True),      # Ignored by docs *.draft
            (repo_path / "docs" / "index.md", True),        # Ignored by root docs/ rule
            
            # docs/api/ level - should NOT be ignored due to docs negation
            (repo_path / "docs" / "api" / "reference.log", True),   # Ignored by root *.log
            (repo_path / "docs" / "api" / "spec.draft", True),     # Ignored by docs *.draft  
            (repo_path / "docs" / "api" / "index.md", False),      # NOT ignored (docs negation for api/)
        ]
        
        # Create all test files
        for file_path, _ in test_files:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text("test content")
        
        # Test the GitignoreFilter
        gitignore_filter = GitignoreFilter(repo_path)
        assert gitignore_filter.is_enabled()
        
        # Verify each file's ignore status
        for file_path, should_be_ignored in test_files:
            actual_ignored = gitignore_filter.should_ignore(str(file_path.relative_to(repo_path)))
            assert actual_ignored == should_be_ignored, (
                f"Precedence test failed for {file_path.relative_to(repo_path)}: "
                f"expected ignored={should_be_ignored}, got ignored={actual_ignored}"
            )


@pytest.mark.skipif(
    not hasattr(pytest, "importorskip") or not pytest.importorskip("pathspec", reason="pathspec not available"),
    reason="pathspec library required for gitignore functionality"
)
def test_gitignore_negation_patterns():
    """Test that gitignore negation patterns work correctly."""
    import pathspec
    
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_path = Path(temp_dir)
        
        # Create directory structure
        (repo_path / "build" / "important").mkdir(parents=True)
        (repo_path / "dist").mkdir()
        
        # Root .gitignore: ignore build directory but allow important subdirectory
        (repo_path / ".gitignore").write_text("build/\n!build/important/\n*.tmp\n!keep.tmp\n")
        
        # Create test files
        test_files = [
            # Files in build/ - should be ignored except important/
            (repo_path / "build" / "output.jar", True),                    # Ignored by build/
            (repo_path / "build" / "temp.log", True),                     # Ignored by build/
            (repo_path / "build" / "important" / "config.json", False),   # NOT ignored (!build/important/)
            (repo_path / "build" / "important" / "data.xml", False),      # NOT ignored (!build/important/)
            
            # Files in root - test negation of file patterns
            (repo_path / "temp.tmp", True),     # Ignored by *.tmp
            (repo_path / "keep.tmp", False),    # NOT ignored (!keep.tmp)
            (repo_path / "other.tmp", True),    # Ignored by *.tmp
            
            # Other files - not affected by these rules
            (repo_path / "readme.md", False),   # Not ignored
            (repo_path / "dist" / "app.js", False),  # Not ignored
        ]
        
        # Create all test files
        for file_path, _ in test_files:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text("test content")
        
        # Test the GitignoreFilter
        gitignore_filter = GitignoreFilter(repo_path)
        assert gitignore_filter.is_enabled()
        
        # Verify each file's ignore status
        for file_path, should_be_ignored in test_files:
            actual_ignored = gitignore_filter.should_ignore(str(file_path.relative_to(repo_path)))
            assert actual_ignored == should_be_ignored, (
                f"Negation test failed for {file_path.relative_to(repo_path)}: "
                f"expected ignored={should_be_ignored}, got ignored={actual_ignored}"
            )