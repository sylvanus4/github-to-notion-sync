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
3. **Parallel-Ready**: Split into `#### Group:` headers when tasks touch different files.
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
2. **Delete verification**: Before instructing deletion of any file, VERIFY the corresponding code/endpoint/feature is truly removed. Check `router.go`, handler files, and swagger annotations. If the code still exists, the doc must NOT be deleted.
3. **Naming verification**: Before specifying folder or file names, cross-reference the actual Go package names, DB table names, and existing naming conventions in the docs directory.
4. **Scope matching**: Each checklist item must specify whether it modifies `docs/` only or also requires source code changes. Never mix scope implicitly.

### 3. Design Groups
- Tasks touch different files → separate `#### Group:` headers (parallel execution)
- Tasks share files or have ordering dependency → single group (sequential execution)
- Few tasks (3 or less) → flat checklist, no groups needed

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

#### Group: [name-1]
- [ ] `path/to/file` — [specific fix description]
- [ ] `path/to/file2` — [specific fix description]

#### Group: [name-2]
- [ ] `path/to/file3` — [specific fix description]

## Should-have (Optional)
- [ ] [lower priority items]
```

> `#### Group:` headers are optional. Omit them if tasks are few or must run sequentially.

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
| bug-fix | `*/internal/**/*.go`, `*/docs/**/*.md` |
| refactor | `*/internal/**/*.go`, `*/docs/**/*.md` |
| migration | `*/migrations/*.sql`, `*/internal/**/*.go` |
| test | `*_test.go`, `*/testdata/**` |
| config | `*.yaml`, `*.toml`, `*.json`, `Makefile` |

The runner enforces `Allowed Paths` — files outside this scope are automatically unstaged before commit.
