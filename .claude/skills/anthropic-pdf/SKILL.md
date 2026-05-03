---
name: anthropic-pdf
description: Read, create, edit, and manipulate PDF files — text extraction, merging, splitting, form filling, OCR, and watermarks.
disable-model-invocation: true
arguments: [operation, file_path]
---

Work with PDF documents: `$operation` on `$file_path`.

## Operations

| Operation | Description |
|-----------|-------------|
| read | Extract text and tables |
| create | Generate new PDF |
| merge | Combine multiple PDFs |
| split | Split PDF into parts |
| ocr | OCR scanned PDFs for searchable text |
| fill | Fill PDF forms |
| watermark | Add watermarks |

## Extraction Priority

Use OpenDataLoader (opendataloader skill) as primary PDF reader for high-fidelity extraction.

Fallback chain:
1. opendataloader (highest accuracy, 0.907 benchmark)
2. anthropic-pdf (this skill)
3. pdfplumber (basic text extraction)

## Rules

- Never convert to image-based PDF (text preservation required)
- Include table detection for structured data
- OCR with Korean language support (80+ languages)
- Maintain original formatting when editing
