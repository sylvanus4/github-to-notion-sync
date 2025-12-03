# Daily Sprint Sync

GitHub Projects와 Notion을 연동하여 스프린트 데이터를 자동으로 동기화하는 시스템입니다.

## 개요

Daily Sprint Sync는 매일 자동으로 실행되어 GitHub Projects의 데이터를 Notion으로 동기화하고, AI 기반 요약을 생성합니다.

### 핵심 기능

| 기능 | 설명 | 출력 |
|------|------|------|
| **Complete Resync** | GitHub Projects 데이터를 Notion DB로 전체 동기화 | Notion Database |
| **PR Review Check** | 스프린트 기간 PR의 리뷰 상태 체크 | Notion Database |
| **Sprint Stats** | 사용자별 이슈/PR/리뷰 통계 | Notion Database |
| **Sprint Summary** | AI 기반 스프린트 전체 요약 | Notion Page |
| **Daily Scrum** | AI 기반 일일 스크럼 요약 | Notion Page |

## 빠른 시작

### 1. 자동 실행 (기본)

워크플로우는 매일 **한국 시간 오전 7시 30분**에 자동 실행됩니다.

### 2. 수동 실행

GitHub Actions 탭에서 `Daily Sprint Sync` 워크플로우를 선택하고 "Run workflow"를 클릭합니다.

**수동 실행 옵션:**
- `team`: 팀 선택 (synos, ragos 등) - **NEW!**
- `sprint_filter`: 특정 스프린트 지정 (예: `25-12-Sprint1`)
- `notion_parent_id`: Notion 부모 페이지 ID
- `run_complete_resync`: 전체 동기화 실행 여부
- `run_pr_review_check`: PR 리뷰 체크 실행 여부
- `run_sprint_stats`: 스프린트 통계 실행 여부
- `run_sprint_summary`: 스프린트 요약 실행 여부
- `run_daily_scrum`: 데일리 스크럼 실행 여부

### 2.1 팀별 실행 (Multi-Team) - NEW!

여러 팀이 각자의 설정으로 동기화를 실행할 수 있습니다:

```bash
# GitHub Actions에서 팀 선택
# 1. Actions → Daily Sprint Sync → Run workflow
# 2. 팀 선택 드롭다운에서 원하는 팀 선택 (synos, ragos 등)
# 3. Run workflow 클릭

# 로컬에서 팀별 실행
PYTHONPATH=. python scripts/daily_scrum_sync.py --team synos
PYTHONPATH=. python scripts/complete_resync.py --team synos --force
```

팀을 선택하면 해당 팀의 `config/teams/{team}/sprint_config.yml` 설정이 자동으로 로드됩니다.

### 3. 스프린트 설정 변경

새 스프린트 시작 시 `config/sprint_config.yml` 파일을 업데이트합니다:

```yaml
current_sprint: 25-12-Sprint1
notion_parent_id: <PR-Checker 페이지 ID>
sprint_checker_parent_id: <SprintChecker 페이지 ID>
daily_scrum_parent_id: <DailyScrum 페이지 ID>
```

## 아키텍처

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│  GitHub Actions │──────│  Python Scripts  │──────│     Notion      │
│   (Scheduler)   │      │                  │      │   (Database)    │
└─────────────────┘      └──────────────────┘      └─────────────────┘
         │                        │                        │
         │                        │                        │
    ┌────▼────┐              ┌────▼────┐              ┌────▼────┐
    │ cron:   │              │ GitHub  │              │ Notion  │
    │ 22:30   │              │ GraphQL │              │   API   │
    │ UTC     │              │   API   │              │         │
    └─────────┘              └─────────┘              └─────────┘
```

## 문서 목차

| 문서 | 설명 |
|------|------|
| [FEATURE-SPECIFICATIONS](./FEATURE-SPECIFICATIONS.md) | 기능별 상세 명세 |
| [INFORMATION-ARCHITECTURE](./INFORMATION-ARCHITECTURE.md) | 시스템 아키텍처 및 데이터 흐름 |
| [WORKFLOW-GUIDE](./WORKFLOW-GUIDE.md) | GitHub Actions 워크플로우 가이드 |
| [CONFIGURATION](./CONFIGURATION.md) | 설정 파일 가이드 |
| [SCRIPTS-REFERENCE](./SCRIPTS-REFERENCE.md) | 스크립트 CLI 레퍼런스 |
| [ENVIRONMENT-SETUP](./ENVIRONMENT-SETUP.md) | 환경 설정 가이드 |
| [TROUBLESHOOTING](./TROUBLESHOOTING.md) | 문제 해결 가이드 |

## 필수 요구사항

### GitHub Secrets
- `GH_TOKEN`: GitHub Personal Access Token (repo, project 권한)
- `NOTION_TOKEN`: Notion Integration Token
- `ANTHROPIC_API_KEY`: Claude API Key (AI 요약용)

### GitHub Variables
- `GH_ORG`: GitHub Organization 이름
- `GH_PROJECT_NUMBER`: GitHub Project 번호
- `NOTION_DB_ID`: Notion Database ID

## 관련 파일

```
├── .github/workflows/
│   └── daily-sprint-sync.yml    # 메인 워크플로우
├── config/
│   ├── sprint_config.yml        # 스프린트 설정 (레거시)
│   ├── field_mappings.yml       # 공통 필드 매핑
│   └── teams/                   # 팀별 설정 (NEW!)
│       ├── synos/
│       │   ├── sprint_config.yml
│       │   └── field_mappings.yml
│       ├── ragos/
│       │   └── sprint_config.yml
│       └── _template/           # 새 팀 추가용 템플릿
│           └── sprint_config.yml
├── src/
│   └── utils/
│       └── team_config.py       # 팀 설정 로더 (NEW!)
└── scripts/
    ├── common/
    │   └── team_args.py         # 팀 인자 처리 (NEW!)
    ├── complete_resync.py       # 전체 동기화
    ├── sprint_pr_review_check.py # PR 리뷰 체크
    ├── sprint_stats.py          # 스프린트 통계
    ├── sprint_summary_sync.py   # 스프린트 요약
    ├── daily_scrum_sync.py      # 데일리 스크럼
    └── migrate_to_multi_team.py # 마이그레이션 스크립트 (NEW!)
```

## 지원

문의사항이 있으시면 GitHub Issues를 통해 연락해주세요.

