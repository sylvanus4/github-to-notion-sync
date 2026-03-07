## UI Suite

Run a full UI/UX lifecycle pipeline: 3 parallel review agents (Design Audit, Web Standards, UX/Design System) analyze UI code, then a UI Builder agent auto-fixes findings and generates missing UI elements.

### Usage

```
# Scoping modes
/ui-suite                              # diff mode — review uncommitted UI changes
/ui-suite today                        # today mode — all UI files changed today
/ui-suite full                         # full mode — entire project UI scan
/ui-suite project                      # alias for full mode

# Focus (combinable with any mode)
/ui-suite focus on accessibility       # prioritize a11y findings
/ui-suite today focus on design tokens # today + prioritize token usage

# Directory scope
/ui-suite src/components/              # scan specific directory only
```

### Workflow

1. **Scope UI files** — Resolve target files by mode, filter to UI-relevant files only
2. **Parallel review** — 3 agents analyze simultaneously (Design Audit, Web Standards, UX/Design System)
3. **Aggregate** — Merge and deduplicate findings by severity
4. **UI Builder** — Auto-fix findings and generate missing UI states
5. **Verify** — Lint check all modified files, fix regressions
6. **Report** — Domain-breakdown summary with applied/skipped fixes

### Execution

Read and follow the `ui-suite` skill (`.cursor/skills/ui-suite/SKILL.md`) for agent prompts, output format, and error handling.

### Examples

Post-feature UI review:
```
/ui-suite
```

Accessibility-focused daily review:
```
/ui-suite today focus on accessibility
```

Full project UI audit:
```
/ui-suite full
```
