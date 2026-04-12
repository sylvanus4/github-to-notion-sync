---
name: meeting-digest
description: >-
  Analyze any meeting content (Notion page, raw transcript, or local file) with
  multi-perspective PM sub-skills and produce structured Korean summaries with
  detailed action items. Always uploads results to Notion as two sub-pages
  (summary + action items) under the default meeting parent page. Optionally
  generates PPTX and Slack posts. Use when the user asks to "digest a meeting",
  "meeting digest", "analyze meeting", "summarize meeting from Notion",
  "회의 분석", "회의 다이제스트", "미팅 요약", "미팅 분석", "회의록 분석",
  "회의 정리", "meeting analysis", "analyze this transcript", "meeting action
  items", "회의 액션 아이템", or shares a Notion meeting page URL for analysis.
  Do NOT use for batch-syncing a Notion meeting database (use notion-meeting-sync).
  Do NOT use for basic meeting transcript-to-notes without PM analysis,
  simple meeting notes, "메모만 정리", "간단 정리", or "요약만" requests (use
  pm-execution summarize-meeting).
  Do NOT use for syncing markdown docs to Notion (use notion-docs-sync).
  Do NOT use for ad-hoc PPTX creation without meeting content (use anthropic-pptx).
metadata:
  author: "thaki"
  version: "2.1.0"
  category: "execution"
---
# Meeting Digest

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

Single-meeting orchestrator that accepts flexible input (Notion page, raw
transcript, or local file), runs multi-perspective PM analysis with meeting-type
detection, and produces structured Korean summaries with detailed action items.

## Configuration

| Key | Value |
|-----|-------|
| Output Directory | `outputs/meeting-digest/{date}/` (see Pipeline Output Protocol) |
| Language | Korean |
| MCP Server (Notion) | `plugin-notion-workspace-notion` |
| MCP Server (Slack) | `plugin-slack-slack` |
| Default Slack Channel | Specify at invocation via `--slack-channel <id>` |
| Default Notion Parent | Specify at invocation via `--notion-parent <id>` |
| Table Conversion Script | `.cursor/skills/notion/md-to-notion/scripts/convert_tables.py` |
| Pipeline run root (this skill) | `outputs/meeting-digest/{date}/` |

## Pipeline initialization (run start)

Before Phase 1, execute once per run:

1. Set `{date}` to the run date in `YYYY-MM-DD` (or a user-provided `--date` if supported).
2. Create the output directory: `outputs/meeting-digest/{date}/` (e.g. `mkdir -p`).
3. Write an initial `outputs/meeting-digest/{date}/manifest.json` with:
   - `pipeline`: `"meeting-digest"`
   - `date`: `{date}`
   - `started_at`: ISO-8601 timestamp
   - `completed_at`: `null`
   - `phases`: `[]` (populate as each phase completes)
   - `flags`: object for CLI flags in effect (e.g. `no_notion`, `pptx`, `slack`)
   - `overall_status`: `"running"`
   - `warnings`: `[]`

## Pipeline Output Protocol (File-First)

This skill uses **file-first** orchestration: every phase persists structured output to disk and records it in `manifest.json`. Downstream phases and any final summary/delivery **read only from these files and the manifest**, not from conversational memory or uncached subagent payloads.

### Directories and filenames

| Artifact | Path |
|----------|------|
| Run directory | `outputs/meeting-digest/{date}/` |
| Phase checkpoints | `outputs/meeting-digest/{date}/phase-{N}-{label}.json` |
| Run manifest | `outputs/meeting-digest/{date}/manifest.json` |
| Human-readable outputs (summary, action items, PPTX) | Same run directory (`summary.md`, `action-items.md`, optional `meeting-summary.pptx`) |
| Ingest audit copy | `outputs/meeting-digest/{date}/raw/{sanitized-title}.md` (normalized source for traceability) |

**Phase file mapping** (N = phase number, label = short slug):

| N | label | File |
|---|--------|------|
| 1 | ingest | `phase-1-ingest.json` |
| 2 | classify | `phase-2-classify.json` |
| 3 | pm-analysis | `phase-3-pm-analysis.json` |
| 4 | generate | `phase-4-generate.json` |
| 5 | deliver | `phase-5-deliver.json` |
| 6 | gbrain | `phase-6-gbrain.json` |

