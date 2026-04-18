## Content Researcher

Research a topic and draft long-form content (blog posts, newsletters, reports) with real citations, matching your writing style.

### Usage

```
/content-researcher "AI agent platforms 2026"  # research and draft
/content-researcher --style blog               # blog post format
/content-researcher --style newsletter         # newsletter format
/content-researcher --style report             # technical report format
```

### Workflow

1. **Research** — Deep web search with parallel queries for comprehensive coverage
2. **Analyze** — Synthesize findings, identify key themes and contrarian angles
3. **Outline** — Structure the content with hook, body sections, and conclusion
4. **Draft** — Write long-form content with real citations and source links
5. **Polish** — Apply brand voice, tighten prose, add SEO optimization

### Execution

Read and follow the `parallel-deep-research` skill (`.cursor/skills/research/parallel-deep-research/SKILL.md`) for exhaustive research. Use `content-repurposing-engine` (`.cursor/skills/standalone/content-repurposing-engine/SKILL.md`) to adapt the output for multiple platforms.

### Examples

Research and write a blog post:
```
/content-researcher --style blog "Kubernetes GPU scheduling best practices"
```

Generate a newsletter section:
```
/content-researcher --style newsletter "This week in AI infrastructure"
```
