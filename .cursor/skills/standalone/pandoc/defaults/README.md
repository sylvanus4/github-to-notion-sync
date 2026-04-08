# Pandoc Defaults Files

YAML defaults files that bundle common Pandoc CLI options for repeatable conversions.

## Included Defaults

| File | Purpose |
|------|---------|
| `financial-report.yaml` | Markdown to DOCX for stock analysis reports (GFM, TOC, Korean tables) |
| `korean-pdf.yaml` | Markdown to PDF with Korean CJK font support (xelatex) |
| `reverse-extract.yaml` | DOCX to GFM markdown with image extraction |
| `batch-html.yaml` | Markdown to standalone HTML with embedded resources and signal colors |

## Usage

```bash
pandoc input.md --defaults=.cursor/skills/standalone/pandoc/defaults/financial-report.yaml -o output.docx
```

Override any defaults option on the command line:

```bash
pandoc input.md --defaults=financial-report.yaml --no-toc -o output.docx
```

## Customization

Copy an existing defaults file and modify for your use case. Key fields:
- `from` / `to`: input/output formats
- `lua-filters`: list of Lua filter paths
- `variables`: template variables (fonts, margins, etc.)
- `metadata`: document metadata (lang, title, author)
