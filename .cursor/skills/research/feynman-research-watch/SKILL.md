---
name: feynman-research-watch
description: "Set up a recurring research watch on a topic, company, paper area, or product surface. Creates a baseline survey and configures recurring monitoring via Cursor Automations or manual re-invocation. Use when the user asks to 'monitor a field', 'track new papers', 'watch for updates', 'set up research alerts', 'recurring research', 'topic monitoring', '연구 모니터링', '논문 추적', '토픽 워치', '연구 알림', '주기적 리서치', 'feynman-research-watch', '/watch', 'research watch'. Do NOT use for one-time deep research (use parallel-deep-research). Do NOT use for HuggingFace trending scan (use hf-trending-intelligence or hf-topic-radar). Do NOT use for paper auto-classification (use paper-auto-classifier). Do NOT use for daily stock monitoring (use today pipeline)."
---

# Research Watch

Set up a recurring research watch that establishes a baseline survey of a topic, defines change signals, and configures periodic re-checks to surface new developments.

## Prerequisites

- The user provides a research topic, company, paper area, or product surface to monitor.
- Optional: check frequency (daily, weekly, biweekly — default: weekly).

## Workflow

### Phase 1: Plan

1. Derive a short slug from the watch topic.
2. Outline the watch plan:
   - **What to monitor**: specific topic, keywords, authors, venues, repos
   - **Signals that matter**: new papers, benchmark improvements, tool releases, API changes, funding rounds
   - **Change threshold**: what counts as a meaningful update worth reporting
   - **Check frequency**: how often to re-check (default: weekly)
   - **Delivery**: where to post updates (Slack channel, file, Notion)
3. Save to `outputs/feynman/<slug>-watch-plan.md`.
4. Present to the user and **wait for confirmation**.

### Phase 2: Baseline Survey

Spawn a `generalPurpose` subagent:

```
You are a research survey agent. Your task:

1. Conduct a comprehensive baseline survey of: <topic>
2. Search using multiple strategies:
   - WebSearch for recent developments, blog posts, product announcements
   - alphaxiv-paper-lookup or alpha CLI for academic papers
   - HuggingFace MCP for models, datasets, spaces (if applicable)
   - GitHub for repositories and tools
3. Build a baseline snapshot:

## Baseline: <topic> (as of <date>)

### Key Players
| Entity | Role | Latest Activity | URL |
|--------|------|----------------|-----|

### Recent Papers (last 6 months)
| Paper | Date | Key Contribution | arXiv ID |
|-------|------|-----------------|----------|

### Tools & Repos
| Tool | Stars | Last Updated | URL |
|------|-------|-------------|-----|

### Current State of the Art
- Best benchmark results
- Dominant approaches
- Open problems

### Signals to Watch
- Upcoming conferences/deadlines
- Active research groups
- Trending keywords

4. Save to `outputs/feynman/<slug>-baseline.md`
```

### Phase 3: Monitoring Configuration

Set up the recurring check. Two options depending on user's setup:

**Option A: Cursor Automations (recommended)**

Guide the user to create a Cursor Automation:
```
Trigger: Schedule (cron: based on user's chosen frequency)
Prompt: "Run feynman-research-watch update for '<topic>'. 
Read the baseline at outputs/feynman/<slug>-baseline.md, 
search for new developments since <last_check_date>, 
and post a delta report to Slack #deep-research-trending."
```

**Option B: Manual re-invocation**

Create a re-check prompt template at `outputs/feynman/<slug>-recheck-prompt.md`:
```markdown
## Research Watch Re-check: <topic>

Run this prompt periodically to check for updates:

"Check for new developments in '<topic>' since <last_check_date>.
Read the baseline at outputs/feynman/<slug>-baseline.md.
Search for new papers, tools, benchmarks, and announcements.
Compare against baseline and report only NEW items.
Update the baseline file with new entries.
Post significant findings to Slack #deep-research-trending."
```

### Phase 4: Delta Report Format

Each recurring check produces a delta report:

```markdown
## Research Watch Update: <topic>
**Period**: <last_check> → <current_date>

### New Developments
🆕 **New Papers**
- [Paper Title](url) — Key finding...

🛠️ **New Tools/Repos**
- [Tool Name](url) — What it does...

📊 **Benchmark Changes**
- Model X now achieves Y on Z benchmark (previously: ...)

⚡ **Breaking Changes**
- API V2 released, deprecates V1

### No Change
- Areas with no significant updates since last check

### Baseline Updated
- Added N new entries to baseline file
```

### Phase 5: Delivery

1. Present the baseline survey to the user
2. Confirm monitoring setup (Automations or manual)
3. Post the baseline summary to the configured Slack channel if requested

## Output Structure

```
outputs/feynman/
├── <slug>-watch-plan.md        # Phase 1 plan
├── <slug>-baseline.md          # Phase 2 baseline (updated on each check)
├── <slug>-recheck-prompt.md    # Phase 3 re-check template
└── <slug>-delta-<date>.md      # Phase 4 delta reports (one per check)
```

## Integration Points

- **Slack**: Post updates to #deep-research-trending or user-specified channel
- **paper-auto-classifier**: Route discovered papers through auto-classification
- **paper-archive**: Archive significant papers found during watches
- **hf-topic-radar**: Complement with HuggingFace-specific trending data

## Verification Before Completion

- [ ] Baseline survey covers key players, papers, tools, and SOTA
- [ ] Watch plan defines clear change signals and thresholds
- [ ] Monitoring method is configured (Automations or manual template)
- [ ] Delivery channel confirmed with user
- [ ] Output files exist at documented paths
