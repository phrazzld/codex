"""Configuration module for thinktank-wrapper.

This module defines the model sets and other static configuration used by
the thinktank-wrapper CLI application. These configurations match the
behavior of the original Bash wrapper script.
"""

import os
from typing import Dict, List

# ALL MODELS - Comprehensive set of models for thorough analysis
MODELS_ALL: List[str] = [
    # OpenAI Models
    "gpt-4.1",
    "o4-mini",
    "o3",

    # Gemini Models
    "gemini-2.5-pro",
    "gemini-2.5-flash",

    # OpenRouter Models
    "openrouter/deepseek/deepseek-chat-v3-0324",
    "openrouter/deepseek/deepseek-prover-v2",
    "openrouter/deepseek/deepseek-r1-0528",
    "openrouter/x-ai/grok-3-beta",
    "openrouter/x-ai/grok-3-mini-beta",
    "openrouter/meta-llama/llama-4-maverick",
    "openrouter/meta-llama/llama-4-scout",
]

# HIGH CONTEXT MODELS - Models with larger context windows for complex files
MODELS_HIGH_CONTEXT: List[str] = [
    # OpenAI Models
    "gpt-4.1",

    # Gemini Models
    "gemini-2.5-pro",
    "gemini-2.5-flash",

    # OpenRouter Models
    "openrouter/meta-llama/llama-4-maverick",
    "openrouter/meta-llama/llama-4-scout",
]

# SYNTHESIS MODEL - Model used for final output generation
SYNTHESIS_MODEL: str = "gemini-2.5-pro"

# Dictionary mapping model set names to their corresponding model lists
# This provides a convenient lookup for the CLI argument parsing
MODEL_SETS: Dict[str, List[str]] = {
    "all": MODELS_ALL,
    "high_context": MODELS_HIGH_CONTEXT,
}

# Default model set to use if none specified
DEFAULT_MODEL_SET: str = "all"

# Maximum directory depth for searching glance.md files
MAX_GLANCE_DEPTH: int = 3

# CLI argument related constants
TEMPLATE_ARG: str = "--template"
LIST_TEMPLATES_ARG: str = "--list-templates"
MODEL_SET_ARG: str = "--model-set"
INCLUDE_LEYLINE_ARG: str = "--include-leyline"
DRY_RUN_ARG: str = "--dry-run"
INSTRUCTIONS_ARG: str = "--instructions"
INJECT_ARG: str = "--inject"

# Template context marker constants
CONTEXT_BEGIN_MARKER: str = "<!-- BEGIN:CONTEXT -->"
CONTEXT_END_MARKER: str = "<!-- END:CONTEXT -->"

# Token counting configuration
LLM_CONTEXT_THRESHOLD: int = int(os.environ.get("LLM_CONTEXT_THRESHOLD", "200000"))
TOKEN_COUNT_PROVIDER: str = os.environ.get("TOKEN_COUNT_PROVIDER", "openai")
ENABLE_TOKEN_COUNTING: bool = os.environ.get("ENABLE_TOKEN_COUNTING", "true").lower() == "true"
