---
name: release-notion-board
description: >-
  Notion CRUD for Weekly Release and Hotfix Queue databases. Create weekly
  release pages, update item statuses, query by status/app/date, and manage
  hotfix queue entries. Use when the user asks to "create release board",
  "update release status", "query release items", "릴리즈 보드 생성", "릴리즈 상태 업데이트",
  "release-notion-board", or any Notion CRUD for release operations. Do NOT
  use for general Notion page creation (use md-to-notion), meeting sync (use
  notion-meeting-sync), or non-release database operations (use Notion MCP
  directly).
disable-model-invocation: true
---

# Release Notion Board

Notion database CRUD operations for the Weekly Release and Hotfix Queue boards. Infrastructure skill used by other release skills — rarely invoked directly.

## When to Use

- Called by `release-collector` to create/populate weekly release pages
- Called by `release-qa-gate` to update QA statuses
- Called by `release-deployer` to transition items to Released
- Called by `hotfix-manager` to create/update hotfix queue entries
- Directly when the user needs to manually create or query release boards

## Prerequisites

- Notion MCP server connected and authenticated
- Parent page ID for release boards configured in `config.json`
- Reference schema: `release-ops-orchestrator/references/notion-schema.md`

## Configuration

Create `.cursor/skills/release/release-notion-board/config.json` if not present:

```json
{
  "weekly_release_parent_page": "<NOTION_PAGE_ID>",
  "hotfix_queue_parent_page": "<NOTION_PAGE_ID>"
}
```

## Workflow

### Operation 1: Create Weekly Release Page

Create a new `Weekly Release - YYYY-MM-DD` page as a Notion database.

1. Calculate the next Thursday date for the title
2. Search Notion for existing page with this title to avoid duplicates
3. Create the database page with properties from the schema:
   - **App** (select): `ai-platform`, `agent-studio`, `other`
   - **Title** (title): Item name
   - **GitHub Issue** (url): Link to GitHub issue
   - **GitHub PR** (url): Link to GitHub PR
   - **Assignee** (people): App owner
   - **Status** (select): `Draft`, `Collected`, `Ready for QA`, `QA Passed`, `Hold`, `Ready for Release`, `Released`
   - **QA Status** (select): `Not Started`, `In Progress`, `Pass`, `Fail`, `Conditional Pass`
   - **Risk** (select): `low`, `medium`, `high`
   - **Business Team Share Status** (checkbox)
   - **QA Team Share Status** (checkbox)
   - **Release Inclusion Status** (select): `Included`, `Excluded`, `Deferred`

4. Return the created page ID for downstream use

**Tools**: Notion MCP `notion-create-pages`

### Operation 2: Add Release Item

Add a row to the weekly release database.

1. Read the weekly release page ID (from Operation 1 or config)
2. Map GitHub PR data to Notion properties:
   - Title from PR title
   - GitHub PR URL
   - GitHub Issue URL (from linked issues)
   - Assignee from PR author
   - App from `app:*` label
   - Risk from `risk:*` label
   - Status: `Collected`
   - QA Status: `Not Started`
   - Release Inclusion: `Included`
3. Create the database row via Notion MCP

**Tools**: Notion MCP `notion-create-pages`

### Operation 3: Update Item Status

Update one or more properties on an existing release item.

1. Find the item by title or GitHub PR URL via `notion-query-database`
2. Validate status transitions:
   - `Draft` → `Collected` (by collector)
   - `Collected` → `Ready for QA` (by collector)
   - `Ready for QA` → `QA Passed` or `Hold` (by qa-gate)
   - `QA Passed` → `Ready for Release` (by qa-gate)
   - `Ready for Release` → `Released` (by deployer)
   - Any → `Hold` (by any skill when issues found)
3. Update via Notion MCP `notion-update-page`

**Tools**: Notion MCP `notion-update-page`

### Operation 4: Query Release Items

Query the release database with filters.

1. Accept filter criteria: status, app, date range, assignee
2. Build Notion filter object
3. Query via `notion-query-database`
4. Return structured results

Common queries:
- All items with status `Ready for QA` (for Wednesday QA)
- All items with status `Ready for Release` (for Thursday deploy)
- All items with status `Hold` (blockers)
- Items by app for per-app owner summaries

**Tools**: Notion MCP `notion-query-database`

### Operation 5: Create Hotfix Entry

Create a new entry in the Hotfix Queue database.

1. Read the hotfix queue page ID from config
2. Create entry with properties:
   - **App** (select): `ai-platform`, `agent-studio`, `other`
   - **Urgency** (select): `Critical`, `High`, `Medium`
   - **Customer/Business Impact** (rich_text): Impact description
   - **Request Background** (rich_text): Context
   - **Today's Deployment Status** (select): `Pending`, `In Progress`, `Deployed`, `Rolled Back`
   - **Business Team Notification** (checkbox)
   - **QA Completion Status** (select): `Not Started`, `In Progress`, `Done`
3. Return the created entry ID

**Tools**: Notion MCP `notion-create-pages`

### Operation 6: Update Hotfix Entry

Update hotfix queue entry status (notification, QA, deployment).

Same pattern as Operation 3 but targeting the Hotfix Queue database.

**Tools**: Notion MCP `notion-update-page`

## Output Artifacts

| Operation | Output | Persistence |
|---|---|---|
| Create Weekly Release | Page ID | Returned to caller |
| Add Release Item | Row ID | Returned to caller |
| Update Status | Updated page | In-place Notion update |
| Query Items | Structured JSON | Returned to caller |
| Create Hotfix | Entry ID | Returned to caller |

## Error Recovery

- If Notion MCP is unavailable: report error with instructions to check MCP connection
- If page already exists (duplicate create): return existing page ID instead of creating duplicate
- If status transition is invalid: reject with current status and allowed transitions

## Gotchas

- Notion API does not support pipe tables — use bulleted lists or structured blocks
- Page IDs are 32-char hex strings without dashes
- Select property values must match exactly (case-sensitive)
- Rate limits: max ~3 requests/second to Notion API; batch operations where possible
