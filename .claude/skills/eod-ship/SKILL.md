---
name: eod-ship
description: End-of-day shipping pipeline — cursor-sync, release-ship all 5 projects, and Slack summary.
disable-model-invocation: true
---

Run the complete end-of-day shipping pipeline.

## Pipeline (Sequential)

1. **Cursor Sync**: Sync .cursor/ assets across all 5 repos via cursor-sync
1½. **Claude Sync**: Sync .claude/ assets (rules, commands, skills, hooks) across all 5 repos via claude-sync
2. **Release Ship**: For each of the 5 managed repos:
   - Domain-split commits for uncommitted changes
   - Git push
   - Create/update PR if needed
3. **Commit-to-Issue**: Create GitHub issues from new commits, link to Project #5
4. **Daily Skill Digest**: Extract coding patterns and skill usage stats
5. **Slack Summary**: Post consolidated EOD report to #효정-할일

## Managed Repositories

- ai-platform-strategy
- ai-model-event-stock-analytics
- research
- ai-template
- github-to-notion-sync

## Rules

- Phase 2¾ commit-to-issue is MANDATORY — never skip
- All issues must be added to ThakiCloud Project #5 with 5 fields set
- Use `git push --no-verify` if pre-push hook hangs >4min on E2E tests
