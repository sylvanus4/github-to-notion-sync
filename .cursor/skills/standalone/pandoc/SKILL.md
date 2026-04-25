---
name: pandoc
description: >-
  Universal document format converter using Pandoc CLI. Supports 60+ input and
  80+ output formats with reference-doc templating, Lua filter pipelines,
  multi-format batch output, document merging, and bidirectional conversion.
  Use when the user asks to "convert document format", "markdown to docx",
  "markdown to pdf", "batch convert", "pandoc", "multi-format output",
  "apply document template", "reference doc", "lua filter", "merge documents",
  "reverse convert docx to markdown", "format conversion", "docx to markdown",
  "html to pdf", "epub to markdown", "ipynb to docx", "defaults file",
  "pandoc batch", or needs universal format conversion between any supported
  document formats.
  Do NOT use for programmatic OOXML slot filling (use docx-template-engine).
  Do NOT use for python-docx table/style manipulation (use anthropic-docx).
  Do NOT use for PPTX slide-by-slide programmatic building (use anthropic-pptx).
  Do NOT use for PDF form filling or merging (use anthropic-pdf).
  Do NOT use for spreadsheet operations (use anthropic-xlsx).
  Do NOT use for Notion page publishing (use md-to-notion).
  Do NOT use for HWP conversion (use rhwp-converter).
  Korean triggers: "문서 변환", "마크다운 변환", "판독", "다중 포맷",
  "배치 변환", "문서 포맷 변환", "docx에서 마크다운", "reference-doc 적용",
  "루아 필터", "문서 합치기", "포맷 변환".
metadata:
  author: ThakiCloud
  version: 0.1.0
  category: standalone
---

# Pandoc -- Universal Document Format Converter

Convert between 60+ input and 80+ output document formats via a single CLI
tool. Pandoc is the de facto standard for format-agnostic document conversion,
particularly strong for Markdown-to-DOCX with corporate template support.

## Quick Reference

```bash
# MD → DOCX (with template)
pandoc input.md --reference-doc=templates/thaki-report.docx -o output.docx

# MD → PDF (Korean)
pandoc input.md -o output.pdf --pdf-engine=xelatex -V mainfont="Noto Sans CJK KR"

# DOCX → MD (reverse)
pandoc input.docx -t gfm --extract-media=media/ --wrap=none -o output.md

# Batch (MD → DOCX + PDF + HTML)
for fmt in docx pdf html; do pandoc input.md -o "output.${fmt}"; done

# Lua filter chain
pandoc input.md --lua-filter=filters/fix-korean-tables.lua --lua-filter=filters/comma-numbers.lua -o output.docx
```

## Prerequisites

| Tool | Install | Required |
|------|---------|----------|
| `pandoc` | `brew install pandoc` | YES |
| TeX Live | `brew install --cask mactex-no-gui` | Only for PDF via LaTeX |
| `weasyprint` | `pip install weasyprint` | Only for HTML-to-PDF |

Verify: `pandoc --version` (requires 3.0+)

## When to Use Pandoc vs Other Skills

| Task | Use This Skill | Use Instead |
|------|----------------|-------------|
| MD -> DOCX (quick, template-based) | YES | -- |
| MD -> DOCX (programmatic OOXML slots) | -- | docx-template-engine |
| MD -> DOCX (python-docx table surgery) | -- | anthropic-docx |
| MD -> PDF | YES | -- |
| MD -> PPTX (slide-level markdown) | YES | -- |
| PPTX (slide-by-slide JS builder) | -- | anthropic-pptx |
| Multi-format batch from one source | YES | -- |
| DOCX -> MD (reverse extraction) | YES | -- |
| PDF form fill / merge | -- | anthropic-pdf |
| Lua filter content transforms | YES | -- |
| Notion publishing | -- | md-to-notion |

## Core Workflows

### Mode 1: Convert (Single Format)

Convert one file between any two supported formats.

```bash
pandoc input.md -o output.docx
pandoc input.html -o output.pdf --pdf-engine=weasyprint
pandoc input.docx -t gfm --wrap=none -o output.md --extract-media=media/
pandoc input.ipynb -o output.docx
pandoc input.epub -t gfm --wrap=none -o output.md
```

