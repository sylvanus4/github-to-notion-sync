---
name: office-template-enforcer
description: >-
  Create company-compliant DOCX and PPTX outputs from approved corporate
  templates without fine-tuning. Orchestrates template selection, content
  generation as structured JSON, template population via sub-engines, and
  automated validation. Use when the user asks to "create a document from
  template", "make a presentation from template", "회사 템플릿으로 문서 만들기",
  "사내 양식으로 PPT 생성", "템플릿 기반 보고서", "corporate template document",
  "template-compliant output", or needs office documents that preserve corporate
  styles, slide masters, layouts, and formatting rules. Do NOT use for creating
  documents from scratch without templates (use anthropic-docx or anthropic-pptx).
  Do NOT use for PPTX template work alone (use ppt-template-engine directly).
  Do NOT use for DOCX template work alone (use docx-template-engine directly).
  Do NOT use for non-office document generation like PDFs or spreadsheets.
metadata:
  author: "thakicloud"
  version: "1.0.0"
  category: "document"
---

# Office Template Enforcer

Orchestrate the creation of corporate-compliant office documents by routing user requests to the correct template engine. This skill ensures that all DOCX and PPTX outputs adhere to approved templates with zero style drift.

## Core Principle

**LLM generates content. Template engines enforce format. Validators block violations.**

No fine-tuning required. No model-specific behavior. Any LLM produces the same compliant output because the template is the authority, not the model.

## Architecture

```
User Request
    ↓
office-template-enforcer (this skill)
    ├─ Detect document type (PPTX or DOCX)
    ├─ Select template from catalog
    ├─ Generate JSON content spec (LLM)
    └─ Delegate to engine
         ├─ ppt-template-engine  → .pptx output
         └─ docx-template-engine → .docx output
              ↓
         Validate → Return or Fail
```

## Workflow

### Step 1: Analyze Request

Determine from the user's request:
- **Document type**: PPTX (presentation, slides, deck, 발표자료, PPT) or DOCX (report, document, proposal text, 보고서, 문서)
- **Content topic**: What the document is about
- **Template hint**: If the user mentions a specific template name or ID

### Step 2: Select Template

Consult `references/template-catalog.md` to find the best matching template. Selection criteria:
1. Document type match (PPTX vs DOCX)
2. Purpose match (proposal, report, meeting notes, etc.)
3. If ambiguous, ask the user which template to use

### Step 3: Generate JSON Content Spec

Based on the selected template's placeholder map, instruct the LLM to generate a structured JSON spec. The spec must:
- Only include keys defined in the template's placeholder map
- Respect all `max_chars`, `max_items`, and `max_rows` limits
- Never include any styling, formatting, or layout directives
- Provide actual content for all `required: true` slots

Read the placeholder map from:
- PPTX: `.cursor/skills/ppt-template-engine/assets/placeholder-maps/<template_id>.json`
- DOCX: `.cursor/skills/docx-template-engine/assets/placeholder-maps/<template_id>.json`

### Step 4: Delegate to Engine

- For PPTX: Follow the `ppt-template-engine` skill workflow
- For DOCX: Follow the `docx-template-engine` skill workflow

### Step 5: Report Results

Return to the user:
1. The generated file path
2. Validation status (passed / warnings / failed)
3. Any warnings for review
4. If failed, the specific violations and instructions to fix

## Template Selection Quick Reference

See `references/template-catalog.md` for the full catalog.

| Template ID | Type | Purpose | Keywords |
|-------------|------|---------|----------|
| thaki-proposal-v1 | PPTX | Corporate proposal deck | proposal, pitch, 제안서, 발표 |
| thaki-report-v1 | DOCX | Corporate report | report, analysis, 보고서, 분석 |

## Content Generation Rules

See `references/authoring-rules.md` for detailed rules. Key rules:
- Content ONLY: text, bullets, table data, speaker notes
- NEVER: fonts, colors, sizes, positions, layouts, shapes
- If content exceeds limits, compress it — do not alter the template

## Examples

### Example 1: PPTX Proposal

**User**: "우리 회사 제안서 템플릿으로 AI PaaS 제안 PPT 만들어줘"

**Action**: Detect PPTX + proposal → select `thaki-proposal-v1` → generate JSON spec with 5 slides → delegate to `ppt-template-engine` → validate → return `output/ai-paas-proposal.pptx`

### Example 2: DOCX Report

**User**: "Create a report about GPU infrastructure using the corporate template"

**Action**: Detect DOCX + report → select `thaki-report-v1` → generate JSON spec with all slots → delegate to `docx-template-engine` → validate → return `output/gpu-infra-report.docx`

### Example 3: Ambiguous Request

**User**: "템플릿으로 문서 만들어줘"

**Action**: Ambiguous type → ask user: "PPTX (발표자료) or DOCX (보고서)?" → proceed based on answer

## Failure Handling

See `references/failure-handling.md` for the complete strategy.
- **Hard fail**: missing template, unfilled placeholders, unauthorized styles/layouts
- **Soft fail**: text too long, too many bullets — auto-compress and retry
