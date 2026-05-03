---
name: full-stack-planner
description: >-
  Generate comprehensive multi-phase implementation plans that map a
  high-level goal to the project's entire skill ecosystem. Produces 5-phase
  pipeline plans with skill assignments, mermaid diagrams, concurrency
  strategies, and structured outputs via the CreatePlan tool. Use when the
  user runs /full-stack-plan, asks to "create a full implementation plan",
  "plan a full-stack pipeline", "generate a multi-phase plan", "전체 구현 계획",
  "풀스택 파이프라인 계획", or needs an enterprise-grade plan spanning 20-50 skills
  across survey, analysis, research, implementation, and testing phases. Do
  NOT use for simple prompt optimization (use plans), runtime workflow
  execution (use mission-control), or developer-focused task lists (use
  sp-writing-plans).
---

# Full-Stack Planner — Multi-Phase Skill Pipeline Generator

Generates comprehensive implementation plans that decompose a high-level goal into 5 standard phases, assign skills to each sub-step, and produce a structured plan via the CreatePlan tool. Each plan includes a mermaid execution flow, concurrency strategy, and skill count summary.

## Workflow

Execute these 6 steps in order.

### Step 1: Receive Goal

Accept the user's high-level implementation goal. This may come from:
- `/full-stack-plan` command `$ARGUMENTS`
- Direct user message
- A feature request, audit scope, or migration brief

If the goal is empty or too vague, ask one clarifying question. Store the original goal text verbatim.

Parse options if present:
- `--phases <list>` — include only specified phases (comma-separated: 1,2,3,4,5)
- `--scope <mode>` — `survey-only` (Phase 1), `plan-only` (Phases 1-3), `full` (default, all 5)
- `--execute` — after plan approval, delegate to mission-control

### Step 2: Survey Project Context

Read current project state to inform phase planning:

1. `README.md` — feature list, tech stack, project overview
2. `MEMORY.md` — decisions, patterns, known constraints
3. `tasks/todo.md` — current backlog, completed work
4. `KNOWN_ISSUES.md` — open bugs, workarounds
5. `docs/prd/` — product requirement documents (if they exist)
6. `docs/roadmap.md`, `docs/okrs.md` — strategic context (if they exist)

Skip files that don't exist. Summarize the project state in 3-5 bullets to reference in plan generation.

### Step 3: Phase Decomposition

Break the goal into up to 5 standard phases. Each phase has a fixed purpose but flexible skill composition based on the goal.

Load phase templates from [references/phase-templates.md](references/phase-templates.md).

For each phase, decide:
- **Include or skip?** — Simple goals may skip Phase 2 (role analysis) or merge Phases 3+4
- **Which skills apply?** — Select from the phase template based on goal domain
- **What are the inputs and outputs?** — Define explicit contracts between phases

Phase selection guidelines:
- Goals touching < 3 files: skip Phases 1-2, start at Phase 3 or 4
- Code-only tasks (no research needed): skip Phase 3
- Audit/review tasks (no implementation): skip Phase 4, expand Phase 5
- Full feature development: include all 5 phases

### Step 4: Skill Assignment

For each included phase, assign skills to sub-steps:

1. Load the skill registry from [references/skill-registry.md](references/skill-registry.md)
2. For each sub-step, select the most specific matching skill
3. Verify each skill exists at `.cursor/skills/{skill-name}/SKILL.md`
4. If no matching skill exists, assign to `generalPurpose` subagent
5. Group skills into parallel batches (max 4 concurrent per batch)

Batching rules:
- Read-only skills (review, analysis) can run in parallel within a phase
- Write skills (implementation, commits) must respect dependency order
- Cross-phase dependencies are always sequential (Phase N completes before Phase N+1)

### Step 5: Plan Generation

Produce the plan using the CreatePlan tool with the following structure:

**YAML Frontmatter:**
```yaml
name: "<Goal Title>"
overview: "<1-2 sentence description of the pipeline>"
todos:
  - id: phase1-<step>
    content: "Phase 1: <description with skill names>"
    status: pending
  # ... one todo per major sub-step
```

**Markdown Body — required sections:**

1. **Phase sections** (one per included phase):
   - Objective (1-2 sentences)
   - Skills Used (grouped by sub-step, with batching annotations)
   - Input Sources (files, outputs from prior phases)
   - Output (explicit deliverable with file path)

