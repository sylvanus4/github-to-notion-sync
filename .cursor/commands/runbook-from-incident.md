---
description: Reads a postmortem, extracts the resolution procedure, and generates a reusable runbook template.
argument-hint: "<postmortem-url or --file path>"
---

# /runbook-from-incident

Reads a postmortem document, extracts the incident type and resolution steps, generalizes the procedure into a reusable runbook template, and publishes to Notion KB and Cognee KG.

## What This Command Does

Accepts a postmortem URL or file path, extracts the incident type and resolution procedure, generalizes steps into a template format with pre-conditions and verification steps, creates a runbook document, indexes it in Cognee knowledge graph, and publishes to Notion KB.

## Required Input

- **Postmortem** — URL to postmortem page or `--file <path>` to local file.

## Execution Steps

1. **Accept postmortem URL or file path** — Fetch or read postmortem content.
2. **Extract incident type and resolution steps** — Parse postmortem for root cause, resolution procedure, and key decisions.
3. **Generalize procedure into template** — Convert incident-specific steps to reusable format.
4. **Add pre-conditions, verification steps** — Include prerequisites and success checks.
5. **Create runbook document** — Use technical-writer and kwp-engineering-documentation for structure.
6. **Index in Cognee KG** — Add runbook to Cognee for future retrieval.
7. **Publish to Notion KB** — Upload runbook via md-to-notion to knowledge base.

## Output

- Runbook markdown document
- Cognee KG index entry
- Notion KB page

## Skills Used

- technical-writer: Runbook structure and formatting
- cognee: Knowledge graph indexing
- md-to-notion: Notion publishing
- kwp-engineering-documentation: Runbook best practices

## Example Usage

```
/runbook-from-incident https://notion.so/thakicloud/Postmortem-2026-03-15-abc123
/runbook-from-incident --file output/incidents/postmortem-2026-03-15.md
```
