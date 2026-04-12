---
name: kb-collect-engineering
description: >-
  Daily collector for Engineering KB topics (engineering-standards, system-architecture).
  Scans repo for new/modified docs, tracks API changes, monitors incident reports,
  and collects engineering best practice content.
  Use when the user asks to "collect engineering data", "update engineering KB",
  "엔지니어링 KB 수집", "기술 문서 수집", "kb-collect-engineering",
  or when invoked by kb-daily-build-orchestrator.
  Do NOT use for design patterns (use kb-collect-design).
  Do NOT use for finance data (use kb-collect-finance).
  Korean triggers: "엔지니어링 KB 수집", "기술 문서 수집", "아키텍처 수집".
metadata:
  author: "thaki"
  version: "1.1.0"
  category: "execution"
  tags: ["knowledge-base", "engineering", "architecture", "daily-collector", "3-day-window"]
---

# KB Collect Engineering — Daily Engineering Intelligence Collector

Automated daily collector that scans the repository for documentation changes, API updates, and engineering content, then ingests into engineering-standards and system-architecture KBs.

## Prerequisites

- Git repository with recent commit history
- WebSearch tool available

## Collection Window

> **NEWS_WINDOW_DAYS=3** — External content searches (engineering best practices, RSS feeds) use a 3-day rolling window. Internal repo scans (git log for docs, APIs, ADRs) retain their 24-hour window.

## Deduplication (collector-side)

Before writing any raw file, check existing files in the target `raw/` directory from the last 3 days:

1. **Scan** all `*.md` files in `knowledge-bases/{topic}/raw/` with dates within the last 3 days (based on filename `{date}-` prefix).
2. **Parse YAML frontmatter** of each file to extract `source` (URL or file path) and `title`.
3. **Skip** writing a new file if either condition matches:
   - Same `source` URL/path already exists in any file from the last 3 days.
   - Same `title` (case-insensitive, trimmed) already exists in any file from the last 3 days.
4. **Track** the count of skipped items and report as `dedup_skipped` in the collector summary returned to the orchestrator.

> For git-sourced content (Phases 1-3): dedup by filename path in `source` field catches re-scans of unchanged docs.

## Workflow

### Phase 1: Repository Documentation Scan

1. Run `git log --since="24 hours ago" --name-only -- docs/ *.md` to find recently modified docs (internal source -- keeps 24h window).
2. For each modified documentation file:
   a. Read the file content.
   b. Create a KB raw entry with diff summary: `knowledge-bases/engineering-standards/raw/{date}-doc-update-{filename}.md`.

### Phase 2: API Change Detection

1. Run `git log --since="24 hours ago" --name-only -- backend/` to find backend changes.
2. Filter for route/handler/middleware changes.
3. If API changes detected, summarize in `knowledge-bases/system-architecture/raw/{date}-api-changes.md`.

### Phase 3: Architecture Decision Tracking

1. Scan for new ADR files (`git log --since="24 hours ago" --name-only -- **/ADR-*.md`).
2. Scan for new architecture docs.
3. Ingest any new ADRs into `knowledge-bases/system-architecture/raw/`.

### Phase 4: Engineering Content Collection

1. WebSearch for Go, Kubernetes, React best practices (from `social-feeds.yaml` → `engineering.rss_feeds`):
   - "Go best practices 2026"
   - "Kubernetes production patterns"
2. Monitor RSS feeds (kubernetes.io, go.dev/blog).
3. Save high-quality content to `knowledge-bases/engineering-standards/raw/{date}-eng-content.md` (only if substantial).

## Output Artifacts

| Phase | Output File | Description |
|-------|-------------|-------------|
| 1 | `knowledge-bases/engineering-standards/raw/{date}-doc-update-*.md` | Doc changes |
| 2 | `knowledge-bases/system-architecture/raw/{date}-api-changes.md` | API changes |
| 3 | `knowledge-bases/system-architecture/raw/{date}-adr-*.md` | New ADRs |
| 4 | `knowledge-bases/engineering-standards/raw/{date}-eng-content.md` | External content |

## Gotchas

- Skip collection if no git commits in the last 24 hours (no-op is fine).
- Large PRs may produce verbose diffs; summarize changes, don't copy full diffs.
- Filter out auto-generated files (lockfiles, compiled assets).
- External content searches (Phase 4) use 3-day window per `NEWS_WINDOW_DAYS`; internal git scans keep 24h.
