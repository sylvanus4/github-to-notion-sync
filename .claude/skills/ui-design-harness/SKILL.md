---
name: ui-design-harness
description: >-
  End-to-end UI design quality pipeline orchestrating 6 design skills across 3
  phases: Prepare, Review (parallel 3-agent), and Fix. Composite pattern
  combining Pipeline with Fan-out/Fan-in.
---

# UI Design Harness

End-to-end UI design quality pipeline orchestrating 6 design skills across 3 phases: Prepare (DESIGN.md generation + prompt enhancement), Review (parallel 3-agent design audit), and Fix (anti-slop guard + auto-fix). Composite pattern combining Pipeline with Fan-out/Fan-in for maximum coverage and minimal latency.

Adapted from [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) patterns, tailored for the ThakiCloud AI Platform's Refined Swiss design system.

## Triggers

Use when the user asks to "run UI design pipeline", "full design quality check", "UI design harness", "design pipeline", "end-to-end UI quality", "UI 디자인 파이프라인", "디자인 품질 전체 점검", "UI 디자인 하네스", "디자인 파이프라인", "UI 전체 점검", "ui-design-harness", "design harness", "full UI audit and fix", "디자인 3단계 점검", "UI 품질 파이프라인", "디자인 준비-리뷰-수정", "UI 하네스 실행", or wants comprehensive design quality assurance from preparation through review to remediation.

Do NOT use for one-off prompt enhancement only (use refined-swiss-prompt-enhancer). Do NOT use for DESIGN.md generation only (use design-md-generator). Do NOT use for anti-pattern scan only (use anti-slop-ui-guard). Do NOT use for design QA checklist only (use design-qa-checklist). Do NOT use for general code review without design focus (use deep-review). Do NOT use for building new UIs from scratch (use implement-screen or fe-pipeline). Do NOT use for Stitch MCP screen generation (use stitch-design). Do NOT use for shadcn/ui component installation (use shadcn-ui).

## Architecture

```
Phase 1: PREPARE (sequential)
  ├── design-md-generator → DESIGN.md
  └── refined-swiss-prompt-enhancer → enhanced prompts (if raw prompt provided)

Phase 2: REVIEW (parallel fan-out → fan-in)
  ├── Agent A: anti-slop-ui-guard → violation report
  ├── Agent B: design-qa-checklist → QA checklist report
  └── Agent C: ux-expert (accessibility subset) → a11y report

Phase 3: FIX (sequential pipeline)
  ├── Merge & deduplicate findings
  ├── Auto-fix deterministic violations
  ├── Verify fixes with ReadLints
  └── Generate consolidated report
```

## Modes

| Mode | Trigger | Description |
|------|---------|-------------|
| `full` | `/ui-design-harness full` | All 3 phases on entire frontend |
| `review` | `/ui-design-harness review` | Phase 2+3 only (skip DESIGN.md gen) |
| `diff` (default) | `/ui-design-harness` | Phase 2+3 on git diff files only |
| `prepare` | `/ui-design-harness prepare` | Phase 1 only (DESIGN.md + prompt) |

## Workflow

### Phase 1 — Prepare

#### Step 1a: DESIGN.md Generation

Check if `DESIGN.md` exists at the project root. If missing or stale (older than 30 days):

1. Read `.cursor/rules/design-system.mdc` as authoritative source
2. Invoke `design-md-generator` skill workflow
3. Save output to `DESIGN.md`

Skip if DESIGN.md exists and is fresh, unless `--force-refresh` is passed.

#### Step 1b: Prompt Enhancement (optional)

If the user provides a raw UI description alongside the harness invocation:

1. Invoke `refined-swiss-prompt-enhancer` with the raw description
2. Save the enhanced prompt to `outputs/ui-harness/enhanced-prompt-{date}.md`
3. Optionally pass to `implement-screen` or `fe-pipeline` for implementation

### Phase 2 — Review (Fan-out)

Launch 3 parallel review agents using the Task tool. Each agent receives the target file list and operates independently.

#### Agent A: Anti-Slop Guard

```
Subagent config:
  subagent_type: generalPurpose
  readonly: true

Prompt must include:
  - Goal: Scan files for Refined Swiss anti-pattern violations
  - File list with absolute paths
  - Reference: .cursor/skills/frontend/anti-slop-ui-guard/SKILL.md
  - Reference: .cursor/rules/design-system.mdc
  - Output format: severity-ranked violation table
  - Return: { status, violations_count, high_count, report_markdown }
```

#### Agent B: Design QA Checklist

