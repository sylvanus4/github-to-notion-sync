---
name: kb-collect-design
description: >-
  Daily collector for Design KB topics (design-patterns). Monitors TDS component
  changes, design system updates, accessibility standards, and UX best practices.
  Use when the user asks to "collect design data", "update design KB",
  "디자인 KB 수집", "디자인 패턴 수집", "kb-collect-design",
  or when invoked by kb-daily-build-orchestrator.
  Do NOT use for engineering docs (use kb-collect-engineering).
  Korean triggers: "디자인 KB 수집", "디자인 패턴 수집", "TDS 수집".
metadata:
  author: "thaki"
  version: "1.1.0"
  category: "execution"
  tags: ["knowledge-base", "design", "tds", "daily-collector", "3-day-window"]
---

# KB Collect Design — Daily Design Intelligence Collector

Automated daily collector for design patterns, TDS component changes, and UX best practices.

## Prerequisites

- Git repository with TDS/design system files
- WebSearch tool available

## Collection Window

> **NEWS_WINDOW_DAYS=3** — External content searches (design system best practices, accessibility updates) use a 3-day rolling window. Internal repo scans (git log for TDS changes) retain their 24-hour window.

## Deduplication (collector-side)

Before writing any raw file, check existing files in the target `raw/` directory from the last 3 days:

1. **Scan** all `*.md` files in `knowledge-bases/{topic}/raw/` with dates within the last 3 days (based on filename `{date}-` prefix).
2. **Parse YAML frontmatter** of each file to extract `source` (URL or file path) and `title`.
3. **Skip** writing a new file if either condition matches:
   - Same `source` URL/path already exists in any file from the last 3 days.
   - Same `title` (case-insensitive, trimmed) already exists in any file from the last 3 days.
4. **Track** the count of skipped items and report as `dedup_skipped` in the collector summary returned to the orchestrator.

## Workflow

### Phase 1: TDS Component Change Scan

1. Run `git log --since="24 hours ago" --name-only -- .cursor/rules/frontend/ src/shared/` to find design system changes (internal source -- keeps 24h window).
2. Summarize any TDS rule or shared component changes.
3. Save to `knowledge-bases/design-patterns/raw/{date}-tds-changes.md` (only if changes found).

### Phase 2: Design Content Collection

1. WebSearch for design system and UX best practices:
   - "design system best practices 2026"
   - "accessibility WCAG updates"
   - "component library patterns"
2. Monitor `social-feeds.yaml` → `design.hashtags`.
3. Save to `knowledge-bases/design-patterns/raw/{date}-design-content.md` (only if substantial).

## Output Artifacts

| Phase | Output File | Description |
|-------|-------------|-------------|
| 1 | `knowledge-bases/design-patterns/raw/{date}-tds-changes.md` | TDS changes |
| 2 | `knowledge-bases/design-patterns/raw/{date}-design-content.md` | Design content |

## Gotchas

- Many days will have no TDS changes; that's normal, produce no output.
- Focus on actionable patterns, not generic design inspiration.
