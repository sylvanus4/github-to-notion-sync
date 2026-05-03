---
name: jira-linear-adapter
description: >-
  Bidirectional sync adapter between GitHub Issues/Projects and Jira or
  Linear. Maps fields (status, priority, sprint, assignee) across platforms,
  supports both cloud and server Jira, and maintains consistency. Use when the
  user asks to "sync with Jira", "sync with Linear", "Jira 연동", "Linear 동기화",
  "jira-linear-adapter", or needs cross-platform project management sync. Do
  NOT use for GitHub-only project management (use commit-to-issue), sprint
  triage (use sprint-orchestrator), or creating issues from commits (use
  commit-to-issue).
---

# Jira/Linear Adapter

Bidirectional sync between GitHub Issues/Projects and enterprise project management tools (Jira, Linear).

## When to Use

- When enterprise teams use Jira/Linear but development happens on GitHub
- When cross-team visibility requires unified project tracking
- For Samsung and similar enterprises with established Jira workflows

## Supported Platforms

| Platform | API | Auth | Features |
|----------|-----|------|----------|
| Jira Cloud | REST v3 | API token / OAuth 2.0 | Full bidirectional sync |
| Jira Server/DC | REST v2 | Personal access token | Full bidirectional sync |
| Linear | GraphQL | API key | Full bidirectional sync |

## Field Mapping

### GitHub → Jira/Linear

| GitHub Field | Jira Field | Linear Field |
|-------------|------------|-------------|
| Issue title | Summary | Title |
| Issue body | Description | Description |
| Labels | Labels / Components | Labels |
| Assignees | Assignee | Assignee |
| Milestone | Fix Version | Cycle |
| Project Status | Status (mapped) | State (mapped) |
| Project Priority | Priority (mapped) | Priority (mapped) |
| Project Sprint | Sprint | Cycle |
| Project Size | Story Points | Estimate |

### Status Mapping (configurable)

| GitHub Status | Jira Status | Linear State |
|--------------|-------------|-------------|
| Backlog | To Do | Backlog |
| Ready | Selected for Dev | Todo |
| In Progress | In Progress | In Progress |
| In Review | In Review | In Review |
| Done | Done | Done |
| Cancelled | Won't Do | Cancelled |

### Priority Mapping

| GitHub Priority | Jira Priority | Linear Priority |
|----------------|---------------|----------------|
| P0 (Critical) | Highest | Urgent |
| P1 (High) | High | High |
| P2 (Medium) | Medium | Medium |
| P3 (Low) | Low | Low |

## Workflow

### Step 1: Configuration

Define sync configuration in `.jira-adapter-config.json`:

```json
{
  "platform": "jira-cloud",
  "jira_url": "https://company.atlassian.net",
  "jira_project": "PROJ",
  "github_repo": "org/repo",
  "github_project": 5,
  "sync_direction": "bidirectional",
  "sync_interval": "5m",
  "field_mapping": { ... },
  "status_mapping": { ... }
}
```

### Step 2: Initial Sync

On first run, reconcile existing items:
1. Fetch all open items from both platforms
2. Match by title/description similarity or explicit link
3. Create missing items on the target platform
4. Add cross-reference links (GitHub issue body ↔ Jira description)

### Step 3: Incremental Sync

On each sync cycle:

**GitHub → Jira/Linear**:
1. Detect new/updated GitHub issues since last sync
2. Create or update corresponding Jira/Linear items
3. Map fields using configuration
4. Add sync metadata comment

**Jira/Linear → GitHub**:
1. Detect new/updated Jira/Linear items since last sync
2. Create or update corresponding GitHub issues
3. Update GitHub Project fields
4. Add sync metadata comment

### Step 4: Conflict Resolution

When both sides are modified between syncs:
- **Last-write-wins** for simple fields (title, description)
- **Merge** for additive fields (comments, labels)
- **Alert** for status conflicts (different status on each side)

### Step 5: Sync Report

```
Jira Sync Report
================
Platform: Jira Cloud (company.atlassian.net)
Project: PROJ ↔ GitHub org/repo
Direction: Bidirectional
Last Sync: 2026-03-19 09:30

Changes:
  GitHub → Jira: 3 created, 5 updated
  Jira → GitHub: 1 created, 2 updated

Conflicts: 1
  PROJ-42 / #123: Status mismatch (Jira: "Done", GitHub: "In Review")
  → Action needed: Verify which is correct

Sync Health: ✅ 98% items in sync (1 conflict / 45 total)
```

## Error Handling

| Error | Action |
|-------|--------|
| Jira/Linear API auth failure | Fail fast with clear message; prompt user to verify API token, URL, and permissions |
| Config file `.jira-adapter-config.json` not found | Exit with setup instructions; create sample config template if requested |
| Field mapping mismatch (target field does not exist) | Log unmapped fields; skip invalid mappings; report which fields could not be synced |
| Sync conflict (both sides modified same item) | Surface conflict in report; apply last-write-wins or prompt user for resolution |
| Webhook registration fails | Fall back to polling mode; log webhook error; notify user of degraded sync behavior |

## Examples

### Example 1: Set up Jira sync
User says: "Sync our GitHub project with Jira"
Actions:
1. Configure connection and field mapping
2. Run initial reconciliation
3. Set up incremental sync
Result: Bidirectional sync established

### Example 2: Resolve sync conflict
User says: "Fix the Jira sync conflict on PROJ-42"
Actions:
1. Show both sides of the conflict
2. Ask user which version is correct
3. Apply resolution to both platforms
Result: Conflict resolved, sync restored
