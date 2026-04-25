---
name: anthropic-docx
description: >-
  Create, read, edit, and manipulate Word documents (.docx). Use when the user
  mentions Word doc, .docx, or requests professional documents with tables of
  contents, headings, page numbers, letterheads; extracting or reorganizing
  content from .docx; inserting or replacing images; find-and-replace; tracked
  changes or comments; reports, memos, letters, templates as Word files. Do NOT
  use for PDFs (use anthropic-pdf), spreadsheets (use anthropic-xlsx), or
  presentations (use anthropic-pptx). Korean triggers: "워드 문서", "docx",
  "문서 생성", "리포트".
metadata:
  author: "anthropic"
  version: "1.0.0"
  license_note: "See LICENSE.txt in skill directory"
  category: "document"
---
# DOCX creation, editing, and analysis

## Overview

A .docx file is a ZIP archive containing XML files.

## Quick Reference

| Task | Approach |
|------|----------|
| Read/analyze content | `pandoc` or unpack for raw XML |
| Create new document | Use `docx-js` - see Creating New Documents below |
| Edit existing document | Unpack → edit XML → repack - see Editing Existing Documents below |

### Converting .doc to .docx

Legacy `.doc` files must be converted before editing:

```bash
python scripts/office/soffice.py --headless --convert-to docx document.doc
```

### Reading Content

```bash
# Text extraction with tracked changes
pandoc --track-changes=all document.docx -o output.md

# Raw XML access
python scripts/office/unpack.py document.docx unpacked/
```

### Converting to Images

```bash
python scripts/office/soffice.py --headless --convert-to pdf document.docx
pdftoppm -jpeg -r 150 document.pdf page
```

### Accepting Tracked Changes

To produce a clean document with all tracked changes accepted (requires LibreOffice):

```bash
python scripts/accept_changes.py input.docx output.docx
```

---

## Creating New Documents

Generate .docx files with JavaScript, then validate. Install: `npm install -g docx`

### Setup
```javascript
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun,
        Header, Footer, AlignmentType, PageOrientation, LevelFormat, ExternalHyperlink,
        InternalHyperlink, Bookmark, FootnoteReferenceRun, PositionalTab,
        PositionalTabAlignment, PositionalTabRelativeTo, PositionalTabLeader,
        TabStopType, TabStopPosition, Column, SectionType,
        TableOfContents, HeadingLevel, BorderStyle, WidthType, ShadingType,
        VerticalAlign, PageNumber, PageBreak } = require('docx');

const doc = new Document({ sections: [{ children: [/* content */] }] });
Packer.toBuffer(doc).then(buffer => fs.writeFileSync("doc.docx", buffer));
```

### Validation
After creating the file, validate it. If validation fails, unpack, fix the XML, and repack.
```bash
python scripts/office/validate.py doc.docx
```

### Page Size

```javascript
// CRITICAL: docx-js defaults to A4, not US Letter
// Always set page size explicitly for consistent results
sections: [{
  properties: {
    page: {
      size: {
        width: 12240,   // 8.5 inches in DXA
        height: 15840   // 11 inches in DXA
      },
      margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } // 1 inch margins
    }
  },
  children: [/* content */]
}]
```

**Common page sizes (DXA units, 1440 DXA = 1 inch):**

