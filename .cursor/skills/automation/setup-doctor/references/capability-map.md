# Capability Map

Detailed prerequisites for each capability group: CLI tools, packages, env vars, MCP servers, install commands, and verification.

## Table of Contents

1. [core-platform](#1-core-platform) — PostgreSQL, Redis, backend/frontend
2. [llm-apis](#2-llm-apis) — OpenAI, Anthropic
3. [slack](#3-slack) — Slack bot, MCP
4. [notion](#4-notion) — Notion integration
5. [google-workspace](#5-google-workspace) — gws CLI
6. [huggingface](#6-huggingface) — HF CLI, Hub
7. [notebooklm](#7-notebooklm) — NLM MCP
8. [twitter](#8-twitter) — X/Twitter cookies
9. [browser](#9-browser) — Playwright
10. [media](#10-media) — ffmpeg, yt-dlp
11. [trading-apis](#11-trading-apis) — Kiwoom, FRED, Jina
12. [ci-cd](#12-ci-cd) — act, pre-commit, ruff
13. [github](#13-github) — gh CLI
14. [mirofish](#14-mirofish) — MiroFish swarm simulation engine
15. [auto-research](#15-auto-research) — AutoResearchClaw pipeline
16. [cognee](#16-cognee) — Knowledge graph engine
17. [paperclip](#17-paperclip) — AI agent orchestration platform
18. [document-generation](#18-document-generation) — DOCX, PPTX, PDF generation
19. [agent-browser](#19-agent-browser) — CLI browser automation
20. [security-scanning](#20-security-scanning) — Secret and vulnerability scanning
21. [scrapling](#21-scrapling) — Web scraping framework
22. [tossinvest](#22-tossinvest) — Toss Securities CLI (tossctl)
23. [dev-browser](#23-dev-browser) — Sandboxed browser automation (QuickJS WASM + Playwright)
24. [expect-qa](#24-expect-qa) — AI agent browser QA testing (expect-cli)
25. [website-cloner](#25-website-cloner) — AI website cloning pipeline

---

## 1. core-platform

**Purpose:** PostgreSQL database, Redis cache, Python backend, and frontend dev server.

**Prerequisites:**

| Type | Item | Install Command |
|------|------|-----------------|
| CLI | docker | `brew install --cask docker` |
| CLI | python3 | `brew install python@3.13` |
| CLI | node | `brew install node` |
| CLI | pip3 | Included with python3 |
| Package (Python) | fastapi, uvicorn, sqlalchemy, asyncpg, alembic, pandas, numpy, yfinance, pykrx | `pip install -r backend/requirements.txt` |
| Package (Node) | React, Vite, etc. | `cd frontend && pnpm install` |
| ENV | DATABASE_URL | `postgresql+asyncpg://postgres:postgres@localhost:5432/stock_analytics` | <!-- pragma: allowlist secret -->
| ENV | REDIS_URL | `redis://localhost:6379` |

**Quick Setup:**

```bash
make install        # Install Python + Node deps + pre-commit
make db-up          # Start PostgreSQL + Redis via Docker
make db-migrate     # Run Alembic migrations
```

**Verification:**

```bash
docker ps | grep -E "postgres|redis"
python3 -c "import fastapi; print(fastapi.__version__)"
curl -s http://localhost:4567/health
```

**Dependent Skills:** today, daily-stock-check, tab-*, weekly-stock-update, stock-csv-downloader, weekly-stock-update

---

## 2. llm-apis

**Purpose:** OpenAI and Anthropic API access for LLM-powered analysis.

**Prerequisites:**

| Type | Item | Install Command |
|------|------|-----------------|
| Package (Python) | openai, anthropic | `pip install openai anthropic` |
| ENV | OPENAI_API_KEY | Get from https://platform.openai.com/api-keys |
| ENV | ANTHROPIC_API_KEY | Get from https://console.anthropic.com/settings/keys |

**Verification:**

```bash
python3 -c "import openai; print('openai OK')"
python3 -c "import anthropic; print('anthropic OK')"
[ -n "$OPENAI_API_KEY" ] && echo "OPENAI_API_KEY set" || echo "OPENAI_API_KEY missing"
[ -n "$ANTHROPIC_API_KEY" ] && echo "ANTHROPIC_API_KEY set" || echo "ANTHROPIC_API_KEY missing"
```

**Dependent Skills:** today, paper-review, alphaear-*, trading-*, role-*, ai-quality-evaluator

---

## 3. slack

**Purpose:** Post messages, threads, and file uploads to Slack channels.

**Prerequisites:**

| Type | Item | Install Command |
|------|------|-----------------|
| ENV | SLACK_BOT_TOKEN | Create Slack App at https://api.slack.com/apps → OAuth & Permissions |
| ENV | SLACK_REPORT_CHANNEL | Channel name (default: `h-report`) |
| ENV (OPT) | SLACK_SIGNING_SECRET | Required for slack-agent bot development |
| ENV (OPT) | SLACK_APP_TOKEN | Required for slack-agent Socket Mode (`xapp-...`) |
| MCP | plugin-slack-slack | Configure in Cursor MCP settings |

**Verification:**

```bash
[ -n "$SLACK_BOT_TOKEN" ] && echo "SLACK_BOT_TOKEN set" || echo "SLACK_BOT_TOKEN missing"
[ -d "$HOME/.cursor/projects/Users-hanhyojung-thaki-ai-platform-webui/mcps/plugin-slack-slack" ] && echo "Slack MCP configured" || echo "Slack MCP missing"
```

**Dependent Skills:** today, paper-review, related-papers-scout, x-to-slack, eod-ship, morning-ship, role-dispatcher, google-daily, slack-agent

---

## 4. notion

**Purpose:** Create, read, and update Notion pages and databases.

**Authentication Strategy:** Token-first → MCP fallback.
- **Primary:** `NOTION_TOKEN` in `.env` enables direct REST API calls via `scripts/notion_api.py`
- **Fallback:** `plugin-notion-workspace-notion` MCP (browser OAuth) when token is unavailable

**Prerequisites:**

| Type | Item | Install Command | Priority |
|------|------|-----------------|----------|
| ENV | NOTION_TOKEN | Create integration at https://www.notion.so/my-integrations, add to `.env` | Primary |
| Python | scripts/notion_api.py | Already included in repo | Primary |
| MCP | plugin-notion-workspace-notion | Configure in Cursor MCP settings | Fallback |
| MCP | user-Notion | Configure in Cursor MCP settings | Fallback |

**Verification:**

```bash
[ -n "$NOTION_TOKEN" ] && echo "NOTION_TOKEN set (direct API ready)" || echo "NOTION_TOKEN missing (will use MCP fallback)"
[ -d "$HOME/.cursor/projects/Users-hanhyojung-thaki-ai-platform-webui/mcps/plugin-notion-workspace-notion" ] && echo "Notion MCP configured (fallback ready)" || echo "Notion MCP missing"
```

**Status Logic:**
- `NOTION_TOKEN` set → READY (direct API)
- `NOTION_TOKEN` empty but MCP configured → PARTIAL (MCP fallback only)
- Both missing → NOT READY

**Dependent Skills:** md-to-notion, notion-docs-sync, paper-archive, paper-review, meeting-digest, notion-meeting-sync, md-enhance-publish, md-notion-slides-publish, deep-research-pipeline, prd-research-factory

---

## 5. google-workspace

**Purpose:** Gmail, Calendar, Drive, Sheets, Docs, Chat access via the gws CLI.

**Prerequisites:**

| Type | Item | Install Command |
|------|------|-----------------|
| CLI | gws | `npm install -g @googleworkspace/cli` |
| Auth | OAuth credentials | `gws auth login` (requires Google Cloud project with OAuth consent) |

**Quick Setup:**

```bash
npm install -g @googleworkspace/cli
gws auth login
```

For detailed setup, invoke the `gws-workspace` skill.

**Verification:**

```bash
command -v gws && echo "gws installed" || echo "gws missing"
gws auth status 2>/dev/null
```

**Dependent Skills:** gws-*, calendar-daily-briefing, gmail-daily-triage, google-daily, ai-chief-of-staff, morning-ship

---

## 6. huggingface

**Purpose:** Download/upload models and datasets, run training jobs on HF infrastructure.

**Prerequisites:**

| Type | Item | Install Command |
|------|------|-----------------|
| CLI | hf | `curl -LsSf https://hf.co/cli/install.sh \| bash -s` or `pip install -U huggingface_hub[cli]` |
| CLI | uv | `pip install uv` (for hf-jobs) |
| ENV | HF_TOKEN | Get from https://huggingface.co/settings/tokens |

**Quick Setup:**

```bash
curl -LsSf https://hf.co/cli/install.sh | bash -s
hf auth login
```

**Verification:**

```bash
command -v hf && echo "hf CLI installed" || echo "hf CLI missing"
hf auth whoami 2>/dev/null
```

**Dependent Skills:** hf-hub, hf-models, hf-repos, hf-papers, hf-jobs, hf-model-trainer, hf-datasets, hf-evaluation, hf-dataset-viewer, hf-trackio

---

## 7. notebooklm

**Purpose:** Manage Google NotebookLM notebooks, sources, and content generation.

**Prerequisites:**

| Type | Item | Install Command |
|------|------|-----------------|
| MCP | user-notebooklm-mcp | Configure in Cursor MCP settings |

**Note:** NotebookLM MCP requires absolute file paths for local source uploads.

**Verification:**

```bash
[ -d "$HOME/.cursor/projects/Users-hanhyojung-thaki-ai-platform-webui/mcps/user-notebooklm-mcp" ] && echo "NotebookLM MCP configured" || echo "NotebookLM MCP missing"
```

**Dependent Skills:** notebooklm, notebooklm-research, notebooklm-studio, nlm-slides, nlm-video, nlm-deep-learn, nlm-arxiv-slides, paper-review

---

## 8. twitter

**Purpose:** Fetch tweets and post analysis to Slack.

**Prerequisites:**

| Type | Item | Install Command |
|------|------|-----------------|
| ENV | TWITTER_COOKIE | Extract from x.com browser cookies (auth_token, ct0, twid) |
| ENV | TWITTER_CSRF_TOKEN | ct0 value from x.com cookies (optional) |
| ENV | TWITTER_BEARER_TOKEN | Authorization bearer from x.com API (optional) |

**How to obtain:** Open x.com in Chrome → DevTools → Application → Cookies → copy `auth_token`, `ct0`, `twid` values into TWITTER_COOKIE.

**Verification:**

```bash
[ -n "$TWITTER_COOKIE" ] && echo "TWITTER_COOKIE set" || echo "TWITTER_COOKIE missing"
```

**Dependent Skills:** x-to-slack, twitter-timeline-to-slack

---

## 9. browser

**Purpose:** Headless browser automation for scraping, testing, and form filling.

**Prerequisites:**

| Type | Item | Install Command |
|------|------|-----------------|
| Package (Python) | playwright | `pip install playwright` |
| Browser binaries | Chromium | `npx playwright install chromium` |

**Quick Setup:**

```bash
pip install playwright
npx playwright install chromium
```

**Verification:**

```bash
python3 -c "from playwright.sync_api import sync_playwright; print('playwright OK')"
npx playwright --version 2>/dev/null
```

**Dependent Skills:** playwright-runner, e2e-testing, e2e-overhaul, stock-csv-downloader, gmail-daily-triage, anthropic-webapp-testing

**Note:** For CLI-based browser automation (as opposed to Playwright test suites), see also the [agent-browser](#19-agent-browser) group.

---

## 10. media

**Purpose:** Video/audio processing and transcription.

**Prerequisites:**

| Type | Item | Install Command |
|------|------|-----------------|
| CLI | ffmpeg | `brew install ffmpeg` |
| CLI | yt-dlp | `brew install yt-dlp` |
| ENV (OPT) | ELEVEN_LABS_API_KEY | Required for transcribee speaker diarization |
| ENV (OPT) | ANTHROPIC_API_KEY | Required for transcribee categorization (reuses llm-apis) |

**Verification:**

```bash
command -v ffmpeg && echo "ffmpeg installed" || echo "ffmpeg missing"
command -v yt-dlp && echo "yt-dlp installed" || echo "yt-dlp missing"
[ -n "$ELEVEN_LABS_API_KEY" ] && echo "ELEVEN_LABS_API_KEY set" || echo "ELEVEN_LABS_API_KEY missing (optional)"
```

**Dependent Skills:** transcribee, video-compress

---

## 11. trading-apis

**Purpose:** External financial data APIs.

**Prerequisites:**

| Type | Item | Install Command |
|------|------|-----------------|
| ENV | KIWOOM_APP_KEY | Register at https://openapi.kiwoom.com |
| ENV | KIWOOM_SECRET_KEY | Register at https://openapi.kiwoom.com |
| ENV | FRED_API_KEY | Register at https://fred.stlouisfed.org/docs/api/api_key.html |
| ENV | JINA_API_KEY | Get from https://jina.ai |
| ENV | FINVIZ_API_KEY | Get from https://finviz.com (optional) |
| ENV | FMP_API_KEY | Get from https://financialmodelingprep.com (optional) |

**Verification:**

```bash
for var in KIWOOM_APP_KEY FRED_API_KEY JINA_API_KEY; do
  [ -n "$(eval echo \$$var)" ] && echo "PASS $var" || echo "FAIL $var"
done
```

**Dependent Skills:** tab-kiwoom, today (FRED), alphaear-search (Jina), trading-finviz-screener, trading-market-top-detector, trading-theme-detector

---

## 12. ci-cd

**Purpose:** Local CI checks, linting, and pre-commit hooks.

**Prerequisites:**

| Type | Item | Install Command |
|------|------|-----------------|
| CLI | act | `brew install act` |
| CLI | docker | Required by act |
| CLI | pre-commit | `pip install pre-commit && pre-commit install` |
| CLI | ruff | `pip install ruff` |

**Quick Setup:**

```bash
brew install act
pip install pre-commit ruff
pre-commit install
```

**Verification:**

```bash
command -v act && echo "act installed" || echo "act missing"
command -v pre-commit && echo "pre-commit installed" || echo "pre-commit missing"
command -v ruff && echo "ruff installed" || echo "ruff missing"
pre-commit --version 2>/dev/null
```

**Dependent Skills:** ci-quality-gate, domain-commit, release-commander, ecc-verification-loop

---

## 13. github

**Purpose:** GitHub CLI for issues, PRs, and project management.

**Prerequisites:**

| Type | Item | Install Command |
|------|------|-----------------|
| CLI | gh | `brew install gh` |
| Auth | GitHub auth | `gh auth login` |

**Verification:**

```bash
command -v gh && echo "gh installed" || echo "gh missing"
gh auth status 2>/dev/null
```

**Dependent Skills:** github-workflow-automation, commit-to-issue, release-ship, ship, pr-review-captain

---

## 14. mirofish

**Purpose:** MiroFish multi-agent swarm intelligence simulation engine for scenario prediction.

**Prerequisites:**

| Type | Item | Install Command |
|------|------|-----------------|
| CLI | uv | `brew install uv` or `pip install uv` |
| CLI | node | `brew install node` (>= 18) |
| CLI | npm | Bundled with Node.js |
| Repo | MiroFish | `cd ~/thaki && git clone https://github.com/666ghj/MiroFish.git` |
| Package (Node) | MiroFish frontend | `cd ~/thaki/MiroFish && npm run setup:all` |
| Package (Python) | MiroFish backend (via uv) | Included in `npm run setup:all` |
| ENV | MIROFISH_LLM_API_KEY | Reuses OPENAI_API_KEY or separate key |
| ENV | MIROFISH_LLM_BASE_URL | OpenAI-compatible endpoint (default: `https://api.openai.com/v1`) |
| ENV | MIROFISH_LLM_MODEL_NAME | Model name (e.g., `gpt-4o`, `qwen-plus`) |
| ENV | MIROFISH_ZEP_API_KEY | Get from https://app.getzep.com/ (free tier) |

**Quick Setup:**

```bash
cd ~/thaki && git clone https://github.com/666ghj/MiroFish.git
cd MiroFish && npm run setup:all
cp .env.example .env
# Edit .env with API keys
npm run dev   # Starts frontend :3000 + backend :5001
```

**Verification:**

```bash
[ -d "$HOME/thaki/MiroFish/backend" ] && echo "PASS repo cloned" || echo "FAIL repo not cloned"
command -v uv && echo "PASS uv" || echo "FAIL uv"
node -v 2>/dev/null | grep -qE "^v(1[89]|[2-9][0-9])" && echo "PASS node >= 18" || echo "FAIL node < 18"
[ -f "$HOME/thaki/MiroFish/.env" ] && echo "PASS .env exists" || echo "FAIL .env missing"
curl -s http://localhost:5001/health 2>/dev/null | grep -q "ok" && echo "PASS backend running" || echo "WARN backend not running"
```

**Dependent Skills:** mirofish, mirofish-financial-sim, mirofish-opinion-sim, mirofish-graph-explorer

---

## 15. auto-research

**Purpose:** AutoResearchClaw 23-stage autonomous research pipeline for generating conference-ready papers.

**Prerequisites:**

| Type | Item | Install Command |
|------|------|-----------------|
| CLI | python3.11 | `brew install python@3.11` |
| CLI | researchclaw | `cd ~/thaki/AutoResearchClaw && .venv/bin/pip install -e .` |
| Repo | AutoResearchClaw | `cd ~/thaki && git clone https://github.com/aiming-lab/AutoResearchClaw.git` |
| Package (Python) | AutoResearchClaw (in venv) | `cd ~/thaki/AutoResearchClaw && /opt/homebrew/bin/python3.11 -m venv .venv && source .venv/bin/activate && pip install -e .` |
| ENV | OPENAI_API_KEY | Get from https://platform.openai.com/api-keys (reuses llm-apis group) |

**Quick Setup:**

```bash
cd ~/thaki && git clone https://github.com/aiming-lab/AutoResearchClaw.git
cd AutoResearchClaw
/opt/homebrew/bin/python3.11 -m venv .venv && source .venv/bin/activate
pip install -e .
cp config.researchclaw.example.yaml config.arc.yaml
researchclaw --help
```

**Verification:**

```bash
[ -d "$HOME/thaki/AutoResearchClaw" ] && echo "PASS repo cloned" || echo "FAIL repo not cloned"
[ -f "$HOME/thaki/AutoResearchClaw/.venv/bin/researchclaw" ] && echo "PASS researchclaw installed" || echo "FAIL researchclaw missing"
command -v python3.11 >/dev/null 2>&1 && echo "PASS python3.11" || echo "FAIL python3.11 missing"
[ -n "$OPENAI_API_KEY" ] && echo "PASS OPENAI_API_KEY set" || echo "FAIL OPENAI_API_KEY missing"
```

**Dependent Skills:** auto-research, auto-research-distribute

---

## 16. cognee

**Purpose:** Persistent AI memory and knowledge graph engine for document ingestion, entity extraction, and graph-enhanced RAG search.

**Prerequisites:**

| Type | Item | Install Command |
|------|------|-----------------|
| Package (Python) | cognee | `pip install cognee` |
| CLI | cognee (optional) | `pip install cognee` (provides `cognee` CLI) |
| ENV | LLM_API_KEY | OpenAI or compatible API key |
| ENV (OPT) | LLM_MODEL | Model name (default: `gpt-4o-mini`) |
| ENV (OPT) | LLM_PROVIDER | Provider name (default: `openai`) |

**Quick Setup:**

```bash
pip install cognee
# Or with extras:
# pip install 'cognee[postgres,neo4j,anthropic]'
```

**Verification:**

```bash
python3 -c "import cognee; print('cognee OK')" 2>/dev/null && echo "PASS cognee" || echo "FAIL cognee"
[ -n "$LLM_API_KEY" ] && echo "PASS LLM_API_KEY set" || echo "FAIL LLM_API_KEY missing"
```

**Dependent Skills:** cognee

---

## 17. paperclip

**Purpose:** Paperclip AI agent orchestration platform for hiring, scheduling, and managing autonomous agents.

**Prerequisites:**

| Type | Item | Install Command |
|------|------|-----------------|
| CLI | pnpm | `npm install -g pnpm` (≥9.15) |
| CLI | node | `brew install node` (≥20) |
| CLI | docker | `brew install --cask docker` |
| System | PostgreSQL 17 or PGlite | Docker: `docker run -p 5432:5432 postgres:17` |
| ENV | BETTER_AUTH_SECRET | Random secret for auth (`openssl rand -hex 32`) |
| ENV (OPT) | OPENAI_API_KEY | Reuses llm-apis group |
| ENV (OPT) | ANTHROPIC_API_KEY | Reuses llm-apis group |

**Quick Setup:**

```bash
npm install -g pnpm
cd <paperclip-dir>
pnpm install
cp .env.example .env
# Edit .env with BETTER_AUTH_SECRET and API keys
pnpm paperclipai doctor
```

**Verification:**

```bash
command -v pnpm && echo "PASS pnpm" || echo "FAIL pnpm"
node -v 2>/dev/null | grep -qE "^v(2[0-9]|[3-9][0-9])" && echo "PASS node >= 20" || echo "FAIL node < 20"
command -v docker && echo "PASS docker" || echo "FAIL docker"
[ -n "$BETTER_AUTH_SECRET" ] && echo "PASS BETTER_AUTH_SECRET set" || echo "FAIL BETTER_AUTH_SECRET missing"
```

**Dependent Skills:** paperclip-setup, paperclip-agents, paperclip-tasks, paperclip-control

---

## 18. document-generation

**Purpose:** Generate professional Word documents, PowerPoint presentations, and PDFs from code.

**Prerequisites:**

| Type | Item | Install Command |
|------|------|-----------------|
| Package (Python) | pdfplumber | `pip install pdfplumber` |
| Package (Python) | defusedxml | `pip install defusedxml` |
| Package (Python) | lxml | `pip install lxml` |
| Package (Python) | python-docx | `pip install python-docx` |
| Package (Python) | pypdf | `pip install pypdf` |
| Package (Python) | pillow | `pip install pillow` |
| Package (Node) | docx | `npm install -g docx` |
| Package (Node) | pptxgenjs | `npm install -g pptxgenjs` |
| CLI (OPT) | pandoc | `brew install pandoc` |

**Quick Setup:**

```bash
pip install pdfplumber defusedxml lxml python-docx pypdf pillow
npm install -g docx pptxgenjs
brew install pandoc
```

**Note:** Node scripts that use `docx` or `pptxgenjs` require `NODE_PATH="$(npm root -g)"` to resolve global packages.

**Verification:**

```bash
for pkg in pdfplumber defusedxml lxml docx pypdf PIL; do
  python3 -c "import $pkg" 2>/dev/null && echo "PASS $pkg" || echo "FAIL $pkg"
done
npm list -g --depth=0 2>/dev/null | grep -q "docx" && echo "PASS docx (npm)" || echo "FAIL docx (npm)"
npm list -g --depth=0 2>/dev/null | grep -q "pptxgenjs" && echo "PASS pptxgenjs (npm)" || echo "FAIL pptxgenjs (npm)"
command -v pandoc && echo "PASS pandoc" || echo "FAIL pandoc (optional)"
```

**Dependent Skills:** paper-review, anthropic-docx, anthropic-pptx, anthropic-pdf, bespin-news-digest, critical-review, related-papers-scout

---

## 19. agent-browser

**Purpose:** CLI-based headless browser automation for navigating pages, filling forms, taking screenshots, and scraping data.

**Prerequisites:**

| Type | Item | Install Command |
|------|------|-----------------|
| CLI | agent-browser | `npm install -g agent-browser` |
| Browser binaries | Chromium | `agent-browser install` |
| ENV (OPT) | BROWSERBASE_API_KEY | For cloud browser sessions (https://browserbase.com) |
| ENV (OPT) | BROWSERBASE_PROJECT_ID | For cloud browser sessions |
| ENV (OPT) | BROWSER_USE_API_KEY | For Browser Use cloud (https://browser-use.com) |
| ENV (OPT) | KERNEL_API_KEY | For Kernel cloud browser |

**Quick Setup:**

```bash
npm install -g agent-browser
agent-browser install
```

**Verification:**

```bash
command -v agent-browser && echo "PASS agent-browser" || echo "FAIL agent-browser"
agent-browser --version 2>/dev/null
```

**Dependent Skills:** agent-browser

---

## 20. security-scanning

**Purpose:** Secret detection and vulnerability scanning in source code.

**Prerequisites:**

| Type | Item | Install Command |
|------|------|-----------------|
| CLI | gitleaks | `brew install gitleaks` |

**Quick Setup:**

```bash
brew install gitleaks
```

**Verification:**

```bash
command -v gitleaks && echo "PASS gitleaks" || echo "FAIL gitleaks"
gitleaks version 2>/dev/null
```

**Dependent Skills:** security-expert, ci-quality-gate

---

## 21. scrapling

**Purpose:** Python web scraping framework with adaptive parsing, anti-bot bypass (Cloudflare Turnstile), and stealth fetching.

**Prerequisites:**

| Type | Item | Install Command |
|------|------|-----------------|
| Package (Python) | scrapling | `pip install 'scrapling[all]'` |

**Quick Setup:**

```bash
pip install 'scrapling[all]'
# Or minimal: pip install scrapling
# Or with specific fetchers: pip install 'scrapling[fetchers]'
```

**Verification:**

```bash
python3 -c "import scrapling; print('scrapling OK')" 2>/dev/null && echo "PASS scrapling" || echo "FAIL scrapling"
```

**Dependent Skills:** scrapling

---

## 22. tossinvest

**Purpose:** Toss Securities brokerage CLI for Korean market trading, portfolio management, and account operations.

**Prerequisites:**

| Type | Item | Install Command |
|------|------|-----------------|
| CLI | tossctl | `go install github.com/JungHoonGhae/tossinvest-cli/cmd/tossctl@latest` |
| CLI | go (>= 1.21) | `brew install go` |
| Package (Python) | playwright | `pip install playwright && playwright install chromium` |
| Browser | chromium | `playwright install chromium` |
| CLI | python3 (>= 3.9) | `brew install python@3.12` |

**Quick Setup:**

```bash
go install github.com/JungHoonGhae/tossinvest-cli/cmd/tossctl@latest
pip install playwright && playwright install chromium
tossctl config init
tossctl doctor
```

**Environment Variables:**

None required. Authentication uses browser-based login via `tossctl auth login`.

**Local State Files:**

| File | Purpose |
|------|---------|
| `~/.config/tossctl/config.json` | Trading permissions and settings |
| `~/.config/tossctl/session.json` | Browser session state |
| `~/.config/tossctl/trading-permission.json` | Temporary trading permission TTL |
| `~/.config/tossctl/trading-lineage.json` | Order lineage for recovery |

**Verification:**

```bash
command -v tossctl && echo "PASS tossctl" || echo "FAIL tossctl"
command -v go && echo "PASS go" || echo "FAIL go"
python3 -c "import playwright; print('PASS playwright')" 2>/dev/null || echo "FAIL playwright"
playwright install --dry-run chromium 2>/dev/null && echo "PASS chromium" || echo "FAIL chromium"
tossctl doctor 2>/dev/null
```

**Dependent Skills:** tossinvest-setup, tossinvest-cli, tossinvest-trading

---

## 23. dev-browser

**Purpose:** Sandboxed browser automation via heredoc JavaScript scripts with QuickJS WASM runtime and full Playwright Page API access, persistent named pages.

**Prerequisites:**

| Type | Item | Install Command |
|------|------|-----------------|
| CLI | dev-browser | `npm install -g dev-browser` |
| Browser binaries | Chromium | `dev-browser install` |

**Quick Setup:**

```bash
npm install -g dev-browser
dev-browser install
```

**Verification:**

```bash
command -v dev-browser && echo "PASS dev-browser" || echo "FAIL dev-browser"
dev-browser --version 2>/dev/null
```

**Dependent Skills:** dev-browser

---

## 24. expect-qa

**Purpose:** AI agent-driven browser QA testing. Scans git changes, generates adversarial test plans, and executes them in a real Playwright browser with rrweb session recording.

**Prerequisites:**

| Type | Item | Install Command |
|------|------|-----------------|
| CLI | expect-cli | `npm install -g expect-cli@latest` |
| CLI | One of: cursor, claude, codex | (agent must be available) |
| Browser binaries | Chromium (via Playwright) | `npx playwright install chromium` |
| Env (optional) | `EXPECT_BASE_URL` | Target app URL (default: http://localhost:3000) |

**Quick Setup:**

```bash
npm install -g expect-cli@latest
npx playwright install chromium
expect-cli init -y
```

**Verification:**

```bash
command -v expect-cli && echo "PASS expect-cli" || echo "FAIL expect-cli"
expect-cli --version 2>/dev/null
(command -v cursor || command -v claude || command -v codex) && echo "PASS agent" || echo "WARN no agent detected"
```

**Dependent Skills:** expect-qa

---

## 25. website-cloner

**Purpose:** Reverse-engineer and rebuild websites as pixel-perfect Next.js 16 clones using browser automation, CSS extraction, and parallel builder subagents.

**Prerequisites:**

| Type | Item | Install Command |
|------|------|-----------------|
| CLI | node (>= 18) | `brew install node` |
| CLI | npm | Bundled with Node.js |
| CLI | git | `brew install git` (usually pre-installed) |
| Browser binaries | Chromium (Playwright) | `npx playwright install chromium` |
| MCP | cursor-ide-browser | Built into Cursor — enable in MCP settings |

**Quick Setup:**

```bash
brew install node
npx playwright install chromium
```

The `cursor-ide-browser` MCP is built into Cursor and must be enabled in the MCP server settings.

**Verification:**

```bash
node -v 2>/dev/null | grep -qE "^v(1[89]|[2-9][0-9])" && echo "PASS node >= 18" || echo "FAIL node < 18"
command -v npm && echo "PASS npm" || echo "FAIL npm"
command -v git && echo "PASS git" || echo "FAIL git"
npx playwright --version 2>/dev/null && echo "PASS playwright" || echo "FAIL playwright"
```

For `cursor-ide-browser` MCP, verify by checking:
```bash
[ -d "$HOME/.cursor/projects/$(basename $PWD)/mcps/cursor-ide-browser" ] && echo "PASS cursor-ide-browser MCP" || echo "FAIL cursor-ide-browser MCP (enable in Cursor MCP settings)"
```

**Dependent Skills:** clone-website