### Subagent Return Contract

Any Task/subagent invoked in this pipeline MUST return **only** this JSON-shaped result (no full analysis body in the message):

```json
{
  "status": "success | skipped | failed",
  "file": "absolute or repo-relative path to the written artifact, or null",
  "summary": "one short paragraph: what was produced and where"
}
```

The parent agent reads substantive content from `file` (or from the phase JSON written by the subagent per step instructions), never from the subagent’s chat transcript.

### Final aggregation rule

Phases that **compose** the Korean summary, action-items documents, Notion payloads, PPTX, or Slack posts MUST:

- Load `manifest.json` to confirm phase order and paths.
- Read inputs **only** from `phase-*.json` files (and the markdown files referenced by those JSON records), **not** from prior in-context summaries.

### `manifest.json` schema

Top-level object:

| Field | Type | Description |
|-------|------|-------------|
| `pipeline` | string | Always `"meeting-digest"`. |
| `date` | string | Run date `YYYY-MM-DD`. |
| `started_at` | string | ISO-8601 when the run began. |
| `completed_at` | string \| null | ISO-8601 when the run finished, or `null` while running. |
| `phases` | array | One entry per phase after completion (see below). |
| `flags` | object | Boolean/string flags (e.g. `no_notion`, `pptx`, `slack`, `slack_channel`, `notion_parent`). |
| `overall_status` | string | `"running"`, `"success"`, `"partial"`, or `"failed"`. |
| `warnings` | array of string | Non-fatal issues (e.g. skipped optional analysis). |

Each element of `phases`:

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Phase number (1–5). |
| `label` | string | Short slug (e.g. `ingest`, `classify`). |
| `status` | string | `"success"`, `"skipped"`, or `"failed"`. |
| `output_file` | string | Path to `phase-{N}-{label}.json`. |
| `started_at` | string | ISO-8601. |
| `elapsed_ms` | number | Wall time for the phase. |
| `summary` | string | Brief description of what was written. |

Update `manifest.json` after **each** phase completes (merge into `phases`, refresh `overall_status`/`warnings` as needed). Set `completed_at` and final `overall_status` when Phase 5 finishes.

### Output Artifacts (file-first)

| Phase | Stage | Output file | Notes |
|-------|--------|---------------|--------|
| 1 | Ingest | `phase-1-ingest.json` | Plus optional `raw/*.md` |
| 2 | Classify | `phase-2-classify.json` | |
| 3 | PM analysis | `phase-3-pm-analysis.json` | Merges core + parallel subagent artifacts |
| 4 | Generate | `phase-4-generate.json` | References `summary.md`, `action-items.md` |
| 5 | Deliver | `phase-5-deliver.json` | Notion/Slack/PPTX results |
| 6 | gbrain | `phase-6-gbrain.json` | Entity extraction (non-blocking) |

## Input Modes

| Mode | Detection | Handling |
|------|-----------|----------|
| **Notion URL/ID** | Input contains `notion.so` or is a 32-char hex ID | Fetch via `notion-fetch` MCP |
| **Local file** | `--file <path>` flag or input is a valid file path | Read from disk |
| **Raw text** | `--raw` flag or inline text without URL/path | Parse directly |
| **Mixed** | Notion URL + additional raw context | Fetch + append raw context |

## Pipeline Overview

```
Phase 1: Ingest       → Fetch/read meeting content, normalize to markdown
Phase 2: Classify      → Detect meeting type, select PM sub-skills
Phase 3: PM Analysis   → Run multi-perspective analysis (parallel, max 4 agents)
Phase 4: Generate      → Structured Korean summary + action items documents
Phase 5: Deliver       → Save files + upload to Notion; optionally PPTX, Slack
Phase 6: gbrain        → Extract entities (people, companies) → gbrain (non-blocking)
```

**Pattern**: Sequential (Phase 1 → 2 → 3 → 4 → 5).
Phase 3 runs parallel subagents for different PM perspectives.

All phases persist to `outputs/meeting-digest/{date}/` and update `manifest.json` (see **Pipeline Output Protocol (File-First)**).

