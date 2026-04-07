# Environment Variable Registry

All environment variables required or used by project skills, organized by capability group.

**Legend:** REQ = Required for group to function, OPT = Optional / enhances functionality

---

## core-platform

| Variable | Priority | Default | Description | Source |
|----------|----------|---------|-------------|--------|
| DATABASE_URL | REQ | `postgresql+asyncpg://postgres:postgres@localhost:5432/stock_analytics` | Async PostgreSQL connection string | Local Docker | <!-- pragma: allowlist secret -->
| DATABASE_ECHO | OPT | `false` | Log SQL queries | — |
| REDIS_URL | OPT | `redis://localhost:6379` | Redis cache URL | Local Docker |
| APP_NAME | OPT | `AI Model Event Stock Analytics` | Application name | — |
| DEBUG | OPT | `true` | Debug mode | — |
| ENVIRONMENT | OPT | `development` | `development` / `staging` / `production` | — |
| LOG_LEVEL | OPT | `INFO` | `DEBUG` / `INFO` / `WARNING` / `ERROR` | — |
| CORS_ORIGINS | OPT | `http://localhost:5173,...` | Allowed CORS origins | — |
| DATA_DIR | OPT | `data` | Data directory path | — |
| CACHE_DIR | OPT | `data/cache` | Cache directory path | — |
| REPORTS_DIR | OPT | `data/reports` | Reports output directory | — |

## llm-apis

| Variable | Priority | Default | Description | Source |
|----------|----------|---------|-------------|--------|
| OPENAI_API_KEY | REQ | — | OpenAI API key | https://platform.openai.com/api-keys |
| OPENAI_MODEL | OPT | `gpt-4o` | Default OpenAI model | — |
| OPENAI_TEMPERATURE | OPT | `1.0` | LLM temperature | — |
| ANTHROPIC_API_KEY | REQ | — | Claude API key | https://console.anthropic.com/settings/keys |

## slack

| Variable | Priority | Default | Description | Source |
|----------|----------|---------|-------------|--------|
| SLACK_BOT_TOKEN | REQ | — | Slack Bot OAuth token (`xoxb-...`) | https://api.slack.com/apps → OAuth |
| SLACK_REPORT_CHANNEL | OPT | `h-report` | Default Slack channel for reports | — |
| SLACK_SIGNING_SECRET | OPT | — | Required for slack-agent bot development | Slack App → Basic Info |
| SLACK_APP_TOKEN | OPT | — | Required for slack-agent Socket Mode (`xapp-...`) | Slack App → Basic Info |
| SLACK_USER_TOKEN | OPT | — | User OAuth token (`xoxp-...`) for slack-orphan-cleaner thread deletion | Slack App → OAuth (User Token Scopes) |

## notion

| Variable | Priority | Default | Description | Source |
|----------|----------|---------|-------------|--------|
| NOTION_TOKEN | REQ | — | Notion integration token (`ntn_...`) | https://www.notion.so/my-integrations |

## google-workspace

No env vars — uses OAuth via `gws auth login`. Credentials stored locally by gws CLI.

## huggingface

| Variable | Priority | Default | Description | Source |
|----------|----------|---------|-------------|--------|
| HF_TOKEN | REQ | — | HuggingFace access token | https://huggingface.co/settings/tokens |
| AA_API_KEY | OPT | — | Artificial Analysis API key (hf-evaluation) | https://artificialanalysis.ai |

## notebooklm

No env vars — uses MCP server configuration in Cursor settings.

## twitter

| Variable | Priority | Default | Description | Source |
|----------|----------|---------|-------------|--------|
| TWITTER_COOKIE | REQ | — | Full cookie string from x.com | Browser DevTools → Cookies |
| TWITTER_CSRF_TOKEN | OPT | — | ct0 value from x.com cookies | Browser DevTools → Cookies |
| TWITTER_BEARER_TOKEN | OPT | — | Bearer token from x.com API | Browser DevTools → Network |

## browser

No env vars — requires Playwright browser binaries installed via `npx playwright install chromium`.

## media

| Variable | Priority | Default | Description | Source |
|----------|----------|---------|-------------|--------|
| ELEVEN_LABS_API_KEY | OPT | — | ElevenLabs API for transcribee speaker diarization | https://elevenlabs.io |

## trading-apis

