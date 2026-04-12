---
name: kb-daily-build-orchestrator
description: >-
  Master orchestrator for the Role-Based Knowledge Wiki daily pipeline.
  Triggers all 7 role-specific collector skills in parallel batches,
  then runs kb-compile and kb-index on updated topics.
  Single daily trigger builds the entire wiki knowledge system and
  posts a consolidated Korean intelligence report to Slack #효정-의사결정.
  Use when the user asks to "build daily KB", "run KB pipeline",
  "daily KB build", "위키 빌드", "일일 KB 빌드", "kb-daily-build",
  "/daily-kb-build", or when invoked by daily-pm-orchestrator.
  Do NOT use for individual collector runs (invoke kb-collect-* directly).
  Do NOT use for manual KB operations (use kb-orchestrator).
  Korean triggers: "일일 KB 빌드", "위키 빌드", "KB 파이프라인".
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "orchestrator"
  tags: ["knowledge-base", "orchestrator", "daily-pipeline", "wiki-rag", "slack-report"]
---

# KB Daily Build Orchestrator — Role-Based Wiki Pipeline

Master orchestrator that runs all role-specific Knowledge Base collectors in parallel, compiles updated topics into wiki format, and posts a consolidated Korean intelligence report to Slack `#효정-의사결정`. Designed as a single daily trigger point.

## Prerequisites

- All 7 `kb-collect-*` skills installed
- `knowledge-bases/competitive-intel/competitor-registry.yaml` exists
- `knowledge-bases/_config/social-feeds.yaml` exists
- `knowledge-bases/_config/notion-meeting-sync.yaml` exists
- Notion MCP server connected (for kb-collect-pm)
- WebSearch available
- defuddle API available
- Slack MCP server connected (for Phase 6 report posting)

## Input

```
/daily-kb-build                     # Full pipeline (all roles + compile + report)
/daily-kb-build --collect-only      # Collection only, skip compile and report
/daily-kb-build --compile-only      # Skip collection, compile existing raw/ + report
/daily-kb-build --roles sales,pm    # Only specific role collectors
/daily-kb-build --skip-compile      # Alias for --collect-only
/daily-kb-build --skip-report       # Full pipeline but skip Slack report
```

## Workflow

### Phase 1: Pre-flight Check (sequential)

1. Verify config files exist:
   - `knowledge-bases/competitive-intel/competitor-registry.yaml`
   - `knowledge-bases/_config/social-feeds.yaml`
   - `knowledge-bases/_config/notion-meeting-sync.yaml`
2. Check Notion MCP connectivity (required for PM collector).
3. Set `DATE=$(date +%Y-%m-%d)` for consistent filenames.
4. Log start time to `outputs/kb-daily-build/{DATE}/run-log.jsonl`.

### Phase 2: Role Collector Dispatch (parallel — 2 batches)

**Batch A** (3 parallel subagents — heavier collectors):
- `kb-collect-sales` — Competitor scraping, G2 reviews, social signals
- `kb-collect-marketing` — Content monitoring, SEO trends, brand reference
- `kb-collect-pm` — Notion meeting sync, competitor features, sprint signals

**Batch B** (4 parallel subagents — lighter collectors):
- `kb-collect-engineering` — Repo doc scan, API changes, ADRs
- `kb-collect-design` — TDS changes, design content
- `kb-collect-finance` — Pricing monitor, SaaS metrics
- `kb-collect-research` — HF papers, arXiv, community signals

Each subagent:
1. Reads the appropriate SKILL.md for instructions.
2. Executes all phases within the collector.
3. Returns a summary: `{files_created: N, topics_updated: [...], errors: [...]}`.

### Phase 3: Collection Summary (sequential)

1. Aggregate results from all 7 collectors.
2. Write summary to `outputs/kb-daily-build/{DATE}/collection-summary.md`:
   ```markdown
   # KB Daily Collection Summary — {DATE}

   | Role | Files Created | Topics Updated | Errors |
   |------|--------------|----------------|--------|
   | Sales | N | competitive-intel, sales-playbook | ... |
   | Marketing | N | brand-guidelines, marketing-playbook, content-library | ... |
   | ... | ... | ... | ... |

   Total new raw files: NN
   ```
3. Identify which KB topics have new raw files (need recompilation).

### Phase 4: Wiki Compilation (parallel per topic)

Skip if `--collect-only` flag is set.

For each KB topic with new raw files:
1. Run `kb-compile` to regenerate wiki articles from raw sources.
2. Run `kb-index` to rebuild index, summary, concept-map, and glossary.

Parallelize across topics (max 4 concurrent compilations).

### Phase 5: Quality Check (sequential)

1. Run `kb-lint` on compiled topics to check consistency.
2. Write build report to `outputs/kb-daily-build/{DATE}/build-report.md`.
3. Log completion time and duration to `run-log.jsonl`.

### Phase 6: Intelligence Report & Distribute (sequential)

Invoke `kb-daily-report` skill with collected context:

1. **Gather**: Read collection summary, scan updated wiki articles
2. **Extract**: Up to 3 key findings per role domain with urgency ratings
3. **Decide**: Identify decision-worthy items requiring human action
4. **Format**: Build 3-message Slack thread (overview → role details → decision items)
5. **Post**: Send to `#효정-의사결정` (`C0ANBST3KDE`)
6. **Persist**: Save full report to `outputs/kb-daily-build/{DATE}/intelligence-report.md`

Skip this phase if `--collect-only` or `--skip-report` flag is set.

## Output Artifacts

| Phase | Output File | Description |
|-------|-------------|-------------|
| 1 | `outputs/kb-daily-build/{DATE}/run-log.jsonl` | Execution log |
| 3 | `outputs/kb-daily-build/{DATE}/collection-summary.md` | Collection results |
| 5 | `outputs/kb-daily-build/{DATE}/build-report.md` | Final build report |
| 6 | `outputs/kb-daily-build/{DATE}/intelligence-report.md` | Korean intelligence digest |
| 6 | Slack thread in `#효정-의사결정` | 3-message intelligence thread |

## Error Recovery

- If a collector fails, other collectors continue; failure is logged.
- If kb-compile fails for a topic, other topics continue; manual recompile needed.
- If Notion MCP is unreachable, skip kb-collect-pm and log warning.
- If Slack MCP is unavailable, save intelligence report to file only and log warning.
- Resume: check `run-log.jsonl` for last completed phase and restart from there.

## Integration Points

- **daily-pm-orchestrator**: Wire as Phase 1.5 (after knowledge consolidation, before strategic analysis).
- **Cursor Automation**: Schedule as a daily cron at 4:00 PM.
- **Manual**: Run `/daily-kb-build` anytime.

## Gotchas

- First run after bootstrap may compile many topics; expect 10-15 minutes.
- Subsequent daily runs are incremental; typically 2-5 minutes.
- Notion rate limits: max ~3 requests/second; PM collector handles this.
- Use `--roles` flag to debug individual collectors without running the full pipeline.