---

## Phase 1: Content Ingestion

### 1.1 Detect Input Type

Parse user input to determine the source:

1. **Notion URL**: Contains `notion.so/` or `notion.site/` — extract page ID
2. **Notion page ID**: 32-character hex string (with or without hyphens)
3. **File path**: Ends with `.md`, `.txt`, or starts with `/`, `./`, `~`
4. **Raw text**: Everything else — treat as inline meeting content

### 1.2 Fetch Content

**CRITICAL**: Content ingestion must succeed before any analysis can proceed.
If the fetch fails, stop the pipeline and report the error.

**Notion source (token-first):**

When `NOTION_TOKEN` is available in `.env`, use `scripts/notion_api.py`:

```python
from scripts.notion_api import NotionClient, is_token_available

if is_token_available():
    client = NotionClient()
    page = client.get_page("<page-id>")
    blocks = client.get_block_children("<page-id>")
    # Paginate with start_cursor if has_more is True
else:
    # Fallback to MCP
    CallMcpTool(
      server="plugin-notion-workspace-notion",
      toolName="notion-fetch",
      arguments={
        "id": "<notion-url-or-page-id>",
        "include_transcript": true,
        "include_discussions": true
      }
    )
```

If both token and MCP fail, instruct the user to set `NOTION_TOKEN` in `.env`
or authorize the Notion MCP integration.

**Local file source:**

Read the file using the Read tool. Verify it exists before reading.

**Raw text source:**

Use the inline text directly.

### 1.3 Normalize Content

Convert fetched content to a normalized markdown document containing:
- Meeting title (extracted from Notion page title, filename, or first heading)
- Raw content body (all text, tables, bullet points preserved)

Save the normalized content to `outputs/meeting-digest/{date}/raw/{sanitized-title}.md`
for audit trail.

### 1.4 Persist & manifest (Phase 1)

1. Write `outputs/meeting-digest/{date}/phase-1-ingest.json` containing at minimum:
   - `input_mode` (notion | file | raw | mixed)
   - `source_ref` (URL, path, or indicator for raw)
   - `normalized_markdown_path`: path to `raw/{sanitized-title}.md`
   - `title`, `ingest_status`
2. Update `manifest.json`: append phase `id: 1`, `label: "ingest"`, `status`, `output_file`, `started_at`, `elapsed_ms`, `summary`.

---

## Phase 2: Meeting Type Classification

**Input for Phase 2**: Load normalized meeting text from the path in `phase-1-ingest.json` (`normalized_markdown_path`). Do not rely on chat context for the raw meeting body.

Classify the meeting content to determine which PM sub-skills to activate.
For the classification heuristics, see
[references/meeting-type-classifier.md](references/meeting-type-classifier.md).

### Meeting Types and Skill Activation

| Type | Activated PM Skills | Trigger Signals |
|------|-------------------|-----------------|
| **discovery** | pm-product-discovery (`summarize-interview`, `identify-assumptions-existing`) | User interviews, customer feedback, hypothesis, assumption |
| **strategy** | pm-product-strategy (`swot-analysis`, `value-proposition`) | Strategy, vision, pivot, competitive, positioning, market |
| **gtm** | pm-go-to-market (`gtm-strategy`, `ideal-customer-profile`) | Launch, pricing, go-to-market, sales, marketing, channel |
| **sprint** | pm-execution (`sprint-plan`, `retro`) | Sprint, backlog, velocity, retrospective, standup |
| **operational** | pm-execution (`summarize-meeting`) only | Status update, sync, weekly, standup, general |

**Default**: If no clear signals, classify as `operational`.
For full keyword lists and disambiguation rules, see
[references/meeting-type-classifier.md](references/meeting-type-classifier.md).

**Override**: If the user provides `--type <type>`, use that classification
regardless of content analysis.

The core `pm-execution/summarize-meeting` analysis always runs regardless of
meeting type.

### 2.1 Persist & manifest (Phase 2)

1. Write `outputs/meeting-digest/{date}/phase-2-classify.json` containing:
   - `meeting_type` (e.g. `discovery`, `strategy`, `gtm`, `sprint`, `operational`)
   - `activated_skills` (list)
   - `override_from_flag` (boolean)
   - `classification_notes` (short string)
