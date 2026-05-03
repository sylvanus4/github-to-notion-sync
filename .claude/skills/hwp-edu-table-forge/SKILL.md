---
name: hwp-edu-table-forge
description: >-
  Generate professional-grade tables for Korean elementary school teachers —
  curriculum progress, lesson plans, rubrics, observation records, research
  tables, management plans, and timetables. Primary output is DOCX via
  python-docx; HWP via rhwp-pipeline conversion; PDF via pandoc or
  rhwp-converter.
---

# HWP Education Table Forge

Generate high-quality, print-ready tables that Korean elementary school teachers
use daily — curriculum planning, lesson plans, rubrics, student observation,
research reports, classroom management, and timetables.

## When to Use

Use when the user asks to create tables for Korean elementary education contexts:
curriculum progress, lesson plans (교수학습과정안), assessment rubrics, student
observation records, research report tables, classroom management plans, or
weekly timetables. Also use when the user mentions "한글 표", "교육용 표", or
any of the 7 template types by Korean or English name.

## When NOT to Use

- General DOCX creation without education table intent → use `anthropic-docx`
- Spreadsheet data modeling or CSV operations → use `anthropic-xlsx`
- Visual HTML tables for web display → use `visual-explainer`
- Figma design system tables → use `figma-dev-pipeline`
- HWP document viewing or debugging → use `rhwp-viewer` / `rhwp-debug`
- Non-Korean education table formats (US Common Core, UK curriculum) → adapt manually

## Skill Composition

| Skill | Role |
|---|---|
| `anthropic-docx` | DOCX generation engine patterns |
| `rhwp-pipeline` | DOCX-to-HWP conversion orchestration |
| `rhwp-converter` | SVG/PDF export from HWP |
| `sentence-polisher` | Korean text quality in cell content |
| `gws-drive` | Google Drive upload (optional distribution) |

## 7 Built-in Table Templates

| # | Korean Name | English Name | Key Structure |
|---|---|---|---|
| 1 | 교과 진도표 | Curriculum Progress | Month × Week × Unit grid with completion tracking |
| 2 | 교수학습과정안 | Lesson Plan | Multi-section plan: objectives, activities, materials, assessment |
| 3 | 평가 루브릭 | Assessment Rubric | Criteria × Achievement Level matrix with NCIC alignment |
| 4 | 학생 관찰 기록표 | Student Observation | Per-student behavior/participation tracking grid |
| 5 | 연구 과제 보고서 표 | Research Report Table | Structured data/analysis table for research reports |
| 6 | 학급 운영 계획 | Classroom Management | Goals, roles, activities, schedule overview |
| 7 | 시간표 | Weekly Timetable | Period × Day grid with subject assignments |

## Execution Flow

### Step 1: Identify Table Type

Determine which of the 7 templates fits the user's request. If ambiguous, ask:

```
어떤 종류의 표를 만들까요?
1. 교과 진도표 (Curriculum Progress)
2. 교수학습과정안 (Lesson Plan)
3. 평가 루브릭 (Assessment Rubric)
4. 학생 관찰 기록표 (Student Observation)
5. 연구 과제 보고서 표 (Research Report)
6. 학급 운영 계획 (Classroom Management)
7. 시간표 (Weekly Timetable)
```

If the request doesn't fit any template, create a custom table following the
style guide in `references/style-guide.md`.

### Step 2: Collect Required Data

Load the JSON schema for the selected template from `references/template-schemas.md`.
Ask the user for required fields that aren't provided. Use sensible defaults
for optional fields:

- **Grade**: 3학년 (default)
- **Semester**: 1학기
- **Subject**: from user context
- **Year**: current year

For the lesson plan template, the minimum required fields are:
- Subject, grade, unit title, lesson objectives, and time allocation.

### Step 3: Generate DOCX

Run the `scripts/edu_table_generator.py` script with collected data:

```bash
python scripts/edu_table_generator.py \
  --template <template_type> \
  --data '<json_data>' \
  --output <output_path.docx>
```

