## Daily PM — Evening Pipeline

Run the full evening automation pipeline: knowledge consolidation, strategic analysis, code shipping, skill evolution, weekly reports (Friday only), and a consolidated EOD Slack briefing. Orchestrates 8+ skills across 5 parallel phases.

### Usage

```
# Full evening pipeline (all phases)
/daily-pm

# Skip specific phases
/daily-pm --skip-phase 2           # skip Strategic Analysis
/daily-pm --skip-phase 4           # skip Skill Evolution

# Run only specific phases
/daily-pm --only-phase 3           # Code Shipping only

# Convenience shortcuts
/daily-pm --skip-strategy          # skip daily-strategy-post
/daily-pm --skip-skills            # skip skill evolution

# Friday overrides
/daily-pm --friday                 # force weekly reports (any day)

# Output control
/daily-pm --no-slack               # suppress all Slack posts
/daily-pm --dry-run                # preview plan, no execution
```

### Workflow

1. **Phase 1**: Knowledge Consolidation — `knowledge-daily-aggregator` → Cognee + MEMORY.md
2. **Phase 2**: Strategic Analysis — `daily-strategy-post` multi-role analysis (after Phase 1)
3. **Phase 3**: Code Shipping — `eod-ship` cursor-sync + release-ship all projects (parallel)
4. **Phase 4**: Skill Evolution — `autoskill-evolve` + `skill-guide-generator` (parallel)
5. **Phase 5**: Weekly Reports — `weekly-status-report` + `portfolio-report-generator` (Friday only, parallel)
6. **Phase 6**: Consolidated EOD Slack briefing to `#효정-할일`

### Execution

Read and follow the `daily-pm-orchestrator` skill (`.cursor/skills/daily-pm-orchestrator/SKILL.md`) for phase details, Friday-conditional logic, and error handling.

### Examples

Full weekday pipeline:
```
/daily-pm
```

Full Friday pipeline (includes weekly reports):
```
/daily-pm
```

Force weekly reports mid-week:
```
/daily-pm --friday
```

Ship code only:
```
/daily-pm --only-phase 3
```

Preview execution plan:
```
/daily-pm --dry-run
```
