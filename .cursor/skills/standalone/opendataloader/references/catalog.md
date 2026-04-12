# OpenDataLoader PDF v2.2.1 — Quick Reference

## Python API

```python
import opendataloader_pdf

opendataloader_pdf.convert(
    input_path,     # str | List[str] — file paths, glob, or directory
    output_dir,     # str — output directory (created if missing)
    format,         # str — "markdown", "json", "html", "text", comma-separated
    hybrid=None,    # str — "docling-fast" | "docling-full" | None (local)
    sanitize=False, # bool — strip hidden text / off-page prompt injection
    quiet=True,     # bool — suppress JVM stdout
)
```

Returns `None`. Output files are written to `output_dir/{stem}.{ext}`.

## CLI

```bash
opendataloader-pdf \
  -i <input>         \   # file, glob, or directory
  -o <output_dir>    \   # output directory
  -f <format>        \   # markdown, json, html, text (comma-sep)
  --hybrid <backend> \   # docling-fast | docling-full
  --sanitize              # AI safety mode
```

## LangChain

```bash
pip install langchain-opendataloader-pdf
```

```python
from langchain_opendataloader_pdf import OpenDataLoaderPDFLoader
loader = OpenDataLoaderPDFLoader("file.pdf")
docs = loader.load()
```

## Hybrid Mode Comparison

| Backend | Speed | When to use |
|---------|-------|-------------|
| None (local) | ~60 pg/s | Digital PDFs, well-formed text |
| `docling-fast` | ~2 pg/s | Scanned PDFs, complex tables, formulas |
| `docling-full` | ~0.5 pg/s | Maximum accuracy, complex charts, borderless tables |

## JSON Output Structure

JSON output includes per-element bounding boxes:

```json
{
  "elements": [
    {
      "type": "heading",
      "level": 1,
      "text": "Introduction",
      "bbox": { "x": 72, "y": 100, "w": 300, "h": 24 },
      "page": 1
    },
    {
      "type": "table",
      "rows": [...],
      "bbox": { "x": 72, "y": 200, "w": 468, "h": 150 },
      "page": 1
    }
  ]
}
```

## AI Safety — Sanitize Mode

Filters out:
- Hidden text (white-on-white, zero-size font)
- Off-page content (positioned outside visible area)
- Invisible Unicode characters
- Potential prompt injection payloads

## OCR Support (Hybrid Mode)

Built-in OCR in hybrid mode supports 80+ languages including:
Korean, English, Japanese, Chinese (Simplified/Traditional), German,
French, Spanish, Portuguese, Arabic, Hindi, Thai, Vietnamese, and more.

No additional OCR engine install needed — handled by hybrid backend.

## Benchmark (v2.2.1)

| Tool | Overall | Table | Heading | ToC | List |
|------|---------|-------|---------|-----|------|
| **OpenDataLoader** | **0.907** | 0.865 | 0.957 | 0.952 | 0.853 |
| MinerU | 0.863 | 0.788 | 0.936 | 0.965 | 0.764 |
| Marker | 0.826 | 0.750 | 0.908 | 0.916 | 0.729 |
| Docling | 0.710 | 0.545 | 0.868 | 0.815 | 0.613 |

## Prerequisites Check Script

```bash
#!/bin/bash
echo "=== OpenDataLoader Prerequisites ==="
echo -n "Java: "; java -version 2>&1 | head -1 || echo "NOT FOUND"
echo -n "Python pkg: "; python3 -c "import opendataloader_pdf; print('v' + opendataloader_pdf.__version__)" 2>/dev/null || echo "NOT FOUND"
echo -n "LangChain: "; python3 -c "import langchain_opendataloader_pdf; print('OK')" 2>/dev/null || echo "not installed (optional)"
```

## Fallback Decision Tree

```
PDF read requested
├─ opendataloader-pdf installed AND Java available?
│  ├─ YES → convert(local mode)
│  │  ├─ output > 100 bytes? → DONE
│  │  └─ output tiny? → retry with hybrid="docling-fast"
│  │     ├─ output OK? → DONE
│  │     └─ still fails? → fall to anthropic-pdf
│  └─ NO → fall to anthropic-pdf
├─ anthropic-pdf (Cursor Read tool on PDF)
│  ├─ works? → DONE
│  └─ fails? → fall to pdfplumber
└─ pdfplumber (text-only, no layout)
   ├─ works? → DONE (low fidelity)
   └─ fails? → raise error
```