> **If PDF fails**: Ensure a PDF engine is installed. Add `--pdf-engine=xelatex` (or `weasyprint`). For Korean, also add `-V mainfont="Noto Sans CJK KR"`.

Key flags:

| Flag | Purpose |
|------|---------|
| `-f` / `--from` | Input format (auto-detected from extension if omitted) |
| `-t` / `--to` | Output format (auto-detected from `-o` extension if omitted) |
| `-o` / `--output` | Output file path |
| `-s` / `--standalone` | Produce complete document with header/footer (auto for docx/pdf/epub) |
| `--extract-media=DIR` | Extract images from binary formats to DIR |
| `--wrap=none` | Disable line wrapping in text outputs |

### Mode 2: Batch (Multi-Format Output)

Generate multiple output formats from a single source file.

```bash
INPUT="report.md"
BASENAME="${INPUT%.md}"
for fmt in docx pdf html; do
  pandoc "$INPUT" -o "${BASENAME}.${fmt}"
done
```

> **If PDF in batch fails**: The batch loop needs `--pdf-engine` for PDF. Use: `pandoc "$INPUT" --pdf-engine=xelatex -o "${BASENAME}.pdf"` separately from the loop, or add engine detection inline.

For PPTX output, add `--slide-level=2` to control heading-to-slide mapping:

```bash
pandoc slides.md --slide-level=2 -o slides.pptx
```

### Mode 3: Template (Reference Doc)

Apply corporate styling from a reference document. Pandoc copies styles,
page layout, headers/footers from the reference doc but ignores its content.

```bash
pandoc input.md --reference-doc=templates/thaki-report.docx -o output.docx
pandoc slides.md --reference-doc=templates/thaki-slides.pptx -o output.pptx
```

> **If reference doc not found**: Verify the path. Use `ls templates/*.docx` to check. Generate a fresh one with the command below.

Generate a starter reference doc to customize:

```bash
pandoc -o custom-reference.docx --print-default-data-file reference.docx
pandoc -o custom-reference.pptx --print-default-data-file reference.pptx
```

Open the generated file in Word/PowerPoint, modify styles (Heading 1-9,
Normal, Title, TOC Heading, Table, etc.), save, and use as `--reference-doc`.

DOCX styles that Pandoc maps: Normal, Body Text, First Paragraph, Compact,
Title, Subtitle, Author, Date, Abstract, Bibliography, Heading 1-9,
Block Text, Footnote Text, Definition Term, Definition, Caption,
Table Caption, Image Caption, Figure, Captioned Figure, TOC Heading,
Header, Footer, and more. See `references/format-matrix.md` for the full list.

### Mode 4: Filter (Lua Transforms)

Apply Lua filters to transform the document AST between parsing and writing.
Filters run in the order specified on the command line.

```bash
pandoc input.md --lua-filter=filters/fix-korean-tables.lua -o output.docx
pandoc input.md --lua-filter=filters/fix-korean-tables.lua --lua-filter=filters/comma-numbers.lua -o out.docx
```

> **If filter not found**: Check the path with `ls filters/*.lua`. Lua filters must exist as files; inline Lua is not supported via `--lua-filter`.

See `references/lua-filters.md` for filter patterns and examples.

### Mode 5: Merge (Multi-Source)

Combine multiple input files into a single output document.

```bash
pandoc ch1.md ch2.md ch3.md metadata.yaml -o book.docx
pandoc --file-scope part1.md part2.md -o combined.docx
```

`--file-scope` treats each file as an independent document (footnote numbering
resets per file). Without it, files are concatenated before parsing.

### Mode 6: Reverse (Binary to Markdown)

Extract clean markdown from binary formats for LLM processing or pipeline
ingestion.

```bash
pandoc input.docx -t gfm --wrap=none -o output.md --extract-media=media/
pandoc input.epub -t gfm --wrap=none -o output.md
pandoc input.html -t gfm --wrap=none -o output.md
pandoc input.odt -t gfm --wrap=none -o output.md
```

