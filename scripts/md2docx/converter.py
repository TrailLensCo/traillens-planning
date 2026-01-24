# Copyright (c) 2025 TrailLensCo
# All rights reserved.
#
# This file is proprietary and confidential.

"""Main conversion orchestration for markdown to DOCX."""

import logging
from pathlib import Path
from typing import Optional

from md2docx.diagrams.cache import DiagramCache
from md2docx.diagrams.detector import DiagramDetector, DiagramType
from md2docx.diagrams.ditaa import DitaaRenderer
from md2docx.diagrams.mermaid import MermaidRenderer
from md2docx.diagrams.plantuml import PlantUMLRenderer
from md2docx.document import DocumentBuilder
from md2docx.elements.blocks import BlockHandler, FootnoteHandler
from md2docx.elements.code import CodeHandler
from md2docx.elements.lists import DefinitionListHandler, ListHandler
from md2docx.elements.media import MediaHandler
from md2docx.elements.tables import TableHandler
from md2docx.elements.text import TextHandler
from md2docx.parser import (
    DocumentMetadata,
    MarkdownParser,
    ParsedToken,
    extract_text_content,
    get_image_info,
    get_link_info,
)
from md2docx.styles import DocumentStyle, StylePreset, get_style_preset
from md2docx.utils import TempFileManager, setup_logging

logger = logging.getLogger(__name__)


