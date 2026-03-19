---
name: anthropic-pptx
description: >-
  Create, read, edit PowerPoint presentations (.pptx). Includes creating slide
  decks, pitch decks, or presentations; reading, parsing, or extracting text
  from .pptx files; editing, modifying, or updating existing presentations;
  combining or splitting slide files; working with templates, layouts, speaker
  notes, or comments. Use when user mentions "deck", "slides", "presentation",
  or references a .pptx filename. Do NOT use for Word documents (use
  anthropic-docx), spreadsheets (use anthropic-xlsx), or PDFs (use
  anthropic-pdf). Korean triggers: "프레젠테이션", "슬라이드", "pptx".
metadata:
  author: "anthropic"
  version: "1.0.0"
  license: "Proprietary. LICENSE.txt has complete terms"
  category: "document"
---
# PPTX Skill

## HARD-GATE (New Presentation Creation Only)

When creating a NEW presentation from scratch (not reading or editing existing ones), do NOT start generating until these are confirmed:

1. **Audience** — Who will see this? (investors, board, engineers, customers, internal team)
2. **Key message** — What is the ONE thing the audience should remember?
3. **Slide count** — Approximate number of slides (default: 10-15 if unspecified)

If any of these are unclear from the user's request, ASK before proceeding. Do not assume audience or message.

This gate does NOT apply to: reading content, editing existing presentations, template-based modifications, or content extraction.

## Quick Reference

| Task | Guide |
|------|-------|
| Read/analyze content | `python -m markitdown presentation.pptx` |
| Edit or create from template | Read [references/editing.md](references/editing.md) |
| Create from scratch | Confirm HARD-GATE requirements → Read [references/pptxgenjs.md](references/pptxgenjs.md) + [references/style-guide.md](references/style-guide.md) |

---

## Reading Content

```bash
# Text extraction
python -m markitdown presentation.pptx

# Visual overview
python scripts/thumbnail.py presentation.pptx

# Raw XML
python scripts/office/unpack.py presentation.pptx unpacked/
```

---

## Editing Workflow

**Read [references/editing.md](references/editing.md) for full details.**

1. Analyze template with `thumbnail.py`
2. Unpack → manipulate slides → edit content → clean → pack

---

## Creating from Scratch

**Read [references/pptxgenjs.md](references/pptxgenjs.md) for full details.**

Use when no template or reference presentation is available.

---

## Design Ideas

**Don't create boring slides.** Read [references/style-guide.md](references/style-guide.md) for color palettes, typography, layout options, spacing rules, and anti-patterns before creating any presentation.

---

## QA (Required)

**Assume there are problems. Your job is to find them.**

Your first render is almost never correct. Approach QA as a bug hunt, not a confirmation step. If you found zero issues on first inspection, you weren't looking hard enough.

### Content QA

```bash
python -m markitdown output.pptx
```

Check for missing content, typos, wrong order.

**When using templates, check for leftover placeholder text:**

```bash
python -m markitdown output.pptx | grep -iE "xxxx|lorem|ipsum|this.*(page|slide).*layout"
```

If grep returns results, fix them before declaring success.

### Visual QA

**⚠️ USE SUBAGENTS** — even for 2-3 slides. You've been staring at the code and will see what you expect, not what's there. Subagents have fresh eyes.

Convert slides to images (see [Converting to Images](#converting-to-images)), then use this prompt:

```
Visually inspect these slides. Assume there are issues — find them.

Look for:
- Overlapping elements (text through shapes, lines through words, stacked elements)
- Text overflow or cut off at edges/box boundaries
- Decorative lines positioned for single-line text but title wrapped to two lines
- Source citations or footers colliding with content above
- Elements too close (< 0.3" gaps) or cards/sections nearly touching
- Uneven gaps (large empty area in one place, cramped in another)
- Insufficient margin from slide edges (< 0.5")
- Columns or similar elements not aligned consistently
- Low-contrast text (e.g., light gray text on cream-colored background)
- Low-contrast icons (e.g., dark icons on dark backgrounds without a contrasting circle)
- Text boxes too narrow causing excessive wrapping
- Leftover placeholder content

For each slide, list issues or areas of concern, even if minor.

Read and analyze these images:
1. /path/to/slide-01.jpg (Expected: [brief description])
2. /path/to/slide-02.jpg (Expected: [brief description])

Report ALL issues found, including minor ones.
```

### Verification Loop

1. Generate slides → Convert to images → Inspect
2. **List issues found** (if none found, look again more critically)
3. Fix issues
4. **Re-verify affected slides** — one fix often creates another problem
5. Repeat until a full pass reveals no new issues

**Do not declare success until you've completed at least one fix-and-verify cycle.**

---

## Converting to Images

Convert presentations to individual slide images for visual inspection:

```bash
python scripts/office/soffice.py --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
```

This creates `slide-01.jpg`, `slide-02.jpg`, etc.

To re-render specific slides after fixes:

```bash
pdftoppm -jpeg -r 150 -f N -l N output.pdf slide-fixed
```

---

## Dependencies

- `pip install "markitdown[pptx]"` - text extraction
- `pip install Pillow` - thumbnail grids
- `npm install -g pptxgenjs` - creating from scratch
- LibreOffice (`soffice`) - PDF conversion (auto-configured for sandboxed environments via `scripts/office/soffice.py`)
- Poppler (`pdftoppm`) - PDF to images

## Examples

### Example 1: Create artifact
**User says:** Request to create, read, edit powerpoint presentations (
**Actions:** Gather requirements, apply the document creation workflow, and produce the artifact.
**Result:** Professional-quality output file in the specified format.

## Error Handling

| Issue | Resolution |
|-------|-----------|
| Unexpected input format | Validate input before processing; ask user for clarification |
| External service unavailable | Retry with exponential backoff; report failure if persistent |
| Output quality below threshold | Review inputs, adjust parameters, and re-run the workflow |