Use `-t gfm` (GitHub-Flavored Markdown) for maximum compatibility with
downstream tools. `--wrap=none` prevents mid-word line breaks in CJK text
and produces single-line paragraphs for cleaner downstream parsing.

## Mode 7: Mermaid-Aware Conversion

Pandoc cannot render Mermaid diagrams natively. When the source Markdown
contains ` ```mermaid ``` ` code blocks, **pre-process** them into PNG images
before running Pandoc using the shared `scripts/preprocess_mermaid.py` script.

**Prerequisites:**
- `npm install -g @mermaid-js/mermaid-cli` (provides `mmdc`)
- Python 3.9+

**Full workflow:**

```bash
# 1. Pre-process Mermaid blocks → PNG images + clean Markdown
python3 scripts/preprocess_mermaid.py input.md \
  --output-dir diagrams/ \
  --output input-for-docx.md \
  --width 1200 --scale 2 --background transparent

# 2. Convert pre-processed Markdown to DOCX
pandoc input-for-docx.md -o output.docx \
  --from markdown --to docx --resource-path=.

# 3. Clean up temp files (optional — keep PNGs if archiving)
rm -rf diagrams/*.mmd
```

**Key points:**
- `--resource-path=.` tells Pandoc to resolve relative image paths from the
  current directory.
- The pre-processing script extracts each Mermaid block, renders it to PNG via
  `mmdc`, replaces the block with `![Diagram N](path.png)`, and strips
  unsupported HTML tags (`<details>`/`<summary>`).
- Combine with `--reference-doc` (Mode 3) for branded output.
- See the `mermaid-render` skill for advanced configuration: theme selection
  (`--theme dark|forest|neutral`), batch processing, and Puppeteer/Chromium
  troubleshooting.

## Mode 8: Korean DOCX Pipeline (Pandoc + python-docx Post-Processing)

When producing Korean DOCX documents, Pandoc's default styling is insufficient.
Use a two-stage pipeline: Pandoc generates the structural DOCX, then `python-docx`
post-processes it for professional Korean formatting.

**Stage 1: Pandoc with Korean reference-doc**

```bash
pandoc input.md -o output.docx \
  --reference-doc=korean-reference.docx \
  --resource-path=. \
  -f markdown -t docx \
  --highlight-style=kate
```

The `korean-reference.docx` template defines base styles (A4, Malgun Gothic,
heading colors). Generate one with `python-docx` — see the `anthropic-docx`
skill's "Korean Style Guide" section for the creation script.

**Stage 2: python-docx post-processing (via anthropic-docx)**

Pandoc's reference-doc applies style *definitions* but doesn't enforce them on
every run. The post-processing script forces consistent formatting:

```python
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

doc = Document("output.docx")

FONT_KR = '맑은 고딕'
FONT_CODE = 'D2Coding'
FONT_CODE_FB = 'Consolas'
COLOR_BODY = RGBColor(0x33, 0x33, 0x33)
COLOR_HEADING = RGBColor(0x1A, 0x3C, 0x6E)
CODE_BG = 'F0F0F0'

# Pandoc syntax-highlight character styles (detect code blocks by these)
TOKEN_STYLES = {
    'AttributeTok', 'FunctionTok', 'KeywordTok', 'NormalTok',
    'StringTok', 'DataTypeTok', 'CommentTok', 'OtherTok', 'DecValTok',
    'BuiltInTok', 'OperatorTok', 'ControlFlowTok', 'VariableTok',
    'BaseNTok', 'FloatTok', 'ConstantTok', 'CharTok', 'SpecialCharTok',
    'SpecialStringTok', 'ImportTok', 'DocumentationTok', 'AnnotationTok',
    'PreprocessorTok', 'InformationTok', 'WarningTok', 'AlertTok',
    'ErrorTok', 'RegionMarkerTok',
}

def is_code_para(para):
    for run in para.runs:
        rs = run.style.name if run.style else ''
        if rs in TOKEN_STYLES:
            return True
    return False

# Apply formatting per paragraph type
for para in doc.paragraphs:
    if is_code_para(para):
        # Monospace + shading
        add_para_shading(para, CODE_BG)
        for run in para.runs:
            set_run_code_font(run)  # D2Coding 9pt
    elif para.style.name.startswith('Heading'):
        for run in para.runs:
            set_run_font_kr(run, FONT_KR, heading_size, COLOR_HEADING, bold=True)
    else:
        for run in para.runs:
            set_run_font_kr(run, FONT_KR, 10, COLOR_BODY)

# Table formatting: header row shading, generous cell padding, alternating rows
for table in doc.tables:
    for row_idx, row in enumerate(table.rows):
        for cell in row.cells:
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            if row_idx == 0:
                set_cell_shading(cell, '1A3C6E')  # dark header
                # white text
            elif row_idx % 2 == 0:
                set_cell_shading(cell, 'F8F9FA')  # zebra stripe

doc.save("output.docx")
```

