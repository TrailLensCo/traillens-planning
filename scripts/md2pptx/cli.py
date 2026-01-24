# Copyright (c) 2025 TrailLensCo
# All rights reserved.
#
# This file is proprietary and confidential.

"""Command-line interface for md2pptx."""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Optional

from md2pptx import __version__
from md2pptx.converter import MarkdownToPptxConverter
from md2pptx.styles import PresentationStyle, StylePreset, get_style_preset

logger = logging.getLogger(__name__)


def parse_args(args: Optional[list[str]] = None) -> argparse.Namespace:
    """
    Parse command-line arguments.

    Args:
        args: Command-line arguments. Uses sys.argv if None.

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        prog="md2pptx",
        description="Convert Markdown files to PowerPoint (PPTX) presentations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  md2pptx input.md                         # Convert to input.pptx
  md2pptx input.md -o slides.pptx          # Custom output name
  md2pptx input.md --toc                   # Include table of contents
  md2pptx input.md --incremental           # Incremental bullet points
  md2pptx input.md --slide-level 1         # H1 starts new slides
  md2pptx input.md --aspect-ratio 4:3      # Use 4:3 aspect ratio
  md2pptx input.md --style modern          # Use modern style preset
  md2pptx input.md --reference-doc ref.pptx # Use reference PPTX for styling
  md2pptx ./docs/ --batch                  # Batch convert directory
  md2pptx input.md --debug                 # Enable debug logging

Background Image:
  Add to markdown front matter:
    ---
    title: "My Presentation"
    background_image: "path/to/background.jpg"
    ---
""",
    )

    parser.add_argument(
        "input",
        type=Path,
        help="Input markdown file or directory (with --batch)",
    )

    parser.add_argument(
        "-o", "--output",
        type=Path,
        dest="output",
        help="Output file path (default: input with .pptx extension)",
    )

    parser.add_argument(
        "--toc",
        action="store_true",
        help="Include table of contents slide",
    )

    parser.add_argument(
        "--incremental",
        action="store_true",
        help="Show bullet points incrementally",
    )

    parser.add_argument(
        "--slide-level",
        type=int,
        default=2,
        choices=[1, 2, 3, 4, 5, 6],
        dest="slide_level",
        help="Heading level for new slides (default: 2)",
    )

    parser.add_argument(
        "--aspect-ratio",
        choices=["16:9", "4:3"],
        default="16:9",
        dest="aspect_ratio",
        help="Presentation aspect ratio (default: 16:9)",
    )

    parser.add_argument(
        "--style",
        choices=["default", "simple", "modern", "professional"],
        default="default",
        dest="style_preset",
        help="Style preset to use (default: default)",
    )

    parser.add_argument(
        "--reference-doc",
        type=Path,
        dest="reference_doc",
        help="Reference PPTX file for styling",
    )

    parser.add_argument(
        "--batch",
        action="store_true",
        help="Batch convert all .md files in directory",
    )

    parser.add_argument(
        "--pattern",
        default="*.md",
        help="Glob pattern for batch conversion (default: *.md)",
    )

    parser.add_argument(
        "--config",
        type=Path,
        dest="config",
        help="JSON config file with input/output mappings",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress non-error output",
    )

    return parser.parse_args(args)


def setup_logging(debug: bool = False, quiet: bool = False) -> None:
    """
    Configure logging.

    Args:
        debug: Enable debug logging.
        quiet: Suppress non-error output.
    """
    if quiet:
        level = logging.ERROR
    elif debug:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s" if not debug else
               "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def get_style_preset_enum(preset_str: str) -> StylePreset:
    """
    Convert style preset string to StylePreset enum.

    Args:
        preset_str: Style preset string.

    Returns:
        StylePreset enum value.
    """
    presets = {
        "default": StylePreset.DEFAULT,
        "simple": StylePreset.SIMPLE,
        "modern": StylePreset.MODERN,
        "professional": StylePreset.PROFESSIONAL,
    }
    return presets.get(preset_str.lower(), StylePreset.DEFAULT)


