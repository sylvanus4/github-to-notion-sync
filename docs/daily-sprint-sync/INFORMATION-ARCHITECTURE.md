# Information Architecture

Daily Sprint Sync 시스템의 정보 아키텍처 문서입니다.

---

## 1. 시스템 개요

### 1.1 아키텍처 목적

Daily Sprint Sync는 **GitHub Projects 중심 데이터 모델**을 기반으로 스프린트 데이터를 Notion으로 동기화하여 팀이 효율적으로 작업을 추적하고 공유할 수 있도록 설계되었습니다.

### 1.2 핵심 컨셉

```mermaid
graph TB
    subgraph "데이터 소스"
        GH[GitHub Projects]
        GHI[GitHub Issues]
        GHPR[GitHub PRs]
        GHR[GitHub Reviews]
    end

    subgraph "처리 계층"
        WF[GitHub Actions<br/>Workflow]
        SC[Python Scripts]
        AI[Claude API<br/>AI 요약]
    end

    subgraph "데이터 출력"
        NDB[Notion Database]
        NP[Notion Pages]
    end

    GH --> WF
    GHI --> SC
    GHPR --> SC
    GHR --> SC
    
    WF --> SC
    SC --> AI
    SC --> NDB
    AI --> NP

    style GH fill:#24292e,color:#fff
    style NDB fill:#000,color:#fff
    style AI fill:#d97706,color:#fff
```

### 1.3 주요 특징

- **스프린트 기반 필터링**: 모든 데이터는 스프린트 단위로 필터링
- **자동 스케줄링**: 매일 KST 07:30 자동 실행
- **AI 기반 요약**: Claude API를 활용한 지능형 요약
- **중복 방지**: GitHub Node ID 기반 중복 체크

---

## 2. 시스템 컨텍스트 다이어그램

### 2.1 C4 Level 1 - 시스템 컨텍스트

```mermaid
graph TB
    subgraph "External Systems"
        GH[("GitHub<br/>Projects API<br/>GraphQL")]
        NT[("Notion<br/>API<br/>REST")]
        CL[("Claude<br/>API<br/>Anthropic")]
    end

    subgraph "Daily Sprint Sync System"
        DSS[Daily Sprint Sync<br/>GitHub Actions + Python]
    end

    subgraph "Users"
        DEV[개발팀]
        PM[PM/스크럼마스터]
    end

    GH -->|"Project Items<br/>Issues, PRs, Reviews"| DSS
    DSS -->|"Create/Update<br/>Pages & Databases"| NT
    DSS -->|"요약 요청"| CL
    CL -->|"AI 요약 응답"| DSS

    DEV -->|"코드 작업"| GH
    PM -->|"스프린트 리뷰"| NT
    PM -->|"수동 트리거"| DSS
```

### 2.2 C4 Level 2 - 컨테이너 다이어그램

```mermaid
graph TB
    subgraph "GitHub Actions Runner"
        WF[Workflow<br/>daily-sprint-sync.yml]
    end

    subgraph "Python Scripts Container"
        CR[complete_resync.py]
        PR[sprint_pr_review_check.py]
        SS[sprint_stats.py]
        SUM[sprint_summary_sync.py]
        DS[daily_scrum_sync.py]
    end

    subgraph "Services Layer"
        GHS[GitHubService]
        NS[NotionService]
    end

    subgraph "Configuration"
        SC[sprint_config.yml]
        FM[field_mappings.yml]
    end

    WF --> CR
    WF --> PR
    WF --> SS
    WF --> SUM
    WF --> DS

    CR --> GHS
    CR --> NS
    PR --> GHS
    PR --> NS
    SS --> GHS
    SS --> NS
    SUM --> GHS
    SUM --> NS
    DS --> GHS
    DS --> NS

    SC --> WF
    FM --> GHS
    FM --> NS
```

---

## 3. 데이터 플로우

### 3.1 전체 동기화 플로우 (Complete Resync)

