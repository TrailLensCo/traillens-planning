# Copyright (c) 2025 TrailLensCo
# All rights reserved.
#
# This file is proprietary and confidential.

"""
md2docx - Markdown to DOCX converter.

A Python library and CLI tool for converting Markdown files to
properly formatted Word (DOCX) documents without requiring Pandoc.
"""

__version__ = "1.0.0"
__author__ = "TrailLens Development Team"

from md2docx.converter import MarkdownToDocxConverter
from md2docx.styles import DocumentStyle, StylePreset

__all__ = [
    "MarkdownToDocxConverter",
    "DocumentStyle",
    "StylePreset",
    "__version__",
]
