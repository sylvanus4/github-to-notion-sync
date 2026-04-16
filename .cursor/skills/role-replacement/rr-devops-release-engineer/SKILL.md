---
name: rr-devops-release-engineer
version: 1.0.0
description: >-
  Role Replacement Case Study: DevOps / Release Engineer — unified SOD + EOD lifecycle
  pipeline that replaces a dedicated release engineer by orchestrating start-of-day git
  sync, end-of-day multi-project shipping, N-repo cursor asset synchronization, domain-split
  commits, release-ship with GitHub Project #5 tracking, KB intelligence routing, session
  memory sync, and environment pre-flight diagnostics across 5 ThakiCloud repositories.
  Thin harness composing sod-ship, eod-ship, cursor-sync, release-ship, domain-commit,
  and kb-daily-router into a unified DevOps role pipeline with MemKraft-powered operational
  memory, pre-flight health checks, and automated Slack reporting.
tags: [role-replacement, harness, devops, release, git, multi-repo, shipping]
triggers:
  - rr-devops-release-engineer
  - devops engineer replacement
  - release engineer automation
  - multi-repo shipping pipeline
  - daily git lifecycle
  - SOD EOD pipeline
  - DevOps 역할 대체
  - 릴리즈 엔지니어 자동화
  - 멀티레포 배포 파이프라인
  - 일일 Git 라이프사이클
  - SOD EOD 파이프라인
do_not_use:
  - Pulling a single repo (use git directly)
  - Running Google daily only (use google-daily)
  - Individual release phase operations (use release-collector, release-qa-gate, or release-deployer)
  - Weekly release cycle management (use release-ops-orchestrator)
  - CI pipeline validation only (use ci-quality-gate)
  - Single-repo commit without multi-repo context (use domain-commit)
  - Cursor asset sync only without git lifecycle (use cursor-sync)
composes:
  - eod-ship
  - cursor-sync
  - sod-ship
  - release-ship
  - domain-commit
  - kb-daily-router
  - memkraft
  - ai-context-router
  - setup-doctor
---

# Role Replacement: DevOps / Release Engineer

## Human Role Being Replaced

A DevOps / Release Engineer who manually:
- Runs morning git sync across 5 repositories (commit dirty repos, push unpushed, pull remote, resolve conflicts)
- Performs end-of-day multi-project shipping (domain-split commits, push, create issues with GitHub Project fields, create PRs, merge)
- Synchronizes `.cursor/` assets (skills, commands, rules) across all repos via the research merge hub
- Manages environment pre-flight checks (CLI tools, MCP connectivity, env vars)
- Routes intelligence artifacts to Karpathy KB topics in the research repo
- Syncs session memory (transcript extraction, index rebuilding, attention decay)
- Handles repository-specific exceptions (ai-platform-webui tmp-only mode, dev branch merges)
- Posts consolidated shipping reports to Slack with threaded per-project details
- Verifies GitHub Project #5 registration and field completeness for all created issues/PRs
- Runs lat.md drift checks across repos with architecture knowledge graphs

This skill replaces 1-2 hours of daily manual DevOps work (30-45 min morning + 30-45 min evening).

## Architecture

