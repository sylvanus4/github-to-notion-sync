---
name: gov-chat-bot-setup
description: >-
  Clone, install, configure, and operate the Gov-chat-bot (SmartBot KR) — an open-source
  KakaoTalk-integrated AI consultation chatbot platform. Handles full lifecycle from
  GitHub clone through Docker deployment, admin setup, FAQ/document management, KakaoTalk
  Open Builder integration, homepage widget embedding, and LLM provider configuration.
triggers:
  - "gov-chat-bot"
  - "install gov-chat-bot"
  - "setup chatbot"
  - "카카오톡 챗봇 설치"
  - "Gov-chat-bot 설치"
  - "SmartBot KR"
  - "공공기관 챗봇"
  - "카카오톡 AI 챗봇"
  - "gov chatbot deploy"
  - "챗봇 플랫폼 설치"
  - "챗봇 설치해줘"
  - "gov-chat-bot 설정"
  - "kakao chatbot setup"
tags:
  - chatbot
  - kakao
  - docker
  - rag
  - faq
  - public-sector
version: "1.0"
---

# Gov-Chat-Bot Setup & Operation

Deploy and operate [Gov-chat-bot (SmartBot KR)](https://github.com/sinmb79/Gov-chat-bot) — an MIT-licensed KakaoTalk AI consultation chatbot with RAG + FAQ + PII masking.

## Prerequisites

| Requirement | Minimum |
|---|---|
| OS | macOS 13+ / Ubuntu 20.04+ / Windows 11 (WSL2) |
| RAM | 4 GB |
| Disk | 20 GB free |
| Docker | 24.x+ with `docker compose` |
| Internet | Required for initial setup (offline operation afterward) |

## Phase 1 — Clone & Install

```bash
# Default install location: ~/Gov-chat-bot
INSTALL_DIR="${GOVBOT_DIR:-$HOME/Gov-chat-bot}"

# Clone
git clone https://github.com/sinmb79/Gov-chat-bot.git "$INSTALL_DIR"
cd "$INSTALL_DIR"

# Run automated installer
chmod +x install.sh
./install.sh
```

The `install.sh` script automatically:
1. Checks Docker installation (installs on Linux if missing)
2. Generates `.env` with a random `SECRET_KEY`
3. Builds Docker images (`backend`, `frontend`)
4. Starts all 5 services: `db` (PostgreSQL 16), `redis` (Redis 7), `chromadb`, `backend` (FastAPI), `frontend` (React)
5. Runs Alembic database migrations
6. Performs health check at `http://localhost:8000/health`

If `install.sh` fails or you need manual control:

```bash
cp .env.example .env
# Edit .env — at minimum set SECRET_KEY
docker compose up -d
docker compose exec backend alembic upgrade head
```

### Verify Services

```bash
# All 5 containers should be running
docker compose ps

# Health check
curl http://localhost:8000/health

# Access points
# Admin dashboard: http://localhost:3000
# API docs:        http://localhost:8000/docs
```

## Phase 2 — Initial Configuration

### Create Admin Account

```bash
docker compose exec backend python -m app.scripts.create_admin
```

Provide:
- **Organization ID** (English lowercase, e.g., `my-org`, `city-hall`, `test-cafe`)
- **Email** (login credential)
- **Password** (8+ characters)

### Configure Organization Info

Set fallback message details via the admin dashboard or API:

| Key | Description | Example |
|---|---|---|
| `tenant_name` | Organization name | 테스트 카페 |
| `phone_number` | Contact number | 02-1234-5678 |
| `fallback_dept` | Fallback department | 고객센터 |

## Phase 3 — FAQ & Document Management

### Register FAQ Entries

1. Login at `http://localhost:3000`
2. Navigate to **FAQ 관리** → **+ FAQ 추가**
3. Enter: category, question, answer
4. Register multiple phrasings for the same answer to improve matching accuracy

Example FAQ set:
```
Category: 영업시간
Q1: "영업시간이 어떻게 되나요?"
Q2: "몇 시에 열어요?"
Q3: "오늘 언제까지 하나요?"
A:  "평일 09:00~18:00, 주말 10:00~15:00 운영합니다."
```

### Upload Documents (Optional)

Supported formats: `.pdf` (text-based only), `.docx`, `.txt`, `.md`

1. **문서 관리** → **+ 문서 업로드** → select file
2. Wait for status to become `processed`
3. Click **승인** (Approve) — documents are NOT used until approved

### Test via Simulator

Use the **시뮬레이터** menu to test questions and verify responses before going live.

## Phase 4 — Channel Integration

### Option A: KakaoTalk Integration (via Kakao i Open Builder)

The backend exposes a skill endpoint at: `POST /skill/{organization_id}`

1. Go to [Kakao i Open Builder](https://i.kakao.com/) and create a channel
2. Create a new skill:
   - **Skill URL**: `http://<YOUR_PUBLIC_IP_OR_DOMAIN>:8000/skill/<your-org-id>`
   - Method: POST
3. Create a scenario block that routes user messages to this skill
4. Deploy the channel

> KakaoTalk integration requires a **publicly accessible server** (public IP, domain, or tunnel like ngrok for testing).

### Option B: Homepage Widget

Add this snippet before `</body>` in your HTML:

```html
<script
  src="http://YOUR_SERVER:8000/widget/govbot-widget.js"
  data-tenant="YOUR_ORG_ID"
  data-api="http://YOUR_SERVER:8000"
  data-title="AI 도우미"
  data-color="#2563eb"
></script>
```

## Phase 5 — LLM Configuration (Optional)

The system works without an LLM (FAQ + document search only). To enable AI-enhanced responses:

Edit `.env`:

```bash
# For Claude
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...

# Or for GPT
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
```

Then restart:
```bash
docker compose restart backend
```

## Operations Reference

### Service Management

```bash
docker compose up -d        # Start all services
docker compose down          # Stop all services
docker compose restart       # Restart all
docker compose logs backend  # View backend logs
docker compose logs -f       # Follow all logs
```

### Database Backup & Restore

```bash
# Backup
docker compose exec db pg_dump -U botuser smartbot > backup_$(date +%Y%m%d).sql

# Restore
docker compose exec -T db psql -U botuser smartbot < backup_YYYYMMDD.sql
```

### Port Conflicts

Edit `docker-compose.yml` to change ports:
- Backend: `"8000:8000"` → `"8080:8000"`
- Frontend: `"3000:80"` → `"3001:80"`

### Embedding Model

First run downloads the Korean embedding model `jhgan/ko-sroberta-multitask` (~400 MB).
If download fails:
```bash
docker compose exec backend curl -I https://huggingface.co
docker compose exec backend rm -rf /root/.cache/huggingface
docker compose restart backend
```

## Architecture

```
User Question
    │
    ▼
① FAQ Search (similarity matching against registered FAQ)
    │ Match found → immediate response
    │ No match ↓
    ▼
② Document Search (RAG from uploaded files via ChromaDB)
    │ Content found + LLM connected → AI-rephrased response
    │ Content found + No LLM       → raw document excerpt
    │ No content ↓
    ▼
③ Fallback (configured contact info / department)
```

### Docker Services

| Service | Image | Port | Purpose |
|---|---|---|---|
| db | postgres:16-alpine | 5432 | Relational data |
| redis | redis:7-alpine | 6379 | Cache & sessions |
| chromadb | chromadb/chroma | 8001 | Vector search |
| backend | custom (FastAPI) | 8000 | API server |
| frontend | custom (React) | 3000 | Admin dashboard |

## Do NOT Use For

- Production deployment without security audit (this skill sets up a dev/test instance)
- KakaoTalk channel management (use Kakao i Open Builder console directly)
- Custom backend development or code modification (edit the code directly)
- ThakiCloud AI Platform integration (use the platform's native chatbot features)
