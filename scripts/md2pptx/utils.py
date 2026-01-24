# Copyright (c) 2025 TrailLensCo
# All rights reserved.
#
# This file is proprietary and confidential.

"""Utility functions and helpers."""

import logging
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Optional


logger = logging.getLogger(__name__)


class TempFileManager:
    """Manager for temporary files and cleanup."""

    def __init__(self):
        """Initialize temp file manager."""
        self._temp_dir: Optional[Path] = None
        self._temp_files: list[Path] = []

    def get_temp_dir(self) -> Path:
        """
        Get or create a temporary directory.

        Returns:
            Path to temporary directory.
        """
        if self._temp_dir is None:
            self._temp_dir = Path(tempfile.mkdtemp(prefix="md2pptx_"))
            logger.debug(f"Created temp directory: {self._temp_dir}")
        return self._temp_dir

    def create_temp_file(self, suffix: str = "", prefix: str = "temp_") -> Path:
        """
        Create a temporary file.

        Args:
            suffix: File suffix (e.g., ".md", ".pptx").
            prefix: File name prefix.

        Returns:
            Path to temporary file.
        """
        temp_dir = self.get_temp_dir()
        fd, path = tempfile.mkstemp(suffix=suffix, prefix=prefix, dir=temp_dir)
        import os
        os.close(fd)
        temp_path = Path(path)
        self._temp_files.append(temp_path)
        logger.debug(f"Created temp file: {temp_path}")
        return temp_path

    def cleanup(self) -> None:
        """Clean up all temporary files and directories."""
        # Remove individual temp files
        for temp_file in self._temp_files:
            try:
                if temp_file.exists():
                    temp_file.unlink()
                    logger.debug(f"Removed temp file: {temp_file}")
            except Exception as e:
                logger.warning(f"Failed to remove temp file {temp_file}: {e}")

        # Remove temp directory
        if self._temp_dir and self._temp_dir.exists():
            try:
                shutil.rmtree(self._temp_dir)
                logger.debug(f"Removed temp directory: {self._temp_dir}")
            except Exception as e:
                logger.warning(f"Failed to remove temp directory {self._temp_dir}: {e}")

        self._temp_files = []
        self._temp_dir = None


def check_pandoc_installed() -> bool:
    """
    Check if pandoc is installed and available.

    Returns:
        True if pandoc is available, False otherwise.
    """
    try:
        result = subprocess.run(
            ["pandoc", "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            version = result.stdout.split("\n")[0]
            logger.debug(f"Found pandoc: {version}")
            return True
        return False
    except (subprocess.SubprocessError, FileNotFoundError, OSError):
        return False


def setup_logging(debug: bool = False) -> None:
    """
    Configure logging for the application.

    Args:
        debug: Enable debug logging.
    """
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s" if not debug else
               "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