```mermaid
sequenceDiagram
    participant WF as Workflow
    participant CR as complete_resync.py
    participant GH as GitHub API
    participant NT as Notion API

    WF->>CR: 실행 (--sprint-filter)
    
    Note over CR: Step 0: DB 타이틀 업데이트
    CR->>NT: Update Database Title
    NT-->>CR: Success

    Note over CR: Step 1: 기존 페이지 삭제
    CR->>NT: Query All Pages
    NT-->>CR: Page List
    loop 각 페이지
        CR->>NT: Delete Page
        NT-->>CR: Deleted
    end

    Note over CR: Step 2: GitHub 데이터 동기화
    CR->>GH: Query Project Items (Sprint Filter)
    GH-->>CR: Project Items

    loop 각 아이템 (배치)
        CR->>NT: Create Page
        NT-->>CR: Created
        CR->>GH: Get Comments
        GH-->>CR: Comments
        CR->>NT: Update Page Content
    end

    CR-->>WF: 완료 통계
```

### 3.2 AI 요약 플로우 (Sprint Summary / Daily Scrum)

```mermaid
sequenceDiagram
    participant WF as Workflow
    participant SC as summary_sync.py
    participant GH as GitHub API
    participant CL as Claude API
    participant NT as Notion API

    WF->>SC: 실행 (--sprint, --notion-parent-id)
    
    Note over SC: Step 1: 데이터 수집
    SC->>GH: Query Project Items
    GH-->>SC: Items
    SC->>GH: Query PR Reviews
    GH-->>SC: Reviews

    Note over SC: Step 2: 상세 정보 수집
    loop 각 아이템
        SC->>GH: Get Body & Comments
        GH-->>SC: Details
    end

    Note over SC: Step 3: 사용자별 데이터 정리
    SC->>SC: collect_user_data()

    Note over SC: Step 4: AI 요약 생성
    loop 각 사용자
        SC->>CL: Generate Summary
        CL-->>SC: Narrative + Tree
    end

    Note over SC: Step 5: Notion 페이지 생성
    SC->>NT: Create Page (Parent)
    NT-->>SC: Page ID
    SC->>NT: Append Blocks
    NT-->>SC: Success

    SC-->>WF: 완료
```

---

## 4. 컴포넌트 아키텍처

### 4.1 모듈 구조

```mermaid
graph TB
    subgraph "Scripts Layer"
        CR[complete_resync.py]
        PR[sprint_pr_review_check.py]
        SS[sprint_stats.py]
        SUM[sprint_summary_sync.py]
        DS[daily_scrum_sync.py]
    end

    subgraph "Services Layer"
        GHS[GitHubService<br/>src/services/github_service.py]
        NS[NotionService<br/>src/services/notion_service.py]
    end

    subgraph "Models Layer"
        GM[GitHubModels<br/>src/models/github_models.py]
        NM[NotionModels<br/>src/models/notion_models.py]
    end

    subgraph "Utils Layer"
        FM[FieldMapper<br/>src/utils/mapping.py]
        LG[Logger<br/>src/utils/logger.py]
        RL[RateLimiter<br/>src/utils/rate_limiter.py]
    end

    subgraph "Config Layer"
        CFG[Config<br/>src/config.py]
        YML[YAML Files<br/>config/*.yml]
    end

    CR --> GHS
    CR --> NS
    PR --> GHS
    PR --> NS
    SS --> GHS
    SS --> NS
    SUM --> GHS
    SUM --> NS
    DS --> GHS
    DS --> NS

    GHS --> GM
    NS --> NM
    GHS --> FM
    NS --> FM

    GHS --> LG
    NS --> LG
    NS --> RL

    GHS --> CFG
    NS --> CFG
    CFG --> YML
```

### 4.2 서비스 간 의존성

