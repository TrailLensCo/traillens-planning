# Copyright (c) 2025 TrailLensCo
# All rights reserved.
#
# This file is proprietary and confidential.

"""Diagram type detection from code blocks."""

import logging
import re
from enum import Enum
from typing import Optional

logger = logging.getLogger(__name__)


class DiagramType(Enum):
    """Supported diagram types."""

    MERMAID = "mermaid"
    PLANTUML = "plantuml"
    DITAA = "ditaa"
    ASCII = "ascii"
    UNKNOWN = "unknown"


class DiagramDetector:
    """Detects diagram types from code block fence info."""

    # Fence type mappings
    FENCE_TYPE_MAP = {
        "mermaid": DiagramType.MERMAID,
        "plantuml": DiagramType.PLANTUML,
        "puml": DiagramType.PLANTUML,
        "uml": DiagramType.PLANTUML,
        "ditaa": DiagramType.DITAA,
        "ascii": DiagramType.ASCII,
        "diagram": DiagramType.ASCII,  # Generic, try ASCII detection
    }

    # PlantUML start patterns
    PLANTUML_PATTERNS = [
        r"@startuml",
        r"@startmindmap",
        r"@startgantt",
        r"@startditaa",
        r"@startwbs",
        r"@startjson",
        r"@startyaml",
    ]

    # Mermaid start patterns
    MERMAID_PATTERNS = [
        r"^\s*graph\s+",
        r"^\s*flowchart\s+",
        r"^\s*sequenceDiagram",
        r"^\s*classDiagram",
        r"^\s*stateDiagram",
        r"^\s*erDiagram",
        r"^\s*journey",
        r"^\s*gantt",
        r"^\s*pie\s+",
        r"^\s*mindmap",
        r"^\s*timeline",
        r"^\s*gitGraph",
    ]

    # ASCII art patterns (boxes, lines)
    ASCII_BOX_PATTERN = re.compile(r"[+\-|]+.*[+\-|]+", re.MULTILINE)

    def __init__(self):
        """Initialize the diagram detector."""
        self._plantuml_re = [re.compile(p, re.IGNORECASE) for p in self.PLANTUML_PATTERNS]
        self._mermaid_re = [re.compile(p, re.MULTILINE) for p in self.MERMAID_PATTERNS]

    def detect(self, fence_info: str, content: str) -> DiagramType:
        """
        Detect the diagram type from fence info and content.

        Args:
            fence_info: The fence info string (e.g., "mermaid", "plantuml").
            content: The code block content.

        Returns:
            Detected DiagramType.
        """
        # Clean fence info
        info = fence_info.strip().lower().split()[0] if fence_info else ""

        # Check explicit fence type
        if info in self.FENCE_TYPE_MAP:
            diagram_type = self.FENCE_TYPE_MAP[info]

            # For generic "diagram" type, try to auto-detect
            if diagram_type == DiagramType.ASCII and info == "diagram":
                detected = self._auto_detect(content)
                if detected != DiagramType.UNKNOWN:
                    return detected

            return diagram_type

        # Try auto-detection
        return self._auto_detect(content)

    def _auto_detect(self, content: str) -> DiagramType:
        """
        Attempt to auto-detect diagram type from content.

        Args:
            content: The code block content.

        Returns:
            Detected DiagramType or UNKNOWN.
        """
        # Check for PlantUML
        for pattern in self._plantuml_re:
            if pattern.search(content):
                logger.debug("Auto-detected PlantUML diagram")
                return DiagramType.PLANTUML

        # Check for Mermaid
        for pattern in self._mermaid_re:
            if pattern.search(content):
                logger.debug("Auto-detected Mermaid diagram")
                return DiagramType.MERMAID

        # Check for ASCII art patterns
        if self._looks_like_ascii_art(content):
            logger.debug("Auto-detected ASCII diagram")
            return DiagramType.ASCII

        return DiagramType.UNKNOWN

    def _looks_like_ascii_art(self, content: str) -> bool:
        """
        Check if content looks like ASCII art.

        Args:
            content: Content to check.

        Returns:
            True if content appears to be ASCII art.
        """
        lines = content.strip().split("\n")
        if len(lines) < 2:
            return False

        # Check for box characters
        box_chars = set("+-|/\\[]{}()<>*#=")
        box_char_count = sum(1 for c in content if c in box_chars)
        total_non_space = sum(1 for c in content if not c.isspace())

        if total_non_space == 0:
            return False

        # If significant portion is box characters, likely ASCII art
        ratio = box_char_count / total_non_space
        return ratio > 0.1 and self.ASCII_BOX_PATTERN.search(content) is not None

    def is_diagram(self, fence_info: str) -> bool:
        """
        Check if a fence info string indicates a diagram.

        Args:
            fence_info: The fence info string.

        Returns:
            True if this is a known diagram type.
        """
        info = fence_info.strip().lower().split()[0] if fence_info else ""
        return info in self.FENCE_TYPE_MAP

    def get_fence_types(self) -> list[str]:
        """
        Get list of supported fence types.

        Returns:
            List of fence type strings.
        """
        return list(self.FENCE_TYPE_MAP.keys())
