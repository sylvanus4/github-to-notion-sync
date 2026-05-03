---
name: x-to-slack
description: Fetch content from any URL (Twitter, GitHub, YouTube, blog), perform web research, classify topic, and post structured 3-message intelligence thread to Slack.
disable-model-invocation: true
arguments: [url]
---

Process `$url` and post structured intelligence to Slack.

## Pipeline

1. **Content Extraction**: Fetch via FxTwitter API (Twitter) or Defuddle/WebFetch (other URLs)
2. **Web Research**: Run supplementary search for context and related information
3. **Topic Classification**: Classify into AI/ML, infrastructure, business, trading, etc.
4. **Channel Routing**: Route to appropriate Slack channel based on classification
5. **3-Message Thread**: Post structured intelligence thread
6. **KB Save (mandatory)**: Persist a markdown artifact to the internal intelligence KB and register the URL in the central dedup registry — see "KB Persistence" below.

## Slack Thread Structure

### Message 1: Summary
- Source, author, date
- Key takeaway (1-2 sentences)
- Classification tags

### Message 2: Analysis
- Context and significance
- Related developments
- Implications for our work

### Message 3: Action Items
- Recommended follow-ups
- Related internal resources
- Links to source material

## Channel Routing

| Topic | Channel |
|-------|---------|
| AI/ML, Claude/Cursor | #ai-coding-radar |
| General tech news | #press |
| Trading/finance | #h-report |
| Default | #press |

## KB Persistence (Step 6)

After the Slack thread is posted, persist a markdown artifact to the **internal** intelligence KB. This is the same registry that `twitter-timeline-to-slack` writes to — single source of truth for dedup across all intelligence skills.

1. Generate a markdown file (`/tmp/x-to-slack-{slug}.md`) with YAML frontmatter (url, source, author, date, channel, topic, classification) and the full Message 2 + Message 3 content.
2. Save and register:

```bash
python3 scripts/intelligence/intel_registry.py save \
  "{url}" "/tmp/x-to-slack-{slug}.md" \
  --type "{tweet|article|github|youtube|blog}" \
  --channel "{channel_name}" \
  --ts "{message_ts}" \
  --topic "{classification_tag}"
```

The script writes to `knowledge-bases/intelligence/raw/YYYY-MM-DD-{slug}.md`, updates `url-registry.json`, and touches `.compile-pending` so the Stop hook auto-runs `kb_auto_compile.py intelligence`.

If `intel_registry.py save` fails (e.g., script missing), log a warning and continue — Slack post is already complete; KB save is non-blocking.

## Rules

- Never post to #random
- Include images and videos when available
- Each item gets its own thread (not combined)
- KB save (Step 6) is mandatory unless the URL is already a duplicate (`intel_registry.py check` exit 1 — skip the entire pipeline upfront)
