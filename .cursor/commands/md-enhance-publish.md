---
description: Enhance markdown with diagrams/tables/evidence, then publish to Notion and post summary to Slack
argument-hint: "<file-or-folder> [--parent <notion-page-id>] [--slack <channel-id>] [--dry-run]"
---

## md-enhance-publish

Enrich markdown documents with Mermaid diagrams, decision matrices, quantitative
evidence, and industry comparisons, then publish to Notion as structured sub-pages
and post a threaded summary to Slack.

### Usage

```
/md-enhance-publish <file.md>
/md-enhance-publish <folder/>
/md-enhance-publish <folder/> --parent <notion-page-id>
/md-enhance-publish <folder/> --parent <id> --slack <channel-id>
/md-enhance-publish <folder/> --dry-run
/md-enhance-publish <file.md> --skip-slack
/md-enhance-publish <folder/> --skip-notion --skip-slack
/md-enhance-publish <file.md> --lang en
```

### Options

| Option | Description |
|--------|-------------|
| (positional) | File path or folder path containing `.md` files |
| `--parent <id>` | Notion parent page ID (default: AI 자동 정리 page) |
| `--slack <channel_id>` | Slack channel ID (default: `C0AA8NT4T8T` = #효정-할일) |
| `--icon <emoji>` | Override auto-icon with uniform emoji |
| `--skip-slack` | Skip Slack posting |
| `--skip-notion` | Enhance files in place only (no Notion upload) |
| `--dry-run` | Show per-file enhancement plan without modifying |
| `--lang <ko\|en>` | Language for added content (default: `ko`) |

### Workflow

1. **Discover** — Collect `.md` files from path
2. **Analyze** — Identify enhancement opportunities (architecture, timeline, comparison, evidence)
3. **Enhance** — Add Mermaid diagrams, tables, metrics, comparisons in place
4. **Convert** — Transform pipe tables to Notion HTML, strip H1 title
5. **Publish** — Create Notion parent page + sub-pages via MCP
6. **Distribute** — Post summary to Slack with Notion links in thread

### Execution

Read and follow the `md-enhance-publish` skill:
`.cursor/skills/md-enhance-publish/SKILL.md`

### Examples

Enhance and publish a folder of Korean docs:
```
/md-enhance-publish docs/multi-cluster-centralization/ko/ \
  --parent 3209eddc34e6801b8921f55d85153730
```

Preview what enhancements would be applied:
```
/md-enhance-publish docs/platform-overview/ --dry-run
```

Enhance a single file, skip Slack:
```
/md-enhance-publish output/plans/release-plan.md --skip-slack
```

Enhance only (no Notion/Slack):
```
/md-enhance-publish docs/technical/ --skip-notion --skip-slack
```

Enhance with English additions:
```
/md-enhance-publish docs/multi-cluster-centralization/en/ --lang en
```

### Differences from Related Commands

| Command | What It Does | When to Use Instead |
|---------|-------------|---------------------|
| `/md-to-notion` | Upload markdown as-is to Notion | When you want raw upload without enhancement |
| `/nlm-slides` | Convert markdown to NotebookLM slides | When you need slide decks, not Notion pages |
| `/paper-review` | Full academic paper review pipeline | When you have a research paper to review |
| `/deep-research-pipeline` | Web research + multi-role analysis | When you need research first, not document enrichment |
