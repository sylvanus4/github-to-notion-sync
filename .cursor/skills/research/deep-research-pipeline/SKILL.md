---
name: deep-research-pipeline
description: >-
  End-to-end research pipeline: deep web research (parallel-deep-research),
  12-role cross-perspective analysis (role-dispatcher), and Notion publishing
  (md-to-notion) in a single sequential workflow. Produces research reports,
  executive briefings, and structured Notion pages from any business or
  technology topic. Use when the user asks to "deep research pipeline",
  "research and analyze", "deep research to notion", "딥 리서치 파이프라인",
  "종합 리서치", "리서치 후 종합 분석", or wants end-to-end research with
  multi-perspective analysis and Notion delivery.
  Do NOT use for deep research only (use parallel-deep-research), role
  dispatch without research (use role-dispatcher), or publishing existing
  files to Notion (use md-to-notion).
  Korean triggers: "딥 리서치 파이프라인", "종합 리서치", "리서치 분석 노션".
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "orchestration"
  composes:
    - parallel-deep-research
    - role-dispatcher
    - md-to-notion
---

# Deep Research Pipeline

Sequential 3-stage pipeline: deep web research, 12-role cross-perspective
analysis with CEO executive briefing, and Notion publishing.

```
Stage 1: Deep Research     → parallel-deep-research → {topic}.md
Stage 2: Role Dispatcher   → role-dispatcher        → role analyses + executive briefing
Stage 3: Notion Publish    → md-to-notion           → structured Notion pages
```

## Input

| Parameter | Required | Description |
|-----------|----------|-------------|
| `<topic>` | Yes | Research topic in natural language |
| `--parent <id>` | No | Notion parent page ID. Defaults to `3239eddc34e680e8a7a5d5b5eac18b38` (AI 자동 정리) |
| `--roles <list>` | No | Whitelist roles for dispatcher (e.g., `cto,pm,cso`) |
| `--skip <list>` | No | Blacklist roles (e.g., `hr,finance`) |
| `--processor <tier>` | No | parallel-cli processor tier: `pro-fast` (default), `ultra-fast`, `ultra` |

## Stage 1: Deep Research

Run `parallel-deep-research` to produce a comprehensive research report.

### 1.1 Generate topic slug

Create a slug from the topic: lowercase, hyphens, max 50 chars.
Example: "NVIDIA LPU inference architecture" → `nvidia-lpu-inference-architecture`

### 1.2 Start research

```bash
parallel-cli research run "<topic>" --processor <tier> --no-wait --json
```

Parse the JSON response to extract `run_id` and the monitoring URL.
Inform the user of the expected latency based on processor tier:

| Processor | Expected Latency |
|-----------|-----------------|
| `pro-fast` | 30s – 5 min |
| `ultra-fast` | 1 – 10 min |
| `ultra` | 5 – 25 min |

### 1.3 Poll for results

```bash
parallel-cli research poll "<run_id>" -o "<topic-slug>" --timeout 540
```

This produces:
- `{topic-slug}.md` — formatted research report
- `{topic-slug}.json` — metadata and sources

If the poll times out, re-run the same command to continue waiting.

### 1.4 Extract key findings

Read the research report `{topic-slug}.md` and extract:
- Executive summary (first section)
- Top 5-10 key findings
- Major data points, statistics, and sources

Store these as `research_context` for Stage 2.

**If `parallel-cli` is not found**: stop immediately, tell the user to run
`/parallel-setup`, then retry. Do NOT substitute with manual web search.

## Stage 1.5: Research Quality Gate

Before invoking role-dispatcher, verify the research output:
- [ ] Research report file `{topic-slug}.md` exists and word count >= 500
- [ ] At least 3 distinct sources cited (URLs, papers, or named references)
- [ ] Key findings are extractable (numbered list or structured sections with headings)
- [ ] No placeholder text remains ("TBD", "TODO", "research needed", "to be added")
- [ ] `{topic-slug}.json` metadata file exists with valid source entries

If research is thin (< 500 words or < 3 sources), warn the user and offer to re-run with broader search terms or a higher processor tier (`ultra` instead of `pro-fast`). If the report is empty, abort the pipeline.

## Stage 2: Role Dispatcher

Run `role-dispatcher` with the research findings as enriched context.

### 2.1 Prepare output directory

```bash
mkdir -p outputs/role-analysis/{topic-slug}
```

### 2.2 Invoke role-dispatcher

Follow the full role-dispatcher workflow from
`.cursor/skills/role/role-dispatcher/SKILL.md` with these inputs:

- **Topic**: The user's original `<topic>`
- **Scope constraints**: Append the `research_context` from Stage 1:
  ```
  The following deep research has been completed on this topic.
  Key findings to inform your analysis:
  {research_context}

  Reference report: {topic-slug}.md
  ```
