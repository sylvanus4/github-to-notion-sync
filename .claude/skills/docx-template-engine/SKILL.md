---
name: docx-template-engine
description: >-
  Populate approved DOCX templates with LLM-generated content via JSON specs,
  enforcing style whitelists, slot contracts, heading hierarchy, and corporate
  formatting. Use when the user asks to "fill a Word template", "generate
  report from template", "populate document template", "DOCX 템플릿 채우기", "워드 템플릿
  적용", "보고서 템플릿 생성", or needs template-compliant DOCX output that preserves
  corporate branding and structure. Do NOT use for creating Word documents
  from scratch without a template (use anthropic-docx). Do NOT use for editing
  existing non-template documents (use anthropic-docx). Do NOT use for PPTX
  template work (use ppt-template-engine). Do NOT use for orchestrating
  template selection across formats (use office-template-enforcer).
---

# DOCX Template Engine

Generate corporate-compliant DOCX files by populating approved templates with structured content. The LLM produces content only; this engine enforces all styles, structure, and formatting rules.

## Core Principle

**Content from LLM. Format from template. No exceptions.**

The LLM never decides fonts, colors, heading styles, or page layout. It only fills named slots with text, tables, or lists.

## Workflow

```
1. Inspect template    → extract styles + slots + bookmarks
2. Generate JSON spec  → LLM fills slot values only
3. Populate template   → scripts/generate_docx.py
4. Validate output     → scripts/validate_docx.py
5. Return or fail      → hard fail blocks; soft fail warns
```

### Step 1: Inspect Template

Run `scripts/inspect_template_docx.py <template.docx>` to discover available styles, bookmarks, and placeholder markers. Review the corresponding placeholder map at `assets/placeholder-maps/<template_id>.json`.

### Step 2: Generate JSON Spec

Instruct the LLM to produce a JSON object matching this schema:

```json
{
  "template_id": "thaki-report-v1",
  "document_title": "Document Title",
  "metadata": {
    "author": "ThakiCloud",
    "department": "AI Platform",
    "subtitle": "Subtitle text"
  },
  "sections": [
    {
      "slot": "EXEC_SUMMARY",
      "content": "Executive summary text here..."
    },
    {
      "slot": "SECTION_1_BODY",
      "content": "Background section content..."
    }
  ],
  "tables": [
    {
      "slot": "RISKS_TABLE",
      "headers": ["Risk", "Impact", "Mitigation"],
      "rows": [
        ["Cost overrun", "High", "Budget reserves"],
        ["Delay", "Medium", "Buffer sprints"]
      ]
    }
  ]
}
```

Rules for the LLM when generating the spec:
- Use ONLY slot names from the placeholder map
- Respect `max_chars` limits for each slot
- For table slots, match the header names exactly
- Respect `max_rows` limits for tables
- Never include styling directives (fonts, colors, sizes)
- Never add extra keys beyond `slot`, `content`, `headers`, `rows`

### Step 3: Populate Template

```bash
python3 scripts/generate_docx.py \
  assets/templates/<template_id>.docx \
  <spec.json> \
  <output.docx>
```

### Step 4: Validate Output

```bash
python3 scripts/validate_docx.py \
  <output.docx> \
  assets/placeholder-maps/<template_id>.json
```

See `references/docx-validation-rules.md` for all 7 rules (3 hard, 4 soft).

### Step 5: Handle Results

- **All passed**: Return the .docx file to the user
- **Soft warnings only**: Return the file with the warning report
- **Hard violations**: Do NOT return the file. Report violations to the user. Regenerate the JSON spec with corrections.

## Available Templates

| Template ID | File | Slots | Purpose |
|-------------|------|-------|---------|
| thaki-report-v1 | `assets/templates/thaki-report-v1.docx` | COVER_TITLE, COVER_SUBTITLE, EXEC_SUMMARY, SECTION_1_BODY, SECTION_2_BODY, RISKS_TABLE, APPENDIX | Corporate report |

## Examples

### Example: Generate a Corporate Report

```bash
# 1. Inspect the template
python3 scripts/inspect_template_docx.py assets/templates/thaki-report-v1.docx

# 2. Create spec.json with content for all slots
# (LLM generates this — see JSON schema in Step 2 above)

# 3. Generate the populated DOCX
python3 scripts/generate_docx.py \
  assets/templates/thaki-report-v1.docx \
  /tmp/spec.json \
  output/report.docx

# 4. Validate
python3 scripts/validate_docx.py \
  output/report.docx \
  assets/placeholder-maps/thaki-report-v1.json
```

Expected output: `{"passed": true, "hard_violations": 0, ...}`

## Output Discipline

- Generate content for defined slots ONLY — do not invent new sections or appendices
- Do not pad slot content with filler text to meet character limits
- Match content depth to the slot's purpose — a 3-sentence executive summary does not need 500 words
- If a slot is optional and there is no meaningful content for it, leave it empty

## Verification

After generating the populated DOCX, verify before returning:

1. **Validation script**: `python3 scripts/validate_docx.py <output.docx> assets/placeholder-maps/<template_id>.json`
2. **Content spot-check**: `pandoc <output.docx> -o /dev/stdout --to plain | head -30` — confirm key slot content appears

Report format:
```text
### Check: Template compliance
**Command run:** `python3 scripts/validate_docx.py output.docx ...`
**Output observed:** [paste actual JSON output]
**Result:** PASS (0 hard violations) or FAIL (N hard violations)
```

## Honest Reporting

- If validation reports hard violations, do NOT return the file — report the violations and regenerate
- Never claim "document generated successfully" when the validation JSON shows `hard_violations > 0`
- If the template file is missing or corrupt, report it — do not attempt to create a document without a template

## Prohibited Actions

- Creating styles not in the `allowed_styles` list
- Using direct formatting (bold/italic) outside style definitions
- Modifying table borders from template defaults
- Altering headers or footers
- Removing section breaks
- Generating OOXML or raw XML directly (use scripts only)
