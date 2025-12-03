# Feature Specifications

Daily Sprint Sync 시스템의 기능별 상세 명세서입니다.

---

## 1. 멀티 팀 지원 (Multi-Team Support) - NEW!

### 1.1 기능 개요

| 항목 | 내용 |
|------|------|
| **모듈** | `src/utils/team_config.py`, `scripts/common/team_args.py` |
| **목적** | 여러 팀이 각자의 설정으로 독립적인 동기화 수행 |
| **적용 범위** | 모든 daily-sprint-sync 스크립트 |

### 1.2 기능 명세

| 기능 | 항목 | 상세 | 비고 |
|------|------|------|------|
| **팀 설정 로드** | 설정 위치 | `config/teams/{team_id}/sprint_config.yml` | |
| | 설정 구조 | team, github, notion, sprint 섹션 | 전체 구조는 CONFIGURATION.md 참조 |
| | 폴백 | 레거시 `config/sprint_config.yml` 지원 | 하위 호환 |
| **필드 매핑** | 공통 매핑 | `config/field_mappings.yml` | 모든 팀 공유 |
| | 팀별 매핑 | `config/teams/{team_id}/field_mappings.yml` | 선택적 오버라이드 |
| | 병합 전략 | 팀별 설정이 공통 설정을 오버라이드 | |
| **CLI 인터페이스** | `--team` 옵션 | 모든 스크립트에서 지원 | |
| | 우선순위 | CLI 옵션 > 팀 설정 > 레거시 설정 | |

### 1.3 설정 파일 구조

```
config/
├── sprint_config.yml          # 레거시 (하위 호환)
├── field_mappings.yml         # 공통 필드 매핑
└── teams/
    ├── synos/
    │   ├── sprint_config.yml  # Synos 팀 설정
    │   └── field_mappings.yml # Synos 팀 필드 매핑 (선택)
    ├── ragos/
    │   └── sprint_config.yml  # RagOS 팀 설정
    └── _template/
        └── sprint_config.yml  # 새 팀 추가용 템플릿
```

### 1.4 TeamConfig 데이터 모델

```python
@dataclass
class TeamConfig:
    team_id: str              # 팀 식별자
    team_name: str            # 팀 표시 이름
    description: str          # 팀 설명
    enabled: bool             # 활성화 여부
    
    github_org: str           # GitHub Organization
    github_project_number: int # GitHub Project 번호
    
    notion_database_id: str   # Notion DB ID (선택)
    
    current_sprint: str       # 현재 스프린트
    notion_parent_id: str     # PR-Checker 페이지 ID
    sprint_checker_parent_id: str  # SprintChecker 페이지 ID
    daily_scrum_parent_id: str     # DailyScrum 페이지 ID
    qa_database_id: str       # QA DB ID (선택)
```

---

## 2. Complete Resync (전체 동기화)

### 2.1 기능 개요

| 항목 | 내용 |
|------|------|
| **스크립트** | `scripts/complete_resync.py` |
| **목적** | GitHub Projects 데이터를 Notion Database로 전체 동기화 |
| **트리거** | 스케줄 (매일 7:30 KST) 또는 수동 실행 |
| **타임아웃** | 30분 |

### 2.2 기능 명세

| 기능 | 항목 | 상세 | 비고 |
|------|------|------|------|
| **데이터베이스 클리어** | 동작 | 기존 Notion 페이지 전체 삭제 | - 삭제 성공률 90% 이상 시 성공 처리<br>- 삭제 간 0.1초 딜레이 |
| | 옵션 | `--dry-run` 시 삭제 대신 카운트만 표시 | |
| **데이터 동기화** | 필터링 | `--sprint-filter` 또는 팀 설정의 `current_sprint` 사용 | |
| | 배치 처리 | 기본 50개 단위 배치 (`--batch-size`) | Rate limit 방지 |
| | 재시도 | 실패 시 최대 3회 재시도 (지수 백오프) | 1초, 2초, 4초 대기 |
| **콘텐츠 동기화** | Body | Issue/PR 본문 Notion 페이지에 추가 | |
| | Comments | Issue/PR 코멘트 수집 및 추가 | |
| **DB 타이틀 업데이트** | 자동 생성 | `GitHub Sync - {Sprint} - {Timestamp}` | `--database-title`로 커스텀 가능 |
| **멀티 팀 지원** | `--team` 옵션 | 팀 설정에서 GitHub/Notion 정보 자동 로드 | NEW! |

### 2.3 입력/출력

**입력:**
```
--team             : 팀 ID (NEW!)
--sprint-filter    : 스프린트 필터 (선택)
--batch-size       : 배치 크기 (기본: 50)
--database-title   : DB 타이틀 (선택, 자동 생성)
--dry-run          : 미리보기 모드
--force            : 확인 프롬프트 스킵
```

