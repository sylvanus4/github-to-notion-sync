## Plan Review

Generate a visual HTML plan review — current codebase state vs. proposed implementation plan with risk assessment.

### Usage

```
/plan-review <plan-file-path>                    # compare plan against current directory
/plan-review <plan-file-path> <codebase-path>    # compare plan against specific codebase
```

### Workflow

1. **Read inputs** — Read the plan file in full, extract problem statement, proposed changes, rejected alternatives, and scope boundaries
2. **Read codebase** — Read every file the plan references plus their dependents. Map the blast radius (imports, tests, configs, public API surface)
3. **Cross-reference** — For each proposed change, verify: Does the file/function/type exist? Does the plan's description of current behavior match reality? Are there implicit assumptions that don't hold?
4. **Verification checkpoint** — Fact sheet of every claim from both the plan and codebase. Cite sources.
5. **Generate HTML** with these sections:
   - Plan summary (the intuition — what problem, what insight)
   - Impact dashboard (files to modify/create/delete, estimated lines, completeness indicators)
   - Current architecture (Mermaid diagram of affected subsystem today, with zoom controls)
   - Planned architecture (Mermaid diagram of post-implementation state, same node names for visual diff)
   - Change-by-change breakdown (side-by-side current vs. planned with rationale extraction)
   - Dependency & ripple analysis (callers, importers, downstream effects color-coded by coverage)
   - Risk assessment (edge cases, assumptions, ordering risks, rollback complexity, cognitive complexity)
   - Plan review (Good/Bad/Ugly/Questions with plan section and code file references)
   - Understanding gaps (decision-rationale gaps + cognitive complexity flags dashboard)
6. **Deliver** — Write to `~/.agent/diagrams/` and open in browser

### Execution

Read and follow the `visual-explainer` skill (`.cursor/skills/visual-explainer/SKILL.md`) for workflow, CSS patterns, templates, and quality checks. Use current-vs-planned visual language (blue=current, green/purple=planned, amber=concern, red=gap).

### Examples

Review an implementation plan:
```
/plan-review docs/plans/auth-redesign.md
```

Review against specific codebase:
```
/plan-review specs/api-v2.md src/api/
```
