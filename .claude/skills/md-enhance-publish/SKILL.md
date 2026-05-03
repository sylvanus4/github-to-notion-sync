---
name: md-enhance-publish
description: >-
  Enhance markdown documents with Mermaid diagrams, decision matrices,
  quantitative evidence, and industry comparisons, then publish to Notion and
  post a summary thread to Slack. Sequential pipeline: discover → analyze →
  enhance → convert → publish → distribute. Use when the user asks to "enhance
  and publish markdown", "enrich docs and upload to Notion", "add diagrams and
  publish", "마크다운 보강 후 노션", "문서 보강해서 노션에 올려", "그래프 추가하고 노션", "도표 보강해서 슬랙에 공유",
  "md-enhance-publish", or wants to enrich existing markdown with visual aids
  and distribute to Notion + Slack. Do NOT use for uploading markdown as-is
  (use md-to-notion). Do NOT use for creating documents from scratch (use
  anthropic-docx). Do NOT use for Notion database operations (use Notion MCP
  directly). Korean triggers: "문서 보강", "마크다운 보강", "그래프 추가 퍼블리시", "도표 추가 노션",
  "보강해서 올려".
disable-model-invocation: true
---

# md-enhance-publish

Enrich markdown → convert for Notion → publish → Slack thread.

## Input