2. Update `manifest.json` with phase `id: 2`, `label: "classify"`, timings, and summary.

---

## Phase 3: Multi-Perspective PM Analysis

**CRITICAL**: Launch parallel subagents (max 4 concurrent) based on the
detected meeting type. Each subagent must read the **normalized meeting content from disk** via `phase-1-ingest.json` → `normalized_markdown_path` (Read tool), not from inline chat context.

**Inputs for Phase 3**: Read `phase-1-ingest.json` and `phase-2-classify.json` only.

### 3.1 Core Analysis (always runs)

Read `.cursor/skills/pm/pm-execution/references/summarize-meeting.md` and follow
its instructions with the normalized meeting content loaded from the file path recorded in `phase-1-ingest.json` as input.

Extract:
- Date, time, participants (names and roles)
- Main topic / agenda
- Key discussion points (capture every topic — miss nothing)
- Decisions made with context and rationale
- Action items with owners and due dates
- Open questions and blockers
- Disagreements or concerns raised

### 3.2 Contextual Analysis (conditional, parallel)

Based on the meeting type from Phase 2, launch additional subagents:

**For `discovery` meetings:**

Launch a Task subagent to:
1. Read `.cursor/skills/pm/pm-product-discovery/SKILL.md`
2. Route to `identify-assumptions-existing`
3. Read `.cursor/skills/pm/pm-product-discovery/references/identify-assumptions-existing.md`
4. Apply the assumption identification framework to the meeting content
5. Write detailed findings to `outputs/meeting-digest/{date}/subagent-discovery.json` (or another deterministic path under the run directory) and return **only** `{ status, file, summary }` per **Subagent Return Contract**.

**For `strategy` meetings:**

Launch a Task subagent to:
1. Read `.cursor/skills/pm/pm-product-strategy/SKILL.md`
2. Route to `swot-analysis` or `value-proposition` (choose based on content)
3. Read the corresponding reference file
4. Apply the framework to the meeting discussion points
5. Write findings to `outputs/meeting-digest/{date}/subagent-strategy.json` and return **only** `{ status, file, summary }`.

**For `gtm` meetings:**

Launch a Task subagent to:
1. Read `.cursor/skills/pm/pm-go-to-market/SKILL.md`
2. Route to `gtm-strategy` or `ideal-customer-profile`
3. Read the corresponding reference file
4. Apply the framework to the meeting content
5. Write findings to `outputs/meeting-digest/{date}/subagent-gtm.json` and return **only** `{ status, file, summary }`.

**For `sprint` meetings:**

Launch a Task subagent to:
1. Read `.cursor/skills/pm/pm-execution/SKILL.md`
2. Route to `sprint-plan` or `retro` (based on content)
3. Read the corresponding reference file
4. Apply the framework to the meeting content
5. Write findings to `outputs/meeting-digest/{date}/subagent-sprint.json` and return **only** `{ status, file, summary }`.

### 3.3 Sentiment & Alignment Analysis (optional)

If the meeting contains significant debate, disagreements, or stakeholder
dynamics, launch an additional subagent to:
1. Read `.cursor/skills/pm/pm-market-research/SKILL.md`
2. Route to `sentiment-analysis`
3. Analyze stakeholder alignment and sentiment on key topics
4. Write findings to `outputs/meeting-digest/{date}/subagent-sentiment.json` and return **only** `{ status, file, summary }`.

Only activate this when the meeting content shows clear signals of
disagreement or multiple competing viewpoints.

### 3.4 Persist & manifest (Phase 3)

1. Merge core analysis and each successful subagent artifact into a single `outputs/meeting-digest/{date}/phase-3-pm-analysis.json` with:
   - `core_analysis` (path to a JSON or markdown snippet file, or structured fields)
   - `contextual_analyses`: array of `{ type, file, subagent_status }`
   - `optional_sentiment`: path or `null`
2. Update `manifest.json` with phase `id: 3`, `label: "pm-analysis"`, timings, summary. On partial failure, set phase `status` to `"partial"` and append entries to `warnings`.

