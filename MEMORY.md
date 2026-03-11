# MEMORY.md

## [decision] User Preferences (extracted from transcripts, 2026-03-10)

- Plans, analysis, and architectural discussions should be in English ("영어로 계획해줘")
- Reports, summaries, and user-facing outputs must be in Korean
- Do not edit hidden/dotfiles directly; use shell commands to modify them
- Always use `--team synos` when running sprint-related workflows; omitting it causes wrong project lookup
- Use GitHub project #5 for Synos — project #22 is deprecated and should not be used
- When implementing a plan, do not edit the plan file itself; mark todos as in_progress and complete all before stopping
- gws CLI requires a Desktop app OAuth client (`{"installed": {...}}`), not a Web app (`{"web": {...}}`)
- Python scripts must run with `.venv/bin/python` or `source .venv/bin/activate` — system Python lacks project dependencies

## [task] Workspace Facts (extracted from transcripts, 2026-03-10)

- GitHub Synos project number: 5 (configured in `config/teams/synos/sprint_config.yml`)
- Sprint field name in GitHub Projects can be `"스프린트"`, `"Sprint"`, or `"Iteration"` — handle all three
- 이상민 GitHub username: `thakicloud-leesangmin` (not `sangmin.lee`)
- ai-platform-webui git workflow: commit → push to `tmp` → issue → report (no PR/merge, tmp-branch only)
- Other repos git workflow: commit → push → issue → PR → merge
- GWS OAuth credentials location: `~/.config/gws/client_secret.json` (global); `client_secret*.json` is in `.gitignore`
- GWS plaintext credentials: `~/.config/gws/credentials.json` with `type: authorized_user` (macOS Keychain workaround)
- Notion meeting database ID: `22c9eddc34e680d5beb9d2cf6c8403b4`
- Notion API uses `NOTION_TOKEN` from `.env`
- Virtual environment path: project root `.venv/`
- If `gh` project linking fails: run `gh auth refresh -s read:org,read:discussion` then retry

## [task] Google Daily (2026-03-10)

- Calendar: 12 events (Research 데일리 스크럼, 기획 스프린트, QA 집중 시간, AI 트렌드/Papers 정리)
- Gmail: 11 emails triaged (spam: 0, notifications: 7, colleague: 1, news: 1, reply-needed: 0)
- Colleague emails: 이정훈 팀장 (경영관리팀) - Google Cloud 비용 계정 생성 완료 회신
- News themes: AI 에이전트 시장 폭발 (오픈클로), AI 보안 취약점, 프로액티브 AI (카톡/나우넛지), AI 이미지 생성 GPU 효율 향상, 네이버 검색 점유율 vs AI 플랫폼
- Action items: Google Cloud 계정 설정 확인 필요
- Slack: summary + 2 threads posted to #효정-할일
- Drive: bespin-news-2026-03-10.docx uploaded to "Google Daily - 2026-03-10" folder

## [issue] continual-learning 스킬 AGENTS.md 문제 (2026-03-10)

- `continual-learning` 스킬(cursor-public 플러그인)은 Claude Code 컨벤션인 `AGENTS.md`를 생성함
- 이 프로젝트는 Cursor IDE를 사용하며 메모리 시스템은 `MEMORY.md`
- continual-learning 실행 시 출력 대상을 `MEMORY.md`로 변경해야 함
