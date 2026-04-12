---
name: opendataloader
description: >-
  PRIMARY PDF reader for all pipelines. Convert PDF documents to high-fidelity
  Markdown, JSON (with bounding boxes), or HTML using OpenDataLoader v2.2.1
  (Hancom, Apache 2.0). Benchmark #1 at 0.907 overall accuracy.
  Two modes: Local (60+ pages/sec, no external API, JDK only) and Hybrid
  (scanned PDFs, complex/borderless tables, LaTeX formulas, chart descriptions
  via docling AI backend with built-in OCR for 80+ languages including Korean).
  Built-in AI safety: prompt injection filtering for hidden text and off-page content.
  Fallback chain: opendataloader → anthropic-pdf → pdfplumber.
  Use when the user asks to "convert PDF to markdown", "parse PDF",
  "extract text from PDF", "opendataloader", "PDF to markdown",
  "high-fidelity PDF extraction", "OpenDataLoader", "PDF 변환",
  "PDF 마크다운 변환", "PDF 파싱", "고품질 PDF 추출", "PDF OCR",
  "스캔 PDF 변환", "PDF 수식 추출", "hybrid mode PDF",
  or when a pipeline skill needs PDF-to-Markdown conversion
  (kb-ingest, paper-review, cognee pre-processing).
  Do NOT use for PDF creation, merging, splitting, or form filling
  (use anthropic-pdf). Do NOT use for simple text-only extraction
  where layout fidelity is not needed (use pdfplumber directly).
  Do NOT use for web page extraction (use defuddle or WebFetch).
metadata:
  author: "thaki"
  version: "2.0.0"
  category: "document"
  tags: ["pdf", "markdown", "parsing", "document-processing", "ocr", "hybrid", "ai-safety"]
  priority: "primary"
---

# OpenDataLoader — PRIMARY PDF Parser (v2.2.1)

Convert PDFs to structured Markdown, JSON, or HTML using Hancom's OpenDataLoader
engine. XY-Cut++ layout analysis handles complex tables, multi-column layouts,
nested elements, LaTeX equations, charts, and embedded images.
**Benchmark #1 at 0.907 overall accuracy** (surpassing Marker 0.826, MinerU 0.863,
Docling 0.710).

> **This skill is the PRIMARY PDF reader.** All pipeline skills (kb-ingest,
> paper-review, cognee, nlm-arxiv-slides) MUST attempt OpenDataLoader first.
> Fall back to alternatives only on failure.

## Prerequisites

1. **JDK 11+** — OpenDataLoader runs a Java CLI under the hood

```bash
java -version   # must be >= 11
# macOS: brew install openjdk@11
# Ubuntu: sudo apt install openjdk-11-jdk
```

**macOS Homebrew PATH setup** (if `java -version` fails after install):

```bash
export JAVA_HOME=/opt/homebrew/opt/openjdk@11/libexec/openjdk.jdk/Contents/Home
export PATH="$JAVA_HOME/bin:$PATH"
```

Add these to `~/.zshrc` for persistence. Alternatively, create a system symlink
with `sudo ln -sfn /opt/homebrew/opt/openjdk@11/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-11.jdk`.

2. **Python package** — `opendataloader-pdf`

```bash
pip install opendataloader-pdf
```

3. **Verify installation**:

```bash
python -c "import opendataloader_pdf; print('OK')"
java -version 2>&1 | head -1
```

4. **Optional — Hybrid mode** requires network access to AI backend (no extra install)

## Fallback Chain

When OpenDataLoader is unavailable or fails, follow this chain:

```
opendataloader-pdf (PRIMARY)
  ↓ Java not found / conversion error
anthropic-pdf skill (Read tool on PDF files)
  ↓ not available / file too large
pdfplumber (simple text extraction)
```

**Decision logic:**

```python
def extract_pdf(pdf_path: str, output_dir: str) -> str:
    """Try opendataloader first, then fallbacks."""
    import os, shutil

    os.makedirs(output_dir, exist_ok=True)
    stem = os.path.splitext(os.path.basename(pdf_path))[0]

    # Attempt 1: OpenDataLoader (primary)
    try:
        import opendataloader_pdf
        opendataloader_pdf.convert(
            input_path=pdf_path,
            output_dir=output_dir,
            format="markdown",
            quiet=True,
        )
        md_path = os.path.join(output_dir, f"{stem}.md")
        if os.path.exists(md_path) and os.path.getsize(md_path) > 50:
            with open(md_path) as f:
                return f.read()
    except Exception:
        pass

    # Attempt 2: Use Cursor's Read tool on the PDF directly
    #   (handled by the calling agent — return sentinel)
    # Attempt 3: pdfplumber
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            text = "\n\n".join(page.extract_text() or "" for page in pdf.pages)
        if text.strip():
            return text
    except Exception:
        pass

    raise RuntimeError(f"All PDF extraction methods failed for {pdf_path}")
```

## Core API

```python
import opendataloader_pdf

opendataloader_pdf.convert(
    input_path="/path/to/document.pdf",   # str or List[str]
    output_dir="/tmp/odl-output",         # output directory
    format="markdown",                    # "markdown", "json", "html", "text", or comma-separated
    quiet=True,                           # suppress JVM stdout
)
```

