---
name: kb-collect-finance
description: >-
  Daily collector for Finance KB topic (finance-policies). Monitors SaaS
  financial metrics reports, cloud pricing changes, and regulatory updates.
  Use when the user asks to "collect finance data", "update finance KB", "재무
  KB 수집", "클라우드 가격 수집", "kb-collect-finance", or when invoked by
  kb-daily-build-orchestrator. Korean triggers: "재무 KB 수집", "가격 모니터링", "SaaS
  지표 수집".
---

# KB Collect Finance — Daily Finance Intelligence Collector

Automated daily collector for SaaS financial metrics, cloud pricing changes, and financial policy content.

## Prerequisites

- WebSearch tool available
- `knowledge-bases/competitive-intel/competitor-registry.yaml` for pricing page URLs

## Collection Window

> **NEWS_WINDOW_DAYS=3** — All external content searches (pricing pages, SaaS benchmarks, financial reports) use a 3-day rolling window. Cloud pricing changes are typically infrequent, so a wider window captures updates reliably.

## Deduplication (collector-side)

Before writing any raw file, check existing files in the target `raw/` directory from the last 3 days:

1. **Scan** all `*.md` files in `knowledge-bases/{topic}/raw/` with dates within the last 3 days (based on filename `{date}-` prefix).
2. **Parse YAML frontmatter** of each file to extract `source` (URL) and `title`.
3. **Skip** writing a new file if either condition matches:
   - Same `source` URL already exists in any file from the last 3 days.
   - Same `title` (case-insensitive, trimmed) already exists in any file from the last 3 days.
4. **Track** the count of skipped items and report as `dedup_skipped` in the collector summary returned to the orchestrator.

## Workflow

### Phase 1: Cloud Pricing Monitor

1. For major competitors (AWS, Azure, GCP, RunPod, Lambda), check pricing page changes via WebSearch.
2. Focus on GPU instance pricing, inference API pricing, and reserved instance offers.
3. Save to `knowledge-bases/finance-policies/raw/{date}-pricing-changes.md` (only if changes detected).

### Phase 2: SaaS Financial Content

1. WebSearch for SaaS financial benchmarks and reports:
   - "SaaS metrics benchmark 2026"
   - "cloud economics report"
   - "GPU cost optimization"
2. Save to `knowledge-bases/finance-policies/raw/{date}-finance-content.md` (only if substantial).

## Output Artifacts

| Phase | Output File | Description |
|-------|-------------|-------------|
| 1 | `knowledge-bases/finance-policies/raw/{date}-pricing-changes.md` | Pricing updates |
| 2 | `knowledge-bases/finance-policies/raw/{date}-finance-content.md` | Finance content |

## Gotchas

- Cloud pricing changes are infrequent (weekly/monthly); most days will be no-op.
- Focus on GPU/AI-specific pricing, not general cloud compute.
