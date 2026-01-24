# Copyright (c) 2025 TrailLensCo
# All rights reserved.
#
# This file is proprietary and confidential.

"""Ditaa and ASCII art diagram rendering."""

import logging
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Optional

from md2docx.utils import TempFileManager

logger = logging.getLogger(__name__)

# Optional PIL import for basic ASCII rendering
try:
    from PIL import Image, ImageDraw, ImageFont

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    logger.debug("PIL not available for basic ASCII rendering")


class DitaaRenderer:
    """Renderer for Ditaa and ASCII art diagrams."""

    # Ditaa jar name
    JAR_NAME = "ditaa.jar"

    # Font settings for ASCII rendering
    FONT_SIZE = 14
    LINE_HEIGHT = 18
    CHAR_WIDTH = 8

    def __init__(
        self,
        temp_manager: Optional[TempFileManager] = None,
        jar_path: Optional[str] = None,
    ):
        """
        Initialize the Ditaa renderer.

        Args:
            temp_manager: Temporary file manager.
            jar_path: Path to ditaa.jar.
        """
        self.temp_manager = temp_manager or TempFileManager()
        self.jar_path = jar_path
        self._jar_available: Optional[bool] = None

    def is_jar_available(self) -> bool:
        """
        Check if Ditaa jar is available.

        Returns:
            True if jar is available and Java is installed.
        """
        if self._jar_available is not None:
            return self._jar_available

        # Check for Java
        java_available = shutil.which("java") is not None
        if not java_available:
            self._jar_available = False
            return False

        # Check for jar file
        if self.jar_path:
            jar_exists = Path(self.jar_path).exists()
        else:
            jar_exists = self._find_jar() is not None

        self._jar_available = jar_exists
        return self._jar_available

    def _find_jar(self) -> Optional[Path]:
        """
        Find ditaa.jar in common locations.

        Returns:
            Path to jar file or None.
        """
        search_paths = [
            Path.cwd() / self.JAR_NAME,
            Path.home() / ".local" / "lib" / self.JAR_NAME,
            Path("/usr/local/lib") / self.JAR_NAME,
            Path("/usr/share/java") / self.JAR_NAME,
        ]

        env_jar = os.environ.get("DITAA_JAR")
        if env_jar:
            search_paths.insert(0, Path(env_jar))

        for path in search_paths:
            if path.exists():
                self.jar_path = str(path)
                return path

        return None

    def render(
        self,
        content: str,
        output_path: Optional[Path] = None,
    ) -> Optional[Path]:
        """
        Render a Ditaa/ASCII diagram.

        Args:
            content: Diagram source (ASCII art).
            output_path: Output file path.

        Returns:
            Path to rendered PNG, or None if rendering failed.
        """
        # Try ditaa jar first
        if self.is_jar_available():
            result = self._render_with_ditaa(content, output_path)
            if result:
                return result

        # Fall back to basic ASCII rendering with PIL
        if PIL_AVAILABLE:
            return self._render_with_pil(content, output_path)

        logger.warning("Neither Ditaa nor PIL available for ASCII rendering")
        return None

    def _render_with_ditaa(
        self,
        content: str,
        output_path: Optional[Path],
    ) -> Optional[Path]:
        """
        Render using Ditaa jar.

        Args:
            content: ASCII art source.
            output_path: Output path.

        Returns:
            Path to rendered image or None.
        """
        input_path = self.temp_manager.create_temp_file(
            suffix=".txt", prefix="ditaa_"
        )

        with open(input_path, "w", encoding="utf-8") as f:
            f.write(content)

        if output_path is None:
            output_path = self.temp_manager.create_temp_file(
                suffix=".png", prefix="ditaa_out_"
            )

        jar_path = self.jar_path or str(self._find_jar())

        cmd = [
            "java",
            "-jar", jar_path,
            str(input_path),
            str(output_path),
            "--no-shadows",
            "--no-antialias",
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
            )

            if result.returncode == 0 and output_path.exists():
                logger.debug(f"Rendered Ditaa diagram to {output_path}")
                return output_path

            logger.error(f"Ditaa rendering failed: {result.stderr}")

        except subprocess.TimeoutExpired:
            logger.error("Ditaa rendering timed out")
        except subprocess.SubprocessError as e:
            logger.error(f"Ditaa rendering error: {e}")

        return None

    def _render_with_pil(
        self,
        content: str,
        output_path: Optional[Path],
    ) -> Optional[Path]:
        """
        Render ASCII art using PIL (basic rendering).

        Args:
            content: ASCII art source.
            output_path: Output path.

        Returns:
            Path to rendered image or None.
        """
        if not PIL_AVAILABLE:
            return None

        lines = content.split("\n")

        # Calculate image dimensions
        max_line_length = max(len(line) for line in lines) if lines else 0
        width = max(max_line_length * self.CHAR_WIDTH + 40, 100)
        height = max(len(lines) * self.LINE_HEIGHT + 40, 50)

        # Create image with white background
        image = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(image)

        # Try to use a monospace font
        try:
            font = ImageFont.truetype("DejaVuSansMono.ttf", self.FONT_SIZE)
        except (OSError, IOError):
            try:
                font = ImageFont.truetype("Courier", self.FONT_SIZE)
            except (OSError, IOError):
                font = ImageFont.load_default()

        # Draw text
        y = 20
        for line in lines:
            draw.text((20, y), line, fill="black", font=font)
            y += self.LINE_HEIGHT

        # Detect and draw boxes/lines
        self._draw_boxes(draw, lines, font)

        # Save image
        if output_path is None:
            output_path = self.temp_manager.create_temp_file(
                suffix=".png", prefix="ascii_"
            )

        image.save(output_path, "PNG")
        logger.debug(f"Rendered ASCII diagram with PIL to {output_path}")
        return output_path

    def _draw_boxes(self, draw: "ImageDraw", lines: list[str], font) -> None:
        """
        Detect and enhance box drawings in ASCII art.

        This is a basic implementation that detects common box patterns.

        Args:
            draw: PIL ImageDraw object.
            lines: Lines of ASCII art.
            font: Font being used.
        """
        # This is a simplified implementation
        # A full implementation would detect box corners and draw proper lines

        # Look for horizontal lines made of dashes
        for y_idx, line in enumerate(lines):
            # Find sequences of dashes
            for match in re.finditer(r"-{3,}", line):
                x1 = 20 + match.start() * self.CHAR_WIDTH
                x2 = 20 + match.end() * self.CHAR_WIDTH
                y = 20 + y_idx * self.LINE_HEIGHT + self.LINE_HEIGHT // 2

                # Draw a slightly thicker line over the dashes
                draw.line([(x1, y), (x2, y)], fill="black", width=1)

    def detect_ascii_art(self, content: str) -> bool:
        """
        Detect if content is ASCII art.

        Args:
            content: Content to check.

        Returns:
            True if content appears to be ASCII art.
        """
        lines = content.strip().split("\n")
        if len(lines) < 2:
            return False

        # Check for box characters
        box_chars = set("+-|/\\[]{}()<>*")
        total_chars = sum(len(line) for line in lines)
        box_char_count = sum(
            1 for line in lines for c in line if c in box_chars
        )

        if total_chars == 0:
            return False

        ratio = box_char_count / total_chars
        return ratio > 0.05  # At least 5% box characters
