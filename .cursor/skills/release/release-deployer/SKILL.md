---
name: release-deployer
description: >-
  Thursday deployment operations for the weekly release cycle. Promotes the
  QA-verified RC image to a production tag (vYYYY.MM.DD), deploys it to
  production via ArgoCD, restores the dev environment to the latest dev HEAD
  image, and posts confirmation to Slack. Use when the user asks to "run
  deployment", "Thursday deploy", "release deploy", "promote RC image",
  "목요일 배포", "릴리즈 배포", "release-deployer", or during the Thursday
  deployment pipeline. Do NOT use for Tuesday collection (use release-collector),
  Wednesday QA (use release-qa-gate), or hotfix deployment (use hotfix-manager).
metadata:
  version: "3.0.0"
  category: "execution"
  author: "thaki"
---
# Release Deployer (Image Promotion to Production)

Thursday deployment lifecycle: lock the release list, promote the QA-verified RC image to a production tag (`vYYYY.MM.DD`), deploy to production via ArgoCD, restore dev to its latest HEAD image, and record the cycle retrospective.

## When to Use

- Thursday morning as part of the release cycle
- Called by `release-ops-orchestrator` on Thursdays
- Manually when deployment operations need to be tracked

## Prerequisites

- QA gate completed — `qa-results.json` from `release-qa-gate` exists with `gate_status = OPEN`
- RC image tag exists on ghcr.io (created by `release-collector`)
- `collection.json` available with `rc_image_tag`
- Kubernetes / ArgoCD access to deploy images to production and dev
- Notion weekly release page populated
- Slack MCP connected
- Reference: `release-ops-rules.mdc` for deployment rules

## Workflow

### Phase 1: Lock Release List

1. Load `outputs/release-ops/{date}/qa-results.json`
2. Verify `gate_status = OPEN` — abort if CLOSED
3. Extract deploy candidates (items with `qa_status` = Pass or Conditional Pass)
4. Enforce Rule 5: reject any requests to add new items on Thursday
5. Generate deploy manifest

```json
{
  "date": "2026-04-10",
  "locked_at": "2026-04-10T09:00:00+09:00",
  "rc_image_tag": "rc-20260408103000",
  "production_tag": "v2026.04.10",
  "deploy_time": "10:00",
  "total": 13,
  "risk_profile": {"high": 2, "medium": 6, "low": 5},
  "items": [...]
}
```

### Phase 2: Pre-Deploy Announcement

Call `release-slack-ops` to `#release-control`:
- Main message: item count, deploy time, RC image tag, production tag, risk profile, LOCKED notice
- Thread 1: Full item list with owners and rollback plans
- Thread 2: Deployment sequence and timeline

### Phase 3: Promote RC Image and Deploy to Production

The RC image (already verified by QA on dev) is promoted to the production tag and deployed:

```bash
# 1. Tag the RC image as the production release
#    source: ghcr.io/thakicloud/ai-platform-webui:rc-20260408103000
#    target: ghcr.io/thakicloud/ai-platform-webui:v2026.04.10
#    Trigger CI workflow to re-tag:
gh workflow run release-webui.yaml -f image_tag=v2026.04.10

# 2. Deploy to production via ArgoCD
#    Update Helm values with the new image tag
#    ArgoCD syncs and deploys the production image

# 3. Verify rollout
kubectl rollout status deployment/<app> -n production --timeout=300s
```

Track deployment status for each service:
- `Ready for Release` → `Released` (successful deployment)
- `Ready for Release` → `Rollback` (deployment failed)

Update Notion for each deployed item.

### Phase 4: Post-Deploy Verification

After production deployment:

1. Run smoke tests against production
2. Monitor error rates and latency for 30 minutes
3. If issues detected → initiate rollback to previous production image tag

### Phase 5: Create Git Release Tag

After production is stable, create the git tag for traceability:

```bash
# Tag the dev commit corresponding to the RC image
git fetch origin dev
git tag v2026.04.10 <dev_head_sha_from_collection>
git push origin v2026.04.10
```

