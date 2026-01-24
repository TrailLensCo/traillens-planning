# Copyright (c) 2025 TrailLensCo
# All rights reserved.
#
# This file is proprietary and confidential.

"""Style definitions for presentation formatting."""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional


class StylePreset(Enum):
    """Predefined presentation style presets."""

    DEFAULT = "default"
    SIMPLE = "simple"
    MODERN = "modern"
    PROFESSIONAL = "professional"


@dataclass
class PresentationStyle:
    """Presentation styling configuration."""

    theme: Optional[str] = None  # Pandoc theme name (e.g., "default", "beamer")
    aspect_ratio: str = "16:9"  # "16:9" or "4:3"
    slide_level: int = 2  # Heading level for new slides (1-6)
    incremental: bool = False  # Incremental bullets
    reference_doc: Optional[Path] = None  # Reference PPTX for styling
    toc: bool = False  # Include table of contents slide
    toc_depth: int = 2  # TOC depth


def get_style_preset(preset: StylePreset) -> PresentationStyle:
    """
    Get a predefined style preset.

    Args:
        preset: Style preset to use.

    Returns:
        PresentationStyle configuration.
    """
    if preset == StylePreset.SIMPLE:
        return PresentationStyle(
            theme="simple",
            slide_level=1,
            incremental=False,
        )
    elif preset == StylePreset.MODERN:
        return PresentationStyle(
            theme="default",
            slide_level=2,
            incremental=True,
        )
    elif preset == StylePreset.PROFESSIONAL:
        return PresentationStyle(
            theme="default",
            slide_level=2,
            incremental=False,
            toc=True,
        )
    else:  # DEFAULT
        return PresentationStyle(
            theme="default",
            slide_level=2,
            incremental=False,
        )
