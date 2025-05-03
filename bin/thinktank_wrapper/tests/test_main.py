"""Tests for the __main__ module."""

import os
import sys
from unittest.mock import MagicMock, patch

import pytest

from thinktank_wrapper import __main__, command_builder, executor, template_loader


@pytest.fixture
def mock_setup_logging():
    """Mock the logging setup."""
    with patch("thinktank_wrapper.logging_config.setup_logging") as mock:
        mock.return_value = "mock-correlation-id"
        yield mock


@pytest.fixture
def mock_parse_args():
    """Mock the argument parsing."""
    with patch("thinktank_wrapper.cli.parse_args") as mock:
        # Create mock parsed args
        args = MagicMock()
        args.list_templates = False
        args.template = "test-template"
        args.instructions = None
        args.include_glance = True
        args.include_philosophy = True
        args.context_paths = ["/path/to/file.md"]
        args.dry_run = False
        
        # Return the mock args and empty unknown args
        mock.return_value = (args, [])
        yield mock


@pytest.fixture
def mock_validate_args():
    """Mock the argument validation."""
    with patch("thinktank_wrapper.cli.validate_args") as mock:
        yield mock


@pytest.fixture
def mock_find_context_files():
    """Mock the context file finding."""
    with patch("thinktank_wrapper.context_finder.find_context_files") as mock:
        mock.return_value = ["/path/to/context1.md", "/path/to/context2.md"]
        yield mock


@pytest.fixture
def mock_load_template():
    """Mock the template loading."""
    with patch("thinktank_wrapper.template_loader.load_template") as mock:
        mock.return_value = "# Mock template content"
        yield mock


@pytest.fixture
def mock_build_command():
    """Mock the command building."""
    with patch("thinktank_wrapper.command_builder.build_command") as mock:
        mock.return_value = (
            ["thinktank", "--model", "gpt-4.1", "--instructions", "/tmp/thinktank-template-12345.md"],
            "/tmp/thinktank-template-12345.md",
        )
        yield mock


@pytest.fixture
def mock_run_command():
    """Mock the command execution."""
    with patch("thinktank_wrapper.executor.run_command") as mock:
        mock.return_value = 0
        yield mock


@pytest.fixture
def mock_os_unlink():
    """Mock the file deletion."""
    with patch("os.unlink") as mock:
        yield mock


@pytest.fixture
def mock_os_path_exists():
    """Mock the file existence check."""
    with patch("os.path.exists") as mock:
        mock.return_value = True
        yield mock


def test_main_success(
    mock_setup_logging,
    mock_parse_args,
    mock_validate_args,
    mock_find_context_files,
    mock_load_template,
    mock_build_command,
    mock_run_command,
    mock_os_unlink,
    mock_os_path_exists,
):
    """Test that main successfully runs the thinktank-wrapper workflow."""
    # Call the function
    result = __main__.main(["--template", "test-template"])
    
    # Assert the result is 0 (success)
    assert result == 0
    
    # Assert all mocks were called
    mock_setup_logging.assert_called_once()
    mock_parse_args.assert_called_once_with(["--template", "test-template"])
    mock_validate_args.assert_called_once()
    mock_find_context_files.assert_called_once()
    mock_load_template.assert_called_once_with("test-template")
    mock_build_command.assert_called_once()
    mock_run_command.assert_called_once()
    
    # Assert temporary file was deleted
    mock_os_unlink.assert_called_once_with("/tmp/thinktank-template-12345.md")


def test_main_list_templates(
    mock_setup_logging,
    mock_parse_args,
    mock_validate_args,
    mock_find_context_files,
    mock_load_template,
    mock_build_command,
    mock_run_command,
):
    """Test that main handles --list-templates correctly."""
    # Mock parse_args to return args with list_templates=True
    args = MagicMock()
    args.list_templates = True
    mock_parse_args.return_value = (args, [])
    
    # Mock handle_list_templates to exit with code 0
    with patch("thinktank_wrapper.cli.handle_list_templates") as mock_handle:
        mock_handle.side_effect = SystemExit(0)
        
        # Call the function and assert it exits with code 0
        with pytest.raises(SystemExit) as excinfo:
            __main__.main(["--list-templates"])
        
        assert excinfo.value.code == 0
        
        # Assert handle_list_templates was called
        mock_handle.assert_called_once()


def test_main_value_error(
    mock_setup_logging,
    mock_parse_args,
    mock_validate_args,
    capsys,
):
    """Test that main handles ValueError correctly."""
    # Mock validate_args to raise ValueError
    mock_validate_args.side_effect = ValueError("Mock validation error")
    
    # Call the function
    result = __main__.main([])
    
    # Assert the result is 1 (error)
    assert result == 1
    
    # Assert the error message was printed
    captured = capsys.readouterr()
    assert "Error: Mock validation error" in captured.err


