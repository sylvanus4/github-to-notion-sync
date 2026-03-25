## Markdown to Visual Explainer

Transform a markdown document into a self-contained visual HTML explainer page with Mermaid diagrams, severity badges, evidence sections, and ELI5 (초등학생 버전) explanations.

### Usage

```
/md-to-visual-explainer <path-to-markdown-file>
```

### What It Does

1. **Analyze** — Parse the markdown for items, severity levels, relationships, and technical concepts
2. **Plan visuals** — Map each item to diagram type, comparison panel, and analogy
3. **Generate HTML** — Produce a dark-themed self-contained page with hero, verdict, stats, TOC, and per-item visual cards
4. **Deliver** — Write HTML next to the source file with `-visual.html` suffix and open in browser

### Output Structure

Each item in the source document gets:
- **Problem Card** — What's the issue
- **Comparison Panel** — Before/after or current/proposed
- **Mermaid Diagram** — Architecture flow, sequence, or dependency graph
- **Evidence Box** — Code refs, doc quotes, data
- **ELI5 Box** — Elementary school version with real-world analogy

### Execution

Read and follow the `md-to-visual-explainer` skill (`.cursor/skills/md-to-visual-explainer/SKILL.md`) for workflow, styling spec, and quality checks.

### Examples

Architecture review:
```
/md-to-visual-explainer docs/multi-cluster-centralization/ko/10-v071-architecture-review.md
```

Technical spec:
```
/md-to-visual-explainer docs/technical-due-diligence/api-design.md
```

PRD or planning doc:
```
/md-to-visual-explainer docs/platform-overview/feature-spec.md
```
