# Pandoc Format Matrix

Supported input/output format pairs relevant to the stock analytics project.
Full lists: `pandoc --list-input-formats` and `pandoc --list-output-formats`.

## Project-Relevant Format Pairs

| From | To | Use Case | CLI Example |
|------|-----|----------|-------------|
| `markdown` (gfm) | `docx` | Daily reports, meeting digests | `pandoc -f gfm input.md -o report.docx` |
| `markdown` | `pdf` | Archival reports | `pandoc input.md -o report.pdf --pdf-engine=xelatex` |
| `markdown` | `html` | Email-ready or web preview | `pandoc input.md -o report.html -s` |
| `markdown` | `pptx` | Slide decks from analysis MD | `pandoc input.md --slide-level=2 -o slides.pptx` |
| `markdown` | `epub` | E-reader export | `pandoc input.md -o report.epub` |
| `markdown` | `plain` | Text extraction / word count | `pandoc input.md -t plain` |
| `markdown` | `latex` | Academic paper source | `pandoc input.md -o paper.tex -s` |
| `markdown` | `rst` | Sphinx docs integration | `pandoc input.md -t rst -o output.rst` |
| `docx` | `gfm` | Reverse extraction for LLM | `pandoc input.docx -t gfm -o output.md --extract-media=media/` |
| `docx` | `plain` | Spot-check / validation | `pandoc input.docx -t plain` |
| `docx` | `html` | Web publishing | `pandoc input.docx -o output.html -s` |
| `html` | `gfm` | Clean markdown from web | `pandoc input.html -t gfm -o output.md` |
| `html` | `docx` | Email-to-DOCX | `pandoc input.html -o output.docx` |
| `html` | `pdf` | PDF from HTML content | `pandoc input.html -o out.pdf --pdf-engine=weasyprint` |
| `epub` | `gfm` | E-book extraction | `pandoc input.epub -t gfm -o output.md` |
| `ipynb` | `gfm` | Notebook to markdown | `pandoc input.ipynb -t gfm -o output.md` |
| `ipynb` | `docx` | Notebook to Word report | `pandoc input.ipynb -o output.docx` |
| `latex` | `gfm` | LaTeX paper extraction | `pandoc input.tex -t gfm -o output.md` |
| `latex` | `docx` | LaTeX to Word | `pandoc input.tex -o output.docx` |
| `json` (pandoc AST) | `gfm` | Debug AST output | `pandoc input.md -t json \| pandoc -f json -t gfm` |
| `rst` | `gfm` | RST docs to markdown | `pandoc input.rst -t gfm -o output.md` |
| `odt` | `gfm` | LibreOffice extraction | `pandoc input.odt -t gfm -o output.md` |
| `csv` | `html` | Quick table view | `pandoc input.csv -t html -o table.html` |

## Format Notes

### Input Format Detection

Pandoc auto-detects the input format from the file extension. Explicit `-f`
is needed when the extension is ambiguous (e.g., `.txt` could be markdown
or plain text) or when using stdin.

Common auto-detection mappings:

| Extension | Detected Format |
|-----------|-----------------|
| `.md`, `.markdown` | `markdown` |
| `.docx` | `docx` |
| `.html`, `.htm` | `html` |
| `.tex` | `latex` |
| `.rst` | `rst` |
| `.epub` | `epub` |
| `.ipynb` | `ipynb` |
| `.odt` | `odt` |
| `.pptx` | `pptx` |
| `.csv` | `csv` |

### Markdown Variants

| Variant | Flag | Notes |
|---------|------|-------|
| Pandoc Markdown | `markdown` | Default; most extensions |
| GitHub-Flavored | `gfm` | Pipe tables, task lists, autolinks |
| CommonMark | `commonmark` | Strict spec compliance |
| MultiMarkdown | `markdown_mmd` | MMD metadata, crossrefs |
| Markdown Strict | `markdown_strict` | Original Gruber spec |

For this project, prefer `gfm` for output (maximum downstream compatibility)
and `markdown` for input (supports YAML frontmatter and extensions).

### DOCX Style Mapping (Reference Doc)

Pandoc maps these internal styles when using `--reference-doc`:

| Pandoc Element | DOCX Style Name |
|----------------|-----------------|
| Heading 1-9 | Heading 1-9 |
| Normal paragraph | Body Text / First Paragraph |
| Block quote | Block Text |
| Code block | Source Code |
| Inline code | Verbatim Char |
| Bullet list | Compact / Body Text |
| Table | Table |
| Caption | Caption / Table Caption / Image Caption |
| Title | Title |
| Subtitle | Subtitle |
| Author | Author |
| Date | Date |
| Abstract | Abstract |
| TOC | TOC Heading |
| Footnote | Footnote Text / Footnote Reference |
| Hyperlink | Hyperlink |
| Header/Footer | Header / Footer |

### PDF Engine Selection Guide

| Scenario | Engine | Why |
|----------|--------|-----|
| Korean documents | `xelatex` | Full CJK Unicode support |
| English-only, fast | `pdflatex` | Fastest LaTeX engine |
| No LaTeX installed | `weasyprint` | HTML-to-PDF, pip installable |
| Lua scripting needed | `lualatex` | Embedded Lua in TeX |
| Modern typesetting | `typst` | Fast, modern alternative to LaTeX |

### Unsupported / Limited Pairs

| From | To | Issue |
|------|-----|-------|
| `pdf` | anything | Pandoc cannot read PDF directly |
| `xlsx` | `docx` | Use `anthropic-xlsx` + this skill |
| `pptx` | `gfm` | Limited: extracts text only, no layout |
| `docx` | `pptx` | Not direct: convert via markdown first |
| `hwp` / `hwpx` | anything | Use `rhwp-converter` instead |
