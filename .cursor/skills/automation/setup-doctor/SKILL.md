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
  version: "3.1.0"
  category: "infrastructure"
---

# Setup Doctor

Diagnose and fix missing prerequisites across all project skill groups. Organizes checks by **capability group** (40 functional clusters) rather than 400+ individual skills.

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
| notion | NOTION_TOKEN (primary, in `.env`), plugin-notion-workspace-notion MCP (fallback) | md-to-notion, notion-docs-sync, paper-archive, paper-review, meeting-digest, md-enhance-publish |
| google-workspace | `gws` CLI, OAuth credentials | gws-*, calendar-daily-briefing, gmail-daily-triage |
| huggingface | `hf` CLI, HF_TOKEN | hf-cli, hf-jobs, hf-model-trainer |
| notebooklm | notebooklm-mcp MCP server | notebooklm, nlm-*, paper-review |
| twitter | TWITTER_COOKIE | x-to-slack, twitter-timeline-to-slack |
| browser | Playwright browsers installed | playwright-runner, e2e-testing, stock-csv-downloader |
| media | ffmpeg, yt-dlp | transcribee, video-compress |
| trading-apis | KIWOOM_APP_KEY, FRED_API_KEY, JINA_API_KEY, FINNHUB_API_KEY, POLYGON_API_KEY, NASDAQ_DATA_LINK_API_KEY, TWELVE_DATA_API_KEY, TIINGO_API_KEY | tab-kiwoom, today, alphaear-search, daily-stock-check |
| tradingview-mcp | `tradingview-mcp-server` Python pkg | tab-tradingview-ta, tab-tradingview-screener, tv-backtest, tv-live-data, tv-sentiment, tv-multi-timeframe, today (--with-tradingview) |
| ci-cd | act, Docker, pre-commit, ruff | ci-quality-gate, domain-commit |
| github | `gh` CLI (authenticated) | github-workflow-automation, release-ship, ship |
| mirofish | `uv`, Node ≥18, MiroFish repo, LLM + Zep keys | mirofish, mirofish-financial-sim, mirofish-opinion-sim, mirofish-graph-explorer |
| auto-research | Python 3.11+, AutoResearchClaw repo, OPENAI_API_KEY | auto-research, auto-research-distribute |
| cognee | `cognee` Python pkg, LLM_API_KEY | cognee |
| paperclip | `pnpm` ≥9.15, Node ≥20, Paperclip instance at `127.0.0.1:3100`, `~/work/thakicloud/paperclip` repo | paperclip-setup, paperclip-agents, paperclip-tasks, paperclip-control |
| agent-browser | `agent-browser` CLI, Chromium | agent-browser |
| security-scanning | `gitleaks` CLI | security-expert |
| document-generation | pdfplumber, python-docx, pypdf, pillow, opendataloader-pdf, JDK 11+, Node `docx`/`pptxgenjs`, pandoc | paper-review, anthropic-docx, anthropic-pptx, anthropic-pdf, opendataloader, bespin-news-digest |
| scrapling | `scrapling` Python pkg | scrapling |
| tossinvest | `tossctl`, Go ≥1.21, Playwright, Chromium | tossinvest-setup, tossinvest-cli, tossinvest-trading |
| dev-browser | `dev-browser` CLI (npm), Chromium | dev-browser |
| expect-qa | `expect-cli` (npm), Agent (cursor/claude/codex), Chromium | expect-qa |
| website-cloner | Node ≥18, npm, Playwright Chromium, Git, `cursor-ide-browser` MCP | clone-website |
| knowledge-base | `marp` CLI (or npx @marp-team/marp-cli), `matplotlib` Python pkg, `feedparser` Python pkg | kb-orchestrator, kb-ingest, kb-compile, kb-output, kb-auto-builder |
| atg-gateway | Docker, ATG container healthy at `http://localhost:4000/api/v1/health`, `.env` with NOTION_API_TOKEN + SLACK_BOT_TOKEN + GITHUB_TOKEN | atg-client (accelerates all Notion/Slack/GitHub skills) |
| agent-reach | `agent-reach` CLI (pipx), `rdt` (Reddit), `yt-dlp`, `gh`, `mcporter` (Exa) | agent-reach (fallback for defuddle, x-to-slack, twitter-timeline-to-slack, kb-ingest, bespin-news-digest, content-repurposing-engine, related-papers-scout) |
| pika-video | FAL_KEY, ffmpeg, `fal-client` Python pkg | pika-text-to-video, pika-video-pipeline, pikastream-video-meeting |
| sleek-mobile | SLEEK_API_KEY | sleek-design-mobile-apps |
| data-designer | `nemo-curator` Python pkg, NVIDIA_API_KEY (opt) | data-designer |
| lat-md | `lat` CLI (npm), LAT_LLM_KEY (opt) | lat-md |
| code-review-graph | `code-review-graph` CLI (pip), Python 3.9+ | code-review-graph, deep-review, simplify, code-review-all, ship, refactor-simulator, codemap-updater, ci-quality-gate, domain-commit |
| rhwp-documents | `rhwp` CLI (cargo), `cargo`, `@rhwp/core` (npm opt) | rhwp-viewer, rhwp-converter, rhwp-debug, rhwp-pipeline, rhwp-setup, rhwp-web-editor |
| stitch-mcp | Stitch MCP server configured, Node ≥18 | stitch-design, stitch-loop, stitch-react-components, stitch-remotion |
| shadcn-ui | Node ≥18, npm, `class-variance-authority` + `clsx` + `tailwind-merge` (npm), shadcn MCP (opt) | shadcn-ui |
| ui-design-quality | `.cursor/rules/design-system.mdc` exists, Node ≥18 | refined-swiss-prompt-enhancer, anti-slop-ui-guard, design-md-generator, ui-design-harness, design-qa-checklist |
| carbonyl-browser | `carbonyl` CLI | carbonyl-browser |
| obsidian-vault | `obsidian` CLI, Obsidian.app | obsidian-files, obsidian-search, obsidian-notes, obsidian-daily, obsidian-admin, obsidian-dev, obsidian-kb-bridge, brain-full-crew |
| feynman-research | `alpha` CLI | feynman-alpha-research, feynman-peer-review, feynman-paper-audit, feynman-replication, feynman-source-comparison, feynman-research-watch |
| diagrams | `dot` (graphviz) | diagrams-generator, visual-explainer, alphaear-logic-visualizer |
| remotion-video | `remotion` + `@remotion/cli` (npm), ffmpeg, Node ≥18 | remotion-motion-forge |
| paperclip-agents | Paperclip health at `127.0.0.1:3100/api/health`, ThakiCloud company exists (`/api/companies`) | paperclip-agents, paperclip-tasks, paperclip-control, paperclip-setup |
| reddit-reaction | ffmpeg, yt-dlp, gTTS, moviepy, Pillow | reddit-reaction-maker |
| runpod-gpu-cloud | `runpodctl` CLI, RUNPOD_API_KEY | runpod-setup, runpod-pods, runpod-volumes, runpod-transfer, feynman-replication (RunPod env) |

