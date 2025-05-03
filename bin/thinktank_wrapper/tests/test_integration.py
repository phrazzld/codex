"""Integration tests for thinktank-wrapper."""

import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from thinktank_wrapper import __main__


@pytest.fixture
def temp_template(tmp_path):
    """Create a temporary template for testing."""
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    template_path = template_dir / "test_template.md"
    template_path.write_text("# Test Template\n\nThis is a test template.")
    return template_path


@pytest.fixture
def mock_subprocess_run():
    """Mock subprocess.run for integration tests."""
    with patch("subprocess.run") as mock_run:
        # Configure the mock to return a success result
        mock_run.return_value = subprocess.CompletedProcess(
            args=["thinktank"],
            returncode=0,
            stdout=None,
            stderr=None,
        )
        yield mock_run


@pytest.fixture
def setup_template_path(monkeypatch, temp_template):
    """Set up the template path for importlib.resources."""
    # Mock importlib.resources.files to return our test template directory
    template_parent = temp_template.parent
    
    def mock_files(package_name):
        if package_name == "thinktank_wrapper.templates":
            return template_parent
        return package_name
    
    with patch("importlib.resources.files", side_effect=mock_files):
        yield temp_template


@pytest.fixture
def setup_env_vars(monkeypatch, tmp_path):
    """Set up environment variables for testing."""
    # Create a mock CODEX_DIR with dev philosophy files
    codex_dir = tmp_path / "codex"
    codex_dir.mkdir()
    docs_dir = codex_dir / "docs"
    docs_dir.mkdir()
    philosophy_path = docs_dir / "DEVELOPMENT_PHILOSOPHY.md"
    philosophy_path.write_text("# Test Development Philosophy")
    
    # Set CODEX_DIR environment variable
    monkeypatch.setenv("CODEX_DIR", str(codex_dir))
    
    return codex_dir


@pytest.fixture
def setup_glance_files(tmp_path):
    """Set up glance.md files for testing."""
    # Create glance.md in the temp directory
    glance_path = tmp_path / "glance.md"
    glance_path.write_text("# Test Glance")
    
    return glance_path


def test_integration_template_dry_run(
    setup_template_path, setup_env_vars, setup_glance_files, mock_subprocess_run, capsys
):
    """Test the entire workflow with --template in dry run mode."""
    # Get paths
    template_name = setup_template_path.stem
    glance_path = setup_glance_files
    
    # Run the main function with our test arguments
    args = [
        "--template", template_name,
        "--model-set", "high_context",
        "--include-glance",
        "--include-philosophy",
        "--dry-run",
        str(glance_path),
    ]
    
    # Call main with our args
    exit_code = __main__.main(args)
    
    # Assert exit code is 0 (success)
    assert exit_code == 0
    
    # Assert the dry run output was printed
    captured = capsys.readouterr()
    assert "Would execute: thinktank" in captured.out
    
    # Assert subprocess.run was not called (dry run mode)
    mock_subprocess_run.assert_not_called()


def test_integration_template_execution(
    setup_template_path, setup_env_vars, setup_glance_files, mock_subprocess_run
):
    """Test the entire workflow with --template in execution mode."""
    # Get paths
    template_name = setup_template_path.stem
    glance_path = setup_glance_files
    
    # Run the main function with our test arguments
    args = [
        "--template", template_name,
        "--model-set", "high_context",
        "--include-glance",
        "--include-philosophy",
        str(glance_path),
    ]
    
    # Call main with our args
    exit_code = __main__.main(args)
    
    # Assert exit code is 0 (success)
    assert exit_code == 0
    
    # Assert subprocess.run was called with the expected arguments
    mock_subprocess_run.assert_called_once()
    call_args = mock_subprocess_run.call_args[0][0]
    
    # Assert the command starts with thinktank
    assert call_args[0] == "thinktank"
    
    # Assert it includes the model set
    assert "--model" in call_args
    
    # Assert it includes the instructions file (which should be a temporary file)
    assert "--instructions" in call_args
    
    # Assert it includes the glance path
    assert str(glance_path) in call_args
    
    # Assert it includes at least one philosophy file
    philosophy_included = False
    for arg in call_args:
        if isinstance(arg, str) and "DEVELOPMENT_PHILOSOPHY" in arg:
            philosophy_included = True
            break
    assert philosophy_included


def test_integration_with_instructions(
    setup_env_vars, setup_glance_files, mock_subprocess_run, tmp_path
):
    """Test the workflow with --instructions instead of --template."""
    # Create an instructions file
    instructions_path = tmp_path / "instructions.md"
    instructions_path.write_text("# Test Instructions")
    
    # Get glance path
    glance_path = setup_glance_files
    
    # Run the main function with our test arguments
    args = [
        "--instructions", str(instructions_path),
        "--model-set", "all",
        "--include-glance",
        str(glance_path),
    ]
    
    # Call main with our args
    exit_code = __main__.main(args)
    
    # Assert exit code is 0 (success)
    assert exit_code == 0
    
    # Assert subprocess.run was called with the expected arguments
    mock_subprocess_run.assert_called_once()
    call_args = mock_subprocess_run.call_args[0][0]
    
    # Assert the command starts with thinktank
    assert call_args[0] == "thinktank"
    
    # Assert it includes the instructions file
    assert "--instructions" in call_args
    instructions_index = call_args.index("--instructions")
    assert call_args[instructions_index + 1] == str(instructions_path)
    
    # Assert it includes the glance path
    assert str(glance_path) in call_args


def test_integration_list_templates(
    setup_template_path, capsys
):
    """Test the --list-templates functionality."""
    # Get template name
    template_name = setup_template_path.stem
    
    # Mock sys.exit to avoid actually exiting
    with patch("sys.exit") as mock_exit:
        mock_exit.side_effect = SystemExit(0)
        
        # Run the main function with --list-templates
        with pytest.raises(SystemExit) as excinfo:
            __main__.main(["--list-templates"])
        
        # Assert exit code is 0 (success)
        assert excinfo.value.code == 0
    
    # Assert the template list was printed
    captured = capsys.readouterr()
    assert "Available templates:" in captured.out
    assert template_name in captured.out


def test_integration_error_handling(
    setup_template_path, mock_subprocess_run, capsys
):
    """Test error handling in the integration workflow."""
    # Get template name
    template_name = setup_template_path.stem
    
    # Configure mock_subprocess_run to fail
    mock_subprocess_run.return_value = subprocess.CompletedProcess(
        args=["thinktank"],
        returncode=1,
        stdout=None,
        stderr=None,
    )
    
    # Run the main function with our test arguments
    args = [
        "--template", template_name,
        "--model-set", "high_context",
    ]
    
    # Call main with our args
    exit_code = __main__.main(args)
    
    # Assert exit code is 1 (error)
    assert exit_code == 1