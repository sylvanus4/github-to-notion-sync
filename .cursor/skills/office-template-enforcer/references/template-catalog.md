# Template Catalog

Registry of all approved corporate templates. Each template has a unique ID, file path, and defined contract (layouts/slots, placeholders, and rules).

## PPTX Templates

### thaki-proposal-v1

- **Template ID**: `thaki-proposal-v1`
- **File**: `.cursor/skills/ppt-template-engine/assets/templates/thaki-proposal-v1.pptx`
- **Placeholder Map**: `.cursor/skills/ppt-template-engine/assets/placeholder-maps/thaki-proposal-v1.json`
- **Purpose**: Corporate proposal and pitch decks
- **Branding**: ThakiCloud blue (#1A56DB), white background, Arial font
- **Slide Dimensions**: 10" x 7.5" (widescreen)

**Allowed Layouts:**

| Layout ID | Slide | Placeholders | Description |
|-----------|-------|--------------|-------------|
| title-slide | 1 | TITLE, SUBTITLE, AUTHOR | Full-bleed blue title slide |
| agenda | 2 | SECTION_TITLE, AGENDA_ITEMS | Section title + bullet list |
| two-column | 3 | LEFT_TITLE, LEFT_BODY, RIGHT_TITLE, RIGHT_BODY | Side-by-side content |
| kpi-dashboard | 4 | KPI_TITLE, KPI_TABLE | Metrics/data area |
| closing | 5 | CLOSING_MESSAGE, CONTACT | Full-bleed blue closing |

**Prohibited:**
- Creating new textboxes outside defined placeholders
- Overriding slide master fonts or colors
- Using layouts not listed above
- Adding background shapes beyond template definitions

**Trigger keywords**: proposal, pitch, deck, 제안서, 제안, 발표, 프레젠테이션

---

## DOCX Templates

### thaki-report-v1

- **Template ID**: `thaki-report-v1`
- **File**: `.cursor/skills/docx-template-engine/assets/templates/thaki-report-v1.docx`
- **Placeholder Map**: `.cursor/skills/docx-template-engine/assets/placeholder-maps/thaki-report-v1.json`
- **Purpose**: Corporate reports and analysis documents
- **Branding**: ThakiCloud blue (#1A56DB) headings, Arial font, page numbers
- **Header**: "ThakiCloud | Confidential"
- **Footer**: "© 2026 ThakiCloud | Page N"

**Allowed Styles:**
Title, Heading1, Heading2, Heading3, Normal, Strong, ListParagraph, Hyperlink

**Slots:**

| Slot Name | Type | Required | Max | Description |
|-----------|------|----------|-----|-------------|
| COVER_TITLE | text | yes | 80 chars | Cover page title |
| COVER_SUBTITLE | text | yes | 120 chars | Cover page subtitle |
| EXEC_SUMMARY | text | yes | 2000 chars | Executive summary |
| SECTION_1_BODY | text | yes | 5000 chars | Background section |
| SECTION_2_BODY | text | yes | 5000 chars | Proposed solution |
| RISKS_TABLE | table | yes | 15 rows | Risk assessment table |
| APPENDIX | text | no | 10000 chars | Appendix content |

**Prohibited:**
- Creating styles not in the allowed list
- Direct formatting outside style definitions
- Modifying table borders
- Altering headers or footers
- Removing section breaks

**Trigger keywords**: report, analysis, document, memo, 보고서, 분석, 문서, 리포트

---

## Adding New Templates

To register a new template:

1. Create the template file (.pptx or .docx) with named placeholders/bookmarks
2. Run the appropriate inspect script to discover structure
3. Create a placeholder map JSON in the engine's `assets/placeholder-maps/` directory
4. Add an entry to this catalog with all fields
5. Test with `generate_*.py` and `validate_*.py` scripts
