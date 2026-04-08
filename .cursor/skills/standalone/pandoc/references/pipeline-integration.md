# Pandoc Pipeline Integration

How the Pandoc skill chains with existing project pipelines and skills.

---

## Integration Points

### 1. `today` Pipeline

The daily stock analysis pipeline produces markdown reports in
`outputs/today/{date}/analysis.md`. Pandoc converts these to distributable
formats.

**Where it fits:** After Phase 6 (report generation), before Slack distribution.

```
today Phase 6 (analysis.md)
  └─> pandoc: gfm -> docx (with thaki-report.docx template)
  └─> pandoc: gfm -> pdf  (Korean PDF via xelatex)
  └─> upload to Google Drive (gws-drive)
  └─> post link to Slack #h-report
```

**Example command:**

```bash
DATE=$(date +%Y-%m-%d)
pandoc "outputs/today/${DATE}/analysis.md" \
  -f gfm \
  --defaults=.cursor/skills/standalone/pandoc/defaults/financial-report.yaml \
  -o "outputs/today/${DATE}/analysis.docx"
```

**Relationship with anthropic-docx:** The `today` pipeline currently uses
`anthropic-docx` for programmatic DOCX generation with python-docx. Pandoc
is the alternative when:
- The source is already clean markdown (no programmatic table/style manipulation)
- Multi-format output is needed (DOCX + PDF + HTML from one source)
- Reference-doc templating is sufficient (no cell-level formatting)

Both can coexist: `anthropic-docx` for complex programmatic documents,
Pandoc for template-based conversion from markdown.

---

### 2. `paper-review` Pipeline

The paper review pipeline ingests arXiv papers and produces structured Korean
review documents. Pandoc helps at two points:

**Ingestion (LaTeX -> Markdown):**

```
arXiv paper (.tex or .pdf)
  └─> pandoc: latex -> gfm (extract text from .tex source)
  └─> paper-review skill (analysis)
  └─> review.md output
```

```bash
pandoc paper.tex -t gfm -o extracted.md --wrap=none
```

**Output conversion (Markdown -> multiple formats):**

```
paper-review output (review.md)
  └─> pandoc: gfm -> docx (for distribution)
  └─> pandoc: gfm -> pdf  (for archival)
  └─> nlm-arxiv-slides (for presentation)
  └─> md-to-notion (for Notion publishing)
```

**Note:** For PDF papers, Pandoc cannot read PDF directly. Use `anthropic-pdf`
to extract text first, then pass to Pandoc if format conversion is needed.

---

### 3. `meeting-digest` Pipeline

Meeting digests produce Korean analysis documents from meeting transcripts.
Pandoc converts the output for different distribution channels.

**Integration flow:**

```
meeting source (Notion page / transcript / file)
  └─> meeting-digest skill (PM analysis)
  └─> digest.md + action-items.md
  └─> pandoc: gfm -> docx (email-ready attachment)
  └─> pandoc: gfm -> html (inline email body)
  └─> md-to-notion (Notion sub-pages)
  └─> Slack post
```

**HTML for email embedding:**

```bash
pandoc digest.md -f gfm -t html --wrap=none
```

The HTML output can be pasted into email bodies or Slack Canvas content
without needing a file attachment.

---

### 4. `md-to-notion` Pipeline

Pandoc and `md-to-notion` are complementary, not competing:

| Task | Tool |
|------|------|
| Markdown -> Notion page | `md-to-notion` (native Notion API) |
| Markdown -> DOCX/PDF/HTML | Pandoc |
| DOCX -> Markdown -> Notion | Pandoc (step 1) + `md-to-notion` (step 2) |
| HTML -> Markdown -> Notion | Pandoc (step 1) + `md-to-notion` (step 2) |

**Reverse conversion pipeline (DOCX -> Notion):**

```
incoming.docx
  └─> pandoc: docx -> gfm (with --extract-media=media/)
  └─> md-to-notion (publish to Notion parent page)
```

```bash
pandoc incoming.docx -t gfm -o extracted.md \
  --extract-media=media/ --wrap=none

# Then invoke md-to-notion on extracted.md
```

---

### 5. `bespin-news-digest` Pipeline

News digests extract articles and produce analysis documents. Pandoc can
convert intermediate HTML content to clean markdown for LLM processing.

**Integration flow:**

```
Gmail news email
  └─> extract article URLs
  └─> defuddle / WebFetch (HTML content)
  └─> pandoc: html -> gfm (clean markdown, optional)
  └─> x-to-slack analysis per article
  └─> pandoc: gfm -> docx (consolidated DOCX report)
  └─> gws-drive upload
```

**When to use Pandoc vs defuddle for HTML -> Markdown:**
- `defuddle`: Best for noisy web pages (strips ads, navigation, UI chrome)
- `pandoc`: Best for clean HTML (preserves table structure, footnotes, math)

---

### 6. `hf-trending-intelligence` Pipeline

