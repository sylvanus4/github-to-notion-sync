---
description: Analyze meeting content (Notion page, file, or raw text) with PM sub-skills and produce Korean summaries with action items
argument-hint: "<notion-url or --file path or --raw text>"
---

## Meeting Digest

Analyze any meeting content with multi-perspective PM sub-skills and produce structured Korean summaries with detailed action items. Automatically classifies meeting type and activates relevant PM analysis frameworks.

### Usage

```
/meeting-digest <notion-url>
/meeting-digest --file <path>
/meeting-digest --raw "meeting content text"
/meeting-digest <notion-url> --pptx --slack
/meeting-digest <notion-url> --pptx --slack --notion
/meeting-digest --file <path> --type strategy
```

### Options

| Option | Description |
|--------|-------------|
| (positional) | Notion page URL or page ID |
| `--file <path>` | Local file path (markdown or text) |
| `--raw` | Inline raw meeting content |
| `--pptx` | Generate PowerPoint presentation |
| `--slack [channel]` | Post digest to Slack (default: `#ai-platform-chapter-기획`) |
| `--notion [parent-id]` | Create structured Notion page |
| `--type <type>` | Force meeting type: `discovery`, `strategy`, `gtm`, `sprint`, `operational` |

### Workflow

1. **Ingest** -- Fetch from Notion, read local file, or parse raw text
2. **Classify** -- Detect meeting type (discovery / strategy / gtm / sprint / operational)
3. **Analyze** -- Run parallel PM sub-skills based on meeting type
4. **Generate** -- Structured Korean summary + detailed action items
5. **Deliver** -- Save markdown files; optionally generate PPTX, post to Slack, create Notion page

### Meeting Types

| Type | Activated Analysis | Trigger Signals |
|------|-------------------|-----------------|
| discovery | Assumption identification, interview synthesis | User interview, hypothesis, validation |
| strategy | SWOT analysis, value proposition | Strategy, competitive, pricing, VC pitch |
| gtm | GTM strategy, ICP definition | Launch, sales, marketing, go-to-market |
| sprint | Sprint planning, retrospective | Sprint, backlog, retro, velocity |
| operational | Core summary only | General sync, status update |

### Execution

Read and follow the `meeting-digest` skill (`.cursor/skills/meeting-digest/SKILL.md`) for pipeline phases, PM skill composition, and output templates.

### Examples

Analyze a Notion meeting page:
```
/meeting-digest https://notion.so/thakicloud/VC-Pitch-Preview-3219eddc...
```

Analyze a local transcript with PPTX and Slack:
```
/meeting-digest --file output/meetings/raw/vc-pitch-preview.md --pptx --slack
```

Force strategy analysis on a Notion page:
```
/meeting-digest --type strategy https://notion.so/thakicloud/Weekly-Sync-...
```

Full output (PPTX + Slack + Notion page):
```
/meeting-digest https://notion.so/thakicloud/Board-Meeting-... --pptx --slack --notion
```

Quick raw text analysis:
```
/meeting-digest --raw "오늘 미팅에서 Q3 로드맵을 논의했습니다. 참석자: 효정, 승우..."
```

### Differences from Related Commands

| Command | What It Does | When to Use Instead |
|---------|-------------|---------------------|
| `/notion-meeting-sync` | Batch sync from Notion meeting DB | When syncing all meetings from the dedicated DB |
| `/pm-execution meeting` | Basic meeting transcript to notes | When you only need simple notes without PM analysis |
