---
name: knowledge-to-paper
description: >-
  Aggregate the day's Cognee-indexed knowledge, select the highest-signal topic,
  run the autonomous research pipeline, generate a presentation, upload to
  Google Drive, and summarize to Slack. Converts accumulated organizational
  knowledge into publishable artifacts. Use when the user asks to "convert
  knowledge to paper", "write paper from today's data", "지식을 논문으로",
  "오늘 쌓인 지식으로 논문 써줘", "knowledge-to-paper", or wants to automatically
  generate research papers from accumulated knowledge. Do NOT use for running
  auto-research on a specific topic (use auto-research directly), creating
  presentations without research (use anthropic-pptx), or general Cognee queries
  (use cognee).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "knowledge-management"
---
# knowledge-to-paper

Aggregate the day's Cognee-indexed knowledge, select the highest-signal topic, run the autonomous research pipeline, and distribute artifacts.

## Workflow

1. **Knowledge scan** — Query `cognee` for today's newly indexed entities and relationships; identify clusters with highest entity count and cross-reference density
2. **Topic selection** — Rank candidate topics by: novelty (new entities), connectivity (cross-domain relationships), strategic relevance (overlap with company priorities)
3. **Research** — Run `auto-research` on the selected topic: literature review, hypothesis generation, experiment design, paper writing
4. **Presentation** — Generate PPTX via `anthropic-pptx` summarizing key findings, methodology, and implications
5. **Upload** — Upload paper (markdown + PPTX) to Google Drive via `gws-drive` in a dated folder
6. **Distribute** — Post to Slack with Google Drive link, executive summary, and key takeaways in a threaded message

## Composed Skills

- `cognee` — Knowledge graph query for topic discovery
- `auto-research` — 23-stage autonomous research pipeline
- `anthropic-pptx` — Presentation generation
- `gws-drive` — File upload to Google Drive
- Slack MCP — Summary distribution

## Error Handling

| Error | Action |
|-------|--------|
| Cognee returns no new entities for today | Report "No new knowledge indexed today — skipping paper generation" |
| No topic scores above relevance threshold | Present top-3 candidate topics to user for manual selection |
| auto-research pipeline fails at a stage | Report failed stage, offer to retry or skip to presentation with partial results |
| PPTX generation fails | Fall back to markdown-only output, upload markdown to Drive |
| Google Drive upload fails | Save files locally in `outputs/papers/`, notify user of local path |
| Slack posting fails | Log error, ensure files are uploaded to Drive as primary distribution |

## Examples

```
User: "오늘 쌓인 지식 중에서 논문 쓸만한 거 골라서 논문 작성하고 드라이브에 올려줘"
→ Scans Cognee → selects "Agent-Era Token Economics" → auto-research → PPTX → Drive → Slack

User: "knowledge-to-paper"
→ Full pipeline: scan → select → research → present → upload → distribute
```
