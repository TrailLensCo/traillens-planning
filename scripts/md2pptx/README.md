# md2pptx - Markdown to PowerPoint Converter

Convert Markdown files to PowerPoint (PPTX) presentations using Pandoc.

## Features

- **Simple Markdown to PPTX conversion** using Pandoc
- **Background images** via front matter configuration
- **Multiple aspect ratios** (16:9 and 4:3)
- **Style presets** for different presentation styles
- **Reference documents** for custom branding
- **Incremental bullets** for progressive reveal
- **Table of contents** generation
- **Batch conversion** for multiple files

## Installation

### Requirements

- Python 3.10+
- Pandoc (must be installed separately)
- python-pptx

### Install Pandoc

**macOS:**
```bash
brew install pandoc
```

**Ubuntu/Debian:**
```bash
sudo apt-get install pandoc
```

**Windows:**
Download from [pandoc.org](https://pandoc.org/installing.html)

### Install Python Package

```bash
pip install python-pptx python-frontmatter
```

## Quick Start

### Basic Usage

```bash
# Convert markdown to PPTX
md2pptx presentation.md

# Specify output name
md2pptx input.md -o slides.pptx

# Include table of contents
md2pptx input.md --toc

# Incremental bullets
md2pptx input.md --incremental
```

### Background Images

Add background image to all slides via front matter:

```markdown
---
title: "My Presentation"
author: "Your Name"
date: "2026-01-19"
background_image: "images/background.jpg"
aspect_ratio: "16:9"
---

# First Slide

Content goes here...

## Second Slide

More content...
```

### Advanced Options

```bash
# Custom slide level (H1 creates new slides)
md2pptx input.md --slide-level 1

# Use 4:3 aspect ratio
md2pptx input.md --aspect-ratio 4:3

# Use style preset
md2pptx input.md --style professional

# Use reference document for branding
md2pptx input.md --reference-doc company_template.pptx

# Batch convert directory
md2pptx ./docs/ --batch --pattern "*.md"
```

## Markdown Syntax

### Slides

By default, H2 headings (`##`) create new slides:

```markdown
## Slide Title

Content for this slide

## Next Slide

More content
```

Change slide level with `--slide-level`:

```markdown
# Top Level Slide (with --slide-level 1)

## Sub-slide

### Content under sub-slide
```

### Bullet Points

```markdown
## Slide with Bullets

- First point
- Second point
  - Sub-point
  - Another sub-point
- Third point
```

### Incremental Bullets

Use `--incremental` flag or in front matter:

```markdown
---
title: "Presentation"
incremental: true
---
```

### Images

```markdown
## Slide with Image

![Image description](path/to/image.jpg)
```

### Code Blocks

````markdown
## Code Example

```python
def hello_world():
    print("Hello, World!")
```
````

### Tables

```markdown
## Data Table

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
| Data 4   | Data 5   | Data 6   |
```

## Front Matter Options

```yaml
---
title: "Presentation Title"        # Main title
author: "Author Name"               # Author
date: "2026-01-19"                  # Date
subtitle: "Optional Subtitle"       # Subtitle
institute: "Your Organization"      # Institution
background_image: "bg.jpg"          # Path to background image
aspect_ratio: "16:9"                # "16:9" or "4:3"
theme: "default"                    # Pandoc theme (if applicable)
---
```

## Style Presets

- **default** - Standard presentation style
- **simple** - Minimal style with H1 slide breaks
- **modern** - Modern style with incremental bullets
- **professional** - Professional style with TOC

```bash
md2pptx input.md --style professional
```

## Reference Documents

Create a custom reference PPTX with your branding and use it as a template:

```bash
md2pptx input.md --reference-doc company_template.pptx
```

The reference document defines:
- Master slide layouts
- Fonts and colors
- Background designs
- Company logos

## Background Image Tips

1. **Resolution:** Use high-resolution images (1920x1080 for 16:9, 1024x768 for 4:3)
2. **Format:** PNG, JPG, or GIF supported
3. **Readability:** Ensure text is readable over the background
4. **File path:** Can be relative to markdown file or absolute

## Examples

See `samples/` directory for example markdown files and outputs.

## Troubleshooting

### Pandoc Not Found

```
RuntimeError: Pandoc is not installed or not in PATH
```

**Solution:** Install pandoc using instructions above and ensure it's in your PATH.

### Background Image Not Found

```
FileNotFoundError: Background image not found: path/to/image.jpg
```

**Solution:** Check that the image path is correct (relative to markdown file).

### Unsupported Image Format

```
ValueError: Unsupported image format: .webp
```

**Solution:** Convert image to JPG or PNG format.

## Command Reference

```
usage: md2pptx [-h] [-o OUTPUT] [--toc] [--incremental]
               [--slide-level {1,2,3,4,5,6}]
               [--aspect-ratio {16:9,4:3}]
               [--style {default,simple,modern,professional}]
               [--reference-doc REFERENCE_DOC] [--batch]
               [--pattern PATTERN] [--debug] [-v] [-q]
               input

positional arguments:
  input                 Input markdown file or directory (with --batch)

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file path (default: input with .pptx extension)
  --toc                 Include table of contents slide
  --incremental         Show bullet points incrementally
  --slide-level {1,2,3,4,5,6}
                        Heading level for new slides (default: 2)
  --aspect-ratio {16:9,4:3}
                        Presentation aspect ratio (default: 16:9)
  --style {default,simple,modern,professional}
                        Style preset to use (default: default)
  --reference-doc REFERENCE_DOC
                        Reference PPTX file for styling
  --batch               Batch convert all .md files in directory
  --pattern PATTERN     Glob pattern for batch conversion (default: *.md)
  --debug               Enable debug logging
  -v, --version         show program's version number and exit
  -q, --quiet           Suppress non-error output
```

## License

Copyright (c) 2025 TrailLensCo. All rights reserved.
This file is proprietary and confidential.

## Version

1.0.0
