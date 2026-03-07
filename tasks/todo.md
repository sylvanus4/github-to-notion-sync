# Tasks

## Current Tasks

### AI Chief of Staff -- GCP OAuth 설정 (브라우저 수동 작업)

- [ ] Google Cloud Console 접속 (https://console.cloud.google.com/)
- [ ] 새 프로젝트 생성 (예: AI-Chief-of-Staff)
- [ ] 3개 API 활성화: Gmail API, Google Calendar API, Google Drive API
- [ ] APIs & Services > OAuth consent screen -- Internal 선택, 앱 이름/이메일 입력
- [ ] APIs & Services > Credentials -- Create Credentials > OAuth client ID > Desktop app > JSON 다운로드
- [ ] `gwcli profiles add work --client ~/Downloads/client_secret_*.json` 실행
- [ ] `gwcli profiles set-default work` 실행
- [ ] 인증 확인: `gwcli gmail list --limit 3 --format json`
- [ ] 인증 확인: `gwcli calendar events --days 1 --format json`
- [ ] 인증 확인: `gwcli drive list --limit 3 --format json`

### AI Chief of Staff -- 라이브 테스트

- [ ] `/morning-sweep` 커맨드 실행 테스트
- [ ] `/meeting-prep-gwcli` 커맨드 실행 테스트
- [ ] `/weekly-digest` 커맨드 실행 테스트

---

## Completed

### AI Chief of Staff -- gwcli 설치 (Completed: 2026-03-07)

- [x] `~/work/tools/google-workspace-cli` 클론 및 빌드
- [x] `npm link`로 gwcli 글로벌 설치
- [x] `gwcli --help` 동작 확인

### AI Chief of Staff -- 스킬 작성 (Completed: 2026-03-07)

- [x] `.cursor/skills/ai-chief-of-staff/SKILL.md` 오케스트레이터 작성
- [x] `references/morning-sweep.md` 작성
- [x] `references/meeting-prep.md` 작성
- [x] `references/weekly-digest.md` 작성

### AI Chief of Staff -- 스킬 최적화 (Completed: 2026-03-07)

- [x] Anthropic audit checklist 기반 감사 수행
- [x] Examples 섹션을 "User says -> Actions -> Result" 형식으로 개선
- [x] gwcli Command Reference를 `references/gwcli-reference.md`로 추출 (progressive disclosure)
- [x] Cursor 커맨드 3개 생성: `/morning-sweep`, `/meeting-prep-gwcli`, `/weekly-digest`
