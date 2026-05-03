---
name: anthropic-docx
description: Create, read, edit, and manipulate Word documents (.docx) with tables of contents, formatting, images, and tracked changes.
disable-model-invocation: true
arguments: [operation, file_path]
---

Work with Word documents: `$operation` on `$file_path`.

## Operations

| Operation | Description |
|-----------|-------------|
| create | Create new .docx with structured content |
| read | Extract text and structure from existing .docx |
| edit | Modify content, formatting, or structure |
| merge | Combine multiple .docx files |
| template | Fill template with data |

## Formatting Standards

- Font: 맑은 고딕 (Malgun Gothic) for Korean documents
- Tables: generous cell padding, consistent borders
- Code blocks: monospace font + shaded background
- Mermaid diagrams: render to PNG via mmdc, then embed as images
- A4 page size with standard margins

## Rules

- Use python-docx for programmatic generation
- Apply pandoc post-processing for complex formatting
- Include table of contents for documents > 5 pages
- Preserve existing formatting when editing
- Export images at 150+ DPI
