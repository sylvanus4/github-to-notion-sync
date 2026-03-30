# STEERING.md Patterns

STEERING.md is the mechanism for redirecting the agent mid-run. The agent reads it at the start of every iteration, before picking a task. Place critical work here to override normal task execution.

## Contents

- [Basic Format](#basic-format)
- [Common Patterns](#common-patterns) (Bug Override, Docker Fixes, Architecture Correction, Dependency Update, Quality Gate)
- [Tips](#tips)

## Basic Format

```markdown
# Critical Steering Work

## [Section Title]

Instructions for critical work. Agent processes this before normal tasks.
Remove items when done.

---

After you finish this work, exit with message `Steering complete`.
```

## Common Patterns

### Pattern 1: Bug Priority Override

When a bug is discovered during the loop and must be fixed before continuing:

```markdown
# Critical Steering Work

## Fix Authentication Bug

The login flow is broken after TASK-012 changes. Before continuing with new tasks:

1. Check `src/auth/login.ts` — the token refresh logic has a race condition
2. Write a regression test in `src/auth/__tests__/login.test.ts`
3. Fix the bug
4. Run all auth tests: `npm test -- --grep auth`
5. Commit with message: `fix: resolve token refresh race condition`
6. Remove this section from STEERING.md when done
```

### Pattern 2: Docker Sandbox Fixes

Common environment issues inside the Docker sandbox:

```markdown
# Critical Steering Work

## Environment Setup

Before starting any task:

1. Run `npm install --ignore-scripts` (avoids native binary SIGILL)
2. Run `npx playwright install chromium --with-deps`
3. If Node version is wrong: `nvm use 20`
4. Remove this section after setup is confirmed working
```

### Pattern 3: Architecture Correction

When the agent took a wrong architectural direction:

```markdown
# Critical Steering Work

## Refactor Data Layer

TASK-015 through TASK-018 used direct SQL queries instead of the ORM.
Before continuing:

1. Refactor all direct queries in `src/db/` to use Prisma
2. Update affected tests
3. Run full test suite
4. Commit: `refactor: migrate direct SQL to Prisma ORM`
5. Remove this section when done
```

### Pattern 4: Dependency Update

When a dependency needs to be updated or replaced mid-run:

```markdown
# Critical Steering Work

## Update React Router

React Router v5 is causing issues. Upgrade to v6:

1. `npm install react-router-dom@6`
2. Update all route definitions to v6 syntax
3. Update all `useHistory` → `useNavigate`
4. Run tests and fix any failures
5. Remove this section when done
```

### Pattern 5: Quality Gate Enforcement

When output quality drops and needs tightening:

```markdown
# Critical Steering Work

## Enforce Test Coverage

Recent tasks had insufficient tests. For ALL remaining tasks:

1. Every new function must have at least 2 test cases (happy path + error case)
2. Run `npm run test:coverage` after each task
3. Coverage must not drop below 80%
4. Add this check to your task completion flow
5. Keep this section active for all remaining iterations
```

## Tips

- **Be specific**: Vague instructions lead to vague results. Include file paths, function names, exact commands.
- **One concern per section**: Multiple unrelated concerns in one steering block confuse the agent.
- **"Remove when done"**: Always include this instruction so the agent cleans up after itself.
- **Persistent rules**: For rules that apply to ALL remaining iterations (like Pattern 5), state "Keep this section active."
- **Check history**: Review `.agent/history/` to see if the agent followed steering instructions correctly.
