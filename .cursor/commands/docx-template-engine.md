---
description: "Populate a DOCX template with content via JSON spec, enforcing style whitelists and slot contracts"
---

# DOCX Template Engine

## Skill Reference

Read and follow the skill at `.cursor/skills/docx-template-engine/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Determine Template

If the user specifies a template ID, use it. Otherwise default to `thaki-report-v1`.

Read the placeholder map: `.cursor/skills/docx-template-engine/assets/placeholder-maps/<template_id>.json`

### Step 2: Inspect Template (if needed)

If the user provides a custom template file:
```bash
python3 .cursor/skills/docx-template-engine/scripts/inspect_template_docx.py <template.docx>
```

### Step 3: Generate JSON Spec

Create a JSON spec matching the template's slot structure. The spec must contain:
- `template_id`: matching the placeholder map
- `sections`: array of objects with `slot` and `content`
- `tables`: array of objects with `slot`, `headers`, and `rows` (if applicable)

Each slot value must respect the `max_chars` limits from the map.

Save the spec as a temporary JSON file.

### Step 4: Generate DOCX

```bash
python3 .cursor/skills/docx-template-engine/scripts/generate_docx.py \
  .cursor/skills/docx-template-engine/assets/templates/<template_id>.docx \
  <spec.json> \
  output/<output_name>.docx
```

### Step 5: Validate

```bash
python3 .cursor/skills/docx-template-engine/scripts/validate_docx.py \
  output/<output_name>.docx \
  .cursor/skills/docx-template-engine/assets/placeholder-maps/<template_id>.json
```

### Step 6: Report

Return the file path and validation report. If hard violations exist, fix the spec and retry (max 2 times).

## Constraints

- Only use styles from the allowed_styles list
- Never add direct formatting outside style definitions
- Never modify table borders from template defaults
- Never alter headers or footers
- Always run validation before returning the file
