## Superpowers Feature Pipeline

Full Superpowers-driven feature development — brainstorming, design approval, TDD implementation plan, subagent execution with 2-stage review, and branch completion.

### Usage

```
/sp-feature [description of the feature or link to issue]
```

### Workflow

**Step 1: Brainstorming (Design-First)**

Read and follow the Superpowers `brainstorming` skill.

- Explore the current project state (files, docs, recent commits)
- Ask questions **one at a time** (prefer multiple choice) to refine the idea
- Propose 2-3 approaches with trade-offs and a clear recommendation
- Present the design in 200-300 word sections, validating each with the user
- Save the validated design to `docs/plans/YYYY-MM-DD-<topic>-design.md`

**Wait for user approval ("OK", "go", "진행해") before proceeding.**

**Step 2: Implementation Plan**

Read and follow the Superpowers `writing-plans` skill.

- Create bite-sized tasks (2-5 minutes each): write failing test → run → implement → run → commit
- Include exact file paths, complete code snippets, and expected test output
- Save plan to `docs/plans/YYYY-MM-DD-<feature-name>.md`

**Step 3: Subagent-Driven Implementation**

Read and follow the Superpowers `subagent-driven-development` skill.

For each task in the plan:
1. Dispatch a fresh **implementer subagent** with full task text + context
2. Implementer follows TDD (Superpowers `test-driven-development` skill)
3. Dispatch **spec reviewer subagent** — confirms code matches the plan
4. Dispatch **code quality reviewer subagent** — checks quality, names, tests
5. Fix any issues found, re-review until approved
6. Mark task complete

Use project domain skills as needed per task scope:
- **backend-expert** (`.cursor/skills/backend-expert/SKILL.md`) for FastAPI/Pydantic work
- **frontend-expert** (`.cursor/skills/frontend-expert/SKILL.md`) for React/Vite work
- **db-expert** (`.cursor/skills/db-expert/SKILL.md`) for schema/migration work

**Step 4: Verification**

Read and follow the Superpowers `verification-before-completion` skill.

- Run all tests and confirm output (no claiming success without evidence)
- Run lint + typecheck
- Confirm no unused imports or dead code introduced

**Step 5: Finish Branch**

Read and follow the Superpowers `finishing-a-development-branch` skill.

- Verify all tests pass
- Present 4 options: merge locally / create PR / keep branch / discard
- Use **domain-commit** (`.cursor/skills/domain-commit/SKILL.md`) to split changes into domain-based commits before merging/PR

### Difference from `/feature-pipeline`

`/feature-pipeline` skips brainstorming and jumps to implementation. This command enforces the full Superpowers discipline: design-first, TDD, 2-stage review per task, and evidence-based verification.

### Output

- Validated design document in `docs/plans/`
- Implementation plan with TDD tasks
- Implemented + tested feature code
- Domain-split commits
- Branch ready to merge or PR created
