## Codebase Archaeologist

Analyze git history for code ownership maps, churn hotspots, bus factor reports, dead code detection, and temporal risk heatmaps.

### Usage

```
/codebase-archaeologist                           # full project analysis
/codebase-archaeologist src/api/                  # scope to directory
/codebase-archaeologist --mode ownership          # ownership map only
/codebase-archaeologist --mode churn              # churn hotspots only
/codebase-archaeologist --mode bus-factor         # bus factor report
/codebase-archaeologist --mode dead-code          # dead code candidates
/codebase-archaeologist --mode risk               # composite risk heatmap
/codebase-archaeologist --since "6 months ago"    # custom time window
```

### Workflow

1. **Determine scope** — Parse target path, analysis mode, and time window
2. **Collect git history** — Run `git log` commands for authorship, frequency, and date data
3. **Analyze** — Ownership map, churn ranking, bus factor, dead code scan, or risk heatmap
4. **Generate report** — Structured findings with key risks and recommendations

### Execution

Read and follow the `codebase-archaeologist` skill (`.cursor/skills/codebase-archaeologist/SKILL.md`) for git commands, analysis formulas, and report format.

### Examples

Full project archaeology:
```
/codebase-archaeologist
```

Who owns the auth module:
```
/codebase-archaeologist src/api/auth/ --mode ownership
```

Risk assessment before refactoring:
```
/codebase-archaeologist src/components/ --mode risk
```
