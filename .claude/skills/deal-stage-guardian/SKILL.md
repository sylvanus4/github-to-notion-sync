---
name: deal-stage-guardian
description: >-
  Monitor Notion pipeline DB for stage changes, enforce checklist completion,
  auto-generate handoff docs, notify teams, track SLA. Use when "deal stage",
  "stage transition", "딜 스테이지", "핸드오프". Do NOT use for single deal analysis
  (use kwp-sales-account-research).
---

# deal-stage-guardian

## Overview
Monitors Notion CRM pipeline for stage transitions. On each stage change, enforces checklist completion, generates handoff documentation for the next stage, notifies relevant teams, and tracks SLA compliance.

## Autonomy Level
**L3** — AI executes on stage change detection, human reviews handoff docs

## Pipeline Architecture
Sequential — Notion DB watch → detect stage change → enforce checklist → generate handoff → notify → track SLA

## Skills Used
- pm-execution
- kwp-product-management-stakeholder-comms
- md-to-notion
