"""Tests for the config module."""

import pytest

from thinktank_wrapper import config


def test_model_sets():
    """Test that the model sets are correctly defined."""
    # There should be a model set named "all"
    assert "all" in config.MODEL_SETS
    assert isinstance(config.MODEL_SETS["all"], list)
    assert len(config.MODEL_SETS["all"]) > 0
    
    # There should be a model set named "high_context"
    assert "high_context" in config.MODEL_SETS
    assert isinstance(config.MODEL_SETS["high_context"], list)
    assert len(config.MODEL_SETS["high_context"]) > 0
    
    # Both model sets should have valid models
    assert all(isinstance(model, str) and model for model in config.MODEL_SETS["all"])
    assert all(isinstance(model, str) and model for model in config.MODEL_SETS["high_context"])
    
    # There should be a synthesis model defined
    assert isinstance(config.SYNTHESIS_MODEL, str)
    assert config.SYNTHESIS_MODEL


def test_default_model_set():
    """Test that the default model set is correctly defined."""
    assert config.DEFAULT_MODEL_SET in config.MODEL_SETS


def test_cli_args():
    """Test that the CLI argument constants are correctly defined."""
    # All CLI arguments should be defined
    assert config.TEMPLATE_ARG
    assert config.LIST_TEMPLATES_ARG
    assert config.MODEL_SET_ARG
    assert config.INCLUDE_LEYLINE_ARG
    assert config.DRY_RUN_ARG
    assert config.INSTRUCTIONS_ARG
    
    # All CLI arguments should start with "--"
    assert config.TEMPLATE_ARG.startswith("--")
    assert config.LIST_TEMPLATES_ARG.startswith("--")
    assert config.MODEL_SET_ARG.startswith("--")
    assert config.INCLUDE_LEYLINE_ARG.startswith("--")
    assert config.DRY_RUN_ARG.startswith("--")
    assert config.INSTRUCTIONS_ARG.startswith("--")