See the `anthropic-docx` skill's "Korean Style Guide" section for complete
helper functions (`set_run_font_kr`, `set_run_code_font`, `add_para_shading`,
`set_cell_margins`, `set_cell_shading`, `set_table_borders`).

**Key points:**
- Pandoc assigns `*Tok` character styles (e.g., `KeywordTok`, `StringTok`) for
  syntax highlighting — there is no `Source Code` *paragraph* style. Detect
  code blocks by checking if any run in a paragraph uses a `*Tok` style.
- `w:eastAsia` font attribute is required for Korean glyphs to render correctly.
- Table cell margins use DXA units (80 DXA ≈ 1.4mm, 120 DXA ≈ 2.1mm).
- Always re-apply A4 page dimensions in post-processing to guarantee consistency.

**Combined one-liner (Mermaid + Korean pipeline):**

```bash
# 1. Pre-process Mermaid (Mode 7)
python3 preprocess_mermaid.py input.md > input-for-docx.md

# 2. Pandoc with Korean reference
pandoc input-for-docx.md -o output.docx \
  --reference-doc=korean-reference.docx \
  --resource-path=. --highlight-style=kate

# 3. Post-process with python-docx
python3 korean_postprocess.py output.docx
```

## Defaults Files

Store repeatable configurations in YAML defaults files to avoid long CLI
commands.

```bash
pandoc -d defaults/financial-report.yaml input.md
```

Defaults files are searched in the working directory, then in
`~/.local/share/pandoc/defaults/`. Extension `.yaml` is added automatically.

Example defaults file:

```yaml
from: markdown
to: docx
standalone: true
wrap: none
reference-doc: templates/thaki-report.docx
lua-filter:
  - filters/fix-korean-tables.lua
metadata:
  author: ThakiCloud
  lang: ko
  date: 2026-04-08
toc: true
toc-depth: 3
number-sections: true
```

See `references/cli-recipes.md` for more defaults file examples.

## Output Protocol

Output files go to `outputs/pandoc/{date}/` for pipeline-generated content,
or to the user-specified path for ad-hoc conversions.

```bash
DATE=$(date +%Y-%m-%d)
mkdir -p "outputs/pandoc/${DATE}"
pandoc input.md -o "outputs/pandoc/${DATE}/report.docx"
```

## Pipeline Integration

| Pipeline | Integration Point |
|----------|-------------------|
| `today` | After analysis MD generation, batch convert to DOCX+PDF |
| `paper-review` | Reverse-convert PDF/DOCX papers to MD for LLM processing |
| `meeting-digest` | Batch-convert summary MD to DOCX+PDF for archive |
| `md-to-notion` | Normalize MD with `pandoc -t gfm` before Notion upload |
| `bespin-news-digest` | Convert collected articles to unified DOCX report |

See `references/pipeline-integration.md` for detailed chaining patterns.

## PDF Engine Options

