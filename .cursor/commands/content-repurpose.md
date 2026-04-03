## Content Repurposing Engine

Transform long-form content (articles, reports, papers, docs) into platform-specific formats: Twitter threads, LinkedIn posts, newsletter sections, blog summaries, video script outlines, and more.

### Usage

```
# Repurpose a report to social media
/content-repurpose "outputs/analysis-2026-04-03.json" --platforms twitter,linkedin

# Repurpose a paper review across all platforms
/content-repurpose "outputs/papers/review.md" --platforms all

# Repurpose from a URL
/content-repurpose "https://example.com/article" --platforms newsletter,blog
```

### Workflow

1. **Ingest** — Read source content (file, URL, Notion page, pasted text)
2. **Extract** — Identify core thesis, key points, data, quotes, narrative arc
3. **Select Platforms** — Choose target formats (Twitter, LinkedIn, Newsletter, Blog, Video Script, Infographic, Email, Slack)
4. **Transform** — Adapt tone, density, and structure per platform
5. **Quality Check** — Verify thesis preserved, constraints met, standalone readability

### Output

All platform-specific pieces in a single structured document with repurposing notes.

### Execution

Read and follow the `content-repurposing-engine` skill (`.cursor/skills/standalone/content-repurposing-engine/SKILL.md`).