class MarkdownToDocxConverter:
    """Converts Markdown files to Word (DOCX) documents."""

    def __init__(
        self,
        style: Optional[DocumentStyle] = None,
        style_preset: Optional[StylePreset] = None,
        enable_diagrams: bool = True,
        include_toc: bool = False,
        include_title_page: bool = True,
        debug: bool = False,
    ):
        """
        Initialize the converter.

        Args:
            style: Custom document style. Uses default if None.
            style_preset: Style preset to use (ignored if style provided).
            enable_diagrams: Enable diagram rendering.
            include_toc: Include table of contents.
            include_title_page: Include title page if metadata present.
            debug: Enable debug logging.
        """
        if debug:
            setup_logging(debug=True)

        # Set up style
        if style:
            self.style = style
        elif style_preset:
            self.style = get_style_preset(style_preset)
        else:
            self.style = DocumentStyle()

        self.enable_diagrams = enable_diagrams
        self.include_toc = include_toc
        self.include_title_page = include_title_page

        # Initialize components
        self.parser = MarkdownParser()
        self.temp_manager = TempFileManager()
        self.diagram_cache = DiagramCache() if enable_diagrams else None
        self.diagram_detector = DiagramDetector() if enable_diagrams else None

        # Diagram renderers (lazy initialized)
        self._mermaid_renderer: Optional[MermaidRenderer] = None
        self._plantuml_renderer: Optional[PlantUMLRenderer] = None
        self._ditaa_renderer: Optional[DitaaRenderer] = None

        logger.debug("Converter initialized")

    def convert(
        self,
        input_path: Path,
        output_path: Optional[Path] = None,
    ) -> Path:
        """
        Convert a markdown file to DOCX.

        Args:
            input_path: Path to the markdown file.
            output_path: Output path. Defaults to input with .docx extension.

        Returns:
            Path to the generated DOCX file.
        """
        input_path = Path(input_path)

        if output_path is None:
            output_path = input_path.with_suffix(".docx")
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
        Convert markdown string to DOCX.

        Args:
            markdown_content: Markdown content string.
            output_path: Output file path.
            base_dir: Base directory for resolving relative paths.

        Returns:
            Path to the generated DOCX file.
        """
        try:
            # Parse markdown
            metadata, tokens = self.parser.parse(markdown_content)

            # Build document
            builder = DocumentBuilder(self.style)
            document = builder.get_document()

            # Initialize handlers
            text_handler = TextHandler(document, self.style)
            list_handler = ListHandler(document, self.style)
            table_handler = TableHandler(document, self.style)
            code_handler = CodeHandler(document, self.style)
            media_handler = MediaHandler(
                document, self.style, base_dir, self.temp_manager
            )
            block_handler = BlockHandler(document, self.style)
            footnote_handler = FootnoteHandler(document, self.style)

            # Add title page if requested and metadata present
            if self.include_title_page and metadata.title:
                builder.add_title_page(metadata)

            # Add table of contents if requested
            if self.include_toc:
                builder.add_table_of_contents()

            # Set up headers and footers
            builder.setup_headers_footers(
                title=metadata.title,
                date=metadata.date,
            )

            # Process tokens
            self._process_tokens(
                tokens,
                text_handler,
                list_handler,
                table_handler,
                code_handler,
                media_handler,
                block_handler,
                footnote_handler,
                base_dir,
            )

            # Add footnotes section if any
            footnote_handler.add_footnotes_section()

            # Save document
            builder.save(output_path)

            return output_path

        finally:
            # Clean up temp files
            self.temp_manager.cleanup()

    def _process_tokens(
        self,
        tokens: list[ParsedToken],
        text_handler: TextHandler,
        list_handler: ListHandler,
        table_handler: TableHandler,
        code_handler: CodeHandler,
        media_handler: MediaHandler,
        block_handler: BlockHandler,
        footnote_handler: FootnoteHandler,
        base_dir: Optional[Path],
    ) -> None:
        """
        Process markdown tokens and generate document elements.

        Args:
            tokens: List of parsed tokens.
            text_handler: Text element handler.
            list_handler: List element handler.
            table_handler: Table element handler.
            code_handler: Code element handler.
            media_handler: Media element handler.
            block_handler: Block element handler.
            footnote_handler: Footnote handler.
            base_dir: Base directory for relative paths.
        """
        i = 0
        table_rows = []
        table_alignments = []
        in_table = False

        while i < len(tokens):
            token = tokens[i]

            # Headings
            if token.type == "heading_open":
                level = int(token.tag[1])  # h1 -> 1, h2 -> 2, etc.
                # Get inline content from next token
                if i + 1 < len(tokens) and tokens[i + 1].type == "inline":
                    inline_token = tokens[i + 1]
                    text_handler.add_heading(
                        level, inline_token.children or [inline_token]
                    )
                    i += 2  # Skip inline token
                i += 1  # Skip heading_close
                continue

            # Paragraphs
            elif token.type == "paragraph_open":
                # Check if we're in a list or blockquote
                if list_handler.in_list:
                    # List item paragraph handled by list handler
                    pass
                elif block_handler.in_blockquote:
                    # Get inline content
                    if i + 1 < len(tokens) and tokens[i + 1].type == "inline":
                        inline_token = tokens[i + 1]
                        block_handler.add_blockquote_paragraph(
                            inline_token.children or [inline_token],
                            text_handler,
                        )
                        i += 2
                else:
                    # Regular paragraph
                    if i + 1 < len(tokens) and tokens[i + 1].type == "inline":
                        inline_token = tokens[i + 1]
                        self._process_paragraph(
                            inline_token,
                            text_handler,
                            media_handler,
                            footnote_handler,
                        )
                        i += 2
                i += 1  # Skip paragraph_close
                continue

            # Lists
            elif token.type == "bullet_list_open":
                list_handler.start_list(ordered=False)
                i += 1
                continue

            elif token.type == "bullet_list_close":
                list_handler.end_list()
                i += 1
                continue

            elif token.type == "ordered_list_open":
                list_handler.start_list(ordered=True)
                i += 1
                continue

            elif token.type == "ordered_list_close":
                list_handler.end_list()
                i += 1
                continue

            elif token.type == "list_item_open":
                # Collect list item content
                item_tokens = []
                i += 1
                while i < len(tokens) and tokens[i].type != "list_item_close":
                    if tokens[i].type == "inline":
                        item_tokens.append(tokens[i])
                    elif tokens[i].type in ("paragraph_open", "paragraph_close"):
                        pass
                    else:
                        item_tokens.append(tokens[i])
                    i += 1

                # Check for task list item
                is_task = token.meta.get("class") == "task-list-item" if token.meta else False
                checked = False
                if is_task and item_tokens:
                    # Extract checkbox state from content
                    content_text = extract_text_content(item_tokens)
                    if content_text.strip().startswith("[x]") or content_text.strip().startswith("[X]"):
                        checked = True

                list_handler.add_list_item(
                    item_tokens,
                    text_handler,
                    is_task=is_task,
                    checked=checked,
                )
                i += 1  # Skip list_item_close
                continue

            # Code blocks
            elif token.type == "fence" or token.type == "code_block":
                language = self.parser.get_language(token)
                content = token.content

                # Check if this is a diagram
                if (
                    self.enable_diagrams
                    and self.diagram_detector
                    and self.diagram_detector.is_diagram(token.info)
                ):
                    image_path = self._render_diagram(content, token.info)
                    if image_path:
                        media_handler.add_diagram_image(
                            image_path,
                            caption=f"{language.title()} Diagram",
                        )
                    else:
                        # Fallback to code block
                        code_handler.add_code_block(
                            content, language, highlight_syntax=False
                        )
                        logger.warning(f"Diagram rendering failed, showing as code")
                else:
                    code_handler.add_code_block(content, language)

                i += 1
                continue

            # Blockquotes
            elif token.type == "blockquote_open":
                block_handler.start_blockquote()
                i += 1
                continue

            elif token.type == "blockquote_close":
                block_handler.end_blockquote()
                i += 1
                continue

            # Horizontal rules
            elif token.type == "hr":
                block_handler.add_horizontal_rule()
                i += 1
                continue

            # Tables
            elif token.type == "table_open":
                in_table = True
                table_rows = []
                table_alignments = []
                table_handler.start_table()
                i += 1
                continue

            elif token.type == "table_close":
                in_table = False
                table_handler.end_table()
                i += 1
                continue

            elif token.type == "thead_open":
                table_handler.start_header()
                i += 1
                continue

            elif token.type == "thead_close":
                table_handler.end_header()
                i += 1
                continue

            elif token.type == "tbody_open" or token.type == "tbody_close":
                i += 1
                continue

            elif token.type == "tr_open":
                # Start collecting row cells
                i += 1
                continue

            elif token.type == "tr_close":
                i += 1
                continue

            elif token.type == "th_open" or token.type == "td_open":
                # Get alignment from style attribute
                style = token.attrs.get("style", "")
                if "text-align:center" in style:
                    alignment = "center"
                elif "text-align:right" in style:
                    alignment = "right"
                else:
                    alignment = "left"

                if len(table_alignments) < 20:  # Reasonable limit
                    if token.type == "th_open":
                        table_alignments.append(alignment)

                # Get cell content
                cell_content = []
                i += 1
                while i < len(tokens) and tokens[i].type not in ("th_close", "td_close"):
                    cell_content.append(tokens[i])
                    i += 1

                # Build row if this is a new cell
                if not table_rows or len(table_rows[-1]) >= len(table_alignments):
                    table_rows.append([])
                table_rows[-1].append(cell_content)

                # If row is complete, add it
                if (
                    table_alignments
                    and len(table_rows[-1]) == len(table_alignments)
                ):
                    table_handler.set_alignments(table_alignments)
                    table_handler.add_row(table_rows[-1], text_handler)
                    table_rows[-1] = []

                i += 1
                continue

            # Footnotes
            elif token.type == "footnote_ref":
                # Footnote reference in text
                # This will be handled when processing inline content
                i += 1
                continue

            elif token.type == "footnote_open":
                # Footnote definition
                ref = token.meta.get("id", "") if token.meta else ""
                content_tokens = []
                i += 1
                while i < len(tokens) and tokens[i].type != "footnote_close":
                    content_tokens.append(tokens[i])
                    i += 1
                content = extract_text_content(content_tokens)
                footnote_handler.register_footnote(ref, content)
                i += 1
                continue

            # Skip unknown tokens
            else:
                logger.debug(f"Skipping unknown token type: {token.type}")
                i += 1

    def _process_paragraph(
        self,
        inline_token: ParsedToken,
        text_handler: TextHandler,
        media_handler: MediaHandler,
        footnote_handler: FootnoteHandler,
    ) -> None:
        """
        Process a paragraph with its inline content.

        Args:
            inline_token: The inline token containing paragraph content.
            text_handler: Text element handler.
            media_handler: Media element handler.
            footnote_handler: Footnote handler.
        """
        children = inline_token.children or [inline_token]

        # Check for standalone images
        if len(children) == 1 and children[0].type == "image":
            img_token = children[0]
            src, alt, title = get_image_info(img_token)
            media_handler.add_image(src, alt, title)
            return

        # Check for images mixed with text
        has_image = any(c.type == "image" for c in children)
        if has_image:
            # Process tokens, extracting images
            current_text_tokens = []
            for child in children:
                if child.type == "image":
                    # Add accumulated text first
                    if current_text_tokens:
                        text_handler.add_paragraph(current_text_tokens)
                        current_text_tokens = []
                    # Add image
                    src, alt, title = get_image_info(child)
                    media_handler.add_image(src, alt, title)
                else:
                    current_text_tokens.append(child)

            # Add remaining text
            if current_text_tokens:
                text_handler.add_paragraph(current_text_tokens)
        else:
            # Regular paragraph
            text_handler.add_paragraph(children)

    def _render_diagram(
        self, content: str, fence_info: str
    ) -> Optional[Path]:
        """
        Render a diagram to an image.

        Args:
            content: Diagram source code.
            fence_info: Fence info string (diagram type).

        Returns:
            Path to rendered image, or None if failed.
        """
        if not self.diagram_detector:
            return None

        diagram_type = self.diagram_detector.detect(fence_info, content)

        # Check cache
        if self.diagram_cache:
            cached = self.diagram_cache.get(content, diagram_type.value)
            if cached:
                return cached

        # Render based on type
        image_path = None

        if diagram_type == DiagramType.MERMAID:
            if self._mermaid_renderer is None:
                self._mermaid_renderer = MermaidRenderer(self.temp_manager)
            image_path = self._mermaid_renderer.render(content)

        elif diagram_type == DiagramType.PLANTUML:
            if self._plantuml_renderer is None:
                self._plantuml_renderer = PlantUMLRenderer(self.temp_manager)
            image_path = self._plantuml_renderer.render(content)

        elif diagram_type in (DiagramType.DITAA, DiagramType.ASCII):
            if self._ditaa_renderer is None:
                self._ditaa_renderer = DitaaRenderer(self.temp_manager)
            image_path = self._ditaa_renderer.render(content)

        # Cache result
        if image_path and self.diagram_cache:
            image_path = self.diagram_cache.put(
                content, diagram_type.value, image_path
            )

        return image_path

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
            List of paths to generated DOCX files.
        """
        input_dir = Path(input_dir)
        output_dir = Path(output_dir) if output_dir else input_dir

        output_dir.mkdir(parents=True, exist_ok=True)

        output_files = []
        for md_file in input_dir.glob(pattern):
            output_path = output_dir / md_file.with_suffix(".docx").name
            try:
                self.convert(md_file, output_path)
                output_files.append(output_path)
            except Exception as e:
                logger.error(f"Failed to convert {md_file}: {e}")

        logger.info(f"Batch converted {len(output_files)} files")
        return output_files
