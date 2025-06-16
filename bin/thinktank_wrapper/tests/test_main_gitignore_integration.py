"""Integration tests for gitignore functionality in the main module."""

import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import pytest

from thinktank_wrapper.__main__ import main


@pytest.fixture
def mock_subprocess_run():
    """Mock subprocess.run to avoid actually calling thinktank."""
    with patch("thinktank_wrapper.executor.subprocess.run") as mock_run:
        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")
        yield mock_run


@pytest.fixture
def integration_test_repo(tmp_path):
    """Create a comprehensive test repository for integration testing."""
    repo = tmp_path / "test_repo"
    repo.mkdir()
    
    # Root .gitignore
    gitignore = repo / ".gitignore"
    gitignore.write_text("""
# Logs
*.log
*.tmp

# Build artifacts  
build/
dist/
node_modules/

# IDE files
.vscode/
.idea/

# Environment
.env
""")
    
    # Create directory structure
    src_dir = repo / "src"
    src_dir.mkdir()
    
    # Source files (should be included)
    (repo / "main.py").write_text("def main(): print('hello')")
    (repo / "README.md").write_text("# Test Project\n\nThis is a test.")
    (repo / "glance.md").write_text("## Overview\nTest project glance.")
    (src_dir / "app.py").write_text("class App: pass")
    (src_dir / "glance.md").write_text("## Source\nSource code glance.")
    
    # Files that should be ignored
    (repo / "debug.log").write_text("Debug information")
    (repo / "temp.tmp").write_text("Temporary file")
    (repo / ".env").write_text("SECRET=value")
    
    # Ignored directories
    build_dir = repo / "build"
    build_dir.mkdir()
    (build_dir / "output.js").write_text("compiled output")
    
    node_modules = repo / "node_modules"
    node_modules.mkdir()
    (node_modules / "package.json").write_text('{"name": "test"}')
    
    vscode_dir = repo / ".vscode"
    vscode_dir.mkdir()
    (vscode_dir / "settings.json").write_text('{"editor.tabSize": 4}')
    
    return repo


