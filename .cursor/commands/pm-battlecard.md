---
description: Create sales-ready competitive battlecards with positioning, feature comparison, objection handling, and win strategies.
argument-hint: "<competitor name> | <product context> | <win/loss pattern>"
---

# PM Battlecard

Create sales-ready competitive battlecards with positioning, feature comparison, objection handling, landmine questions, trap questions, and win/loss patterns. References pm-go-to-market skill, competitive-battlecard sub-skill.

## Usage

```
/pm-battlecard Create battlecard vs Competitor X for our B2B analytics product
/pm-battlecard 경쟁사 A 대비 세일즈 배틀카드 만들어줘
```

## Workflow

### Step 1: Load skill and reference

Read the `pm-go-to-market` skill (`.cursor/skills/pm-go-to-market/SKILL.md`) and the `references/competitive-battlecard.md` file.

### Step 2: Gather context

Collect from the user (or request if missing):

- Competitor name(s) and product
- Our product, positioning, and differentiators
- Recent win/loss patterns or anecdotal feedback
- Key objections sales teams encounter

### Step 3: Build battlecard sections

Produce a structured battlecard with:

1. **Positioning** — Our vs competitor positioning, elevator pitch
2. **Feature comparison** — Side-by-side matrix (features, parity, gaps)
3. **Objection handling** — Top 5–7 objections with rebuttal scripts
4. **Landmine questions** — Questions to surface competitor weaknesses
5. **Trap questions** — Questions competitors struggle with (avoid asking if our answer is weak)
6. **Win strategies** — When we win; when to walk away
7. **Loss patterns** — Common reasons we lose; how to avoid

### Step 4: Output

Deliver markdown with tables, bullets, and ready-to-use sales scripts. Flag any gaps that need research validation.

## Notes

- Keep rebuttals factual; avoid disparaging competitors.
- Update battlecards quarterly or after major competitive changes.
- Include internal-only sections (landmines, traps) vs customer-facing content.
