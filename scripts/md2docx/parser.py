# Copyright (c) 2025 TrailLensCo
# All rights reserved.
#
# This file is proprietary and confidential.

"""Markdown parsing and token handling."""

import logging
import re
from dataclasses import dataclass, field
from typing import Any, Optional

import frontmatter
from markdown_it import MarkdownIt
from mdit_py_plugins.deflist import deflist_plugin
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.tasklists import tasklists_plugin

logger = logging.getLogger(__name__)


@dataclass
class DocumentMetadata:
    """Document metadata from YAML front matter."""

    title: Optional[str] = None
    author: Optional[str] = None
    date: Optional[str] = None
    abstract: Optional[str] = None
    keywords: list[str] = field(default_factory=list)
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class ParsedToken:
    """Wrapper for parsed markdown tokens with additional metadata."""

    type: str
    tag: str = ""
    content: str = ""
    children: list["ParsedToken"] = field(default_factory=list)
    attrs: dict[str, str] = field(default_factory=dict)
    info: str = ""
    level: int = 0
    nesting: int = 0
    markup: str = ""
    block: bool = False
    hidden: bool = False
    meta: dict[str, Any] = field(default_factory=dict)


class MarkdownParser:
    """Parser for converting markdown to structured tokens."""

    # Diagram fence types
    DIAGRAM_TYPES = frozenset({
        "mermaid",
        "plantuml",
        "ditaa",
        "ascii",
        "diagram",
    })

    def __init__(self):
        """Initialize the markdown parser with plugins."""
        self._md = MarkdownIt("commonmark", {"html": True, "typographer": True})

        # Enable tables (GFM extension)
        self._md.enable("table")

        # Enable strikethrough
        self._md.enable("strikethrough")

        # Add plugins
        self._md.use(footnote_plugin)
        self._md.use(deflist_plugin)
        self._md.use(tasklists_plugin)

        logger.debug("Markdown parser initialized with plugins")

    def parse(self, content: str) -> tuple[DocumentMetadata, list[ParsedToken]]:
        """
        Parse markdown content into metadata and tokens.

        Args:
            content: Raw markdown content (may include YAML front matter).

        Returns:
            Tuple of (metadata, list of parsed tokens).
        """
        # Extract front matter
        metadata = self._parse_front_matter(content)

        # Get markdown body (without front matter)
        parsed = frontmatter.loads(content)
        markdown_body = parsed.content

        # Parse markdown into tokens
        raw_tokens = self._md.parse(markdown_body)

        # Convert to our token format
        tokens = [self._convert_token(t) for t in raw_tokens]

        logger.debug(f"Parsed {len(tokens)} tokens from markdown")

        return metadata, tokens

    def _parse_front_matter(self, content: str) -> DocumentMetadata:
        """
        Extract metadata from YAML front matter.

        Args:
            content: Raw markdown content.

        Returns:
            DocumentMetadata instance.
        """
        try:
            parsed = frontmatter.loads(content)
            fm = parsed.metadata

            if not fm:
                return DocumentMetadata()

            metadata = DocumentMetadata(
                title=fm.get("title"),
                author=fm.get("author"),
                date=str(fm.get("date")) if fm.get("date") else None,
                abstract=fm.get("abstract"),
                keywords=fm.get("keywords", []),
            )

            # Store extra fields
            known_fields = {"title", "author", "date", "abstract", "keywords"}
            for key, value in fm.items():
                if key not in known_fields:
                    metadata.extra[key] = value

            return metadata

        except Exception as e:
            logger.warning(f"Failed to parse front matter: {e}")
            return DocumentMetadata()

    def _convert_token(self, token: Any) -> ParsedToken:
        """
        Convert a markdown-it token to our ParsedToken format.

        Args:
            token: Raw markdown-it token.

        Returns:
            ParsedToken instance.
        """
        # Convert attributes to dict (may be dict or list of tuples)
        attrs = {}
        if token.attrs:
            if isinstance(token.attrs, dict):
                attrs = dict(token.attrs)
            else:
                # List of tuples or items
                for item in token.attrs:
                    if isinstance(item, (list, tuple)) and len(item) >= 2:
                        attrs[item[0]] = item[1]
                    elif isinstance(item, str):
                        attrs[item] = ""

        # Convert children recursively
        children = []
        if token.children:
            children = [self._convert_token(c) for c in token.children]

        return ParsedToken(
            type=token.type,
            tag=token.tag or "",
            content=token.content or "",
            children=children,
            attrs=attrs,
            info=token.info or "",
            level=token.level or 0,
            nesting=token.nesting or 0,
            markup=token.markup or "",
            block=token.block if hasattr(token, "block") else False,
            hidden=token.hidden if hasattr(token, "hidden") else False,
            meta=token.meta if hasattr(token, "meta") and token.meta else {},
        )

    def is_diagram_block(self, token: ParsedToken) -> bool:
        """
        Check if a fence token is a diagram code block.

        Args:
            token: Token to check.

        Returns:
            True if this is a diagram code block.
        """
        if token.type != "fence":
            return False

        # Get the language/info string
        info = token.info.strip().lower().split()[0] if token.info else ""
        return info in self.DIAGRAM_TYPES

    def get_language(self, token: ParsedToken) -> str:
        """
        Get the language identifier from a fence token.

        Args:
            token: Fence token.

        Returns:
            Language identifier string.
        """
        if not token.info:
            return ""
        return token.info.strip().split()[0].lower()