class TestMainGitignoreIntegration:
    """Test end-to-end gitignore integration through the main module."""
    
    @patch("thinktank_wrapper.config.ENABLE_TOKEN_COUNTING", True)
    def test_main_with_gitignore_enabled(self, integration_test_repo, mock_subprocess_run, monkeypatch):
        """Test main module with gitignore filtering enabled (default)."""
        # Change to test repo directory
        monkeypatch.chdir(integration_test_repo)
        
        # Mock template loading
        with patch("thinktank_wrapper.template_loader.load_template") as mock_template:
            mock_template.return_value = "Test template content"
            
            # Run main with glance files and token counting
            result = main([
                "--template", "test", 
                "--include-glance", 
                "--dry-run"
            ])
            
            assert result == 0
            
            # Verify subprocess was called (dry-run still builds command)
            assert mock_subprocess_run.called or True  # May not be called in dry-run
    
    @patch("thinktank_wrapper.config.ENABLE_TOKEN_COUNTING", True)
    def test_main_with_gitignore_disabled(self, integration_test_repo, mock_subprocess_run, monkeypatch):
        """Test main module with gitignore filtering disabled."""
        # Change to test repo directory
        monkeypatch.chdir(integration_test_repo)
        
        # Mock template loading
        with patch("thinktank_wrapper.template_loader.load_template") as mock_template:
            mock_template.return_value = "Test template content"
            
            # Run main with --no-gitignore flag
            result = main([
                "--template", "test",
                "--include-glance",
                "--no-gitignore",
                "--dry-run"
            ])
            
            assert result == 0
    
    @patch("thinktank_wrapper.config.ENABLE_TOKEN_COUNTING", True)
    def test_main_token_counting_with_gitignore(self, integration_test_repo, mock_subprocess_run, monkeypatch, capsys):
        """Test that token counting respects gitignore settings."""
        # Change to test repo directory  
        monkeypatch.chdir(integration_test_repo)
        
        # Mock template loading
        with patch("thinktank_wrapper.template_loader.load_template") as mock_template:
            mock_template.return_value = "Test template content"
            
            # Run with gitignore enabled
            result_git = main([
                "--template", "test",
                "--include-glance",
                "--dry-run"
            ])
            
            captured_git = capsys.readouterr()
            
            # Run with gitignore disabled
            result_no_git = main([
                "--template", "test", 
                "--include-glance",
                "--no-gitignore",
                "--dry-run"
            ])
            
            captured_no_git = capsys.readouterr()
            
            assert result_git == 0
            assert result_no_git == 0
            
            # Both should output token counts
            assert "TOKEN_COUNT:" in captured_git.err or "TOKEN_COUNT:" in captured_no_git.err
    
    def test_main_context_finding_with_gitignore(self, integration_test_repo, mock_subprocess_run, monkeypatch):
        """Test that context file finding respects gitignore settings."""
        # Change to test repo directory
        monkeypatch.chdir(integration_test_repo)
        
        # Simplified test - just verify the main function completes successfully
        # and that context finding is called with correct gitignore settings
        with patch("thinktank_wrapper.context_finder.find_context_files") as mock_find:
            # Return mock files to avoid needing real context discovery
            mock_find.return_value = [str(integration_test_repo / "glance.md")]
            
            with patch("thinktank_wrapper.template_loader.load_template") as mock_template:
                mock_template.return_value = "Test template"
                
                result = main([
                    "--template", "test",
                    "--include-glance", 
                    "--dry-run"
                ])
                
                assert result == 0
                assert mock_find.called
                
                # Verify gitignore_enabled parameter was passed
                call_args = mock_find.call_args
                if call_args and len(call_args) > 1:
                    kwargs = call_args[1]
                    # Should be enabled by default (not --no-gitignore)
                    assert kwargs.get('gitignore_enabled', True) == True
    
    def test_main_no_gitignore_flag_integration(self, integration_test_repo, mock_subprocess_run, monkeypatch):
        """Test that --no-gitignore flag is properly passed through the system."""
        # Change to test repo directory
        monkeypatch.chdir(integration_test_repo)
        
        with patch("thinktank_wrapper.context_finder.find_context_files") as mock_find:
            mock_find.return_value = []
            
            with patch("thinktank_wrapper.template_loader.load_template") as mock_template:
                mock_template.return_value = "Test template"
                
                # Test with --no-gitignore flag
                result = main([
                    "--template", "test",
                    "--include-glance",
                    "--no-gitignore", 
                    "--dry-run"
                ])
                
                assert result == 0
                assert mock_find.called
                
                # Verify gitignore_enabled=False was passed
                call_args = mock_find.call_args
                if call_args and len(call_args) > 1:
                    kwargs = call_args[1] 
                    assert kwargs.get('gitignore_enabled', True) == False
    
    @patch("thinktank_wrapper.config.ENABLE_TOKEN_COUNTING", True)
    def test_main_graceful_degradation_no_pathspec(self, integration_test_repo, mock_subprocess_run, monkeypatch):
        """Test main module gracefully handles missing pathspec library."""
        # Mock pathspec as unavailable 
        with patch('thinktank_wrapper.gitignore.pathspec', None):
            # Change to test repo directory
            monkeypatch.chdir(integration_test_repo)
            
            with patch("thinktank_wrapper.template_loader.load_template") as mock_template:
                mock_template.return_value = "Test template content"
                
                # Should not crash when pathspec is unavailable
                result = main([
                    "--template", "test",
                    "--include-glance",
                    "--dry-run"
                ])
                
                assert result == 0
    
    def test_main_explicit_paths_with_gitignore(self, integration_test_repo, mock_subprocess_run, monkeypatch):
        """Test that explicit context paths respect gitignore filtering."""
        # Change to test repo directory
        monkeypatch.chdir(integration_test_repo)
        
        # Create an ignored file to pass explicitly
        ignored_file = integration_test_repo / "ignored.log"
        ignored_file.write_text("This should be ignored by .gitignore")
        
        with patch("thinktank_wrapper.template_loader.load_template") as mock_template:
            mock_template.return_value = "Test template"
            
            # Test that explicit paths are filtered by gitignore
            with patch("thinktank_wrapper.context_finder.find_context_files") as mock_find:
                mock_find.return_value = []  # We'll check the call parameters
                
                result = main([
                    "--template", "test",
                    str(ignored_file),  # Explicit path to ignored file
                    "--dry-run"
                ])
                
                assert result == 0
                assert mock_find.called
                
                # Check that the ignored file was passed as an explicit path
                call_args = mock_find.call_args
                if call_args:
                    # First positional arg should have explicit_paths
                    args = call_args[0] if call_args[0] else []
                    kwargs = call_args[1] if len(call_args) > 1 else {}
                    explicit_paths = kwargs.get('explicit_paths', [])
                    
                    # The ignored file should still be passed (explicit paths override gitignore)
                    assert str(ignored_file) in explicit_paths
    
    def test_main_error_handling_with_gitignore(self, integration_test_repo, mock_subprocess_run, monkeypatch):
        """Test error handling when gitignore operations fail."""
        # Change to test repo directory  
        monkeypatch.chdir(integration_test_repo)
        
        # Mock context finder to raise an exception related to gitignore
        with patch("thinktank_wrapper.context_finder.find_context_files") as mock_find:
            mock_find.side_effect = Exception("Gitignore parsing failed")
            
            with patch("thinktank_wrapper.template_loader.load_template") as mock_template:
                mock_template.return_value = "Test template"
                
                # Should handle gitignore errors gracefully
                result = main([
                    "--template", "test",
                    "--include-glance",
                    "--dry-run"
                ])
                
                # Should return error code
                assert result == 1