For full details on each group (install commands, env vars, verification), see [references/capability-map.md](references/capability-map.md).

For the complete env var registry, see [references/env-var-registry.md](references/env-var-registry.md).

## Workflow

### Phase 1: System Scan — CLI Tools

Check each tool via `command -v`:

```bash
for tool in gws hf gh act ffmpeg yt-dlp docker playwright pre-commit ruff uv rsync node python3 python3.11 pip3 npm npx pnpm researchclaw gitleaks rtk agent-browser dev-browser expect-cli pandoc jq cognee tossctl go marp agent-reach rdt mcporter rhwp cargo carbonyl obsidian alpha dot lat paperclip runpodctl java code-review-graph; do
  command -v "$tool" >/dev/null 2>&1 && echo "PASS $tool" || echo "FAIL $tool"
done
```

Record results in a table: `Tool | Status | Required By | Install Command`.

### Phase 2: Package Scan

**Python packages** — check critical packages via `pip show`:

```bash
for pkg in fastapi uvicorn sqlalchemy asyncpg alembic pandas numpy yfinance pykrx openai anthropic playwright feedparser huggingface-hub pdfplumber defusedxml lxml python-docx pypdf pillow opendataloader-pdf scrapling cognee beautifulsoup4 pyyaml imageio requests fal-client nemo-curator fastembed data-designer gTTS moviepy tradingview-mcp-server code-review-graph; do
  pip show "$pkg" >/dev/null 2>&1 && echo "PASS $pkg" || echo "FAIL $pkg"
done
```

