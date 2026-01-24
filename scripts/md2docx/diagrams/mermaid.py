# Copyright (c) 2025 TrailLensCo
# All rights reserved.
#
# This file is proprietary and confidential.

"""Mermaid diagram rendering."""

import logging
import shutil
import subprocess
from pathlib import Path
from typing import Optional

from md2docx.utils import TempFileManager

logger = logging.getLogger(__name__)


class MermaidRenderer:
    """Renderer for Mermaid diagrams using mermaid-cli (mmdc)."""

    # Default mmdc command
    MMDC_COMMAND = "mmdc"

    # Mermaid config for better output
    DEFAULT_CONFIG = {
        "theme": "default",
        "themeVariables": {
            "fontSize": "14px",
        },
    }

    def __init__(
        self,
        temp_manager: Optional[TempFileManager] = None,
        mmdc_path: Optional[str] = None,
    ):
        """
        Initialize the Mermaid renderer.

        Args:
            temp_manager: Temporary file manager.
            mmdc_path: Custom path to mmdc executable.
        """
        self.temp_manager = temp_manager or TempFileManager()
        self.mmdc_path = mmdc_path or self.MMDC_COMMAND
        self._available: Optional[bool] = None

    def is_available(self) -> bool:
        """
        Check if mermaid-cli (mmdc) is available.

        Returns:
            True if mmdc is available.
        """
        if self._available is not None:
            return self._available

        self._available = shutil.which(self.mmdc_path) is not None

        if self._available:
            logger.debug("Mermaid CLI (mmdc) is available")
        else:
            logger.warning(
                "Mermaid CLI (mmdc) not found. Install with: npm install -g @mermaid-js/mermaid-cli"
            )

        return self._available

    def render(
        self,
        content: str,
        output_path: Optional[Path] = None,
        width: int = 800,
        height: int = 600,
        background_color: str = "white",
    ) -> Optional[Path]:
        """
        Render a Mermaid diagram to PNG.

        Args:
            content: Mermaid diagram source.
            output_path: Output file path. Uses temp file if None.
            width: Output image width.
            height: Output image height.
            background_color: Background color.

        Returns:
            Path to rendered PNG, or None if rendering failed.
        """
        if not self.is_available():
            logger.error("Cannot render Mermaid: mmdc not available")
            return None

        # Create temp file for input
        input_path = self.temp_manager.create_temp_file(
            suffix=".mmd", prefix="mermaid_"
        )

        # Write content to temp file
        with open(input_path, "w", encoding="utf-8") as f:
            f.write(content)

        # Determine output path
        if output_path is None:
            output_path = self.temp_manager.create_temp_file(
                suffix=".png", prefix="mermaid_out_"
            )

        # Build command
        cmd = [
            self.mmdc_path,
            "-i", str(input_path),
            "-o", str(output_path),
            "-w", str(width),
            "-H", str(height),
            "-b", background_color,
            "--quiet",
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
            )

            if result.returncode != 0:
                logger.error(f"Mermaid rendering failed: {result.stderr}")
                return None

            if output_path.exists():
                logger.debug(f"Rendered Mermaid diagram to {output_path}")
                return output_path
            else:
                logger.error("Mermaid output file not created")
                return None

        except subprocess.TimeoutExpired:
            logger.error("Mermaid rendering timed out")
            return None
        except subprocess.SubprocessError as e:
            logger.error(f"Mermaid rendering error: {e}")
            return None

    def render_svg(
        self,
        content: str,
        output_path: Optional[Path] = None,
    ) -> Optional[Path]:
        """
        Render a Mermaid diagram to SVG.

        Args:
            content: Mermaid diagram source.
            output_path: Output file path. Uses temp file if None.

        Returns:
            Path to rendered SVG, or None if rendering failed.
        """
        if not self.is_available():
            return None

        # Create temp file for input
        input_path = self.temp_manager.create_temp_file(
            suffix=".mmd", prefix="mermaid_"
        )

        with open(input_path, "w", encoding="utf-8") as f:
            f.write(content)

        if output_path is None:
            output_path = self.temp_manager.create_temp_file(
                suffix=".svg", prefix="mermaid_out_"
            )

        cmd = [
            self.mmdc_path,
            "-i", str(input_path),
            "-o", str(output_path),
            "--quiet",
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
            )

            if result.returncode == 0 and output_path.exists():
                return output_path

        except (subprocess.TimeoutExpired, subprocess.SubprocessError) as e:
            logger.error(f"Mermaid SVG rendering error: {e}")

        return None

    def get_version(self) -> Optional[str]:
        """
        Get the mermaid-cli version.

        Returns:
            Version string or None if not available.
        """
        if not self.is_available():
            return None

        try:
            result = subprocess.run(
                [self.mmdc_path, "--version"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except (subprocess.TimeoutExpired, subprocess.SubprocessError):
            pass

        return None
