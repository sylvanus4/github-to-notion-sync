---
name: gws-recipe-doc-from-template
description: >-
  Copy a Google Docs template, fill in content, and share with collaborators.
  Use when the user asks to create a document from a template, duplicate a
  template doc, or generate a doc with pre-filled content. Do NOT use for
  blank document creation (use gws-docs) or spreadsheet templates (use
  gws-sheets).
metadata:
  author: googleworkspace/cli (adapted)
  version: 1.0.0
---

# Recipe: Create a Google Doc from a Template

> **Required skills**: `gws-drive`, `gws-docs`

Copy a Google Docs template, fill in content, and share with collaborators.

## Steps

1. **Copy the template** via Drive:

```bash
gws drive files copy \
  --params '{"fileId": "TEMPLATE_DOC_ID"}' \
  --json '{"name": "Project Brief - Q2 Launch"}'
```

2. **Extract the new document ID** from the response (`id` field).

3. **Add content** to the new document:

```bash
gws docs +write --document NEW_DOC_ID \
  --text 'Project: Q2 Launch

Objective
Launch the new feature by end of Q2.

Timeline
- Phase 1: March
- Phase 2: April
- Launch: May'
```

Note: `+write` appends plain text. For structured formatting (headings, bold), use `docs documents batchUpdate` with formatting requests. For placeholder replacement in templates, use `replaceAllText`:

```bash
gws docs documents batchUpdate \
  --params '{"documentId": "DOC_ID"}' \
  --json '{"requests": [{"replaceAllText": {"containsText": {"text": "{{PROJECT}}", "matchCase": true}, "replaceText": "Q2 Launch"}}]}'
```

4. **Share with the team**:

```bash
gws drive permissions create \
  --params '{"fileId": "NEW_DOC_ID"}' \
  --json '{"role": "writer", "type": "user", "emailAddress": "team@company.com"}'
```

> **Write command** -- all steps modify Drive/Docs. Confirm template ID and sharing recipients with the user.

## Tips

- Use `gws drive files list --params '{"q": "name contains '\''template'\''"}'` to find templates
- For placeholder replacement, use `docs documents batchUpdate` with `replaceAllText` requests
- Consider sharing with a Google Group instead of individual users for team access
