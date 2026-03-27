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
  version: "2.0.1"
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
| Output Directory | `output/meetings/` |
| Language | Korean |
| MCP Server (Notion) | `plugin-notion-workspace-notion` |
| MCP Server (Slack) | `plugin-slack-slack` |
| Default Slack Channel | Specify at invocation via `--slack-channel <id>` |
| Default Notion Parent | Specify at invocation via `--notion-parent <id>` |
| Table Conversion Script | `.cursor/skills/md-to-notion/scripts/convert_tables.py` |

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
```

**Pattern**: Sequential (Phase 1 → 2 → 3 → 4 → 5).
Phase 3 runs parallel subagents for different PM perspectives.

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

**Notion source:**

```
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

If the fetch fails with authentication error, instruct the user to authorize
the Notion integration.

**Local file source:**

Read the file using the Read tool. Verify it exists before reading.

**Raw text source:**

Use the inline text directly.

### 1.3 Normalize Content

Convert fetched content to a normalized markdown document containing:
- Meeting title (extracted from Notion page title, filename, or first heading)
- Raw content body (all text, tables, bullet points preserved)

Save the normalized content to `output/meetings/raw/{sanitized-title}.md`
for audit trail.

---

## Phase 2: Meeting Type Classification

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

---

## Phase 3: Multi-Perspective PM Analysis

**CRITICAL**: Launch parallel subagents (max 4 concurrent) based on the
detected meeting type. Each subagent must receive the full normalized
meeting content from Phase 1.

### 3.1 Core Analysis (always runs)

Read `.cursor/skills/pm-execution/references/summarize-meeting.md` and follow
its instructions with the normalized meeting content as input.

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
1. Read `.cursor/skills/pm-product-discovery/SKILL.md`
2. Route to `identify-assumptions-existing`
3. Read `.cursor/skills/pm-product-discovery/references/identify-assumptions-existing.md`
4. Apply the assumption identification framework to the meeting content
5. Return: list of assumptions, confidence levels, and validation suggestions

**For `strategy` meetings:**

Launch a Task subagent to:
1. Read `.cursor/skills/pm-product-strategy/SKILL.md`
2. Route to `swot-analysis` or `value-proposition` (choose based on content)
3. Read the corresponding reference file
4. Apply the framework to the meeting discussion points
5. Return: SWOT matrix or value proposition canvas

**For `gtm` meetings:**

Launch a Task subagent to:
1. Read `.cursor/skills/pm-go-to-market/SKILL.md`
2. Route to `gtm-strategy` or `ideal-customer-profile`
3. Read the corresponding reference file
4. Apply the framework to the meeting content
5. Return: GTM strategy elements or ICP definition

**For `sprint` meetings:**

Launch a Task subagent to:
1. Read `.cursor/skills/pm-execution/SKILL.md`
2. Route to `sprint-plan` or `retro` (based on content)
3. Read the corresponding reference file
4. Apply the framework to the meeting content
5. Return: Sprint plan or retrospective output

### 3.3 Sentiment & Alignment Analysis (optional)

If the meeting contains significant debate, disagreements, or stakeholder
dynamics, launch an additional subagent to:
1. Read `.cursor/skills/pm-market-research/SKILL.md`
2. Route to `sentiment-analysis`
3. Analyze stakeholder alignment and sentiment on key topics
4. Return: Sentiment breakdown per topic and participant

Only activate this when the meeting content shows clear signals of
disagreement or multiple competing viewpoints.

---

## Phase 4: Document Generation

Combine Phase 3 analysis into two structured Korean documents.

### 4.1 Summary Document

Generate a comprehensive Korean summary following the template in
[references/summary-template.md](references/summary-template.md).

Save to `output/meetings/{date}/summary.md` where `{date}` is today's date
in `YYYY-MM-DD` format. If a directory for today already exists and contains
output from a different meeting, append a sequence number:
`output/meetings/{date}-{N}/`.

### 4.2 Action Items Document

Generate detailed action items following the template in
[references/action-items-template.md](references/action-items-template.md).

Save to `output/meetings/{date}/action-items.md`.

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

---

## Phase 5: Output Delivery

### 5.1 Local Files (always)

Files are always saved to `output/meetings/{date}/`:
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

python .cursor/skills/md-to-notion/scripts/convert_tables.py \
  --outdir "$TMPDIR" \
  output/meetings/{date}/summary.md \
  output/meetings/{date}/action-items.md
```

This converts pipe tables to Notion `<table header-row="true">` HTML blocks,
extracts H1 titles, and outputs JSON to `$TMPDIR/notion_page_0.json` and
`$TMPDIR/notion_page_1.json`.

Each JSON file has either `"content"` (single page) or `"split": true` with
`"parts"` (array of `{subtitle, body}`) for documents exceeding the
threshold. Meeting digest outputs are typically under 15K chars, so splitting
is rare. If splitting occurs, create a parent page and sub-pages following
the split protocol in `.cursor/skills/md-to-notion/SKILL.md` Step 3.

**Step 2: Create two Notion sub-pages**

**MANDATORY**: Use the Read tool to load `$TMPDIR/notion_page_0.json` and
`$TMPDIR/notion_page_1.json`. Parse each JSON and extract the `content` field
value. Pass that value **verbatim** as the `content` argument below.
NEVER manually type, summarize, abbreviate, or replace any portion of the
content with "see local file" or similar references. The `content` must be
the COMPLETE output from the JSON file — no omissions.

```
CallMcpTool(
  server="plugin-notion-workspace-notion",
  toolName="notion-create-pages",
  arguments={
    "parent": {"page_id": "<parent-id>"},
    "pages": [
      {
        "properties": {"title": "[{YYYY-MM-DD}] {meeting-title} — summary report (Korean title per template)"},
        "icon": "📋",
        "content": "<FULL content from $TMPDIR/notion_page_0.json>"
      },
      {
        "properties": {"title": "[{YYYY-MM-DD}] action items dashboard (Korean title per template)"},
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

Fetch the parent page to confirm both sub-pages appear:

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
summary page and compare with the original `summary.md`. If the Notion page
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

1. Read `.cursor/skills/anthropic-pptx/SKILL.md` and follow its creation flow
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
5. Save to `output/meetings/{date}/meeting-summary.pptx`

### 5.4 Slack Post (--slack flag)

When the `--slack` flag is provided:

1. Post main message to the target channel (specified via `--slack-channel`)
2. Reply in-thread with detailed discussion points
3. Reply in-thread with action items dashboard
4. Reply in-thread with next steps

Each message must stay under 4000 characters. Split if needed.
Use Slack mrkdwn syntax (`*bold*`, `_italic_`, `` `code` ``).

No file uploads — only text-based summaries are posted.

---

## Output Structure

```
output/meetings/
├── raw/                          # Normalized source content
│   └── {sanitized-title}.md
└── {YYYY-MM-DD}/                 # Date-stamped output
    ├── summary.md                # Korean summary with PM analysis
    ├── action-items.md           # Detailed action items + dashboard
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
5. Generate `output/meetings/2026-03-13/summary.md` with PM appendix
6. Generate `output/meetings/2026-03-13/action-items.md` with 9 items
7. Convert tables via `convert_tables.py`, upload 2 sub-pages to Notion
8. Verify both pages appear under default parent

Result: Complete meeting digest in `output/meetings/2026-03-13/` + Notion pages

### Example 2: Local file with PPTX and Slack

User says: `/meeting-digest --file output/meetings/raw/vc-pitch-preview.md --pptx --slack`

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

## Error Handling

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
