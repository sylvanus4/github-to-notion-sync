---
name: pipeline-builder
description: >-
  Build and manage automated data pipelines using existing Python scripts,
  GitHub Actions, and cron schedules without writing new code. Generates YAML
  pipeline definitions, GitHub Actions workflows, script chains, and Makefile
  targets for the stock analytics project. Use when the user asks to "build a
  pipeline", "automate this process", "create a GitHub Action", "chain these
  scripts", "schedule this task", "파이프라인 빌드", "자동화", "스크립트 체인", "GitHub
  Actions 워크플로우 생성", or wants to compose existing scripts into repeatable
  automated pipelines. Do NOT use for designing AI-powered analysis workflows
  (use ai-workflow-integrator). Do NOT use for running the existing daily
  pipeline (use today). Do NOT use for CI/CD pipeline review (use
  sre-devops-expert). Do NOT use for deployment or infrastructure (use
  sre-devops-expert).
disable-model-invocation: true
---

# Pipeline Builder

Build automated data pipelines by composing existing Python scripts, Makefile targets, and GitHub Actions workflows. No new code required -- pipelines are defined as YAML configurations or shell script chains.

## Meta-Orchestration

### Prompt router (representative user phrases)

| # | Example prompt | This skill? | Delegation order (numbered) | Output merge strategy | User overrides |
|---|----------------|-------------|------------------------------|------------------------|----------------|
| 1 | AI 리포트 품질을 자동 평가해줘 | No | 1) `ai-quality-evaluator` (not a GHA/Makefile concern unless user asks) | — | — |
| 2 | 데일리 파이프라인을 설계해줘 | Partial | If **runtime** automation: 1) `ai-workflow-integrator` for stage logic → 2) this skill to emit workflow/Makefile/shell | Artifact bundle: YAML + optional Makefile target + inventory entry | `RUNNER=github|local`; cron expr; secrets list |
| 3 | 이 프로세스를 자동화할지 결정해줘 | No | 1) `automation-strategist` → 2) this skill for implementation | Decision + generated config files | — |
| 4 | 시스템 데이터 흐름을 분석해줘 | No | 1) `system-thinker` → 2) this skill only to materialize scheduled automation | Map + pipeline file | — |
| 5 | 프로젝트 컨텍스트를 업데이트해줘 | No | 1) `context-engineer` | — | — |

### Error recovery (pipeline construction)

| Failure mode | Retry | Fallback | Abort |
|--------------|-------|----------|-------|
| Template conflict with existing workflow | — | Diff against `daily-today.yml`; extend don’t duplicate | — |
| Secret missing | — | Stub with `secrets.*`; list required keys for user | Cannot deploy until user confirms |
| Stage flaky | — | `continue-on-error` + notification; or retry loop in shell | User sets policy |

### Output aggregation

Ship **one** pipeline definition plus **inventory markdown block** (trigger, stages, secrets, duration). If multiple formats (GHA + Makefile), list execution order: prefer CI for schedule, Makefile for local.

## Available Scripts

These are the building blocks for pipelines:

| Script | Path | Purpose | Key Args |
|--------|------|---------|----------|
| Weekly stock update | `backend/scripts/weekly_stock_update.py` | Fetch prices from Yahoo Finance | `--status`, `--days N`, `--ticker T` |
| CSV import | `backend/scripts/import_csv.py` | Import CSV files into DB | `PATH --directory` |
| Daily stock check | `backend/scripts/daily_stock_check.py` | Run technical analysis | `--source db`, `--dir DIR`, `--tickers T` |
| Hot stock discovery | `backend/scripts/discover_hot_stocks.py` | Find trending untracked stocks | (none) |
| Report generator | `outputs/scripts/generate-report.js` | Generate .docx report | `{date}` |

## Existing Pipelines

Review these before creating new ones to avoid duplication:

| Pipeline | Location | Trigger | Stages |
|----------|----------|---------|--------|
| Daily today | `.github/workflows/daily-today.yml` | Cron 09:00 KST | Migrate → Seed → CSV import → Yahoo sync → Analysis → Report → Slack |
| Makefile dev | `Makefile` | Manual | Install → DB up → Backend → Frontend |

## Workflow

### Step 1: Define Pipeline Requirements

Ask or infer:

1. **What does it do?** (data sync, analysis, reporting, alerting)
2. **What triggers it?** (cron schedule, manual, webhook, file change)
3. **Which scripts does it chain?** (from the Available Scripts table)
4. **Where does it run?** (local, GitHub Actions, both)
5. **What are the outputs?** (DB records, files, Slack messages, logs)

### Step 2: Choose Pipeline Format

| Format | Best For | Location |
|--------|----------|----------|
| **GitHub Actions workflow** | Scheduled/automated pipelines | `.github/workflows/` |
| **Makefile target** | Local developer pipelines | `Makefile` |
| **Shell script** | Complex local pipelines with logic | `scripts/` |
| **Cursor command** | Interactive pipelines via agent | `.cursor/commands/` |

### Step 3: Build the Pipeline

#### Format A: GitHub Actions Workflow

Generate a workflow YAML following the project's existing pattern from `.github/workflows/daily-today.yml`:

