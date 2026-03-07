## Release Commander

Full release lifecycle pipeline: code review, security scan, test validation, performance check, i18n sync, dependency audit, changelog, commits, and PR — orchestrating 10 skills.

### Usage

```
/release-commander                              # full pipeline
/release-commander --skip security,i18n         # skip specific checks
/release-commander --dry-run                    # validation only, no commits/PR
/release-commander --base release-v1.2          # specify PR base branch
/release-commander --changelog-only             # generate changelog only
```

### Workflow

1. **Pre-flight** — Verify changes exist, parse skip flags, check for existing PRs
2. **Review** (parallel) — deep-review + security-expert + performance-profiler
3. **Validate** (parallel) — test-suite + i18n-sync + dependency-auditor
4. **Package** — Generate changelog, create domain-split commits
5. **Ship** — PR summary, risk assessment, push branch, create PR
6. **Report** — Full pipeline results with PR URL

### Execution

Read and follow the `release-commander` skill (`.cursor/skills/release-commander/SKILL.md`) for pipeline groups, gate checks, and report format.

### Examples

Full release pipeline:
```
/release-commander
```

Dry run to preview findings:
```
/release-commander --dry-run
```

Skip security and i18n checks:
```
/release-commander --skip security,i18n
```
