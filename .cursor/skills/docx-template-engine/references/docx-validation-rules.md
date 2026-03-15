# DOCX Validation Rules

7 compliance rules enforced by `validate_docx.py` after every generation.

## Hard Fail Rules (block output)

### R1: Style Whitelist
Only styles listed in the placeholder map's `allowed_styles` array may be used. Any paragraph or character style not in the whitelist is a violation.

### R5: Placeholder Fill
All `{{SLOT}}` markers must be replaced with actual content. Any remaining marker text in the document is a hard failure.

### R6: Header/Footer Preservation
The template's header and footer files must be present in the output. Missing headers or footers indicate the template structure was corrupted during generation.

## Soft Fail Rules (warn, attempt auto-fix)

### R2: Heading Order
Headings must follow a logical hierarchy (Title > Heading1 > Heading2 > Heading3). Skipping levels (e.g., Heading1 directly to Heading3) triggers a warning.

### R3: Direct Formatting Abuse
Excessive use of direct formatting (bold, italic, font size, color applied inline rather than via styles) triggers a warning when it exceeds 50 runs. Auto-fix: strip direct formatting and rely on styles.

### R4: Table Style Integrity
If the placeholder map defines table slots, the output must contain corresponding tables. Missing tables generate a warning.

### R7: Content Length
Slot content exceeding `max_chars` triggers a warning. Auto-fix: truncate with "..." or request content compression.

## Severity Escalation

- 1+ hard violations: output is **rejected**, user is informed of specific failures
- Soft warnings only: output is **accepted** with a warning report
- 0 violations, 0 warnings: output is **clean**
