---
name: pm-sentinel
description: >-
  Autonomous PM loop that continuously researches, monitors, and improves the
  project using a YAML state DB and CLI validation gates. Wakes hourly via
  Cursor Automation, picks the next highest-priority mission, executes it
  with evidence-based completion (rejects "done" without proof), and outputs
  forced reminders to exploit LLM recency bias. Composes 12+ existing skills
  across 7 mission domains. Use when the user asks to "start sentinel",
  "pm sentinel", "autonomous loop", "continuous improvement", "무한 루프",
  "자율 PM", "sentinel status", "sentinel report", "seed missions",
  "heartbeat", or wants the project to improve itself without prompting.
  Do NOT use for single-task execution (invoke the specific skill directly),
  interactive debugging (use diagnose), or one-off code review (use simplify
  or deep-review). Korean triggers: "자율 PM", "무한 루프", "센티넬",
  "프로젝트 자동 개선", "하트비트".
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "orchestration"
---

# PM Sentinel — Autonomous Project Improvement Loop

An enterprise-grade autonomous PM system that uses YAML state DB + CLI validation gates to ensure AI agents continuously research, improve, and grow the project without human prompting. The CLI enforces evidence-based completion — the AI cannot claim a task is done without providing specific proof.

## Architecture

```
Trigger (hourly cron / manual)
    │
    ▼
CLI: pm-sentinel-cli.py
    │
    ├── Reads sentinel-state.yaml (YAML state DB)
    ├── Resolves next action (priority + dependency ordering)
    ├── Validates evidence (rejects incomplete/empty)
    ├── Updates state atomically
    └── Outputs reminder block (NEXT + WARN + 2 random tips)
         │
         ▼
    Agent executes mission phases using existing skills
         │
         ▼
    CLI validates evidence → updates state → next phase
```

## Prerequisites

- Python 3.10+ with PyYAML (`pip install pyyaml`)
- All files in `.cursor/sentinel/` directory
- Backend and frontend dev environment (for health scans)

## CLI Reference

All state mutations go through the CLI. Never edit `sentinel-state.yaml` directly.

```bash
CLI=".cursor/sentinel/pm-sentinel-cli.py"

# Status and navigation
python $CLI status              # Current state, active mission, next action
python $CLI next                # JSON descriptor of the next action to take
python $CLI tips                # Output reminder block only

# Mission lifecycle
python $CLI seed                # Populate all 7 mission types
python $CLI seed --types data-quality-patrol,project-health-scan
python $CLI add-mission <type> --priority 1
python $CLI start <mission-id>
python $CLI complete-phase <mission-id> <phase-id> --evidence '{"key":"value"}'
python $CLI complete <mission-id> --output <report-path>
python $CLI fail <mission-id> --reason "description"

# Control
python $CLI heartbeat           # Full cycle: increment counter, resolve next, output action
python $CLI pause               # Pause sentinel (no missions execute)
python $CLI resume              # Resume sentinel
python $CLI report              # Cycle summary and metrics
```

## Workflow

### Step 1: Initialize

On first run or when missions are empty:

```bash
python .cursor/sentinel/pm-sentinel-cli.py resume
python .cursor/sentinel/pm-sentinel-cli.py seed
```

This populates all 7 mission types with their phase blueprints from `mission-templates.yaml`.

### Step 2: Heartbeat Cycle

Each heartbeat (hourly via Cursor Automation or manual):

```bash
python .cursor/sentinel/pm-sentinel-cli.py heartbeat
```

The CLI returns a JSON action descriptor:

```json
{
  "action": "start_mission",
  "mission_id": "M-001",
  "mission_type": "data-quality-patrol",
  "priority": 1,
  "message": "Start mission M-001 (data-quality-patrol). Run: start M-001"
}
```

### Step 3: Execute Mission

Follow the action descriptor. For each mission:

1. **Start**: `python $CLI start M-001`
2. **Execute each phase** using the mapped skill:
   - Read the phase requirements from the CLI status output
   - Invoke the corresponding skill (e.g., `weekly-stock-update`, `deep-review`)
   - Collect evidence (file paths, metrics, counts)
3. **Complete each phase** with evidence:
   ```bash
   python $CLI complete-phase M-001 M-001-DQP-01 --evidence '{
     "total_tickers": 25,
     "stale_tickers": 3,
     "freshest_date": "2026-03-15",
     "oldest_date": "2026-03-10",
     "gap_count": 2
   }'
   ```
4. **Complete mission** when all phases pass:
   ```bash
   python $CLI complete M-001 --output "outputs/sentinel/data-quality-2026-03-15.md"
   ```

### Step 4: Handle Failures

If a phase or skill execution fails:

