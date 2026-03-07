---
name: gws-recipe-audit-sharing
description: >-
  Find and review Google Drive files shared outside the organization, with
  option to revoke external access. Use when the user asks to audit external
  sharing, find publicly shared files, review Drive permissions, or check
  for data leaks. Do NOT use for internal permission management (use
  gws-drive) or compliance documentation (use compliance-governance).
metadata:
  author: googleworkspace/cli (adapted)
  version: 1.0.0
---

# Recipe: Audit External Drive Sharing

> **Required skills**: `gws-drive`

Find and review Google Drive files shared outside the organization.

> **CAUTION**: Revoking permissions immediately removes access. Confirm with the file owner first.

## Steps

1. **List externally shared files**:

```bash
gws drive files list \
  --params '{"q": "visibility = '\''anyoneWithLink'\''"}' \
  --fields "files(id,name,owners,webViewLink)"
```

2. **Check permissions** on a specific file:

```bash
gws drive permissions list \
  --params '{"fileId": "FILE_ID"}' \
  --fields "permissions(id,type,role,emailAddress)"
```

3. **Revoke external access** if needed:

```bash
gws drive permissions delete \
  --params '{"fileId": "FILE_ID", "permissionId": "PERM_ID"}' --dry-run
```

Remove `--dry-run` only after confirming with the file owner.

> **Destructive command** -- always use `--dry-run` first, and confirm with the user before actual deletion.

## Tips

- Use `--page-all` to paginate through all shared files in large organizations
- Filter by owner: add `"and 'user@company.com' in owners"` to the query
- Export results: pipe to `jq` for structured reports
- For domain-wide audits, use a service account with domain-wide delegation
