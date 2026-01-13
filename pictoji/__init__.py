"""
ㄕICTOji - A Relatable Algebra for the People

A new old language to explore what an AI-assisted mathemojics of meaning could possibly be.

This package contains:
- pictoji.cli - tools for developing Pictoji specs and lexicons (target for v1.0)
"""

# Read version from installed package metadata (pyproject.toml is source of truth)
try:
    from importlib.metadata import version
    __version__ = version("pictoji")
except Exception:
    # Fallback for development before pip install -e .
    __version__ = "1.0.0"

__author__ = "Pictoji Team"

__all__ = [
    "__version__",
    "__author__",
]
