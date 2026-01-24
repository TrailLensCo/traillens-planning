# Copyright (c) 2025 TrailLensCo
# All rights reserved.
#
# This file is proprietary and confidential.

"""Utility functions and helpers for md2docx."""

import hashlib
import logging
import os
import shutil
import tempfile
from pathlib import Path
from typing import Optional, Union
from urllib.parse import urlparse

import requests

logger = logging.getLogger(__name__)


class TempFileManager:
    """Manages temporary files and directories for the conversion process."""

    def __init__(self, base_dir: Optional[Path] = None):
        """
        Initialize the temp file manager.

        Args:
            base_dir: Base directory for temp files. Uses system temp if None.
        """
        self._base_dir = base_dir
        self._temp_dirs: list[Path] = []
        self._temp_files: list[Path] = []

    def create_temp_dir(self, prefix: str = "md2docx_") -> Path:
        """
        Create a temporary directory.

        Args:
            prefix: Prefix for the directory name.

        Returns:
            Path to the created directory.
        """
        if self._base_dir:
            temp_dir = Path(tempfile.mkdtemp(prefix=prefix, dir=self._base_dir))
        else:
            temp_dir = Path(tempfile.mkdtemp(prefix=prefix))
        self._temp_dirs.append(temp_dir)
        return temp_dir

    def create_temp_file(
        self, suffix: str = "", prefix: str = "md2docx_"
    ) -> Path:
        """
        Create a temporary file.

        Args:
            suffix: File extension/suffix.
            prefix: Prefix for the filename.

        Returns:
            Path to the created file.
        """
        fd, path = tempfile.mkstemp(suffix=suffix, prefix=prefix)
        os.close(fd)
        temp_path = Path(path)
        self._temp_files.append(temp_path)
        return temp_path

    def cleanup(self) -> None:
        """Clean up all temporary files and directories."""
        for temp_file in self._temp_files:
            try:
                if temp_file.exists():
                    temp_file.unlink()
            except OSError as e:
                logger.warning(f"Failed to delete temp file {temp_file}: {e}")

        for temp_dir in self._temp_dirs:
            try:
                if temp_dir.exists():
                    shutil.rmtree(temp_dir)
            except OSError as e:
                logger.warning(f"Failed to delete temp dir {temp_dir}: {e}")

        self._temp_files.clear()
        self._temp_dirs.clear()

    def __enter__(self) -> "TempFileManager":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit - cleanup temp files."""
        self.cleanup()


def compute_content_hash(content: Union[str, bytes]) -> str:
    """
    Compute a SHA256 hash of content for caching purposes.

    Args:
        content: String or bytes content to hash.

    Returns:
        Hexadecimal hash string.
    """
    if isinstance(content, str):
        content = content.encode("utf-8")
    return hashlib.sha256(content).hexdigest()[:16]


def is_url(path: str) -> bool:
    """
    Check if a path is a URL.

    Args:
        path: Path string to check.

    Returns:
        True if the path is a URL.
    """
    try:
        result = urlparse(path)
        return result.scheme in ("http", "https")
    except Exception:
        return False


def download_file(
    url: str, dest_path: Path, timeout: int = 30
) -> Optional[Path]:
    """
    Download a file from a URL.

    Args:
        url: URL to download from.
        dest_path: Destination path for the downloaded file.
        timeout: Request timeout in seconds.

    Returns:
        Path to downloaded file, or None if download failed.
    """
    try:
        response = requests.get(url, timeout=timeout, stream=True)
        response.raise_for_status()

        with open(dest_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return dest_path
    except requests.RequestException as e:
        logger.warning(f"Failed to download {url}: {e}")
        return None


def resolve_path(
    path: str, base_dir: Optional[Path] = None
) -> Optional[Path]:
    """
    Resolve a path relative to a base directory.

    Args:
        path: Path string (can be relative or absolute).
        base_dir: Base directory for relative paths.

    Returns:
        Resolved absolute Path, or None if resolution failed.
    """
    if is_url(path):
        return None

    path_obj = Path(path)
    if path_obj.is_absolute():
        return path_obj if path_obj.exists() else None

    if base_dir:
        resolved = base_dir / path_obj
        if resolved.exists():
            return resolved

    # Try current directory
    if path_obj.exists():
        return path_obj.absolute()

    return None


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename by removing invalid characters.

    Args:
        filename: Original filename.

    Returns:
        Sanitized filename safe for filesystem use.
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, "_")
    return filename.strip()


def inches_to_emu(inches: float) -> int:
    """
    Convert inches to EMUs (English Metric Units).

    Args:
        inches: Value in inches.

    Returns:
        Value in EMUs (914400 EMUs per inch).
    """
    return int(inches * 914400)


def pt_to_twips(points: float) -> int:
    """
    Convert points to twips.

    Args:
        points: Value in points.

    Returns:
        Value in twips (20 twips per point).
    """
    return int(points * 20)


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """
    Convert hex color to RGB tuple.

    Args:
        hex_color: Hex color string (with or without #).

    Returns:
        Tuple of (red, green, blue) values 0-255.
    """
    hex_color = hex_color.lstrip("#")
    return (
        int(hex_color[0:2], 16),
        int(hex_color[2:4], 16),
        int(hex_color[4:6], 16),
    )


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """
    Convert RGB values to hex color string.

    Args:
        r: Red value 0-255.
        g: Green value 0-255.
        b: Blue value 0-255.

    Returns:
        Hex color string without #.
    """
    return f"{r:02X}{g:02X}{b:02X}"


def setup_logging(debug: bool = False) -> None:
    """
    Configure logging for md2docx.

    Args:
        debug: Enable debug logging if True.
    """
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
