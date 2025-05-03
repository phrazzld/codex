"""Tests for the template_loader module."""

import importlib.resources
from typing import List
from unittest.mock import patch

import pytest

from thinktank_wrapper.template_loader import TemplateNotFoundError, list_templates, load_template


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