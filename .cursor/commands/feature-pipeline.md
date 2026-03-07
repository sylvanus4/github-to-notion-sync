## Feature Pipeline

End-to-end orchestrated workflow for implementing a new feature — from spec analysis through implementation, testing, review, commit, and PR creation.

### Usage

```
/feature-pipeline [description of the feature or link to issue]
```

### Workflow

1. Read the mission-control skill at `.cursor/skills/mission-control/SKILL.md`
2. Follow **WF-2: Feature Pipeline** defined there
3. Execute in this order:

**Step 1: Spec Analysis**
- Parse the feature description or issue
- Identify affected services, components, and data models
- Determine scope (backend-only, frontend-only, or full-stack)

**Step 2: Design (Parallel)**
Use Task subagents:
- **backend-expert** (`.cursor/skills/backend-expert/SKILL.md`): Review API design, Pydantic models, error handling patterns for the new feature
- **frontend-expert** (`.cursor/skills/frontend-expert/SKILL.md`): Review component architecture, state management, routing for the new feature

**Step 3: Implementation**
- Implement the feature following the design recommendations
- Follow existing patterns in the codebase

**Step 4: Testing (Parallel)**
Use Task subagents:
- **qa-test-expert** (`.cursor/skills/qa-test-expert/SKILL.md`): Generate test plan and unit tests
- **e2e-testing** (`.cursor/skills/e2e-testing/SKILL.md`): Write Playwright E2E tests if the feature has UI

**Step 5: Review**
- **pr-review-captain** (`.cursor/skills/pr-review-captain/SKILL.md`): Review all changes, assess risk, generate review checklist

**Step 6: Commit & PR**
- **domain-commit** (`.cursor/skills/domain-commit/SKILL.md`): Split changes into domain-based commits
- Create PR following the template in `.github/pull_request_template.md`

### Output

- Implemented feature code
- Unit tests and E2E tests
- Domain-split commits
- PR ready for review