| Engine | Format Path | Install |
|--------|-------------|---------|
| `pdflatex` | LaTeX -> PDF (default) | TeX Live |
| `xelatex` | LaTeX -> PDF (Unicode/CJK) | TeX Live |
| `lualatex` | LaTeX -> PDF (Lua scripting) | TeX Live |
| `weasyprint` | HTML -> PDF | `pip install weasyprint` |
| `prince` | HTML -> PDF (commercial) | prince.com |
| `typst` | Typst -> PDF | `brew install typst` |
| `context` | ConTeXt -> PDF | TeX Live |

For Korean documents, use `xelatex` with appropriate CJK font settings:

```bash
pandoc input.md -o output.pdf --pdf-engine=xelatex \
  -V mainfont="Noto Sans CJK KR" \
  -V CJKmainfont="Noto Sans CJK KR"
```

## Gotchas

1. **PDF requires LaTeX or weasyprint** -- `pandoc input.md -o output.pdf`
   fails without a PDF engine installed. Use `--pdf-engine` to select one.

2. **PPTX slide splitting** -- By default, level-1 headings become slide
   titles. Use `--slide-level=N` to control which heading level splits slides.
   Horizontal rules (`---`) also create slide breaks.

3. **Image paths in DOCX->MD** -- Always use `--extract-media=DIR` when
   reversing DOCX to MD, otherwise images are lost. Paths in the output MD
   will be relative to DIR.

4. **Table rendering** -- Complex merged-cell tables may lose structure in
   conversion. Pandoc pipe tables and grid tables have limited column span
   support. For complex tables, consider Lua filters or post-processing.

5. **Korean line breaks** -- Use `--wrap=none` for Korean content to prevent
   mid-word line breaks in text-based output formats.

6. **Reference-doc content ignored** -- `--reference-doc` only copies styles
   and document properties. The content of the reference document is discarded.

7. **Metadata precedence** -- CLI `-M` overrides defaults file `metadata:`
   which overrides document YAML frontmatter for the same key.

8. **Extension syntax** -- Format extensions use `+`/`-`:
   `pandoc -f markdown+emoji-smart` enables emoji, disables smart quotes.

## Verification

After generating output, run the format-specific validation:

| Output | Validation Command | Pass Criteria |
|--------|-------------------|---------------|
| DOCX | `pandoc output.docx --to plain \| head -50` | Readable text, no garbled chars |
| PDF | `pdfinfo output.pdf \| grep Pages` | Pages >= 1 |
| HTML | `pandoc output.html --to plain \| wc -w` | Word count > 0 |
| MD (reverse) | `head -20 output.md` | Clean markdown, no binary artifacts |
| PPTX | `unzip -l output.pptx \| grep -c 'ppt/slides/slide'` | Slide count >= 1 |
| EPUB | `pandoc output.epub --to plain \| wc -w` | Word count > 0 |
| **All formats** | `test -s OUTPUT \|\| echo "ERROR: Empty"` | File exists and non-zero size |

For pipeline outputs, always run the "All formats" check before proceeding
to the next stage. For Korean content, additionally spot-check that CJK
characters render correctly (not mojibake).

## See Also

- `anthropic-docx` -- Programmatic DOCX creation with python-docx
- `anthropic-pdf` -- PDF manipulation with pypdf
- `anthropic-pptx` -- Slide-by-slide PPTX builder
- `md-to-notion` -- Publish markdown to Notion pages
- `rhwp-converter` -- HWP/HWPX document conversion
- `docx-template-engine` -- OOXML slot-based template filling

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `pandoc: Unknown input format` | Unsupported or misspelled format | Check `pandoc --list-input-formats` |
| `pandoc: Cannot find pdf engine` | PDF engine not installed | Install: `brew install --cask mactex-no-gui` or `pip install weasyprint` |
| `pandoc: Could not find reference doc` | Wrong path to template | Verify path; use absolute path or `--data-dir` |
| `pandoc: openBinaryFile: does not exist` | Input file not found | Check file path and working directory |
| Empty DOCX output | Input has no parseable content | Verify input format matches `-f` flag |
| Garbled Korean text in PDF | Missing CJK fonts | Use `xelatex` with `-V mainfont` and `-V CJKmainfont` |
| Tables misaligned | Pipe table column width issues | Use `--columns=120` or grid tables |
