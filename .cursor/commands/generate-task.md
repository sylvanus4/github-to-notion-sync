# Generate Task

Analyze the request and generate a task document for runner.sh execution.

## Request: $ARGUMENTS

> Pre-condition: Read `MEMORY.md` and project context first.

---

## When to Use

Use for any work that is NOT a new feature (use `generate-prd` for new features). Examples:
- Bug fixes
- Documentation sync / inconsistency fixes
- Refactoring
- Code migration
- Config / environment changes
- Adding tests
- Performance improvements
- Batch of miscellaneous changes

---

## Principles
1. **Analyze First**: Read all relevant code/docs thoroughly before defining tasks.
2. **Evidence-Based**: Each checklist item must reference a specific file and describe the concrete fix.
3. **Parallel-Ready**: Split into `**Group:**` labels when tasks touch different files.
4. **Actionable**: Each `- [ ]` item must be completable by an AI agent in one iteration.
5. **Architecture Compliance**: Read `my-specs/CONTEXT.md` §6.1 (A1~A6). Compliance gaps → 🔴 Critical items.

---

## Process

### 1. Parse Request
- From `$ARGUMENTS`, identify:
  - **Work type**: bug fix, docs sync, refactor, migration, etc.
  - **Target scope**: which files, directories, or domains
  - **Reference source**: code, docs, or standards to compare against

### 2. Investigate
- Read all target files/code
- Cross-reference as needed:
  - Implementation code (handlers, repositories, services)
  - DB schemas, event definitions, API docs, architecture guides
- Categorize findings:
  - 🔴 Critical: Affects behavior, wrong logic, missing pieces
  - 🟡 Medium: Inconsistencies, outdated information
  - 🟢 Minor: Style, formatting, typos

#### ⚠️ Mandatory Verification Rules
1. **Path verification**: Before specifying any file path in a checklist item, VERIFY the path exists (or its parent exists) by reading the actual directory. Do NOT assume folder names from memory or context — always `ls` or `read` to confirm.
2. **Delete verification**: Before instructing deletion of any file, VERIFY the corresponding code/endpoint/feature is truly removed. For backend: check `router.go`, handler files, and swagger annotations. For frontend: check route definitions, page components, and feature index exports. If the code still exists, the doc/file must NOT be deleted.
3. **Naming verification**: Before specifying folder or file names, cross-reference actual naming conventions. Backend: Go package names, DB table names, docs directory conventions. Frontend: FSD module names (`entities/`, `features/`, `widgets/`, `pages/`), domain naming in `src/`.
4. **Scope matching**: Each checklist item must specify whether it modifies `docs/` only, backend source, frontend source, or a combination. Never mix scope implicitly.

### 3. Design Groups
- Tasks touch different files → separate `**Group:**` labels (parallel execution)
- Tasks share files or have ordering dependency → single group (sequential execution)
- Few tasks (3 or less) → flat checklist, no groups needed
- Use `**Group: name**` (bold text), NOT `#### Group:` (heading syntax breaks runner parsing)

### 4. Generate Task Document

Save to: `my-specs/tasks/{descriptive-name}.md`

---

## Template

```markdown
# [Task Title]

> Generated: [date]
> Type: [bug-fix / docs-sync / refactor / migration / config / test / perf / misc]
> Scope: [target scope summary]
> Allowed Paths: [glob patterns of files the agent MAY modify, comma-separated]

## Context
[Why this work is needed, background]

## Findings (if applicable)
| Category | Count | Details |
|----------|-------|---------|
| 🔴 Critical | N | ... |
| 🟡 Medium | N | ... |
| 🟢 Minor | N | ... |

## Must-have

**Group: [name-1]**
- [ ] `path/to/file` — [specific fix description]
- [ ] `path/to/file2` — [specific fix description]

**Group: [name-2]**
- [ ] `path/to/file3` — [specific fix description]

## Should-have (Optional)
- [ ] [lower priority items]
```

> `**Group:**` labels are optional. Omit them if tasks are few or must run sequentially.

---

## Output

1. Save the task document to `my-specs/tasks/`
2. Print summary:

```
✅ Task: my-specs/tasks/fix-pipeline-docs.md
   Type: docs-sync
   Items: 11 (8 critical, 3 medium)
   Groups: 2 (api-docs, schema-and-events)

   Run: ./my-specs/runner/runner.sh my-specs/tasks/fix-pipeline-docs.md
```

---

## Checklist
- [ ] All target files/code were read and analyzed?
- [ ] Each item references a specific file and fix?
- [ ] No file overlap between groups?
- [ ] Each item is completable by an agent independently?
- [ ] `Allowed Paths` glob patterns correctly restrict the agent's modification scope?
- [ ] All file paths in checklist items were verified to exist (or parent dir exists)?
- [ ] All "delete" items verified that the underlying code/endpoint is truly removed?
- [ ] Folder names match actual Go package names / existing conventions?
- [ ] **Architecture Compliance**: `CONTEXT.md` §6.1 (A1~A6) 준수?

### Allowed Paths Guide

| Type | Typical Allowed Paths |
|------|----------------------|
| docs-sync | `*/docs/**/*.md`, `*/docs/swagger/*` |
| bug-fix (backend) | `*/internal/**/*.go`, `*/docs/**/*.md` |
| bug-fix (frontend) | `ai-platform/frontend/src/**/*.{ts,tsx}`, `ai-platform/frontend/src/**/locales/**/*.json` |
| refactor (backend) | `*/internal/**/*.go`, `*/docs/**/*.md` |
| refactor (frontend) | `ai-platform/frontend/src/**/*.{ts,tsx}` |
| migration | `*/migrations/*.sql`, `*/internal/**/*.go` |
| test (backend) | `*_test.go`, `*/testdata/**` |
| test (frontend) | `ai-platform/frontend/src/**/*.test.{ts,tsx}` |
| config | `*.yaml`, `*.toml`, `*.json`, `Makefile` |

The agent prompt (`my-specs/runner/prompt.md`) instructs the AI agent to respect `Allowed Paths`. This is a **soft constraint** — the runner does NOT parse or enforce it automatically.
