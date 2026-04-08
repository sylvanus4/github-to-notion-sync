# Pandoc Reference Templates

Reference-doc templates for `--reference-doc` flag. Pandoc copies styles
(fonts, heading sizes, margins, colors) from these DOCX files into output.

## Bootstrap a Template

Generate Pandoc's default reference DOCX, then customize it in Word/LibreOffice:

```bash
pandoc -o .cursor/skills/standalone/pandoc/templates/thaki-report.docx \
  --print-default-data-file reference.docx
```

Open in Word or LibreOffice, modify styles (Heading 1-6, Body Text, First
Paragraph, Table, Block Text, etc.), then save. Pandoc will use your
customized styles for all future conversions.

## Key Styles to Customize

| Style Name | Pandoc Element |
|------------|---------------|
| Heading 1-6 | `#` through `######` |
| Body Text / First Paragraph | Normal paragraphs |
| Block Text | Block quotes (`>`) |
| Definition Term / Definition | Definition lists |
| Table | Pipe tables |
| Source Code | Fenced code blocks |
| Compact / Tight list | Tight bullet/numbered lists |

## Usage

```bash
pandoc report.md -f gfm \
  --reference-doc=.cursor/skills/standalone/pandoc/templates/thaki-report.docx \
  -o output.docx
```