```yaml
name: Pipeline Name
on:
  schedule:
    - cron: '0 0 * * 1-5'  # weekdays at UTC midnight
  workflow_dispatch:         # manual trigger

env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}

jobs:
  pipeline:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r backend/requirements.txt
      - name: Stage 1 - Description
        run: cd backend && python scripts/script_name.py --args
      - name: Stage 2 - Description
        run: cd backend && python scripts/script_name.py --args
```

Key rules:
- Use `secrets` for DATABASE_URL, API keys -- never hardcode
- Add `continue-on-error: true` for non-critical stages
- Use `if: success()` for conditional stages
- Set `timeout-minutes` for long-running stages

#### Format B: Makefile Target

Add targets following existing Makefile patterns:

```makefile
.PHONY: pipeline-name
pipeline-name: ## Description of what the pipeline does
	cd backend && python scripts/stage1.py --args
	cd backend && python scripts/stage2.py --args
	@echo "Pipeline complete"
```

Key rules:
- Add `.PHONY` declaration
- Include `## comment` for `make help` display
- Use `@` prefix for echo commands
- Chain with `&&` for fail-fast or `;` for continue-on-error

#### Format C: Shell Script

Create a shell script with error handling:

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATE=$(date +%Y-%m-%d)

echo "=== Stage 1: Description ==="
cd "$SCRIPT_DIR/../backend"
python scripts/stage1.py --args || { echo "Stage 1 failed"; exit 1; }

echo "=== Stage 2: Description ==="
python scripts/stage2.py --args || echo "Stage 2 failed (non-critical), continuing..."

echo "=== Pipeline complete ==="
```

#### Format D: Cursor Command

Create a command markdown that references skills and scripts:

```markdown
## Pipeline Name

### Workflow
1. Run script X with args Y
2. Use skill Z for analysis
3. Post results to Slack

### Execution
Read and follow [skill-name] skill for detailed instructions.
```

### Step 4: Add Error Handling

For each stage, define failure behavior:

| Stage Criticality | Behavior | Implementation |
|-------------------|----------|----------------|
| Critical | Abort pipeline | `set -e` / no `continue-on-error` |
| Important | Retry then skip | `for i in 1 2 3; do cmd && break; done` |
| Optional | Log and continue | `cmd \|\| echo "skipped"` / `continue-on-error: true` |

### Step 5: Add Notifications

For GitHub Actions pipelines, add Slack notification on completion:

```yaml
- name: Notify Slack
  if: always()
  uses: slackapi/slack-github-action@v2
  with:
    webhook: ${{ secrets.SLACK_WEBHOOK }}
    payload: |
      {"text": "Pipeline ${{ job.status }}: ${{ github.workflow }}"}
```

For local pipelines, suggest using the Slack MCP tool via a Cursor command.

### Step 6: Validate Pipeline

Before finalizing:

1. **Dry run**: Execute each stage individually to verify it works
2. **Dependency check**: Ensure all required scripts exist and dependencies are installed
3. **Secret check**: Verify no credentials are hardcoded
4. **Idempotency**: Confirm the pipeline can be re-run safely (upserts, not inserts)

### Step 7: Document the Pipeline

Add to the project's pipeline inventory:

```markdown
### [Pipeline Name]
- **Trigger**: cron / manual / event
- **Location**: .github/workflows/ or Makefile or scripts/
- **Stages**: [ordered list]
- **Secrets required**: [list]
- **Estimated duration**: [time]
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| GitHub Actions workflow fails | Missing secrets | Add required secrets in repo Settings > Secrets |
| Makefile target not found | Missing `.PHONY` declaration | Add `.PHONY: target-name` before the target |
| Shell script permission denied | Not executable | Run `chmod +x scripts/pipeline-name.sh` |
| Script dependency not found | Virtual env not activated | Add `source .venv/bin/activate` or install deps in the step |
| Duplicate pipeline | Similar workflow already exists | Check existing pipelines table before creating |
| Cron not triggering | Wrong timezone or syntax | Use [crontab.guru](https://crontab.guru) to verify; GitHub Actions uses UTC |

## Examples

### Example 1: Weekly data refresh pipeline

User says: "Create a GitHub Actions workflow that refreshes all stock data every Monday"

Actions:
1. Generate `.github/workflows/weekly-refresh.yml`
2. Stages: Yahoo Finance sync (7 days) → CSV import → Status check
3. Cron: `0 1 * * 1` (Monday 01:00 UTC)
4. Add Slack notification on completion

### Example 2: Local analysis pipeline

User says: "Add a Makefile target that runs analysis and generates the report"

Actions:
1. Add `analysis-report` target to `Makefile`
2. Stages: `daily_stock_check.py --source db` → `generate-report.js`
3. Output: `outputs/reports/daily-{date}.docx`

### Example 3: Multi-stage data pipeline

User says: "Chain CSV download, import, and analysis into one script"

Actions:
1. Create `scripts/full-pipeline.sh`
2. Stages: CSV download → Import → Yahoo sync → Analysis
3. Error handling: Abort on import failure, continue on Yahoo timeout

## Integration

- **Existing workflows**: `.github/workflows/daily-today.yml`, `.github/workflows/ci.yml`
- **Makefile**: `Makefile` (install, dev, test, lint targets)
- **Scripts**: `backend/scripts/` directory
- **Related skills**: `ai-workflow-integrator` (AI-level design), `today` (existing daily pipeline), `sre-devops-expert` (infrastructure review)
