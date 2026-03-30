# Authoring Rules

Rules the LLM must follow when generating content for template-based documents.

## What the LLM Produces

The LLM generates ONLY these content types:

- **Text**: titles, subtitles, headings, body paragraphs, captions
- **Bullet lists**: ordered or unordered items
- **Table data**: headers and row values
- **Speaker notes**: presentation notes (PPTX only)
- **Image captions**: descriptive text for image placeholders

## What the LLM NEVER Produces

The LLM must NEVER generate or reference:

- Font names, sizes, or weights
- Colors (hex, RGB, or named)
- Text alignment or spacing
- Shape positions (left, top, width, height)
- Slide layout names or IDs (these come from the template catalog)
- CSS, OOXML, or any markup
- Page margins, headers, footers
- Table border styles or cell shading
- Background colors or gradients

## Content Constraints

### Text Length

Every placeholder has a `max_chars` limit. If content exceeds it:
1. Summarize key points
2. Move details to speaker notes (PPTX) or appendix (DOCX)
3. Split across multiple sections if the template supports it

### Bullet Lists

Every bullet list placeholder has a `max_items` limit. If items exceed it:
1. Group related items
2. Prioritize top items
3. Move remaining to speaker notes or appendix

### Tables

Every table slot has a `max_rows` limit and fixed headers. Rules:
1. Match header names exactly as defined in the placeholder map
2. Do not add or remove columns
3. If rows exceed the limit, show the top N most important rows

## Language

- Content language follows user request (Korean, English, or mixed)
- Placeholder keys and template IDs are always English
- JSON spec keys are always English

## Quality Standards

- No placeholder text like "TBD", "TODO", or "Lorem ipsum"
- Every required slot must have substantive content
- Content should be professional and consistent in tone
- Numbers should include units and context
