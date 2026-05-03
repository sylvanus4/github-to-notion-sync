---
name: dependency-auditor
description: Audit and update Python, Go, and Node.js dependencies. Scan for CVEs, classify severity, apply safe patch updates, and generate impact reports.
disable-model-invocation: true
---

# Dependency Auditor

Manages dependencies across the polyglot stack.

## Dependency Map

| Stack | Files | Manager |
|-------|-------|---------|
| Python | `services/*/pyproject.toml`, `shared/python/pyproject.toml` | pip / uv |
| Go | `services/call-manager/go.mod` | go mod |
| Node.js | `frontend/package.json` | pnpm |

## Scan Commands

```bash
# Python
pip-audit --requirement requirements.txt
safety check

# Go
govulncheck ./...

# Node.js
pnpm audit
```

## Severity Classification

| Level | Action | Timeline |
|-------|--------|----------|
| CRITICAL | Patch immediately | Same day |
| HIGH | Patch this sprint | Within 1 week |
| MEDIUM | Schedule update | Within 1 month |
| LOW | Track only | Next major update |

## Safe Update Strategy

1. **Patch updates**: Apply automatically (e.g., 1.2.3 → 1.2.4)
2. **Minor updates**: Apply with test verification (e.g., 1.2.x → 1.3.0)
3. **Major updates**: Generate impact report, require manual approval

## Output Format

1. Vulnerability summary (by severity)
2. Outdated packages list
3. Safe update commands
4. Breaking change warnings
5. Recommended action plan

Do NOT use for: security threat modeling (use security-expert), CI pipeline (use ci-quality-gate).
