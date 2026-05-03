---
name: autoskill-evolve
description: E2E skill evolution pipeline — extract skill candidates from agent session transcripts, compare against existing skills, and merge or create.
disable-model-invocation: true
---

Run the full skill evolution pipeline.

## Pipeline Stages

1. **Extract**: Mine agent session transcripts for reusable patterns
   - Detect user corrections (3+ occurrences = skill candidate)
   - Identify repeated multi-step workflows
   - Find persistent preferences not captured in existing skills
2. **Judge**: Evaluate each candidate against existing skills
   - **add**: New capability not covered by any skill
   - **merge**: Overlaps with existing skill — merge capabilities
   - **discard**: Already covered or too narrow
3. **Create/Merge**: Execute the decision
   - New skills follow create-skill conventions
   - Merges use semantic union with version bump
4. **Verify**: Test the new/modified skill
   - Trigger accuracy check
   - Boundary validation

## Input

- Agent transcript files: `agent-transcripts/*.jsonl`
- Existing skills: `.cursor/skills/**/*.md` + `.claude/skills/**/SKILL.md`

## Output

- New or updated SKILL.md files
- Evolution log with decisions and rationale

## Rules

- Never create a skill for patterns occurring < 3 times
- Always check for existing skill overlap before creating
- Preserve existing skill triggers when merging