| Variable | Priority | Default | Description | Source |
|----------|----------|---------|-------------|--------|
| KIWOOM_APP_KEY | OPT | — | Kiwoom Securities API key | https://openapi.kiwoom.com |
| KIWOOM_SECRET_KEY | OPT | — | Kiwoom Securities secret | https://openapi.kiwoom.com |
| KIWOOM_ENV | OPT | `mock` | `production` / `mock` | — |
| KIWOOM_ACCOUNT_1 | OPT | — | Primary Kiwoom account | — |
| KIWOOM_ACCOUNT_2 | OPT | — | Secondary Kiwoom account | — |
| FRED_API_KEY | OPT | — | Federal Reserve Economic Data API | https://fred.stlouisfed.org/docs/api/api_key.html |
| JINA_API_KEY | OPT | — | Jina AI search API key | https://jina.ai |
| FINVIZ_API_KEY | OPT | — | FinViz screener API key | https://finviz.com |
| FMP_API_KEY | OPT | — | Financial Modeling Prep API | https://financialmodelingprep.com |

## ci-cd

No env vars — requires CLI tools (act, pre-commit, ruff, Docker).

## github

No env vars — uses `gh auth login` for authentication.

---

## Auth and Security (not group-specific)

| Variable | Priority | Default | Description |
|----------|----------|---------|-------------|
| REQUIRE_AUTH | OPT | `false` | Enable API authentication |
| API_KEY | OPT | — | API key for endpoint protection |
| JWT_SECRET_KEY | OPT | `change-me-in-production` | JWT signing secret |
| JWT_ALGORITHM | OPT | `HS256` | JWT algorithm |
| JWT_ACCESS_TOKEN_EXPIRE_MINUTES | OPT | `60` | Access token TTL |
| JWT_REFRESH_TOKEN_EXPIRE_MINUTES | OPT | `10080` | Refresh token TTL (7 days) |

## Observability (not group-specific)

| Variable | Priority | Default | Description |
|----------|----------|---------|-------------|
| SENTRY_DSN | OPT | — | Sentry error tracking DSN |
| VITE_SENTRY_DSN | OPT | — | Frontend Sentry DSN |
| SLOW_QUERY_THRESHOLD_MS | OPT | `100` | Slow query logging threshold |

## mirofish

| Variable | Priority | Default | Description | Source |
|----------|----------|---------|-------------|--------|
| MIROFISH_LLM_API_KEY | REQ | — | LLM API key for MiroFish (can reuse OPENAI_API_KEY) | https://platform.openai.com/api-keys |
| MIROFISH_LLM_BASE_URL | REQ | `https://api.openai.com/v1` | OpenAI-compatible API base URL | — |
| MIROFISH_LLM_MODEL_NAME | REQ | `gpt-4o` | LLM model name | — |
| MIROFISH_ZEP_API_KEY | REQ | — | Zep Cloud API key for agent long-term memory | https://app.getzep.com/ |
| MIROFISH_LLM_BOOST_API_KEY | OPT | — | Faster LLM for high-throughput agent interactions | — |
| MIROFISH_LLM_BOOST_BASE_URL | OPT | — | Boost model API base URL | — |
| MIROFISH_LLM_BOOST_MODEL_NAME | OPT | — | Boost model name | — |

## ML / Sentiment (AlphaEar skills)

| Variable | Priority | Default | Description |
|----------|----------|---------|-------------|
| BERT_SENTIMENT_MODEL | OPT | `ProsusAI/finbert` | Sentiment model HF ID |
| EMBEDDING_MODEL | OPT | `paraphrase-multilingual-MiniLM-L12-v2` | Embedding model for hybrid search |
| SENTIMENT_MODE | OPT | `auto` | `auto` / `bert` / `llm` |

## cognee

| Variable | Priority | Default | Description | Source |
|----------|----------|---------|-------------|--------|
| LLM_API_KEY | REQ | — | LLM API key for cognee knowledge engine | https://platform.openai.com/api-keys |
| LLM_MODEL | OPT | `gpt-4o-mini` | LLM model name | — |
| LLM_PROVIDER | OPT | `openai` | LLM provider (`openai` / `anthropic` / `ollama`) | — |

## paperclip

| Variable | Priority | Default | Description | Source |
|----------|----------|---------|-------------|--------|
| BETTER_AUTH_SECRET | REQ | — | Auth secret for Paperclip (`openssl rand -hex 32`) | Generated locally |
| API_KEY | OPT | — | API key for Paperclip agent LLM access | — |
| API_BASE | OPT | — | Base URL for Paperclip LLM endpoint | — |

