---
name: visual-explainer
description: Generate self-contained HTML pages that visually explain systems, code changes, plans, and data with Mermaid diagrams, comparison tables, and visual layouts.
disable-model-invocation: true
arguments: [topic]
---

Create a visual explanation for `$topic`.

## Output Types

1. **System Architecture**: Component diagrams with Mermaid
2. **Diff Review**: Before/after comparisons with highlighted changes
3. **Plan Review**: Phase diagrams with dependencies
4. **Data Visualization**: Tables, charts, comparison matrices
5. **Project Recap**: Timeline with milestones

## HTML Page Structure

- Self-contained (inline CSS/JS, no external dependencies)
- Dark theme with accessible contrast
- Mermaid diagrams rendered inline
- Responsive layout
- Print-friendly

## When to Use

- About to render a complex ASCII table (4+ rows or 3+ columns)
- Explaining architecture or system design
- Reviewing code changes across multiple files
- Presenting plans with dependencies

## Rules

- Always self-contained HTML (no CDN dependencies)
- Include alt text for diagrams
- Use semantic color coding (green=good, red=risk, yellow=warning)
- Save to outputs/ directory with descriptive filename
