---
name: release-collector
description: >-
  Tuesday RC branch creation for the weekly release cycle. Scans merged PRs on
  dev since the last release, enforces the 3-label gate system (release:approved
  / release:hold / release:blocked), auto-holds unlabeled PRs, cuts an RC branch,
  reverts excluded PRs, creates the Notion weekly release page, and posts results
  to Slack. Use when the user asks to "collect release items", "run Tuesday
  collection", "cut RC branch", "release collector", "화요일 취합", "릴리즈 후보
  수집", "RC 브랜치 생성", "release-collect", or during the Tuesday morning release
  pipeline. Do NOT use for hotfix collection (use hotfix-manager), QA operations
  (use release-qa-gate), or deployment (use release-deployer).
metadata:
  version: "2.0.0"
  category: "execution"
  author: "thaki"
---
# Release Collector (Label-Gated RC Branch)

Tuesday morning workflow: enforce the opt-in label policy, cut an RC branch from dev, revert excluded PRs, build the RC image, populate Notion, and announce on Slack.

## When to Use

- Every Tuesday at 10:00 KST as part of the release cycle
- Called by `release-ops-orchestrator` on Tuesdays
- Manually when an RC branch needs to be (re-)cut mid-week

## Prerequisites

- GitHub CLI (`gh`) authenticated with repo access
- Git access to push branches and tags to origin
- Notion MCP or API token (for `release-notion-board`)
- Slack MCP connected (for `release-slack-ops`)
- Reference: `release-ops-rules.mdc` for the 3-label gate system

## Configuration

`.cursor/skills/release/release-collector/config.json`:

```json
{
  "repository": "thakicloud/ai-platform-webui",
  "collection_deadline": "10:00",
  "timezone": "Asia/Seoul",
  "dev_branch": "dev",
  "release_branch_prefix": "release/"
}
```

## Workflow

### Phase 1: Identify Merged PRs Since Last Release

```bash
# Find the last release tag
LAST_RELEASE=$(git tag --list 'v20*' --sort=-creatordate | head -1)
LAST_DATE=$(git log -1 --format=%ci $LAST_RELEASE | cut -d' ' -f1)

# List all merged PRs since the last release
gh pr list --state merged --base dev \
  --search "merged:>=$LAST_DATE" \
  --json number,title,body,labels,assignees,mergeCommit,mergedAt,url,author \
  --limit 200
```

Collect all merged PRs into a candidate list.

### Phase 2: Classify by Release Label

For each merged PR, classify by its release-inclusion label:

| Label Present | Classification | RC Inclusion |
|---|---|---|
| `release:approved` | Approved | ✅ Included |
| `release:hold` | Held | ❌ Excluded (reverted) |
| `release:blocked` | Blocked | ❌ Excluded (reverted) |
| *(none of the above)* | Unlabeled | ❌ Auto-hold → Excluded |

**2a. Auto-hold unlabeled PRs**

For each merged PR with NO release label (`release:approved`, `release:hold`, `release:blocked`):

```bash
gh pr edit <number> --add-label "release:hold"
```

Log the auto-hold action with PR number and title for the Slack report.

**2b. Validate approved PRs**

For each `release:approved` PR, run validation:
1. Exactly one `risk:*` label (`risk:low`, `risk:medium`, `risk:high`)
2. PR description has 5 required sections (Changes, User Impact, QA Method, Rollback Method, Related Issue/Ticket)
3. PR has an assignee (app owner)
4. `release:approved` and `hotfix` do NOT coexist

Classify validated PRs as:
- **Ready**: All checks pass → included in RC
- **Missing Info**: Validation failures → still included but flagged for resolution before QA
- **Invalid**: Critical issues (missing assignee, conflicting labels) → demoted to `release:hold`

### Phase 3: Cut RC Branch

```bash
RELEASE_DATE=$(date +%Y-%m-%d)  # next Thursday date

# Ensure dev is up to date
git fetch origin dev
git checkout -b release/$RELEASE_DATE origin/dev
```

### Phase 4: Revert Excluded PRs

Collect merge commit SHAs from all excluded PRs (hold + blocked + auto-held). Sort by merge date **newest first** to minimize conflicts:

```bash
# For each excluded PR, in reverse chronological order:
git revert --no-edit <merge_commit_sha>
```

**Conflict handling**:
1. Attempt automated resolution
2. If auto-resolution fails, check if the conflict involves an approved PR
3. If the conflicting approved PR cannot be cleanly preserved → set it to `release:hold` and skip
4. Log all conflict resolutions for the report

After all reverts:

```bash
git push origin release/$RELEASE_DATE

# Tag the RC
RC_TAG="v$(date +%Y.%m.%d)-rc"
git tag $RC_TAG
git push origin $RC_TAG
```

### Phase 5: Create/Update Notion Board

1. Call `release-notion-board` to create the weekly release page
2. For each approved PR (included in RC):
   - Add as release item with Status `Collected`, QA Status `Not Started`
   - Map risk label, assignee, PR URL
   - Add `qa:needed` label to GitHub PR
3. Add a summary section listing held/blocked/auto-held PRs for transparency

### Phase 6: Generate Collection Report

```
📋 RC Branch Created — release/{date}

Included (release:approved): {n} items
Excluded:
  - release:hold (explicit): {n}
  - release:hold (auto): {n}
  - release:blocked: {n}

RC Tag: v{YYYY.MM.DD}-rc
RC Image Build: [pending/triggered]
```

Per-item details:
- Included items: PR link, Owner, Risk, validation status
- Auto-held items: PR link, Owner (so they know their PR was deferred)
- Blocked items: PR link, blocking reason

### Phase 7: Post to Slack

Call `release-slack-ops` with the collection report to `#release-control`:
- Main message: RC branch summary with counts
- Thread 1: Included items table (approved PRs)
- Thread 2: Excluded items table (hold + blocked + auto-held) with reasons
- Thread 3: Action items — QA team can start Wednesday, missing info deadlines

### Phase 8: Persist State

Write to `outputs/release-ops/{date}/collection.json`:

```json
{
  "date": "2026-04-08",
  "target_release_date": "2026-04-10",
  "rc_branch": "release/2026-04-10",
  "rc_tag": "v2026.04.10-rc",
  "notion_page_id": "<page_id>",
  "total_merged": 48,
  "included": 15,
  "excluded_hold_explicit": 20,
  "excluded_hold_auto": 10,
  "excluded_blocked": 3,
  "revert_conflicts": [],
  "items": [
    {
      "pr_number": 123,
      "pr_url": "https://github.com/...",
      "title": "...",
      "merge_commit": "abc123",
      "label": "release:approved",
      "risk": "medium",
      "assignee": "user",
      "rc_status": "included",
      "validation": {"risk": true, "template": true, "assignee": true, "exclusive": true}
    }
  ]
}
```

## Output Artifacts

| Phase | Output | Skip Flag |
|---|---|---|
| 1 | `outputs/release-ops/{date}/merged-prs.json` | `skip-scan` |
| 2 | `outputs/release-ops/{date}/classification.json` | `skip-classify` |
| 4 | `release/{date}` branch + RC tag | `skip-branch` |
| 5 | Notion weekly release page | `skip-notion` |
| 7 | Slack `#release-control` message | `skip-slack` |
| 8 | `outputs/release-ops/{date}/collection.json` | — |

## Error Recovery

- GitHub API failure: retry once, then report with error details
- Git revert conflict: log, attempt skip, demote conflicting approved PR to hold
- Notion failure: persist to local JSON, report
- Slack failure: save to `outputs/release-ops/{date}/pending-slack-collection.md`
- RC branch already exists: prompt to delete and re-cut, or abort

## Gotchas

- PRs without ANY release label are auto-held — this is by design (opt-in model)
- Revert order matters: newest-first minimizes cascading conflicts
- A PR's merge commit SHA is required for revert; `gh pr view --json mergeCommit` provides it
- Multiple merge commits from the same PR (squash vs merge commit) need careful handling
- The RC image must be deployed to dev for QA — coordinate with CI/CD pipeline
- Auto-held PRs: app owners should be individually notified so they can plan for next cycle
