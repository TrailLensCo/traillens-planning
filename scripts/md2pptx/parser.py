# Copyright (c) 2025 TrailLensCo
# All rights reserved.
#
# This file is proprietary and confidential.

"""Markdown parsing and front matter handling."""

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import frontmatter

logger = logging.getLogger(__name__)


@dataclass
class PresentationMetadata:
    """Presentation metadata from YAML front matter."""

    title: Optional[str] = None
    author: Optional[str] = None
    date: Optional[str] = None
    subtitle: Optional[str] = None
    institute: Optional[str] = None
    theme: Optional[str] = None
    background_image: Optional[Path] = None
    aspect_ratio: str = "16:9"  # 16:9 or 4:3
    extra: dict[str, Any] = field(default_factory=dict)


class MarkdownParser:
    """Parser for extracting metadata from markdown with front matter."""

    def parse_front_matter(self, content: str, base_dir: Optional[Path] = None) -> tuple[PresentationMetadata, str]:
        """
        Extract metadata from YAML front matter.

        Args:
            content: Raw markdown content.
            base_dir: Base directory for resolving relative paths.

        Returns:
            Tuple of (metadata, markdown_body).
        """
        try:
            parsed = frontmatter.loads(content)
            fm = parsed.metadata
            markdown_body = parsed.content

            if not fm:
                return PresentationMetadata(), markdown_body

            metadata = PresentationMetadata(
                title=fm.get("title"),
                author=fm.get("author"),
                date=str(fm.get("date")) if fm.get("date") else None,
                subtitle=fm.get("subtitle"),
                institute=fm.get("institute"),
                theme=fm.get("theme"),
                aspect_ratio=fm.get("aspect_ratio", "16:9"),
            )

            # Handle background image path
            if "background_image" in fm:
                bg_path = Path(fm["background_image"])
                if not bg_path.is_absolute() and base_dir:
                    bg_path = base_dir / bg_path
                metadata.background_image = bg_path

            # Store extra fields
            known_fields = {
                "title", "author", "date", "subtitle", "institute",
                "theme", "background_image", "aspect_ratio"
            }
            for key, value in fm.items():
                if key not in known_fields:
                    metadata.extra[key] = value

            logger.debug(f"Parsed metadata: title={metadata.title}, background_image={metadata.background_image}")
            return metadata, markdown_body

        except Exception as e:
            logger.warning(f"Failed to parse front matter: {e}")
            return PresentationMetadata(), content
