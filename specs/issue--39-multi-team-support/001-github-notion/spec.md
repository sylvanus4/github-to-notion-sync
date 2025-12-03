# Feature Specification: 멀티 팀 구조 지원 - Daily Sprint Sync 워크플로우 확장

**Feature Branch**: `issue/#39-multi-team-support`
**Created**: 2025-12-03
**Updated**: 2025-12-03
**Status**: Draft
**Scope**: Daily Sprint Sync 워크플로우 및 관련 설정 파일 (MVP)

---

## 📋 Referenced Artifacts
*이 기능이 수정해야 할 기존 파일들*

| 파일 | 설명 | 변경 유형 |
|------|------|----------|
| `.github/workflows/daily-sprint-sync.yml` | Daily Sprint Sync 워크플로우 | 팀 선택 기능 추가 |
| `config/sprint_config.yml` | 스프린트 설정 (현재 Synos용) | 팀별 분리 |
| `config/field_mappings.yml` | 필드/사용자 매핑 (현재 Synos용) | 팀별 분리 (선택적) |

---

## 🎯 Scope Definition (MVP)

### ✅ 포함 (In Scope)

1. **팀별 설정 파일 구조**
   - `config/teams/{team-id}/sprint_config.yml` - 팀별 스프린트 설정
   - `config/teams/{team-id}/field_mappings.yml` - 팀별 필드 매핑 (선택적)

2. **Daily Sprint Sync 워크플로우 확장**
   - `--team` 옵션으로 특정 팀 지정
   - 워크플로우 입력에 팀 선택 추가
   - 팀별 설정 파일 로딩

3. **기존 스크립트 수정**
   - `scripts/complete_resync.py`
   - `scripts/sprint_pr_review_check.py`
   - `scripts/sprint_stats.py`
   - `scripts/sprint_summary_sync.py`
   - `scripts/daily_scrum_sync.py`

### ❌ 제외 (Out of Scope - 향후 확장)

- 새로운 CLI 인터페이스 (`src/cli.py`)
- `src/services/` 전면 리팩토링
- 웹훅 서비스 멀티팀 지원
- 실시간 동기화 멀티팀 지원

---

## ⚡ Quick Guidelines
- ✅ 기존 워크플로우 확장에 집중
- ✅ 공통 설정은 그대로 유지
- ❌ 불필요한 구조 변경 없음

---

## User Scenarios & Testing *(mandatory)*

### Primary User Story
DevOps 담당자가 GitHub Actions 워크플로우에서 팀을 선택하여 해당 팀의 Daily Sprint Sync를 실행할 수 있다.

**현재 상태**: Synos 팀 전용 설정으로 고정
**목표 상태**: 워크플로우에서 팀을 선택하면 해당 팀의 설정으로 동기화 실행

### Acceptance Scenarios

1. **Given** `config/teams/synos/sprint_config.yml` 파일이 존재할 때,
   **When** 워크플로우에서 team=synos를 선택하면,
   **Then** Synos 팀의 설정으로 Daily Sprint Sync가 실행되어야 한다.

2. **Given** `config/teams/ragos/sprint_config.yml` 파일이 존재할 때,
   **When** 워크플로우에서 team=ragos를 선택하면,
   **Then** RagOS 팀의 설정으로 Daily Sprint Sync가 실행되어야 한다.

3. **Given** 팀 설정 파일에 `field_mappings.yml`이 없을 때,
   **When** 해당 팀의 동기화를 실행하면,
   **Then** 공통 `config/field_mappings.yml`을 사용해야 한다.

4. **Given** 워크플로우에서 팀을 지정하지 않았을 때,
   **When** schedule 트리거로 실행되면,
   **Then** 모든 활성 팀에 대해 순차적으로 동기화가 실행되어야 한다.

5. **Given** 기존 환경변수 방식으로 설정된 상태에서,
   **When** `config/teams/` 디렉토리가 없으면,
   **Then** 기존 방식대로 동작해야 한다 (하위 호환성).

### Edge Cases

- **팀 설정 파일이 없는 경우**: 해당 팀 건너뛰고 경고 로그
- **필수 필드 누락**: 명확한 에러 메시지와 함께 실패
- **잘못된 Notion ID**: 연결 실패 시 해당 팀만 실패 처리

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: 팀별 스프린트 설정 파일을 지원해야 한다.
  - 위치: `config/teams/{team-id}/sprint_config.yml`
  - 필수 필드: current_sprint, notion_parent_id, sprint_checker_parent_id, daily_scrum_parent_id
  - 선택 필드: qa_database_id

- **FR-002**: 팀별 필드 매핑 설정 파일을 지원해야 한다 (선택적).
  - 위치: `config/teams/{team-id}/field_mappings.yml`
  - 없으면 공통 `config/field_mappings.yml` 사용

- **FR-003**: 워크플로우에서 팀을 선택할 수 있어야 한다.
  - workflow_dispatch 입력: team (dropdown 또는 string)
  - 기본값: 모든 팀 (schedule 트리거 시)

- **FR-004**: 기존 스크립트들이 `--team` 옵션을 지원해야 한다.
  - 영향 스크립트: complete_resync.py, sprint_pr_review_check.py, sprint_stats.py, sprint_summary_sync.py, daily_scrum_sync.py

- **FR-005**: 팀 설정 로딩 유틸리티를 제공해야 한다.
  - `config/teams/{team-id}/` 디렉토리에서 설정 로드
  - 없는 설정은 공통 설정으로 폴백

- **FR-006**: 하위 호환성을 유지해야 한다.
  - `config/teams/` 디렉토리 없으면 기존 방식 동작
  - 기존 환경변수 지원 유지

