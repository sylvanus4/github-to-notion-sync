## Dependency Audit

Scan Python, Go, and Node.js dependencies for CVEs, outdated packages, and abandoned libraries. Output a prioritized fix list.

### Usage

```
/dependency-audit                      # audit all package managers
/dependency-audit --python             # Python only
/dependency-audit --node               # Node.js only
/dependency-audit --go                 # Go only
/dependency-audit --fix                # auto-apply safe patch updates
```

### Workflow

1. **Scan** — Detect all dependency files (requirements.txt, package.json, go.mod)
2. **Audit** — Check for CVEs, outdated versions, and abandoned packages
3. **Classify** — Rank by severity (critical, high, moderate, low)
4. **Recommend** — Suggest safe patch updates vs. major updates needing review
5. **Report** — Prioritized fix list with upgrade commands and impact notes

### Execution

Read and follow the `dependency-auditor` skill (`.cursor/skills/review/dependency-auditor/SKILL.md`) for scanning, classification, and safe patch application.

### Examples

Full dependency audit:
```
/dependency-audit
```

Auto-fix safe patches:
```
/dependency-audit --fix --node
```
