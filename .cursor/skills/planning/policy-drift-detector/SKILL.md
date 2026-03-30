---
name: policy-drift-detector
description: >-
  Detect drift between policy documents in Notion and actual code/UI implementation:
  scan code for policy violations, compare UI strings to policy rules, check behaviors
  against constraints; produce severity-ranked drift reports and Slack alerts for critical issues.
  Korean triggers: "정책 드리프트", "정책 위반 감지", "정책 코드 불일치".
  English triggers: "policy drift", "policy violation scan", "policy-drift-detector".
  Do NOT use for generating compliant copy from policy alone (use policy-text-generator),
  or full document quality scoring without implementation scope (use doc-quality-gate).
metadata:
  version: "1.0.1"
  category: review
  author: thaki
---

# Policy Drift Detector

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

## Purpose

Compare **canonical policy text** (Notion) against **implementation reality** (codebase strings, feature flags, config, observable behaviors) and produce a **drift report** with **severity**, **evidence**, and **remediation**. Escalate **critical** drift via **Slack**.

## Prerequisites

- **Notion MCP**: policy page(s) or policy database; stable URLs or IDs.
- **Repository access**: read-only search (grep, codebase search) over UI strings, configs, and feature logic as scoped by the user.
- **Slack MCP**: channel or user destination for critical alerts.
- Optional: **ux-copy-audit** or **policy-text-generator** rubrics as cross-check references (concepts only—no external paths).

## Severity rubric

| Level | Definition | Example |
|-------|------------|---------|
| Critical | Legal/compliance risk or user harm | Prohibited data collected |
| High | Explicit policy rule violated in UI or default behavior | Wrong retention messaging |
| Medium | Ambiguity or partial compliance | Missing secondary disclosure |
| Low | Style or non-binding guidance mismatch | Wording not aligned with tone guide |

## Procedure

1. **Scope** — Define policy documents (Notion URLs), product surface (repo paths, apps), and timebox. Confirm whether **strings-only** or **behavioral** checks are in scope.

2. **Pull policy** — Fetch policy text via **Notion MCP**. Extract **must / must-not** rules, **definitions**, and **numeric thresholds** into a checklist (working notes may be English; **delivered report in Korean**).

3. **Scan implementation** — Search codebase for: user-visible strings, error messages, feature names, config keys, and guards related to the policy topics. Map each finding to a **rule ID** (derive from section headings).

4. **Compare** — For each rule: **pass**, **fail**, or **unknown**. Record **file path + snippet** (or Notion UI reference for product-only checks). Flag **contradictions** between multiple policies if detected.

5. **Report** — Produce a Korean markdown report: executive summary, findings table (severity, rule, evidence, remediation), and **backlog suggestions** (owner TBD).

6. **Slack** — For **Critical** or **High**: post **Slack MCP** message in Korean with count, top 3 titles, and link to full report (Notion page or pasted summary in thread).

7. **Notion archive** — Optionally create a child page under an agreed parent via **Notion MCP** using the team’s drift-log title pattern.

## Notion MCP usage

- Retrieve latest policy revision; note **last edited** timestamp in the report.
- Create or update a **drift log** page if the team maintains one.

## Slack MCP usage

- Critical alert: Korean headline, severity, impact summary, suggested immediate action, link to details.
- Avoid pasting secrets or PII from code snippets; paraphrase or redact.

## Output structure

Deliver in Korean: summary (qualitative or compliance overview); counts by severity; detail table (rule, evidence, recommended fix); repro/verification notes; suggested next scan date.

## Error handling

- If policy text is unstructured: infer rules conservatively and mark **low confidence** in Korean.
- If repo access is incomplete: list **unscanned areas** explicitly.

## Examples

- **Retention policy** says 30-day deletion; UI says “we keep data indefinitely” → **High** drift.
- **Marketing copy** outside scanned paths → **unknown** with scope gap note.

## Guardrails

- Do not auto-edit production code unless the user explicitly requests implementation.
- Distinguish **draft policy** vs **published** using Notion page status if available.
