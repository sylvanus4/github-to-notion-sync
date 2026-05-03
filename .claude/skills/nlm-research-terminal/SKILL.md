---
name: nlm-research-terminal
description: >-
  YouTube/arXiv/web -> NLM notebook -> cited Q&A -> Obsidian vault with
  passage citations. Triggers: "리서치 터미널", "연구 노트북", "리서치 파이프라인",
  "YouTube 리서치", "논문 리서치 노트북", "NLM 리서치 엔진", "research terminal".
  NOT for: NLM CRUD (notebooklm), studio-only (notebooklm-studio),
  Obsidian-only export (nlm-obsidian-sync).
---

# NLM Research Terminal

Single-command research pipeline: topic in, cited knowledge out.

```
Input: topic + optional questions
  │
  ├─ Phase 1: Source Discovery (YouTube, arXiv, web)
  ├─ Phase 2: NLM Notebook Build (create + parallel upload)
  ├─ Phase 3: Persona & Q&A (configure + cited queries)
  ├─ Phase 4: Content Generation (audio, mind map, flashcards)
  └─ Phase 5: Obsidian Export (nlm-obsidian-sync)
```

## Prerequisites

- `notebooklm-mcp` MCP server authenticated (`nlm login --check`)
- WebSearch tool available
- HF MCP tools available (`mcp__hf__paper_search`)
- Obsidian CLI configured + vault open (for Phase 5)

## Input

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `<topic>` | Yes | -- | Research topic in natural language |
| `--questions` | No | auto-generated | Comma-separated research questions |
| `--sources` | No | `youtube,arxiv,web` | Source types to search |
| `--max-sources` | No | `20` | Max sources to upload (NLM limit: 50) |
| `--persona` | No | `terse` | Chat persona: `terse`, `academic`, `analyst` |
| `--generate` | No | `audio,mind_map` | Artifacts to generate |
| `--vault-folder` | No | `Research/{topic-slug}` | Obsidian output folder |
| `--lang` | No | `ko` | Output language |
| `--skip-obsidian` | No | `false` | Skip Obsidian export |

## Phase 1: Source Discovery

Run 3 parallel search agents (model: haiku) to maximize coverage, minimize cost.

### 1.1 YouTube Search

Search for relevant YouTube videos. NotebookLM natively processes YouTube URLs.

```
WebSearch("site:youtube.com {topic} 2025 OR 2026", max_results=10)
WebSearch("{topic} youtube tutorial OR lecture OR analysis", max_results=10)
```

**Rank by:** relevance, channel authority, recency (12 months), duration > 10 min, view count.
Select top `max_sources / 3` videos.

### 1.2 arXiv Paper Search

```
mcp__hf__paper_search(query="{topic}", limit=10)
```

For each paper, construct the arXiv URL: `https://arxiv.org/abs/{paper_id}`

NotebookLM can process arXiv URLs directly as sources.

Select top `max_sources / 3` papers by relevance.

### 1.3 Web Sources

Search for high-quality web content: blog posts, reports, documentation.

```
WebSearch("{topic} analysis OR guide OR report 2025 OR 2026", max_results=10)
WebSearch("{topic} {competitor_keywords} blog OR whitepaper", max_results=10)
```

Filter: skip paywalled sites, social media posts, thin content.
Select top `max_sources / 3` URLs.

### 1.4 Source Manifest

Write discovered sources to scratch file for audit trail:

```
/tmp/nlm-research-{slug}-sources.json
```

Schema: `{"topic", "discovered_at", "sources": [{"type", "url", "title", "score", "paper_id?"}]}`

Report source count by type + top 5 titles. Ask confirmation before upload.

## Phase 2: NLM Notebook Build

### 2.1 Create Notebook

```
notebook_create(title="Research: {topic} ({date})")
```

Save `notebook_id` for all subsequent calls.

### 2.2 Configure Persona

```
chat_configure(
  notebook_id,
  goal="You are a research analyst. Provide cited, evidence-based answers. No speculation. Reference specific sources by name.",
  response_length="comprehensive"
)
```

Persona presets:

| Preset | Goal |
|--------|------|
| `terse` | Concise analyst. Cite sources. No intro, no fluff. Bullet points. |
| `academic` | Academic reviewer. Cite with passage references. Note methodology gaps. |
| `analyst` | Business analyst. Data-driven. Quantify claims. Compare across sources. |

### 2.3 Parallel Source Upload

Upload all sources. Batch in groups of 5 to avoid rate limits.

```
for each batch of 5 sources:
  source_add(notebook_id, source_type="url", url=src.url, wait=True, wait_timeout=120)
```

