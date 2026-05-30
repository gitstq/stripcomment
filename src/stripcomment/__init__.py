"""
StripComment - A powerful CLI tool to intelligently strip comments from source code.

This package provides functionality to remove comments from various programming
languages while preserving string literals and offering flexible configuration.
"""

__version__ = "1.0.0"
__author__ = "gitstq"
__license__ = "MIT"

from stripcomment.core import StripComment
from stripcomment.languages import LanguageConfig

__all__ = ["StripComment", "LanguageConfig"]
