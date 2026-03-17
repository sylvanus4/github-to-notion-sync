---
description: Analyze meeting content (Notion page, file, or raw text) with PM sub-skills and produce Korean summaries with action items. Always uploads to Notion.
argument-hint: "<notion-url or --file path or --raw text>"
---

## Meeting Digest

Analyze any meeting content with multi-perspective PM sub-skills and produce structured Korean summaries with detailed action items. Automatically classifies meeting type, activates relevant PM analysis frameworks, and uploads results to Notion as two sub-pages (summary + action items).

### Usage

```
/meeting-digest <notion-url>
/meeting-digest --file <path>
/meeting-digest --raw "meeting content text"
/meeting-digest <notion-url> --pptx --slack
/meeting-digest --file <path> --type strategy
/meeting-digest --raw "..." --no-notion
/meeting-digest <notion-url> --notion-parent <custom-id>
```

### Options

| Option | Description |
|--------|-------------|
| (positional) | Notion page URL or page ID |
| `--file <path>` | Local file path (markdown or text) |
| `--raw` | Inline raw meeting content |
| `--pptx` | Generate PowerPoint presentation |
| `--slack [channel]` | Post digest to Slack (default: `#ai-platform-chapter-기획`) |
| `--no-notion` | Skip Notion upload (uploads by default) |
| `--notion-parent <id>` | Override default Notion parent page |
| `--type <type>` | Force meeting type: `discovery`, `strategy`, `gtm`, `sprint`, `operational` |

### Workflow

1. **Ingest** -- Fetch from Notion, read local file, or parse raw text
2. **Classify** -- Detect meeting type (discovery / strategy / gtm / sprint / operational)
3. **Analyze** -- Run parallel PM sub-skills based on meeting type
4. **Generate** -- Structured Korean summary + detailed action items
5. **Deliver** -- Save markdown files + upload to Notion; optionally generate PPTX, post to Slack

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

Analyze a Notion meeting page (auto-uploads to Notion):
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

Full output with custom Notion parent:
```
/meeting-digest https://notion.so/thakicloud/Board-Meeting-... --pptx --slack --notion-parent abc123...
```

Quick raw text analysis without Notion upload:
```
/meeting-digest --raw "오늘 미팅에서 Q3 로드맵을 논의했습니다. 참석자: 효정, 승우..." --no-notion
```

### Differences from Related Commands

| Command | What It Does | When to Use Instead |
|---------|-------------|---------------------|
| `/md-to-notion` | One-shot markdown-to-Notion publisher | When uploading arbitrary markdown without PM analysis |
| `/notion-meeting-sync` | Batch sync from Notion meeting DB | When syncing all meetings from the dedicated DB |
| `/pm-execution meeting` | Basic meeting transcript to notes | When you only need simple notes without PM analysis |