**출력:**
- Notion Database에 동기화된 페이지들
- 실행 통계 (총 아이템, 생성/삭제 수, 실패 수)

### 2.4 필드 매핑

| GitHub Field | Notion Property | Type |
|--------------|-----------------|------|
| `title` | 피드백 제목 | title |
| `id` | GitHub ID | rich_text |
| `__typename` | 태그 | multi_select |
| `Status` | 진행 상태 | status |
| `Priority` | 우선순위 | select |
| `End date` | 마감일 | date |
| `Estimate` | 스토리포인트 | number |
| `Assignees` | 담당자 | people |

---

## 3. Sprint PR Review Check (PR 리뷰 체크)

### 3.1 기능 개요

| 항목 | 내용 |
|------|------|
| **스크립트** | `scripts/sprint_pr_review_check.py` |
| **목적** | 스프린트 기간 PR들의 리뷰 상태 체크 및 리포팅 |
| **트리거** | 스케줄 또는 수동 실행 |
| **타임아웃** | 15분 |

### 3.2 기능 명세

| 기능 | 항목 | 상세 | 비고 |
|------|------|------|------|
| **스프린트 기간 조회** | 자동 계산 | GitHub Project의 Iteration 필드에서 날짜 추출 | 스프린트명으로 검색 |
| **PR 수집** | 범위 | 조직 전체 레포지토리의 PR | GraphQL API 사용 |
| | 필터링 | 스프린트 기간 내 생성/머지된 PR | |
| **리뷰 상태 체크** | 분류 | Reviewed / Not Reviewed | |
| | 봇 제외 | `coderabbitai` 등 봇 리뷰어 제외 | `BOT_REVIEWERS_TO_IGNORE` |
| **Notion 동기화** | DB 생성 | `PR Review Status - {Sprint} - {Timestamp}` | 부모 페이지 하위에 생성 |
| | 페이지 생성 | PR별 상태 페이지 생성 | |
| **멀티 팀 지원** | `--team` 옵션 | 팀 설정에서 `notion_parent_id` 자동 로드 | NEW! |

### 3.3 Notion Database 스키마

| Property | Type | 설명 |
|----------|------|------|
| PR | title | PR 번호 + 제목 |
| Author | people | PR 작성자 |
| Repository | rich_text | 레포지토리명 |
| Reviewed | checkbox | 리뷰 완료 여부 |
| Review Count | number | 리뷰 개수 |
| Reviewers | multi_select | 리뷰어 목록 |
| Created At | date | PR 생성일 |
| PR URL | url | PR 링크 |
| Last Updated | date | 마지막 업데이트 |

---

## 4. Sprint Stats (스프린트 통계)

### 4.1 기능 개요

| 항목 | 내용 |
|------|------|
| **스크립트** | `scripts/sprint_stats.py` |
| **목적** | 사용자별 이슈/PR/리뷰 통계 수집 및 리포팅 |
| **트리거** | 스케줄 또는 수동 실행 |
| **타임아웃** | 15분 |

### 4.2 기능 명세

| 기능 | 항목 | 상세 | 비고 |
|------|------|------|------|
| **데이터 수집** | 이슈 | 스프린트 내 할당된 이슈 카운트 | Assignees 기준 |
| | PR | 스프린트 내 작성한 PR 카운트 | Author 기준 |
| | 리뷰 | 스프린트 기간 수행한 리뷰 카운트 | Reviewer 기준 |
| **사용자 매핑** | GitHub → Notion | 공통 또는 팀별 `field_mappings.yml` 매핑 사용 | |
| | 표시 이름 | 한글 이름으로 표시 | `github_to_display_name` |
| **Notion 동기화** | DB 생성 | `Sprint Statistics - {Sprint} - {Timestamp}` | |
| | 페이지 생성 | 사용자별 통계 페이지 | |
| **멀티 팀 지원** | `--team` 옵션 | 팀 설정에서 스프린트 정보 자동 로드 | NEW! |

### 4.3 Notion Database 스키마

| Property | Type | 설명 |
|----------|------|------|
| Sprint | title | 스프린트 + 사용자명 |
| User | people | Notion 사용자 |
| Issues | number | 이슈 개수 |
| PRs | number | PR 개수 |
| Reviews | number | 리뷰 개수 |
| Last Updated | date | 마지막 업데이트 |

---

## 5. Sprint Summary Sync (AI 스프린트 요약)

### 5.1 기능 개요

| 항목 | 내용 |
|------|------|
| **스크립트** | `scripts/sprint_summary_sync.py` |
| **목적** | AI 기반 스프린트 전체 작업 요약 생성 |
| **트리거** | 스케줄 또는 수동 실행 |
| **타임아웃** | 15분 |
| **AI 모델** | Claude claude-sonnet-4-20250514 |

