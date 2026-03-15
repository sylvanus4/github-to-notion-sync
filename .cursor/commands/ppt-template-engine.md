---
description: "Populate a PPTX template with content via JSON spec, enforcing slide layouts and placeholder contracts"
---

# PPT Template Engine

## Skill Reference

Read and follow the skill at `.cursor/skills/ppt-template-engine/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Determine Template

If the user specifies a template ID, use it. Otherwise default to `thaki-proposal-v1`.

Read the placeholder map: `.cursor/skills/ppt-template-engine/assets/placeholder-maps/<template_id>.json`

### Step 2: Inspect Template (if needed)

If the user provides a custom template file:
```bash
python3 .cursor/skills/ppt-template-engine/scripts/inspect_template_pptx.py <template.pptx>
```

### Step 3: Generate JSON Spec

Create a JSON spec matching the template's layout and placeholder structure. The spec must contain:
- `template_id`: matching the placeholder map
- `slides`: array of objects with `layout_id` and `placeholders`

Each placeholder value must respect the `max_chars` and `max_items` limits from the map.

Save the spec as a temporary JSON file.

### Step 4: Generate PPTX

```bash
python3 .cursor/skills/ppt-template-engine/scripts/generate_pptx.py \
  .cursor/skills/ppt-template-engine/assets/templates/<template_id>.pptx \
  <spec.json> \
  output/<output_name>.pptx
```

### Step 5: Validate

```bash
python3 .cursor/skills/ppt-template-engine/scripts/validate_pptx.py \
  output/<output_name>.pptx \
  .cursor/skills/ppt-template-engine/assets/placeholder-maps/<template_id>.json
```

### Step 6: Report

Return the file path and validation report. If hard violations exist, fix the spec and retry (max 2 times).

## Constraints

- Only use layouts defined in the placeholder map
- Never add shapes or textboxes outside placeholders
- Never override theme fonts or colors
- Always run validation before returning the file
