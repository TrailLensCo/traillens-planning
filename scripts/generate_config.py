#!/usr/bin/env python3
# Copyright (c) 2025 TrailLensCo
# All rights reserved.
#
# This file is proprietary and confidential.

"""Generate JSON configuration for markdown to docx/pptx conversion."""

import json
import hashlib
from pathlib import Path
from typing import Dict, List


def compute_md5(file_path: Path) -> str:
    """
    Compute MD5 hash of a file.

    Args:
        file_path: Path to the file

    Returns:
        MD5 hash as hex string
    """
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            md5.update(chunk)
    return md5.hexdigest()


def generate_conversion_config(
    docs_dir: Path,
    output_dir: Path,
    exclude_patterns: List[str] = None
) -> Dict[str, Dict[str, str]]:
    """
    Generate conversion configuration for markdown files.

    Args:
        docs_dir: Directory containing markdown files
        output_dir: Directory for output files (relative path)
        exclude_patterns: List of patterns to exclude (case-insensitive)

    Returns:
        Dictionary mapping source files to conversion info
    """
    if exclude_patterns is None:
        exclude_patterns = ['prompt']

    config = {}

    # Find all markdown files
    for md_file in docs_dir.rglob('*.md'):
        # Skip files matching exclude patterns
        if any(pattern.lower() in md_file.name.lower()
               for pattern in exclude_patterns):
            continue

        # Compute relative path from docs_dir
        rel_path = md_file.relative_to(docs_dir)

        # Generate output filename (replace .md with .docx)
        docx_filename = rel_path.with_suffix('.docx')
        output_path = output_dir / docx_filename

        # Compute MD5
        md5_hash = compute_md5(md_file)

        # Create relative paths for JSON (from repository root)
        source_rel = Path('docs') / rel_path
        output_rel = output_path

        config[str(source_rel)] = {
            'md5': md5_hash,
            'docx': str(output_rel),
            'source': str(source_rel)
        }

    return config


def main() -> None:
    """Main entry point."""
    # Get script directory
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent

    # Set up paths
    docs_dir = repo_root / 'docs'
    output_dir = Path('build')
    config_file = docs_dir / 'conversion_config.json'

    if not docs_dir.exists():
        print(f"Error: docs directory not found at {docs_dir}")
        return

    # Generate configuration
    config = generate_conversion_config(
        docs_dir=docs_dir,
        output_dir=output_dir,
        exclude_patterns=['prompt', 'PROMPT']
    )

    # Write configuration to JSON file
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2, sort_keys=True)

    print(f"Generated configuration for {len(config)} files")
    print(f"Configuration written to: {config_file}")


if __name__ == '__main__':
    main()
