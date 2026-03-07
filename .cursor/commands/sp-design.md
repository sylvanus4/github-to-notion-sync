## Superpowers Design

Collaborative design brainstorming followed by a detailed implementation plan — without writing any code. Design and plan only.

### Usage

```
/sp-design [feature idea, requirement, or problem statement]
```

### Workflow

**Step 1: Brainstorming**

Read and follow the Superpowers `brainstorming` skill.

1. Check the current project state (files, docs, recent commits)
2. Ask questions **one at a time** to refine the idea:
   - Prefer multiple choice when possible
   - Only one question per message
   - Focus on: purpose, constraints, success criteria
3. Propose 2-3 approaches with trade-offs:
   - Lead with your recommendation and explain why
   - Present options conversationally
4. Present the design in sections (200-300 words each):
   - Architecture, components, data flow
   - Error handling, testing strategy
   - Ask after each section: "이 부분 괜찮아요?"
5. Apply YAGNI ruthlessly — remove unnecessary features

**Step 2: Design Document**

Save the validated design to:
```
docs/plans/YYYY-MM-DD-<topic>-design.md
```

**Step 3: Implementation Plan**

Read and follow the Superpowers `writing-plans` skill.

Create a detailed plan with bite-sized TDD tasks (2-5 minutes each):

```markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Step 1:** Write the failing test
**Step 2:** Run test to verify it fails
**Step 3:** Write minimal implementation
**Step 4:** Run test to verify it passes
**Step 5:** Commit
```

Include exact file paths, complete code, and expected test output for every step.

Save the plan to:
```
docs/plans/YYYY-MM-DD-<feature-name>.md
```

**Step 4: Execution Handoff**

Present the choice:

```
Plan complete and saved. Two execution options:

1. Subagent-Driven (this session) — dispatch fresh subagent per task, review between tasks
2. Separate Session — open new session and use /sp-feature to execute

Which approach?
```

**This command does NOT implement code.** It produces the design and plan only.

### Difference from `/plan`

`/plan` is a generic 3-phase planning template. This command enforces Superpowers' brainstorming discipline: one question at a time, multiple choice preferred, YAGNI, incremental design validation, and TDD-ready implementation plans with exact file paths and code.

### Output

- Design document in `docs/plans/YYYY-MM-DD-<topic>-design.md`
- Implementation plan in `docs/plans/YYYY-MM-DD-<feature-name>.md`
- No code written — ready for `/sp-feature` or subagent execution
