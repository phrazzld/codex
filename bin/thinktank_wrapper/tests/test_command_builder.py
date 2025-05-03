"""Tests for the command_builder module."""

import argparse
import os
import tempfile
from typing import List, Optional, Tuple
from unittest.mock import patch

import pytest

from thinktank_wrapper import command_builder, config
from thinktank_wrapper.command_builder import CommandBuilderError


@pytest.fixture
def mock_args():
    """Create a mock args namespace for testing."""
    args = argparse.Namespace()
    args.model_set = "all"
    args.instructions = None
    args.context_files = ["/path/to/file1.md", "/path/to/file2.md"]
    args.dry_run = False
    return args


def test_add_model_args():
    """Test that _add_model_args adds the correct model arguments."""
    # Set up
    cmd_args: List[str] = []
    
    # Call the function
    command_builder._add_model_args(cmd_args, "all")
    
    # Assert the correct model arguments were added
    assert "--model" in cmd_args
    assert len(cmd_args) >= len(config.MODELS_ALL) * 2  # Each model has two args: --model and the model name
    assert "--synthesis-model" in cmd_args
    assert config.SYNTHESIS_MODEL in cmd_args


def test_add_model_args_invalid_model_set():
    """Test that _add_model_args raises CommandBuilderError for an invalid model set."""
    # Set up
    cmd_args: List[str] = []
    
    # Call the function and assert it raises CommandBuilderError
    with pytest.raises(CommandBuilderError):
        command_builder._add_model_args(cmd_args, "invalid_model_set")


def test_build_command_with_instructions(mock_args):
    """Test that build_command correctly builds a command with instructions."""
    # Set up
    mock_args.instructions = "/path/to/instructions.md"
    unknown_args: List[str] = []
    
    # Call the function
    cmd_args, temp_file_path = command_builder.build_command(mock_args, unknown_args)
    
    # Assert the command is built correctly
    assert cmd_args[0] == "thinktank"
    assert config.INSTRUCTIONS_ARG in cmd_args
    assert "/path/to/instructions.md" in cmd_args
    assert mock_args.context_files[0] in cmd_args
    assert mock_args.context_files[1] in cmd_args
    
    # Assert no temporary file was created
    assert temp_file_path is None


def test_build_command_with_template_content(mock_args):
    """Test that build_command correctly builds a command with template content."""
    # Set up
    unknown_args: List[str] = []
    template_content = "# Test template content"
    
    # Use a patch for tempfile.mkstemp to control the temp file creation
    with patch("tempfile.mkstemp") as mock_mkstemp:
        # Set up the mock to return a file descriptor and a known path
        mock_fd, mock_path = 123, "/tmp/thinktank-template-12345.md"
        mock_mkstemp.return_value = (mock_fd, mock_path)
        
        # Also patch os.fdopen to prevent actual file operations
        with patch("os.fdopen") as mock_fdopen:
            # Call the function
            cmd_args, temp_file_path = command_builder.build_command(
                mock_args, unknown_args, template_content
            )
    
    # Assert the command is built correctly
    assert cmd_args[0] == "thinktank"
    assert config.INSTRUCTIONS_ARG in cmd_args
    assert mock_path in cmd_args  # The temp file path should be in the command
    assert mock_args.context_files[0] in cmd_args
    assert mock_args.context_files[1] in cmd_args
    
    # Assert the temporary file path was returned
    assert temp_file_path == mock_path


def test_build_command_with_unknown_args(mock_args):
    """Test that build_command correctly handles unknown arguments."""
    # Set up
    mock_args.instructions = "/path/to/instructions.md"
    unknown_args = ["--unknown-flag", "value", "--another-flag"]
    
    # Call the function
    cmd_args, _ = command_builder.build_command(mock_args, unknown_args)
    
    # Assert the unknown arguments are included in the command
    assert "--unknown-flag" in cmd_args
    assert "value" in cmd_args
    assert "--another-flag" in cmd_args


def test_build_command_no_instructions_no_template():
    """Test that build_command raises CommandBuilderError when neither instructions nor template content is provided."""
    # Set up
    args = argparse.Namespace()
    args.instructions = None
    args.context_files = []
    unknown_args: List[str] = []
    
    # Call the function and assert it raises CommandBuilderError
    with pytest.raises(CommandBuilderError):
        command_builder.build_command(args, unknown_args)


def test_build_command_io_error(mock_args):
    """Test that build_command handles IO errors during temporary file creation."""
    # Set up
    unknown_args: List[str] = []
    template_content = "# Test template content"
    
    # Use a patch for tempfile.mkstemp to control the temp file creation
    with patch("tempfile.mkstemp") as mock_mkstemp:
        # Set up the mock to return a file descriptor and a known path
        mock_fd, mock_path = 123, "/tmp/thinktank-template-12345.md"
        mock_mkstemp.return_value = (mock_fd, mock_path)
        
        # Also patch os.fdopen to raise an IOError
        with patch("os.fdopen") as mock_fdopen:
            mock_fdopen.side_effect = IOError("Mock IO error")
            
            # Also patch os.unlink to prevent actual file deletion
            with patch("os.unlink") as mock_unlink:
                # Call the function and assert it raises CommandBuilderError
                with pytest.raises(CommandBuilderError):
                    command_builder.build_command(
                        mock_args, unknown_args, template_content
                    )
                
                # Assert the cleanup was attempted
                mock_unlink.assert_called_once_with(mock_path)