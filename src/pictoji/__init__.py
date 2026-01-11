"""
ㄕICTOji - A Relatable Algebra for the People

A new old language to explore what an AI-assisted mathemojics of meaning could possibly be.

This package includes:
- AI token counter for Claude, GPT, and Gemini models
- Unicode block analyzer
- Complete Pictoji language specifications
"""

__version__ = "1.0.0"
__author__ = "Pictoji Team"

# Import main CLI functions for programmatic access
from .cli import (
    count_claude_tokens,
    count_gpt_tokens,
    count_gemini_tokens,
    analyze_unicode_blocks,
    get_unicode_block,
)

__all__ = [
    "__version__",
    "__author__",
    "count_claude_tokens",
    "count_gpt_tokens",
    "count_gemini_tokens",
    "analyze_unicode_blocks",
    "get_unicode_block",
]
