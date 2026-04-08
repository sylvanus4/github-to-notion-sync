# Pandoc CLI Recipes

Copy-paste ready CLI commands and defaults file examples for the stock analytics
project. All paths are relative to the project root.

---

## Quick Reference Flags

| Flag | Purpose |
|------|---------|
| `-f FORMAT` | Input format (auto-detected from extension) |
| `-t FORMAT` | Output format |
| `-o FILE` | Output file |
| `-s` | Standalone (includes head/preamble) |
| `--reference-doc=FILE` | Template for DOCX/PPTX/ODT |
| `--lua-filter=FILE` | Apply Lua AST filter (chainable) |
| `--defaults=FILE` | Load options from YAML defaults file |
| `--toc` | Generate table of contents |
| `--toc-depth=N` | TOC heading depth |
| `--number-sections` | Number headings |
| `--pdf-engine=ENGINE` | PDF rendering engine |
| `--extract-media=DIR` | Extract images on reverse conversion |
| `--metadata=KEY:VAL` | Set metadata variable |
| `--resource-path=DIRS` | Search path for images/includes |
| `--template=FILE` | Custom output template |
| `--wrap=none` | Disable line wrapping in output |
| `--columns=N` | Line wrap width (default 72) |
| `--shift-heading-level-by=N` | Shift heading levels |
| `--strip-comments` | Remove HTML comments |
| `--verbose` | Debug output |

---

## Daily Reports (Markdown -> DOCX)

### Basic conversion

```bash
pandoc outputs/today/$(date +%Y-%m-%d)/analysis.md \
  -f gfm -o outputs/today/$(date +%Y-%m-%d)/analysis.docx
```

### With Korean reference template

```bash
pandoc outputs/today/$(date +%Y-%m-%d)/analysis.md \
  -f gfm \
  --reference-doc=.cursor/skills/standalone/pandoc/templates/thaki-report.docx \
  -o outputs/today/$(date +%Y-%m-%d)/analysis.docx
```

### With Lua filters for financial formatting

```bash
pandoc outputs/today/$(date +%Y-%m-%d)/analysis.md \
  -f gfm \
  --reference-doc=.cursor/skills/standalone/pandoc/templates/thaki-report.docx \
  --lua-filter=.cursor/skills/standalone/pandoc/filters/korean-date.lua \
  --lua-filter=.cursor/skills/standalone/pandoc/filters/comma-numbers.lua \
  --lua-filter=.cursor/skills/standalone/pandoc/filters/signal-colors.lua \
  -o outputs/today/$(date +%Y-%m-%d)/analysis.docx
```

---

## PDF Generation

### Korean PDF with XeLaTeX

```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V mainfont="Noto Sans CJK KR" \
  -V monofont="D2Coding" \
  -V geometry:margin=2.5cm \
  -V fontsize=11pt \
  --toc
```

### English PDF with Weasyprint (no LaTeX needed)

```bash
pandoc input.md -o output.pdf \
  --pdf-engine=weasyprint \
  --css=.cursor/skills/standalone/pandoc/templates/report.css \
  -s
```

### Archival PDF with metadata

```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V mainfont="Noto Sans CJK KR" \
  --metadata title="Daily Stock Analysis" \
  --metadata author="ThakiCloud AI Analytics" \
  --metadata date="$(date +%Y-%m-%d)" \
  --toc --number-sections
```

---

## Reverse Conversion (DOCX -> Markdown)

### Basic extraction

```bash
pandoc input.docx -t gfm -o output.md --wrap=none
```

### With media extraction

```bash
pandoc input.docx -t gfm -o output.md \
  --extract-media=media/ \
  --wrap=none
```

### Clean extraction (strip comments, normalize headings)

```bash
pandoc input.docx -t gfm -o output.md \
  --extract-media=media/ \
  --wrap=none \
  --strip-comments \
  --shift-heading-level-by=0
```

---

## Multi-Format Batch Output

### Single source to 4 formats

```bash
INPUT=outputs/today/$(date +%Y-%m-%d)/analysis.md
BASE="${INPUT%.md}"

pandoc "$INPUT" -f gfm -o "${BASE}.docx" \
  --reference-doc=.cursor/skills/standalone/pandoc/templates/thaki-report.docx

pandoc "$INPUT" -f gfm -o "${BASE}.pdf" \
  --pdf-engine=xelatex -V mainfont="Noto Sans CJK KR"

pandoc "$INPUT" -f gfm -o "${BASE}.html" -s \
  --metadata title="Daily Analysis"

pandoc "$INPUT" -f gfm -t plain -o "${BASE}.txt"

echo "Generated: .docx .pdf .html .txt"
```

### Shell function for batch conversion

```bash
pandoc_batch() {
  local input="$1"
  local base="${input%.*}"
  local formats="${2:-docx,pdf,html}"

  IFS=',' read -ra fmts <<< "$formats"
  for fmt in "${fmts[@]}"; do
    case "$fmt" in
      pdf)
        pandoc "$input" -f gfm -o "${base}.pdf" \
          --pdf-engine=xelatex -V mainfont="Noto Sans CJK KR"
        ;;
      docx)
        pandoc "$input" -f gfm -o "${base}.docx" \
          --reference-doc=.cursor/skills/standalone/pandoc/templates/thaki-report.docx
        ;;
      html)
        pandoc "$input" -f gfm -o "${base}.html" -s
        ;;
      pptx)
        pandoc "$input" -f gfm -o "${base}.pptx" --slide-level=2
        ;;
      epub)
        pandoc "$input" -f gfm -o "${base}.epub"
        ;;
    esac
    echo "  -> ${base}.${fmt}"
  done
}

# Usage: pandoc_batch report.md "docx,pdf,html"
```

