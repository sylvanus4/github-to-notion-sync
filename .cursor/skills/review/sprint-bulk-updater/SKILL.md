---
name: sprint-bulk-updater
description: >-
  Bulk update GitHub Project sprint field for all items with Status 'Todo' or
  'In Progress' assigned to a given user, pulling them into the current week's
  sprint iteration. Paginates the full project board via GraphQL, identifies
  mismatched items, confirms with user, and executes batch mutations with rate
  limiting. Use when the user asks to 'pull all items to this sprint', 'bulk
  update sprint', 'move todo/in-progress to current sprint', 'consolidate
  sprint assignments', 'sprint-bulk-updater', or wants to align scattered
  sprint assignments to the active iteration. Korean triggers: '스프린트 일괄
  변경', '이번주 스프린트로 당겨줘', '스프린트 벌크 업데이트', '스프린트 당겨줘',
  '스프린트 정리', '일괄 스프린트', '스프린트 통합', 'Todo 스프린트 변경',
  '미래 스프린트 당기기'. Do NOT use for single-issue sprint changes (use
  gh project item-edit directly). Do NOT use for creating new issues (use
  commit-to-issue). Do NOT use for sprint triage and priority assignment (use
  sprint-orchestrator). Do NOT use for status changes without sprint context.
  Do NOT use for cross-project bulk operations (this targets a single GitHub
  Project).
metadata:
  author: thaki
  version: "2.0.0"
  category: review
---

# Sprint Bulk Updater

Pull all **Todo** and **In Progress** items assigned to a user into the current week's sprint in one batch.

## Workflow

### Phase 0: Pre-flight Validation

1. Run `gh auth status` — abort with `Run 'gh auth login' first` if not authenticated
2. Verify org/project access with a lightweight query (`projectV2(number: N) { id }`)
3. Confirm the sprint iteration field exists in the project

If any check fails, STOP with a specific remediation message before making API calls.

### Phase 1: Discover Current Sprint

Query the project's iteration field to find the sprint whose date range contains today.

```bash
gh api graphql -f query='
query {
  organization(login: "ThakiCloud") {
    projectV2(number: 5) {
      fields(first: 50) {
        nodes {
          ... on ProjectV2IterationField {
            id name
            configuration {
              iterations { id title startDate duration }
            }
          }
        }
      }
    }
  }
}'
```

**Date comparison logic**: For each iteration, compute `endDate = startDate + (duration * 7) days`. Select the iteration where `startDate ≤ today < endDate`. If `--sprint` is provided, match by title instead — validate the title exists in the iteration list before proceeding.

If no matching iteration exists, STOP and report with the list of available sprint titles.

### Phase 2: Paginated Scan

Fetch all project items page-by-page (`first: 100`, follow `endCursor`) and filter. Project #5 has 400+ items — expect 4-6 pages. Report progress: `Scanning page X... Y matches so far`.

Criteria:
1. **Content type** is Issue (skip `DraftIssue` nodes — they have no `assignees`)
2. **Assignee** matches the target user(s). When `--user` contains commas (e.g., `user1,user2`), split and match any (OR logic)
3. **Status** matches any value in `--statuses`. Parse: split by comma, trim whitespace, case-insensitive match against the project's SingleSelect options. If a provided status doesn't match any option, warn and skip it
4. **Sprint (스프린트)** is null, empty, or NOT equal to the target sprint from Phase 1

Collect each match as `{ item_id, number, title, status, sprint }`.

If a page fetch fails (network error, GraphQL error), log the cursor value and page number, attempt the next page, and note the gap in coverage at the end.

After all pages: report `Scanned X pages (Y total items). Z items match criteria.`

See `references/project-config.md` for the GraphQL query template and jq filter.

### Phase 3: Confirm

Present a summary table to the user:

```
Found N items to update → TARGET_SPRINT

| # | Issue | Current Status | Current Sprint |
|---|-------|---------------|----------------|
| 1 | #1234 Title | Todo | 26-04-Sprint4 |
| 2 | #5678 Title | In Progress | none |

Proceed? (Y/n)
```

If `--dry-run`, print the table and STOP. Otherwise wait for user confirmation before mutating.

### Phase 4: Batch Mutation

For each item, run the `updateProjectV2ItemFieldValue` mutation.

**Rate limiting and retry strategy:**

| Attempt | Sleep before | On failure |
|---------|-------------|------------|
| 1st | 300ms | Retry |
| 2nd | 1s | Retry |
| 3rd | 3s | Log FAIL, move to next item |

**Circuit breaker:** If 5 consecutive items fail, STOP batch and report partial results — persistent failures indicate a systemic issue (auth expiry, API outage).

