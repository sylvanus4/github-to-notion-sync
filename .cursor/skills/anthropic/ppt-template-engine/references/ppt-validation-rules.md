# PPT Validation Rules

8 compliance rules enforced by `validate_pptx.py` after every generation.

## Hard Fail Rules (block output)

### R1: Layout Compliance
Every slide must use a layout declared in the template's placeholder map. Slides exceeding the template slide count are violations.

### R2: No Rogue Shapes
No textboxes, shapes, or images may be added beyond what the template defines. Only named placeholders (from the placeholder map) and structural elements (BG_RECT, DIVIDER) are allowed.

### R3: Placeholder Fill
All required placeholders must contain actual content. If a `{{MARKER}}` string remains in the output, the placeholder was not filled.

### R7: Residual Markers
Any `{{PLACEHOLDER}}` text remaining anywhere in the output is a hard failure, indicating the generation step missed a substitution.

## Soft Fail Rules (warn, attempt auto-fix)

### R4: Theme Preservation
Fonts must be from the approved set (Arial, Pretendard, Calibri). Non-standard fonts trigger a warning. Auto-fix: reset to template default font.

### R5: Text Length
Each placeholder has a `max_chars` limit. Exceeding it triggers a warning. Auto-fix: truncate with ellipsis or request content compression from LLM.

### R6: Bullet Count
Bullet list placeholders have a `max_items` limit. Exceeding it triggers a warning. Auto-fix: group items or move overflow to speaker notes.

### R8: Master Integrity
Output slide count should match the expected template layout count. Mismatches generate a warning (may be intentional for multi-slide expansions).

## Severity Escalation

- 1+ hard violations: output is **rejected**, user is informed of specific failures
- Soft warnings only: output is **accepted** with a warning report
- 0 violations, 0 warnings: output is **clean**
