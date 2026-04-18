## PPTX

Create, read, edit PowerPoint presentations — slide decks, pitch decks, speaker notes, layouts, and templates.

### Usage

```
/pptx create "Q1 review deck"         # create from description
/pptx read deck.pptx                  # extract content from existing
/pptx edit deck.pptx --slide 3        # edit a specific slide
/pptx combine deck1.pptx deck2.pptx   # merge presentations
```

### Workflow

1. **Plan** — Define deck structure: title, sections, slide count, audience
2. **Generate** — Create slides with content, layouts, and speaker notes
3. **Polish** — Apply consistent formatting, transitions, and visual hierarchy
4. **Export** — Save as .pptx file

### Execution

Read and follow the `anthropic-pptx` skill (`.cursor/skills/anthropic/anthropic-pptx/SKILL.md`) for comprehensive PowerPoint creation, reading, editing, and template management.

### Examples

Create a pitch deck:
```
/pptx create "investor pitch for AI cloud platform, 12 slides"
```

Extract content from existing:
```
/pptx read quarterly-review.pptx
```
