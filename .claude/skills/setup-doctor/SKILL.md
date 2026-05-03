---
name: setup-doctor
description: Scan system prerequisites, environment variables, CLI tools, packages, and MCP servers, then produce a diagnostic pass/fail report.
disable-model-invocation: true
arguments: [scope]
---

Run diagnostic checks for `$scope` (all, infra, trading, research, frontend, etc.).

## Check Categories

1. **System Tools**: git, docker, kubectl, helm, node, pnpm, python, go, uv
2. **CLI Tools**: gh, gws, hf, tossctl, runpodctl, rtk
3. **Environment Variables**: API keys, tokens, credentials (existence check only)
4. **Python Packages**: Per skill group requirements
5. **Node Packages**: Global and project-level
6. **MCP Servers**: Connection status for configured servers
7. **Docker Services**: Running containers for dev stack

## Output

```markdown
## Setup Doctor Report
Scope: [scope]
Date: [YYYY-MM-DD]

### Summary: X/Y checks passed

### Failures
| Check | Status | Fix Command |
|-------|--------|-------------|
| ... | FAIL | `brew install ...` |

### Warnings
[Non-critical issues]

### All Passed
[List of passing checks]
```

## Rules

- Never display actual secret values — only check existence
- Provide exact fix commands for each failure
- Group checks by skill dependency
