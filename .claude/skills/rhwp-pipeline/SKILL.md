---
name: rhwp-pipeline
description: >-
  Orchestrate end-to-end HWP document workflows: generate reports, convert to
  HWP format, export as SVG/PDF, and distribute via Slack or archival.
  Integrates with existing pipeline skills (anthropic-docx, today,
  visual-explainer) to add HWP format support to the project's data pipelines.
  Use when the user asks to "HWP pipeline", "HWP 파이프라인", "generate HWP
  report", "HWP 보고서 생성", "batch HWP processing", "HWP 일괄 처리", "rhwp-pipeline",
  "HWP report workflow", or wants end-to-end HWP document processing
  integrated with existing pipelines. Do NOT use for individual conversion
  (use rhwp-converter). Do NOT use for viewing (use rhwp-viewer). Do NOT use
  for debugging (use rhwp-debug). Do NOT use for setup (use rhwp-setup).
---

# rhwp Pipeline — End-to-End HWP Document Workflows

Orchestrate HWP document workflows that integrate with the project's existing
pipeline infrastructure. Covers report generation, format conversion, and
multi-channel distribution.

## Workflow Modes

| Mode | Description | Skills Composed |
|------|-------------|----------------|
| Convert & Distribute | Convert HWP → SVG/PDF → Slack/Drive | rhwp-converter, Slack MCP, gws-drive |
| Report Enhancement | Add HWP export to existing report pipelines | anthropic-docx, rhwp-converter |
| Batch Processing | Process multiple HWP files in parallel | rhwp-converter (batch mode) |
| Archive | Convert and archive HWP documents with metadata | rhwp-converter, daily-db-sync |

## Workflow

### Step 1: Pre-flight Check

Verify rhwp CLI is available:

```bash
rhwp --help > /dev/null 2>&1 || { echo "ERROR: rhwp CLI not found. Run /rhwp-setup first."; exit 1; }
```

### Step 2: Determine Pipeline Mode

Based on the user's request, select the appropriate pipeline:

#### Mode A: Convert & Distribute

Convert HWP files and distribute outputs to Slack or Google Drive:

```bash
INPUT_FILE="<HWP_FILE>"
OUTPUT_DIR="outputs/rhwp/$(date +%Y-%m-%d)"
mkdir -p "$OUTPUT_DIR"

# Convert to SVG
rhwp export-svg "$INPUT_FILE" -o "$OUTPUT_DIR/"

# Convert first page SVG to PDF for sharing
FIRST_SVG=$(ls "$OUTPUT_DIR"/*.svg | head -1)
if command -v cairosvg &> /dev/null; then
  python3 -c "import cairosvg; cairosvg.svg2pdf(url='$FIRST_SVG', write_to='$OUTPUT_DIR/preview.pdf')"
fi
```

Then distribute via Slack MCP or Google Drive (gws-drive skill).

#### Mode B: Report Enhancement

Add HWP format support to the daily report pipeline. After `anthropic-docx`
generates a DOCX report, the HWP pipeline can:

1. Accept the DOCX output path
2. Convert to HWP if an HWP template is available (use `rhwp-web-editor`
   hwpctl API to programmatically build HWP from structured data)
3. Export preview SVGs for Slack posting
4. Archive both DOCX and HWP versions

For template-based HWP generation, use the Field API (PutFieldText) to fill
named fields in an HWP template — see `rhwp-web-editor` skill.

#### Mode C: Batch Processing

Process a directory of HWP files using `rhwp-converter`'s batch mode
(see Step 3c in rhwp-converter SKILL.md). This pipeline adds error tracking
and manifest generation on top of the converter's batch loop.

#### Mode D: Archive with Metadata

Convert and archive with a manifest for the daily pipeline:

```bash
OUTPUT_DIR="outputs/rhwp/$(date +%Y-%m-%d)"
mkdir -p "$OUTPUT_DIR"

# After conversion, create manifest
cat > "$OUTPUT_DIR/manifest.json" << EOF
{
  "date": "$(date +%Y-%m-%d)",
  "pipeline": "rhwp-pipeline",
  "files": [
    $(ls "$OUTPUT_DIR"/*.svg 2>/dev/null | while read f; do echo "\"$(basename "$f")\""; done | paste -sd, -)
  ],
  "source": "$INPUT_FILE",
  "format": "svg"
}
EOF
```

### Step 3: Post-Processing

After conversion, optionally run downstream steps:

- **Quality check**: Verify SVG output is valid and contains content
- **Slack posting**: Upload preview images to project channels
- **Knowledge base**: Index document metadata in Cognee

### Step 4: Report Results

```
## Pipeline Results

| Stage | Status | Output |
|-------|--------|--------|
| Conversion | OK | N pages exported |
| PDF generation | OK/SKIP | preview.pdf |
| Distribution | OK/SKIP | Posted to #channel |
| Archive | OK | manifest.json created |
```

## Integration Points

| Existing Skill | Integration |
|---------------|-------------|
| `today` | Add HWP export as optional Phase 6.5 |
| `anthropic-docx` | Chain DOCX → HWP conversion when templates available |
| `visual-explainer` | Embed HWP-derived SVGs in HTML explainer pages |
| `md-to-notion` | Reference HWP exports in Notion pages |
| `gws-drive` | Upload converted PDFs/HWPX to Google Drive |

### Google Drive Upload — MIME Type Warning

HWPX files are ZIP-based archives. When uploading to Google Drive via API,
**never** use `application/zip` as the MIME type — Google Drive will unpack
the archive and display individual internal files (Contents/, META-INF/, etc.)
instead of showing a single document.

| File Type | Correct MIME | Wrong MIME |
|-----------|-------------|------------|
| `.hwpx` | `application/octet-stream` | `application/zip` |
| `.hwp` | `application/octet-stream` | `application/zip` |
| `.pdf` | `application/pdf` | — |
| `.svg` | `image/svg+xml` | — |

When using `gws drive upload`, the CLI auto-detects MIME types — prefer
it over raw Google API calls to avoid this issue.

## Examples

### Single Report Conversion

User: "이 HWP 보고서를 PDF로 변환하고 슬랙에 올려줘"

→ Mode A activated: `rhwp export-svg report.hwp` → SVG → PDF via cairosvg → Slack upload via MCP → result table posted.

### Daily Pipeline Integration

User: "today 파이프라인에 HWP 출력 추가"

→ Mode B activated: Hooks into the `today` skill at Phase 6.5 → generates HWP export alongside the existing DOCX report → archives both in `outputs/rhwp/{date}/`.

### Batch Archive

User: "contracts 폴더의 HWP 파일 전부 변환해서 아카이브해"

→ Mode C (batch via rhwp-converter) + Mode D (archive with manifest) chained → `manifest.json` created with file list and metadata.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `rhwp` CLI not found | Run `/rhwp-setup` to install |
| SVG output is empty (0 bytes) | Check input file is valid HWP/HWPX via `rhwp info` |
| cairosvg PDF conversion fails | Install: `pip install cairosvg` |
| Slack upload fails | Verify Slack MCP connection and channel permissions |
| manifest.json has empty file list | Verify conversion produced SVGs in the output directory |

## Intermediate Persistence

All pipeline outputs are saved to `outputs/rhwp/{date}/` with:
- Individual SVG files per page
- Optional PDF conversions
- `manifest.json` with metadata
- Error logs for failed conversions
