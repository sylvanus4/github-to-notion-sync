## Project Recap

Generate a visual HTML project recap — rebuild mental model of a project's current state, recent decisions, and cognitive debt hotspots. Designed for context switching back into a project.

### Usage

```
/project-recap              # default: last 2 weeks
/project-recap 2w           # last 2 weeks
/project-recap 30d          # last 30 days
/project-recap 3m           # last 3 months
```

### Workflow

1. **Determine time window** — Parse the argument as git `--since` format (`2w` → "2 weeks ago", `30d` → "30 days ago"). Default: `2w`
2. **Data gathering**:
   - Project identity: README, CHANGELOG, package manifest, top-level structure
   - Recent activity: `git log --oneline --since=<window>`, `git log --stat`, `git shortlog -sn`
   - Current state: uncommitted changes, stale branches, TODOs/FIXMEs in recent files
   - Decision context: commit messages, plan docs, RFCs, ADRs
   - Architecture scan: entry points, public API surface, frequently changed files
3. **Verification checkpoint** — Fact sheet of every claim (commit counts, file counts, module names). Cite sources.
4. **Generate HTML** with these sections:
   - Project identity (current-state summary, version, elevator pitch)
   - Architecture snapshot (Mermaid diagram of conceptual modules, with zoom controls — this is the visual anchor)
   - Recent activity (human-readable narrative grouped by theme, not raw git log)
   - Decision log (key design decisions with rationale — highest-value section for fighting cognitive debt)
   - State of things (KPI dashboard: working/in-progress/broken/blocked)
   - Mental model essentials (5-10 things to hold in your head: invariants, coupling, gotchas, conventions)
   - Cognitive debt hotspots (amber-tinted cards with severity: undocumented changes, untested modules, overlapping modifications)
   - Next steps (inferred from recent activity and TODOs)
5. **Deliver** — Write to `~/.agent/diagrams/` and open in browser

### Execution

Read and follow the `visual-explainer` skill (`.cursor/skills/visual-explainer/SKILL.md`) for workflow, CSS patterns, templates, and quality checks. Use warm editorial or paper/ink aesthetic.

### Examples

Quick context recovery:
```
/project-recap
```

Monthly review:
```
/project-recap 30d
```

Quarter retrospective:
```
/project-recap 3m
```