**Key behaviors:**
- Returns `None` — output is written to disk
- Output filename: `{original_name}.md` (or `.json`, `.html`)
- Each call spawns a JVM process; batch input is more efficient
- JSON output includes bounding box coordinates per element

## Modes

### Mode 1: Local (Default) — Fast, Offline

60+ pages/sec on CPU. No external API calls. Best for well-formed digital PDFs.

```python
opendataloader_pdf.convert(
    input_path="/tmp/report.pdf",
    output_dir="/tmp/output",
    format="markdown",
    quiet=True,
)
```

### Mode 2: Hybrid — Scanned PDFs, Complex Tables, Formulas

~2 pages/sec. Uses AI backend for pages that need it. Built-in OCR for 80+ languages.

```python
opendataloader_pdf.convert(
    input_path="/tmp/scanned-doc.pdf",
    output_dir="/tmp/output",
    format="markdown",
    hybrid="docling-fast",    # or "docling-full" for maximum accuracy
    quiet=True,
)
```

**When to use Hybrid:**
- Scanned PDFs (image-only pages)
- Complex or borderless tables
- LaTeX formulas needing extraction
- Charts requiring AI description
- Documents mixing digital text with scanned pages

**Hybrid backends:**
| Backend | Speed | Accuracy | Use case |
|---------|-------|----------|----------|
| `docling-fast` | ~2 pg/s | High | Default hybrid choice |
| `docling-full` | ~0.5 pg/s | Highest | Maximum quality needed |

### Mode 3: Batch Conversion (Preferred)

Amortizes JVM startup across multiple files:

```python
opendataloader_pdf.convert(
    input_path=["paper1.pdf", "paper2.pdf", "folder/"],
    output_dir="/tmp/batch-output",
    format="markdown,json",
    quiet=True,
)
```

### Mode 4: Multi-Format Output

```python
opendataloader_pdf.convert(
    input_path="/tmp/report.pdf",
    output_dir="/tmp/multi",
    format="markdown,json,html",
    quiet=True,
)
```

### Mode 5: Sanitize Mode — AI Safety

Strip hidden text and off-page content that could be prompt injection attacks:

```python
opendataloader_pdf.convert(
    input_path="/tmp/untrusted.pdf",
    output_dir="/tmp/safe-output",
    format="markdown",
    sanitize=True,
    quiet=True,
)
```

Use sanitize mode when processing PDFs from untrusted sources before feeding
to LLMs for RAG or analysis.

### Mode 6: CLI Usage

```bash
# Local mode
opendataloader-pdf -i input.pdf -o output/ -f markdown

# Hybrid mode
opendataloader-pdf -i scanned.pdf -o output/ --hybrid docling-fast

# Batch + multi-format
opendataloader-pdf -i folder/ -o output/ -f markdown,json

# Sanitize mode
opendataloader-pdf -i untrusted.pdf -o output/ --sanitize
```

### Mode 7: LangChain Integration

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

If Java is missing, try Hybrid mode first (may still work depending on setup),
then fall back to anthropic-pdf/pdfplumber.

### Step 2: Choose Mode

| PDF Type | Mode | Command |
|----------|------|---------|
| Digital, well-formed | Local (default) | `format="markdown"` |
| Scanned / image-only | Hybrid | `hybrid="docling-fast"` |
| Complex tables | Hybrid | `hybrid="docling-fast"` |
| LaTeX formulas | Hybrid | `hybrid="docling-full"` |
| Untrusted source | Sanitize | `sanitize=True` |
| Multiple files | Batch | `input_path=[list]` |

### Step 3: Run Conversion

```python
import opendataloader_pdf
import os

output_dir = "/tmp/odl-output"
os.makedirs(output_dir, exist_ok=True)

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

```python
assert os.path.exists(md_path), f"Output not found: {md_path}"
assert os.path.getsize(md_path) > 100, "Output suspiciously small — try hybrid mode"
```

If local mode produces empty or poor output, retry with hybrid:

```python
opendataloader_pdf.convert(
    input_path=pdf_path,
    output_dir=output_dir,
    format="markdown",
    hybrid="docling-fast",
    quiet=True,
)
```

## Pipeline Integration Patterns

### kb-ingest Integration

```python
import opendataloader_pdf, os

pdf_src = "~/papers/sim-to-real.pdf"
output_dir = "/tmp/odl-output"
os.makedirs(output_dir, exist_ok=True)

opendataloader_pdf.convert(
    input_path=pdf_src,
    output_dir=output_dir,
    format="markdown",
    quiet=True,
)

stem = os.path.splitext(os.path.basename(pdf_src))[0]
md_path = os.path.join(output_dir, f"{stem}.md")
# Copy md_path to knowledge-bases/{topic}/raw/{slug}.md
```

### paper-review Integration

Replace pdfplumber in Phase 1 with automatic hybrid fallback:

```python
import opendataloader_pdf, os

pdf_path = f"/tmp/arxiv-{ID}.pdf"
output_dir = "/tmp/odl-output"
os.makedirs(output_dir, exist_ok=True)

