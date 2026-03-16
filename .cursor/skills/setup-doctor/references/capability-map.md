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
| ENV | DATABASE_URL | `postgresql+asyncpg://postgres:postgres@localhost:5432/stock_analytics` |
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
| MCP | plugin-slack-slack | Configure in Cursor MCP settings |

**Verification:**

```bash
[ -n "$SLACK_BOT_TOKEN" ] && echo "SLACK_BOT_TOKEN set" || echo "SLACK_BOT_TOKEN missing"
[ -d "$HOME/.cursor/projects/Users-hanhyojung-thaki-ai-model-event-stock-analytics/mcps/plugin-slack-slack" ] && echo "Slack MCP configured" || echo "Slack MCP missing"
```

**Dependent Skills:** today, paper-review, related-papers-scout, x-to-slack, eod-ship, morning-ship, role-dispatcher, google-daily

---

## 4. notion

**Purpose:** Create, read, and update Notion pages and databases.

**Prerequisites:**

| Type | Item | Install Command |
|------|------|-----------------|
| ENV | NOTION_TOKEN | Create integration at https://www.notion.so/my-integrations |
| MCP | plugin-notion-workspace-notion | Configure in Cursor MCP settings |
| MCP | user-Notion | Configure in Cursor MCP settings |

**Verification:**

```bash
[ -n "$NOTION_TOKEN" ] && echo "NOTION_TOKEN set" || echo "NOTION_TOKEN missing"
[ -d "$HOME/.cursor/projects/Users-hanhyojung-thaki-ai-model-event-stock-analytics/mcps/plugin-notion-workspace-notion" ] && echo "Notion MCP configured" || echo "Notion MCP missing"
```

**Dependent Skills:** md-to-notion, notion-docs-sync, paper-archive, meeting-digest, notion-meeting-sync

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
| CLI | hf | `pip install huggingface-hub[cli]` |
| CLI | uv | `pip install uv` (for hf-jobs) |
| ENV | HF_TOKEN | Get from https://huggingface.co/settings/tokens |

**Quick Setup:**

```bash
pip install huggingface-hub[cli]
huggingface-cli login
```

**Verification:**

```bash
command -v huggingface-cli && echo "hf CLI installed" || echo "hf CLI missing"
huggingface-cli whoami 2>/dev/null
```

**Dependent Skills:** hf-cli, hf-jobs, hf-model-trainer, hf-datasets, hf-evaluation, hf-dataset-viewer, hf-trackio

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
[ -d "$HOME/.cursor/projects/Users-hanhyojung-thaki-ai-model-event-stock-analytics/mcps/user-notebooklm-mcp" ] && echo "NotebookLM MCP configured" || echo "NotebookLM MCP missing"
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

---

## 10. media

**Purpose:** Video/audio processing and transcription.

**Prerequisites:**

| Type | Item | Install Command |
|------|------|-----------------|
| CLI | ffmpeg | `brew install ffmpeg` |
| CLI | yt-dlp | `brew install yt-dlp` |

**Verification:**

```bash
command -v ffmpeg && echo "ffmpeg installed" || echo "ffmpeg missing"
command -v yt-dlp && echo "yt-dlp installed" || echo "yt-dlp missing"
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

**Dependent Skills:** tab-kiwoom, today (FRED), alphaear-search (Jina), trading-finviz-screener, trading-market-top-detector

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
