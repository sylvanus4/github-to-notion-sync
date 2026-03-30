# PR Review Captain — Reference

## PR Title Convention (from CONTRIBUTING.md)

```
#<ISSUE_NUMBER> [<TYPE>] <Summary>
```

Types: `feat`, `enhance`, `refactor`, `docs`, `fix`, `style`, `test`, `chore`

Examples:
- `#123 [feat] Add user authentication system`
- `#456 [fix] Resolve race condition in call-manager WebSocket`
- `#789 [enhance] Improve RAG query performance with hybrid search`

## Commit Message Convention

```
[<TYPE>] <Summary>          ← max 50 chars, imperative, English

- Detail line 1             ← wrap at 72 chars
- Detail line 2             ← Korean or English
```

## Review Comment Templates

### Critical Issue

```markdown
**critical.must** — [Brief title]

**Problem**: [What is wrong and why it matters]

**Location**: `file.py:42`

**Suggested fix**:
\`\`\`python
# corrected code
\`\`\`

**Reference**: [link to docs/standard if applicable]
```

### High Recommendation

```markdown
**high.imo** — [Brief title]

This could cause [problem] in [scenario].

Consider:
\`\`\`python
# recommended approach
\`\`\`
```

### Question

```markdown
**info.q** — [Brief question]

I'm not sure I understand [aspect]. Could you clarify [specific question]?
```

## Release Note Writing Tips

1. **Write for users, not developers** — focus on outcomes, not implementation
2. **Be specific** — "Fixed login timeout on slow connections" not "Fixed auth bug"
3. **Group related changes** — if 3 PRs improved RAG performance, combine into one entry
4. **Highlight breaking changes** with migration instructions
5. **Credit contributors** by GitHub username

## Automated Release Note Generation

Using `gh` CLI to collect PRs since last tag:

```bash
# Find last release tag
LAST_TAG=$(gh release list --limit 1 --json tagName --jq '.[0].tagName')

# List merged PRs since last tag
gh pr list --state merged --base main \
  --search "merged:>=$(git log -1 --format=%aI $LAST_TAG)" \
  --json number,title,author,labels \
  --jq '.[] | "#\(.number) \(.title) @\(.author.login)"'
```

## File Path to Service Mapping

| Path pattern | Service | Review focus |
|-------------|---------|-------------|
| `services/call-manager/` | call-manager (Go) | WebSocket, goroutine safety |
| `services/stt-pipeline/` | stt-pipeline | Audio processing, PII masking |
| `services/rag-engine/` | rag-engine | Vector search, embedding quality |
| `services/llm-inference/` | llm-inference | Prompt safety, token limits |
| `services/admin/` | admin | RBAC, tenant isolation |
| `services/pii-redaction/` | pii-redaction | PII patterns, data leakage |
| `frontend/` | React app | Accessibility, performance |
| `db/migrations/` | Database | Migration safety, locks |
| `infra/` | Infrastructure | Resource limits, security |
| `shared/python/` | Shared library | Breaking changes to consumers |