| Paper | Width | Height | Content Width (1" margins) |
|-------|-------|--------|---------------------------|
| US Letter | 12,240 | 15,840 | 9,360 |
| A4 (default) | 11,906 | 16,838 | 9,026 |

**Landscape orientation:** docx-js swaps width/height internally, so pass portrait dimensions and let it handle the swap:
```javascript
size: {
  width: 12240,   // Pass SHORT edge as width
  height: 15840,  // Pass LONG edge as height
  orientation: PageOrientation.LANDSCAPE  // docx-js swaps them in the XML
},
// Content width = 15840 - left margin - right margin (uses the long edge)
```

### Styles (Override Built-in Headings)

Use Arial as the default font (universally supported). Keep titles black for readability.

```javascript
const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 24 } } }, // 12pt default
    paragraphStyles: [
      // IMPORTANT: Use exact IDs to override built-in styles
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 240, after: 240 }, outlineLevel: 0 } }, // outlineLevel required for TOC
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 180, after: 180 }, outlineLevel: 1 } },
    ]
  },
  sections: [{
    children: [
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Title")] }),
    ]
  }]
});
```

### Lists (NEVER use unicode bullets)

```javascript
// ❌ WRONG - never manually insert bullet characters
new Paragraph({ children: [new TextRun("• Item")] })  // BAD
new Paragraph({ children: [new TextRun("\u2022 Item")] })  // BAD

// ✅ CORRECT - use numbering config with LevelFormat.BULLET
const doc = new Document({
  numbering: {
    config: [
      { reference: "bullets",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "numbers",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    ]
  },
  sections: [{
    children: [
      new Paragraph({ numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Bullet item")] }),
      new Paragraph({ numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("Numbered item")] }),
    ]
  }]
});

// ⚠️ Each reference creates INDEPENDENT numbering
// Same reference = continues (1,2,3 then 4,5,6)
// Different reference = restarts (1,2,3 then 1,2,3)
```

### Tables

**CRITICAL: Tables need dual widths** - set both `columnWidths` on the table AND `width` on each cell. Without both, tables render incorrectly on some platforms.

```javascript
// CRITICAL: Always set table width for consistent rendering
// CRITICAL: Use ShadingType.CLEAR (not SOLID) to prevent black backgrounds
const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };

new Table({
  width: { size: 9360, type: WidthType.DXA }, // Always use DXA (percentages break in Google Docs)
  columnWidths: [4680, 4680], // Must sum to table width (DXA: 1440 = 1 inch)
  rows: [
    new TableRow({
      children: [
        new TableCell({
          borders,
          width: { size: 4680, type: WidthType.DXA }, // Also set on each cell
          shading: { fill: "D5E8F0", type: ShadingType.CLEAR }, // CLEAR not SOLID
          margins: { top: 80, bottom: 80, left: 120, right: 120 }, // Cell padding (internal, not added to width)
          children: [new Paragraph({ children: [new TextRun("Cell")] })]
        })
      ]
    })
  ]
})
```

**Table width calculation:**

Always use `WidthType.DXA` — `WidthType.PERCENTAGE` breaks in Google Docs.

```javascript
// Table width = sum of columnWidths = content width
// US Letter with 1" margins: 12240 - 2880 = 9360 DXA
width: { size: 9360, type: WidthType.DXA },
columnWidths: [7000, 2360]  // Must sum to table width
```

**Width rules:**
- **Always use `WidthType.DXA`** — never `WidthType.PERCENTAGE` (incompatible with Google Docs)
- Table width must equal the sum of `columnWidths`
- Cell `width` must match corresponding `columnWidth`
- Cell `margins` are internal padding - they reduce content area, not add to cell width
- For full-width tables: use content width (page width minus left and right margins)

### Images

```javascript
// CRITICAL: type parameter is REQUIRED
new Paragraph({
  children: [new ImageRun({
    type: "png", // Required: png, jpg, jpeg, gif, bmp, svg
    data: fs.readFileSync("image.png"),
    transformation: { width: 200, height: 150 },
    altText: { title: "Title", description: "Desc", name: "Name" } // All three required
  })]
})
```

### Mermaid-to-DOCX Pipeline

When source Markdown contains ` ```mermaid ``` ` code blocks, **ALWAYS** pre-process
with the `mermaid-render` skill before DOCX generation. Neither Pandoc nor docx-js
can render Mermaid natively — diagrams must be converted to PNG images first.

**3-step pipeline:**

**Step 1 — Pre-process Mermaid blocks into PNG images:**
```bash
python3 scripts/preprocess_mermaid.py input.md \
  --output-dir diagrams/ \
  --output clean.md \
  --width 1200 --scale 2 --background transparent
```
This extracts all ` ```mermaid ``` ` blocks, renders each to PNG via `mmdc`,
strips unsupported HTML tags (`<details>`, `<summary>`), and writes clean
Markdown with `![Diagram N](path.png)` image references.

**Step 2 — Generate DOCX from clean Markdown:**

Option A — docx-js with `ImageRun` embedding (programmatic control):
```javascript
const fs = require("fs");
const glob = require("glob");
const { Document, Packer, Paragraph, ImageRun, AlignmentType, TextRun } = require("docx");

const pngFiles = glob.sync("diagrams/diagram-*.png").sort();
const diagramSections = pngFiles.map((png, i) => [
  new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [new ImageRun({
      type: "png",
      data: fs.readFileSync(png),
      transformation: { width: 600, height: 400 },
      altText: {
        title: `Diagram ${i + 1}`,
        description: "Mermaid diagram",
        name: `diagram-${i + 1}`
      }
    })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: `Figure ${i + 1}`, italics: true, size: 20 })]
  })
]).flat();
```

Option B — Pandoc (simpler, uses image refs already in clean.md):
```bash
pandoc clean.md -o output.docx --reference-doc=template.docx
```

**Step 3 — Clean up temp files:**
```bash
rm -rf diagrams/*.mmd  # keep PNGs if archiving, or rm -rf diagrams/
```

> **Advanced options:** See the `mermaid-render` skill for theme selection
> (`--theme dark|forest|neutral`), batch processing, and troubleshooting
> Puppeteer/Chromium issues.

### Page Breaks

```javascript
// CRITICAL: PageBreak must be inside a Paragraph
new Paragraph({ children: [new PageBreak()] })

// Or use pageBreakBefore
new Paragraph({ pageBreakBefore: true, children: [new TextRun("New page")] })
```

### Hyperlinks

```javascript
// External link
new Paragraph({
  children: [new ExternalHyperlink({
    children: [new TextRun({ text: "Click here", style: "Hyperlink" })],
    link: "https://example.com",
  })]
})

// Internal link (bookmark + reference)
// 1. Create bookmark at destination
new Paragraph({ heading: HeadingLevel.HEADING_1, children: [
  new Bookmark({ id: "chapter1", children: [new TextRun("Chapter 1")] }),
]})
// 2. Link to it
new Paragraph({ children: [new InternalHyperlink({
  children: [new TextRun({ text: "See Chapter 1", style: "Hyperlink" })],
  anchor: "chapter1",
})]})
```

### Footnotes

```javascript
const doc = new Document({
  footnotes: {
    1: { children: [new Paragraph("Source: Annual Report 2024")] },
    2: { children: [new Paragraph("See appendix for methodology")] },
  },
  sections: [{
    children: [new Paragraph({
      children: [
        new TextRun("Revenue grew 15%"),
        new FootnoteReferenceRun(1),
        new TextRun(" using adjusted metrics"),
        new FootnoteReferenceRun(2),
      ],
    })]
  }]
});
```

### Tab Stops

```javascript
// Right-align (e.g., date opposite title)
new Paragraph({ children: [new TextRun("Company Name"), new TextRun("\tJanuary 2025")],
  tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }] })
// Dot leader (TOC-style): use PositionalTab with PositionalTabLeader.DOT
```

### Multi-Column Layouts

```javascript
sections: [{
  properties: { column: { count: 2, space: 720, equalWidth: true, separate: true } },
  children: [/* content flows across columns */]
}]
// Custom widths: equalWidth: false, children: [new Column({ width, space }), ...]
// Column break: new section with type: SectionType.NEXT_COLUMN
```

### Table of Contents

```javascript
// CRITICAL: Headings must use HeadingLevel ONLY - no custom styles
new TableOfContents("Table of Contents", { hyperlink: true, headingStyleRange: "1-3" })
```

### Headers/Footers

```javascript
sections: [{
  properties: {
    page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } // 1440 = 1 inch
  },
  headers: {
    default: new Header({ children: [new Paragraph({ children: [new TextRun("Header")] })] })
  },
  footers: {
    default: new Footer({ children: [new Paragraph({
      children: [new TextRun("Page "), new TextRun({ children: [PageNumber.CURRENT] })]
    })] })
  },
  children: [/* content */]
}]
```

### Critical Rules for docx-js

- **Page size**: Set explicitly (docx-js defaults to A4). US Letter: 12240×15840 DXA. Landscape: pass portrait dims, set `orientation: PageOrientation.LANDSCAPE`
- **Never `\n`** — use separate Paragraphs. **Never unicode bullets** — use `LevelFormat.BULLET`
- **PageBreak** must be inside a Paragraph. **ImageRun** requires `type` (png/jpg/etc)
- **Tables**: Use `WidthType.DXA` only (PERCENTAGE breaks in Google Docs). Set `columnWidths` AND cell `width`. Use `ShadingType.CLEAR`, add cell margins
- **No tables as dividers** — use Paragraph `border: { bottom: {...} }` or tab stops for two-column footers
- **TOC**: Use `HeadingLevel` only, include `outlineLevel` (0 for H1, 1 for H2). Override styles with exact IDs: "Heading1", "Heading2"

---

## Editing Existing Documents

**Follow all 3 steps in order.**

### Step 1: Unpack
```bash
python scripts/office/unpack.py document.docx unpacked/
```
Extracts XML, pretty-prints, merges adjacent runs, and converts smart quotes to XML entities (`&#x201C;` etc.) so they survive editing. Use `--merge-runs false` to skip run merging.

### Step 2: Edit XML

Edit files in `unpacked/word/`. See [references/xml-reference.md](references/xml-reference.md) for schema compliance, tracked changes, comments, and images.

**Use "Claude" as the author** for tracked changes and comments, unless the user explicitly requests use of a different name.

**Use the Edit tool directly for string replacement. Do not write Python scripts.** Scripts introduce unnecessary complexity. The Edit tool shows exactly what is being replaced.

**CRITICAL: Use smart quotes for new content.** When adding text with apostrophes or quotes, use XML entities to produce smart quotes:
```xml
<!-- Use these entities for professional typography -->
<w:t>Here&#x2019;s a quote: &#x201C;Hello&#x201D;</w:t>
```
| Entity | Character |
|--------|-----------|
| `&#x2018;` | ‘ (left single) |
| `&#x2019;` | ’ (right single / apostrophe) |
| `&#x201C;` | “ (left double) |
| `&#x201D;` | ” (right double) |

**Adding comments:** Use `comment.py` to handle boilerplate across multiple XML files (text must be pre-escaped XML):
```bash
python scripts/comment.py unpacked/ 0 "Comment text with &amp; and &#x2019;"
python scripts/comment.py unpacked/ 1 "Reply text" --parent 0  # reply to comment 0
python scripts/comment.py unpacked/ 0 "Text" --author "Custom Author"  # custom author name
```
Then add markers to document.xml (see [references/xml-reference.md](references/xml-reference.md)#comments).

### Step 3: Pack
```bash
python scripts/office/pack.py unpacked/ output.docx --original document.docx
```
Validates with auto-repair, condenses XML, and creates DOCX. Use `--validate false` to skip.

**Auto-repair will fix:**
- `durableId` >= 0x7FFFFFFF (regenerates valid ID)
- Missing `xml:space="preserve"` on `<w:t>` with whitespace

**Auto-repair won't fix:**
- Malformed XML, invalid element nesting, missing relationships, schema violations

### Common Pitfalls

- **Replace entire `<w:r>` elements**: When adding tracked changes, replace the whole `<w:r>...</w:r>` block with `<w:del>...<w:ins>...` as siblings. Don't inject tracked change tags inside a run.
- **Preserve `<w:rPr>` formatting**: Copy the original run's `<w:rPr>` block into your tracked change runs to maintain bold, font size, etc.

---

## XML Reference

See [references/xml-reference.md](references/xml-reference.md) for schema compliance, tracked changes (insertions, deletions, minimal edits, paragraph deletion, rejecting/restoring changes), comments, and images.

---

## Examples

**Create a simple report with headings and table:**
```javascript
const doc = new Document({
  styles: { /* override Heading1, Heading2 */ },
  sections: [{
    children: [
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Report Title")] }),
      new Paragraph({ children: [new TextRun("Summary text.")] }),
      new Table({ /* columnWidths, rows */ })
    ]
  }]
});
```

**Edit existing document (tracked change):** Unpack → edit `unpacked/word/document.xml` using patterns from [references/xml-reference.md](references/xml-reference.md) → pack.

---

## Korean Style Guide (한글 DOCX)

When producing Korean DOCX documents, apply this pipeline for professional formatting.
Pandoc's default styling is insufficient for Korean — always post-process with `python-docx`.

### Design Tokens

| Token | Value |
|-------|-------|
| Page size | A4 (21.0 × 29.7 cm) |
| Margins | 2.54 cm all sides |
| Body font | 맑은 고딕 (Malgun Gothic) 10pt |
| Heading font | 맑은 고딕 Bold, color `#1A3C6E` |
| Code font | D2Coding 9pt (fallback: Consolas) |
| Body color | `#333333` |
| Code background | `#F0F0F0` |
| Table header BG | `#1A3C6E` (white text) |
| Zebra stripe BG | `#F8F9FA` |
| Line spacing | 1.15 |

### Heading Sizes

| Level | Size | Space Before | Space After |
|-------|------|-------------|-------------|
| H1 | 18pt | 24pt | 12pt |
| H2 | 14pt | 18pt | 8pt |
| H3 | 12pt | 14pt | 6pt |
| H4 | 11pt | 10pt | 4pt |

### Reference Document Generator

Generate a `korean-reference.docx` for Pandoc's `--reference-doc`:

```python
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

doc = Document()

for section in doc.sections:
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(2.54)
    section.right_margin = Cm(2.54)

FONT_KR = '맑은 고딕'
COLOR_HEADING = RGBColor(0x1A, 0x3C, 0x6E)
COLOR_BODY = RGBColor(0x33, 0x33, 0x33)

def set_font(style, name, size, bold=False, color=None):
    font = style.font
    font.name = name
    font.size = Pt(size) if size else None
    font.bold = bold
    if color:
        font.color.rgb = color
    rpr = style.element.get_or_add_rPr()
    ea = rpr.find(qn('w:rFonts'))
    if ea is None:
        ea = parse_xml(f'<w:rFonts {nsdecls("w")} w:eastAsia="{name}"/>')
        rpr.insert(0, ea)
    else:
        ea.set(qn('w:eastAsia'), name)

set_font(doc.styles['Normal'], FONT_KR, 10, color=COLOR_BODY)
doc.styles['Normal'].paragraph_format.space_after = Pt(4)
doc.styles['Normal'].paragraph_format.line_spacing = 1.15

for name, size, sb, sa in [
    ('Heading 1', 18, 24, 12), ('Heading 2', 14, 18, 8),
    ('Heading 3', 12, 14, 6),  ('Heading 4', 11, 10, 4),
]:
    s = doc.styles[name]
    set_font(s, FONT_KR, size, bold=True, color=COLOR_HEADING)
    s.paragraph_format.space_before = Pt(sb)
    s.paragraph_format.space_after = Pt(sa)

doc.add_heading('Heading 1', level=1)
doc.add_heading('Heading 2', level=2)
doc.add_paragraph('Normal paragraph text.')
doc.save('korean-reference.docx')
```

### Post-Processing Helpers (python-docx)

These functions are used in the Pandoc post-processing step (see `pandoc` skill Mode 8).

```python
from docx.shared import Pt, Cm, RGBColor
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

FONT_KR = '맑은 고딕'
FONT_CODE = 'D2Coding'
FONT_CODE_FB = 'Consolas'
COLOR_BODY = RGBColor(0x33, 0x33, 0x33)
COLOR_HEADING = RGBColor(0x1A, 0x3C, 0x6E)
CODE_BG = 'F0F0F0'

# Pandoc syntax-highlight character styles
TOKEN_STYLES = {
    'AttributeTok', 'FunctionTok', 'KeywordTok', 'NormalTok',
    'StringTok', 'DataTypeTok', 'CommentTok', 'OtherTok', 'DecValTok',
    'BuiltInTok', 'OperatorTok', 'ControlFlowTok', 'VariableTok',
    'BaseNTok', 'FloatTok', 'ConstantTok', 'CharTok', 'SpecialCharTok',
    'SpecialStringTok', 'ImportTok', 'DocumentationTok', 'AnnotationTok',
    'PreprocessorTok', 'InformationTok', 'WarningTok', 'AlertTok',
    'ErrorTok', 'RegionMarkerTok',
}

def set_run_font_kr(run, name, size, color, bold=False):
    """Set Korean-compatible font on a run (body/heading text)."""
    run.font.name = name
    run.font.size = Pt(size)
    run.font.color.rgb = color
    run.font.bold = bold
    rpr = run._element.get_or_add_rPr()
    ea = rpr.find(qn('w:rFonts'))
    if ea is None:
        ea = parse_xml(f'<w:rFonts {nsdecls("w")} w:eastAsia="{name}"/>')
        rpr.insert(0, ea)
    else:
        ea.set(qn('w:eastAsia'), name)

def set_run_code_font(run):
    """Set monospace font on a code run."""
    run.font.name = FONT_CODE
    run.font.size = Pt(9)
    rpr = run._element.get_or_add_rPr()
    ea = rpr.find(qn('w:rFonts'))
    if ea is None:
        ea = parse_xml(
            f'<w:rFonts {nsdecls("w")} w:eastAsia="{FONT_CODE}" '
            f'w:hAnsi="{FONT_CODE}" w:cs="{FONT_CODE_FB}"/>'
        )
        rpr.insert(0, ea)
    else:
        ea.set(qn('w:eastAsia'), FONT_CODE)
        ea.set(qn('w:hAnsi'), FONT_CODE)
        ea.set(qn('w:cs'), FONT_CODE_FB)

def add_para_shading(para, hex_color):
    """Add background shading to an entire paragraph."""
    ppr = para._element.get_or_add_pPr()
    shd = ppr.find(qn('w:shd'))
    if shd is not None:
        ppr.remove(shd)
    shd = parse_xml(
        f'<w:shd {nsdecls("w")} w:val="clear" w:color="auto" w:fill="{hex_color}"/>'
    )
    ppr.append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    """Set cell padding in DXA units (80 DXA ≈ 1.4mm, 120 DXA ≈ 2.1mm)."""
    tc = cell._element
    tcPr = tc.find(qn('w:tcPr'))
    if tcPr is None:
        tcPr = parse_xml(f'<w:tcPr {nsdecls("w")}/>')
        tc.insert(0, tcPr)
    mar = tcPr.find(qn('w:tcMar'))
    if mar is not None:
        tcPr.remove(mar)
    mar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:start w:w="{left}" w:type="dxa"/>'
        f'<w:end w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(mar)

def set_cell_shading(cell, hex_color):
    """Set cell background color."""
    tc = cell._element
    tcPr = tc.find(qn('w:tcPr'))
    if tcPr is None:
        tcPr = parse_xml(f'<w:tcPr {nsdecls("w")}/>')
        tc.insert(0, tcPr)
    shd = tcPr.find(qn('w:shd'))
    if shd is not None:
        tcPr.remove(shd)
    shd = parse_xml(
        f'<w:shd {nsdecls("w")} w:val="clear" w:color="auto" w:fill="{hex_color}"/>'
    )
    tcPr.append(shd)

def set_table_borders(table, color='999999', size='4'):
    """Apply uniform borders to a table."""
    tbl = table._element
    tblPr = tbl.find(qn('w:tblPr'))
    if tblPr is None:
        tblPr = parse_xml(f'<w:tblPr {nsdecls("w")}/>')
        tbl.insert(0, tblPr)
    borders = tblPr.find(qn('w:tblBorders'))
    if borders is not None:
        tblPr.remove(borders)
    border_xml = f'<w:tblBorders {nsdecls("w")}>'
    for side in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        border_xml += (
            f'<w:{side} w:val="single" w:sz="{size}" '
            f'w:space="0" w:color="{color}"/>'
        )
    border_xml += '</w:tblBorders>'
    tblPr.append(parse_xml(border_xml))

def is_code_para(para):
    """Detect code paragraphs by Pandoc's *Tok character styles."""
    for run in para.runs:
        if run.style and run.style.name in TOKEN_STYLES:
            return True
    return False
```

### Full Post-Processing Pipeline

```python
from docx import Document

doc = Document("output.docx")

# A4 page setup
for section in doc.sections:
    from docx.shared import Cm
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(2.54)
    section.right_margin = Cm(2.54)

HEADING_SIZES = {'Heading 1': 18, 'Heading 2': 14, 'Heading 3': 12, 'Heading 4': 11}

for para in doc.paragraphs:
    sn = para.style.name if para.style else ''
    if is_code_para(para):
        add_para_shading(para, CODE_BG)
        for run in para.runs:
            set_run_code_font(run)
    elif sn in HEADING_SIZES:
        for run in para.runs:
            set_run_font_kr(run, FONT_KR, HEADING_SIZES[sn], COLOR_HEADING, bold=True)
    else:
        for run in para.runs:
            set_run_font_kr(run, FONT_KR, 10, COLOR_BODY)

for table in doc.tables:
    set_table_borders(table)
    for row_idx, row in enumerate(table.rows):
        for cell in row.cells:
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            if row_idx == 0:
                set_cell_shading(cell, '1A3C6E')
                for p in cell.paragraphs:
                    for r in p.runs:
                        set_run_font_kr(r, FONT_KR, 9, RGBColor(0xFF, 0xFF, 0xFF), bold=True)
            elif row_idx % 2 == 0:
                set_cell_shading(cell, 'F8F9FA')

doc.save("output.docx")
```

### Key Points

- **`w:eastAsia` font attribute** is required for Korean glyphs to render correctly in
  Word; set it on every run that may contain Korean text.
- **Pandoc code blocks** use character-level `*Tok` styles (`KeywordTok`, `StringTok`,
  etc.) — there is no paragraph-level `Source Code` style. Detect code paragraphs by
  checking if any run uses a `*Tok` style.
- **Table cell margins** use DXA units (80 DXA ≈ 1.4mm, 120 DXA ≈ 2.1mm).
- **Combine with Mermaid pipeline** (see "Creating New Documents > Mermaid Diagram
  Embedding") for diagrams in Korean documents.
- See the `pandoc` skill "Mode 8: Korean DOCX Pipeline" for the complete two-stage
  workflow (Pandoc + post-processing).

---

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| Validation fails after pack | Malformed XML, invalid nesting | Run `scripts/office/validate.py`; fix reported errors in unpacked XML |
| Black table backgrounds | `ShadingType.SOLID` | Use `ShadingType.CLEAR` |
| Table renders wrong in Google Docs | `WidthType.PERCENTAGE` | Use `WidthType.DXA` only |
| Empty paragraph after accepting changes | Missing `<w:del/>` in paragraph mark | Add `<w:del/>` inside `<w:pPr><w:rPr>` when deleting entire paragraph |
| Smart quotes lost after edit | Plain ASCII quotes in new text | Use XML entities: `&#x2019;` (apostrophe), `&#x201C;`/`&#x201D;` (quotes) |
| `durableId` validation error | ID >= 0x7FFFFFFF | Auto-repair in pack regenerates; or fix manually in XML |

---

## Output Discipline

- Do not add sections, chapters, or formatting elements beyond what was requested
- Do not pad documents with placeholder text ("[TBD]", "[Insert here]") or generic boilerplate
- Match document length to content depth — a 2-page topic does not need 10 pages
- Try the simplest document structure first; add complexity only when content requires it
- Three paragraphs of substance are better than ten pages of filler

## Verification

Before returning any generated or edited .docx file, verify it:

1. **Validate**: Run `python scripts/office/validate.py <output.docx>` — must pass without errors
2. **Content check**: Run `pandoc <output.docx> -o /dev/stdout --to plain | head -50` — confirm headings, sections, and key content are present
3. **Visual check** (for complex documents): Convert to images and inspect layout

```text
### Check: Document validation
**Command run:** `python scripts/office/validate.py output.docx`
**Output observed:** [paste actual output]
**Result:** PASS or FAIL
```

Report outcomes faithfully. If validation fails, say so with the error output. Never claim "document created successfully" without running validation.

## Honest Reporting

- If a step fails (validation error, XML corruption, missing dependency), report it with the relevant output
- Never claim "document created successfully" when validation shows errors
- If LibreOffice conversion fails, report the failure — do not silently skip the step
- When a check passes, state it plainly without unnecessary hedging

---

## Dependencies

- **pandoc**: Text extraction
- **docx**: `npm install -g docx` (new documents)
- **LibreOffice**: PDF conversion (auto-configured for sandboxed environments via `scripts/office/soffice.py`)
- **Poppler**: `pdftoppm` for images