The script applies **Korean teacher-style** formatting from `references/style-guide.md`:
- Malgun Gothic (맑은 고딕) font, 9-10pt body, 11pt headers (bold, centered)
- Thick outer borders (1.5pt black), header bottom separator (1.0pt gray)
- Thin inner horizontal lines (0.5pt gray), minimal vertical lines (0.25pt light gray)
- Light gray (#F2F2F2) header row shading, optional first-column shading (#F9F9F9)
- Cell padding: 6pt top/bottom, 8pt left/right with 1.3x line spacing
- White + Gray + Black only — no saturated colors, no alternate row shading
- Extensive cell merging for hierarchical first-column labels
- A4 page with 20mm margins (170mm usable width)
- Table numbering: `<표 N> 제목` above each table

If the script is unavailable, generate the DOCX inline using `python-docx`
following the style guide rules. See [`references/docx-code-patterns.md`](references/docx-code-patterns.md)
for complete constants, page setup, border, and cell-margin patterns.

### Step 4: Validate Quality

Before delivering, verify Korean teacher-style compliance:

- [ ] All cells have content (no unintended blanks; use `-` for intentionally empty)
- [ ] Header hierarchy matches the template spec (correct merge spans)
- [ ] Column widths sum to ≤ 170mm (A4 usable width)
- [ ] Font is Malgun Gothic throughout
- [ ] Outer borders 1.5pt black, header bottom 1.0pt gray
- [ ] Inner horizontal lines 0.5pt gray, vertical lines 0.25pt light gray (minimal)
- [ ] Header row: #F2F2F2 background, bold, centered, 11pt
- [ ] First column: #F9F9F9 background with hierarchical merge
- [ ] Cell padding: 6pt top/bottom, 8pt left/right
- [ ] Line spacing: 1.3x
- [ ] Colors: white + gray + black ONLY — no saturated colors
- [ ] Table title follows `<표 N> 제목` convention
- [ ] Korean text passes `sentence-polisher` quality check

### Step 5: Convert to HWP (if requested)

If the user requests HWP output, invoke `rhwp-pipeline`:

1. Save the DOCX to a temporary path
2. Use rhwp-pipeline's DOCX-to-HWP conversion
3. Verify the HWP output preserves table structure

If rhwp-pipeline is unavailable, deliver the DOCX and inform the user:
"DOCX 파일로 생성했습니다. HWP 변환이 필요하시면 한컴오피스에서 열어 다른 이름으로 저장해주세요."

### Step 6: Distribute (optional)

Based on user preference:
- **Local file**: Save to `outputs/edu-tables/{date}/`
- **Google Drive**: Upload via `gws-drive` skill
- **Slack**: Post to specified channel with file attachment
- **Notion**: Create a page with the table embedded (limited formatting)

## Constraints

- All table text MUST be in Korean (except English proper nouns like subject names)
- Tables MUST fit on A4 paper without horizontal scrolling
- Maximum 15 columns per table (readability limit)
- Header rows limited to 2-level hierarchy (avoid 3+ level nesting)
- Cell content should be concise: max 50 characters per cell for body text
- Never use color as the sole differentiator (print-friendly design)
- Follow NCIC (국가교육과정정보센터) standards for curriculum terminology

## Error Handling

| Scenario | Action |
|---|---|
| Missing required JSON fields | Prompt user for the missing fields; do NOT generate with blank cells |
| Template type not recognized | Show the 7-template selection menu from Step 1 |
| `edu_table_generator.py` import error | Fall back to inline `python-docx` generation using Step 3 patterns |
| Column count exceeds 15 | Reject and suggest splitting into multiple tables |
| Total column width > 170mm | Auto-adjust proportionally; warn user if content truncation occurs |
| `rhwp-pipeline` unavailable for HWP | Deliver DOCX with conversion instructions for Hancom Office |
| Korean font not installed | Use system fallback; warn that print output may differ |

## References

- `references/template-schemas.md` — JSON schemas for all 7 table types
- `references/style-guide.md` — Korean education table formatting rules
- `references/example-tables.md` — Annotated example structures

## Output Defaults

| Setting | Value |
|---|---|
| Primary format | DOCX |
| Page size | A4 (210 × 297mm) |
| Margins | 20mm all sides |
| Font | 맑은 고딕 (Malgun Gothic) |
| Header font size | 11pt bold, centered |
| Body font size | 9-10pt |
| Header shading | #F2F2F2 (light gray) |
| First column shading | #F9F9F9 (optional) |
| Outer borders | 1.5pt black |
| Header bottom border | 1.0pt gray |
| Inner horizontal | 0.5pt gray |
| Inner vertical | 0.25pt light gray (minimal) |
| Cell padding | 6pt top/bottom, 8pt left/right |
| Line spacing | 1.3x |
| Color palette | White + Gray + Black only |
| Output directory | `outputs/edu-tables/{YYYY-MM-DD}/` |
