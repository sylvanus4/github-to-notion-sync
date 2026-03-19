# DOCX Style Guide

Formatting conventions and visual standards for Word document creation. Load this file alongside `assets/templates/document-structure.md` when creating new documents.

## Font Standards

| Context | Font | Size |
|---------|------|------|
| Default body | Arial | 12pt (size: 24 in docx-js half-points) |
| Heading 1 | Arial Bold | 16pt (size: 32) |
| Heading 2 | Arial Bold | 14pt (size: 28) |
| Heading 3 | Arial Bold | 12pt (size: 24) |
| Code blocks | Consolas / Courier New | 9pt, light gray background |
| Captions | Arial Italic | 10pt, muted gray |

**Rationale:** Arial is universally supported across platforms. Keep headings black for readability.

## Heading Style Overrides

Override built-in Word styles using exact IDs for TOC compatibility:

```javascript
paragraphStyles: [
  { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
    run: { size: 32, bold: true, font: "Arial" },
    paragraph: { spacing: { before: 240, after: 240 }, outlineLevel: 0 } },
  { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
    run: { size: 28, bold: true, font: "Arial" },
    paragraph: { spacing: { before: 180, after: 180 }, outlineLevel: 1 } },
]
```

`outlineLevel` is required for TOC generation.

## Spacing Standards

| Element | Value |
|---------|-------|
| Line spacing | 1.15 |
| Paragraph spacing (after) | 6pt |
| Heading 1 spacing (before/after) | 240 twips (12pt) |
| Heading 2 spacing (before/after) | 180 twips (9pt) |
| Cell padding | top/bottom: 80 twips, left/right: 120 twips |

## Color Conventions

| Element | Color | Usage |
|---------|-------|-------|
| Table header background | `D5E8F0` (light blue) | Always use `ShadingType.CLEAR` |
| Table borders | `CCCCCC` (light gray) | `BorderStyle.SINGLE`, size: 1 |
| Body text | Black (default) | No explicit color needed |
| Accent/highlight | Context-dependent | Match document purpose |

## Table Rules

- **Always use `WidthType.DXA`** — `WidthType.PERCENTAGE` breaks in Google Docs
- Table width must equal the sum of `columnWidths`
- Cell `width` must match corresponding `columnWidth`
- Cell `margins` are internal padding — they reduce content area, not add to cell width
- Full-width tables: use content width (page width minus left + right margins)

## Lists

- **NEVER use unicode bullets** — always use `LevelFormat.BULLET` with numbering config
- Each `reference` creates independent numbering; same reference continues count
- Indent: `left: 720, hanging: 360` for standard list indentation

## Smart Typography

| Entity | Character | Usage |
|--------|-----------|-------|
| `&#x2018;` | ' (left single quote) | Opening single quote |
| `&#x2019;` | ' (right single / apostrophe) | Closing single quote, apostrophes |
| `&#x201C;` | " (left double quote) | Opening double quote |
| `&#x201D;` | " (right double quote) | Closing double quote |
