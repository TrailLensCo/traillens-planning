# md2pptx Quick Start Guide

Convert Markdown files to PowerPoint presentations in 3 simple steps.

## Installation

### 1. Install Pandoc

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

### 2. Install md2pptx

```bash
# From the TrailLens root directory
source scripts/activate-env.sh
pip install -e scripts/
```

### 3. Verify Installation

```bash
md2pptx --version
```

## Basic Usage

### Convert a File

```bash
md2pptx presentation.md
```

This creates `presentation.pptx` in the same directory.

### Specify Output

```bash
md2pptx input.md -o output.pptx
```

## Markdown Structure

### Basic Example

```markdown
---
title: "My Presentation"
author: "Your Name"
date: "2026-01-19"
---

# Title Slide

## First Content Slide

- Point 1
- Point 2
- Point 3

## Second Slide

Content here...
```

### Add Background Image

```markdown
---
title: "My Presentation"
background_image: "images/background.jpg"
aspect_ratio: "16:9"
---

## Slide 1

Your content...
```

**Tips for background images:**
- Use 1920x1080 for 16:9 presentations
- Use 1024x768 for 4:3 presentations
- PNG and JPG formats work best
- Path can be relative or absolute

## Common Options

### Table of Contents

```bash
md2pptx presentation.md --toc
```

### Incremental Bullets

```bash
md2pptx presentation.md --incremental
```

### Custom Slide Level

```bash
# H1 creates new slides (instead of default H2)
md2pptx presentation.md --slide-level 1
```

### 4:3 Aspect Ratio

```bash
md2pptx presentation.md --aspect-ratio 4:3
```

### Style Presets

```bash
# Available: default, simple, modern, professional
md2pptx presentation.md --style professional
```

## Advanced Features

### Reference Document (Custom Branding)

Create a PowerPoint template with your company branding:

```bash
md2pptx presentation.md --reference-doc company_template.pptx
```

### Batch Conversion

Convert all markdown files in a directory:

```bash
md2pptx ./presentations/ --batch
```

### Debug Mode

```bash
md2pptx presentation.md --debug
```

## Complete Example

```bash
# Create a professional presentation with:
# - Table of contents
# - Incremental bullets
# - 16:9 aspect ratio
# - Modern style

md2pptx slides.md \
  --toc \
  --incremental \
  --aspect-ratio 16:9 \
  --style modern \
  -o final-presentation.pptx
```

## Markdown Syntax

### Slides

By default, H2 (`##`) creates new slides:

```markdown
## Slide Title

Content here
```

### Lists

```markdown
## Bulleted List

- Item 1
- Item 2
  - Sub-item A
  - Sub-item B
- Item 3

## Numbered List

1. First
2. Second
3. Third
```

### Code Blocks

````markdown
## Code Example

```python
def greet(name):
    print(f"Hello, {name}!")
```
````

### Images

```markdown
## Slide with Image

![Description](path/to/image.jpg)
```

### Tables

```markdown
## Data Table

| Column 1 | Column 2 |
|----------|----------|
| Data 1   | Data 2   |
```

## Troubleshooting

### "Pandoc is not installed"

Install pandoc using the installation instructions above.

### "Background image not found"

Check that the image path in front matter is correct:
```yaml
background_image: "path/to/image.jpg"  # Relative to markdown file
```

### Slides not breaking correctly

Adjust the slide level:
```bash
md2pptx input.md --slide-level 1  # Use H1 for slides
```

## Next Steps

- Read the full [README.md](README.md) for all features
- Explore [samples/](samples/) for examples
- Run tests with `python test_basic.py`

## Getting Help

```bash
md2pptx --help
```

For more information, see the full documentation in [README.md](README.md).
