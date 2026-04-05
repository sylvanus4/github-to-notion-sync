---
name: rhwp-converter
description: >-
  Convert HWP/HWPX documents to SVG, PDF, or other formats using the rhwp CLI.
  Supports single-file, page-specific, and batch conversion modes. Designed for
  pipeline integration — output files can feed into Slack posts, report
  generation, or archival workflows. Use when the user asks to "convert HWP",
  "HWP to SVG", "HWP to PDF", "export HWP", "HWP 변환", "HWP를 SVG로",
  "HWP 내보내기", "rhwp-converter", "batch convert HWP", or needs HWP documents
  converted for downstream consumption. Do NOT use for viewing or inspecting
  HWP documents (use rhwp-viewer). Do NOT use for debugging HWP structure (use
  rhwp-debug). Do NOT use for installing rhwp (use rhwp-setup).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "execution"
---
# rhwp Converter — HWP/HWPX Document Format Conversion

Convert HWP/HWPX documents to SVG or PDF using the rhwp CLI. Supports
single-file conversion, page-specific export, and batch processing for
pipeline integration. The renderer handles paragraphs, tables (with cell
merging and formulas), multi-column layout, equations, numbering/bullets,
vertical text, header/footer, master pages, and inline object placement.

## Input

- One or more HWP/HWPX file paths
- Target format: `svg` (default) or `pdf`
- Optional: specific page numbers, output directory

## Workflow

### Step 1: Verify CLI

```bash
rhwp --help > /dev/null 2>&1 || { echo "ERROR: rhwp CLI not found. Run /rhwp-setup first."; exit 1; }
```

### Step 2: Determine Conversion Mode

| Mode | Input | Command |
|------|-------|---------|
| Single file, all pages | One HWP file | `rhwp export-svg file.hwp -o out/` |
| Single file, one page | One HWP + page number | `rhwp export-svg file.hwp -p N -o out/` |
| Batch (multiple files) | Glob or file list | Loop over files |
| PDF export | One HWP file | `rhwp export-pdf` (experimental) or SVG → PDF |

### Step 3a: Single File Conversion (SVG)

```bash
INPUT_FILE="<FILE_PATH>"
OUTPUT_DIR="outputs/rhwp/$(date +%Y-%m-%d)"
mkdir -p "$OUTPUT_DIR"

rhwp export-svg "$INPUT_FILE" -o "$OUTPUT_DIR/"
echo "SVG output: $OUTPUT_DIR/"
ls "$OUTPUT_DIR/"
```

### Step 3b: Page-Specific Export

```bash
# Export only page 0 (first page)
rhwp export-svg "$INPUT_FILE" -p 0 -o "$OUTPUT_DIR/"
```

### Step 3c: Batch Conversion

```bash
INPUT_DIR="<DIRECTORY_WITH_HWP_FILES>"
OUTPUT_DIR="outputs/rhwp/batch-$(date +%Y-%m-%d)"
mkdir -p "$OUTPUT_DIR"

for f in "$INPUT_DIR"/*.hwp "$INPUT_DIR"/*.hwpx; do
  [ -f "$f" ] || continue
  BASENAME=$(basename "$f" | sed 's/\.[^.]*$//')
  SUB_DIR="$OUTPUT_DIR/$BASENAME"
  mkdir -p "$SUB_DIR"
  rhwp export-svg "$f" -o "$SUB_DIR/"
  echo "Converted: $f -> $SUB_DIR/"
done

echo "Batch conversion complete. Output: $OUTPUT_DIR/"
```

### Step 3d: PDF Conversion

Option A — Native PDF export (experimental, may not cover all features):

```bash
rhwp export-pdf "$INPUT_FILE" -o "$OUTPUT_DIR/"
```

Option B — SVG to PDF via secondary tool (more reliable):

```bash
# Using rsvg-convert (librsvg)
for svg in "$OUTPUT_DIR"/*.svg; do
  PDF_OUT="${svg%.svg}.pdf"
  rsvg-convert -f pdf -o "$PDF_OUT" "$svg"
done

# Or using Inkscape
for svg in "$OUTPUT_DIR"/*.svg; do
  PDF_OUT="${svg%.svg}.pdf"
  inkscape "$svg" --export-type=pdf --export-filename="$PDF_OUT"
done

# Or using cairosvg (Python)
pip install cairosvg 2>/dev/null
python3 -c "
import cairosvg, glob, os
for svg in glob.glob('$OUTPUT_DIR/*.svg'):
    pdf = svg.replace('.svg', '.pdf')
    cairosvg.svg2pdf(url=svg, write_to=pdf)
    print(f'Converted: {svg} -> {pdf}')
"
```

### Step 4: Verify Output

```bash
echo "=== Conversion Results ==="
echo "Output directory: $OUTPUT_DIR"
echo "Files:"
ls -la "$OUTPUT_DIR/"
echo "Total: $(ls "$OUTPUT_DIR/" | wc -l) files"
```

### Step 5: Pipeline Integration (Optional)

After conversion, outputs can feed into existing pipelines:

- **Slack**: Upload SVG/PDF to Slack channels via MCP
- **Reports**: Embed SVG in HTML reports via `visual-explainer`
- **Archival**: Copy to `outputs/` directory for daily pipeline tracking

## Examples

### Quick SVG Export

User: "이 HWP 파일 SVG로 변환해줘"

```bash
rhwp export-svg report.hwpx -o ./output/
# → output/page-001.svg, output/page-002.svg, ...
```

### PDF via cairosvg

```bash
rhwp export-svg doc.hwp -o /tmp/svg/
python3 -c "import cairosvg; cairosvg.svg2pdf(url='/tmp/svg/page-001.svg', write_to='doc.pdf')"
```

### Batch Conversion

```bash
for f in contracts/*.hwpx; do
  BASENAME=$(basename "$f" .hwpx)
  rhwp export-svg "$f" -o "output/$BASENAME/"
done
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `rhwp` CLI not found | Run `/rhwp-setup` to install |
| SVG pages missing text | Verify fonts are installed; use `--embed-fonts` if available |
| cairosvg import error | `pip install cairosvg` |
| inkscape CLI not found | `brew install inkscape` (macOS) or `apt install inkscape` |
| rsvg-convert not found | `brew install librsvg` (macOS) or `apt install librsvg2-bin` |

## Output

Report conversion results:

| Input File | Pages | Output Format | Output Path |
|-----------|-------|---------------|-------------|
| `file.hwp` | 5 | SVG | `outputs/rhwp/...` |

## Intermediate Persistence

Per `pipeline-skill-intermediate-persistence.mdc`, conversion outputs are saved
to `outputs/rhwp/{date}/` with manifest metadata for resumability and debugging.
