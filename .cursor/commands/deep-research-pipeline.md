---
description: Run deep web research, 12-role cross-perspective analysis, and publish all results to Notion
argument-hint: "<research topic>"
---

## Deep Research Pipeline

End-to-end pipeline that chains deep web research, 12-role multi-perspective
analysis with CEO executive briefing, and Notion publishing into a single flow.

### Usage

```
/deep-research-pipeline <research topic>
/deep-research-pipeline <topic> --roles cto,pm,cso
/deep-research-pipeline <topic> --skip hr,finance
/deep-research-pipeline <topic> --processor ultra-fast
/deep-research-pipeline <topic> --parent <notion-page-id>
```

### Options

| Option | Description |
|--------|-------------|
| (positional) | Research topic in natural language |
| `--parent <id>` | Notion parent page ID (default: AI 자동 정리 page) |
| `--roles <list>` | Analyze only specific roles (comma-separated) |
| `--skip <list>` | Skip specific roles (comma-separated) |
| `--processor <tier>` | parallel-cli tier: `pro-fast` (default), `ultra-fast`, `ultra` |

### Workflow

1. **Deep Research** — Run `parallel-cli` to produce a comprehensive research report
2. **Role Dispatch** — Feed research findings to 12 role-perspective analyzers, synthesize CEO executive briefing
3. **Notion Publish** — Create a hub page with sub-pages for research report, executive briefing, and role analyses

### Execution

Read and follow the `deep-research-pipeline` skill:
`.cursor/skills/deep-research-pipeline/SKILL.md`

### Examples

Research a technology topic with full pipeline:
```
/deep-research-pipeline NVIDIA Vera Rubin LPU architecture and its impact on AI cloud infrastructure
```

Research with specific roles only:
```
/deep-research-pipeline Kubernetes GPU scheduling evolution --roles cto,developer,cso
```

Research with higher depth:
```
/deep-research-pipeline LPU vs GPU inference cost comparison 2027 --processor ultra-fast
```

### Differences from Related Commands

| Command | What It Does | When to Use Instead |
|---------|-------------|---------------------|
| `/role-dispatch` | Multi-role analysis without prior research | When you already have context and don't need web research |
| `/plans` | Prompt optimization + execution planning | When you need a skill-based execution plan, not research |
| `/deep-research` | Deep web research only (no role analysis) | When you only need the research report |
