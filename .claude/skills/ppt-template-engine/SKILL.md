---
name: ppt-template-engine
description: >-
  Populate approved PPTX templates with LLM-generated content via JSON specs,
  enforcing slide master layouts, placeholder contracts, and corporate
  styling. Use when the user asks to "fill a PPT template", "generate slides
  from template", "populate presentation template", "PPT 템플릿 채우기", "슬라이드 템플릿
  적용", "프레젠테이션 템플릿 생성", or needs template-compliant PPTX output that preserves
  corporate branding. Do NOT use for creating presentations from scratch
  without a template (use anthropic-pptx). Do NOT use for editing existing
  non-template presentations (use anthropic-pptx). Do NOT use for DOCX
  template work (use docx-template-engine). Do NOT use for orchestrating
  template selection across formats (use office-template-enforcer).
---

# PPT Template Engine

Generate corporate-compliant PPTX files by populating approved templates with structured content. The LLM produces content only; this engine enforces all layout, style, and branding rules.

## Core Principle

**Content from LLM. Format from template. No exceptions.**

The LLM never decides fonts, colors, positions, or layouts. It only fills named placeholders with text, bullet lists, or table data.

## Workflow

```
1. Inspect template    → extract layouts + placeholders
2. Generate JSON spec  → LLM fills placeholder values only
3. Populate template   → scripts/generate_pptx.py
4. Validate output     → scripts/validate_pptx.py
5. Return or fail      → hard fail blocks; soft fail warns
```

### Step 1: Inspect Template

Run `scripts/inspect_template_pptx.py <template.pptx>` to discover available layouts and placeholder names. Review the corresponding placeholder map at `assets/placeholder-maps/<template_id>.json`.

### Step 2: Generate JSON Spec

Instruct the LLM to produce a JSON object matching this schema:

```json
{
  "template_id": "thaki-proposal-v1",
  "presentation_title": "Title here",
  "slides": [
    {
      "layout_id": "title-slide",
      "placeholders": {
        "TITLE": "Presentation Title",
        "SUBTITLE": "Subtitle text",
        "AUTHOR": "Author Name"
      }
    }
  ]
}
```

Rules for the LLM when generating the spec:
- Use ONLY layout IDs from the placeholder map
- Use ONLY placeholder names defined for that layout
- Respect `max_chars` and `max_items` limits
- For `bullet_list` type placeholders, provide a JSON array of strings
- Never include styling directives (fonts, colors, sizes)
- Never add extra keys beyond `layout_id` and `placeholders`

### Step 3: Populate Template

```bash
python3 scripts/generate_pptx.py \
  assets/templates/<template_id>.pptx \
  <spec.json> \
  <output.pptx>
```

### Step 4: Validate Output

```bash
python3 scripts/validate_pptx.py \
  <output.pptx> \
  assets/placeholder-maps/<template_id>.json
```

See `references/ppt-validation-rules.md` for all 8 rules (4 hard, 4 soft).

### Step 5: Handle Results

- **All passed**: Return the .pptx file to the user
- **Soft warnings only**: Return the file with the warning report
- **Hard violations**: Do NOT return the file. Report violations to the user. Regenerate the JSON spec with corrections.

## Available Templates

| Template ID | File | Layouts | Purpose |
|-------------|------|---------|---------|
| thaki-proposal-v1 | `assets/templates/thaki-proposal-v1.pptx` | title-slide, agenda, two-column, kpi-dashboard, closing | Corporate proposal deck |

## Examples

### Example: Generate a 5-slide Proposal

```bash
# 1. Inspect the template
python3 scripts/inspect_template_pptx.py assets/templates/thaki-proposal-v1.pptx

# 2. Create spec.json with content for all 5 slides
# (LLM generates this — see JSON schema in Step 2 above)

# 3. Generate the populated PPTX
python3 scripts/generate_pptx.py \
  assets/templates/thaki-proposal-v1.pptx \
  /tmp/spec.json \
  output/proposal.pptx

# 4. Validate
python3 scripts/validate_pptx.py \
  output/proposal.pptx \
  assets/placeholder-maps/thaki-proposal-v1.json
```

Expected output: `{"passed": true, "hard_violations": 0, ...}`

## Output Discipline

- Generate content for defined placeholders ONLY — do not invent extra slides or layouts
- Do not pad bullet lists to fill `max_items` if the content is better expressed in fewer points
- Match content density to the slide layout — do not cram 10 bullet points into a layout designed for 4
- If a placeholder is optional and there is no meaningful content, leave it empty

## Verification

After generating the populated PPTX, verify before returning:

1. **Validation script**: `python3 scripts/validate_pptx.py <output.pptx> assets/placeholder-maps/<template_id>.json`
2. **Slide count check**: Confirm the number of slides matches the spec
3. **Visual spot-check** (for complex decks): Convert to thumbnails and inspect

Report format:

```text
### Check: Template compliance
**Command run:** `python3 scripts/validate_pptx.py output.pptx ...`
**Output observed:** [paste actual JSON output]
**Result:** PASS (0 hard violations) or FAIL (N hard violations)
```

## Honest Reporting

- If validation reports hard violations, do NOT return the file — report the violations and regenerate
- Never claim "presentation generated successfully" when validation shows hard violations
- If the template file is missing, report it — do not attempt to create slides without a template

## Prohibited Actions

- Adding textboxes or shapes not in the placeholder map
- Overriding slide master fonts or colors
- Using layouts not listed in the placeholder map
- Inserting background shapes outside template definitions
- Generating OOXML or raw XML directly (use scripts only)
