## PDF

Read, create, edit, merge, split, and manipulate PDF files — extract text/tables, fill forms, add watermarks, encrypt, and OCR scanned documents.

### Usage

```
/pdf read report.pdf                   # extract text and tables
/pdf merge doc1.pdf doc2.pdf           # merge PDFs
/pdf split report.pdf --pages 1-5      # split specific pages
/pdf fill form.pdf --data input.json   # fill form fields
```

### Workflow

1. **Identify** — Determine the PDF operation needed
2. **Process** — Execute: read, create, merge, split, rotate, watermark, encrypt, OCR
3. **Validate** — Verify output integrity and content accuracy
4. **Export** — Save processed PDF to the specified location

### Execution

Read and follow the `anthropic-pdf` skill (`.cursor/skills/anthropic/anthropic-pdf/SKILL.md`) for comprehensive PDF operations. For high-fidelity PDF-to-markdown conversion, use `opendataloader` (`.cursor/skills/standalone/opendataloader/SKILL.md`) as the primary reader.

### Examples

Extract content from a PDF:
```
/pdf read quarterly-report.pdf
```

Merge multiple PDFs:
```
/pdf merge chapter1.pdf chapter2.pdf chapter3.pdf --output book.pdf
```