- **Role whitelist**: Pass `--roles` if provided
- **Role blacklist**: Pass `--skip` if provided

This produces:
- Per-role analyses: `outputs/role-analysis/{topic-slug}/role-{name}.md`
- Executive briefing: `outputs/role-analysis/{topic-slug}/executive-briefing.md`
- Executive briefing DOCX: `outputs/role-analysis/{topic-slug}/executive-briefing.docx`
- Slack delivery to `#효정-할일`

### 2.3 Collect output manifest

After role-dispatcher completes, build a list of all generated markdown files:
1. The deep research report: `{topic-slug}.md`
2. The executive briefing: `outputs/role-analysis/{topic-slug}/executive-briefing.md`
3. All role analyses with score >= 5: `outputs/role-analysis/{topic-slug}/role-*.md`

## Stage 3: Notion Publish

Publish all outputs as structured Notion pages.

### 3.1 Determine parent page

Use `--parent` if provided, otherwise default to `3239eddc34e680e8a7a5d5b5eac18b38`.

### 3.2 Create hub page

Create a top-level hub page under the parent with title:
`"🔬 {Topic} — Deep Research & Analysis"`

Use the Notion MCP to create this page:

```
CallMcpTool(
  server="plugin-notion-workspace-notion",
  toolName="notion-create-pages",
  arguments={
    "parent": {"page_id": "<parent-id>"},
    "pages": [{
      "properties": {"title": "🔬 {Topic} — Deep Research & Analysis"},
      "icon": "🔬",
      "content": "<hub page content with overview and links>"
    }]
  }
)
```

The hub page content should include:
- Date and topic
- Research processor tier used
- Number of participating roles (N/12)
- Links to sub-pages (added after sub-page creation)

### 3.3 Publish sub-pages

Follow the md-to-notion workflow from `.cursor/skills/notion/md-to-notion/SKILL.md`
to publish each file as a sub-page under the hub page:

1. **Deep Research Report** — publish `{topic-slug}.md` with icon 📊
2. **Executive Briefing** — publish the executive briefing with icon 📋
3. **Role Analyses** — publish each relevant role analysis with icon matching
   the role (or default 📄)

For each file:
- Extract H1 as title (or derive from filename)
- Convert pipe tables to Notion `<table>` format
- Split if content exceeds 15,000 characters

### 3.4 Verify

Fetch the hub page to confirm all sub-pages are visible:

```
CallMcpTool(
  server="plugin-notion-workspace-notion",
  toolName="notion-fetch",
  arguments={"id": "<hub-page-id>"}
)
```

Report any missing pages.

## Output Summary

After all three stages complete, print a completion report:

```
## Deep Research Pipeline Complete

**Topic**: {topic}
**Processor**: {tier}
**Research**: {topic-slug}.md ({word count} words)
**Roles**: {N}/12 participated

**Generated files**:
- {topic-slug}.md (deep research report)
- {topic-slug}.json (research metadata)
- outputs/role-analysis/{topic-slug}/role-*.md (role analyses)
- outputs/role-analysis/{topic-slug}/executive-briefing.md
- outputs/role-analysis/{topic-slug}/executive-briefing.docx

**Notion**: {M} pages created under hub page
  → {hub page URL}

**Slack**: Posted to #효정-할일
```

## Error Handling

| Stage | Issue | Resolution |
|-------|-------|------------|
| 1 | `parallel-cli` not found | Stop. Tell user to run `/parallel-setup` |
| 1 | Research poll timeout | Re-run poll command. If 3 retries fail, proceed with partial results |
| 1 | Research returns empty | Abort pipeline. Inform user |
| 2 | Role subagent fails | Log error, continue with remaining roles (role-dispatcher handles this) |
| 2 | Fewer than 2 relevant roles | Warn user but continue |
| 3 | Notion page creation fails | Retry once. If still fails, save locally and inform user |
| 3 | Content too large | Auto-split by H2 headings (md-to-notion handles this) |
| Any | User interrupts | Report progress and output files generated so far |

## Example

**User**: `/deep-research-pipeline NVIDIA Vera Rubin LPU architecture and its impact on AI cloud infrastructure`

**Execution**:
1. Topic slug: `nvidia-vera-rubin-lpu-architecture`
2. Stage 1: `parallel-cli research run` with `pro-fast` → produces 15-page research report
3. Stage 2: role-dispatcher with research context → 10/12 roles participate, executive briefing generated
4. Stage 3: Hub page + 12 sub-pages created in Notion, Slack thread posted
5. Total time: ~15-25 minutes (mostly Stage 1 research + Stage 2 parallel analysis)
