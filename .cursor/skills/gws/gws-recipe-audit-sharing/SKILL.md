---
name: gws-recipe-audit-sharing
description: >-
  Find and review Google Drive files shared outside the organization, with
  option to revoke external access. Use when the user asks to audit external
  sharing, find publicly shared files, review Drive permissions, or check for
  data leaks. Do NOT use for internal permission management (use gws-drive) or
  compliance documentation (use compliance-governance). Korean triggers: "외부 공유", "권한 감사".
metadata:
  author: "googleworkspace/cli (adapted)"
  version: "1.0.0"
  category: "integration"
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

## Examples

### Example 1: Basic operation

**User says:** "Audit external sharing"

**Actions:**
1. Verify `gws` CLI is authenticated (`gws drive files list 2>&1 | head -3`)
2. Execute the appropriate `gws` command with required parameters
3. Confirm the result and report back

### Example 2: Troubleshooting

**User says:** "The command failed with an authentication error"

**Actions:**
1. Verify `GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE` is set: `echo $GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE`
2. Re-authenticate: `python3 ~/.config/gws/oauth2_manual.py`
3. Clean stale caches: `rm -f ~/.config/gws/token_cache.json ~/.config/gws/credentials.enc`
4. Retry the original command
## Error Handling

| Issue | Resolution |
|-------|-----------|
| Authentication error | Run `python3 ~/.config/gws/oauth2_manual.py` and clean caches (`rm -f ~/.config/gws/token_cache.json ~/.config/gws/credentials.enc`) |
| API rate limit | Wait and retry. For bulk operations, add delays between requests |
| Resource not found | Verify the resource ID/name and check permissions |
