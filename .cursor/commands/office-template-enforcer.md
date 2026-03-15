---
description: "Create company-compliant DOCX or PPTX from approved corporate templates"
---

# Office Template Enforcer

## Skill Reference

Read and follow the skill at `.cursor/skills/office-template-enforcer/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Analyze Request

Determine the document type and content topic from the user's request:
- **PPTX indicators**: presentation, slides, deck, PPT, 발표, 프레젠테이션, 슬라이드
- **DOCX indicators**: report, document, memo, Word, 보고서, 문서, 리포트

If ambiguous, ask the user which format they need.

### Step 2: Select Template

Read `.cursor/skills/office-template-enforcer/references/template-catalog.md` to find the best template match. If the user specifies a template ID, use it directly.

Available templates:
- `thaki-proposal-v1` (PPTX) — corporate proposals
- `thaki-report-v1` (DOCX) — corporate reports

### Step 3: Load Placeholder Map

Read the placeholder map JSON for the selected template:
- PPTX: `.cursor/skills/ppt-template-engine/assets/placeholder-maps/<template_id>.json`
- DOCX: `.cursor/skills/docx-template-engine/assets/placeholder-maps/<template_id>.json`

### Step 4: Generate JSON Content Spec

Based on the user's content requirements and the placeholder map, generate a complete JSON spec. Follow the authoring rules in `.cursor/skills/office-template-enforcer/references/authoring-rules.md`.

Save the spec to a temp file.

### Step 5: Run Engine

For PPTX:
```bash
python3 .cursor/skills/ppt-template-engine/scripts/generate_pptx.py \
  .cursor/skills/ppt-template-engine/assets/templates/<template_id>.pptx \
  <spec.json> \
  output/<output_name>.pptx
```

For DOCX:
```bash
python3 .cursor/skills/docx-template-engine/scripts/generate_docx.py \
  .cursor/skills/docx-template-engine/assets/templates/<template_id>.docx \
  <spec.json> \
  output/<output_name>.docx
```

### Step 6: Validate

For PPTX:
```bash
python3 .cursor/skills/ppt-template-engine/scripts/validate_pptx.py \
  output/<output_name>.pptx \
  .cursor/skills/ppt-template-engine/assets/placeholder-maps/<template_id>.json
```

For DOCX:
```bash
python3 .cursor/skills/docx-template-engine/scripts/validate_docx.py \
  output/<output_name>.docx \
  .cursor/skills/docx-template-engine/assets/placeholder-maps/<template_id>.json
```

### Step 7: Report

Provide the user with:
1. Generated file path
2. Validation status
3. Any warnings

If validation failed, follow the failure handling strategy in `.cursor/skills/office-template-enforcer/references/failure-handling.md`.

## Constraints

- NEVER generate office files without using an approved template
- NEVER include styling in the JSON spec
- Always validate before returning the file
- Maximum 2 retries on hard failures
