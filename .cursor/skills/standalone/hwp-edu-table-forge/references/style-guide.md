# Korean Education Table Style Guide

Formatting rules for tables used by Korean elementary school teachers.
All rules target A4 print output and are compatible with both DOCX and HWP formats.

---

## 1. Page Layout

| Property | Value |
|---|---|
| Paper size | A4 (210 × 297mm) |
| Orientation | Portrait (default); Landscape permitted for timetables or wide tables |
| Top margin | 20mm |
| Bottom margin | 20mm |
| Left margin | 20mm |
| Right margin | 20mm |
| Usable width | 170mm (portrait) / 257mm (landscape) |
| Header/footer | 15mm reserved if school letterhead is needed |

---

## 2. Typography

### Font Family

| Priority | Font | Fallback |
|---|---|---|
| 1 | 맑은 고딕 (Malgun Gothic) | Primary for all text |
| 2 | 함초롬돋움 (HCR Dotum) | HWP-native fallback |
| 3 | 나눔고딕 (NanumGothic) | Web/cross-platform fallback |

### Font Sizes

| Element | Size | Weight | Alignment |
|---|---|---|---|
| Document title | 14pt | Bold | Center |
| Table title (`<표 N>`) | 11pt | Bold | Left |
| Table header cells | 10-11pt | Bold | Center |
| Table body cells | 9-10pt | Regular | Left (text) / Center (numbers, symbols) |
| Table footnotes | 8pt | Regular | Left |
| Source citations | 8pt | Italic | Right |

### Line Spacing

| Context | Value |
|---|---|
| Body text (in cells) | 1.3x (130%) — generous spacing for clean look |
| Paragraph spacing in cells | 0pt before, 3pt after |
| Between table title and table | 6pt |
| Between table and footnote | 4pt |

Target a "breathing" feel: 1.2-1.5x line spacing prevents cramped cells.

---

## 3. Table Structure

### Border Rules — Korean Teacher Style

The guiding principle is **"sections, not boxes"**: thick outer frame, clear horizontal
dividers, and minimal vertical lines so the table reads as structured layout rather
than a spreadsheet grid.

