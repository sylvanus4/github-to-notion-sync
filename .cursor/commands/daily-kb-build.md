## Daily KB Build — Role-Based Wiki Pipeline

Run the daily Knowledge Base collection, compilation, and reporting pipeline. Triggers all 7 role-specific collectors (sales, marketing, PM, engineering, design, finance, research) in parallel, compiles updated topics into wiki format, and posts a consolidated Korean intelligence report to `#효정-의사결정`.

### Usage

```
# Full pipeline (collect + compile + report)
/daily-kb-build

# Collection only, skip compilation and report
/daily-kb-build --collect-only

# Compile only (no new collection) + report
/daily-kb-build --compile-only

# Run specific role collectors only
/daily-kb-build --roles sales,pm,marketing

# Skip specific roles
/daily-kb-build --skip-roles finance,design

# Full pipeline but skip Slack report
/daily-kb-build --skip-report
```

### What It Does

1. **Pre-flight**: Verifies config files and MCP connectivity
2. **Collect** (parallel): Dispatches 7 role-specific collectors
   - Sales: competitor pages, G2 reviews, industry news, social signals
   - Marketing: competitor content, SEO trends, benchmarks, brand reference
   - PM: Notion meeting notes (3 databases), competitor features, sprint data
   - Engineering: repo doc changes, API changes, ADRs
   - Design: TDS changes, design content
   - Finance: cloud pricing changes, SaaS metrics
   - Research: HF papers, arXiv, community signals
3. **Compile**: Rebuilds wiki articles for topics with new raw files
4. **Quality**: Runs kb-lint health check on updated topics
5. **Report**: Generates collection summary and build report
6. **Intelligence Digest**: Synthesizes findings per role, posts 3-message Slack thread to `#효정-의사결정` with key findings and decision items

### Output

- `outputs/kb-daily-build/{date}/collection-summary.md` — What was collected
- `outputs/kb-daily-build/{date}/build-report.md` — Final compilation report
- `outputs/kb-daily-build/{date}/intelligence-report.md` — Korean intelligence digest
- Slack thread in `#효정-의사결정` — Consolidated daily intelligence with decision items

### Integration

This command is designed to be wired into the daily-pm-orchestrator as Phase 1.5, or scheduled via Cursor Automation at 4:00 PM daily.

### Skill

`kb-daily-build-orchestrator`