```
Mode A: SOD (Start-of-Day) — invoked at 7:00 AM or machine switch
  Phase 0: MemKraft Context Pre-load
    └─ ai-context-router → repo states, conflict history, MCP status patterns
  Phase 1: Environment Pre-flight
    └─ sod-ship Phase 0 → CLI checks, MCP probes (13 servers), ATG gateway
  Phase 2: Git Sync (all 5 repos)
    └─ sod-ship Phases 1-4 → scan, commit, push, pull, dev merge, conflict resolution
  Phase 3: Post-Sync
    ├─ cursor-sync → N-repo .cursor/ asset propagation
    ├─ KB intel routing → research repo artifact routing
    └─ Skill guide sync + Canvas update
  Phase 4: Reporting
    ├─ Slack threaded report → #효정-할일
    └─ MemKraft write-back → operational patterns

Mode B: EOD (End-of-Day) — invoked at 5:00 PM or session end
  Phase 0: MemKraft Context Pre-load
    └─ ai-context-router → today's work, repo states, pending issues
  Phase 1: Asset Sync
    └─ cursor-sync → propagate today's .cursor/ changes
  Phase 2: Session Memory Sync
    └─ extract-sessions.py → build-index.py → attention_decay.py
  Phase 3: KB Intel Routing
    └─ kb_intel_router.py → route intelligence to KB topics
  Phase 4: Multi-Project Shipping (sequential, 6 repos)
    └─ release-ship per repo → domain-commit, push, issue, PR, merge
  Phase 5: Quality Gate
    └─ No secrets, clean repos, Project #5 verification, lat.md check
  Phase 6: Reporting
    ├─ Slack consolidated report → #효정-할일
    └─ MemKraft write-back → shipping patterns, conflict history

Mode C: SYNC-ONLY — cursor-sync without git operations
  └─ cursor-sync full N-repo cycle (pull + push)
```

## Execution

### Mode Selection

The skill auto-detects the appropriate mode based on invocation:

| Trigger | Mode | Time Context |
|---------|------|-------------|
| `/rr-devops-release-engineer --sod` | SOD | Morning / machine switch |
| `/rr-devops-release-engineer --eod` | EOD | Evening / session end |
| `/rr-devops-release-engineer --sync` | SYNC-ONLY | Anytime (cursor assets only) |
| `/rr-devops-release-engineer` (no flag) | Auto-detect | Before noon → SOD; after noon → EOD |

---

### Phase 0: MemKraft Context Pre-load (All Modes)

Before any git operations, load operational context from personal memory:

```
ai-context-router query:
  - "repository conflict history and resolution patterns"
  - "MCP server health patterns and recent disconnections"
  - "shipping patterns: which repos tend to have dirty state"
  - "GitHub Project #5 field setting issues and workarounds"
  - "cursor-sync recent conflicts and merge resolution history"
```

**MemKraft layers loaded:**
- **HOT**: Current repo states from last session, active branch per repo, pending push/pull status
- **WARM**: Conflict resolution history (last 30 days), MCP connectivity patterns, common shipping errors, repo activity frequency
- **Knowledge**: Project registry paths (office/home), cursor-sync skill group whitelists, repository-specific rules (tmp-only for webui), GitHub Project #5 field IDs and option mappings

Store loaded context as `ops_context` for all downstream phases.

---

### Mode A: SOD (Start-of-Day)

#### A1: Environment Pre-flight

Invoke `sod-ship` Phase 0 logic:

1. **CLI checks**: Verify `git`, `rsync`, `node`, `python3` on `$PATH`
2. **Env var checks**: `GITHUB_TOKEN`, `SLACK_USER_TOKEN`
3. **MCP connectivity probes**: Probe all 13 registered MCP servers in parallel batches (max 4 concurrent) using Task tool with `model: "fast"`
4. **ATG Gateway probe**: `curl -sf --max-time 3 http://localhost:4000/api/v1/health`

**MemKraft enhancement**: Compare current MCP connectivity against `ops_context.mcp_patterns`:
- If a previously stable server is now disconnected, flag as `regression` (higher severity)
- If a historically flaky server is disconnected, flag as `expected` (lower severity)

Build `preflight` map with `connected`, `disconnected`, `work_items`.

**Output**: `phase-a1-preflight.json`

#### A2: Git Sync (All 5 Repos)

Invoke `sod-ship` Phases 1-4 in sequence:

1. **Pre-flight scan**: Scan all 5 repos for dirty state, unpushed commits, behind commits
2. **Ship local changes**: For dirty repos, domain-commit + push (webui → `HEAD:tmp`, others → `HEAD`)
3. **Pull remote changes**: Fetch + pull for all repos (webui → `pull origin tmp`, others → standard pull)
4. **Dev merge** (webui only): `git merge origin/dev --no-edit` into current branch
5. **Verify sync**: Classify each repo as SYNCED / PARTIAL / FAILED / SKIPPED

**MemKraft enhancement**: During conflict resolution:
- Query `ops_context.conflict_history` for similar past conflicts and their resolution
- If the same file has conflicted 3+ times, flag for user attention with pattern note

**Path resolution**: Each project has two candidate paths (`Path (회사)` and `Path (집)`). Try office path first, fall back to home path. Per `eod-ship` and `sod-ship` project-registry.md.

**Output**: `phase-a2-git-sync.json` with per-repo status

#### A3: Post-Sync

After git sync completes, run three parallel post-sync operations:

##### A3a: Cursor Sync

Invoke `cursor-sync` skill:
1. **Pull Phase**: `rsync -au` from 4 target repos → research (newest wins)
2. **Push Phase**: `rsync -ac` from research → 4 target repos (checksum-based, group-filtered)
3. **Verify**: All 5 repos have consistent file counts

##### A3b: KB Intelligence Routing

Route intelligence artifacts from research repo:

```bash
RESEARCH_REPO="${RESEARCH_REPO:-$HOME/thaki/research}"
if [ -d "$RESEARCH_REPO" ] && [ -f "$RESEARCH_REPO/scripts/intelligence/kb_intel_router.py" ]; then
    python3 "$RESEARCH_REPO/scripts/intelligence/kb_intel_router.py"
fi
```

If new artifacts routed, commit and push KB changes.

##### A3c: Skill Guide Sync + lat.md Check

1. Run `skill-guide-generator` in `--readme-only` mode
2. For repos with `lat.md/` directory, run `lat check` (non-blocking)

**Output**: `phase-a3-post-sync.json`

#### A4: Reporting

1. **Slack**: Post consolidated SOD report to `#효정-할일` with threaded per-project details (per `sod-ship` Phase 5 template)
2. **Canvas**: Append dated digest to canvas `F0AN2C7UKCY`
3. **Chat**: Display formatted Korean report

---

### Mode B: EOD (End-of-Day)

#### B1: Asset Sync

Invoke `cursor-sync` to propagate today's `.cursor/` changes before shipping:
1. Pull Phase: absorb any changes made in other repos during the day
2. Push Phase: distribute merged assets to all targets

**Output**: `phase-b1-cursor-sync.json`

#### B2: Session Memory Sync

Sync agent session memory before shipping:

```bash
cd /Users/hanhyojung/work/thakicloud/ai-model-event-stock-analytics

python scripts/memory/extract-sessions.py --incremental
python scripts/memory/build-index.py --skip-embeddings

POINTER_COUNT=$(grep -c '^\- \[' MEMORY.md 2>/dev/null || echo 0)
if [ "$POINTER_COUNT" -gt 50 ]; then
    python scripts/memory/attention_decay.py --apply
fi
```

**Output**: `phase-b2-memory-sync.json`

#### B3: KB Intelligence Routing

Route accumulated intelligence artifacts to Karpathy KB topics (same as A3b).

**Output**: `phase-b3-kb-routing.json`

#### B4: Multi-Project Shipping

Invoke `eod-ship` Phases 2-3 logic for 6 projects (current + 5 managed):

**Execution order** (from project-registry.md):
1. Current project (ai-model-event-stock-analytics)
2. github-to-notion-sync
3. ai-template
4. ai-model-event-stock-analytics (if not current)
5. research
6. ai-platform-webui (tmp-only mode: commit → push → issue → report, no PR/merge)