### 5.2 기능 명세

| 기능 | 항목 | 상세 | 비고 |
|------|------|------|------|
| **데이터 수집** | 이슈 | 스프린트 이슈 + 본문 + 코멘트 | |
| | PR | 스프린트 PR + 본문 + 코멘트 | |
| | 리뷰 | 스프린트 기간 리뷰 | |
| **AI 요약** | 서술형 요약 | 3-5문장 요약 (스프린트 회고용) | |
| | 작업 트리 | 리포지토리별 완료/진행중 구분 | Mermaid 트리 형식 |
| **Notion 페이지** | 위치 | SprintChecker 페이지 하위 | 팀 설정의 `sprint_checker_parent_id` |
| | 구조 | 헤더 + 통계 + 사용자별 섹션 | |
| **멀티 팀 지원** | `--team` 옵션 | 팀 설정에서 `sprint_checker_parent_id` 자동 로드 | NEW! |

### 5.3 AI 요약 형식

**서술형 요약:**
```
이번 스프린트에서 {사용자}님은 주로 {작업영역}에 집중했습니다.
{완료된 주요 작업}을 완료했으며, 현재 {진행중인 작업}을 진행 중입니다.
```

**작업 트리:**
```
✅ 완료한 일
- [리포지토리명]
    - 완료된 작업 1 (완료)
    - 완료된 작업 2 (완료)

🔄 진행중인 일
- [리포지토리명]
    - 진행중인 작업 1 (진행중)
```

---

## 6. Daily Scrum Sync (AI 데일리 스크럼)

### 6.1 기능 개요

| 항목 | 내용 |
|------|------|
| **스크립트** | `scripts/daily_scrum_sync.py` |
| **목적** | AI 기반 일일 스크럼 요약 생성 |
| **트리거** | 스케줄 (매일 7:30 KST) 또는 수동 실행 |
| **타임아웃** | 15분 |
| **AI 모델** | Claude claude-sonnet-4-20250514 |

### 6.2 기능 명세

| 기능 | 항목 | 상세 | 비고 |
|------|------|------|------|
| **데이터 수집** | 기간 | 어제 + 오늘 (기본 2일) | `--days` 옵션 |
| | 필터링 | 활동이 있는 아이템만 | `updated_at`, `created_at`, `closed_at` 기준 |
| **AI 요약** | 서술형 요약 | 3-5문장 요약 (스크럼 미팅용) | |
| | 작업 트리 | 어제 한 일 / 오늘 할 일 구분 | |
| **Notion 페이지** | 위치 | DailyScrum 페이지 하위 | 팀 설정의 `daily_scrum_parent_id` |
| | 제목 | `Daily Scrum - {YYYY-MM-DD}` | KST 기준 |
| **멀티 팀 지원** | `--team` 옵션 | 팀 설정에서 `daily_scrum_parent_id` 자동 로드 | NEW! |

### 6.3 AI 요약 형식

**작업 트리:**
```
📌 어제 한 일
- [리포지토리명]
    - 완료된 작업 1 (완료)

📋 오늘 할 일
- [리포지토리명]
    - 진행중인 작업 1 (진행중)
```

---

## 7. 공통 기능

### 7.1 Rate Limit 처리

| 항목 | 설정 |
|------|------|
| Notion API | 3 requests/second |
| GitHub API | 5000 requests/hour |
| 배치 간 딜레이 | 1초 |
| 페이지 생성 간 딜레이 | 0.3초 |

### 7.2 에러 처리

| 상황 | 처리 |
|------|------|
| API 실패 | 최대 3회 재시도 (지수 백오프) |
| Rate Limit | 자동 대기 후 재시도 |
| 부분 실패 | 90% 이상 성공 시 전체 성공 처리 |

### 7.3 사용자 매핑

GitHub 사용자와 Notion 사용자 간 매핑은 다음 위치에서 관리합니다:

**공통 매핑:** `config/field_mappings.yml`
**팀별 매핑:** `config/teams/{team_id}/field_mappings.yml` (선택)

```yaml
github_to_notion:
  assignees:
    value_mappings:
      "github-username": "notion-user-id"

github_to_display_name:
  "github-username": "표시 이름"
```

### 7.4 봇 사용자 제외

다음 봇 사용자는 통계에서 자동 제외됩니다:
- `coderabbitai`
- `dependabot[bot]`
- `github-actions[bot]`

### 7.5 설정 우선순위 - NEW!

```
1. CLI 옵션 (--sprint, --notion-parent-id 등) - 최우선
   ↓
2. 팀 설정 (config/teams/{team}/sprint_config.yml)
   ↓
3. 레거시 설정 (config/sprint_config.yml)
   ↓
4. 환경 변수 (GH_ORG, GH_PROJECT_NUMBER 등)
```