| Border type | Thickness | Color | Notes |
|---|---|---|---|
| Outer border (top, bottom, left, right) | 1.5pt (12 half-pt) | Black (#000000) | Frames the entire table |
| Header bottom separator | 1.0pt (8 half-pt) | Black (#000000) | Visually anchors header |
| Inner horizontal lines | 0.5pt (4 half-pt) | Gray (#808080) | Row separation |
| Inner vertical lines | 0.25pt (2 half-pt) | Light gray (#BFBFBF) | Deliberately thinner than H-lines |

**Vertical line minimization**: Where a merged first-column label cell spans
multiple rows, the vertical border between label and content should be the only
prominent vertical divider; other vertical lines within the content area use the
thinnest weight or are omitted entirely.

### Cell Padding (Korean Teacher Style)

Generous margins prevent the "cramped spreadsheet" feel. Target 0.2-0.3cm per side.

| Direction | Value | Notes |
|---|---|---|
| Top | 6pt (0.21cm / 2.1mm) | Generous vertical breathing room |
| Bottom | 6pt (0.21cm / 2.1mm) | Matches top for symmetry |
| Left | 8pt (0.28cm / 2.8mm) | Comfortable text start offset |
| Right | 8pt (0.28cm / 2.8mm) | Matches left |

In `python-docx`: set via `cell.paragraphs[0].paragraph_format` plus
`tc.tcPr` cell margin overrides (top/bottom/left/right in EMU).

### Column Width Guidelines

- All column widths must sum to exactly 170mm (portrait) or 257mm (landscape)
- Minimum column width: 10mm (for narrow number/symbol columns)
- Maximum single column width: 80mm (readability limit)
- Proportional distribution: wider columns for text content, narrower for numbers

### Row Height

- Minimum row height: 7mm (ensures readability at 9pt font)
- Header rows: 8-10mm
- Auto-height: preferred for body rows with variable content length

---

## 4. Header Formatting

### Header Row Shading — Korean Teacher Style

| Property | Value | Notes |
|---|---|---|
| Background color | #F2F2F2 (light gray) | Subtle, professional — no saturated colors |
| Text color | #000000 (black) | |
| Font weight | Bold | Key visual anchor for header |
| Font size | 10-11pt (1pt larger than body) | Slight size bump reinforces hierarchy |
| Text alignment | Center (both H and V) | Headers are always centered |
| Vertical alignment | Center | |

The header row is one of the **Three Key Differentiators** of Korean teacher-style
tables — it must be visually distinct via shading + bold + size, not via heavy borders.

### Multi-Level Headers

Maximum 2 levels of header hierarchy:

```
┌─────────────────────────────┬──────────┐
│     교수·학습 활동 (L1)      │ 자료 및  │
├──────────────┬──────────────┤ 유의점   │
│ 교사 활동 (L2)│ 학생 활동 (L2)│  (L1)    │
├──────────────┼──────────────┼──────────┤
```

- Level 1 headers: merge across child columns
- Level 2 headers: individual column headers
- Both levels use the same #F2F2F2 shading and bold text

### Header Text Rules

- Use concise labels (2-6 Korean characters preferred)
- Include parenthetical English only for commonly bilingual terms
- Standard abbreviations: 번호→No., 비고→Notes

---

## 5. Cell Content Formatting — Korean Teacher Style

### Alignment Rules (Critical Differentiator)

| Content type | Horizontal | Vertical | Notes |
|---|---|---|---|
| Header text | Center | Center | Always — no exceptions |
| Row labels (first column) | Center or Left | Center | Bold when acting as category label |
| Prose / descriptions | Left | Top (if multi-line) | Left-aligned with generous padding |
| Numbers / scores / percentages | Right | Center | Aligns decimal points visually |
| Dates, short codes | Center | Center | |
| Symbols (○, △, ×, ✓) | Center | Center | |

**Minimize alignment mixing within a column** — if 80%+ of a column is numbers,
right-align the entire column including occasional text cells.

### Empty Cells

- Use `—` (em dash) for intentionally empty cells
- Use blank for cells to be filled later by the teacher
- Never leave structural cells (headers, labels) empty

### Symbols and Marks

| Symbol | Meaning | Context |
|---|---|---|
| ○ | Completed / Positive | Progress tracking |
| △ | Partial / Moderate | Observation records |
| × | Not done / Negative | Progress tracking |
| ◈ | Materials indicator | Lesson plan materials column |
| ※ | Caution/Note indicator | Lesson plan notes column |
| ✓ | Check mark | Completion column |
| ☆ | Special/Excellent | Recognition |

### Number Formatting

- Period numbers: Arabic numerals (1, 2, 3...)
- Month: Arabic numerals without leading zero (3, 4, 5...)
- Dates: YYYY.MM.DD or MM/DD
- Percentages: include % symbol (e.g., 30%)
- Scores: right-aligned with consistent decimal places

---

## 6. Table Numbering and Titles

### Numbering Convention

```
<표 1> 3학년 1학기 국어 교과 진도표
```

- Format: `<표 N> 제목`
- Angular brackets `< >` are required per Korean academic convention
- Numbering is sequential within the document
- Title placed above the table, left-aligned, 11pt bold

### Title Content

Include enough context for standalone comprehension:
- Subject, grade, semester (if applicable)
- Time period or scope
- Purpose of the table

### Source Citations (below table)

```
출처: 2022 개정 교육과정 국어과 성취기준 (교육부, 2022)
```

- Placed below the table, right-aligned, 8pt italic
- Required when referencing NCIC standards or external data

---

## 7. Color Usage — Korean Teacher Style

### Core Principle: White + Gray + Black

Korean teacher-style tables achieve visual hierarchy through **structure** (borders,
merging, alignment) rather than color. The palette is intentionally monotone.

### Permitted Colors

| Purpose | Color | Hex | Usage |
|---|---|---|---|
| Header background | Light gray | #F2F2F2 | All header rows — the primary differentiator |
| First-column label background | Very light gray | #F9F9F9 | Optional — subtle emphasis on row labels |
| Body cell background | White | #FFFFFF | Default for all body cells |
| Text color | Black | #000000 | All text, always |

### Prohibited / Discouraged

| Pattern | Status | Alternative |
|---|---|---|
| Saturated color backgrounds | **Prohibited** | Use gray shading only |
| Phase-specific colors (blue, green, yellow) | **Discouraged** | Use text labels (도입/전개/정리) instead |
| Alternate row shading (zebra stripes) | **Discouraged** | Use horizontal lines for row separation |
| Color to encode meaning | **Prohibited** | Use symbols (○, △, ×) or text |

### Color Rules

1. Maximum 2 distinct background colors per table (header gray + white)
2. Tables must be 100% readable in grayscale print without information loss
3. If phase indicators are absolutely needed, use the lightest possible pastel and
   add a text label — never rely on color alone

---

## 8. Cell Merging Rules — Korean Teacher Style

### Core Principle: "Table = Layout"

Cell merging is the **primary structural tool** in Korean teacher-style tables.
It transforms flat grids into hierarchical, document-like layouts where the first
column acts as a section label spanning multiple content rows.

### First-Column Emphasis (Key Differentiator)

The first column is the **structural backbone** of the table:

| Pattern | Description | Example |
|---|---|---|
| Category span | First-column cell spans 3-5 rows, labeling a logical group | "수업 전개" spanning activity rows |
| Section divider | Merged first-column cell with bold text acts as section header | "평가 계획" as a section |
| Hierarchy nesting | First column merged for parent, second column for sub-categories | 단원 > 차시 > 활동 |

### Permitted Merges

| Merge Type | When to Use |
|---|---|
| Vertical merge (first column) | **Always** — group rows sharing a category (month, phase, unit) |
| Vertical merge (other columns) | Sparingly — only when content genuinely spans rows |
| Horizontal merge | Multi-level headers; full-width content rows (objectives, notes) |
| Block merge (both) | Document info block (lesson plan header section) |

### Merge Constraints

1. Never merge body cells across unrelated columns
2. Merged cells must have centered text (both H and V), bold for labels
3. Maximum vertical merge span: 10 rows (readability)
4. Merged header cells must clearly indicate the grouping relationship
5. The first-column merged cell should use a slightly larger or bolder font
   to reinforce its role as a section label

### `python-docx` Merge Pattern

```python
# First-column category spanning 3 rows
cell = table.cell(row_start, 0)
cell.merge(table.cell(row_start + 2, 0))
cell.text = "수업 전개"
cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
run = cell.paragraphs[0].runs[0]
run.bold = True
cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
```

---

## 9. Specific Template Style Notes

### 교수학습과정안 (Lesson Plan)

- Header info section uses a 2-column or 4-column key-value layout
- Key cells: right-aligned, bold
- Value cells: left-aligned, regular
- Learning objectives row spans full width
- Phase column uses vertical merge within each phase
- ◈ and ※ symbols prefix materials and cautions respectively

### 평가 루브릭 (Rubric)

- Achievement standard code in header section: `[4국01-03]` format
- Level columns must be equal width
- Level descriptors use present-tense descriptive language
- Include scoring guidance in parentheses if point-based

### 시간표 (Timetable)

- Day column headers: 월/화/수/목/금 (abbreviated)
- Period column: left-most, narrow (20mm)
- Subject names centered in each cell
- Lunch break row shaded light gray (#F2F2F2) with "점심" label
- Consistent cell height for uniform grid appearance

---

## 10. Accessibility and Readability

1. Minimum font size: 8pt (footnotes only); 9pt for all table content
2. Minimum contrast ratio: 4.5:1 (text to background)
3. Table must not exceed A4 width — no horizontal scrolling in print
4. Maximum 15 columns (beyond this, consider splitting into multiple tables)
5. For tables with 30+ rows, repeat header row on each printed page
6. Avoid text rotation in cells (use abbreviations instead)
7. Cell content should be ≤ 50 characters for body text (line breaks permitted for longer content)

---

## 11. NCIC Terminology Reference

When referencing curriculum standards, use official NCIC (국가교육과정정보센터) terminology:

| Term | Korean | Context |
|---|---|---|
| Achievement standard | 성취기준 | Rubric, lesson plan |
| Core competency | 핵심역량 | Lesson plan header |
| Unit | 단원 | Progress table, lesson plan |
| Period/lesson hour | 차시 | Progress table, timetable |
| Performance assessment | 수행평가 | Rubric |
| Formative assessment | 형성평가 | Rubric |
| Summative assessment | 총괄평가 | Rubric |
| Cross-curricular | 범교과 학습 | Lesson plan |
| Textbook | 교과서 | Progress table |
| Teacher's guide | 교사용 지도서 | Lesson plan materials |
| Achievement level | 성취수준 | Rubric (상/중/하) |

---

## 12. Quality Checklist — Korean Teacher Style

Before finalizing any table, verify:

### Structure & Layout
- [ ] First-column labels use `merge_cells` to span related content rows
- [ ] Merged cells are centered both horizontally and vertically, with bold text
- [ ] All column widths sum to exactly 170mm (or 257mm for landscape)
- [ ] Table has a `<표 N> 제목` title above it

### Borders (Sections, Not Boxes)
- [ ] Outer borders are 1.5pt black — frames the entire table
- [ ] Header bottom separator is 1.0pt black
- [ ] Inner horizontal lines are 0.5pt gray
- [ ] Inner vertical lines are 0.25pt light gray (thinner than horizontal)
- [ ] Unnecessary vertical lines removed where merging provides structure

### Header & Shading
- [ ] Header row has #F2F2F2 background with bold, centered text
- [ ] Header font is 1pt larger than body (10-11pt)
- [ ] Body cells have white (#FFFFFF) background — no zebra stripes
- [ ] Maximum 2 background colors in the entire table (header gray + white)

### Typography & Spacing
- [ ] Font is Malgun Gothic throughout (no system font fallback)
- [ ] Cell padding is 6pt top/bottom, 8pt left/right — generous breathing room
- [ ] Line spacing is 1.3x (130%) for body text
- [ ] No empty header or label cells

### Alignment
- [ ] Headers: center-aligned
- [ ] Numbers/scores: right-aligned
- [ ] Prose/descriptions: left-aligned
- [ ] Alignment is consistent within each column (no mixing)

### Content Quality
- [ ] Content is readable at A4 print size
- [ ] Korean text is grammatically correct and uses formal register
- [ ] Numbers and symbols are consistently formatted
- [ ] Table is 100% readable in grayscale print
- [ ] Color is decorative only (table is readable in grayscale)
- [ ] Source citations present for referenced standards

---

## 13. Three Key Differentiators — Korean Teacher Style Summary

Every table generated by this skill must exhibit these three characteristics that
distinguish Korean teacher-style tables from generic spreadsheet-style grids:

### 1. Header Background Color
- Light gray (#F2F2F2) shading + bold + 1pt larger font
- Creates a clear visual anchor without heavy borders

### 2. First-Column Emphasis
- Active use of `merge_cells` to span category labels across content rows
- First column acts as the structural backbone of the table
- Bold, centered text in merged cells reinforces hierarchy

### 3. Removal of Unnecessary Lines
- Outer frame is thick (1.5pt), inner lines are thin (0.25-0.5pt)
- Vertical lines are deliberately thinner than horizontal lines
- Structure comes from merging and alignment, not from grid lines
- "Sections, not boxes" — the table reads as a document layout
