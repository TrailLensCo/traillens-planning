# Copyright (c) 2025 TrailLensCo
# All rights reserved.
#
# This file is proprietary and confidential.

"""Style definitions for document formatting."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class PageSize(Enum):
    """Standard page sizes."""

    LETTER = "letter"
    A4 = "a4"


class TextAlignment(Enum):
    """Text alignment options."""

    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    JUSTIFY = "justify"


class StylePreset(Enum):
    """Predefined style presets."""

    DEFAULT = "default"
    MINIMAL = "minimal"
    ACADEMIC = "academic"
    MODERN = "modern"


@dataclass
class FontStyle:
    """Font styling configuration."""

    name: str = "Calibri"
    size_pt: float = 11.0
    bold: bool = False
    italic: bool = False
    underline: bool = False
    strikethrough: bool = False
    color: Optional[str] = None  # Hex color without #
    highlight: Optional[str] = None


@dataclass
class ParagraphStyle:
    """Paragraph styling configuration."""

    font: FontStyle = field(default_factory=FontStyle)
    alignment: TextAlignment = TextAlignment.LEFT
    space_before_pt: float = 0.0
    space_after_pt: float = 6.0
    line_spacing: float = 1.15
    first_line_indent_inches: float = 0.0
    left_indent_inches: float = 0.0
    right_indent_inches: float = 0.0
    keep_with_next: bool = False
    keep_together: bool = False


@dataclass
class HeadingStyle:
    """Heading level styling configuration."""

    font: FontStyle = field(default_factory=FontStyle)
    space_before_pt: float = 12.0
    space_after_pt: float = 6.0
    keep_with_next: bool = True
    outline_level: int = 0


@dataclass
class CodeStyle:
    """Code block styling configuration."""

    font: FontStyle = field(default_factory=lambda: FontStyle(
        name="Consolas",
        size_pt=10.0
    ))
    background_color: str = "F5F5F5"
    border_color: str = "E0E0E0"
    border_width_pt: float = 0.5
    padding_pt: float = 3.0


@dataclass
class BlockquoteStyle:
    """Blockquote styling configuration."""

    font: FontStyle = field(default_factory=lambda: FontStyle(italic=True))
    left_indent_inches: float = 0.5
    border_color: str = "808080"
    border_width_pt: float = 3.0
    padding_pt: float = 6.0


@dataclass
class TableStyle:
    """Table styling configuration."""

    header_background: str = "1F4E79"  # Dark blue
    header_text_color: str = "FFFFFF"  # White
    header_bold: bool = True
    row_alt_background: str = "F8F8F8"
    border_color: str = "CCCCCC"
    border_width_pt: float = 0.5
    cell_padding_pt: float = 4.0


@dataclass
class PageStyle:
    """Page layout configuration."""

    size: PageSize = PageSize.LETTER
    margin_top_inches: float = 1.0
    margin_bottom_inches: float = 1.0
    margin_left_inches: float = 1.0
    margin_right_inches: float = 1.0
    different_first_page: bool = True


@dataclass
class HeaderFooterStyle:
    """Header and footer configuration."""

    header_font: FontStyle = field(default_factory=lambda: FontStyle(
        size_pt=10.0,
        color="666666"
    ))
    footer_font: FontStyle = field(default_factory=lambda: FontStyle(
        size_pt=10.0,
        color="666666"
    ))
    show_page_numbers: bool = True
    page_number_format: str = "Page {page} of {total}"


@dataclass
class DocumentStyle:
    """Complete document style configuration."""

    # Page layout
    page: PageStyle = field(default_factory=PageStyle)

    # Text styles
    body: ParagraphStyle = field(default_factory=ParagraphStyle)
    body_alignment: TextAlignment = TextAlignment.LEFT

    # Heading styles
    heading1: HeadingStyle = field(default_factory=lambda: HeadingStyle(
        font=FontStyle(
            name="Calibri Light",
            size_pt=24.0,
            bold=True,
            color="1F4E79"  # Navy blue
        ),
        space_before_pt=24.0,
        space_after_pt=12.0,
        outline_level=0
    ))
    heading2: HeadingStyle = field(default_factory=lambda: HeadingStyle(
        font=FontStyle(
            name="Calibri Light",
            size_pt=18.0,
            bold=True,
            color="2E75B6"  # Dark blue
        ),
        space_before_pt=18.0,
        space_after_pt=8.0,
        outline_level=1
    ))
    heading3: HeadingStyle = field(default_factory=lambda: HeadingStyle(
        font=FontStyle(
            name="Calibri Light",
            size_pt=14.0,
            bold=True,
            color="5A5A5A"  # Dark gray
        ),
        space_before_pt=12.0,
        space_after_pt=6.0,
        outline_level=2
    ))
    heading4: HeadingStyle = field(default_factory=lambda: HeadingStyle(
        font=FontStyle(
            name="Calibri Light",
            size_pt=12.0,
            bold=True,
            color="666666"
        ),
        space_before_pt=10.0,
        space_after_pt=4.0,
        outline_level=3
    ))
    heading5: HeadingStyle = field(default_factory=lambda: HeadingStyle(
        font=FontStyle(
            name="Calibri Light",
            size_pt=12.0,
            bold=True,
            italic=True,
            color="767676"
        ),
        space_before_pt=8.0,
        space_after_pt=4.0,
        outline_level=4
    ))
    heading6: HeadingStyle = field(default_factory=lambda: HeadingStyle(
        font=FontStyle(
            name="Calibri Light",
            size_pt=11.0,
            bold=True,
            color="808080"
        ),
        space_before_pt=6.0,
        space_after_pt=4.0,
        outline_level=5
    ))

    # Special element styles
    code: CodeStyle = field(default_factory=CodeStyle)
    blockquote: BlockquoteStyle = field(default_factory=BlockquoteStyle)
    table: TableStyle = field(default_factory=TableStyle)
    header_footer: HeaderFooterStyle = field(default_factory=HeaderFooterStyle)

    # Title page settings
    title_font: FontStyle = field(default_factory=lambda: FontStyle(
        name="Calibri Light",
        size_pt=36.0,
        bold=True,
        color="1F4E79"
    ))
    author_font: FontStyle = field(default_factory=lambda: FontStyle(
        size_pt=14.0,
        color="666666"
    ))
    date_font: FontStyle = field(default_factory=lambda: FontStyle(
        size_pt=12.0,
        color="808080"
    ))

    # Hyperlink style
    hyperlink_color: str = "0563C1"

    # Image settings
    max_image_width_inches: float = 6.0
    image_caption_font: FontStyle = field(default_factory=lambda: FontStyle(
        size_pt=10.0,
        italic=True,
        color="666666"
    ))

    def get_heading_style(self, level: int) -> HeadingStyle:
        """
        Get heading style for a specific level.

        Args:
            level: Heading level (1-6).

        Returns:
            HeadingStyle for the specified level.
        """
        styles = {
            1: self.heading1,
            2: self.heading2,
            3: self.heading3,
            4: self.heading4,
            5: self.heading5,
            6: self.heading6,
        }
        return styles.get(level, self.heading6)


def get_style_preset(preset: StylePreset) -> DocumentStyle:
    """
    Get a predefined style preset.

    Args:
        preset: The style preset to use.

    Returns:
        DocumentStyle configured for the preset.
    """
    if preset == StylePreset.MINIMAL:
        style = DocumentStyle()
        # Simplified, clean styling
        style.body_alignment = TextAlignment.LEFT
        style.heading1.font.color = "000000"
        style.heading2.font.color = "333333"
        style.heading3.font.color = "555555"
        style.table.header_background = "333333"
        return style

    elif preset == StylePreset.ACADEMIC:
        style = DocumentStyle()
        # Academic paper styling
        style.body.font = FontStyle(name="Times New Roman", size_pt=12.0)
        style.body_alignment = TextAlignment.JUSTIFY
        style.body.line_spacing = 2.0  # Double-spaced
        style.body.first_line_indent_inches = 0.5
        style.page.margin_top_inches = 1.0
        style.page.margin_bottom_inches = 1.0
        style.page.margin_left_inches = 1.25
        style.page.margin_right_inches = 1.25
        return style

    elif preset == StylePreset.MODERN:
        style = DocumentStyle()
        # Modern, sleek styling
        style.body.font = FontStyle(name="Segoe UI", size_pt=11.0)
        style.heading1.font = FontStyle(
            name="Segoe UI",
            size_pt=28.0,
            bold=True,
            color="2B579A"
        )
        style.heading2.font = FontStyle(
            name="Segoe UI",
            size_pt=20.0,
            bold=True,
            color="3B6BA5"
        )
        style.code.font = FontStyle(name="Cascadia Code", size_pt=10.0)
        return style

    # Default style
    return DocumentStyle()