## agent-browser

| Variable | Priority | Default | Description | Source |
|----------|----------|---------|-------------|--------|
| BROWSERBASE_API_KEY | OPT | — | BrowserBase cloud browser sessions | https://browserbase.com |
| BROWSERBASE_PROJECT_ID | OPT | — | BrowserBase project identifier | https://browserbase.com |
| BROWSER_USE_API_KEY | OPT | — | Browser Use cloud API key | https://browser-use.com |
| KERNEL_API_KEY | OPT | — | Kernel cloud browser API key | — |

## document-generation

No env vars — requires Python packages (pdfplumber, python-docx, pypdf, pillow, defusedxml, lxml) and Node globals (docx, pptxgenjs).

## security-scanning

No env vars — requires `gitleaks` CLI tool.

## scrapling

No env vars — requires `scrapling` Python package.

## pika-video

| Variable | Priority | Default | Description | Source |
|----------|----------|---------|-------------|--------|
| FAL_KEY | REQ | — | fal.ai API key for Pika v2.2 video generation | https://fal.ai/dashboard/keys |

## sleek

| Variable | Priority | Default | Description | Source |
|----------|----------|---------|-------------|--------|
| SLEEK_API_KEY | REQ | — | Sleek REST API key for mobile app screen design | https://sleek.design |

## data-designer

| Variable | Priority | Default | Description | Source |
|----------|----------|---------|-------------|--------|
| NVIDIA_API_KEY | OPT | — | NVIDIA NIM API key for synthetic data generation | https://build.nvidia.com |
| OPENROUTER_API_KEY | OPT | — | OpenRouter API key (alternative LLM provider) | https://openrouter.ai/keys |
| NEMO_TELEMETRY_ENABLED | OPT | `false` | Enable NeMo telemetry reporting | — |

## lat-md

| Variable | Priority | Default | Description | Source |
|----------|----------|---------|-------------|--------|
| LAT_LLM_KEY | OPT | — | LLM API key for `lat search` semantic queries | Reuse OPENAI_API_KEY or ANTHROPIC_API_KEY |

## knowledge-base

| Variable | Priority | Default | Description | Source |
|----------|----------|---------|-------------|--------|
| KB_ROOT | OPT | `knowledge-bases` | Root directory for Knowledge Base topics | — |
| EMBEDDING_PROVIDER | OPT | `openai` | Embedding provider (`openai` / `fastembed` / `local`) | — |
| EMBEDDING_MODEL | OPT | `text-embedding-3-small` | Embedding model name | — |
| EMBEDDING_DIMENSIONS | OPT | `1536` | Embedding vector dimensions | — |
| RESEARCH_REPO | OPT | — | Path to research repo for KB source sync | — |

## pikastream

| Variable | Priority | Default | Description | Source |
|----------|----------|---------|-------------|--------|
| FAL_KEY | REQ | — | fal.ai API key (shared with pika-video) for PikaStreaming avatar + voice | https://fal.ai/dashboard/keys |

## google-seo

| Variable | Priority | Default | Description | Source |
|----------|----------|---------|-------------|--------|
| GOOGLE_CREDENTIALS_FILE | OPT | — | Path to Google service account JSON (for Search Console) | Google Cloud Console |
| GOOGLE_CLIENT_ID | OPT | — | OAuth client ID for Google APIs | Google Cloud Console |
| GOOGLE_CLIENT_SECRET | OPT | — | OAuth client secret for Google APIs | Google Cloud Console |

## atg-gateway

| Variable | Priority | Default | Description | Source |
|----------|----------|---------|-------------|--------|
| NOTION_API_TOKEN | REQ | — | Notion API token for ATG Notion connector | https://www.notion.so/my-integrations |
| SLACK_BOT_TOKEN | REQ | — | Slack Bot token for ATG Slack connector (shared with slack group) | Slack App → OAuth |
| GITHUB_TOKEN | REQ | — | GitHub token for ATG GitHub connector | `gh auth token` or https://github.com/settings/tokens |

## agent-reach

No env vars — individual channels use their own auth (Twitter cookie, Exa MCP config, etc.). Run `agent-reach doctor` for per-channel health.

## reddit-reaction

No env vars — Reddit scraping uses public `.json` endpoints (no API key). Font auto-downloads on first run.
