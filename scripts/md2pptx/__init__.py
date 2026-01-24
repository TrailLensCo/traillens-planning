# Copyright (c) 2025 TrailLensCo
# All rights reserved.
#
# This file is proprietary and confidential.

"""
md2pptx - Markdown to PowerPoint (PPTX) converter.

A Python library and CLI tool for converting Markdown files to
properly formatted PowerPoint presentations using Pandoc.
"""

__version__ = "1.0.0"
__author__ = "TrailLens Development Team"

from md2pptx.converter import MarkdownToPptxConverter
from md2pptx.styles import PresentationStyle, StylePreset

__all__ = [
    "MarkdownToPptxConverter",
    "PresentationStyle",
    "StylePreset",
    "__version__",
]