For each project with dirty state:
1. `domain-commit` → domain-split commits by directory prefix
2. `git push` → webui to `HEAD:tmp`, others to `HEAD`
3. `release-ship` Step 4 → Create issues from commits, add to Project #5, set all 5 fields
4. `release-ship` Steps 5-6 → Create/update PR, squash-merge (skip for webui)

**Pipeline mode**: No confirmation prompts. Issues, PRs, and merges execute automatically.

**MemKraft enhancement**: Use `ops_context.shipping_patterns` to:
- Predict which repos will have changes (skip unnecessary scans for historically clean repos)
- Pre-populate issue priority based on domain (e.g., `scripts/` changes → P2, `backend/` → P1)

**Output**: `phase-b4-shipping.json` with per-repo results

#### B5: Quality Gate

Pre-Slack verification (from `eod-ship` Phase 3½):

- [ ] No `.env`, credentials, or secrets committed
- [ ] All shipped repos have clean `git status`
- [ ] No orphaned untracked content files
- [ ] Branch consistency (webui → tmp, others → standard)
- [ ] Issue field completeness: ALL 5 fields set for every issue on Project #5
- [ ] GitHub Project #5 registration verified for all issues and PRs
- [ ] lat.md drift check for repos with knowledge graphs

**Output**: `phase-b5-quality-gate.json`

#### B6: Reporting

1. **Slack**: Post consolidated EOD report to `#효정-할일` (per `eod-ship` Phase 4 template)
2. **Chat**: Display formatted Korean report
3. **MemKraft write-back**: Update operational memory

---

### Mode C: SYNC-ONLY

Invoke `cursor-sync` full N-repo cycle:
1. Pull Phase from 4 targets → research
2. Push Phase from research → 4 targets
3. Verify file counts
4. Report results

No git operations, no shipping, no Slack posting.

---

## MemKraft Write-back (Modes A & B)

After all phases complete, update operational memory:

```
memkraft-ingest entries:
  - topic: "devops-session-summary"
    content: "Mode {A|B} on {date}. Repos: {synced}/{total} SYNCED. Commits: {created} created, {received} received. Issues: {count}. Conflicts: {conflict_repos}."
    tier: WARM
    provenance: rr-devops-release-engineer

  - topic: "conflict-history-update"
    content: "{repo}: {file} conflict resolved via {method}. Pattern: {description}."
    tier: WARM
    provenance: rr-devops-release-engineer

  - topic: "mcp-health-pattern"
    content: "MCP connectivity: {connected}/{total}. Regressions: {regressed_servers}. Stable disconnects: {known_disconnects}."
    tier: WARM
    provenance: rr-devops-release-engineer
```

## Channel Routing

| Destination | Channel ID | Content |
|------------|------------|---------|
| `#효정-할일` | `C0AA8NT4T8T` | SOD/EOD consolidated reports, threaded per-project details |

## Output Protocol (File-First)

```
outputs/rr-devops-release-engineer/{date}/
├── manifest.json                          # Pipeline run status (mode, phases, timing)
├── phase-0-memkraft-context.json          # Loaded ops context summary
├── phase-a1-preflight.json                # SOD: environment diagnostics
├── phase-a2-git-sync.json                 # SOD: per-repo sync status
├── phase-a3-post-sync.json                # SOD: cursor-sync, KB routing, skill guide
├── phase-b1-cursor-sync.json              # EOD: asset sync results
├── phase-b2-memory-sync.json              # EOD: session memory sync results
├── phase-b3-kb-routing.json               # EOD: KB intel routing results
├── phase-b4-shipping.json                 # EOD: per-repo shipping results
├── phase-b5-quality-gate.json             # EOD: quality gate pass/fail
└── phase-final-memkraft-writeback.json    # MemKraft entries written
```

## Prerequisites

