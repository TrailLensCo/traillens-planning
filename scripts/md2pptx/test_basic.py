#!/usr/bin/env python3
# Copyright (c) 2025 TrailLensCo
# All rights reserved.
#
# This file is proprietary and confidential.

"""Basic tests for md2pptx functionality."""

import sys
from pathlib import Path

from md2pptx import MarkdownToPptxConverter
from md2pptx.styles import StylePreset


def test_basic_conversion():
    """Test basic markdown to PPTX conversion."""
    print("Testing basic conversion...")

    # Create test markdown
    markdown = """---
title: "Test Presentation"
author: "Test Author"
date: "2026-01-19"
---

# Welcome

## Slide 1

This is a test slide.

## Slide 2

- Bullet 1
- Bullet 2
- Bullet 3
"""

    # Convert
    converter = MarkdownToPptxConverter()
    output_path = Path("test_output.pptx")

    try:
        converter.convert_string(markdown, output_path)

        if output_path.exists():
            print(f"✅ Basic conversion successful: {output_path}")
            print(f"   File size: {output_path.stat().st_size} bytes")
            output_path.unlink()  # Clean up
            return True
        else:
            print("❌ Output file not created")
            return False

    except Exception as e:
        print(f"❌ Conversion failed: {e}")
        return False


def test_background_image():
    """Test background image support."""
    print("\nTesting background image support...")

    # Create a simple test image
    try:
        from PIL import Image
        img = Image.new('RGB', (1920, 1080), color=(100, 150, 200))
        img.save('test_bg.png')
        print("✅ Test background image created")
    except Exception as e:
        print(f"❌ Could not create test image: {e}")
        return False

    # Create markdown with background
    markdown = """---
title: "Background Test"
background_image: "test_bg.png"
---

# Test

## Slide 1

Background image test
"""

    converter = MarkdownToPptxConverter()
    output_path = Path("test_bg_output.pptx")

    try:
        converter.convert_string(markdown, output_path, base_dir=Path.cwd())

        if output_path.exists():
            print(f"✅ Background image conversion successful: {output_path}")
            output_path.unlink()
            Path("test_bg.png").unlink()
            return True
        else:
            print("❌ Output file not created")
            return False

    except Exception as e:
        print(f"❌ Background conversion failed: {e}")
        return False


def test_style_presets():
    """Test style presets."""
    print("\nTesting style presets...")

    markdown = """---
title: "Style Test"
---

# Test

## Slide 1

Style preset test
"""

    success_count = 0
    for preset in [StylePreset.DEFAULT, StylePreset.SIMPLE, StylePreset.MODERN]:
        try:
            converter = MarkdownToPptxConverter(style_preset=preset)
            output_path = Path(f"test_{preset.value}.pptx")
            converter.convert_string(markdown, output_path)

            if output_path.exists():
                print(f"✅ {preset.value} style successful")
                output_path.unlink()
                success_count += 1
            else:
                print(f"❌ {preset.value} style failed")

        except Exception as e:
            print(f"❌ {preset.value} style error: {e}")

    return success_count == 3


def main():
    """Run all tests."""
    print("=" * 60)
    print("md2pptx Basic Test Suite")
    print("=" * 60)

    results = []

    # Run tests
    results.append(("Basic Conversion", test_basic_conversion()))
    results.append(("Background Image", test_background_image()))
    results.append(("Style Presets", test_style_presets()))

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
