---
name: kb-collect-pm
description: >-
  Daily collector for Product Management KB topics (product-strategy, prd-library).
  Syncs new meeting notes from 3 Notion databases (AI Platform, Cross-Team, Company-Wide),
  collects competitor feature updates, and gathers product management content.
  Use when the user asks to "collect PM data", "sync meeting notes",
  "PM KB 수집", "회의록 동기화", "프로덕트 KB 수집", "kb-collect-pm",
  or when invoked by kb-daily-build-orchestrator.
  Do NOT use for sales data (use kb-collect-sales).
  Do NOT use for marketing content (use kb-collect-marketing).
  Korean triggers: "PM KB 수집", "회의록 동기화", "프로덕트 데이터 수집".
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "execution"
  tags: ["knowledge-base", "product-management", "notion-sync", "daily-collector"]
---

# KB Collect PM — Daily Product Management Collector

Automated daily collector that syncs Notion meeting notes and gathers product management intelligence into the product-strategy and prd-library Knowledge Bases.

## Prerequisites

- `knowledge-bases/_config/notion-meeting-sync.yaml` — Notion database IDs and sync config
- Notion MCP server connected and authenticated
- WebSearch tool available

## Workflow

### Phase 1: Notion Meeting Notes Sync

Read `notion-meeting-sync.yaml` for database configurations. For each database:

1. **Query Notion database** using Notion MCP `notion_query_database` with filter for entries created/modified in the last 24 hours.
2. For each new/updated entry:
   a. Fetch full page content via `notion_get_page_content`.
   b. Convert to clean markdown with YAML frontmatter:
   ```yaml
   ---
   title: "{meeting_title}"
   source: "notion:{database_id}/{page_id}"
   date_collected: "YYYY-MM-DD"
   content_type: "meeting-notes"
   meeting_type: "{daily-scrum|sprint-planning|retro|ad-hoc|cross-team|all-hands}"
   database: "{ai_platform_meetings|cross_team_meetings|company_wide_meetings}"
   ---
   ```
   c. Save to `knowledge-bases/product-strategy/raw/{date}-{meeting_type}-{slug}.md`.

### Phase 2: Competitor Feature Tracking

1. WebSearch for competitor product updates (last 24 hours):
   - "{competitor} new feature release 2026"
   - "{competitor} product update announcement"
2. Focus on direct competitors from `competitor-registry.yaml` (ai_platform and agent_studio categories).
3. Save to `knowledge-bases/product-strategy/raw/{date}-competitor-features.md` (only if new content found).

### Phase 3: PM Content Collection

1. WebSearch for product management thought leadership:
   - "AI product management best practices"
   - "platform product strategy"
2. Collect only high-quality, actionable content.
3. Save to `knowledge-bases/prd-library/raw/{date}-pm-content.md` (only if substantial new content).

### Phase 4: Sprint & OKR Signal Collection

1. Check GitHub for recent sprint-related activity (issues, PRs with sprint labels).
2. Compile a daily sprint signal summary.
3. Save to `knowledge-bases/product-strategy/raw/{date}-sprint-signals.md`.

## Output Artifacts

| Phase | Output File | Description |
|-------|-------------|-------------|
| 1 | `knowledge-bases/product-strategy/raw/{date}-{type}-{slug}.md` | Meeting notes |
| 2 | `knowledge-bases/product-strategy/raw/{date}-competitor-features.md` | Feature updates |
| 3 | `knowledge-bases/prd-library/raw/{date}-pm-content.md` | PM content |
| 4 | `knowledge-bases/product-strategy/raw/{date}-sprint-signals.md` | Sprint signals |

## Gotchas

- Notion MCP must be authenticated; check with `notion_search` before querying databases.
- Meeting notes may contain sensitive internal data; keep within the KB system, do not post to Slack.
- Large meetings (all-hands) may exceed context; summarize key decisions and action items.
- The 24-hour filter uses `Created` property; some DBs may use `Last Edited` instead.
