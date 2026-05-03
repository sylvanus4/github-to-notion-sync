---
name: rhwp-debug
description: >-
  Debug HWP/HWPX document rendering and structure issues using the rhwp CLI's
  diagnostic tools. Supports IR dump, IR diff (HWP vs HWPX comparison), debug
  overlay SVG export, and page layout analysis with a systematic 3-step
  debugging workflow. Use when the user asks to "debug HWP", "HWP 디버그",
  "inspect HWP structure", "compare HWP formats", "HWP IR diff", "rhwp-debug",
  "HWP 렌더링 문제", "HWP 구조 분석", or encounters rendering issues in HWP documents.
  Do NOT use for simple viewing (use rhwp-viewer). Do NOT use for format
  conversion (use rhwp-converter). Do NOT use for installing rhwp (use
  rhwp-setup).
---

# rhwp Debug — HWP/HWPX Document Debugging

Systematically debug HWP/HWPX document rendering and structure issues using
the rhwp CLI's diagnostic tools: IR dump, IR diff, debug overlay, and page
layout analysis.

## Input

- Path to the HWP/HWPX file with the issue
- Optional: section number, paragraph number, page number
- Optional: second file for IR diff comparison

## Workflow

### Step 1: Verify CLI

```bash
rhwp --help > /dev/null 2>&1 || { echo "ERROR: rhwp CLI not found. Run /rhwp-setup first."; exit 1; }
```

### Step 2: Systematic Debugging (3-Step Process)

Follow the rhwp project's recommended debugging workflow:

#### Step 2a: Debug Overlay — Identify Problem Area

Render the document with paragraph and table boundary overlays:

```bash
mkdir -p /tmp/rhwp-debug
rhwp export-svg "<FILE_PATH>" --debug-overlay -o /tmp/rhwp-debug/
echo "Debug overlay SVGs: /tmp/rhwp-debug/"
```

Open the SVGs and identify which paragraphs or tables show rendering issues.
Each element gets a colored boundary rectangle with labels:
- Paragraphs: `s{section}:pi={index} y={coord}`
- Tables: `s{section}:pi={index} ci={control} {rows}x{cols} y={coord}`

Use the `pi=` index to cross-reference with `dump` commands in Step 2c.

#### Step 2b: Page Layout Dump — Check Layout

Inspect the page layout to understand positioning:

```bash
# Dump layout for the problematic page (0-indexed)
rhwp dump-pages "<FILE_PATH>" -p <PAGE_NUMBER>
```

This reveals paragraph positions, column layout, table cell coordinates,
and text flow direction for the specified page. All coordinates use HWPUNIT
(1 inch = 7,200 HWPUNIT ≈ 0.00353 mm).

#### Step 2c: IR Dump — Inspect Properties

Deep-inspect the specific paragraph or table:

```bash
# Dump a specific section and paragraph
rhwp dump "<FILE_PATH>" -s <SECTION> -p <PARAGRAPH>

# Dump an entire section
rhwp dump "<FILE_PATH>" -s <SECTION>
```

Key properties to check:
- **ParaShape**: paragraph spacing, alignment, indentation
- **LINE_SEG**: line segment positions and heights
- **CharShape**: font, size, color, bold/italic
- **Table properties**: cell merges, borders, padding

### Step 3: IR Diff — Compare HWP vs HWPX (Optional)

Compare the intermediate representation of two versions of the same document
(e.g., HWP binary vs HWPX XML):

```bash
# Full comparison
rhwp ir-diff "<FILE_A>" "<FILE_B>"

# The output highlights structural differences between the two formats
```

Common use case: verify that HWPX conversion preserves all document properties.

### Step 4: File Info & Conversion Debugging

Quick summary of document metadata:

```bash
rhwp info "<FILE_PATH>"
```

For conversion comparisons:

```bash
rhwp ir-diff original.hwpx converted.hwp
rhwp dump original.hwpx -s 0 -p 0
rhwp dump converted.hwp -s 0 -p 0
```

### Step 5: Report Findings

Summarize the debugging session:

| Finding | Section/Page | Detail |
|---------|-------------|--------|
| Layout issue | Page N, Section M | Paragraph overlap at coordinates... |
| Property mismatch | S:0 P:5 | LINE_SEG height differs between versions |
| Table rendering | Page 2 | Cell merge not preserved in HWPX |

## Quick Reference

```bash
# 0. Quick info
rhwp info doc.hwp

# 1. Visual overlay (Step 1 of 3)
rhwp export-svg doc.hwp --debug-overlay -o /tmp/debug/

# 2. Page layout (Step 2 of 3)
rhwp dump-pages doc.hwp -p 5

# 3. Paragraph details (Step 3 of 3)
rhwp dump doc.hwp -s 2 -p 45

# 4. Format comparison
rhwp ir-diff doc.hwpx doc.hwp
```

## Examples

### Text Overlap Investigation

User: "HWP 문서에서 텍스트가 겹쳐 보여"

```bash
rhwp dump-pages doc.hwp -p 3    # page 3의 라인 위치 확인
rhwp dump doc.hwp -s 0 -p 12    # 겹침 의심 paragraph의 CharShape 확인
```

→ `lineSpacing` 값이 `-1`(단위 무시)인 경우 발견 → 원본 HWP에서 줄간격 수정 후 재변환.

### IR Diff for Format Migration

User: "HWPX에서 HWP로 변환했는데 차이가 있는지 확인해줘"

```bash
rhwp ir-diff original.hwpx converted.hwp
```

→ diff 출력에서 누락된 section/paragraph 식별 가능.

## Troubleshooting

| Issue | Diagnostic Command |
|-------|--------------------|
| Text overlapping | `dump-pages -p N` to check line positions |
| Missing content | `dump -s N` to verify paragraph count |
| Table misalignment | `dump -s N -p M` to check table cell properties |
| Font rendering | `dump -s N -p M` to verify CharShape settings |
| Format conversion loss | `ir-diff original.hwpx converted.hwp` |