| Requirement | Check | Recovery |
|------------|-------|----------|
| `git` CLI | `which git` | Install via Homebrew |
| `rsync` CLI | `which rsync` | Built-in on macOS |
| `gh` CLI authenticated | `gh auth status` | `gh auth login` |
| `python3` | `which python3` | Install via Homebrew |
| `GITHUB_TOKEN` env var | `test -n "$GITHUB_TOKEN"` | Set in `.env` or shell profile |
| Slack MCP available | Test `slack_send_message` | Check `.env` SLACK tokens |
| Project registry accessible | `ls .cursor/skills/pipeline/eod-ship/references/project-registry.md` | Verify eod-ship skill installed |
| Memory scripts exist | `ls scripts/memory/extract-sessions.py` | Check repo integrity |

## Memory Configuration

```yaml
memkraft:
  tiers:
    HOT:
      - current repo states (branch, dirty, unpushed per repo)
      - active conflict resolutions in progress
      - today's shipping results (issues created, PRs merged)
    WARM:
      - conflict resolution history (last 30 days, per repo + file)
      - MCP server connectivity patterns (uptime %, regression detection)
      - repo activity frequency (which repos are typically dirty at SOD/EOD)
      - shipping error patterns (common failures and their fixes)
      - cursor-sync merge conflict history
    Knowledge:
      - project registry (5 repos, office/home paths, modes)
      - cursor-sync skill group whitelists per target repo
      - GitHub Project #5 field IDs and option mappings
      - repository-specific rules (webui tmp-only, dev merge protocol)
      - domain-commit path-to-type mapping

  provenance_tag: rr-devops-release-engineer
  dream_cycle_hook: "analyze weekly conflict patterns and shipping failure trends for process improvements"
```

## Slack Integration

| Destination | Channel ID | Content |
|------------|------------|---------|
| `#효정-할일` | `C0AA8NT4T8T` | SOD/EOD reports + threaded details |

## Error Recovery

| Phase | Failure | Recovery |
|-------|---------|----------|
| Phase 0 | MemKraft unavailable | Proceed with default ops rules (no personalization) |
| A1 | MCP probe timeout | Classify as DISCONNECTED; non-blocking |
| A1 | ATG gateway down | Non-blocking (optional accelerator) |
| A2 | Single repo pull conflict | Attempt rebase; if fails, abort and mark PARTIAL; continue with others |
| A2 | Push rejected (diverged) | Defer push, pull first, retry; if still fails, mark FAILED |
| A2 | Dev merge conflict (webui) | Auto-resolve simple (--theirs); complex → abort, report files |
| A3a | cursor-sync rsync failure | Warn and continue; git sync results unaffected |
| A3b | KB router script missing | Skip KB routing (research repo may not exist on this machine) |
| B2 | Memory script failure | Warn and continue; memory sync is optional |
| B3 | KB routing failure | Warn and continue; non-critical |
| B4 | release-ship fails on one repo | Log error, continue with remaining repos |
| B4 | Pre-commit hook failure | Fix lint, re-stage, new commit (never amend) |
| B4 | Issue creation fails | Log error, continue with PR creation |
| B4 | Project #5 field set fails | Retry once; if fails, log and continue |
| B4 | PR merge fails | Try `--admin`; if fails, report PR URL |
| B5 | Secrets detected in staged files | BLOCK shipping for that repo; alert user |
| B6 | Slack rate limit | Wait 20s, retry; if persistent, queue |
| B6 | Slack message fails | Still display chat report |
| C | cursor-sync target missing | Skip target; sync remaining |

## Security & Compliance

- Never force push (`--force`) to any branch in any project
- Never push directly to `main` or `dev`
- Never amend failed commits; create new ones
- Never commit `.env`, credentials, or secret files
- ai-platform-webui: Never create PRs or merge — tmp-only mode
- Always return to original working directory after each project
- `GITHUB_TOKEN`, `SLACK_TOKEN` never logged in output files
- GitHub Project #5 field values use option IDs, not raw values (tamper-resistant)

## Honest Reporting

