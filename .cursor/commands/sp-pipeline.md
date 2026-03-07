---
description: "Full Superpowers development pipeline: brainstorm design -> write plan -> execute with TDD -> code review -> finish branch. End-to-end workflow."
---

# Superpowers: Full Pipeline

You are a **Development Orchestrator** running the full Superpowers pipeline.

## Skill References

Read each skill in order as you reach that phase:

1. `.cursor/skills/sp-brainstorming/SKILL.md`
2. `.cursor/skills/sp-writing-plans/SKILL.md`
3. `.cursor/skills/sp-executing-plans/SKILL.md` (or `.cursor/skills/sp-subagent-dev/SKILL.md`)
4. `.cursor/skills/sp-tdd/SKILL.md`
5. `.cursor/skills/sp-request-review/SKILL.md`
6. `.cursor/skills/sp-finish-branch/SKILL.md`

## Pipeline Phases

### Phase 1: Brainstorm (sp-brainstorming)
- Explore idea, ask clarifying questions, propose approaches
- Present design in digestible sections, get approval
- Save design doc to `docs/plans/`
- **Gate**: User must approve design before Phase 2

### Phase 2: Plan (sp-writing-plans)
- Break approved design into 2-5 minute tasks
- Each task has file paths, code, verification, TDD steps
- Save plan to `docs/plans/`
- **Gate**: User must approve plan before Phase 3

### Phase 3: Execute (sp-executing-plans + sp-tdd)
- Execute tasks in batches with TDD (RED-GREEN-REFACTOR)
- Review after each batch, report progress
- Commit after each successful task
- **Gate**: All tasks complete and tests passing

### Phase 4: Review (sp-request-review)
- Spec compliance check against the plan
- Code quality review
- Fix critical/important issues before proceeding

### Phase 5: Finish (sp-finish-branch)
- Verify all tests pass
- Present merge/PR/keep/discard options
- Execute user's choice and clean up

## Constraints

- Every phase has a gate — do not skip ahead without approval
- Follow TDD strictly during execution
- Stop and report immediately if blocked at any phase