def test_main_template_not_found_error(
    mock_setup_logging,
    mock_parse_args,
    mock_validate_args,
    mock_load_template,
    capsys,
):
    """Test that main handles TemplateNotFoundError correctly."""
    # Mock load_template to raise TemplateNotFoundError
    mock_load_template.side_effect = template_loader.TemplateNotFoundError(
        "test-template", ["template1", "template2"]
    )
    
    # Call the function
    result = __main__.main([])
    
    # Assert the result is 1 (error)
    assert result == 1
    
    # Assert the error message was printed
    captured = capsys.readouterr()
    assert "Error: Template 'test-template' not found" in captured.err


def test_main_command_builder_error(
    mock_setup_logging,
    mock_parse_args,
    mock_validate_args,
    mock_find_context_files,
    mock_load_template,
    mock_build_command,
    capsys,
):
    """Test that main handles CommandBuilderError correctly."""
    # Mock build_command to raise CommandBuilderError
    mock_build_command.side_effect = command_builder.CommandBuilderError("Mock command builder error")
    
    # Call the function
    result = __main__.main([])
    
    # Assert the result is 1 (error)
    assert result == 1
    
    # Assert the error message was printed
    captured = capsys.readouterr()
    assert "Error: Mock command builder error" in captured.err


def test_main_thinktank_not_found_error(
    mock_setup_logging,
    mock_parse_args,
    mock_validate_args,
    mock_find_context_files,
    mock_load_template,
    mock_build_command,
    mock_run_command,
    mock_os_unlink,
    mock_os_path_exists,
    capsys,
):
    """Test that main handles ThinktankNotFoundError correctly."""
    # Mock run_command to raise ThinktankNotFoundError
    mock_run_command.side_effect = executor.ThinktankNotFoundError("Mock thinktank not found error")
    
    # Call the function
    result = __main__.main([])
    
    # Assert the result is 1 (error)
    assert result == 1
    
    # Assert the error message was printed
    captured = capsys.readouterr()
    assert "Error: Mock thinktank not found error" in captured.err
    
    # Assert temporary file was deleted
    mock_os_unlink.assert_called_once_with("/tmp/thinktank-template-12345.md")


def test_main_thinktank_execution_error(
    mock_setup_logging,
    mock_parse_args,
    mock_validate_args,
    mock_find_context_files,
    mock_load_template,
    mock_build_command,
    mock_run_command,
    mock_os_unlink,
    mock_os_path_exists,
    capsys,
):
    """Test that main handles ThinktankExecutionError correctly."""
    # Mock run_command to raise ThinktankExecutionError
    mock_run_command.side_effect = executor.ThinktankExecutionError(
        ["thinktank"], 42, "Mock thinktank execution error"
    )
    
    # Call the function
    result = __main__.main([])
    
    # Assert the result is 42 (the error code from ThinktankExecutionError)
    assert result == 42
    
    # Assert the error message was printed
    captured = capsys.readouterr()
    assert "Error:" in captured.err
    
    # Assert temporary file was deleted
    mock_os_unlink.assert_called_once_with("/tmp/thinktank-template-12345.md")


def test_main_keyboard_interrupt(
    mock_setup_logging,
    mock_parse_args,
    mock_validate_args,
    mock_find_context_files,
    mock_load_template,
    mock_build_command,
    mock_run_command,
    mock_os_unlink,
    mock_os_path_exists,
    capsys,
):
    """Test that main handles KeyboardInterrupt correctly."""
    # Mock run_command to raise KeyboardInterrupt
    mock_run_command.side_effect = KeyboardInterrupt()
    
    # Call the function
    result = __main__.main([])
    
    # Assert the result is 130 (standard exit code for SIGINT)
    assert result == 130
    
    # Assert the error message was printed
    captured = capsys.readouterr()
    assert "Interrupted by user" in captured.err
    
    # Assert temporary file was deleted
    mock_os_unlink.assert_called_once_with("/tmp/thinktank-template-12345.md")


def test_main_unexpected_error(
    mock_setup_logging,
    mock_parse_args,
    mock_validate_args,
    mock_find_context_files,
    mock_load_template,
    mock_build_command,
    mock_run_command,
    mock_os_unlink,
    mock_os_path_exists,
    capsys,
):
    """Test that main handles unexpected errors correctly."""
    # Mock run_command to raise an unexpected error
    mock_run_command.side_effect = RuntimeError("Mock unexpected error")
    
    # Call the function
    result = __main__.main([])
    
    # Assert the result is 1 (error)
    assert result == 1
    
    # Assert the error message was printed
    captured = capsys.readouterr()
    assert "Error: An unexpected error occurred" in captured.err
    assert "Mock unexpected error" in captured.err
    
    # Assert temporary file was deleted
    mock_os_unlink.assert_called_once_with("/tmp/thinktank-template-12345.md")