2. **Execution Flow Diagram** — Mermaid flowchart showing phase dependencies and skill groupings:
   ```mermaid
   flowchart TD
       P1[Phase1: Survey] --> P2[Phase2: Analysis]
       P2 --> P3[Phase3: Planning]
       P3 --> P4[Phase4: Implementation]
       P4 --> P5[Phase5: Testing]
       subgraph phase1Skills [Phase 1 Skills]
           skill1[skill-name]
           skill2[skill-name]
       end
       P1 --- phase1Skills
   ```

3. **Skill Count Summary** — Table with phase, category, skill count

4. **Concurrency Strategy** — Bullet list explaining max concurrency, batching, and sequential constraints

5. **Key Files Touched** — Input files, generated files, modified files

### Step 6: Optional Customization

After presenting the plan, offer customization:
- Add/remove phases
- Swap skills within a phase
- Adjust scope (broader or narrower)
- Change concurrency limits

If `--execute` was specified and the user approves, read the `mission-control` skill at `.cursor/skills/workflow/mission-control/SKILL.md` and delegate the plan for execution.

## Output Format

The plan is created via CreatePlan with the structure shown in Step 5. The plan file appears in Cursor's Plans UI at `.cursor/plans/`.

## Error Handling

| Problem | Solution |
|---------|----------|
| Goal is empty | Ask user to provide a goal description |
| Goal too vague for 5 phases | Ask one clarifying question about scope and expected outcome |
| No project context files found | Proceed with Phase 3+ only; note limited context in plan |
| Skill from registry does not exist | Assign to generalPurpose subagent, note in plan |
| Phase has no applicable skills | Merge with adjacent phase or skip with explanation |
| Too many skills per phase (>15) | Split phase into sub-phases (e.g., 4A, 4B, 4C) |
| `--execute` fails | Follow mission-control failure classification protocol |

## Examples

### Example 1: New feature implementation

**User**: `/full-stack-plan Add a backtesting engine for trading strategies`

**Actions**:
1. Survey project context (stock analytics platform, FastAPI backend, React frontend)
2. Decompose into 5 phases: survey existing code → role analysis → PM research + PRD → implement engine → test
3. Assign ~35 skills across phases
4. Generate plan with mermaid diagram, 12 todos, and concurrency strategy

**Result**: Structured plan with Phase 1 (codebase-archaeologist, recall), Phase 2 (10 roles via role-dispatcher), Phase 3 (pm-execution PRD, technical-writer ADR), Phase 4 (backend-expert, db-expert, deep-review), Phase 5 (qa-test-expert, ci-quality-gate, security-expert).

### Example 2: Scoped audit (phases 1,5 only)

**User**: `/full-stack-plan --phases 1,5 Security and quality audit of the backend`

**Actions**:
1. Skip Phases 2-4 per --phases flag
2. Phase 1: survey with codebase-archaeologist + recall
3. Phase 5: security-expert, dependency-auditor, compliance-governance, test-suite, ci-quality-gate
4. Generate compact 2-phase plan

**Result**: Focused audit plan with 8 skills and 5 todos.

### Example 3: Research-only plan

**User**: `/full-stack-plan --scope plan-only Evaluate whether to add real-time streaming to our platform`

**Actions**:
1. Phase 1: survey current architecture
2. Phase 2: role-dispatcher analysis (CTO, PM, Developer perspectives)
3. Phase 3: pm-product-strategy SWOT, pm-market-research competitive analysis, technical-writer ADR
4. No Phase 4/5 (plan-only scope)

**Result**: Research plan with 20 skills and decision framework, no implementation.

## References

- Phase templates: [references/phase-templates.md](references/phase-templates.md)
- Skill registry: [references/skill-registry.md](references/skill-registry.md)
- Execution engine: [mission-control](.cursor/skills/workflow/mission-control/SKILL.md)
- Workflow patterns: see `workflow-patterns.mdc` for Sequential/Parallel/Evaluator-Optimizer guidance


## Subagent Contract

When spawning Task tool subagents:

- Always pass **absolute file paths** — subagent working directories are unpredictable
- Share only **load-bearing code snippets** — omit boilerplate the subagent can discover itself
- Require subagents to return: `{ status, file, summary }` — not full analysis text
- Include a **purpose statement** in every subagent prompt: "You are a subagent whose job is to [specific goal]"
- Never say "do everything" — list the 3-5 specific outputs expected
