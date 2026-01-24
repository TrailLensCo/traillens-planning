# Copyright (c) 2025 TrailLensCo
# All rights reserved.
#
# This file is proprietary and confidential.

"""Diagram caching for avoiding re-rendering."""

import json
import logging
import os
import time
from pathlib import Path
from typing import Optional

from md2docx.utils import compute_content_hash

logger = logging.getLogger(__name__)


class DiagramCache:
    """Cache for rendered diagram images."""

    # Cache metadata file name
    CACHE_META_FILE = "cache_meta.json"

    # Default cache expiry (7 days)
    DEFAULT_EXPIRY_SECONDS = 7 * 24 * 60 * 60

    def __init__(
        self,
        cache_dir: Optional[Path] = None,
        expiry_seconds: int = DEFAULT_EXPIRY_SECONDS,
    ):
        """
        Initialize the diagram cache.

        Args:
            cache_dir: Directory for cached images. Uses temp dir if None.
            expiry_seconds: Cache entry expiry time in seconds.
        """
        if cache_dir is None:
            # Use a default cache directory in user's home
            cache_dir = Path.home() / ".cache" / "md2docx" / "diagrams"

        self.cache_dir = cache_dir
        self.expiry_seconds = expiry_seconds
        self._meta: dict = {}

        # Ensure cache directory exists
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Load existing cache metadata
        self._load_meta()

    def get(self, content: str, diagram_type: str) -> Optional[Path]:
        """
        Get a cached diagram image if available.

        Args:
            content: Diagram source content.
            diagram_type: Type of diagram (mermaid, plantuml, etc.).

        Returns:
            Path to cached image, or None if not cached/expired.
        """
        cache_key = self._make_key(content, diagram_type)

        if cache_key not in self._meta:
            logger.debug(f"Cache miss for {diagram_type} diagram")
            return None

        entry = self._meta[cache_key]

        # Check expiry
        if time.time() - entry["timestamp"] > self.expiry_seconds:
            logger.debug(f"Cache entry expired for {diagram_type} diagram")
            self._remove_entry(cache_key)
            return None

        # Check if file exists
        image_path = Path(entry["path"])
        if not image_path.exists():
            logger.debug(f"Cached file missing for {diagram_type} diagram")
            self._remove_entry(cache_key)
            return None

        logger.debug(f"Cache hit for {diagram_type} diagram")
        return image_path

    def put(
        self, content: str, diagram_type: str, image_path: Path
    ) -> Path:
        """
        Store a diagram image in the cache.

        Args:
            content: Diagram source content.
            diagram_type: Type of diagram.
            image_path: Path to the rendered image.

        Returns:
            Path to the cached image.
        """
        cache_key = self._make_key(content, diagram_type)

        # Generate cached file path
        content_hash = compute_content_hash(content)
        suffix = image_path.suffix or ".png"
        cached_path = self.cache_dir / f"{diagram_type}_{content_hash}{suffix}"

        # Copy file to cache
        if image_path != cached_path:
            import shutil
            shutil.copy2(image_path, cached_path)

        # Update metadata
        self._meta[cache_key] = {
            "path": str(cached_path),
            "timestamp": time.time(),
            "diagram_type": diagram_type,
        }

        self._save_meta()
        logger.debug(f"Cached {diagram_type} diagram as {cached_path.name}")

        return cached_path

    def clear(self) -> int:
        """
        Clear all cached diagrams.

        Returns:
            Number of entries cleared.
        """
        count = 0
        for key in list(self._meta.keys()):
            self._remove_entry(key)
            count += 1

        self._save_meta()
        logger.info(f"Cleared {count} cached diagrams")
        return count

    def cleanup_expired(self) -> int:
        """
        Remove expired cache entries.

        Returns:
            Number of entries removed.
        """
        count = 0
        current_time = time.time()

        for key in list(self._meta.keys()):
            entry = self._meta[key]
            if current_time - entry["timestamp"] > self.expiry_seconds:
                self._remove_entry(key)
                count += 1

        if count > 0:
            self._save_meta()
            logger.info(f"Removed {count} expired cache entries")

        return count

    def _make_key(self, content: str, diagram_type: str) -> str:
        """
        Create a cache key from content and type.

        Args:
            content: Diagram content.
            diagram_type: Diagram type.

        Returns:
            Cache key string.
        """
        content_hash = compute_content_hash(content)
        return f"{diagram_type}:{content_hash}"

    def _remove_entry(self, key: str) -> None:
        """
        Remove a cache entry.

        Args:
            key: Cache key to remove.
        """
        if key in self._meta:
            entry = self._meta[key]
            # Try to delete the cached file
            try:
                path = Path(entry["path"])
                if path.exists():
                    path.unlink()
            except OSError as e:
                logger.warning(f"Failed to delete cached file: {e}")

            del self._meta[key]

    def _load_meta(self) -> None:
        """Load cache metadata from disk."""
        meta_path = self.cache_dir / self.CACHE_META_FILE
        if meta_path.exists():
            try:
                with open(meta_path, "r", encoding="utf-8") as f:
                    self._meta = json.load(f)
                logger.debug(f"Loaded {len(self._meta)} cache entries")
            except (json.JSONDecodeError, OSError) as e:
                logger.warning(f"Failed to load cache metadata: {e}")
                self._meta = {}
        else:
            self._meta = {}

    def _save_meta(self) -> None:
        """Save cache metadata to disk."""
        meta_path = self.cache_dir / self.CACHE_META_FILE
        try:
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(self._meta, f, indent=2)
        except OSError as e:
            logger.warning(f"Failed to save cache metadata: {e}")

    @property
    def size(self) -> int:
        """Get the number of cached entries."""
        return len(self._meta)

    @property
    def cache_path(self) -> Path:
        """Get the cache directory path."""
        return self.cache_dir
