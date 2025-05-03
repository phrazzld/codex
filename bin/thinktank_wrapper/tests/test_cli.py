"""Tests for the cli module."""

import io
import sys
from unittest.mock import patch

import pytest

from thinktank_wrapper import cli, config, template_loader


@pytest.fixture
def mock_available_templates():
    """Set up mock available templates for testing."""
    with patch("thinktank_wrapper.template_loader.list_templates") as mock_list:
        mock_list.return_value = ["template1", "template2", "template3"]
        yield mock_list


@pytest.fixture
def mock_load_template():
    """Set up mock template loading for testing."""
    with patch("thinktank_wrapper.template_loader.load_template") as mock_load:
        mock_load.return_value = "# Mock template content"
        yield mock_load


def test_parse_args_defaults():
    """Test that parse_args sets default values correctly."""
    # Call the function with an empty list of arguments
    args, unknown = cli.parse_args([])
    
    # Assert the defaults
    assert args.template is None
    assert not args.list_templates
    assert args.model_set == config.DEFAULT_MODEL_SET
    assert not args.include_glance
    assert not args.include_philosophy
    assert not args.dry_run
    assert args.instructions is None
    assert args.context_paths == []
    assert unknown == []


def test_parse_args_template():
    """Test that parse_args handles --template correctly."""
    # Call the function with --template
    args, unknown = cli.parse_args(["--template", "test-template"])
    
    # Assert the template is set
    assert args.template == "test-template"


def test_parse_args_list_templates():
    """Test that parse_args handles --list-templates correctly."""
    # Call the function with --list-templates
    args, unknown = cli.parse_args(["--list-templates"])
    
    # Assert list_templates is set
    assert args.list_templates


def test_parse_args_model_set():
    """Test that parse_args handles --model-set correctly."""
    # Call the function with --model-set
    args, unknown = cli.parse_args(["--model-set", "high_context"])
    
    # Assert the model set is set
    assert args.model_set == "high_context"


def test_parse_args_include_flags():
    """Test that parse_args handles --include-* flags correctly."""
    # Call the function with --include-glance and --include-philosophy
    args, unknown = cli.parse_args(["--include-glance", "--include-philosophy"])
    
    # Assert the flags are set
    assert args.include_glance
    assert args.include_philosophy


def test_parse_args_dry_run():
    """Test that parse_args handles --dry-run correctly."""
    # Call the function with --dry-run
    args, unknown = cli.parse_args(["--dry-run"])
    
    # Assert dry_run is set
    assert args.dry_run


def test_parse_args_instructions():
    """Test that parse_args handles --instructions correctly."""
    # Call the function with --instructions
    args, unknown = cli.parse_args(["--instructions", "/path/to/instructions.md"])
    
    # Assert the instructions path is set
    assert args.instructions == "/path/to/instructions.md"


def test_parse_args_context_paths():
    """Test that parse_args handles context paths correctly."""
    # Call the function with context paths
    args, unknown = cli.parse_args(["/path/to/file1.md", "/path/to/file2.md"])
    
    # Assert the context paths are set
    assert args.context_paths == ["/path/to/file1.md", "/path/to/file2.md"]


def test_parse_args_unknown():
    """Test that parse_args handles unknown args correctly."""
    # Call the function with unknown args
    args, unknown = cli.parse_args(["--unknown-flag", "value", "--another-flag"])
    
    # Assert the unknown args are returned
    assert unknown == ["--unknown-flag", "value", "--another-flag"]


def test_handle_list_templates(mock_available_templates, capsys):
    """Test that handle_list_templates lists templates and exits."""
    # Mock sys.exit to avoid actually exiting
    with pytest.raises(SystemExit) as excinfo:
        with patch("sys.exit") as mock_exit:
            mock_exit.side_effect = SystemExit(0)
            cli.handle_list_templates()
    
    # Assert that sys.exit was called with 0
    assert excinfo.value.code == 0
    
    # Assert the output
    captured = capsys.readouterr()
    assert "Available templates:" in captured.out
    assert "template1" in captured.out
    assert "template2" in captured.out
    assert "template3" in captured.out


def test_handle_list_templates_no_templates(capsys):
    """Test that handle_list_templates handles no templates correctly."""
    # Mock list_templates to return an empty list
    with pytest.raises(SystemExit) as excinfo:
        with patch("thinktank_wrapper.template_loader.list_templates") as mock_list:
            mock_list.return_value = []
            with patch("sys.exit") as mock_exit:
                mock_exit.side_effect = SystemExit(0)
                cli.handle_list_templates()
    
    # Assert that sys.exit was called with 0
    assert excinfo.value.code == 0
    
    # Assert the output
    captured = capsys.readouterr()
    assert "No templates found." in captured.out


def test_validate_args_valid(mock_load_template):
    """Test that validate_args passes for valid arguments."""
    # Create valid args with --template
    args = type("Args", (), {
        "list_templates": False,
        "template": "template1",
        "instructions": None,
    })()
    
    # Call the function
    cli.validate_args(args)
    
    # Assert template_loader.load_template was called
    mock_load_template.assert_called_once_with("template1")


def test_validate_args_valid_instructions():
    """Test that validate_args passes for valid arguments with --instructions."""
    # Create valid args with --instructions
    args = type("Args", (), {
        "list_templates": False,
        "template": None,
        "instructions": "/path/to/instructions.md",
    })()
    
    # Call the function
    cli.validate_args(args)
    
    # No assertions needed, just checking that no exceptions are raised


def test_validate_args_invalid_missing_both():
    """Test that validate_args raises ValueError when both --template and --instructions are missing."""
    # Create invalid args
    args = type("Args", (), {
        "list_templates": False,
        "template": None,
        "instructions": None,
    })()
    
    # Call the function and assert it raises ValueError
    with pytest.raises(ValueError) as excinfo:
        cli.validate_args(args)
    
    # Assert the error message
    assert "Either --template or --instructions must be provided" in str(excinfo.value)


def test_validate_args_invalid_template(mock_available_templates):
    """Test that validate_args raises ValueError when the template is invalid."""
    # Create args with an invalid template
    args = type("Args", (), {
        "list_templates": False,
        "template": "invalid-template",
        "instructions": None,
    })()
    
    # Mock load_template to raise TemplateNotFoundError
    with patch("thinktank_wrapper.template_loader.load_template") as mock_load:
        mock_load.side_effect = template_loader.TemplateNotFoundError(
            "invalid-template", ["template1", "template2", "template3"]
        )
        
        # Call the function and assert it raises ValueError
        with pytest.raises(ValueError) as excinfo:
            cli.validate_args(args)
    
    # Assert the error message
    assert "Template 'invalid-template' not found" in str(excinfo.value)