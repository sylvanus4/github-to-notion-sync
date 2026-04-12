---
description: Convert a sprint retrospective Notion page into tracked GitHub issues on Project #5. Fetches content, runs PM analysis, extracts action items, applies quality critique, and creates issues with full project field setup.
argument-hint: "<notion-url> [--skip-analysis] [--skip-critique] [--dry-run] [--assignee username]"
---

## Sprint Retro-to-Issues

End-to-end pipeline that converts sprint retrospective meetings into tracked GitHub work items.

### Usage

```
/sprint-retro-to-issues <notion-url>
/sprint-retro-to-issues <notion-url> --dry-run
/sprint-retro-to-issues <notion-url> --skip-analysis --assignee sylvanus4
```

### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `notion-url` | Yes | — | Notion page URL containing the sprint retrospective |
| `--assignee` | No | `sylvanus4` | GitHub username for issue assignment |
| `--dry-run` | No | off | Preview issues without creating them on GitHub |
| `--skip-analysis` | No | off | Skip PM analysis (Phase 2), use raw content directly |
| `--skip-critique` | No | off | Skip quality gate (Phase 4), create issues from raw extraction |

### Pipeline Phases

1. **Collect** — Fetch Notion page with transcript via MCP
2. **Analyze** — Multi-perspective PM analysis (retrospective, process gaps, tech debt)
3. **Extract** — Structure action items with priority, size, acceptance criteria
4. **Critique** — Adversarial quality gate scoring 5 dimensions (completeness, clarity, actionability, traceability, feasibility)
5. **Create Issues** — `gh issue create` + Project #5 field setup (Status, Priority, Size, Estimate, Sprint)
6. **Report** — Korean summary to `report.md` + Slack thread to `#효정-할일`

### Output

All artifacts are persisted to `outputs/sprint-retro-to-issues/{date}/`:

- `phase-{N}-{name}.json` — Per-phase structured results
- `action-items.md` — Extracted action items in Korean
- `report.md` — Final summary report with GitHub issue links
- `manifest.json` — Pipeline execution metadata

### Examples

Full pipeline with quality gate:
```
/sprint-retro-to-issues https://www.notion.so/thakicloud/26-04-Sprint2-ing-33a9eddc34e680efaca6dbbac8641138
```

Preview what would be created without actually creating issues:
```
/sprint-retro-to-issues https://www.notion.so/thakicloud/26-04-Sprint2-ing-33a9eddc34e680efaca6dbbac8641138 --dry-run
```

Skip analysis and critique for fast issue creation:
```
/sprint-retro-to-issues https://www.notion.so/thakicloud/... --skip-analysis --skip-critique
```

### Skill

This command invokes the `sprint-retro-to-issues` skill at `.cursor/skills/pipeline/sprint-retro-to-issues/SKILL.md`.

### Prerequisites

- `gh` CLI authenticated with `repo` and `project` scopes
- Notion MCP server authenticated
- Slack MCP server available
- Access to ThakiCloud GitHub org and Project #5