def main(args: Optional[list[str]] = None) -> int:
    """
    Main entry point for the CLI.

    Args:
        args: Command-line arguments. Uses sys.argv if None.

    Returns:
        Exit code (0 for success, non-zero for failure).
    """
    parsed_args = parse_args(args)

    # Set up logging
    setup_logging(debug=parsed_args.debug, quiet=parsed_args.quiet)

    # Validate input
    input_path = parsed_args.input
    if not input_path.exists():
        logger.error(f"Input not found: {input_path}")
        return 1

    # Get style with overrides
    style_preset = get_style_preset_enum(parsed_args.style_preset)
    style = get_style_preset(style_preset)

    # Apply CLI overrides
    style.slide_level = parsed_args.slide_level
    style.incremental = parsed_args.incremental
    style.toc = parsed_args.toc
    style.aspect_ratio = parsed_args.aspect_ratio

    if parsed_args.reference_doc:
        if not parsed_args.reference_doc.exists():
            logger.error(f"Reference document not found: {parsed_args.reference_doc}")
            return 1
        style.reference_doc = parsed_args.reference_doc

    # Create converter
    try:
        converter = MarkdownToPptxConverter(
            style=style,
            debug=parsed_args.debug,
        )
    except RuntimeError as e:
        logger.error(str(e))
        return 1

    try:
        if parsed_args.config:
            # Config-based batch conversion
            config_path = parsed_args.config
            if not config_path.exists():
                logger.error(f"Config file not found: {config_path}")
                return 1

            with open(config_path, 'r') as f:
                config = json.load(f)

            output_files = []
            errors = []

            for source_file, file_config in config.items():
                source_path = Path(source_file)
                # For pptx, we need to modify the output extension
                output_path = Path(file_config['docx']).with_suffix('.pptx')

                # Make source path absolute if relative
                if not source_path.is_absolute():
                    source_path = config_path.parent / source_path

                if not source_path.exists():
                    errors.append(f"Source not found: {source_path}")
                    continue

                try:
                    # Create output directory if needed
                    output_path.parent.mkdir(parents=True, exist_ok=True)

                    # Convert
                    result = converter.convert(source_path, output_path)
                    output_files.append(result)

                    if not parsed_args.quiet:
                        print(f"Converted: {source_path} -> {result}")

                except Exception as e:
                    errors.append(f"Failed to convert {source_path}: {e}")

            if errors and not parsed_args.quiet:
                print(f"\nErrors ({len(errors)}):")
                for error in errors:
                    print(f"  {error}")

            if not parsed_args.quiet:
                print(f"\nConverted {len(output_files)}/{len(config)} files")

            return 1 if errors else 0

        elif parsed_args.batch:
            # Batch conversion
            if not input_path.is_dir():
                logger.error(f"Batch mode requires a directory: {input_path}")
                return 1

            output_dir = parsed_args.output if parsed_args.output else input_path
            output_files = converter.batch_convert(
                input_path,
                output_dir,
                pattern=parsed_args.pattern,
            )

            if not parsed_args.quiet:
                print(f"Converted {len(output_files)} files")
                for f in output_files:
                    print(f"  {f}")

        else:
            # Single file conversion
            if input_path.is_dir():
                logger.error(
                    f"Input is a directory. Use --batch for batch conversion."
                )
                return 1

            output_path = converter.convert(input_path, parsed_args.output)

            if not parsed_args.quiet:
                print(f"Created: {output_path}")

        return 0

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return 1
    except PermissionError as e:
        logger.error(f"Permission denied: {e}")
        return 1
    except subprocess.CalledProcessError as e:
        logger.error(f"Pandoc conversion failed: {e.stderr if e.stderr else e}")
        return 1
    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        if parsed_args.debug:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
