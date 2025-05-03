"""Pytest configuration for thinktank-wrapper tests.

This module provides pytest fixtures and configuration for the test suite.
"""

import os
import tempfile
from pathlib import Path
from typing import Generator, List

import pytest


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for tests.
    
    Yields:
        Path to the temporary directory.
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def mock_codex_dir(temp_dir: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Set up a mock CODEX_DIR environment variable and directory structure.
    
    Args:
        temp_dir: Temporary directory fixture.
        monkeypatch: Pytest monkeypatch fixture.
        
    Returns:
        Path to the mock CODEX_DIR.
    """
    # Create a mock CODEX_DIR
    codex_dir = temp_dir / "mock_codex"
    codex_dir.mkdir(exist_ok=True)
    
    # Create a docs directory
    docs_dir = codex_dir / "docs"
    docs_dir.mkdir(exist_ok=True)
    
    # Create mock philosophy files
    (docs_dir / "DEVELOPMENT_PHILOSOPHY.md").write_text("# Mock Philosophy")
    (docs_dir / "DEVELOPMENT_PHILOSOPHY_APPENDIX_TYPESCRIPT.md").write_text(
        "# Mock TypeScript Philosophy"
    )
    
    # Set the CODEX_DIR environment variable
    monkeypatch.setenv("CODEX_DIR", str(codex_dir))
    
    return codex_dir


@pytest.fixture
def mock_glance_files(temp_dir: Path) -> List[Path]:
    """Create mock glance.md files in the temporary directory.
    
    Args:
        temp_dir: Temporary directory fixture.
        
    Returns:
        List of paths to the mock glance.md files.
    """
    # Create directories with glance.md files
    glance_files = []
    
    # Root level glance.md
    root_glance = temp_dir / "glance.md"
    root_glance.write_text("# Root Glance")
    glance_files.append(root_glance)
    
    # Nested glance.md files
    for i in range(3):
        nested_dir = temp_dir / f"nested{i}"
        nested_dir.mkdir(exist_ok=True)
        nested_glance = nested_dir / "glance.md"
        nested_glance.write_text(f"# Nested Glance {i}")
        glance_files.append(nested_glance)
    
    return glance_files