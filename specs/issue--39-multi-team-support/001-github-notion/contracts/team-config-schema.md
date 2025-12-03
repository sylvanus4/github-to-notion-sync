# Team Configuration Schema Contract

**Feature**: issue/#39-multi-team-support
**Date**: 2025-12-03

---

## 1. File Structure

```
config/
├── teams/                      # 팀별 설정 디렉토리
│   ├── synos.yml              # Synos 팀
│   ├── cloud-infra.yml        # 클라우드인프라 팀
│   ├── cloud-dev.yml          # 클라우드개발 팀
│   ├── security.yml           # 보안 팀
│   ├── network.yml            # 네트워크 팀
│   ├── ragos.yml              # RagOS 팀
│   └── planning-design.yml    # 기획/디자인 팀
├── field_mappings.yml         # 전역 필드 매핑 (기본값)
├── sync_config.yml            # 전역 동기화 설정
└── webhook_events.yml         # 웹훅 이벤트 설정
```

---

## 2. Team Configuration Schema (YAML)

### 2.1 Full Schema

```yaml
# config/teams/{team-id}.yml
# Version: 1.0

# [REQUIRED] 팀 기본 정보
team:
  # [REQUIRED] 팀 고유 식별자
  # Pattern: ^[a-z0-9-]+$
  # Length: 2-50
  id: "synos"
  
  # [REQUIRED] 팀 표시 이름
  # Length: 1-100
  name: "Synos"
  
  # [OPTIONAL] 팀 설명
  description: "Synos 팀 GitHub-Notion 동기화 설정"
  
  # [OPTIONAL] 활성화 여부 (default: true)
  enabled: true

# [REQUIRED] GitHub 연결 설정
github:
  # [REQUIRED] GitHub Organization 이름
  # Length: 1-39
  org: "ThakiCloud"
  
  # [REQUIRED] GitHub Projects v2 번호
  # Range: > 0
  project_number: 5
  
  # [OPTIONAL] 토큰 환경변수 이름 (default: "GH_TOKEN")
  # 팀별로 다른 토큰 사용 가능
  token_env: "GH_TOKEN"

# [REQUIRED] Notion 연결 설정
notion:
  # [REQUIRED] Notion 데이터베이스 ID
  # Format: 32자 hex (하이픈 포함/미포함 모두 허용)
  database_id: "1234abcd5678efgh9012ijkl3456mnop"
  
  # [OPTIONAL] 토큰 환경변수 이름 (default: "NOTION_TOKEN")
  token_env: "NOTION_TOKEN"

# [OPTIONAL] 팀별 필드 매핑 (null이면 전역 설정 사용)
# 전역 field_mappings.yml의 구조와 동일
field_mappings:
  # 완전히 생략하거나 null로 설정하면 전역 설정 사용
  # 정의하면 전역 설정을 완전히 대체 (merge 아님)
  
  title:
    github_field: "title"
    notion_property: "피드백 제목"
    type: "title"
    required: true
  
  status:
    github_field: "Status"
    notion_property: "진행 상태"
    type: "status"
    value_mappings:
      "Epic": "시작 전"
      "Todo": "시작 전"
      "In Progress": "진행 중"
      "Done": "완료"
    default_value: "시작 전"

# [OPTIONAL] GitHub → Notion 사용자 매핑
# Key: GitHub username, Value: Notion user ID
user_mappings:
  "sylvanus4": "229d872b-594c-816d-ae7c-0002f11615c0"
  "duyeol-yu": "229d872b-594c-8104-b58b-000212f60087"

# [OPTIONAL] 팀별 동기화 옵션
sync_options:
  # 배치 크기 (default: 100, range: 1-500)
  batch_size: 100
  
  # 재시도 횟수 (default: 3, range: 0-10)
  retry_attempts: 3
  
  # 재시도 지연 (초) (default: 1, range: 0-60)
  retry_delay: 1
  
  # 아카이브된 항목 제외 (default: true)
  exclude_archived: true
  
  # 동기화 간격 (cron 형식, null이면 전역 설정)
  sync_interval: null
```

### 2.2 Minimal Schema (필수 필드만)