def extract_text_content(tokens: list[ParsedToken]) -> str:
    """
    Extract plain text content from a list of tokens.

    Args:
        tokens: List of tokens to extract text from.

    Returns:
        Plain text string.
    """
    text_parts = []

    for token in tokens:
        if token.type == "text":
            text_parts.append(token.content)
        elif token.type == "code_inline":
            text_parts.append(token.content)
        elif token.type == "softbreak":
            text_parts.append(" ")
        elif token.type == "hardbreak":
            text_parts.append("\n")
        elif token.children:
            text_parts.append(extract_text_content(token.children))

    return "".join(text_parts)


def get_link_info(token: ParsedToken) -> tuple[str, str]:
    """
    Extract URL and title from a link token.

    Args:
        token: Link token (link_open).

    Returns:
        Tuple of (href, title).
    """
    href = token.attrs.get("href", "")
    title = token.attrs.get("title", "")
    return href, title


def get_image_info(token: ParsedToken) -> tuple[str, str, str]:
    """
    Extract src, alt, and title from an image token.

    Args:
        token: Image token.

    Returns:
        Tuple of (src, alt, title).
    """
    src = token.attrs.get("src", "")
    alt = token.attrs.get("alt", token.content or "")
    title = token.attrs.get("title", "")
    return src, alt, title


def get_table_alignment(token: ParsedToken) -> list[str]:
    """
    Extract column alignments from table tokens.

    Args:
        token: Table-related token with alignment info.

    Returns:
        List of alignment strings ('left', 'center', 'right', or '').
    """
    # Alignment is typically stored in token style attributes
    alignments = []

    if token.attrs and "style" in token.attrs:
        style = token.attrs["style"]
        if "text-align:left" in style:
            alignments.append("left")
        elif "text-align:center" in style:
            alignments.append("center")
        elif "text-align:right" in style:
            alignments.append("right")
        else:
            alignments.append("")

    return alignments


def parse_task_list_item(token: ParsedToken) -> tuple[bool, str]:
    """
    Parse a task list item to get checkbox state and content.

    Args:
        token: Task list item token.

    Returns:
        Tuple of (is_checked, content_text).
    """
    # Check for task list marker
    is_checked = False
    content = ""

    if token.children:
        for child in token.children:
            if child.type == "paragraph_open":
                continue
            elif child.type == "paragraph_close":
                continue
            elif child.type == "inline":
                text = extract_text_content([child])
                # Check for checkbox pattern
                checkbox_match = re.match(r"^\s*\[([ xX])\]\s*", text)
                if checkbox_match:
                    is_checked = checkbox_match.group(1).lower() == "x"
                    content = text[checkbox_match.end():]
                else:
                    content = text

    return is_checked, content