Track success/fail count. Report: "{N}/{total} uploaded. {failures} failed."
If > 30% failure rate, warn + suggest retry.

## Phase 3: Research Q&A

### 3.1 Auto-generate Questions (if not provided)

If user did not supply `--questions`, generate 5 research questions:

1. Core concept definition question
2. Current state / trends question
3. Key players / approaches comparison
4. Risks / limitations question
5. Future outlook / implications question

### 3.2 Run Queries

For each question:

```
notebook_query(notebook_id, query=question)
```

Capture the response including:
- Answer text
- Source citations (which sources were referenced)
- Passage references (specific quotes)

Write all Q&A results to scratch:

```
/tmp/nlm-research-{slug}-qa.json
```

### 3.3 Citation Accuracy Audit

After all queries, compile citation stats:
- Total citations across all answers
- Citation frequency per source (which sources got cited most)
- Sources never cited (low-value indicator)
- Unique passages cited

Report: "Sources cited: {n}/{total}. Most cited: {source_name} ({count}x)"

## Phase 4: Content Generation

Generate artifacts based on `--generate` flag. Run in parallel where possible.

| Artifact | Tool Call | Output |
|----------|-----------|--------|
| Audio podcast | `studio_create(notebook_id, artifact_type="audio", format="deep_dive", language=lang, confirm=True)` | MP3 |
| Mind map | `studio_create(notebook_id, artifact_type="mind_map", language=lang, confirm=True)` | Image |
| Flashcards | `studio_create(notebook_id, artifact_type="flashcards", difficulty="medium", language=lang, confirm=True)` | Deck |
| Study guide | `studio_create(notebook_id, artifact_type="report", report_format="Study Guide", language=lang, confirm=True)` | Doc |
| Quiz | `studio_create(notebook_id, artifact_type="quiz", question_count=15, language=lang, confirm=True)` | Quiz |

Poll `studio_status(notebook_id)` every 30s until all complete.

Download artifacts:
```
download_artifact(notebook_id, artifact_type="audio", output_path="/tmp/nlm-research-{slug}-podcast.mp3")
```

## Phase 5: Obsidian Export

Invoke `nlm-obsidian-sync` skill with:

```
topic: {topic}
slug: {topic-slug}
notebook_id: {notebook_id}
sources_file: /tmp/nlm-research-{slug}-sources.json
qa_file: /tmp/nlm-research-{slug}-qa.json
vault_folder: {vault-folder}
artifacts: [list of downloaded artifact paths]
```

See `nlm-obsidian-sync` skill for Obsidian output structure.

## Use Case Recipes

### Academic Research

```
/nlm-research-terminal "transformer attention mechanisms"
  --sources arxiv,web
  --persona academic
  --generate audio,flashcards,mind_map
  --questions "What are the main attention variants?,How does flash attention improve efficiency?,What are open problems in attention research?"
```

### Competitive Analysis

```
/nlm-research-terminal "Anthropic vs OpenAI model capabilities 2026"
  --sources youtube,web
  --persona analyst
  --generate mind_map,report
```

### Podcast Research

```
/nlm-research-terminal "AI agents in production systems"
  --sources youtube
  --max-sources 10
  --persona terse
  --generate audio
```

### Personal Second Brain

```
/nlm-research-terminal "my Obsidian vault on productivity systems"
  --sources web
  --persona terse
  --vault-folder "SecondBrain/Productivity"
```

## Subagent Routing

| Phase | Agent Model | Rationale |
|-------|-------------|-----------|
| 1.1-1.3 Source discovery | `haiku` | Simple search + ranking |
| 2.3 Source upload | main context | MCP tool calls |
| 3.1 Question generation | `haiku` | Template-based |
| 3.2-3.3 Q&A + audit | main context | MCP tool calls + analysis |
| 4 Content generation | main context | MCP tool calls |
| 5 Obsidian export | `sonnet` | Structured writing |

## Error Handling

| Error | Recovery |
|-------|----------|
| NLM auth expired | `refresh_auth()` then retry; if still fails, prompt `nlm login` |
| Source upload fails | Log URL, continue with remaining sources |
| No YouTube results | Fall back to web-only search |
| `paper_search` unavailable | Skip arXiv, increase web/YouTube quota |
| Obsidian CLI not found | Skip Phase 5, output to `/tmp/` markdown files instead |
| Studio generation stuck | Timeout after 10 min, skip artifact, continue |

## Output Summary

At completion, report:

```
Research Complete: {topic}
├─ Notebook: {notebook_id} ({source_count} sources)
├─ Q&A: {question_count} questions, {citation_count} citations
├─ Artifacts: {list of generated artifacts}
└─ Obsidian: {vault_folder}/ ({note_count} notes created)
```