- **FR-007**: GitHub Actions 워크플로우가 팀별 환경변수를 설정해야 한다.
  - 팀 설정에서 GH_ORG, GH_PROJECT_NUMBER, NOTION_DB_ID 등 로드
  - GitHub Secrets/Variables 참조 방식 결정 필요

### Key Entities

- **TeamSprintConfig**: 팀별 스프린트 설정 (sprint_config.yml 내용)
- **TeamFieldMappings**: 팀별 필드 매핑 (field_mappings.yml 내용, 선택적)

---

## 📁 설정 파일 구조

### 현재 구조 (단일 팀)
```
config/
├── field_mappings.yml      # Synos 팀용
├── sprint_config.yml       # Synos 팀용
├── sync_config.yml
└── webhook_events.yml
```

### 목표 구조 (멀티 팀)
```
config/
├── teams/
│   ├── synos/
│   │   ├── sprint_config.yml       # Synos 스프린트 설정
│   │   └── field_mappings.yml      # (선택) Synos 필드 매핑
│   ├── ragos/
│   │   ├── sprint_config.yml       # RagOS 스프린트 설정
│   │   └── field_mappings.yml      # (선택) RagOS 필드 매핑
│   └── cloud-infra/
│       └── sprint_config.yml       # 클라우드인프라 스프린트 설정
│                                    # field_mappings.yml 없음 → 공통 사용
├── field_mappings.yml              # 공통 기본 필드 매핑 (기존 유지)
├── sprint_config.yml               # 레거시 호환용 (삭제 가능)
├── sync_config.yml                 # 공통
└── webhook_events.yml              # 공통
```

---

## 📄 팀별 설정 파일 스키마

### sprint_config.yml (팀별 필수)

```yaml
# config/teams/{team-id}/sprint_config.yml

# 팀 기본 정보
team:
  id: "synos"
  name: "Synos"

# GitHub 연결 설정
github:
  org: "ThakiCloud"
  project_number: 5
  # token은 환경변수 GH_TOKEN 사용 (공통)

# Notion 연결 설정
notion:
  database_id: "xxx..."  # 메인 동기화 DB
  # token은 환경변수 NOTION_TOKEN 사용 (공통)

# 스프린트 설정
sprint:
  current: "25-12-Sprint1"
  notion_parent_id: "2939eddc34e680f58c7ad076e5ba3e88"
  sprint_checker_parent_id: "2ba9eddc34e680ff82dad5032418ab58"
  daily_scrum_parent_id: "2ba9eddc34e6800cbb43c744a495df3f"
  qa_database_id: "27a9eddc34e68117bdb7d7af6ea38706"  # 선택
```

### field_mappings.yml (팀별 선택)

```yaml
# config/teams/{team-id}/field_mappings.yml
# 이 파일이 없으면 config/field_mappings.yml 사용

github_to_notion:
  # ... 팀별 커스텀 매핑 ...

# 팀별 사용자 매핑 (GitHub username → Notion user ID)
github_to_notion.assignees.value_mappings:
  "team-member1": "notion-user-id-1"
  "team-member2": "notion-user-id-2"
```

---

## 📋 지원 팀 목록 (초기)

| 팀 ID | 팀 이름 | 우선순위 | 비고 |
|-------|--------|----------|------|
| `synos` | Synos | 1 (MVP) | 기존 설정 마이그레이션 |
| `ragos` | RagOS | 2 | |
| `cloud-infra` | 클라우드인프라 | 3 | |
| `cloud-dev` | 클라우드개발 | - | 향후 추가 |
| `security` | 보안 | - | 향후 추가 |
| `network` | 네트워크 | - | 향후 추가 |
| `planning-design` | 기획/디자인팀 | - | 향후 추가 |

---

## 🔄 워크플로우 변경 사항

### workflow_dispatch 입력 추가

```yaml
workflow_dispatch:
  inputs:
    team:
      description: '팀 선택 (비워두면 모든 팀)'
      required: false
      type: choice
      options:
        - ''  # 모든 팀
        - synos
        - ragos
        - cloud-infra
    # ... 기존 입력들 유지 ...
```

### 팀 설정 로딩 스텝

```yaml
- name: Load team config
  id: team_config
  run: |
    TEAM="${{ github.event.inputs.team }}"
    if [ -n "$TEAM" ]; then
      # 특정 팀 설정 로드
      CONFIG_PATH="config/teams/${TEAM}/sprint_config.yml"
    else
      # 레거시 설정 사용
      CONFIG_PATH="config/sprint_config.yml"
    fi
    # ... 설정 파싱 및 환경변수 설정 ...
```

---

## Clarification Items (해결됨)

1. **환경변수 이름**: `DEFAULT_TEAM` 사용 (스크립트에서)
2. **일괄 동기화 방식**: 순차 실행 (워크플로우 job당 팀 하나씩)

---

## Review & Acceptance Checklist

### Content Quality
- [x] Scope가 명확히 정의됨 (Daily Sprint Sync 중심)
- [x] 공통 설정 유지 원칙 명시
- [x] 하위 호환성 요구사항 포함

### Requirement Completeness
- [x] 모든 [NEEDS CLARIFICATION] 해결됨
- [x] Requirements가 테스트 가능하고 명확함
- [x] 범위가 명확히 제한됨

---

## Execution Status

- [x] User description parsed
- [x] Scope narrowed to Daily Sprint Sync
- [x] Key scenarios defined
- [x] Requirements generated
- [x] Config structure defined
- [x] Review checklist passed

---