---

## Phase 4: Document Generation

Combine Phase 3 analysis into two structured Korean documents **by reading only** `phase-3-pm-analysis.json`, `phase-1-ingest.json` (for title/metadata), and the referenced artifact files — **not** from uncached chat history.

### 4.1 Summary Document

Generate a comprehensive Korean summary following the template in
[references/summary-template.md](references/summary-template.md).

Save to `outputs/meeting-digest/{date}/summary.md` where `{date}` is the run
date in `YYYY-MM-DD` format. If a directory for today already exists and contains
output from a different meeting, append a sequence number:
`outputs/meeting-digest/{date}-{N}/`.

### 4.2 Action Items Document

Generate detailed action items following the template in
[references/action-items-template.md](references/action-items-template.md).

Save to `outputs/meeting-digest/{date}/action-items.md`.

### 4.3 PM Analysis Appendix (conditional)

If Phase 3 produced contextual PM analysis (SWOT, assumptions, ICP, etc.),
append it as an additional section in the summary document under a Korean appendix heading (e.g. appendix for PM analysis).

### Quality Checklist

Before proceeding to Phase 5, verify:
- [ ] Every discussion topic is captured
- [ ] All decisions listed with context
- [ ] All participants mentioned with roles
- [ ] No action items missing
- [ ] Open questions documented
- [ ] PM analysis appendix included (if applicable)
- [ ] Language is clear, professional Korean

### 4.4 Persist & manifest (Phase 4)

1. Write `outputs/meeting-digest/{date}/phase-4-generate.json` containing:
   - `summary_md`: `summary.md` (path relative to run dir or absolute)
   - `action_items_md`: `action-items.md`
   - `quality_checklist`: key booleans from the checklist above
2. Update `manifest.json` with phase `id: 4`, `label: "generate"`, timings, summary.

---

## Phase 5: Output Delivery

**Inputs for Phase 5**: Read `manifest.json`, `phase-4-generate.json`, `summary.md`, and `action-items.md` from `outputs/meeting-digest/{date}/` only. Do not reconstruct narrative from prior conversation turns.

### 5.1 Local Files (always)

Files are always saved to `outputs/meeting-digest/{date}/`:
- `summary.md` — Comprehensive Korean summary
- `action-items.md` — Detailed action items with dashboard

### 5.2 Notion Upload (always, unless --no-notion)

Notion upload runs by default after local file save. Use `--no-notion` to
skip. Use `--notion-parent <id>` to override the default parent page.

**Step 0: Fetch Notion Markdown Spec**

Before processing files, fetch the Notion enhanced markdown specification:

```
FetchMcpResource(
  server="plugin-notion-workspace-notion",
  uri="notion://docs/enhanced-markdown-spec"
)
```

Use this spec as reference for Notion-flavored markdown syntax in later steps.

**Step 1: Convert tables for Notion compatibility**

Create a temporary directory, then run the shared `convert_tables.py` script on
both output files:

```bash
TMPDIR=$(mktemp -d /tmp/notion-upload-XXXXXX)

python .cursor/skills/notion/md-to-notion/scripts/convert_tables.py \
  --outdir "$TMPDIR" \
  outputs/meeting-digest/{date}/summary.md \
  outputs/meeting-digest/{date}/action-items.md
```

This converts pipe tables to Notion `<table header-row="true">` HTML blocks,
extracts H1 titles, and outputs JSON to `$TMPDIR/notion_page_0.json` and
`$TMPDIR/notion_page_1.json`.

Each JSON file has either `"content"` (single page) or `"split": true` with
`"parts"` (array of `{subtitle, body}`) for documents exceeding the
threshold. Meeting digest outputs are typically under 15K chars, so splitting
is rare. If splitting occurs, create a parent page and sub-pages following
the split protocol in `.cursor/skills/notion/md-to-notion/SKILL.md` Step 3.

**Step 2: Create two Notion sub-pages**

**MANDATORY**: Use the Read tool to load `$TMPDIR/notion_page_0.json` and
`$TMPDIR/notion_page_1.json`. Parse each JSON and extract the `content` field
value. The `content` must be the COMPLETE output from the JSON file — no
omissions.

