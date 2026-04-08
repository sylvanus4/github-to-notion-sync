---
name: opendataloader
description: >-
  Convert PDF documents to high-fidelity Markdown, JSON, or HTML using the
  OpenDataLoader engine (Hancom, Apache 2.0). Supports complex layouts,
  tables, LaTeX equations, charts, and image OCR at 60+ pages/sec on CPU.
  100% local processing with no external API calls.
  Use when the user asks to "convert PDF to markdown", "parse PDF",
  "extract text from PDF", "opendataloader", "PDF to markdown",
  "high-fidelity PDF extraction", "OpenDataLoader", "PDF 변환",
  "PDF 마크다운 변환", "PDF 파싱", "고품질 PDF 추출",
  or when a pipeline skill needs PDF-to-Markdown conversion
  (kb-ingest, paper-review, cognee pre-processing).
  Do NOT use for PDF creation, merging, splitting, or form filling
  (use anthropic-pdf). Do NOT use for simple text-only extraction
  where layout fidelity is not needed (use pdfplumber directly).
  Do NOT use for web page extraction (use defuddle or WebFetch).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "document"
  tags: ["pdf", "markdown", "parsing", "document-processing"]
---

# OpenDataLoader — High-Fidelity PDF Parser

Convert PDFs to structured Markdown, JSON, or HTML using Hancom's
OpenDataLoader engine. XY-Cut++ layout analysis handles complex tables,
multi-column layouts, nested elements, LaTeX equations, charts, and
embedded images with benchmark score 0.90 (surpassing Marker and MinerU).

## Prerequisites

1. **JDK 11+** — OpenDataLoader runs a Java CLI under the hood

```bash
java -version   # must be >= 11
# macOS: brew install openjdk@11
# Ubuntu: sudo apt install openjdk-11-jdk
```

2. **Python package** — `opendataloader-pdf`

```bash
pip install opendataloader-pdf
```

3. **Verify installation**:

```bash
python -c "import opendataloader_pdf; print('OK')"
```

## Core API

The primary function is `opendataloader_pdf.convert()`:

```python
import opendataloader_pdf

opendataloader_pdf.convert(
    input_path="/path/to/document.pdf",      # str or List[str]
    output_dir="/tmp/odl-output",            # where output files are written
    format="markdown",                       # "markdown", "json", "html", or comma-separated
    quiet=True,                              # suppress JVM stdout
)
```

**Key behaviors:**
- Returns `None` — output is written to disk
- Output filename: `{original_name}.md` (or `.json`, `.html`)
- Each call spawns a JVM process via `subprocess.run(["java", "-jar", ...])`
- Batch input (`List[str]`) is more efficient than repeated single-file calls

## Modes

### Mode 1: Single File Conversion

```python
import opendataloader_pdf
import os

pdf_path = "/tmp/arxiv-2509.04664.pdf"
output_dir = "/tmp/odl-output"
os.makedirs(output_dir, exist_ok=True)

opendataloader_pdf.convert(
    input_path=pdf_path,
    output_dir=output_dir,
    format="markdown",
    quiet=True,
)

md_path = os.path.join(output_dir, "arxiv-2509.04664.md")
with open(md_path, "r") as f:
    text = f.read()
```

### Mode 2: Batch Conversion (Preferred)

Batch mode amortizes the JVM startup cost across multiple files:

```python
import opendataloader_pdf

pdf_files = [
    "/tmp/paper1.pdf",
    "/tmp/paper2.pdf",
    "/tmp/paper3.pdf",
]

opendataloader_pdf.convert(
    input_path=pdf_files,
    output_dir="/tmp/odl-batch-output",
    format="markdown",
    quiet=True,
)
```

### Mode 3: Multi-Format Output

Generate Markdown and JSON simultaneously:

```python
opendataloader_pdf.convert(
    input_path="/tmp/report.pdf",
    output_dir="/tmp/odl-multi",
    format="markdown,json",
    quiet=True,
)
```

### Mode 4: LangChain Integration

For RAG pipelines using LangChain:

```python
from langchain_opendataloader_pdf import OpenDataLoaderPDFLoader

loader = OpenDataLoaderPDFLoader("/path/to/document.pdf")
docs = loader.load()
```

Requires: `pip install langchain-opendataloader-pdf`

## Workflow

### Step 1: Verify Prerequisites

```bash
java -version 2>&1 | head -1
python -c "import opendataloader_pdf; print('OK')"
```

If Java is missing, report and stop. If `opendataloader_pdf` is missing,
suggest `pip install opendataloader-pdf`.

### Step 2: Prepare Output Directory

```bash
mkdir -p /tmp/odl-output
```

### Step 3: Run Conversion

```python
import opendataloader_pdf
import os

opendataloader_pdf.convert(
    input_path=pdf_path,
    output_dir=output_dir,
    format="markdown",
    quiet=True,
)
```

### Step 4: Read and Use Output

```python
stem = os.path.splitext(os.path.basename(pdf_path))[0]
md_path = os.path.join(output_dir, f"{stem}.md")

with open(md_path, "r") as f:
    markdown_text = f.read()
```

### Step 5: Verify Output Quality

