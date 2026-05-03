---
name: rhwp-viewer
description: >-
  View and inspect HWP/HWPX documents using the rhwp toolkit. Opens files in
  the Cursor IDE via the VS Code custom editor extension, or uses the CLI for
  SVG rendering, page layout inspection, and structure dumps. Use when the
  user asks to "view HWP", "open HWP", "inspect HWP", "HWP 열기", "HWP 보기", "HWP
  구조 확인", "rhwp-viewer", or wants to visually examine or inspect the structure
  of an HWP document. Do NOT use for converting HWP to other formats for
  pipeline use (use rhwp-converter). Do NOT use for systematic debugging with
  ir-diff (use rhwp-debug). Do NOT use for installing rhwp (use rhwp-setup).
---

# rhwp Viewer — HWP/HWPX Document Viewing and Inspection

View HWP/HWPX documents inside the Cursor IDE or inspect their structure via
the CLI. Supports visual rendering, page layout analysis, and paragraph-level
structure dumps.

## Input

The user provides a path to an `.hwp` or `.hwpx` file.

## Workflow

### Step 1: Verify rhwp is Installed

```bash
rhwp --help > /dev/null 2>&1 || echo "ERROR: rhwp CLI not found. Run /rhwp-setup first."
```

### Step 2: Choose Viewing Mode

Ask the user which mode to use (or infer from context):

| Mode | When to Use | Tool |
|------|-------------|------|
| IDE Viewer | Visual viewing inside Cursor | VS Code extension |
| SVG Render | Render pages as SVG images | `rhwp export-svg` |
| Page Layout | Inspect page layout and paragraph positions | `rhwp dump-pages` |
| Structure Dump | Inspect paragraph shapes, LINE_SEG, properties | `rhwp dump` |
| Debug Overlay | Visualize paragraph and table boundaries | `rhwp export-svg --debug-overlay` |

### Step 3a: IDE Viewer Mode

Open the file in Cursor. The `rhwp-vscode` extension automatically handles
`.hwp` and `.hwpx` files with its custom editor:

```bash
cursor "<FILE_PATH>"
```

If Cursor CLI is not available:

```bash
code "<FILE_PATH>"
```

The custom editor renders the HWP document using WASM in a webview panel with:
- Canvas 2D high-quality rendering
- Virtual scroll (large document support)
- Zoom in/out (Ctrl+mouse wheel or status bar buttons)
- Page navigation (current page shown in status bar)

### Step 3b: SVG Render Mode

Render all pages (or specific pages) as SVG:

```bash
# All pages
rhwp export-svg "<FILE_PATH>" -o output/

# Specific page (0-indexed)
rhwp export-svg "<FILE_PATH>" -p 0 -o output/
```

Open the resulting SVG in a browser or viewer for visual inspection.

### Step 3c: Page Layout Mode

Inspect the layout of a specific page:

```bash
# Dump page layout (0-indexed page number)
rhwp dump-pages "<FILE_PATH>" -p 0
```

This shows paragraph positions, table boundaries, and text flow for the given
page. Useful for understanding how the document is laid out.

### Step 3d: Structure Dump Mode

Deep-inspect a specific section and paragraph:

```bash
# Dump section 0, paragraph 0
rhwp dump "<FILE_PATH>" -s 0 -p 0

# Dump all paragraphs in section 0
rhwp dump "<FILE_PATH>" -s 0
```

Output includes ParaShape, LINE_SEG, CharShape, table properties, and other
internal HWP data structures.

### Step 3e: Debug Overlay Mode

Render SVG with colored overlays showing paragraph and table boundaries:

```bash
rhwp export-svg "<FILE_PATH>" --debug-overlay -o output/
```

Each paragraph and table cell gets a colored rectangle overlay with labels:
- Paragraphs: `s{section}:pi={index} y={coord}`
- Tables: `s{section}:pi={index} ci={control} {rows}x{cols} y={coord}`

### Step 3f: File Info Mode

Get a quick summary of the document:

```bash
rhwp info "<FILE_PATH>"
```

Output includes file size, HWP version, section count, and font list.

### Step 4: Report Results

For CLI modes, report:
- Number of pages in the document
- File format (HWP binary vs HWPX XML)
- Output file locations (for SVG mode)
- Key structural observations (for dump modes)

## Examples

### Quick Document Preview

User: "이 HWP 파일 내용 보여줘"

```bash
rhwp info doc.hwp                     # 기본 정보 확인
rhwp export-svg doc.hwp -o /tmp/view/ # 전체 페이지 렌더링
open /tmp/view/page-001.svg           # 첫 페이지 미리보기
```

### Layout Debugging

User: "5페이지 레이아웃이 이상해"

```bash
rhwp dump-pages doc.hwp -p 5          # 페이지 5의 라인/테이블 좌표
# → 겹침이나 잘림이 있는 요소 좌표 확인
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `rhwp` CLI not found | Run `/rhwp-setup` to install |
| SVG renders blank page | Verify file is valid: `rhwp info <file>` |
| Debug overlay not visible | Use `--debug-overlay` flag with `export-svg` |
| Dump output unreadable | Pipe to `less` or redirect: `rhwp dump doc.hwp > dump.txt` |

## Quick Reference

```bash
# File info
rhwp info doc.hwp

# Visual render
rhwp export-svg doc.hwp -o output/

# Page layout for page 5
rhwp dump-pages doc.hwp -p 5

# Structure of section 2, paragraph 10
rhwp dump doc.hwp -s 2 -p 10

# Debug overlay
rhwp export-svg doc.hwp --debug-overlay -o output/
```