#### Path A: Token-based (preferred)

When `NOTION_TOKEN` is available:

```python
from scripts.notion_api import NotionClient

client = NotionClient()

# Read and parse each JSON to get markdown content, then convert to blocks
summary_blocks = NotionClient.md_to_blocks(summary_content)
actions_blocks = NotionClient.md_to_blocks(actions_content)

summary_page = client.create_page(
    parent_id="<parent-id>",
    title="[{YYYY-MM-DD}] {meeting-title} — 회의 요약",
    children=summary_blocks,
    icon_emoji="📋",
)
actions_page = client.create_page(
    parent_id="<parent-id>",
    title="[{YYYY-MM-DD}] 액션 아이템 대시보드",
    children=actions_blocks,
    icon_emoji="✅",
)
```

#### Path B: MCP fallback

When `NOTION_TOKEN` is NOT available:

```
CallMcpTool(
  server="plugin-notion-workspace-notion",
  toolName="notion-create-pages",
  arguments={
    "parent": {"page_id": "<parent-id>"},
    "pages": [
      {
        "properties": {"title": "[{YYYY-MM-DD}] {meeting-title} — summary report"},
        "icon": "📋",
        "content": "<FULL content from $TMPDIR/notion_page_0.json>"
      },
      {
        "properties": {"title": "[{YYYY-MM-DD}] action items dashboard"},
        "icon": "✅",
        "content": "<FULL content from $TMPDIR/notion_page_1.json>"
      }
    ]
  }
)
```

**CRITICAL**: The `parent` field must be an object `{"page_id": "..."}`,
not a bare string. The parent page ID must be provided via `--notion-parent`.

**Step 3: Verify upload**

Token path: `client.get_page(page_id)` to confirm each page exists.
MCP fallback:

```
CallMcpTool(
  server="plugin-notion-workspace-notion",
  toolName="notion-fetch",
  arguments={"id": "<parent-id>"}
)
```

Check that both created titles appear in the response. Report any missing
pages.

**Section-count verification**: Count `##` headings in the uploaded Notion
summary page and compare with the original `outputs/meeting-digest/{date}/summary.md`. If the Notion page
has fewer `##` headings (difference > 1), the upload is INCOMPLETE — delete
and re-upload using the full JSON content.

**Step 4: Cleanup temporary files**

After upload verification completes (or on any error after the temporary
directory was created), delete the temporary directory:

```bash
rm -rf "$TMPDIR"
```

### 5.3 PPTX Generation (--pptx flag)

When the `--pptx` flag is provided:

1. Read `.cursor/skills/anthropic/anthropic-pptx/SKILL.md` and follow its creation flow
2. Read `.cursor/skills/anthropic-theme-factory/SKILL.md` for theme application
3. Generate a slide deck with this structure:

| # | Slide | Content |
|---|-------|---------|
| 1 | Cover | Meeting summary title + date + meeting name (Korean) |
| 2 | Agenda | Major sections overview |
| 3 | Meeting overview | Attendees, time, topics |
| 4-N | Key discussion | One slide per major topic |
| N+1 | Key decisions | Decision table or cards |
| N+2 | Action items | Priority-grouped action table |
| N+3 | Open issues | Open questions + timelines |
| N+4 | Next steps | Follow-ups + timeline |

4. Apply "Modern Minimalist" theme (or user preference)
5. Save to `outputs/meeting-digest/{date}/meeting-summary.pptx`

**PPTX content source**: Build slides only from `phase-3-pm-analysis.json`, `summary.md`, and `action-items.md` on disk — not from chat memory.

### 5.4 Slack Post (--slack flag)

When the `--slack` flag is provided:

1. Load thread copy **only** from `outputs/meeting-digest/{date}/summary.md`, `action-items.md`, and `phase-3-pm-analysis.json` / `phase-4-generate.json` as needed for structure — do not paraphrase from earlier conversation context.
2. Post main message to the target channel (specified via `--slack-channel`)
3. Reply in-thread with detailed discussion points
4. Reply in-thread with action items dashboard
5. Reply in-thread with next steps

Each message must stay under 4000 characters. Split if needed.
Use Slack mrkdwn syntax (`*bold*`, `_italic_`, `` `code` ``).