---

## Document Merging

### Merge multiple markdown files

```bash
pandoc part1.md part2.md part3.md \
  -f gfm -o combined.docx \
  --reference-doc=.cursor/skills/standalone/pandoc/templates/thaki-report.docx \
  --toc
```

### Merge with section breaks (DOCX)

Create a Lua filter to insert page breaks between files:

```bash
pandoc part1.md part2.md part3.md \
  -f gfm \
  --lua-filter=.cursor/skills/standalone/pandoc/filters/section-break.lua \
  -o combined.docx
```

### Merge pipeline outputs for a date

```bash
DATE=$(date +%Y-%m-%d)
pandoc \
  outputs/today/${DATE}/analysis.md \
  outputs/hf-trending/${DATE}/phase5-report.md \
  -f gfm -o "outputs/today/${DATE}/combined-report.docx" \
  --metadata title="Daily Combined Report - ${DATE}" \
  --toc
```

---

## Slide Decks

### Markdown to PPTX

```bash
pandoc slides.md -o slides.pptx --slide-level=2
```

### With reference template

```bash
pandoc slides.md -o slides.pptx \
  --slide-level=2 \
  --reference-doc=.cursor/skills/standalone/pandoc/templates/thaki-slides.pptx
```

### Slide structure convention

```markdown
# Section Title (slide separator at level 1)

## Slide Title (new slide at level 2)

- Bullet point
- Another point

## Another Slide

Content here.

---

This horizontal rule also creates a new slide.
```

---

## Notebook Conversion

### Jupyter to Markdown

```bash
pandoc notebook.ipynb -t gfm -o notebook.md --extract-media=media/
```

### Jupyter to DOCX report

```bash
pandoc notebook.ipynb -o report.docx \
  --reference-doc=.cursor/skills/standalone/pandoc/templates/thaki-report.docx
```

### Jupyter to PDF

```bash
pandoc notebook.ipynb -o report.pdf \
  --pdf-engine=xelatex -V mainfont="Noto Sans CJK KR"
```

---

## HTML Operations

### HTML to clean Markdown

```bash
pandoc input.html -t gfm -o output.md --wrap=none
```

### Markdown to self-contained HTML

```bash
pandoc input.md -o output.html -s --self-contained \
  --metadata title="Report Title"
```

### HTML to PDF via Weasyprint

```bash
pandoc input.html -o output.pdf --pdf-engine=weasyprint
```

---

## LaTeX / Academic

### Markdown to LaTeX source

```bash
pandoc paper.md -o paper.tex -s \
  --citeproc --bibliography=refs.bib
```

### LaTeX to Markdown (paper extraction)

```bash
pandoc paper.tex -t gfm -o paper.md --wrap=none
```

### LaTeX to DOCX (for reviewers)

```bash
pandoc paper.tex -o paper.docx \
  --citeproc --bibliography=refs.bib
```

---

## Defaults Files

Defaults files simplify repeated commands. Store in
`.cursor/skills/standalone/pandoc/defaults/`.

### defaults/financial-report.yaml

```yaml
from: gfm
to: docx
standalone: true
reference-doc: .cursor/skills/standalone/pandoc/templates/thaki-report.docx
filters:
  - .cursor/skills/standalone/pandoc/filters/inject-metadata.lua
  - .cursor/skills/standalone/pandoc/filters/korean-date.lua
  - .cursor/skills/standalone/pandoc/filters/comma-numbers.lua
  - .cursor/skills/standalone/pandoc/filters/signal-colors.lua
table-of-contents: true
toc-depth: 3
metadata:
  lang: ko-KR
  author: ThakiCloud AI Analytics
```

Usage:

```bash
pandoc --defaults=.cursor/skills/standalone/pandoc/defaults/financial-report.yaml \
  input.md -o report.docx
```

### defaults/korean-pdf.yaml

```yaml
from: gfm
to: pdf
pdf-engine: xelatex
standalone: true
table-of-contents: true
number-sections: true
variables:
  mainfont: "Noto Sans CJK KR"
  monofont: "D2Coding"
  geometry: "margin=2.5cm"
  fontsize: "11pt"
  linestretch: 1.5
metadata:
  lang: ko-KR
  author: ThakiCloud AI Analytics
```

### defaults/reverse-extract.yaml

```yaml
from: docx
to: gfm
wrap: none
extract-media: media/
strip-comments: true
```

### defaults/batch-html.yaml

```yaml
from: gfm
to: html
standalone: true
self-contained: true
metadata:
  lang: ko-KR
```

---

## Verification Commands

### Check pandoc version and features

```bash
pandoc --version
```

### List all supported formats

```bash
pandoc --list-input-formats
pandoc --list-output-formats
```

### Validate conversion (check output exists and has content)

```bash
pandoc input.md -o output.docx && \
  [ -s output.docx ] && echo "OK: $(wc -c < output.docx) bytes" || echo "FAIL"
```

### PDF page count check (requires pdfinfo from poppler)

```bash
pandoc input.md -o output.pdf --pdf-engine=xelatex && \
  pdfinfo output.pdf | grep Pages
```

### Diff-check reverse conversion fidelity

```bash
pandoc original.md -o temp.docx
pandoc temp.docx -t gfm -o roundtrip.md --wrap=none
diff original.md roundtrip.md
```