No branch merge is needed — the image tagging model does not use release branches.

### Phase 6: Restore Dev Environment

Restore the dev environment from the RC image back to the latest `dev` HEAD image:

```bash
# Deploy the latest dev HEAD image to the dev environment
# The latest dev-{TIMESTAMP} image from CI is used
# ArgoCD or Helm redeploy to dev with the dev HEAD image tag
```

This unblocks app owners to test their held/blocked PRs for the next cycle.

### Phase 7: Post-Deploy Cleanup

1. PRs with `release:approved` + `qa:done`: no action needed (already shipped)
2. PRs with `release:hold`: remain on `dev` for next cycle consideration
3. PRs with `release:blocked`: need fixes before reconsideration; app owner notified
4. Remove `release:approved` labels from shipped PRs (cycle complete)

### Phase 8: Post-Deploy Announcement + Retrospective

Call `release-slack-ops` to `#release-control`:
- Main message: deployed count, production tag, RC image tag, monitoring status
- Thread 1: Deployed items with confirmation
- Thread 2: Rolled back items with reasons (if any)
- Thread 3: 3 improvement points for next cycle

Collect and record improvement points:

```json
{
  "date": "2026-04-10",
  "production_tag": "v2026.04.10",
  "rc_image_tag": "rc-20260408103000",
  "rc_image_url": "ghcr.io/thakicloud/ai-platform-webui:rc-20260408103000",
  "deployed": 13,
  "rolled_back": 0,
  "dev_restored": true,
  "improvements": [
    "Improvement 1: ...",
    "Improvement 2: ...",
    "Improvement 3: ..."
  ],
  "monitoring_end": "2026-04-10T14:00:00+09:00"
}
```

### Phase 9: Persist Final State

Write to `outputs/release-ops/{date}/deploy-results.json`:

```json
{
  "date": "2026-04-10",
  "rc_image_tag": "rc-20260408103000",
  "rc_image_url": "ghcr.io/thakicloud/ai-platform-webui:rc-20260408103000",
  "production_tag": "v2026.04.10",
  "git_tag": "v2026.04.10",
  "total_candidates": 13,
  "deployed": 13,
  "rolled_back": 0,
  "dev_restored": true,
  "items": [
    {
      "pr_number": 123,
      "pr_url": "...",
      "title": "...",
      "risk": "medium",
      "status": "Released",
      "deployed_at": "2026-04-10T10:15:00+09:00"
    }
  ]
}
```

## Output Artifacts

| Phase | Output | Skip Flag |
|---|---|---|
| 1 | `outputs/release-ops/{date}/deploy-manifest.json` | — |
| 2 | Slack `#release-control` pre-deploy | `skip-slack` |
| 3 | Production deployment + image promotion | `skip-deploy` |
| 5 | Git release tag | `skip-tag` |
| 6 | Dev environment restore | `skip-dev-restore` |
| 8 | Slack `#release-control` post-deploy | `skip-slack` |
| 9 | `outputs/release-ops/{date}/deploy-results.json` | — |

## Error Recovery

- QA gate not OPEN: abort deployment, alert Release Owner
- Image promotion fails: retry CI workflow, report status
- Production deploy fails: rollback to previous production image tag, record in results
- Dev restore fails: retry, alert — dev should not stay on RC image
- Slack failure: save to `outputs/release-ops/{date}/pending-slack-deploy.md`

## Gotchas

- The RC image deployed to production is the SAME image that passed QA on dev — no rebuild
- Image promotion = re-tagging the same image digest, not rebuilding
- No branch merges or branch deletions — the image tagging model eliminates release branches entirely
- After production deploy, dev MUST be restored to dev HEAD to unblock development
- Rule 5 enforcement: no new items on Thursday, only approved hotfixes via `#hotfix-alert`
- Monitoring duration: 30 min minimum for high-risk items, 15 min for low-risk
- The 3 improvement points are mandatory — even if everything went well, note what worked
- Label cleanup (`release:approved` removal) signals cycle completion for that PR
