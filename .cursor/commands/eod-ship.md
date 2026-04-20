## EOD Ship

End-of-day multi-project shipping pipeline: cursor-sync assets, release-ship the current project (푸시 포함), **작업 브랜치를 `main`에 머지·푸시(Phase 2½)**, 5개 관리 프로젝트 release-ship, Slack `#효정-할일`에 요약.

### Usage

```
# Full pipeline (sync + ship all + Slack notify)
/eod-ship

# Skip cursor-sync, ship only
/eod-ship --skip-sync

# Ship specific projects only (comma-separated)
/eod-ship --targets research,ai-template

# Preview only (no commits, no push, no Slack)
/eod-ship --dry-run

# Skip Slack notification
/eod-ship --no-slack
```

### Workflow

1. **Cursor Sync** — Sync `.cursor/` assets to all target projects
2. **Ship Current** — `release-ship`로 현재 레포 커밋·푸시(서브모듈 포인터 `ai-suite` / `thaki-ui` / `ai-platform-webui` 포함)
3. **Merge to main** — 현재 브랜치가 `main`이 아니면 `main`에 머지 후 `git push origin main`, 다시 원래 브랜치로 복귀
4. **Ship 5 Projects** — 관리 프로젝트를 순서대로 release-ship
5. **Slack** — Post consolidated report to `#효정-할일`
6. **Report** — Display summary in chat

### Execution

Read and follow the `eod-ship` skill (`.cursor/skills/eod-ship/SKILL.md`) for pipeline phases, project registry, and error handling.

### Examples

Wrap up everything at end of day:
```
/eod-ship
```

Ship without syncing cursor assets:
```
/eod-ship --skip-sync
```

Ship only specific projects:
```
/eod-ship --targets research
```

Preview what would be shipped:
```
/eod-ship --dry-run
```
