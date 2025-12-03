# Data Model: 멀티 팀 구조 지원

**Feature**: issue/#39-multi-team-support
**Date**: 2025-12-03

---

## 1. Entity Definitions

### 1.1 Team

회사 내 팀을 나타내는 핵심 엔티티

```python
@dataclass
class Team:
    """팀 기본 정보"""
    id: str                    # 고유 식별자 (slug), e.g., "synos"
    name: str                  # 표시 이름, e.g., "Synos"
    description: str | None    # 팀 설명 (선택)
    enabled: bool = True       # 활성화 여부
```

**Validation Rules**:
- `id`: 소문자, 숫자, 하이픈만 허용 (`^[a-z0-9-]+$`)
- `id`: 2-50자 길이
- `name`: 1-100자 길이
- `id`는 전역적으로 고유해야 함

### 1.2 GitHubConfig

팀별 GitHub 연결 설정

```python
@dataclass
class GitHubConfig:
    """GitHub 프로젝트 연결 설정"""
    org: str                   # GitHub Organization 이름
    project_number: int        # GitHub Projects v2 번호
    token_env: str = "GH_TOKEN"  # 토큰 환경변수 이름
    
    @property
    def token(self) -> str:
        """환경변수에서 토큰 로드"""
        return os.environ.get(self.token_env, "")
```

**Validation Rules**:
- `org`: 1-39자, GitHub org 이름 규칙 준수
- `project_number`: 양의 정수
- `token_env`: 유효한 환경변수 이름

### 1.3 NotionConfig

팀별 Notion 연결 설정

```python
@dataclass
class NotionConfig:
    """Notion 데이터베이스 연결 설정"""
    database_id: str           # Notion 데이터베이스 ID (32자 hex)
    token_env: str = "NOTION_TOKEN"  # 토큰 환경변수 이름
    
    @property
    def token(self) -> str:
        """환경변수에서 토큰 로드"""
        return os.environ.get(self.token_env, "")
```

**Validation Rules**:
- `database_id`: 32자 hex 문자열 (하이픈 제거 후)
- `token_env`: 유효한 환경변수 이름

### 1.4 TeamConfiguration

팀별 전체 설정을 포함하는 복합 엔티티

```python
@dataclass
class TeamConfiguration:
    """팀별 전체 설정"""
    team: Team
    github: GitHubConfig
    notion: NotionConfig
    field_mappings: dict[str, Any] | None = None  # null이면 기본값 사용
    user_mappings: dict[str, str] | None = None   # GitHub → Notion 사용자 매핑
    sync_options: TeamSyncOptions | None = None   # 동기화 옵션
```

**Relationships**:
- 1:1 Team
- 1:1 GitHubConfig
- 1:1 NotionConfig
- 0..1 field_mappings (없으면 전역 기본값)
- 0..1 user_mappings (없으면 전역 기본값)

### 1.5 TeamSyncOptions

팀별 동기화 옵션

```python
@dataclass
class TeamSyncOptions:
    """팀별 동기화 옵션"""
    batch_size: int = 100
    retry_attempts: int = 3
    retry_delay: int = 1
    exclude_archived: bool = True
    sync_interval: str | None = None  # cron 형식 (null이면 전역 설정)
```

### 1.6 TeamSyncStatus

팀별 동기화 상태 및 통계

```python
@dataclass
class TeamSyncStatus:
    """팀별 동기화 상태"""
    team_id: str
    last_sync_time: datetime | None
    last_sync_result: str | None      # "success", "partial", "failed"
    total_synced: int = 0
    items_created: int = 0
    items_updated: int = 0
    items_failed: int = 0
    errors: list[str] = field(default_factory=list)
```

### 1.7 TeamContext

서비스에서 사용하는 런타임 컨텍스트

```python
@dataclass
class TeamContext:
    """팀별 런타임 컨텍스트 (서비스 주입용)"""
    config: TeamConfiguration
    github_service: "GitHubService"
    notion_service: "NotionService"
    field_mapper: "FieldMapper"
    status: TeamSyncStatus
```

---

## 2. Configuration File Schema

### 2.1 팀 설정 파일 (YAML)

```yaml
# config/teams/{team-id}.yml

# 팀 기본 정보
team:
  id: "synos"           # required, unique
  name: "Synos"         # required
  description: "Synos 팀 GitHub-Notion 동기화"
  enabled: true         # optional, default: true

# GitHub 연결 설정
github:
  org: "ThakiCloud"               # required
  project_number: 5               # required
  token_env: "GH_TOKEN"           # optional, default: "GH_TOKEN"

# Notion 연결 설정
notion:
  database_id: "xxxxxxxx..."      # required (32자)
  token_env: "NOTION_TOKEN"       # optional, default: "NOTION_TOKEN"

# 필드 매핑 (선택적 - 없으면 전역 field_mappings.yml 사용)
field_mappings:
  # null 또는 생략하면 전역 설정 사용
  # 또는 팀별 커스텀 매핑 정의
  status:
    github_field: "Status"
    notion_property: "진행 상태"
    type: "status"
    value_mappings:
      "Epic": "시작 전"
      "Todo": "시작 전"
      "In Progress": "진행 중"
      "Done": "완료"

# 사용자 매핑 (선택적)
user_mappings:
  "github-username": "notion-user-id"
  "sylvanus4": "229d872b-594c-816d-ae7c-0002f11615c0"

# 동기화 옵션 (선택적)
sync_options:
  batch_size: 100
  retry_attempts: 3
  exclude_archived: true
```

### 2.2 Pydantic 모델 (검증용)