```bash
python $CLI fail M-001 --reason "Yahoo Finance API rate limited, backfill incomplete"
```

The CLI resets incomplete phases to `pending` and increments `error_count`. After `max_retries` (default 2), the mission is blocked.

### Step 5: Read Reminders

Every CLI output ends with a forced reminder block:

```
═══ SENTINEL REMINDER ═══
NEXT: Execute phase M-001-DQP-02: Validate data quality and consistency
WARN: No warnings
TIP1: Stock splits cause apparent price drops -- verify adjusted close prices.
TIP2: Run tests before marking any phase complete.
══════════════════════════
```

This exploits LLM recency bias — the most recent context in the window gets the strongest attention. Tips are randomized from phase-specific pools to prevent pattern recognition.

## Mission Types (7 Domains)

| Type | Skills Composed | Cadence | Priority |
|------|----------------|---------|----------|
| `project-health-scan` | deep-review, simplify, ci-quality-gate | 6h | 1 |
| `pipeline-optimizer` | today (dry-run), ai-quality-evaluator, performance-profiler | 12h | 2 |
| `skill-ecosystem-growth` | autoskill-evolve, skill-optimizer, workflow-miner | 24h | 3 |
| `data-quality-patrol` | weekly-stock-update, trading-data-quality-checker | 6h | 1 |
| `security-dependency-sweep` | security-expert, dependency-auditor, compliance-governance | 24h | 2 |
| `test-coverage-patrol` | test-suite, qa-test-expert, e2e-testing | 12h | 2 |
| `doc-freshness-checker` | context-engineer, technical-writer, codebase-archaeologist | 48h | 4 |

Each mission type has 4 phases with specific evidence requirements defined in `mission-templates.yaml`.

## Validation Gates

The CLI enforces these gates deterministically (not by LLM judgment):

1. **Evidence completeness** — Cannot complete a phase without all required evidence fields
2. **Evidence non-emptiness** — Cannot provide null/empty/[] for required fields
3. **Phase ordering** — Cannot complete a phase before its dependencies
4. **Mission ordering** — Cannot start a mission before its dependencies complete
5. **Single active mission** — Only one mission can be `in_progress` at a time
6. **Status transitions** — Only `pending` missions can be started
7. **Retry limits** — Missions with `error_count >= max_retries` are blocked

Each rejection includes an ERROR message and REMEDIATION instruction so the agent can self-correct.

## Files

| File | Purpose |
|------|---------|
| `.cursor/sentinel/pm-sentinel-cli.py` | CLI validation gate and state manager |
| `.cursor/sentinel/sentinel-state.yaml` | YAML state DB (missions, phases, evidence) |
| `.cursor/sentinel/mission-templates.yaml` | Phase blueprints for all 7 mission types |
| `.cursor/sentinel/sentinel-tips.yaml` | Phase-specific tip pools (30+ general, 15+ per domain) |
| `.cursor/sentinel/mission-log.yaml` | Completed mission history and metrics |

## Cursor Automation Setup (Hourly Heartbeat)

To run the sentinel autonomously every hour:

1. Go to **cursor.com/automations/new**
2. Configure:
   - **Name**: PM Sentinel Heartbeat
   - **Trigger**: Scheduled — `0 * * * *` (every hour)
   - **Tools**: Shell (read/write), Read File, Write File
   - **Memory**: Enabled (read/write)
3. Use this prompt:

```
You are the PM Sentinel for the ai-model-event-stock-analytics project.

## Goal
Execute one heartbeat cycle: determine the next mission, execute it with evidence, and report results.

## Procedure
1. Run: python .cursor/sentinel/pm-sentinel-cli.py heartbeat
2. Parse the JSON action descriptor from the output
3. If action is "start_mission": run `start <mission-id>`, then execute each phase
4. For each phase: invoke the mapped skill, collect evidence, run `complete-phase` with evidence JSON
5. If all phases complete: run `complete <mission-id> --output <path>`
6. If any step fails: run `fail <mission-id> --reason "<description>"`
7. Always read and follow the SENTINEL REMINDER at the end of each CLI output

## Rules
- NEVER mark a phase complete without actual evidence (file paths, metrics, counts)
- NEVER skip phases or reorder them
- NEVER edit sentinel-state.yaml directly — always use the CLI
- If the CLI rejects your action, read the REMEDIATION and fix the issue
- After completing a mission, run `seed` to replenish if no pending missions remain
```

## Constraints

- All state mutations MUST go through the CLI — never edit YAML directly
- Evidence must be specific and verifiable (file paths, numeric metrics, command outputs)
- One mission at a time — complete or fail the current one before starting another
- Tip pool randomization prevents LLM pattern recognition
- Mission outputs should be saved under `outputs/sentinel/` for traceability
