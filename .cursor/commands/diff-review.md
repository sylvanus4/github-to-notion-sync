## Diff Review

Generate a visual HTML diff review — before/after architecture comparison with code review analysis.

### Usage

```
/diff-review                       # diff against main (default)
/diff-review main                  # diff against specific branch
/diff-review HEAD                  # uncommitted changes only
/diff-review abc123                # specific commit
/diff-review #42                   # PR number (uses gh pr diff)
/diff-review abc123..def456        # range between two commits
/diff-review --slides              # output as slide deck instead
```

### Workflow

1. **Scope detection** — Determine what to diff based on the argument (branch, commit, HEAD, PR number, range, or default to main)
2. **Data gathering** — Run git commands to understand full scope:
   - `git diff --stat` for file overview
   - `git diff --name-status` for new/modified/deleted files
   - Line counts comparison between ref and working tree
   - New public API surface (grep for exported symbols)
   - Read all changed files in full
   - Reconstruct decision rationale from commit messages and conversation context
3. **Verification checkpoint** — Produce a fact sheet of every quantitative figure, function name, and behavior description. Cite sources. Verify against code.
4. **Generate HTML** with these sections:
   - Executive summary (the "aha moment" — why do these changes exist?)
   - KPI dashboard (lines added/removed, files changed, housekeeping indicators)
   - Module architecture (Mermaid dependency graph with zoom controls)
   - Major feature comparisons (side-by-side before/after panels)
   - Flow diagrams (Mermaid for new lifecycle/pipeline patterns)
   - File map (color-coded new/modified/deleted)
   - Test coverage (before/after comparison)
   - Code review (Good/Bad/Ugly/Questions with file references)
   - Decision log (what was decided, why, alternatives, confidence level)
   - Re-entry context (invariants, non-obvious coupling, gotchas, follow-ups)
5. **Deliver** — Write to `~/.agent/diagrams/` and open in browser

### Execution

Read and follow the `visual-explainer` skill (`.cursor/skills/visual-explainer/SKILL.md`) for workflow, CSS patterns, templates, and quality checks. Use diff-style visual language (red=removed, green=added, yellow=modified, blue=context).

### Examples

Pre-merge review:
```
/diff-review feature/auth
```

Quick uncommitted changes review:
```
/diff-review HEAD
```

PR review:
```
/diff-review #42
```