Check that the output is non-empty and contains expected content:

```python
assert os.path.exists(md_path), f"Output not found: {md_path}"
assert os.path.getsize(md_path) > 100, "Output suspiciously small"
```

## Pipeline Integration Patterns

### kb-ingest Integration

When ingesting local PDFs into a Knowledge Base:

```python
import opendataloader_pdf, os

pdf_src = "~/papers/sim-to-real.pdf"
output_dir = "/tmp/odl-output"
os.makedirs(output_dir, exist_ok=True)

opendataloader_pdf.convert(input_path=pdf_src, output_dir=output_dir, format="markdown", quiet=True)

stem = os.path.splitext(os.path.basename(pdf_src))[0]
md_path = os.path.join(output_dir, f"{stem}.md")
# Copy md_path to knowledge-bases/{topic}/raw/{slug}.md
```

**Fallback**: If OpenDataLoader fails (Java not found, conversion error),
fall back to `anthropic-pdf` skill for text extraction.

### paper-review Integration

Replace pdfplumber full-text extraction in Phase 1:

```python
import opendataloader_pdf, os

pdf_path = f"/tmp/arxiv-{ID}.pdf"
output_dir = "/tmp/odl-output"
os.makedirs(output_dir, exist_ok=True)

opendataloader_pdf.convert(input_path=pdf_path, output_dir=output_dir, format="markdown", quiet=True)

md_path = os.path.join(output_dir, f"arxiv-{ID}.md")
with open(md_path) as f:
    text = f.read()
with open(f"/tmp/arxiv-{ID}-extracted.md", "w") as f:
    f.write(text)
```

**Fallback**: If OpenDataLoader is unavailable, fall back to pdfplumber:

```python
import pdfplumber
with pdfplumber.open(pdf_path) as pdf:
    text = "\n\n".join(page.extract_text() or "" for page in pdf.pages)
```

### cognee Pre-processing

Convert PDFs to Markdown before feeding to `cognee.add()` for higher
quality knowledge graph extraction:

```python
import opendataloader_pdf, cognee, os

pdf_path = "/path/to/report.pdf"
output_dir = "/tmp/odl-output"
os.makedirs(output_dir, exist_ok=True)
opendataloader_pdf.convert(input_path=pdf_path, output_dir=output_dir, format="markdown", quiet=True)

stem = os.path.splitext(os.path.basename(pdf_path))[0]
md_path = os.path.join(output_dir, f"{stem}.md")

await cognee.add(md_path, dataset_name="research")
await cognee.cognify(datasets=["research"])
```

## Performance Notes

- **Standard mode**: ~20 pages/sec on modern CPU
- **Batch parallelism**: 60-100+ pages/sec with multiple files
- **JVM cold start**: Each `convert()` call spawns a new JVM process (~1-2s overhead)
- **Optimization**: Prefer batch `List[str]` input over repeated single-file calls
- **No GPU required**: CPU-only processing; suitable for CPU-first Phase 0 environments

## Error Handling

| Error | Symptom | Action |
|-------|---------|--------|
| Java not found | `FileNotFoundError` from subprocess | Install JDK 11+: `brew install openjdk@11` |
| Package not installed | `ModuleNotFoundError: opendataloader_pdf` | `pip install opendataloader-pdf` |
| Conversion fails | `subprocess.CalledProcessError` | Check PDF is valid; try with `quiet=False` to see Java error output |
| Empty output | Output `.md` file is 0 bytes | PDF may be image-only (scanned); try with OCR-enabled mode or fall back to pytesseract |
| Permission error | Cannot write to output_dir | Ensure output directory exists and is writable |

## Examples

### Example 1: Convert a single PDF

**User says:** "Convert this PDF to markdown: ~/papers/attention.pdf"

**Actions:**
1. Verify JDK and opendataloader-pdf installed
2. Run `opendataloader_pdf.convert(input_path="~/papers/attention.pdf", output_dir="/tmp/odl-output", format="markdown", quiet=True)`
3. Read `/tmp/odl-output/attention.md`
4. Present the converted markdown

### Example 2: Batch convert for KB ingestion

**User says:** "Convert all PDFs in ~/papers/ to markdown for the AI KB"

**Actions:**
1. Glob `~/papers/*.pdf` to get file list
2. Run batch conversion with `input_path=file_list`
3. Copy each `.md` output to `knowledge-bases/ai/raw/`
4. Update manifest.json

### Example 3: Pre-process for Cognee

**User says:** "Index this PDF into the knowledge graph"

**Actions:**
1. Convert PDF to Markdown via OpenDataLoader
2. Feed the Markdown file to `cognee.add()`
3. Run `cognee.cognify()`

## Related Skills

- **anthropic-pdf** — PDF creation, merging, splitting, form filling (complementary, not competing)
- **kb-ingest** — Knowledge base ingestion (uses OpenDataLoader for PDF extraction)
- **paper-review** — Academic paper review pipeline (uses OpenDataLoader in Phase 1)
- **cognee** — Knowledge graph engine (benefits from OpenDataLoader pre-processing)
- **pandoc** — Universal document format conversion (different scope: format conversion vs PDF parsing)