```mermaid
graph LR
    subgraph "Independent"
        CFG[Config]
        LG[Logger]
    end

    subgraph "Core Services"
        GHS[GitHubService]
        NS[NotionService]
    end

    subgraph "Script Services"
        CRS[CompleteResyncService]
        PRS[SprintPRReviewService]
        SSS[SprintStatsService]
        SUMS[SprintSummarySyncService]
        DSS[DailyScrumSyncService]
    end

    CFG --> GHS
    CFG --> NS
    LG --> GHS
    LG --> NS

    GHS --> CRS
    NS --> CRS
    GHS --> PRS
    NS --> PRS
    GHS --> SSS
    NS --> SSS
    GHS --> SUMS
    NS --> SUMS
    GHS --> DSS
    NS --> DSS

    style CFG fill:#E3F2FD
    style LG fill:#E3F2FD
    style GHS fill:#4CAF50,color:#fff
    style NS fill:#4CAF50,color:#fff
```

---

## 5. 데이터 모델

### 5.1 GitHub 데이터 모델

```mermaid
erDiagram
    PROJECT ||--o{ PROJECT_ITEM : contains
    PROJECT_ITEM ||--o| ISSUE : references
    PROJECT_ITEM ||--o| PULL_REQUEST : references
    PROJECT_ITEM }|--|| SPRINT : belongs_to
    ISSUE ||--o{ COMMENT : has
    PULL_REQUEST ||--o{ COMMENT : has
    PULL_REQUEST ||--o{ REVIEW : has
    USER ||--o{ ISSUE : assigned
    USER ||--o{ PULL_REQUEST : authors
    USER ||--o{ REVIEW : submits

    PROJECT {
        string id PK
        int number
        string title
    }

    PROJECT_ITEM {
        string id PK
        string type
        string status
        string priority
        date end_date
        int estimate
    }

    SPRINT {
        string id PK
        string title
        date start_date
        int duration
    }

    ISSUE {
        string id PK
        int number
        string title
        string body
        string state
    }

    PULL_REQUEST {
        string id PK
        int number
        string title
        string body
        datetime merged_at
    }

    REVIEW {
        string id PK
        string state
        datetime submitted_at
    }

    USER {
        string login PK
        string name
    }

    COMMENT {
        string id PK
        string body
        datetime created_at
    }
```

### 5.2 Notion 출력 데이터 모델

```mermaid
erDiagram
    WORKSPACE ||--o{ PAGE : contains
    PAGE ||--o{ DATABASE : contains
    DATABASE ||--o{ PAGE : has_pages
    PAGE ||--o{ BLOCK : has_blocks

    WORKSPACE {
        string id PK
    }

    PAGE {
        string id PK
        string title
        string parent_id FK
        string type
    }

    DATABASE {
        string id PK
        string title
        json properties_schema
    }

    BLOCK {
        string id PK
        string type
        json content
    }
```

---

## 6. 워크플로우 실행 플로우

### 6.1 전체 실행 순서

```mermaid
flowchart TD
    START([시작]) --> CHECKOUT[코드 체크아웃]
    CHECKOUT --> CONFIG[설정 로드<br/>sprint_config.yml]
    CONFIG --> SETUP[Python 환경 설정]
    SETUP --> DEPS[의존성 설치]
    DEPS --> ENV[환경 변수 설정]

    ENV --> COND1{run_complete_resync?}
    COND1 -->|Yes| RESYNC[Complete Resync<br/>30분 타임아웃]
    COND1 -->|No| COND2

    RESYNC --> COND2{run_pr_review_check?}
    COND2 -->|Yes| PRCHECK[PR Review Check<br/>15분 타임아웃]
    COND2 -->|No| COND3

    PRCHECK --> COND3{run_sprint_stats?}
    COND3 -->|Yes| STATS[Sprint Stats<br/>15분 타임아웃]
    COND3 -->|No| COND4

    STATS --> COND4{run_sprint_summary?}
    COND4 -->|Yes| SUMMARY[Sprint Summary<br/>15분 타임아웃]
    COND4 -->|No| COND5

    SUMMARY --> COND5{run_daily_scrum?}
    COND5 -->|Yes| SCRUM[Daily Scrum<br/>15분 타임아웃]
    COND5 -->|No| UPLOAD

    SCRUM --> UPLOAD[Artifacts 업로드]
    UPLOAD --> END([종료])

    style RESYNC fill:#4CAF50,color:#fff
    style PRCHECK fill:#2196F3,color:#fff
    style STATS fill:#9C27B0,color:#fff
    style SUMMARY fill:#FF9800,color:#fff
    style SCRUM fill:#E91E63,color:#fff
```