| Parameter | Required | Default |
|-----------|----------|---------|
| `<path>` | Yes | — |
| `--parent <id>` | No | `3239eddc34e680e8a7a5d5b5eac18b38` |
| `--slack <channel_id>` | No | `C0AA8NT4T8T` (#효정-할일) |
| `--icon <emoji>` | No | Auto-assigned per doc |
| `--skip-slack` | No | false |
| `--skip-notion` | No | false (enhance only) |
| `--dry-run` | No | false (show plan, no edits) |
| `--lang <ko\|en>` | No | `ko` |

## Subagent Strategy

Use parallel subagents to maximize throughput:

| Phase | Parallelizable | Strategy |
|-------|---------------|----------|
| Discover + Analyze | No | Sequential — need file list first |
| Enhance | Yes | 1 subagent per file (max 4 concurrent) |
| Convert | Yes | Batch via script |
| Publish | Partially | 2 pages per MCP call, sequential calls |
| Distribute | No | Sequential — need all page IDs |

For ≤3 files, run enhancement sequentially in main context.
For 4+ files, fan out to parallel subagents.

## Workflow

### Phase 0: Notion Spec

Fetch the Notion markdown specification before any conversion:

```
FetchMcpResource(server="plugin-notion-workspace-notion", uri="notion://docs/enhanced-markdown-spec")
```

Key rules from spec: pipe tables → `<table>` HTML blocks, Mermaid uses ````mermaid` blocks.

### Phase 1: Discover

1. Resolve `<path>` → file list (single file or `**/*.md` glob)
2. Skip `README.md`, `CHANGELOG.md`, `LICENSE.md`
3. Abort if no `.md` files found
4. Sort alphabetically

### Phase 2: Analyze

Per file, scan for enhancement opportunities:

| Signal in Content | → Enhancement |
|-------------------|---------------|
| System/component descriptions | `flowchart TD` architecture diagram |
| Phases, milestones, schedules | `gantt` chart |
| Options, alternatives, trade-offs | Decision matrix table + `xychart-beta` bar |
| Priority/severity lists | `quadrantChart` |
| Step-by-step flows | `sequenceDiagram` |
| Proportional breakdowns | `pie` chart |
| Dependency/ordering | `flowchart TD` with styled links |
| Vague claims without numbers | Specific metrics, latency, cost data |
| Assertions without backing | Industry comparisons, benchmarks |

`--dry-run` outputs per-file plan and stops.

### Phase 3: Enhance

#### Mermaid Rules

- Fenced ````mermaid` blocks; include `title` where supported
- Node labels ≤30 chars; Korean when `--lang ko`
- Prefer `flowchart TD` over LR for >4 nodes

#### Table Rules

- Pipe tables with header row (converted in Phase 4)
- ≥3 data rows; decision matrices score 1-10 with weighted total

#### Evidence Rules

- **Specific numbers** for vague claims (latency ms, cost $, capacity)
- **Industry comparisons** (GKE Fleet, AWS EKS, Azure Arc etc.)
- **Blockquotes** for key insights
- **Analogies** for complex concepts when `--lang ko`

#### Constraints

- Do NOT remove or rephrase existing content — only add
- Additions proportional to original size (50-line doc ≠ 500 lines added)
- Place diagram immediately after the section it illustrates
- Brief intro sentence before each enhancement

### Phase 4: Convert

Run the bundled script:

```bash
python .cursor/skills/md-enhance-publish/scripts/convert_for_notion.py <file.md>
```

Performs: extract H1 title → strip from body → convert pipe tables to `<table header-row="true">` HTML → preserve fenced code/Mermaid blocks → output to stdout.

Fallback if script unavailable: convert inline per md-to-notion table conversion pattern.

### Phase 5: Publish to Notion

**Authentication**: Token-first — check `NOTION_TOKEN` in `.env`.
If available, use `scripts/notion_api.py`. Otherwise fall back to MCP.

#### Path A: Token-based (preferred)

```python
from scripts.notion_api import NotionClient

client = NotionClient()

# Step 5a — Parent page
toc_blocks = NotionClient.md_to_blocks(table_of_contents)
parent_page = client.create_page(
    parent_id="<parent-id>",
    title="<title> (<YYYY-MM-DD>)",
    children=toc_blocks,
    icon_emoji="🏗️",
)

# Step 5b — Sub-pages
for section in sections:
    blocks = NotionClient.md_to_blocks(section["content"])
    client.create_page(
        parent_id=parent_page["id"],
        title=section["title"],
        children=blocks,
        icon_emoji=section["icon"],
    )
```

#### Path B: MCP fallback

**Step 5a — Parent page:**

```
CallMcpTool(
  server="plugin-notion-workspace-notion",
  toolName="notion-create-pages",
  arguments={
    "parent": {"page_id": "<parent-id>"},
    "pages": [{
      "properties": {"title": "<title> (<YYYY-MM-DD>)"},
      "icon": "🏗️",
      "content": "<table-of-contents>"
    }]
  }
)
```

**Step 5b — Sub-pages (batch 2 per call):**

```
arguments={
  "parent": {"page_id": "<step-5a-page-id>"},
  "pages": [{
    "properties": {"title": "<extracted-title>"},
    "icon": "<auto-icon>",
    "content": "<converted-content>"
  }]
}
```

**CRITICAL**: `parent` must be `{"page_id": "..."}` object, never a bare string.

**Auto-icon mapping:**

| Content Pattern | Icon |
|----------------|------|
| Overview / summary | 📋 |
| Problem / analysis | 🔍 |
| Conflict / challenge | ⚡ |
| Solution / design | 🎯 |
| Evaluation / review | ⚠️ |
| Plan / timeline | 📅 |
| Architecture | 🏛️ |
| Default | 📄 |

**Step 5c — Verify:** Fetch parent page, confirm all sub-pages listed.

### Phase 6: Distribute to Slack

**Step 6a — Main message:**

```
slack_send_message(channel_id, message="""
🏗️ *<Title> 문서 보강 완료*

`<path>` N개 문서를 보강하고 Notion에 업로드했습니다.

*추가:* Mermaid 다이어그램 N개, 결정 매트릭스, 정량적 근거

*문서:*
1. <icon> <title-1>
2. <icon> <title-2>
...
👉 Notion 링크는 쓰레드에 정리했습니다.
""")
```

**Step 6b — Thread reply** (using `thread_ts` from 6a):

```
📚 *Notion 링크*
🏠 <parent-link|title>
1️⃣ <link|title-1>
2️⃣ <link|title-2>
```

## Phase Skip Behavior

| Flags | Phases Executed |
|-------|----------------|
| (none) | 0→1→2→3→4→5→6 |
| `--skip-notion` | 1→2→3 (enhance in place, no convert/publish) |
| `--skip-slack` | 0→1→2→3→4→5 |
| `--skip-notion --skip-slack` | 1→2→3 (enhance only) |
| `--dry-run` | 1→2 (analyze only) |

## Error Handling

| Issue | Resolution |
|-------|------------|
| No `.md` files | Abort with clear message |
| Notion parent not found | Abort: "Parent page {id} not accessible" |
| Page creation fails | Log, continue remaining files, report at end |
| Slack fails | Warn, report Notion URLs in chat instead |
| Content too large | Split by H2 (reuse md-to-notion split logic) |
| Mermaid syntax error | Fix or skip with warning |
| Rate limit (429) | Retry: 2s → 4s → 8s (max 3) |

## Composed Skills

- **md-to-notion** — Table conversion, Notion MCP patterns, split logic
- **visual-explainer** — Mermaid diagram type selection
- **kwp-slack-slack-messaging** — Slack mrkdwn formatting

## Subagent Contract

When spawning Task tool subagents:

- Always pass **absolute file paths** — subagent working directories are unpredictable
- Share only **load-bearing code snippets** — omit boilerplate the subagent can discover itself
- Require subagents to return: `{ status, file, summary }` — not full analysis text
- Include a **purpose statement** in every subagent prompt: "You are a subagent whose job is to [specific goal]"
- Never say "do everything" — list the 3-5 specific outputs expected