**Response validation:** Each successful mutation response must contain the updated iteration value. If the response lacks confirmation, count as UNCERTAIN and include in the verification phase.

Track results per item as OK/FAIL/UNCERTAIN. Report grouped summary:

```
Updated N/M items to TARGET_SPRINT

Uncertain: #3456 (no confirmation in response)
Failures by type:
  RATE_LIMITED (retries exhausted): #1234, #5678
  NOT_FOUND (deleted): #9012
  UNKNOWN: #3456 — [raw error]
```

### Phase 5: Post-update Verification

Re-scan the project to count items now on the target sprint for the target user. Compare against expected count (Phase 4 successes + previously correct items).

```
Verification: X items on TARGET_SPRINT (expected: Y)
Discrepancies: #1234 still on old sprint, #5678 not found
```

If discrepancies exist, list issue numbers and suggest manual review.

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--user` | `sylvanus4` | GitHub login(s) to filter. Comma-separated for multiple (OR logic) |
| `--project` | `5` | ThakiCloud project number |
| `--org` | `ThakiCloud` | GitHub organization |
| `--sprint` | auto-detect | Target sprint title (auto from today's date if omitted). Must match an existing iteration title |
| `--statuses` | `Todo,In Progress` | Comma-separated status values. Case-insensitive, validated against project's SingleSelect options |
| `--dry-run` | `false` | Print what would change without mutating |

### Parameter Validation

| Parameter | Invalid Input | Behavior |
|-----------|---------------|----------|
| `--user` | Non-existent login | No items match — reported as "0 items match criteria" |
| `--statuses` | Unknown status value | Warn per invalid value, proceed with valid ones. If ALL invalid, STOP |
| `--sprint` | Non-existent title | STOP with list of available sprint titles |
| `--project` | Non-existent project | STOP with "Project not found" after Phase 0 query fails |
| `--org` | Non-existent org | STOP with "Organization not found" |

### Parameter Interactions

- `--sprint` overrides auto-detect but all other filters (`--user`, `--statuses`) still apply
- `--dry-run` is compatible with all other parameters
- When `--statuses=Todo` is used alone, only Todo items are processed (In Progress excluded)
- After bulk sprint update, optionally invoke `sprint-orchestrator` for priority assignment

## Key Constants

See `references/project-config.md` for Project ID, Field IDs, Status Option IDs, Sprint discovery queries, GraphQL templates, and jq filters.

## Examples

### Example 1: Pull all Todo/In Progress to current sprint

User says: "이번주 스프린트로 다 당겨줘"

1. Phase 0 verifies auth and project access
2. Phase 1 discovers `26-04-Sprint5` as the current iteration
3. Phase 2 scans 5 pages (487 items), finds 34 matches
4. Phase 3 shows summary table, user confirms
5. Phase 4 mutates all 34 items with retry, reports `Updated 34/34`
6. Phase 5 verifies 34 items now on `26-04-Sprint5`

### Example 2: Dry run check

User says: "sprint-bulk-updater --dry-run"

1-3 same as above, but stops after Phase 3 without mutating

### Example 3: Override target sprint

User says: "26-05-Sprint1으로 일괄 변경해줘"

1. Phase 1 matches `26-05-Sprint1` by title instead of date
2-6 proceed normally with the overridden target

### Example 4: Todo only, custom user

User says: "Todo인 것만 당겨줘 --user=otherdev"

1. Phase 1 auto-detects current sprint
2. Phase 2 filters: Status=Todo only, Assignee=otherdev
3-6 proceed normally

## Error Handling

| Error | Retry | Action |
|-------|-------|--------|
| `gh auth` failure | No | STOP in Phase 0 with `gh auth login` instructions |
| Rate limiting | Up to 3x (300ms→1s→3s) | Log FAIL after 3rd attempt, continue next item |
| NOT_FOUND item | No | Log and skip — item deleted between scan and mutation |
| No matching sprint | No | STOP with available sprint titles — do not guess |
| Empty result set | No | Report "0 items match" — valid outcome |
| Page fetch failure | No | Log cursor, skip page, continue. Note coverage gap |
| 5 consecutive failures | No | Circuit breaker: STOP batch, report partial results |
| Unexpected GraphQL error | No | Log raw error, classify as UNKNOWN in failure report |
| Invalid status value | No | Warn and skip; proceed with remaining valid statuses |

## Constraints

- NEVER change Status — this skill only touches the Sprint (스프린트) field
- NEVER create or delete issues
- NEVER modify items not assigned to the target user(s)
- Always confirm with the user before batch mutation (unless `--dry-run`)
- Sprint field name in the project is Korean: `스프린트`
- Skip `DraftIssue` content types — they lack assignee data
