"""Tests for the template_loader module."""

import importlib.resources
from typing import List
from unittest.mock import patch

import pytest

from thinktank_wrapper.template_loader import (
    TemplateNotFoundError, list_templates, load_template, inject_context
)
from thinktank_wrapper import config


class MockPath:
    """Mock class for Path objects returned by importlib.resources."""
    
    def __init__(self, name: str, is_file: bool = True):
        self.name = name
        self._is_file = is_file
    
    def is_file(self) -> bool:
        """Return whether this path is a file."""
        return self._is_file
    
    @property
    def stem(self) -> str:
        """Return the stem of the filename."""
        if self.name.endswith(".md"):
            return self.name[:-3]
        return self.name


class MockTemplatesDir:
    """Mock class for the templates directory resource."""
    
    def __init__(self, files: List[str]):
        self.files = files
    
    def iterdir(self):
        """Iterate over the files in the directory."""
        for name in self.files:
            yield MockPath(name)
    
    def joinpath(self, name: str):
        """Join this path with another."""
        return MockTemplateFile(name)


class MockTemplateFile:
    """Mock class for a template file resource."""
    
    def __init__(self, name: str):
        self.name = name
    
    def read_text(self, encoding: str = "utf-8") -> str:
        """Read the text of the file."""
        return f"# Mock content for {self.name}"


@pytest.fixture
def mock_templates():
    """Mock the templates directory for testing."""
    files = ["template1.md", "template2.md", "__init__.py", "README.txt"]
    with patch("importlib.resources.files") as mock_files:
        mock_files.return_value = MockTemplatesDir(files)
        yield


def test_list_templates(mock_templates):
    """Test that list_templates returns the correct templates."""
    templates = list_templates()
    assert templates == ["template1", "template2"]


def test_load_template_success(mock_templates):
    """Test that load_template returns the content of a template."""
    content = load_template("template1")
    assert content == "# Mock content for template1.md"


def test_load_template_with_extension(mock_templates):
    """Test that load_template works when the template name includes the extension."""
    content = load_template("template1.md")
    assert content == "# Mock content for template1.md"


def test_load_template_not_found(mock_templates):
    """Test that load_template raises TemplateNotFoundError for unknown templates."""
    with pytest.raises(TemplateNotFoundError) as excinfo:
        load_template("unknown")
    
    assert "Template 'unknown' not found" in str(excinfo.value)
    assert "template1, template2" in str(excinfo.value)


@pytest.fixture
def template_with_context(temp_dir):
    """Create a template file with a CONTEXT section."""
    template_content = f"""# Test Template

This is a test template.

{config.CONTEXT_BEGIN_MARKER}
Default context content that should be replaced.
{config.CONTEXT_END_MARKER}

Some more template content.
"""
    template_file = temp_dir / "template_with_context.md"
    template_file.write_text(template_content)
    return template_file


@pytest.fixture
def template_without_context(temp_dir):
    """Create a template file without a CONTEXT section."""
    template_content = """# Test Template

This is a test template without a CONTEXT section.

Some template content.
"""
    template_file = temp_dir / "template_without_context.md"
    template_file.write_text(template_content)
    return template_file


@pytest.fixture
def context_file(temp_dir):
    """Create a context file with custom content."""
    context_content = """# Custom Context

This is custom context that should replace the default content.

- Item 1
- Item 2
- Item 3
"""
    context_file = temp_dir / "custom_context.md"
    context_file.write_text(context_content)
    return context_file


def test_inject_context_with_markers(template_with_context, context_file):
    """Test that inject_context replaces the content between markers."""
    # Read the original template content
    template_content = template_with_context.read_text()
    
    # Read the context content
    context_content = context_file.read_text()
    
    # Inject the context
    result = inject_context(template_content, str(context_file))
    
    # Check that the result contains the context content
    assert context_content in result
    
    # Check that the result does not contain the default content
    assert "Default context content that should be replaced." not in result
    
    # Check that the markers are still there
    assert config.CONTEXT_BEGIN_MARKER in result
    assert config.CONTEXT_END_MARKER in result
    
    # Check that the rest of the template content is preserved
    assert "# Test Template" in result
    assert "This is a test template." in result
    assert "Some more template content." in result


def test_inject_context_without_markers(template_without_context, context_file):
    """Test that inject_context raises ValueError when markers are not found."""
    # Read the original template content
    template_content = template_without_context.read_text()
    
    # Try to inject the context
    with pytest.raises(ValueError) as excinfo:
        inject_context(template_content, str(context_file))
    
    # Check the error message
    assert "Template does not contain required markers" in str(excinfo.value)
    assert config.CONTEXT_BEGIN_MARKER in str(excinfo.value)
    assert config.CONTEXT_END_MARKER in str(excinfo.value)


def test_inject_context_nonexistent_file(template_with_context):
    """Test that inject_context raises ValueError when the context file does not exist."""
    # Read the original template content
    template_content = template_with_context.read_text()
    
    # Try to inject from a nonexistent file
    with pytest.raises(ValueError) as excinfo:
        inject_context(template_content, "/nonexistent/file.md")
    
    # Check the error message
    assert "Failed to read context file" in str(excinfo.value)


def test_inject_context_none_file(template_with_context):
    """Test that inject_context returns the original content when context_file_path is None."""
    # Read the original template content
    template_content = template_with_context.read_text()
    
    # Inject None as the context file
    result = inject_context(template_content, None)
    
    # Check that the result is the same as the original
    assert result == template_content