```python
from pydantic import BaseModel, Field, field_validator
import re

class TeamModel(BaseModel):
    id: str = Field(..., min_length=2, max_length=50)
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = None
    enabled: bool = True
    
    @field_validator('id')
    @classmethod
    def validate_team_id(cls, v: str) -> str:
        if not re.match(r'^[a-z0-9-]+$', v):
            raise ValueError('team id must contain only lowercase letters, numbers, and hyphens')
        return v

class GitHubConfigModel(BaseModel):
    org: str = Field(..., min_length=1, max_length=39)
    project_number: int = Field(..., gt=0)
    token_env: str = "GH_TOKEN"

class NotionConfigModel(BaseModel):
    database_id: str = Field(..., min_length=32, max_length=36)
    token_env: str = "NOTION_TOKEN"
    
    @field_validator('database_id')
    @classmethod
    def validate_database_id(cls, v: str) -> str:
        clean = v.replace('-', '')
        if len(clean) != 32:
            raise ValueError('database_id must be 32 hex characters')
        return clean

class TeamSyncOptionsModel(BaseModel):
    batch_size: int = Field(default=100, gt=0, le=500)
    retry_attempts: int = Field(default=3, ge=0, le=10)
    retry_delay: int = Field(default=1, ge=0, le=60)
    exclude_archived: bool = True
    sync_interval: str | None = None

class TeamConfigurationModel(BaseModel):
    team: TeamModel
    github: GitHubConfigModel
    notion: NotionConfigModel
    field_mappings: dict | None = None
    user_mappings: dict[str, str] | None = None
    sync_options: TeamSyncOptionsModel | None = None
```

---

## 3. Entity Relationships

```
┌─────────────────────────────────────────────────────────────┐
│                    TeamConfiguration                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐  ┌──────────────┐  ┌─────────────┐           │
│  │   Team   │  │ GitHubConfig │  │ NotionConfig│           │
│  │          │  │              │  │             │           │
│  │ - id     │  │ - org        │  │ - db_id     │           │
│  │ - name   │  │ - project_no │  │ - token_env │           │
│  │ - enabled│  │ - token_env  │  │             │           │
│  └──────────┘  └──────────────┘  └─────────────┘           │
│                                                              │
│  ┌──────────────────┐  ┌──────────────────────┐            │
│  │  field_mappings  │  │    user_mappings     │            │
│  │  (optional)      │  │    (optional)        │            │
│  └──────────────────┘  └──────────────────────┘            │
│                                                              │
│  ┌──────────────────┐                                       │
│  │ TeamSyncOptions  │                                       │
│  │ (optional)       │                                       │
│  └──────────────────┘                                       │
└─────────────────────────────────────────────────────────────┘
                          │
                          │ creates at runtime
                          ▼
               ┌──────────────────────┐
               │    TeamContext       │
               │                      │
               │ - config             │
               │ - github_service     │
               │ - notion_service     │
               │ - field_mapper       │
               │ - status             │
               └──────────────────────┘
                          │
                          │ tracks
                          ▼
               ┌──────────────────────┐
               │   TeamSyncStatus     │
               │                      │
               │ - team_id            │
               │ - last_sync_time     │
               │ - total_synced       │
               │ - items_created      │
               │ - items_updated      │
               │ - items_failed       │
               │ - errors             │
               └──────────────────────┘
```

---

## 4. State Transitions

### 4.1 팀 동기화 상태

```
                    ┌─────────────┐
                    │    IDLE     │
                    └──────┬──────┘
                           │ sync_start()
                           ▼
                    ┌─────────────┐
          ┌────────│  SYNCING    │────────┐
          │        └──────┬──────┘        │
          │               │               │
          │ error         │ complete      │ partial
          ▼               ▼               ▼
   ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
   │   FAILED    │ │   SUCCESS   │ │   PARTIAL   │
   └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
          │               │               │
          └───────────────┴───────────────┘
                          │ reset()
                          ▼
                    ┌─────────────┐
                    │    IDLE     │
                    └─────────────┘
```

---

## 5. Migration from Legacy

### 5.1 레거시 환경변수 → TeamConfiguration 변환

```python
def migrate_legacy_to_team_config() -> TeamConfiguration:
    """기존 환경변수를 TeamConfiguration으로 변환"""
    return TeamConfiguration(
        team=Team(
            id="legacy",
            name="Legacy (Migrated)",
            description="자동 마이그레이션된 레거시 설정"
        ),
        github=GitHubConfig(
            org=os.environ["GH_ORG"],
            project_number=int(os.environ["GH_PROJECT_NUMBER"]),
            token_env="GH_TOKEN"
        ),
        notion=NotionConfig(
            database_id=os.environ["NOTION_DB_ID"],
            token_env="NOTION_TOKEN"
        ),
        field_mappings=None,  # 전역 설정 사용
        user_mappings=None    # 전역 설정 사용
    )
```

---

## 6. Indexes and Performance

### 6.1 In-Memory Lookups

| Lookup | Data Structure | Time Complexity |
|--------|---------------|-----------------|
| Team by ID | `dict[str, TeamConfiguration]` | O(1) |
| All Teams | `list[TeamConfiguration]` | O(n) |
| Enabled Teams | Filter on load | O(n) |

### 6.2 File System

| Operation | Pattern | Notes |
|-----------|---------|-------|
| Load all teams | `config/teams/*.yml` | Glob on startup |
| Load single team | `config/teams/{id}.yml` | Direct path |
| Hot reload | File watcher (optional) | Future enhancement |

