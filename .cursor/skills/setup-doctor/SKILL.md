---
name: setup-doctor
description: >-
  Scan system prerequisites, environment variables, CLI tools, Python/Node
  packages, and MCP servers required by all project skills, then produce a
  diagnostic pass/fail report and optionally install missing dependencies.
  Use when the user asks to "check setup", "setup doctor", "verify
  prerequisites", "install dependencies", "check environment", "what's
  missing", "설치 확인", "환경 점검", "의존성 확인", "셋업 닥터",
  or wants to validate that the system is ready to run specific skill groups.
  Do NOT use for creating new skills (use create-skill). Do NOT use for
  running the daily pipeline (use today). Do NOT use for individual tool
  setup guides (use gws-workspace, paperclip-setup, etc. directly).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "infrastructure"
---

# Setup Doctor

Diagnose and fix missing prerequisites across all project skill groups. Organizes checks by **capability group** (14 functional clusters) rather than 400+ individual skills.

## Input

The user provides:
1. **Mode** (optional) — parsed from `$ARGUMENTS`:
   - *(no args)* — Full scan of all capability groups
   - `--group <name>` — Check a single group (e.g., `--group slack`)
   - `--fix` — Auto-install missing items where safe (brew/pip/npm)
   - `--env` — Environment variable check only
   - `--report` — Generate a markdown report file at `outputs/setup-doctor-report.md`
   - `--slack` — Post the report to Slack `#효정-할일` after scanning

## Capability Groups

| Group | Key Prerequisites | Dependent Skills |
|-------|-------------------|------------------|
| core-platform | PostgreSQL, Redis, Python backend deps | today, daily-stock-check, tab-*, weekly-stock-update |
| llm-apis | OPENAI_API_KEY, ANTHROPIC_API_KEY | today, paper-review, alphaear-*, trading-* |
| slack | SLACK_BOT_TOKEN, plugin-slack-slack MCP | today, x-to-slack, eod-ship, morning-ship |
| notion | NOTION_TOKEN, plugin-notion-workspace-notion MCP | md-to-notion, notion-docs-sync, paper-archive |
| google-workspace | `gws` CLI, OAuth credentials | gws-*, calendar-daily-briefing, gmail-daily-triage |
| huggingface | `hf` CLI, HF_TOKEN | hf-cli, hf-jobs, hf-model-trainer |
| notebooklm | notebooklm-mcp MCP server | notebooklm, nlm-*, paper-review |
| twitter | TWITTER_COOKIE | x-to-slack, twitter-timeline-to-slack |
| browser | Playwright browsers installed | playwright-runner, e2e-testing, stock-csv-downloader |
| media | ffmpeg, yt-dlp | transcribee, video-compress |
| trading-apis | KIWOOM_APP_KEY, FRED_API_KEY, JINA_API_KEY | tab-kiwoom, today, alphaear-search |
| ci-cd | act, Docker, pre-commit, ruff | ci-quality-gate, domain-commit |
| github | `gh` CLI (authenticated) | github-workflow-automation, release-ship, ship |
| mirofish | `uv`, Node ≥18, MiroFish repo, LLM + Zep keys | mirofish, mirofish-financial-sim, mirofish-opinion-sim, mirofish-graph-explorer |

For full details on each group (install commands, env vars, verification), see [references/capability-map.md](references/capability-map.md).

For the complete env var registry, see [references/env-var-registry.md](references/env-var-registry.md).

## Workflow

### Phase 1: System Scan — CLI Tools

Check each tool via `command -v`:

```bash
for tool in gws hf gh act ffmpeg yt-dlp docker playwright pre-commit ruff uv rsync node python3 pip3 npm; do
  command -v "$tool" >/dev/null 2>&1 && echo "PASS $tool" || echo "FAIL $tool"
done
```

Record results in a table: `Tool | Status | Required By | Install Command`.

### Phase 2: Package Scan

**Python packages** — check critical packages via `pip show`:

```bash
for pkg in fastapi uvicorn sqlalchemy asyncpg alembic pandas numpy yfinance pykrx openai anthropic playwright feedparser huggingface-hub; do
  pip show "$pkg" >/dev/null 2>&1 && echo "PASS $pkg" || echo "FAIL $pkg"
done
```

**Node global packages** — check via `npm list -g --depth=0`:

```bash
npm list -g --depth=0 2>/dev/null | grep -q "@googleworkspace/cli" && echo "PASS gws" || echo "FAIL gws"
```

### Phase 3: Environment Scan

1. Check if `.env` file exists in project root
2. Parse `.env.example` for all variable names
3. For each variable in `.env.example`, check if it exists and is non-empty in `.env`
4. Also check skill-specific vars NOT in `.env.example`: `HF_TOKEN`, `NOTION_TOKEN`, `JINA_API_KEY`, `AA_API_KEY`, `MIROFISH_LLM_API_KEY`, `MIROFISH_ZEP_API_KEY`
5. Classify each as: SET (non-empty), EMPTY (exists but blank), MISSING (not in .env)

