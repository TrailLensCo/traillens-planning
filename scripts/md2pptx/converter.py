# Copyright (c) 2025 TrailLensCo
# All rights reserved.
#
# This file is proprietary and confidential.

"""Main conversion orchestration for markdown to PPTX."""

import logging
import subprocess
from pathlib import Path
from typing import Optional

from md2pptx.parser import MarkdownParser, PresentationMetadata
from md2pptx.reference import ReferenceDocGenerator
from md2pptx.styles import PresentationStyle, StylePreset, get_style_preset
from md2pptx.utils import TempFileManager, check_pandoc_installed, setup_logging

logger = logging.getLogger(__name__)


class MarkdownToPptxConverter:
    """Converts Markdown files to PowerPoint (PPTX) presentations."""

    def __init__(
        self,
        style: Optional[PresentationStyle] = None,
        style_preset: Optional[StylePreset] = None,
        debug: bool = False,
    ):
        """
        Initialize the converter.

        Args:
            style: Custom presentation style. Uses default if None.
            style_preset: Style preset to use (ignored if style provided).
            debug: Enable debug logging.

        Raises:
            RuntimeError: If pandoc is not installed.
        """
        if debug:
            setup_logging(debug=True)

        # Check for pandoc
        if not check_pandoc_installed():
            raise RuntimeError(
                "Pandoc is not installed or not in PATH. "
                "Please install pandoc: https://pandoc.org/installing.html"
            )

        # Set up style
        if style:
            self.style = style
        elif style_preset:
            self.style = get_style_preset(style_preset)
        else:
            self.style = PresentationStyle()

        # Initialize components
        self.parser = MarkdownParser()
        self.temp_manager = TempFileManager()
        self.ref_generator = ReferenceDocGenerator()

        logger.debug("Converter initialized")

    def convert(
        self,
        input_path: Path,
        output_path: Optional[Path] = None,
    ) -> Path:
        """
        Convert a markdown file to PPTX.

        Args:
            input_path: Path to the markdown file.
            output_path: Output path. Defaults to input with .pptx extension.

        Returns:
            Path to the generated PPTX file.

        Raises:
            FileNotFoundError: If input file doesn't exist.
            subprocess.CalledProcessError: If pandoc conversion fails.
        """
        input_path = Path(input_path)

        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        if output_path is None:
            output_path = input_path.with_suffix(".pptx")
        else:
            output_path = Path(output_path)

        logger.info(f"Converting {input_path} to {output_path}")

        # Read markdown content
        with open(input_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Convert content
        self.convert_string(
            content,
            output_path,
            base_dir=input_path.parent,
        )

        return output_path

    def convert_string(
        self,
        markdown_content: str,
        output_path: Path,
        base_dir: Optional[Path] = None,
    ) -> Path:
        """
        Convert markdown string to PPTX.

        Args:
            markdown_content: Markdown content string.
            output_path: Output file path.
            base_dir: Base directory for resolving relative paths.

        Returns:
            Path to the generated PPTX file.

        Raises:
            subprocess.CalledProcessError: If pandoc conversion fails.
        """
        try:
            # Parse front matter
            metadata, markdown_body = self.parser.parse_front_matter(
                markdown_content, base_dir
            )

            # Create temporary markdown file
            temp_md = self.temp_manager.create_temp_file(suffix=".md")

            # Build pandoc metadata if not in front matter
            markdown_with_meta = self._build_markdown_with_metadata(
                markdown_body, metadata
            )

            with open(temp_md, "w", encoding="utf-8") as f:
                f.write(markdown_with_meta)

            # Prepare reference document if background image specified
            reference_doc = None
            if metadata.background_image:
                if self.ref_generator.validate_image(metadata.background_image):
                    reference_doc = self.temp_manager.create_temp_file(suffix=".pptx")
                    self.ref_generator.create_with_background(
                        metadata.background_image,
                        reference_doc,
                        metadata.aspect_ratio,
                    )
                else:
                    logger.warning("Background image validation failed, proceeding without it")

            # Build pandoc command
            cmd = self._build_pandoc_command(
                temp_md,
                output_path,
                metadata,
                reference_doc,
            )

            # Run pandoc
            logger.debug(f"Running pandoc: {' '.join(str(x) for x in cmd)}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
            )

            if result.returncode != 0:
                logger.error(f"Pandoc failed with error:\n{result.stderr}")
                raise subprocess.CalledProcessError(
                    result.returncode,
                    cmd,
                    output=result.stdout,
                    stderr=result.stderr,
                )

            logger.info(f"Successfully created {output_path}")
            return output_path

        finally:
            # Clean up temp files
            self.temp_manager.cleanup()

    def _build_markdown_with_metadata(
        self,
        markdown_body: str,
        metadata: PresentationMetadata,
    ) -> str:
        """
        Build markdown with pandoc-compatible metadata block.

        Args:
            markdown_body: Markdown content without front matter.
            metadata: Presentation metadata.

        Returns:
            Markdown string with metadata.
        """
        # Build YAML front matter for pandoc
        yaml_parts = ["---"]

        if metadata.title:
            yaml_parts.append(f"title: {metadata.title}")
        if metadata.author:
            yaml_parts.append(f"author: {metadata.author}")
        if metadata.date:
            yaml_parts.append(f"date: {metadata.date}")
        if metadata.subtitle:
            yaml_parts.append(f"subtitle: {metadata.subtitle}")
        if metadata.institute:
            yaml_parts.append(f"institute: {metadata.institute}")

        yaml_parts.append("---")
        yaml_parts.append("")

        return "\n".join(yaml_parts) + markdown_body

    def _build_pandoc_command(
        self,
        input_path: Path,
        output_path: Path,
        metadata: PresentationMetadata,
        reference_doc: Optional[Path] = None,
    ) -> list[str]:
        """
        Build pandoc command with all options.

        Args:
            input_path: Input markdown file path.
            output_path: Output PPTX file path.
            metadata: Presentation metadata.
            reference_doc: Optional reference PPTX for styling.

        Returns:
            List of command arguments.
        """
        cmd = [
            "pandoc",
            str(input_path),
            "-o", str(output_path),
            "-t", "pptx",
        ]

        # Add slide level
        cmd.extend(["--slide-level", str(self.style.slide_level)])

        # Add reference document if provided
        if reference_doc:
            cmd.extend(["--reference-doc", str(reference_doc)])
        elif self.style.reference_doc:
            cmd.extend(["--reference-doc", str(self.style.reference_doc)])

        # Add TOC if requested
        if self.style.toc:
            cmd.append("--toc")
            cmd.extend(["--toc-depth", str(self.style.toc_depth)])

        # Add incremental bullets if requested
        if self.style.incremental:
            cmd.append("--incremental")

        # Add standalone flag
        cmd.append("--standalone")

        return cmd

    def batch_convert(
        self,
        input_dir: Path,
        output_dir: Optional[Path] = None,
        pattern: str = "*.md",
    ) -> list[Path]:
        """
        Batch convert markdown files in a directory.

        Args:
            input_dir: Input directory containing markdown files.
            output_dir: Output directory. Uses input_dir if None.
            pattern: Glob pattern for markdown files.

        Returns:
            List of paths to generated PPTX files.
        """
        input_dir = Path(input_dir)
        output_dir = Path(output_dir) if output_dir else input_dir

        output_dir.mkdir(parents=True, exist_ok=True)

        output_files = []
        for md_file in input_dir.glob(pattern):
            output_path = output_dir / md_file.with_suffix(".pptx").name
            try:
                self.convert(md_file, output_path)
                output_files.append(output_path)
            except Exception as e:
                logger.error(f"Failed to convert {md_file}: {e}")

        logger.info(f"Batch converted {len(output_files)} files")
        return output_files
