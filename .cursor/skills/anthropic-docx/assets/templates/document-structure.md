# DOCX Document Structure Templates

Standard document structures for the `anthropic-docx` skill. Select the appropriate template based on document type.

## Professional Report

```
Cover Page → Table of Contents → Executive Summary → Sections → Appendix
```

| Section | Heading Level | Required |
|---------|--------------|----------|
| Cover Page | (no heading) | Yes |
| Table of Contents | (auto-generated) | Recommended |
| Executive Summary | H1 | Yes |
| Body Sections | H1/H2/H3 | Yes |
| Conclusions | H1 | Recommended |
| References | H1 | If citations used |
| Appendix | H1 | Optional |

## Business Memo

```
Header Block → Body → Action Items
```

| Element | Details |
|---------|---------|
| TO / FROM / DATE / RE | Header block, bold labels |
| Body | 1-3 paragraphs, no heading hierarchy |
| Action Items | Bulleted list at end |

## Formal Letter

```
Letterhead → Date → Recipient → Salutation → Body → Closing → Signature
```

| Element | Formatting |
|---------|-----------|
| Letterhead | Company name, address, contact info |
| Date | Right-aligned or left-aligned per convention |
| Body | Single-spaced, paragraph breaks between sections |
| Signature Block | "Sincerely," + name + title |

## Technical Manual

```
Title Page → Version History → TOC → Chapters → Glossary → Index
```

| Section | Notes |
|---------|-------|
| Version History | Table: Version, Date, Author, Changes |
| Chapters | H1 per chapter, H2/H3 for subsections |
| Code Blocks | Monospace font, 9pt, light gray background |
| Glossary | Alphabetical definition list |

## Common Elements

### Page Setup Defaults

| Property | Value |
|----------|-------|
| Page size | A4 (210mm × 297mm) |
| Margins | Top/Bottom: 25mm, Left/Right: 25mm |
| Font | Body: 11pt, Headings: proportional |
| Line spacing | 1.15 |
| Paragraph spacing | 6pt after |

### Header/Footer

| Element | Position |
|---------|----------|
| Document title | Header left |
| Page number | Footer center or right |
| Date | Footer left (optional) |
