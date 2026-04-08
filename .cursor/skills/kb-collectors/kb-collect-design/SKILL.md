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
  version: "1.0.0"
  category: "execution"
  tags: ["knowledge-base", "design", "tds", "daily-collector"]
---

# KB Collect Design — Daily Design Intelligence Collector

Automated daily collector for design patterns, TDS component changes, and UX best practices.

## Prerequisites

- Git repository with TDS/design system files
- WebSearch tool available

## Workflow

### Phase 1: TDS Component Change Scan

1. Run `git log --since="24 hours ago" --name-only -- .cursor/rules/frontend/ src/shared/` to find design system changes.
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
