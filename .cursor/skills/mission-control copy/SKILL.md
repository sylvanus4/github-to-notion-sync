---
name: mission-control
description: Orchestrate multi-skill autonomous workflows — decompose high-level goals into sub-tasks, delegate to specialist skills via subagents, aggregate results, and track progress. Use when the user asks for a full review, release prep, quality audit, incident response, or any task spanning multiple domains. Do NOT use for single-domain tasks that map to one specific skill.
metadata:
  version: "1.0.0"
  category: orchestrator
---

# Mission Control — Agent Orchestrator

The meta-skill that coordinates all other skills. Decomposes high-level goals into sub-tasks, delegates to specialist skills via the Task tool, aggregates results, and tracks progress.

## When to Use

- Any task that spans 2+ specialist domains
- Workflow commands: `/full-quality-audit`, `/feature-pipeline`, `/release-prep`, `/incident-response`, `/dependency-sweep`, `/i18n-check`
- When the user says "do a full review", "prepare for release", "check everything"
- Complex goals that need parallel investigation

## Core Principles

1. **Decompose first**: Break the goal into concrete sub-tasks before acting
2. **Delegate to specialists**: Each sub-task maps to a specific skill
3. **Parallelize**: Use up to 4 Task subagents concurrently
4. **Track progress**: Update `tasks/todo.md` with checkable items
5. **Aggregate results**: Combine outputs into a unified report
6. **Handle failures**: Retry or fall back gracefully

## Skill Registry

22 specialist skills organized into Execution (7), Review (10), and Generation (2) categories, plus this orchestrator. For the full registry and goal-to-skill mapping, see [references/skill-registry.md](references/skill-registry.md).

## Orchestration Protocol

### Step 1: Analyze Goal

Read the user's request and identify:
- **Primary objective**: What needs to be achieved
- **Scope**: Which parts of the codebase are affected
- **Constraints**: Time, safety, or scope limitations
- **Matching workflow**: Does it match a predefined workflow?

### Step 2: Create Task Plan

Write a plan to `tasks/todo.md`:

```markdown
## [Goal Title]
Date: YYYY-MM-DD

- [ ] Sub-task 1 → skill: [skill-name]
- [ ] Sub-task 2 → skill: [skill-name]
- [ ] Sub-task 3 → skill: [skill-name]
- [ ] Aggregate results and report
```

### Step 3: Delegate via Subagents

Use the Task tool to run skills in parallel. Maximum 4 concurrent subagents.

For each subagent:
1. Read the target skill's SKILL.md first
2. Include the specific sub-task in the prompt
3. Include relevant context (file paths, error messages, etc.)
4. Request structured output

```
Task(
  description="Run [skill-name] for [sub-task]",
  prompt="Read the skill at [SKILL.md path] and follow its instructions to [specific task]. Return structured results.",
  subagent_type="generalPurpose"
)
```

**Parallelization strategy:**
- Review skills (read-only) can all run in parallel
- Execution skills must respect dependency order
- CI quality gate should run after code modifications
- domain-commit should be the final execution step

### Step 4: Aggregate Results

Collect outputs from all subagents and:
1. Merge findings by severity/priority
2. De-duplicate overlapping findings
3. Create a unified summary
4. Update `tasks/todo.md` with completed items

### Step 5: Present Results

Deliver a structured report to the user:

```
Mission Control Report
======================
Goal: [original goal]
Date: [YYYY-MM-DD]
Skills invoked: [N]

Summary:
  [2-3 sentence executive summary]

Findings by Priority:
  Critical: [N]
  High: [N]
  Medium: [N]
  Low: [N]

Detailed Results:
  [Skill 1]: [summary of findings]
  [Skill 2]: [summary of findings]
  ...

Actions Taken:
  1. [action]
  2. [action]

Recommended Next Steps:
  1. [recommendation]
  2. [recommendation]
```

### Step 6: Self-Improvement

After task completion, if any errors or unexpected results occurred:
- Document the lesson in `tasks/lessons.md`
- Pattern: `[Date] [Skill] [What went wrong] → [What to do differently]`

## Examples

### Example 1: Full quality audit
User says: "Do a full quality check on the codebase"
Actions:
1. Analyze goal → map to `/full-quality-audit` workflow
2. Launch parallel batch: ci-quality-gate + security-expert + compliance-governance
3. Aggregate findings, auto-fix lint issues, commit via domain-commit
Result: Mission Control Report with unified findings across all domains

### Example 2: Incident response
User says: "The admin service is down, fix it"
Actions:
1. Analyze goal → map to `/incident-response` workflow
2. Run service-health-doctor to identify DOWN services
3. Diagnose root cause with backend-expert + db-expert
4. Apply fix, verify recovery, generate postmortem
Result: Service recovered with documented postmortem

## Predefined Workflows

### WF-1: Full Quality Audit (`/full-quality-audit`)

**Parallel batch 1** (read-only analysis):
1. ci-quality-gate → lint, test, build results
2. security-expert → STRIDE, OWASP, secrets
3. compliance-governance → data governance, access control

**Sequential** (after batch 1):
4. Aggregate findings → generate unified report
5. Auto-fix if applicable (ruff --fix, black, eslint --fix)
6. domain-commit → commit fixes

### WF-2: Feature Pipeline (`/feature-pipeline`)

**Sequential**:
1. Analyze spec/requirements
2. **Parallel**: backend-expert (API design) + frontend-expert (component design)
3. Implement code changes
4. **Parallel**: qa-test-expert (test plan) + e2e-testing (write tests)
5. pr-review-captain → review changes
6. domain-commit → split commits
7. Create PR

### WF-3: Release Prep (`/release-prep`)

**Parallel batch 1**:
1. pr-review-captain → diff analysis, risk assessment
2. technical-writer → release notes, changelog

**Sequential**:
3. sre-devops-expert → deployment readiness check
4. ci-quality-gate → full CI validation
5. Generate release preparation report

### WF-4: Incident Response (`/incident-response`)

**Sequential** (time-critical):
1. service-health-doctor → status check, identify down services
2. Diagnose root cause (logs, metrics)
3. **Parallel**: backend-expert + db-expert → root cause analysis
4. Apply fix
5. service-health-doctor → verify recovery
6. technical-writer → postmortem document

### WF-5: Dependency Sweep (`/dependency-sweep`)

**Sequential**:
1. dependency-auditor → full scan across Python/Go/Node
2. Apply safe patch updates
3. ci-quality-gate → verify updates don't break anything
4. domain-commit → commit per domain (Python/Go/Frontend)

### WF-6: i18n Check (`/i18n-check`)

**Sequential**:
1. i18n-sync → detect missing keys, generate drafts
2. User review of translations
3. Apply confirmed translations
4. domain-commit → commit translation changes

## Error Handling

- **Subagent timeout**: Re-launch with `model: "fast"` for simpler analysis
- **Skill not found**: Log to `tasks/lessons.md` and continue with available skills
- **Conflicting results**: Present both findings to the user for resolution
- **Partial failure**: Complete remaining tasks and report partial results
- **All failed**: Report the failure pattern and suggest manual investigation

## Integration Notes

- This skill is the orchestrator — it reads other skills but is never called by them
- Always read the target skill's SKILL.md before delegating (skills may have been updated)
- Respect the safety rules: never push to upstream, never force delete
- Track all orchestration runs in `tasks/todo.md` for audit trail