### 6.2 설정 우선순위

```mermaid
flowchart LR
    subgraph "입력 우선순위"
        M[수동 입력<br/>workflow_dispatch] --> |우선| C[config 파일<br/>sprint_config.yml]
        C --> |폴백| D[기본값]
    end

    subgraph "결과"
        M --> R[SPRINT_FILTER]
        M --> N[NOTION_PARENT_ID]
        C --> R
        C --> N
    end
```

---

## 7. 상태 관리

### 7.1 동기화 상태

| 상태 | 의미 | 처리 |
|------|------|------|
| `synced` | 동기화 완료 | - |
| `pending` | 대기 중 | 다음 실행 시 처리 |
| `failed` | 실패 | 재시도 또는 로그 기록 |
| `skipped` | 스킵됨 | 필터 조건 불일치 |

### 7.2 GitHub Node ID 기반 중복 방지

```mermaid
sequenceDiagram
    participant SC as Script
    participant NS as NotionService
    participant NT as Notion DB

    SC->>NS: upsert_github_item(item)
    NS->>NT: Query by GitHub ID
    
    alt 존재함
        NT-->>NS: Existing Page
        NS->>NT: Update Properties
        NT-->>NS: Updated
    else 존재하지 않음
        NT-->>NS: Not Found
        NS->>NT: Create Page
        NT-->>NS: Created
    end

    NS-->>SC: Page Object
```

---

## 8. 요약 및 핵심 인사이트

### 8.1 핵심 IA 특징

1. **스프린트 중심 필터링**
   - 모든 데이터는 스프린트 단위로 필터링
   - `config/sprint_config.yml`에서 현재 스프린트 관리

2. **자동화된 실행**
   - 매일 KST 07:30 자동 실행 (cron: UTC 22:30)
   - 수동 트리거 지원 (workflow_dispatch)
   - 선택적 기능 실행 옵션

3. **AI 기반 요약**
   - Claude claude-sonnet-4-20250514 모델 사용
   - 서술형 요약 + 작업 트리 생성
   - 리포지토리별 그룹화

4. **Rate Limit 대응**
   - 배치 처리 (50개 단위)
   - 요청 간 딜레이 (0.3초 ~ 1초)
   - 지수 백오프 재시도

### 8.2 설계 결정사항

| 설계 영역 | 결정사항 | 이유 |
|----------|---------|------|
| **실행 시간** | KST 07:30 | 업무 시작 전 데이터 준비 |
| **배치 크기** | 50개 | Rate limit 방지 + 적절한 처리 속도 |
| **성공 기준** | 90% 이상 | 일부 실패 허용하여 전체 프로세스 안정성 확보 |
| **AI 모델** | Claude claude-sonnet-4-20250514 | 비용 대비 품질 균형 |
| **시간대** | KST (UTC+9) | 한국 팀 기준 |

### 8.3 데이터 출력 위치

| 기능 | 출력 위치 | 설정 키 |
|------|----------|---------|
| Complete Resync | 기존 Notion DB | `NOTION_DB_ID` |
| PR Review Check | PR-Checker 하위 | `notion_parent_id` |
| Sprint Stats | PR-Checker 하위 | `notion_parent_id` |
| Sprint Summary | SprintChecker 하위 | `sprint_checker_parent_id` |
| Daily Scrum | DailyScrum 하위 | `daily_scrum_parent_id` |