HuggingFace trending reports can be converted for different audiences.

```
phase5-report.md
  └─> pandoc: gfm -> docx (stakeholder distribution)
  └─> pandoc: gfm -> pptx (presentation slides, --slide-level=2)
  └─> md-to-notion (Notion archive)
```

---

### 7. `google-daily` Pipeline

The Google Workspace daily automation generates DOCX outputs. Pandoc enables
bidirectional flow:

```
gmail-daily-triage output (.docx)
  └─> pandoc: docx -> gfm (for LLM re-analysis or KB ingest)
  └─> kb-ingest (knowledge base)

calendar-daily-briefing output (.md)
  └─> pandoc: gfm -> docx (formal briefing document)
  └─> gws-drive upload
```

---

### 8. Knowledge Base (`kb-*`) Pipeline

Pandoc converts various source formats to clean markdown for KB ingestion:

```
raw source (HTML, DOCX, LaTeX, EPUB, RST)
  └─> pandoc: {format} -> gfm (normalize to markdown)
  └─> kb-ingest (add to knowledge-bases/{topic}/raw/)
  └─> kb-compile (build wiki)
```

This extends `kb-ingest`'s native capabilities to handle formats it does
not directly support.

---

## Chaining Patterns

### Pattern A: Pre-processing (format -> markdown)

Convert non-markdown inputs to GFM before feeding to LLM-based skills.

```bash
pandoc input.docx -t gfm -o input.md --extract-media=media/ --wrap=none
# Now feed input.md to any skill that expects markdown
```

Applicable before: `paper-review`, `meeting-digest`, `kb-ingest`,
`content-repurposing-engine`, `long-form-compressor`

### Pattern B: Post-processing (markdown -> distributable formats)

Convert skill outputs to distributable formats.

```bash
# After any skill produces output.md
pandoc output.md -f gfm \
  --defaults=.cursor/skills/standalone/pandoc/defaults/financial-report.yaml \
  -o output.docx
```

Applicable after: `today`, `paper-review`, `meeting-digest`,
`hf-trending-intelligence`, `daily-strategy-post`, `weekly-status-report`

### Pattern C: Multi-format batch (one source -> N outputs)

```bash
INPUT="report.md"
BASE="${INPUT%.md}"

pandoc "$INPUT" -f gfm -o "${BASE}.docx" \
  --defaults=.cursor/skills/standalone/pandoc/defaults/financial-report.yaml
pandoc "$INPUT" -f gfm -o "${BASE}.pdf" \
  --defaults=.cursor/skills/standalone/pandoc/defaults/korean-pdf.yaml
pandoc "$INPUT" -f gfm -o "${BASE}.html" \
  --defaults=.cursor/skills/standalone/pandoc/defaults/batch-html.yaml
```

### Pattern D: Merge + convert (N sources -> 1 output)

```bash
DATE=$(date +%Y-%m-%d)
pandoc \
  "outputs/today/${DATE}/analysis.md" \
  "outputs/hf-trending/${DATE}/phase5-report.md" \
  -f gfm \
  --defaults=.cursor/skills/standalone/pandoc/defaults/financial-report.yaml \
  --metadata title="Daily Combined Intelligence - ${DATE}" \
  -o "outputs/today/${DATE}/combined.docx"
```

---

## Decision Matrix: When to Use Pandoc in a Pipeline

| Scenario | Use Pandoc? | Alternative |
|----------|-------------|-------------|
| Markdown report -> DOCX with template | Yes | `anthropic-docx` if cell-level control needed |
| Markdown -> PDF (Korean) | Yes | `weasyprint` standalone if no LaTeX |
| DOCX -> Markdown for LLM | Yes | `defuddle` if DOCX is from web |
| HTML -> clean Markdown | Yes | `defuddle` for noisy web pages |
| LaTeX paper -> Markdown | Yes | None (Pandoc is the only tool) |
| Notebook -> DOCX report | Yes | `nbconvert` for Jupyter-native flow |
| Programmatic DOCX with tables | No | `anthropic-docx` (python-docx) |
| PDF form filling | No | `anthropic-pdf` |
| PPTX with complex layouts | No | `anthropic-pptx` |
| Markdown -> Notion page | No | `md-to-notion` (native API) |
| HWP/HWPX conversion | No | `rhwp-converter` |
| Spreadsheet operations | No | `anthropic-xlsx` |

---

## Subagent Invocation Example

When a pipeline skill needs Pandoc conversion, use a shell subagent:

```python
# Pseudocode for pipeline integration
Task(
    subagent_type="shell",
    prompt=f"""
    Convert {input_path} to DOCX using Pandoc with the financial report defaults:

    pandoc "{input_path}" \\
      --defaults=.cursor/skills/standalone/pandoc/defaults/financial-report.yaml \\
      -o "{output_path}"

    Verify the output exists and report the file size.
    """,
    model="fast"
)
```
