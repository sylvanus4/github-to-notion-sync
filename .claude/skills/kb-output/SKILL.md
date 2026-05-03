---
name: kb-output
description: >-
  Generate formatted outputs from a Knowledge Base wiki — markdown articles,
  Marp slide decks, matplotlib charts, comparison tables, research reports,
  and visual diagrams. Outputs are saved to the KB's outputs/ directory and
  optionally filed back into the wiki. Use when the user asks to "generate
  slides from KB", "create a report", "kb output", "make a chart from KB
  data", "render KB as slides", "create a summary document", or wants
  visual/formatted artifacts derived from their knowledge base. Do NOT use for
  querying KB for text answers (use kb-query). Do NOT use for compiling the
  wiki itself (use kb-compile). Do NOT use for general slide creation (use
  anthropic-pptx). Korean triggers: "KB 출력", "슬라이드 생성", "KB 리포트", "지식베이스 출력",
  "KB에서 차트 만들기".
disable-model-invocation: true
---

# KB Output — Knowledge Base Artifact Generator

Generate rich visual and formatted outputs from a Knowledge Base wiki. Transforms KB content into slides, reports, charts, and visual aids for consumption beyond the IDE.

## Output Formats

| Format | Extension | Viewer | Description |
|--------|-----------|--------|-------------|
| Markdown article | `.md` | Obsidian/IDE | Long-form written output |
| Marp slides | `.marp.md` | Marp CLI/Obsidian Marp plugin | Presentation slides |
| Matplotlib chart | `.png` | Image viewer | Data visualizations |
| HTML explainer | `.html` | Browser | Interactive visual explainer |
| Mermaid diagram | `.md` | Obsidian/GitHub | Relationship diagrams |
| Research report | `.md` + `.docx` | Obsidian/Word | Structured report |
| Comparison table | `.md` | Obsidian/IDE | Side-by-side analysis |

## Output Directory

```
knowledge-bases/{topic}/outputs/
├── slides/
│   └── {title}.marp.md
├── charts/
│   └── {title}.png
├── reports/
│   └── {title}.md
├── diagrams/
│   └── {title}.md
└── explainers/
    └── {title}.html
```

## Workflow

### Step 1: Determine Output Type

Based on the user's request, identify the desired output format. If ambiguous, suggest the most appropriate format.

### Step 2: Research KB Content

Use the kb-query approach to gather relevant content:
1. Read `_index.md`
2. Identify relevant articles
3. Read them in full
4. Extract the data needed for the output

### Step 3: Generate Output

#### Marp Slides

Generate a Marp-format markdown presentation:

```markdown
---
marp: true
theme: default
paginate: true
header: "{Topic} Knowledge Base"
footer: "Generated {date}"
---

# {Title}

## {Subtitle}

---

## Key Concept 1

- Point 1
- Point 2
- Point 3

![bg right:40%](../wiki/images/concept-1.png)

---

## Key Concept 2

> "Notable quote from source" — Author

1. Detail 1
2. Detail 2

---

## Summary

| Aspect | Finding |
|--------|---------|
| Theme 1 | Summary |
| Theme 2 | Summary |
```

Save to `outputs/slides/{title}.marp.md`.

#### Matplotlib Charts

Generate a Python script that creates the visualization:

```python
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

fig, ax = plt.subplots(figsize=(10, 6))
# ... chart logic from KB data ...
plt.savefig('knowledge-bases/{topic}/outputs/charts/{title}.png', dpi=150, bbox_inches='tight')
plt.close()
```

Execute the script and save the resulting image.

#### Research Reports

Generate a structured markdown report:

```markdown
# {Title}

**Generated from:** {topic} Knowledge Base
**Date:** {date}
**Articles consulted:** {N}

## Executive Summary

[500-word summary]

## Detailed Findings

### Finding 1: {Title}

[Analysis with citations to KB articles]

### Finding 2: {Title}

[Analysis with citations]

## Recommendations

1. [Recommendation]
2. [Recommendation]

## Methodology

This report was synthesized from {N} articles in the {topic} KB,
covering {W}K words of source material from {S} original sources.

## References

- [[concept-1]] — {summary}
- [[concept-2]] — {summary}
```

#### HTML Explainer

Use the visual-explainer skill pattern to generate a self-contained HTML page with:
- Mermaid diagrams
- Collapsible sections
- Before/after comparisons
- Color-coded categories

#### Comparison Tables

Generate side-by-side comparison markdown:

```markdown
# {Item A} vs {Item B}

| Dimension | {Item A} | {Item B} |
|-----------|----------|----------|
| Category 1 | Details | Details |
| Category 2 | Details | Details |

## Analysis

[Synthesized comparison narrative]
```

### Step 4: File Back (Auto)

By default, every generated output is automatically filed back into the wiki. This implements the Karpathy feedback loop: "I end up filing the outputs back into the wiki to enhance it for further queries. So my own explorations always add up." Use `--no-file-back` to skip.

Copy the output into the wiki:

```
knowledge-bases/{topic}/wiki/outputs/{title}.md
```

Run kb-index to update the index with the new content.

### Step 5: Report

```
✓ Generated: {format} output
  File: knowledge-bases/{topic}/outputs/{subdir}/{filename}
  Based on: {N} KB articles

  To view:
  - Marp slides: `scripts/kb_render_slides.sh {topic}` (renders all .marp.md to PDF/HTML)
  - Charts: `python scripts/kb_render_charts.py {topic}` (renders matplotlib blocks to PNG)
  - HTML: open in browser
```

## Examples

### Example 1: Generate presentation slides

**User says:** "Create a slide deck from my transformer-architectures KB"

**Actions:**
1. Read KB index and summary
2. Select 8-12 most important concepts
3. Generate Marp-format slides with diagrams
4. Save to outputs/slides/

### Example 2: Create comparison chart

**User says:** "Chart the timeline of key developments in my ML KB"

**Actions:**
1. Extract dated concepts from KB
2. Generate matplotlib timeline visualization
3. Save PNG to outputs/charts/

### Example 3: Research report for a specific question

**User says:** "Generate a report on attention mechanisms from my KB"

**Actions:**
1. Research attention-related articles in KB
2. Write a structured 2000-word report
3. Save as markdown + optionally convert to DOCX

## Error Handling

| Error | Symptom | Action |
|-------|---------|--------|
| Insufficient KB content | Too few articles for requested output | Report minimum requirements |
| matplotlib not available | Import error | Suggest `pip install matplotlib` |
| Marp not installed | Cannot render slides | Provide raw .marp.md, suggest `npm install -g @marp-team/marp-cli` or use `scripts/kb_render_slides.sh` which also supports npx |
| Output too large | Generated report > 10K words | Split into sections or summarize |
