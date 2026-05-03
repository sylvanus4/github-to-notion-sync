---
name: release-collector
description: >-
  Tuesday RC image tagging for the weekly release cycle. Scans merged PRs on
  dev since the last release, enforces the 3-label gate system
  (release:approved / release:hold / release:blocked), auto-holds unlabeled
  PRs, re-tags the dev HEAD image as rc-{TIMESTAMP}, creates the Notion weekly
  release page, and posts results to Slack. Use when the user asks to "collect
  release items", "run Tuesday collection", "tag RC image", "release
  collector", "화요일 취합", "릴리즈 후보 수집", "RC 이미지 태깅", "release-collect", or during
  the Tuesday morning release pipeline. Do NOT use for hotfix collection (use
  hotfix-manager), QA operations (use release-qa-gate), or deployment (use
  release-deployer).
---

# Release Collector (Image Tagging Model)

Tuesday morning workflow: enforce the opt-in label policy, verify dev HEAD contains all approved PRs, re-tag the dev image as `rc-{TIMESTAMP}`, deploy the RC image to dev for QA, populate Notion, and announce on Slack.

## When to Use

- Every Tuesday at 10:00 KST as part of the release cycle
- Called by `release-ops-orchestrator` on Tuesdays
- Manually when an RC image needs to be (re-)tagged mid-week

## Prerequisites

- GitHub CLI (`gh`) authenticated with repo access
- Git access to the repository
- CI/CD pipeline access (to trigger image re-tagging via `release-webui.yaml`)
- Notion MCP or API token (for `release-notion-board`)
- Slack MCP connected (for `release-slack-ops`)
- Reference: `release-ops-rules.mdc` for the 3-label gate system

## Configuration

`.cursor/skills/release/release-collector/config.json`:

```json
{
  "repository": "thakicloud/ai-platform-strategy",
  "collection_deadline": "10:00",
  "timezone": "Asia/Seoul",
  "dev_branch": "dev",
  "image_registry": "ghcr.io/thakicloud/ai-platform-strategy"
}
```

## Workflow

### Phase 1: Identify Merged PRs Since Last Release

```bash
LAST_RELEASE=$(git tag --list 'v20*' --sort=-creatordate | head -1)
LAST_DATE=$(git log -1 --format=%ci $LAST_RELEASE | cut -d' ' -f1)

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
| `release:hold` | Held | ❌ Excluded |
| `release:blocked` | Blocked | ❌ Excluded |
| *(none of the above)* | Unlabeled | ❌ Auto-hold → Excluded |

**2a. Auto-hold unlabeled PRs**

For each merged PR with NO release label:

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

### Phase 3: Verify Dev HEAD and Select Image

Verify that `dev` HEAD contains all approved PRs and does not include any `release:blocked` changes that would require exclusion.

```bash
git fetch origin dev

# Get the dev HEAD SHA
DEV_HEAD=$(git rev-parse origin/dev)

# Identify the dev image tag corresponding to HEAD
# The CI produces dev-{TIMESTAMP} tags; find the latest
DEV_IMAGE_TAG="dev-$(date -u +%Y%m%d%H%M%S)"  # approximate; verify via ghcr.io
```

**Handling exclusions**: If a `release:blocked` PR is interleaved with approved changes on dev HEAD:

1. **Best case**: An earlier dev image (before the blocked PR was merged) contains all approved PRs. Select that image.
2. **Revert case**: Revert the blocked PR from `dev`, wait for CI to build a new `dev-{TIMESTAMP}` image, then proceed with the new HEAD.
3. The RC is always a single immutable image — no partial modifications.

### Phase 4: Tag RC Image

Once the correct dev image is identified, re-tag it as the RC:

```bash
RC_TIMESTAMP=$(date +%Y%m%d%H%M%S)
RC_TAG="rc-${RC_TIMESTAMP}"

# Trigger CI to re-tag the image
gh workflow run release-webui.yaml -f image_tag=$RC_TAG
```

Deploy the RC image to the dev environment for QA:

```bash
# ArgoCD or Helm deployment to dev with the RC image tag
# The exact mechanism depends on the deploy pipeline
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
📋 RC Image Tagged — rc-{TIMESTAMP}

Included (release:approved): {n} items
Excluded:
  - release:hold (explicit): {n}
  - release:hold (auto): {n}
  - release:blocked: {n}

Source: dev HEAD ({short_sha})
RC Image: ghcr.io/thakicloud/ai-platform-strategy:rc-{TIMESTAMP}
Production Tag (Thursday): vYYYY.MM.DD
```

Per-item details:
- Included items: PR link, Owner, Risk, validation status
- Auto-held items: PR link, Owner (so they know their PR was deferred)
- Blocked items: PR link, blocking reason

### Phase 7: Post to Slack

Call `release-slack-ops` with the collection report to `#release-control`:
- Main message: RC image summary with counts and image tag
- Thread 1: Included items table (approved PRs)
- Thread 2: Excluded items table (hold + blocked + auto-held) with reasons
- Thread 3: Action items — QA team can start Wednesday, missing info deadlines

### Phase 8: Persist State

Write to `outputs/release-ops/{date}/collection.json`:

```json
{
  "date": "2026-04-08",
  "target_release_date": "2026-04-10",
  "dev_head_sha": "abc123def",
  "rc_image_tag": "rc-20260408103000",
  "rc_image_url": "ghcr.io/thakicloud/ai-platform-strategy:rc-20260408103000",
  "production_tag": "v2026.04.10",
  "notion_page_id": "<page_id>",
  "total_merged": 48,
  "included": 15,
  "excluded_hold_explicit": 20,
  "excluded_hold_auto": 10,
  "excluded_blocked": 3,
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
| 4 | RC image tag on ghcr.io | `skip-tag` |
| 5 | Notion weekly release page | `skip-notion` |
| 7 | Slack `#release-control` message | `skip-slack` |
| 8 | `outputs/release-ops/{date}/collection.json` | — |

## Error Recovery

- GitHub API failure: retry once, then report with error details
- Image tagging failure: report CI workflow status, suggest manual re-trigger
- Notion failure: persist to local JSON, report
- Slack failure: save to `outputs/release-ops/{date}/pending-slack-collection.md`
- RC image already exists with same tag: use a new timestamp suffix

## Gotchas

- PRs without ANY release label are auto-held — this is by design (opt-in model)
- No branch cuts or reverts — the image tagging model freezes the artifact, not the branch
- If a blocked PR must be excluded and it's already in dev HEAD, either select an earlier dev image or revert from dev and rebuild
- The RC image must be deployed to dev for QA — coordinate with the CI/CD pipeline
- Auto-held PRs: app owners should be individually notified so they can plan for next cycle
- The RC image tag is immutable once created — if changes are needed, create a new RC with a new timestamp
