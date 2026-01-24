# Copyright (c) 2025 TrailLensCo
# All rights reserved.
#
# This file is proprietary and confidential.

"""PlantUML diagram rendering."""

import logging
import os
import shutil
import subprocess
import zlib
from pathlib import Path
from typing import Optional

import requests

from md2docx.utils import TempFileManager

logger = logging.getLogger(__name__)


class PlantUMLRenderer:
    """Renderer for PlantUML diagrams using local jar or public server."""

    # Public PlantUML server
    PUBLIC_SERVER = "https://www.plantuml.com/plantuml"

    # PlantUML jar name pattern
    JAR_NAME = "plantuml.jar"

    # Base64-like encoding for PlantUML server
    PLANTUML_ALPHABET = (
        "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
    )

    def __init__(
        self,
        temp_manager: Optional[TempFileManager] = None,
        jar_path: Optional[str] = None,
        server_url: Optional[str] = None,
        use_server_fallback: bool = True,
    ):
        """
        Initialize the PlantUML renderer.

        Args:
            temp_manager: Temporary file manager.
            jar_path: Path to plantuml.jar.
            server_url: Custom PlantUML server URL.
            use_server_fallback: Fall back to public server if jar not available.
        """
        self.temp_manager = temp_manager or TempFileManager()
        self.jar_path = jar_path
        self.server_url = server_url or self.PUBLIC_SERVER
        self.use_server_fallback = use_server_fallback
        self._jar_available: Optional[bool] = None

    def is_jar_available(self) -> bool:
        """
        Check if PlantUML jar is available.

        Returns:
            True if jar is available and Java is installed.
        """
        if self._jar_available is not None:
            return self._jar_available

        # Check for Java
        java_available = shutil.which("java") is not None
        if not java_available:
            logger.warning("Java not found, PlantUML jar cannot be used")
            self._jar_available = False
            return False

        # Check for jar file
        if self.jar_path:
            jar_exists = Path(self.jar_path).exists()
        else:
            # Look for plantuml.jar in common locations
            jar_exists = self._find_jar() is not None

        self._jar_available = jar_exists

        if jar_exists:
            logger.debug("PlantUML jar is available")
        else:
            logger.info("PlantUML jar not found, will use server fallback")

        return self._jar_available

    def _find_jar(self) -> Optional[Path]:
        """
        Find plantuml.jar in common locations.

        Returns:
            Path to jar file or None.
        """
        search_paths = [
            Path.cwd() / self.JAR_NAME,
            Path.home() / ".local" / "lib" / self.JAR_NAME,
            Path("/usr/local/lib") / self.JAR_NAME,
            Path("/usr/share/java") / self.JAR_NAME,
        ]

        # Check PLANTUML_JAR environment variable
        env_jar = os.environ.get("PLANTUML_JAR")
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
        format: str = "png",
    ) -> Optional[Path]:
        """
        Render a PlantUML diagram.

        Args:
            content: PlantUML diagram source.
            output_path: Output file path. Uses temp file if None.
            format: Output format (png, svg).

        Returns:
            Path to rendered image, or None if rendering failed.
        """
        # Try local jar first
        if self.is_jar_available():
            result = self._render_with_jar(content, output_path, format)
            if result:
                return result

        # Fall back to server
        if self.use_server_fallback:
            return self._render_with_server(content, output_path, format)

        return None

    def _render_with_jar(
        self,
        content: str,
        output_path: Optional[Path],
        format: str,
    ) -> Optional[Path]:
        """
        Render using local PlantUML jar.

        Args:
            content: PlantUML source.
            output_path: Output path.
            format: Output format.

        Returns:
            Path to rendered image or None.
        """
        # Create temp file for input
        input_path = self.temp_manager.create_temp_file(
            suffix=".puml", prefix="plantuml_"
        )

        # Ensure content has @startuml/@enduml
        if "@startuml" not in content.lower():
            content = f"@startuml\n{content}\n@enduml"

        with open(input_path, "w", encoding="utf-8") as f:
            f.write(content)

        # Determine output path
        if output_path is None:
            output_path = self.temp_manager.create_temp_file(
                suffix=f".{format}", prefix="plantuml_out_"
            )

        jar_path = self.jar_path or str(self._find_jar())

        cmd = [
            "java",
            "-jar", jar_path,
            f"-t{format}",
            "-o", str(output_path.parent),
            str(input_path),
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
            )

            if result.returncode != 0:
                logger.error(f"PlantUML jar rendering failed: {result.stderr}")
                return None

            # PlantUML creates output with same base name as input
            expected_output = input_path.with_suffix(f".{format}")
            if expected_output.exists():
                # Move to desired location
                if output_path != expected_output:
                    import shutil
                    shutil.move(expected_output, output_path)
                logger.debug(f"Rendered PlantUML diagram to {output_path}")
                return output_path

        except subprocess.TimeoutExpired:
            logger.error("PlantUML rendering timed out")
        except subprocess.SubprocessError as e:
            logger.error(f"PlantUML rendering error: {e}")

        return None

    def _render_with_server(
        self,
        content: str,
        output_path: Optional[Path],
        format: str,
    ) -> Optional[Path]:
        """
        Render using PlantUML server.

        Args:
            content: PlantUML source.
            output_path: Output path.
            format: Output format.

        Returns:
            Path to rendered image or None.
        """
        # Encode content for URL
        encoded = self._encode_plantuml(content)

        # Build URL
        url = f"{self.server_url}/{format}/{encoded}"

        if output_path is None:
            output_path = self.temp_manager.create_temp_file(
                suffix=f".{format}", prefix="plantuml_srv_"
            )

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            with open(output_path, "wb") as f:
                f.write(response.content)

            logger.debug(f"Rendered PlantUML via server to {output_path}")
            return output_path

        except requests.RequestException as e:
            logger.error(f"PlantUML server rendering failed: {e}")
            return None

    def _encode_plantuml(self, content: str) -> str:
        """
        Encode PlantUML content for server URL.

        Args:
            content: PlantUML source.

        Returns:
            Encoded string.
        """
        # Compress content
        compressed = zlib.compress(content.encode("utf-8"))[2:-4]

        # Encode to PlantUML alphabet
        encoded = []
        for i in range(0, len(compressed), 3):
            if i + 2 < len(compressed):
                b1, b2, b3 = compressed[i], compressed[i + 1], compressed[i + 2]
            elif i + 1 < len(compressed):
                b1, b2, b3 = compressed[i], compressed[i + 1], 0
            else:
                b1, b2, b3 = compressed[i], 0, 0

            encoded.append(self.PLANTUML_ALPHABET[(b1 >> 2) & 0x3F])
            encoded.append(self.PLANTUML_ALPHABET[((b1 << 4) | (b2 >> 4)) & 0x3F])
            encoded.append(self.PLANTUML_ALPHABET[((b2 << 2) | (b3 >> 6)) & 0x3F])
            encoded.append(self.PLANTUML_ALPHABET[b3 & 0x3F])

        return "".join(encoded)
