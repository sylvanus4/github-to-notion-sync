---
name: autoskill-judge
description: >-
  Evaluate skill candidates produced by autoskill-extractor and decide whether
  each should be added, merged into an existing skill, or discarded. Use when
  processing extracted candidates, when invoked by autoskill-evolve, or when
  the user asks to "judge skill candidate", "evaluate extracted skill",
  "스킬 후보 평가", "autoskill judge". Do NOT use for skill quality auditing
  (use skill-optimizer), creating skills from scratch (use create-skill), or
  general code review.
metadata:
  author: thaki
  version: "0.1.0"
  category: self-improvement
---

# AutoSkill Judge

Evaluate skill candidates produced by autoskill-extractor and decide whether each should be added as a new skill, merged into an existing skill, or discarded. Adapts AutoSkill's P_judge and P_decide methodology for the Cursor ecosystem.

## Instructions

### Input

- A skill candidate JSON from `outputs/autoskill-candidates/` (produced by `autoskill-extractor`)
- Access to the existing skills directory at `.cursor/skills/`

### Decision Process

1. **Retrieve Similar Skills**: Use `scripts/memory/search.py` with hybrid search (BM25 + semantic) to find the top-3 most similar existing skills based on the candidate's name, description, and triggers.

2. **Capability Identity Test**: For each similar skill, evaluate on four axes:
   - **Job-to-be-done**: Do both solve the same core problem?
   - **Deliverable type**: Do both produce the same kind of output?
   - **Hard constraints/success criteria**: Do both enforce similar quality rules?
   - **Required tools/workflow**: Do both use similar tool chains?

3. **Apply Decision Logic**:

   **DISCARD** when:
   - Candidate captures a generic, non-portable task
   - Candidate has confidence < 0.6
   - Candidate duplicates an existing skill with no new constraints
   - Candidate contradicts established project conventions without user confirmation
   - Candidate is too narrow (applies to only one specific file/module)

   **MERGE** when:
   - An existing skill has the same capability (same job-to-be-done)
   - Candidate adds new constraints, triggers, or refinements to an existing skill
   - After removing instance-specific details, both skills serve the same purpose
   - The merge would strengthen the existing skill without changing its identity

   **ADD** when:
   - No existing skill covers this capability family
   - The candidate represents a genuinely new workflow or preference pattern
   - The candidate's deliverable type or audience differs materially from all existing skills

4. **Hard Rules**:
   - Same capability → MUST NOT be `add` (must be `merge` or `discard`)
   - Name collision with existing skill after normalization → MUST NOT be `add`
   - If the candidate's primary deliverable class changes from the similar skill → different capability → `add`
   - If the candidate's intended audience differs materially → different capability → `add`

### Output

```json
{
  "action": "add|merge|discard",
  "target_skill_id": "existing-skill-name or null",
  "confidence": 0.85,
  "reason": "Concise explanation of the decision",
  "similar_skills": [
    {"name": "skill-name", "similarity": 0.82, "same_capability": true}
  ]
}
```

Write decisions to `outputs/autoskill-decisions/<date>-<candidate-name>.json`.

### Reference Prompts

See `references/judge-prompt.md` for the full adapted judge prompt template.

### Integration

- Receives candidates from `autoskill-extractor`
- Feeds `merge` decisions to `autoskill-merger`
- Feeds `add` decisions directly to skill creation flow
- Invoked by `autoskill-evolve` orchestrator
