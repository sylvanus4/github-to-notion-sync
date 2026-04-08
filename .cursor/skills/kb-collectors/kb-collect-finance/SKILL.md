---
name: kb-collect-finance
description: >-
  Daily collector for Finance KB topic (finance-policies). Monitors SaaS financial
  metrics reports, cloud pricing changes, and regulatory updates.
  Use when the user asks to "collect finance data", "update finance KB",
  "재무 KB 수집", "클라우드 가격 수집", "kb-collect-finance",
  or when invoked by kb-daily-build-orchestrator.
  Korean triggers: "재무 KB 수집", "가격 모니터링", "SaaS 지표 수집".
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "execution"
  tags: ["knowledge-base", "finance", "pricing", "daily-collector"]
---

# KB Collect Finance — Daily Finance Intelligence Collector

Automated daily collector for SaaS financial metrics, cloud pricing changes, and financial policy content.

## Prerequisites

- WebSearch tool available
- `knowledge-bases/competitive-intel/competitor-registry.yaml` for pricing page URLs

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