```yaml
# config/teams/example.yml
# 최소 필수 설정

team:
  id: "example"
  name: "Example Team"

github:
  org: "ThakiCloud"
  project_number: 10

notion:
  database_id: "1234abcd5678efgh9012ijkl3456mnop"
```

---

## 3. JSON Schema (검증용)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "TeamConfiguration",
  "type": "object",
  "required": ["team", "github", "notion"],
  "properties": {
    "team": {
      "type": "object",
      "required": ["id", "name"],
      "properties": {
        "id": {
          "type": "string",
          "pattern": "^[a-z0-9-]+$",
          "minLength": 2,
          "maxLength": 50
        },
        "name": {
          "type": "string",
          "minLength": 1,
          "maxLength": 100
        },
        "description": {
          "type": ["string", "null"]
        },
        "enabled": {
          "type": "boolean",
          "default": true
        }
      }
    },
    "github": {
      "type": "object",
      "required": ["org", "project_number"],
      "properties": {
        "org": {
          "type": "string",
          "minLength": 1,
          "maxLength": 39
        },
        "project_number": {
          "type": "integer",
          "minimum": 1
        },
        "token_env": {
          "type": "string",
          "default": "GH_TOKEN"
        }
      }
    },
    "notion": {
      "type": "object",
      "required": ["database_id"],
      "properties": {
        "database_id": {
          "type": "string",
          "minLength": 32,
          "maxLength": 36
        },
        "token_env": {
          "type": "string",
          "default": "NOTION_TOKEN"
        }
      }
    },
    "field_mappings": {
      "type": ["object", "null"]
    },
    "user_mappings": {
      "type": ["object", "null"],
      "additionalProperties": {
        "type": "string"
      }
    },
    "sync_options": {
      "type": ["object", "null"],
      "properties": {
        "batch_size": {
          "type": "integer",
          "minimum": 1,
          "maximum": 500,
          "default": 100
        },
        "retry_attempts": {
          "type": "integer",
          "minimum": 0,
          "maximum": 10,
          "default": 3
        },
        "retry_delay": {
          "type": "integer",
          "minimum": 0,
          "maximum": 60,
          "default": 1
        },
        "exclude_archived": {
          "type": "boolean",
          "default": true
        },
        "sync_interval": {
          "type": ["string", "null"]
        }
      }
    }
  }
}
```

---

## 4. Validation Rules

### 4.1 팀 ID 규칙

- 소문자, 숫자, 하이픈만 허용
- 시작은 소문자 또는 숫자
- 연속 하이픈 불가 (`--`)
- 끝은 하이픈 불가
- 예약어 불가: `all`, `default`, `legacy`, `none`

### 4.2 데이터베이스 ID 규칙

- 32자 hex 문자열
- 하이픈 포함 형식도 허용 (자동 제거)
- 예: `1234abcd-5678-efgh-9012-ijkl3456mnop` → `1234abcd5678efgh9012ijkl3456mnop`

### 4.3 중복 검사

- 팀 ID는 전역적으로 고유해야 함
- 같은 Notion database_id에 여러 팀 연결 시 경고 (허용)
- 같은 GitHub project에 여러 팀 연결 시 경고 (허용)

---

## 5. Migration from Legacy

### 5.1 자동 감지

시스템 시작 시:
1. `config/teams/` 디렉토리 존재 여부 확인
2. 있으면: 멀티 팀 모드
3. 없으면: 레거시 모드 (환경변수 사용)

### 5.2 레거시 환경변수 매핑

| 환경변수 | 팀 설정 필드 |
|----------|-------------|
| `GH_ORG` | `github.org` |
| `GH_PROJECT_NUMBER` | `github.project_number` |
| `GH_TOKEN` | `github.token_env` (값 아님) |
| `NOTION_DB_ID` | `notion.database_id` |
| `NOTION_TOKEN` | `notion.token_env` (값 아님) |

### 5.3 마이그레이션 스크립트

```bash
# 레거시 → 멀티 팀 변환
python scripts/migrate_to_multi_team.py

# 결과
# config/teams/legacy.yml 생성
# 기존 환경변수 기반 설정 마이그레이션
```

