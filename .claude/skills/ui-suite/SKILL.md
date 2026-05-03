---
name: ui-suite
description: >-
  Run a full UI/UX lifecycle pipeline: 3 parallel review agents (Design Audit,
  Web Standards, UX/Design System) analyze UI code, then a UI Builder agent
  auto-fixes findings and generates missing UI elements. Supports
  diff/today/full scoping. Use when the user runs /ui-suite, asks for "UI
  review", "design audit", "UX check", "frontend quality review", or "fix my
  UI". Do NOT use for building new UIs from scratch without existing code (use
  frontend-design), single-domain code review (use /simplify or /deep-review),
  or backend-only review. Korean triggers: "감사", "리뷰", "빌드", "분석".
---

# UI Suite — UI/UX Full-Lifecycle Orchestrator

Review UI code from 3 design perspectives simultaneously, aggregate findings, then auto-fix issues and generate missing UI elements. Combines design auditing with hands-on improvement.

## Scoping Modes

| Mode | Trigger | Scope |
|------|---------|-------|
| `diff` (default) | `/ui-suite` | Git diff (unstaged + staged + HEAD) |
| `today` | `/ui-suite today` | All files changed today |
| `full` | `/ui-suite full` | All source files in the project |

Combinable with focus: `/ui-suite today focus on accessibility`.

## Workflow

### Step 1: Identify UI Files

Resolve target files using the scoping mode (same commands as `/simplify`), then filter to UI-relevant files only:

**Include**: `*.tsx`, `*.jsx`, `*.vue`, `*.svelte`, `*.css`, `*.scss`, `*.html`, files in `components/`, `pages/`, `views/`, `layouts/`, `styles/`, `ui/`

**Exclude**: `*.test.*`, `*.spec.*`, pure utility/helper files with no UI exports, config files

If no UI files are found, inform the user and suggest scoping to a UI directory.

### Step 2: Launch 3 Parallel Review Agents

Use the Task tool to spawn 3 read-only sub-agents. Each agent receives the list of UI files and their contents. For detailed prompts, see [references/agent-prompts.md](references/agent-prompts.md).

```
Agent 1: Design Audit Agent     → Visual hierarchy, spacing, typography, component consistency, states
Agent 2: Web Standards Agent    → HTML semantics, CSS patterns, WCAG accessibility, responsive design
Agent 3: UX/Design System Agent → Design tokens, color/typography system, UX patterns, anti-patterns
```

Sub-agent configuration:
- `subagent_type`: `generalPurpose`
- `model`: `fast`
- `readonly`: `true`

Each agent returns findings in this structure:

```
DOMAIN: [agent domain]
FINDINGS:
- severity: [Critical|High|Medium|Low]
  file: [path]
  line: [number or range]
  issue: [description]
  fix: [suggested change]
```

### Step 3: Aggregate and Deduplicate

1. Merge all agent outputs into a single findings list
2. Remove duplicates (same file + same line + similar issue)
3. Sort: Critical > High > Medium > Low
4. Group by file within same severity

### Step 4: UI Builder Agent

Launch a single write-enabled sub-agent that receives:
- The aggregated findings list
- The original file contents

```
Agent 4: UI Builder Agent → Apply fixes, generate missing states, improve layouts
```

Sub-agent configuration:
- `subagent_type`: `generalPurpose`
- `model`: `fast`
- `readonly`: `false`

The builder agent applies fixes in order of severity and:
- Fixes token misuse (hardcoded colors/spacing to design tokens)
- Fixes accessibility violations (missing alt text, aria-labels, focus styles)
- Adds missing UI states (loading, error, empty)
- Improves spacing and layout consistency
- Skips fixes that are ambiguous or require architectural decisions

### Step 5: Verify and Report

1. Run `ReadLints` on all modified files
2. Fix any introduced lint errors
3. Present report using the template in [references/report-template.md](references/report-template.md)

## Optional Arguments

```
/ui-suite                              # diff mode — review uncommitted UI changes
/ui-suite today                        # today mode — all UI files changed today
/ui-suite full                         # full mode — entire project UI scan
/ui-suite focus on accessibility       # prioritize a11y findings
/ui-suite src/components/              # scope to specific directory
```

## Examples

### Example 1: Post-feature UI review

User runs `/ui-suite` after implementing a new dashboard page.

Actions:
1. `git diff HEAD` finds 6 UI files (3 components, 2 styles, 1 page)
2. 3 review agents analyze in parallel
3. Findings: 1 Critical (missing keyboard navigation), 2 High (hardcoded colors, no error state), 4 Medium
4. UI Builder applies 6/7 fixes, skips 1 (layout restructure)
5. Lint verification passes
6. Report with domain breakdown

### Example 2: Full project UI audit

User runs `/ui-suite full` for a design consistency check.

Actions:
1. Find 28 UI files across `src/components/`, `src/pages/`
2. 3 review agents each evaluate all files from their perspective
3. Findings: 2 Critical, 5 High, 10 Medium, 8 Low
4. UI Builder applies fixes by severity, batched by file
5. Comprehensive UI health report

### Example 3: Accessibility-focused review

User runs `/ui-suite today focus on accessibility`.

Actions:
1. Find 4 UI files changed today
2. All 3 agents run; Web Standards agent a11y findings highlighted first
3. Findings: 2 High (missing focus-visible, no aria-labels), 3 Medium
4. All fixes applied by UI Builder
5. Accessibility-focused report

## Error Handling

| Scenario | Action |
|----------|--------|
| No UI files found | Suggest specifying a UI directory or using `full` mode |
| No changes detected | Suggest `today` or `full` mode |
| Sub-agent timeout | Re-launch once; if still fails, report partial results |
| Lint errors after fix | Auto-fix; if unfixable, revert that fix |
| Conflicting fixes across domains | Apply first fix, skip subsequent with explanation |

## Troubleshooting

- **"No UI files found"**: The filter may be too strict for your project structure; try scoping to a specific directory
- **Overlap with /deep-review**: `/deep-review` includes a frontend agent but covers all domains; `/ui-suite` goes deeper on UI/UX specifically
- **Large projects**: UI files are batched at 30+ files per agent round

## Subagent Contract

When spawning Task tool subagents:

- Always pass **absolute file paths** — subagent working directories are unpredictable
- Share only **load-bearing code snippets** — omit boilerplate the subagent can discover itself
- Require subagents to return: `{ status, file, summary }` — not full analysis text
- Include a **purpose statement** in every subagent prompt: "You are a subagent whose job is to [specific goal]"
- Never say "do everything" — list the 3-5 specific outputs expected