# Try local first, fall back to hybrid for scanned papers
opendataloader_pdf.convert(
    input_path=pdf_path,
    output_dir=output_dir,
    format="markdown",
    quiet=True,
)

md_path = os.path.join(output_dir, f"arxiv-{ID}.md")
if os.path.getsize(md_path) < 100:
    opendataloader_pdf.convert(
        input_path=pdf_path,
        output_dir=output_dir,
        format="markdown",
        hybrid="docling-fast",
        quiet=True,
    )

with open(md_path) as f:
    text = f.read()
```

### cognee Pre-processing

Convert PDFs to Markdown before feeding to `cognee.add()`:

```python
import opendataloader_pdf, cognee, os

pdf_path = "/path/to/report.pdf"
output_dir = "/tmp/odl-output"
os.makedirs(output_dir, exist_ok=True)
opendataloader_pdf.convert(
    input_path=pdf_path,
    output_dir=output_dir,
    format="markdown",
    sanitize=True,    # safety for external PDFs
    quiet=True,
)

stem = os.path.splitext(os.path.basename(pdf_path))[0]
md_path = os.path.join(output_dir, f"{stem}.md")

await cognee.add(md_path, dataset_name="research")
await cognee.cognify(datasets=["research"])
```

## Output Formats

| Format | Extension | Content |
|--------|-----------|---------|
| Markdown | `.md` | Clean markdown with tables, headers, lists |
| JSON | `.json` | Structured elements with bounding boxes and coordinates |
| HTML | `.html` | Semantic HTML preserving layout |
| Text | `.txt` | Plain text extraction |
| Annotated PDF | `.pdf` | Original PDF with layout annotations overlay |

## Performance

| Mode | Speed | Accuracy | Network |
|------|-------|----------|---------|
| Local | ~60 pg/s | 0.907 | None |
| Hybrid (docling-fast) | ~2 pg/s | Higher | Required |
| Hybrid (docling-full) | ~0.5 pg/s | Highest | Required |

- **JVM cold start**: ~1-2s overhead per `convert()` call
- **Optimization**: Prefer batch `List[str]` input over repeated calls
- **No GPU required**: CPU-only processing

## Error Handling

| Error | Symptom | Action |
|-------|---------|--------|
| Java not found | `FileNotFoundError` | Install JDK 11+: `brew install openjdk@11`; set `JAVA_HOME` if needed |
| JAVA_NOT_FOUND | `java -version` fails | Set `JAVA_HOME=/opt/homebrew/opt/openjdk@11/libexec/openjdk.jdk/Contents/Home` |
| Package missing | `ModuleNotFoundError` | `pip install opendataloader-pdf` |
| Conversion fails | `subprocess.CalledProcessError` | Run with `quiet=False`; try hybrid mode |
| Empty output | `.md` file < 100 bytes | PDF may be scanned — retry with `hybrid="docling-fast"` |
| Scanned PDF | Very short text, garbled chars | Use hybrid mode with OCR |
| Permission error | Cannot write to output_dir | Ensure directory exists and is writable |

## Examples

### Example 1: Convert a single PDF

**User says:** "Convert this PDF to markdown: ~/papers/attention.pdf"

**Actions:**
1. Verify JDK and opendataloader-pdf installed
2. Convert with local mode
3. If output is poor/empty, retry with hybrid
4. Present the converted markdown

### Example 2: Process scanned Korean document

**User says:** "이 스캔 PDF를 마크다운으로 변환해줘"

**Actions:**
1. Use hybrid mode directly (scanned → OCR needed)
2. `opendataloader_pdf.convert(input_path=path, output_dir=out, format="markdown", hybrid="docling-fast", quiet=True)`
3. OCR automatically handles Korean text (80+ languages supported)

### Example 3: Safe extraction from untrusted PDF

**User says:** "이 외부 PDF를 안전하게 추출해줘"

**Actions:**
1. Use sanitize mode to strip potential prompt injection
2. `opendataloader_pdf.convert(input_path=path, output_dir=out, format="markdown", sanitize=True, quiet=True)`

### Example 4: Extract with formulas

**User says:** "수식이 있는 논문 PDF를 LaTeX 수식 포함해서 추출"

**Actions:**
1. Use hybrid mode for formula extraction
2. `opendataloader_pdf.convert(input_path=path, output_dir=out, format="markdown", hybrid="docling-full", quiet=True)`
3. Formulas are extracted as LaTeX notation in markdown

## Related Skills

- **anthropic-pdf** — PDF creation, merging, splitting, form filling (FALLBACK #2 for reading)
- **kb-ingest** — Knowledge base ingestion (uses OpenDataLoader for PDF extraction)
- **paper-review** — Academic paper review pipeline (uses OpenDataLoader in Phase 1)
- **cognee** — Knowledge graph engine (benefits from OpenDataLoader pre-processing)
- **nlm-arxiv-slides** — arXiv paper to slides pipeline (uses OpenDataLoader)
- **pandoc** — Universal document format conversion (different scope)
- **defuddle** — Web page extraction (not for PDFs)
