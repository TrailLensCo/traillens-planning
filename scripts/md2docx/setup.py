# Copyright (c) 2025 TrailLensCo
# All rights reserved.
#
# This file is proprietary and confidential.

from setuptools import setup, find_packages

setup(
    name="md2docx",
    version="0.1.0",
    description="Convert Markdown files to Word (DOCX) documents",
    author="TrailLens Development Team",
    python_requires=">=3.9",
    packages=find_packages(exclude=["tests", "docs", "examples"]),
    install_requires=[
        "python-docx>=1.1.0",
        "markdown-it-py>=3.0.0",
        "mdit-py-plugins>=0.4.0",
        "python-frontmatter>=1.1.0",
        "Pygments>=2.17.0",
        "Pillow>=10.0.0",
    ],
    entry_points={
        "console_scripts": [
            "md2docx=md2docx.cli:main",
        ]
    },
    include_package_data=True,
    zip_safe=False,
)