```
Subagent config:
  subagent_type: generalPurpose
  readonly: true

Prompt must include:
  - Goal: Run Refined Swiss design QA checklist
  - File list with absolute paths
  - Reference: .cursor/skills/frontend/design-qa-checklist/SKILL.md
  - Reference: .cursor/rules/design-system.mdc
  - Output format: pass/fail checklist with evidence
  - Return: { status, pass_count, fail_count, checklist_markdown }
```

#### Agent C: Accessibility Auditor

```
Subagent config:
  subagent_type: generalPurpose
  readonly: true

Prompt must include:
  - Goal: WCAG AA accessibility audit of UI components
  - File list with absolute paths
  - Focus: ARIA attributes, focus management, touch targets, color contrast, keyboard nav
  - Output format: violation list with WCAG criteria references
  - Return: { status, violations_count, critical_count, audit_markdown }
```

### Phase 3 — Fix (Sequential)

#### Step 3a: Merge & Deduplicate

1. Collect all 3 agent reports
2. Normalize findings to a common format:
   ```
   { file, line, severity, category, violation_id, description, fix_suggestion }
   ```
3. Deduplicate: same file + same line + overlapping issue → keep highest severity
4. Sort: HIGH > MEDIUM > LOW, then by file

#### Step 3b: Auto-Fix

Launch a single write-enabled subagent:

```
Subagent config:
  subagent_type: generalPurpose
  readonly: false

Prompt must include:
  - Goal: Apply deterministic auto-fixes for design violations
  - Merged findings list
  - Rules for safe auto-fix:
    * rounded-md → rounded-lg on buttons
    * Add motion-reduce:animate-none next to animate-spin/animate-pulse
    * Add scope="col" to <th> elements
    * disabled:opacity-60 → disabled:opacity-50
    * Add overflow-x-auto wrapper to bare <table> elements
  - Rules for skip (require human judgment):
    * Semantic color token selection
    * Layout restructuring
    * Component variant changes
  - Return: { fixed_count, skipped_count, files_modified }
```

#### Step 3c: Verify

1. Run `ReadLints` on all modified files
2. If lint errors introduced, fix them
3. Run `anti-slop-ui-guard` in `--diff` mode on fixed files to confirm zero HIGH regressions

#### Step 3d: Consolidated Report

Generate a final report saved to `outputs/ui-harness/report-{date}.md`:

```markdown
# UI Design Harness Report — {date}

## Summary
- Mode: [full|review|diff|prepare]
- Files scanned: N
- Total findings: N (HIGH: N, MEDIUM: N, LOW: N)
- Auto-fixed: N
- Skipped (human needed): N
- Final status: PASS / FAIL

## Phase 1: Prepare
- DESIGN.md: [Generated / Up-to-date / Skipped]
- Prompt enhanced: [Yes (path) / No]

## Phase 2: Review
### Anti-Slop Guard
[Agent A report summary]

### Design QA Checklist
[Agent B report summary]

### Accessibility Audit
[Agent C report summary]

## Phase 3: Fix
### Auto-Fixed
| File | Line | Violation | Fix Applied |
|------|------|-----------|-------------|
| ... | ... | ... | ... |

### Requires Human Attention
| File | Line | Severity | Issue | Suggested Fix |
|------|------|----------|-------|---------------|
| ... | ... | ... | ... | ... |

## Next Steps
- [ ] Review human-attention items above
- [ ] Run `/ui-design-harness review` after manual fixes
```

## Context Isolation Rules

Every subagent prompt MUST include:
1. The complete goal statement
2. Absolute file paths (subagents cannot resolve relative paths)
3. Skill file paths to read for methodology
4. Design system rule path (`.cursor/rules/design-system.mdc`)
5. Expected output format and structure
6. Quality criteria for pass/fail

Subagents do NOT inherit parent conversation context.

## Integration

- Run before `ship` or `release-commander` as a design quality gate
- Run after `implement-screen` or `fe-pipeline` to validate generated UI
- Compose with `ui-suite` for combined design + web standards review
- Use `prepare` mode to bootstrap DESIGN.md for new projects
- Chain with `figma-dev-pipeline` for Figma→code→validation workflows

## Error Handling

| Scenario | Action |
|----------|--------|
| Subagent timeout | Retry once; if still fails, report partial results |
| No UI files in scope | Suggest `--full` mode or specifying a directory |
| DESIGN.md generation fails | Continue with Phase 2 using design-system.mdc directly |
| Conflicting fixes across agents | Apply first fix, skip subsequent with explanation |
| Lint errors after auto-fix | Revert that fix and add to "human attention" list |
