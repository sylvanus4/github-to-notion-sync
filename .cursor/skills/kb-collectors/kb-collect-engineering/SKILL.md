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
  version: "1.0.0"
  category: "execution"
  tags: ["knowledge-base", "engineering", "architecture", "daily-collector"]
---

# KB Collect Engineering — Daily Engineering Intelligence Collector

Automated daily collector that scans the repository for documentation changes, API updates, and engineering content, then ingests into engineering-standards and system-architecture KBs.

## Prerequisites

- Git repository with recent commit history
- WebSearch tool available

## Workflow

### Phase 1: Repository Documentation Scan

1. Run `git log --since="24 hours ago" --name-only -- docs/ *.md` to find recently modified docs.
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
