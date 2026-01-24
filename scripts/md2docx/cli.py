# Copyright (c) 2025 TrailLensCo
# All rights reserved.
#
# This file is proprietary and confidential.

"""Command-line interface for md2docx."""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Optional

from md2docx import __version__
from md2docx.converter import MarkdownToDocxConverter
from md2docx.styles import PageSize, StylePreset, get_style_preset

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
        prog="md2docx",
        description="Convert Markdown files to Word (DOCX) documents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  md2docx input.md                      # Convert to input.docx
  md2docx input.md -o report.docx       # Custom output name
  md2docx input.md --toc                # Include table of contents
  md2docx input.md --no-diagrams        # Skip diagram rendering
  md2docx input.md --no-title-page      # Skip title page
  md2docx input.md --page-size A4       # Use A4 page size
  md2docx input.md --style minimal      # Use minimal style preset
  md2docx ./docs/ --batch               # Batch convert directory
  md2docx input.md --debug              # Enable debug logging
""",
    )

    parser.add_argument(
        "input",
        type=Path,
        nargs='?',
        help="Input markdown file or directory (with --batch), or omit when using --config",
    )

    parser.add_argument(
        "-o", "--output",
        type=Path,
        dest="output",
        help="Output file path (default: input with .docx extension)",
    )

    parser.add_argument(
        "--toc",
        action="store_true",
        help="Include table of contents",
    )

    parser.add_argument(
        "--no-diagrams",
        action="store_true",
        dest="no_diagrams",
        help="Skip diagram rendering",
    )

    parser.add_argument(
        "--no-title-page",
        action="store_true",
        dest="no_title_page",
        help="Skip title page even if metadata present",
    )

    parser.add_argument(
        "--page-size",
        choices=["letter", "Letter", "LETTER", "a4", "A4"],
        default="letter",
        dest="page_size",
        help="Page size (default: letter)",
    )

    parser.add_argument(
        "--style",
        choices=["default", "minimal", "academic", "modern"],
        default="default",
        dest="style_preset",
        help="Style preset to use (default: default)",
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


def get_page_size(size_str: str) -> PageSize:
    """
    Convert page size string to PageSize enum.

    Args:
        size_str: Page size string.

    Returns:
        PageSize enum value.
    """
    if size_str.upper() == "A4":
        return PageSize.A4
    return PageSize.LETTER


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
        "minimal": StylePreset.MINIMAL,
        "academic": StylePreset.ACADEMIC,
        "modern": StylePreset.MODERN,
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
    if not parsed_args.config and not input_path:
        logger.error("Either input file or --config must be provided")
        return 1
    if input_path and not input_path.exists():
        logger.error(f"Input not found: {input_path}")
        return 1

    # Get style with page size override
    style_preset = get_style_preset_enum(parsed_args.style_preset)
    style = get_style_preset(style_preset)
    style.page.size = get_page_size(parsed_args.page_size)

    # Create converter
    converter = MarkdownToDocxConverter(
        style=style,
        enable_diagrams=not parsed_args.no_diagrams,
        include_toc=parsed_args.toc,
        include_title_page=not parsed_args.no_title_page,
        debug=parsed_args.debug,
    )

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
                output_path = Path(file_config['docx'])

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
    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        if parsed_args.debug:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
