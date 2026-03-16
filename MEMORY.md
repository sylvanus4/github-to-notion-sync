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

## [task] Google Daily (2026-03-12)

- Calendar: 5 events (09:30 데일리 스크럼, 10:00 경쟁사 벤치마크 보고서 리뷰, 11:00 Synos 개발 스프린트, 14:00 ML파이프라인 설계 워크숍, 15:30 제안서 검토 미팅)
- Gmail: 15+ emails triaged (spam: 2 trashed, notifications: 11 moved to Low Priority, colleague: 1 이미 회신 완료, news: 1 Bespin News)
- Notification categories moved to Label_9: Notion, RunPod, NotebookLM, Calendar accepts, Google security, Gemini, GitHub
- News themes: 하이브리드 클라우드 재평가, 한국 AI 챗봇 '제타' 1위, 오픈AI IPO 고평가 논란, AWS·노키아 에이전틱 AI 네트워크, 아마존 300조원 AI 투자, MS 에이전트 관리 플랫폼, 삼성SDS 국가AI컴퓨팅센터, AI 자율형 보안운영센터
- ThakiCloud 인사이트: 하이브리드 AI 인프라 포지셔닝 강화, 에이전트 플랫폼 로드맵 가속화, GPU 비용 최적화 차별화, 보안 레이어 강화, 공공 GPU 클라우드 사업 기회
- Action items: 없음 (미회신 메일 없음)
- Slack: summary + 2 threads (뉴스 다이제스트 + AI/GPU Cloud 인사이트) posted to #효정-할일
- Drive: 생성 문서 없음, 건너뛰기

## [task] Google Daily (2026-03-13)

- Calendar: 10 events (면접 1 - PM 박종철, 미팅 3 - Research 스크럼/DeepResearch 회고/Sprint Retro, 외부미팅 1 - 라이너 김하영 팀장 저녁, 기타 5)
- 집중 가능: 09:00~10:00, 12:30~14:00, 16:30~18:00 (약 4.5시간)
- Gmail: 13 emails triaged (spam: 0, notifications: 6 moved to Low Priority, colleague: 5, news: 1 Bespin News 37건, reply-needed: 0, sent: 2 skip)
- Notification categories moved to Label_9: Notion, RunPod, NotebookLM, Google Security, Cursor, Calendar accept
- Colleague emails: 전승훈 CTO x3 (Meeting 참석요청/Agent Cloud 로드맵+Financial Model/nvidia Nemotron3), 상면규 (B200 VPN 완료), 정훈 (Thaki Suite 배포 공지)
- News themes: 엔비디아 Nemotron3 Super 에이전트 모델, Nvidia $2B Nebius 투자, 젠슨 황 인프라 수조 달러, AMD 리사 수 방한, Databricks Genie Code+Quotient AI, 에이전트 카드/결제, AI 앱 구독 유지율 21%, Kai $125M 보안 에이전트
- ThakiCloud 인사이트: Nemotron3 블랙웰 최적화 추론 차별화, Neocloud 파트너십 포지셔닝, B2B 인프라 과금 모델 유리, 에이전트 평가/보안 레이어 통합 필수, GPU 인프라 장기 성장 구간 진입
- Action items: Financial Model 자료 준비 여부 확인 (전승훈 CTO → 윤성노 요청건)
- Slack: summary + 7 threads (팀원 메일 5 + 뉴스 다이제스트 + AI/GPU Cloud 인사이트) posted to #효정-할일
- Drive: 생성 문서 없음, 건너뛰기

## [task] Google Daily (2026-03-16)

- Calendar: 6 events (스프린트 계획회의, 점심, 전사 주간 업무 보고(HIGH, 전승훈 CTO), DeepResearch 정기 회의(전승훈 CTO), 개인 작업 3건)
- 집중 가능: 09:00~10:00, 10:30~11:30, 16:00~18:30 (약 4.5시간)
- Gmail: 3 emails triaged (spam: 0, notifications: 3 moved to Low Priority, colleague: 0, news: 0, reply-needed: 0)
- Notification categories moved to Label_9: NotebookLM, Notion, Google AI Studio
- Colleague emails: 없음 (일요일)
- News themes: 없음
- Action items: Google AI Studio Gemini API 결제 설정 확인 필요
- Slack: summary posted to #효정-할일 (쓰레드 없음 — 팀원 메일/뉴스 0건)
- Drive: 생성 문서 없음, 건너뛰기

## [issue] continual-learning 스킬 AGENTS.md 문제 (2026-03-10)

- `continual-learning` 스킬(cursor-public 플러그인)은 Claude Code 컨벤션인 `AGENTS.md`를 생성함
- 이 프로젝트는 Cursor IDE를 사용하며 메모리 시스템은 `MEMORY.md`
- continual-learning 실행 시 출력 대상을 `MEMORY.md`로 변경해야 함