Present results grouped by capability group.

### Phase 4: MCP Scan

Check MCP server configs exist under the project's mcps directory:

```bash
MCP_DIR="$HOME/.cursor/projects/Users-hanhyojung-thaki-ai-model-event-stock-analytics/mcps"
for server in user-notebooklm-mcp plugin-notion-workspace-notion plugin-slack-slack cursor-ide-browser user-daiso-mcp user-public-apis; do
  [ -d "$MCP_DIR/$server" ] && echo "PASS $server" || echo "FAIL $server"
done
```

### Phase 5: Report and Fix

**Report format:**

```
Setup Doctor Report
====================
Date: YYYY-MM-DD

CLI Tools:        [N]/[T] passed
Python Packages:  [N]/[T] passed
Node Packages:    [N]/[T] passed
Environment Vars: [N]/[T] set
MCP Servers:      [N]/[T] configured

Capability Group Status:
  core-platform:     READY / PARTIAL / NOT READY
  llm-apis:          READY / PARTIAL / NOT READY
  slack:             READY / PARTIAL / NOT READY
  ...

Missing Items:
  [GROUP] [TYPE] [ITEM] — Install: [COMMAND]
```

**If `--fix` mode:**

For each missing CLI tool or package, run the install command from [references/capability-map.md](references/capability-map.md). Only install items with safe, non-destructive install commands (brew, pip, npm). Never auto-set env vars or credentials.

**If `--report` mode:**

Write the full report to `outputs/setup-doctor-report.md`.

**If `--group <name>` mode:**

Run phases 1-4 but filter results to only the specified capability group.

**If `--slack` mode (or combined with other modes):**

After generating the report, post it to Slack `#효정-할일` (channel ID: `C0AA8NT4T8T`) using the `plugin-slack-slack` MCP's `slack_send_message` tool.

Post as a 2-message thread:
1. **Main message**: Summary line with pass/fail counts and overall status
2. **Thread reply**: Full diagnostic report with capability group details and missing items

Main message format:
```
:stethoscope: *Setup Doctor Report* — YYYY-MM-DD

*Summary:* CLI [N]/[T] | Packages [N]/[T] | Env [N]/[T] | MCP [N]/[T]
*Status:* [N] READY, [N] PARTIAL, [N] NOT READY
```

Thread reply format: The full report with capability group breakdown and actionable fix commands for missing items.

## Examples

### Example 1: Full scan

User says: `/setup-doctor`

Output:
```
Setup Doctor Report
====================
Date: 2026-03-16

CLI Tools:        11/14 passed
Python Packages:  12/14 passed
Node Packages:    0/1 passed
Environment Vars: 8/15 set
MCP Servers:      5/6 configured

Capability Group Status:
  core-platform:     READY
  llm-apis:          READY
  slack:             READY
  notion:            PARTIAL (NOTION_TOKEN empty)
  google-workspace:  NOT READY (gws CLI not installed)
  huggingface:       NOT READY (hf CLI missing, HF_TOKEN missing)
  notebooklm:        READY
  twitter:           NOT READY (TWITTER_COOKIE missing)
  browser:           READY
  media:             PARTIAL (yt-dlp missing)
  trading-apis:      PARTIAL (JINA_API_KEY missing)
  ci-cd:             READY
  github:            READY
  mirofish:          PARTIAL (ZEP_API_KEY missing)

Missing Items:
  google-workspace  CLI   gws       — Install: npm install -g @googleworkspace/cli
  huggingface       CLI   hf        — Install: pip install huggingface-hub
  huggingface       ENV   HF_TOKEN  — Add to .env (get from https://huggingface.co/settings/tokens)
  media             CLI   yt-dlp    — Install: brew install yt-dlp
  twitter           ENV   TWITTER_COOKIE — Add to .env (extract from x.com browser cookies)
```

### Example 2: Check single group

User says: `/setup-doctor --group slack`

Output: Only Slack-related checks (SLACK_BOT_TOKEN, plugin-slack-slack MCP).

### Example 3: Auto-fix

User says: `/setup-doctor --fix`

Actions: Runs full scan, then installs missing CLI tools and packages. Skips env vars (reports them as manual action items).

## Error Handling

| Error | Action |
|-------|--------|
| `.env` file not found | Copy `.env.example` to `.env` and report all vars as MISSING |
| `pip`/`npm`/`brew` not available | Skip package checks for that manager, report as WARNING |
| MCP directory not found | Report all MCP servers as UNKNOWN, continue |
| `--fix` install command fails | Report the failure, continue with remaining items |
| Unknown `--group` name | List valid group names and abort |
