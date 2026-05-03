---
name: ops-kpi-autopilot
description: >-
  Scheduled ops KPI dashboard from Notion + monitoring data. Use when "ops
  KPI", "운영 KPI", "ops dashboard". Do NOT use for business sales metrics (use
  sales-weekly-dashboard).
---

# ops-kpi-autopilot

## Overview
Scheduled L4 pipeline: queries Notion ops DBs + git commit stats + incident counts → computes KPIs → generates visual dashboard → posts to Slack + archives.

## Autonomy Level
**L4** — Runs on schedule without human trigger

## Skills Used
- kwp-data-interactive-dashboard-builder, visual-explainer, codebase-archaeologist, md-to-slack-canvas