**Node global packages** — check via `npm list -g --depth=0`:

```bash
for pkg in "@googleworkspace/cli" docx pptxgenjs agent-browser dev-browser expect-cli "@rhwp/core" remotion "@remotion/cli" lat.md "@paperclip-ai/cli" class-variance-authority clsx tailwind-merge; do
  npm list -g --depth=0 2>/dev/null | grep -q "$pkg" && echo "PASS $pkg" || echo "FAIL $pkg"
done
```

### Phase 3: Environment Scan

1. Check if `.env` file exists in project root
2. Parse `.env.example` for all variable names
3. For each variable in `.env.example`, check if it exists and is non-empty in `.env`
4. Also check skill-specific vars NOT in `.env.example`: `HF_TOKEN`, `NOTION_TOKEN`, `JINA_API_KEY`, `AA_API_KEY`, `MIROFISH_LLM_API_KEY`, `MIROFISH_ZEP_API_KEY`, `TWITTER_COOKIE`, `ELEVEN_LABS_API_KEY`, `LLM_API_KEY`, `LLM_MODEL`, `LLM_PROVIDER`, `BETTER_AUTH_SECRET`, `BROWSERBASE_API_KEY`, `FINVIZ_API_KEY`, `FMP_API_KEY`, `SLACK_SIGNING_SECRET`, `SLACK_APP_TOKEN`, `SLACK_USER_TOKEN`, `FAL_KEY`, `SLEEK_API_KEY`, `NVIDIA_API_KEY`, `OPENROUTER_API_KEY`, `LAT_LLM_KEY`, `GOOGLE_CREDENTIALS_FILE`, `KB_ROOT`, `EMBEDDING_PROVIDER`, `EMBEDDING_DIMENSIONS`, `RESEARCH_REPO`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `NOTION_API_TOKEN`, `SLACK_BOT_TOKEN`, `GITHUB_TOKEN`, `PAPERCLIP_API_KEY`, `RUNPOD_API_KEY`, `FINNHUB_API_KEY`, `POLYGON_API_KEY`, `NASDAQ_DATA_LINK_API_KEY`, `TWELVE_DATA_API_KEY`, `TIINGO_API_KEY`
5. Classify each as: SET (non-empty), EMPTY (exists but blank), MISSING (not in .env)

Present results grouped by capability group.

### Phase 4: MCP Scan

Check MCP server configs exist under the project's mcps directory:

```bash
MCP_DIR="$HOME/.cursor/projects/Users-hanhyojung-thaki-ai-model-event-stock-analytics/mcps"
for server in user-notebooklm-mcp plugin-notion-workspace-notion plugin-slack-slack cursor-ide-browser user-daiso-mcp user-public-apis user-Context7 user-GitHub user-Figma user-Notion plugin-context7-plugin-context7 plugin-huggingface-skills-huggingface-skills plugin-figma-figma cursor-app-control; do
  [ -d "$MCP_DIR/$server" ] && echo "PASS $server" || echo "FAIL $server"
done
```

### Phase 4.5: ATG Gateway Probe

Check if the Agent Tool Gateway Docker container is running and healthy:

