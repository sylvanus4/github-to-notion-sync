# Environment Variable Registry

All environment variables required or used by project skills, organized by capability group.

**Legend:** REQ = Required for group to function, OPT = Optional / enhances functionality

---

## core-platform

| Variable | Priority | Default | Description | Source |
|----------|----------|---------|-------------|--------|
| DATABASE_URL | REQ | `postgresql+asyncpg://postgres:postgres@localhost:5432/stock_analytics` | Async PostgreSQL connection string | Local Docker |
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

No env vars — requires ffmpeg and yt-dlp CLI tools.

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