- Report outcomes faithfully — never claim all phases passed when any failed
- Never suppress errors, partial results, or skipped phases
- Surface unexpected findings even if they complicate the narrative
- If a phase produces no actionable output, say so explicitly

## Coordinator Synthesis

- Do not reconstruct phase outputs from chat context — always read from persisted files
- Each phase dispatch includes a purpose statement explaining the expected transformation
- File paths and line numbers must be specific, not inferred
- Never delegate with vague instructions like "analyze this" — provide concrete specs

## Examples

**Standard SOD dispatch:**
User: "rr-devops-release-engineer" or "SOD EOD 파이프라인"
→ Auto-detects morning, runs SOD pipeline (git pull 5 repos → cursor-sync → pre-flight), posts summary to Slack

**EOD with uncommitted changes:**
User: "rr-devops-release-engineer" at 5PM with dirty working directories
→ Runs domain-commit per repo, release-ship, cursor-sync, KB routing, MemKraft write-back

## Operational Runbook

### Morning Start (SOD)

```
/rr-devops-release-engineer --sod
```

Or as part of `daily-am-orchestrator` Phase 1 (git sync track).

### Evening Wrap-up (EOD)

```
/rr-devops-release-engineer --eod
```

Or as part of `daily-pm-orchestrator` Phase 3 (code shipping track).

### Cursor Asset Sync Only

```
/rr-devops-release-engineer --sync
```

Quick sync without git operations. Useful after editing skills in one repo.

### Machine Switch (Full Bidirectional Sync)

```
/rr-devops-release-engineer --sod --skip-doctor
```

Skips MCP diagnostics for faster sync when switching machines.

### Dry Run (Preview Only)

```
/rr-devops-release-engineer --sod --dry-run
/rr-devops-release-engineer --eod --dry-run
```

Shows what would be committed/pushed/pulled without executing. No Slack posting.

### Ship Specific Repos Only

```
/rr-devops-release-engineer --eod --targets research,ai-template
```

Limits shipping to specified repos. Cursor-sync still runs for all.

## Comparison: Human DevOps/Release Engineer vs. rr-devops-release-engineer

| Dimension | Human Engineer | rr-devops-release-engineer |
|-----------|---------------|---------------------------|
| Morning sync time | 30-45 min (manual per repo) | 5-10 min (automated parallel scan) |
| Evening ship time | 30-45 min (manual commits, PRs) | 10-15 min (automated pipeline mode) |
| Repos managed | 2-3 (attention limit) | 5+ (sequential, no fatigue) |
| Domain-split commits | Often skipped (single commit) | Enforced (domain-commit pattern) |
| Issue tracking | Often forgotten | Mandatory (Project #5, all 5 fields) |
| Conflict resolution | Manual, context-dependent | MemKraft-enhanced (historical patterns) |
| Asset sync | Manual rsync / copy-paste | N-repo bidirectional (cursor-sync) |
| Pre-flight checks | Rarely done (skip to work) | Automated (13 MCP probes, CLI, env) |
| Memory sync | Never (context lost) | Automated (transcript extraction, indexing) |
| KB routing | Manual file moves | Automated (kb_intel_router.py) |
| Reporting | Often skipped | Automated Slack + Canvas + Chat |
| Consistency | Varies by fatigue/day | Enforced (quality gates, safety rules) |
| Cost | $80K-120K/year FTE partial | ~$3-5/day in compute costs |

## Subagent Contract

When spawning Task tool subagents for MCP probes or parallel operations:

- Pass **absolute file paths** for all input/output locations
- Require return: `{ "status": "completed|failed|skipped", "file": "<phase-output-path>", "summary": "<one-line>" }`
- Include purpose: "You are a DevOps subagent for the daily git lifecycle pipeline"
- Use `model: "fast"` for MCP probe subagents and read-only scan subagents
- Phase A2/B4 git operations MUST run in main context (not subagents) to prevent concurrent git conflicts