```bash
# 1. Check Docker is available and ATG container exists
docker ps --filter "name=agent-tool-gateway" --format "{{.Names}} {{.Status}}" 2>/dev/null | grep -q "Up" \
  && echo "PASS atg-container-running" || echo "WARN atg-container-not-running (optional)"

# 2. Health check endpoint
curl -sf --max-time 3 http://localhost:4000/api/v1/health >/dev/null 2>&1 \
  && echo "PASS atg-health-endpoint" || echo "WARN atg-health-unreachable (optional)"
```

ATG is an **accelerator**, not a dependency. Mark failures as WARN (not FAIL) — skills work without ATG but benefit from caching, deduplication, and compression when it's running.

If ATG is healthy, additionally verify connector env vars are set for its native connectors:
- `NOTION_API_TOKEN` — required for ATG Notion connector
- `SLACK_BOT_TOKEN` — required for ATG Slack connector
- `GITHUB_TOKEN` — required for ATG GitHub connector

### Phase 4.6: Agent-Reach Channel Scan

Run `agent-reach doctor` to check channel health:

```bash
command -v agent-reach >/dev/null 2>&1 && agent-reach doctor 2>&1 || echo "SKIP agent-reach not installed"
```

Parse the doctor output for per-channel status. Key channels to verify:
- `github` (gh CLI) — zero-config
- `youtube` (yt-dlp) — zero-config
- `reddit` (rdt-cli) — zero-config
- `web/jina` (curl) — zero-config
- `twitter` (twitter-cli + cookie) — cookie required
- `exa` (mcporter + config) — MCP config required

Mark WARN (not FAIL) for missing cookie-required channels since they need manual setup.

### Phase 4.7: Project MCP Servers

Check MCP servers defined in `.cursor/mcp.json` (project-local servers distinct from Phase 4's Cursor-managed servers):

```bash
PROJECT_MCP="$(git rev-parse --show-toplevel)/.cursor/mcp.json"
if [ -f "$PROJECT_MCP" ]; then
  for server in huggingface kis-backtest tradingview-ta tradingview-screener kb-brain code-review-graph; do
    jq -e ".mcpServers[\"$server\"]" "$PROJECT_MCP" >/dev/null 2>&1 \
      && echo "PASS project-mcp:$server" || echo "WARN project-mcp:$server not configured"
  done
else
  echo "WARN .cursor/mcp.json not found"
fi
```

These are optional integrations — mark failures as WARN (not FAIL). Verify connectivity only when the server entry exists.

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
ATG Gateway:      [HEALTHY/UNREACHABLE] (optional accelerator)
Agent-Reach:      [N]/[T] channels active (fallback content router)
Project MCPs:     [N]/[T] configured (optional integrations)

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

CLI Tools:        16/23 passed
Python Packages:  20/26 passed
Node Packages:    1/4 passed
Environment Vars: 10/25 set
MCP Servers:      9/11 configured
ATG Gateway:      HEALTHY (caching Notion/Slack/GitHub calls)

Capability Group Status:
  core-platform:     READY
  llm-apis:          READY
  slack:             READY
  notion:            PARTIAL (NOTION_TOKEN empty — Notion MCP usable as fallback)
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
  auto-research:     READY
  cognee:            NOT READY (cognee missing, LLM_API_KEY missing)
  paperclip:         NOT READY (pnpm missing)
  agent-browser:     NOT READY (agent-browser missing)
  security-scanning: PARTIAL (gitleaks missing)
  document-generation: PARTIAL (pdfplumber missing, docx npm missing)
  scrapling:         NOT READY (scrapling missing)
  expect-qa:         NOT READY (expect-cli missing)
  atg-gateway:       HEALTHY (optional accelerator)

Missing Items:
  google-workspace  CLI   gws       — Install: npm install -g @googleworkspace/cli
  huggingface       CLI   hf        — Install: pip install huggingface-hub
  huggingface       ENV   HF_TOKEN  — Add to .env (get from https://huggingface.co/settings/tokens)
  media             CLI   yt-dlp    — Install: brew install yt-dlp
  twitter           ENV   TWITTER_COOKIE — Add to .env (extract from x.com browser cookies)
  expect-qa         CLI   expect-cli — Install: npm install -g expect-cli@latest
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
