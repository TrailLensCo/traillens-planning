# Copyright (c) 2025 TrailLensCo
# All rights reserved.
#
# This file is proprietary and confidential.

"""Test script for md2docx converter."""

import os
import sys
import tempfile
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def test_basic_conversion():
    """Test basic markdown to docx conversion."""
    from md2docx.converter import MarkdownToDocxConverter

    # Simple markdown content
    markdown = """# Test Document

This is a **test** paragraph with *formatting*.

## Section 1

- Item 1
- Item 2
- Item 3

## Section 2

```python
def hello():
    print("Hello, World!")
```

| Name | Value |
|------|-------|
| A    | 1     |
| B    | 2     |
"""

    converter = MarkdownToDocxConverter(
        enable_diagrams=False,
        include_toc=False,
        include_title_page=False,
    )

    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as f:
        output_path = Path(f.name)

    try:
        result = converter.convert_string(markdown, output_path)

        assert result.exists(), "Output file should exist"
        assert result.stat().st_size > 0, "Output file should not be empty"

        print(f"SUCCESS: Basic conversion test passed")
        print(f"  Output: {result}")
        print(f"  Size: {result.stat().st_size} bytes")
        return True

    except Exception as e:
        print(f"FAILED: Basic conversion test failed: {e}")
        return False

    finally:
        if output_path.exists():
            output_path.unlink()


def test_frontmatter_parsing():
    """Test YAML front matter parsing."""
    from md2docx.parser import MarkdownParser

    markdown = """---
title: Test Title
author: Test Author
date: 2025-01-14
abstract: This is an abstract.
---

# Content

Body text here.
"""

    parser = MarkdownParser()
    metadata, tokens = parser.parse(markdown)

    assert metadata.title == "Test Title", "Title should be parsed"
    assert metadata.author == "Test Author", "Author should be parsed"
    assert metadata.date == "2025-01-14", "Date should be parsed"
    assert metadata.abstract == "This is an abstract.", "Abstract should be parsed"

    print("SUCCESS: Front matter parsing test passed")
    return True


def test_sample_document():
    """Test conversion of the sample document."""
    from md2docx.converter import MarkdownToDocxConverter

    # Find the sample document
    script_dir = Path(__file__).parent.parent
    sample_path = script_dir / "samples" / "sample.md"

    if not sample_path.exists():
        print(f"SKIPPED: Sample document not found at {sample_path}")
        return True

    converter = MarkdownToDocxConverter(
        enable_diagrams=False,  # Skip diagrams for basic test
        include_toc=True,
        include_title_page=True,
    )

    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as f:
        output_path = Path(f.name)

    try:
        result = converter.convert(sample_path, output_path)

        assert result.exists(), "Output file should exist"
        assert result.stat().st_size > 10000, "Sample output should be substantial"

        print(f"SUCCESS: Sample document conversion test passed")
        print(f"  Input: {sample_path}")
        print(f"  Output: {result}")
        print(f"  Size: {result.stat().st_size} bytes")
        return True

    except Exception as e:
        print(f"FAILED: Sample document conversion failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        if output_path.exists():
            output_path.unlink()


def test_style_presets():
    """Test different style presets."""
    from md2docx.styles import StylePreset, get_style_preset

    for preset in StylePreset:
        style = get_style_preset(preset)
        assert style is not None, f"Style preset {preset} should return a style"
        assert style.heading1 is not None, f"Style should have heading1"

    print("SUCCESS: Style presets test passed")
    return True


def test_cli_help():
    """Test CLI help output."""
    from md2docx.cli import main

    try:
        # Capture help output
        import io
        import contextlib

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            try:
                main(["--help"])
            except SystemExit:
                pass

        output = f.getvalue()
        assert "md2docx" in output or len(output) > 0

        print("SUCCESS: CLI help test passed")
        return True

    except Exception as e:
        print(f"FAILED: CLI help test failed: {e}")
        return False


def run_all_tests():
    """Run all tests and report results."""
    print("=" * 60)
    print("md2docx Test Suite")
    print("=" * 60)
    print()

    tests = [
        ("Front matter parsing", test_frontmatter_parsing),
        ("Style presets", test_style_presets),
        ("Basic conversion", test_basic_conversion),
        ("Sample document", test_sample_document),
        ("CLI help", test_cli_help),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        print(f"\nRunning: {name}")
        print("-" * 40)
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"FAILED: {name} raised exception: {e}")
            failed += 1

    print()
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
