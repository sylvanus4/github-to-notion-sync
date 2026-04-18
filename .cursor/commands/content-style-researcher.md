## Content Style Researcher

Learn a writer's style from samples, build a reusable style profile, and generate new content that authentically mirrors their voice.

### Usage

```
/content-style-researcher --samples "url1, url2, url3" --topic "AI in healthcare"
/content-style-researcher --profile "outputs/style-profiles/paulgraham.md" --topic "startup mistakes"
/content-style-researcher --analyze "paste or URL of writing samples"
```

### Workflow

1. **Collect** — Gather 3-10 writing samples (URLs, pasted text, or files), normalize to markdown
2. **Extract** — Analyze 8 style dimensions (sentence architecture, vocabulary, rhythm, structure, rhetoric, tone, formatting, quirks)
3. **Validate** — Generate test paragraph, compare to original, iterate until indistinguishable
4. **Research & Draft** — Research the target topic with real citations, outline in their structure, draft in their voice
5. **Deliver** — Output content with Style Compliance Report and archive the Style Profile for reuse

### Execution

Read and follow the `content-style-researcher` skill (`.cursor/skills/standalone/content-style-researcher/SKILL.md`) for the full 5-phase workflow.

### Examples

Build a style profile from blog posts:
```
/content-style-researcher --samples "https://paulgraham.com/articles.html" --analyze
```

Generate content using a saved profile:
```
/content-style-researcher --profile "outputs/style-profiles/paulgraham.md" --topic "why startups fail"
```
