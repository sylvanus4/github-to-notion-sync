# Task Format Reference

## .agent/ Directory Structure

```
.agent/
├── PROMPT.md              # Main iteration instructions (sent every loop)
├── STEERING.md            # Mid-run direction changes
├── STRUCTURE.md           # Project directory structure (optional)
├── tasks.json             # Task lookup table (compact, loaded every iteration)
├── tasks/                 # Per-task detailed specs
│   ├── TASK-001.json
│   ├── TASK-002.json
│   └── ...
├── prd/
│   ├── PRD.md             # Full product requirements document
│   └── SUMMARY.md         # Short project overview for the agent
├── logs/
│   └── LOG.md             # Progress log (appended each iteration)
├── history/               # Per-iteration full output
│   ├── ITERATION-{SESSION}-1.txt
│   └── ...
├── screenshots/           # UI screenshots (TASK-{ID}-{index}.png)
└── skills/                # Reusable agent skills
```

## tasks.json Schema

Compact array loaded every iteration. Keep entries minimal — full details go in task spec files.

```json
[
  {
    "id": "001",
    "name": "Set up project scaffolding",
    "passes": false,
    "priority": 1
  },
  {
    "id": "002",
    "name": "Implement user authentication",
    "passes": false,
    "priority": 2
  },
  {
    "id": "003",
    "name": "Create dashboard layout",
    "passes": true,
    "priority": 3
  }
]
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Zero-padded task ID (e.g., "001", "042") |
| `name` | string | Short task name (1 line) |
| `passes` | boolean | `false` = pending, `true` = completed and tests pass |
| `priority` | number | Execution order (1 = highest priority) |

## TASK-{ID}.json Schema

Full specification for a single task. The agent reads this when it picks a task.

```json
{
  "id": "001",
  "name": "Set up project scaffolding",
  "description": "Initialize the project with Next.js 14, TypeScript, Tailwind CSS, and the required directory structure.",
  "steps": [
    "Run `npx create-next-app@latest` with TypeScript and Tailwind options",
    "Create directory structure: src/components/, src/lib/, src/hooks/",
    "Set up path aliases in tsconfig.json",
    "Add base layout component in src/app/layout.tsx",
    "Verify dev server starts without errors"
  ],
  "acceptance_criteria": [
    "`npm run dev` starts without errors",
    "`npm run build` completes successfully",
    "TypeScript strict mode enabled",
    "Tailwind CSS classes render correctly"
  ],
  "verification": {
    "unit_test": "Run `npm test` — all tests pass",
    "e2e_test": "Navigate to localhost:3000, verify page loads",
    "type_check": "Run `tsc --noEmit` — no errors"
  },
  "dependencies": [],
  "technical_notes": "Use App Router (not Pages Router). Pin Next.js to 14.x."
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Must match tasks.json entry |
| `name` | string | Short task name |
| `description` | string | Detailed description of what to build |
| `steps` | string[] | Ordered implementation steps |
| `acceptance_criteria` | string[] | Conditions that must be true when done |
| `verification` | object | How to verify the task is complete |
| `dependencies` | string[] | IDs of tasks that must be completed first |
| `technical_notes` | string | Additional context, constraints, or gotchas |

## LOG.md Format

Append one entry per completed task:

```markdown
## TASK-001: Set up project scaffolding
- **Status**: DONE
- **Date**: 2026-03-05
- **Changes**: Created Next.js project with TypeScript, Tailwind, path aliases
- **Tests**: All passing (3 unit, 1 e2e)
- **Commit**: abc1234

## TASK-002: Implement user authentication
- **Status**: DONE
- **Date**: 2026-03-05
- **Changes**: Added NextAuth with GitHub OAuth, session middleware
- **Tests**: All passing (8 unit, 2 e2e)
- **Commit**: def5678
```

## Task Design Guidelines

- **One concern per task**: Each task should produce one logical commit
- **Include verification**: Every task needs at least one testable acceptance criterion
- **Order by dependency**: Set priorities so dependent tasks come after their prerequisites
- **Keep specs self-contained**: The agent reads only one task spec per iteration — include all needed context
- **Atomic granularity**: Prefer 50 small tasks over 10 large ones — smaller tasks are more reliably completed
