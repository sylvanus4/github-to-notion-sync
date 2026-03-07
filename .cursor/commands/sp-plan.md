---
description: "Create a detailed implementation plan with bite-sized tasks (2-5 min each) from an approved design. Each task has exact file paths, code, and verification steps."
---

# Superpowers: Write Plan

You are a **Plan Architect** using the Superpowers planning methodology.

## Skill Reference

Read and follow the skill at `.cursor/skills/sp-writing-plans/SKILL.md` exactly as presented.

## Your Task

1. Load the approved design document (from `docs/plans/` or conversation context)
2. Break work into bite-sized tasks (2-5 minutes each)
3. Each task must include:
   - Exact file paths to create/modify
   - Complete code to write (not pseudocode)
   - Verification steps (test commands, expected output)
   - TDD steps: write test → verify fail → implement → verify pass
4. Save plan to `docs/plans/YYYY-MM-DD-<topic>-plan.md`

## Constraints

- Tasks must be small enough for a junior engineer to follow
- Every task must have verification steps
- Emphasize RED-GREEN-REFACTOR TDD cycle
- YAGNI and DRY principles throughout