No file uploads — only text-based summaries are posted.

### 5.5 Persist & manifest (Phase 5)

1. Write `outputs/meeting-digest/{date}/phase-5-deliver.json` containing:
   - `notion`: page IDs or URLs if uploaded, or `skipped: true` if `--no-notion`
   - `pptx_path`: path or `null`
   - `slack`: `{ channel, thread_ts }` or `skipped: true`
   - `tmp_dir_cleaned`: boolean
2. Update `manifest.json`: append phase `id: 5`, `label: "deliver"`, set `completed_at`, `overall_status` (`success` / `partial` / `failed`), and final `warnings`.

---

## Output Structure

```
outputs/meeting-digest/
└── {YYYY-MM-DD}/                 # Date-stamped run
    ├── manifest.json             # Phase index + status
    ├── phase-1-ingest.json
    ├── phase-2-classify.json
    ├── phase-3-pm-analysis.json
    ├── phase-4-generate.json
    ├── phase-5-deliver.json
    ├── phase-6-gbrain.json       # Entity extraction results (non-blocking)
    ├── raw/                      # Normalized source content
    │   └── {sanitized-title}.md
    ├── summary.md                # Korean summary with PM analysis
    ├── action-items.md           # Detailed action items + dashboard
    ├── subagent-*.json           # Optional per-subagent artifacts
    └── meeting-summary.pptx      # PowerPoint (if --pptx)
```

---

## Examples

### Example 1: Notion page meeting digest

User says: `/meeting-digest https://notion.so/thakicloud/VC-Pitch-Preview-3219eddc...`

Actions:
1. Detect Notion URL, extract page ID
2. Fetch page via `notion-fetch` with transcript
3. Classify as `strategy` meeting (contains pricing, positioning, competitive)
4. Run 3 parallel agents: summarize-meeting + SWOT analysis + sentiment
5. Generate `outputs/meeting-digest/2026-03-13/summary.md` with PM appendix
6. Generate `outputs/meeting-digest/2026-03-13/action-items.md` with 9 items
7. Convert tables via `convert_tables.py`, upload 2 sub-pages to Notion
8. Verify both pages appear under default parent

Result: Complete meeting digest in `outputs/meeting-digest/2026-03-13/` + Notion pages

### Example 2: Local file with PPTX and Slack

User says: `/meeting-digest --file outputs/meeting-digest/2026-03-13/raw/vc-pitch-preview.md --pptx --slack`

Actions:
1. Read local markdown file
2. Classify meeting type from content
3. Run PM analysis pipeline
4. Generate summary + action items
5. Upload 2 sub-pages to Notion (default behavior)
6. Create PPTX with themed slides
7. Post digest to the configured planning Slack channel with threaded replies

Result: Full output package + Notion pages + Slack notification

### Example 3: Raw transcript paste (no Notion)

User says: `/meeting-digest --raw "Today we discussed the Q3 roadmap..." --no-notion`

Actions:
1. Parse inline text as meeting content
2. Classify as `operational` (general sync)
3. Run core summary analysis only
4. Generate summary + action items
5. Skip Notion upload (--no-notion)

Result: Lean output without PM analysis or Notion upload

### Example 4: Force meeting type with custom Notion parent

User says: `/meeting-digest --type discovery --notion-parent abc123... https://notion.so/...`

Actions:
1. Fetch Notion page
2. Skip classification, use `discovery` type
3. Run core summary + assumption identification
4. Generate output with discovery-focused appendix
5. Upload to custom Notion parent `abc123...`

Result: Discovery-perspective analysis with Notion upload to custom parent

---

## Phase 6: gbrain Entity Extraction (auto, non-blocking)

After Phase 5 delivery, extract entities from the meeting and push them to gbrain for entity-centric knowledge compounding. This phase is **non-blocking** — failures do not affect the overall pipeline status.

**Prerequisites**: `gbrain` CLI available at `~/.local/bin/gbrain`, PostgreSQL running.

### 6.1 Extract Entities from Phase 3 Output

Read `phase-3-pm-analysis.json` and `phase-1-ingest.json`. Extract:

1. **People** — meeting participants (names, roles if available)
2. **Companies** — organizations mentioned in the discussion
3. **Ideas** — key concepts, product ideas, or strategic themes discussed

### 6.2 Stage Entity Files

Create a temporary staging directory and generate markdown files with YAML frontmatter:

```bash
STAGING=$(mktemp -d /tmp/gbrain-meeting-XXXXXX)
```

For each person:
```markdown
---
tags: [meeting-contact, {meeting-type}]
---
# {Person Name}

- **Role**: {role if known}
- **Context**: Participated in [{meeting-title}] on {date}

## Meeting Notes
- {relevant discussion points involving this person}
```
→ Save as `$STAGING/people/{slugified-name}.md`

For each company:
```markdown
---
tags: [company, {meeting-type}]
---
# {Company Name}

Mentioned in [{meeting-title}] on {date}.

## Context
- {relevant discussion points about this company}
```
→ Save as `$STAGING/companies/{slugified-name}.md`

For the meeting itself:
```markdown
---
tags: [meeting, {meeting-type}]
---
# {Meeting Title} ({date})

## Participants
{list of attendees}

## Key Decisions
{from Phase 3 analysis}

## Action Items
{from Phase 4 action-items.md}
```
→ Save as `$STAGING/meetings/{date}-{slugified-title}.md`

### 6.3 Import to gbrain

```bash
~/.local/bin/gbrain import "$STAGING" --no-embed --json
```

Use `--no-embed` to avoid OpenAI API dependency during pipeline execution. Embeddings are generated in batch by `gbrain embed --stale` during the PM orchestrator's maintenance phase.

### 6.4 Persist & manifest (Phase 6)

1. Write `outputs/meeting-digest/{date}/phase-6-gbrain.json` containing:
   - `entities_extracted`: `{ people: N, companies: N, meetings: 1 }`
   - `import_result`: parsed JSON from `gbrain import` output
   - `staging_dir`: path (cleaned up after import)
   - `status`: `"success"` | `"skipped"` (if gbrain unavailable) | `"failed"`
2. Update `manifest.json`: append phase `id: 6`, `label: "gbrain"`, timings, summary.
3. Phase 6 failure sets its own status to `"failed"` but does NOT change `overall_status` from Phase 5's result.

### 6.5 Skip Conditions

Skip Phase 6 entirely (status: `"skipped"`) when:
- `gbrain` CLI is not found at `~/.local/bin/gbrain`
- PostgreSQL is not reachable (test with `gbrain doctor --json`)
- `--no-gbrain` flag is provided
- Phase 3 produced no extractable entities

---

## Error Handling

If a phase fails after earlier phases succeeded, use `manifest.json` and the latest `phase-*.json` files under `outputs/meeting-digest/{date}/` as the resume checkpoint; re-run from the failed phase after fixing the issue.

| Error | Recovery |
|-------|----------|
| Notion MCP not authenticated | Instruct user to authorize the Notion integration |
| Notion page not found (input) | Verify URL/ID, check permissions |
| Empty meeting content | Report "Meeting content is empty" and exit |
| File not found | Report file path error, suggest corrections |
| Meeting type ambiguous | Default to `operational`, note in output |
| PM sub-skill reference missing | Skip that analysis, continue with available skills |
| `convert_tables.py` fails | Fall back to raw markdown upload without table conversion |
| Notion upload fails | Save files locally, report Notion upload failure, continue with PPTX/Slack |
| `parent: "Expected object"` | Fix: use `{"page_id": "..."}` format (not a bare string) |
| PPTX generation fails | Save markdown outputs, report PPTX failure |
| Slack post fails | Save all files locally, report Slack failure |
| Content too short for analysis | Run core summary only, skip contextual PM skills |


## Subagent Contract

When spawning Task tool subagents:

- Always pass **absolute file paths** — subagent working directories are unpredictable
- Share only **load-bearing code snippets** — omit boilerplate the subagent can discover itself
- Require subagents to return: `{ status, file, summary }` — not full analysis text
- Include a **purpose statement** in every subagent prompt: "You are a subagent whose job is to [specific goal]"
- Never say "do everything" — list the 3-5 specific outputs expected
