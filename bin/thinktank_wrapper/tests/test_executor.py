"""Tests for the executor module."""

import subprocess
from unittest.mock import patch

import pytest

from thinktank_wrapper.executor import (
    ThinktankExecutionError,
    ThinktankNotFoundError,
    run_command,
)


def test_run_command_dry_run(capsys):
    """Test that run_command in dry run mode prints the command and doesn't execute it."""
    # Set up
    cmd = ["thinktank", "--model", "gpt-4.1", "--instructions", "/path/to/instructions.md"]
    
    # Call the function
    return_code = run_command(cmd, dry_run=True)
    
    # Assert the function returned 0
    assert return_code == 0
    
    # Assert the output contains the command
    captured = capsys.readouterr()
    assert "Would execute:" in captured.out
    assert "thinktank" in captured.out
    assert "--model" in captured.out
    assert "gpt-4.1" in captured.out
    assert "--instructions" in captured.out
    assert "/path/to/instructions.md" in captured.out


def test_run_command_success():
    """Test that run_command successfully executes a command and returns its exit code."""
    # Set up
    cmd = ["thinktank", "--model", "gpt-4.1", "--instructions", "/path/to/instructions.md"]
    
    # Mock subprocess.run to return a CompletedProcess with returncode 0
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = subprocess.CompletedProcess(
            args=cmd,
            returncode=0,
            stdout=None,
            stderr=None,
        )
        
        # Call the function
        return_code = run_command(cmd)
    
    # Assert the function returned the correct exit code
    assert return_code == 0
    
    # Assert subprocess.run was called with the correct arguments
    mock_run.assert_called_once()
    args, kwargs = mock_run.call_args
    assert args[0] == cmd
    assert kwargs["check"] is False
    assert kwargs["shell"] is False
    assert kwargs["text"] is True


def test_run_command_failure():
    """Test that run_command handles command failure correctly."""
    # Set up
    cmd = ["thinktank", "--model", "gpt-4.1", "--instructions", "/path/to/instructions.md"]
    
    # Mock subprocess.run to return a CompletedProcess with returncode 1
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = subprocess.CompletedProcess(
            args=cmd,
            returncode=1,
            stdout=None,
            stderr=None,
        )
        
        # Call the function
        return_code = run_command(cmd)
    
    # Assert the function returned the correct exit code
    assert return_code == 1


def test_run_command_not_found():
    """Test that run_command raises ThinktankNotFoundError when the command is not found."""
    # Set up
    cmd = ["thinktank", "--model", "gpt-4.1", "--instructions", "/path/to/instructions.md"]
    
    # Mock subprocess.run to raise FileNotFoundError
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = FileNotFoundError("No such file or directory: 'thinktank'")
        
        # Call the function and assert it raises ThinktankNotFoundError
        with pytest.raises(ThinktankNotFoundError) as excinfo:
            run_command(cmd)
    
    # Assert the error message
    assert "Thinktank executable not found in PATH" in str(excinfo.value)


def test_run_command_subprocess_error():
    """Test that run_command raises ThinktankExecutionError when subprocess.run raises an error."""
    # Set up
    cmd = ["thinktank", "--model", "gpt-4.1", "--instructions", "/path/to/instructions.md"]
    
    # Mock subprocess.run to raise a subprocess.SubprocessError
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = subprocess.SubprocessError("Subprocess error")
        
        # Call the function and assert it raises ThinktankExecutionError
        with pytest.raises(ThinktankExecutionError) as excinfo:
            run_command(cmd)
    
    # Assert the error attributes
    assert excinfo.value.command == cmd
    assert excinfo.value.return_code == -1
    assert "Subprocess error" in excinfo.value.stderr


def test_thinktank_execution_error_str():
    """Test the string representation of ThinktankExecutionError."""
    # Create an error instance
    cmd = ["thinktank", "--model", "gpt-4.1"]
    error = ThinktankExecutionError(cmd, 1, "Error output")
    
    # Assert the string representation
    error_str = str(error)
    assert "Command 'thinktank --model gpt-4.1'" in error_str
    assert "failed with return code 1" in error_str
    assert "Error output: Error output" in error_str