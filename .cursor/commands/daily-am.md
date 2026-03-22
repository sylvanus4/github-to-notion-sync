## Daily AM — Morning Pipeline

Run the full morning automation pipeline: pre-flight checks, git sync, Google Workspace (calendar + Gmail), email intelligence, market intelligence, news/content, AI research, dev intelligence, and a consolidated Slack briefing. Orchestrates 15+ skills across 8 parallel phases.

### Usage

```
# Full morning pipeline (all 8 phases)
/daily-am

# Skip specific phases
/daily-am --skip-phase 4           # skip Market Intelligence
/daily-am --skip-phase 3,6         # skip Email Intel + AI Research

# Run only specific phases
/daily-am --only-phase 2,3         # Google + Email only

# Convenience shortcuts
/daily-am --skip-market            # skip market (auto on weekends)
/daily-am --skip-email             # skip email intelligence
/daily-am --skip-research          # skip AI research

# Output control
/daily-am --no-slack               # suppress all Slack posts
/daily-am --dry-run                # preview plan, no execution
```

### Workflow

1. **Phase 0**: Pre-flight — `setup-doctor` validates PostgreSQL, gws auth, env vars, MCP
2. **Phase 1**: Git Sync — `sod-ship` commits, pushes, pulls all 5 projects
3. **Phase 2**: Google Workspace — `google-daily` (calendar + Gmail + Drive)
4. **Phase 3**: Email Intelligence — `email-auto-reply`, `email-research-dispatcher`, `proactive-meeting-scheduler`, `feedback-meeting-scheduler`
5. **Phase 4**: Market Intelligence — `today` pipeline (parallel with 2-3)
6. **Phase 5**: News & Content — `bespin-news-digest`, `twitter-timeline-to-slack` (parallel)
7. **Phase 6**: AI Research — `hf-trending-intelligence`, `paper-auto-classifier` (parallel)
8. **Phase 7**: Dev Intelligence — `github-sprint-digest`, `standup-digest` (parallel)
9. **Phase 8**: Consolidated Slack briefing to `#효정-할일`

### Execution

Read and follow the `daily-am-orchestrator` skill (`.cursor/skills/daily-am-orchestrator/SKILL.md`) for phase details, parallelism strategy, and error handling.

### Examples

Full weekday pipeline:
```
/daily-am
```

Weekend (skip market):
```
/daily-am --skip-market
```

Quick Google + Email only:
```
/daily-am --only-phase 2,3
```

Preview execution plan:
```
/daily-am --dry-run
```
