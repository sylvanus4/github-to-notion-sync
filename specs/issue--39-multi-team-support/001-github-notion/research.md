# Research: 멀티 팀 구조 지원

**Feature**: issue/#39-multi-team-support
**Date**: 2025-12-03

---

## 1. Technical Context Resolution

### 1.1 환경변수 이름 결정 (FR-004)

**Decision**: `DEFAULT_TEAM` 사용

**Rationale**:
- 기존 환경변수 명명 규칙과 일관성 유지 (`GH_ORG`, `NOTION_DB_ID` 등)
- `SYNC_TEAM`보다 의미가 명확함 (기본 팀 지정 목적)
- 대체 팀 지정은 CLI 옵션 `--team`으로 처리

**Alternatives Considered**:
- `SYNC_TEAM`: 동기화 팀이라는 의미가 모호
- `TEAM_ID`: 기본값이라는 의미가 없음

### 1.2 일괄 동기화 방식 결정 (FR-009)

**Decision**: 순차 실행 기본, `--parallel` 옵션으로 병렬 지원

**Rationale**:
- **안정성**: 순차 실행은 리소스 경합 없이 안정적
- **디버깅 용이**: 문제 발생 시 어느 팀에서 발생했는지 추적 용이
- **선택적 병렬**: 빠른 실행이 필요한 경우 옵션으로 선택 가능

**Alternatives Considered**:
- 병렬 전용: 복잡한 오류 추적, 리소스 경합 위험
- 순차 전용: 대규모 팀에서 너무 느림

---

## 2. 기존 코드베이스 분석

### 2.1 현재 설정 구조

**src/config.py - Settings 클래스**:
```python
class Settings(BaseSettings):
    notion_token: str
    notion_db_id: str
    github_token: str
    github_org: str
    github_project_number: int
    # ... 단일 설정만 지원
```

**문제점**:
- 모든 설정이 환경변수로 하드코딩
- 팀별 분리 구조 없음
- 설정 파일(`field_mappings.yml`)이 전역으로 적용

### 2.2 현재 서비스 구조

**src/services/sync_service.py**:
- `SyncService`가 `GitHubService`, `NotionService` 직접 생성
- 팀 컨텍스트 없이 전역 설정 사용
- 통계 추적이 전역적

### 2.3 설정 파일 구조

```
config/
├── field_mappings.yml      # 전역 필드 매핑
├── sync_config.yml         # 동기화 설정 (비어있음)
├── webhook_events.yml      # 웹훅 이벤트 설정
└── sprint_config.yml       # 스프린트 설정
```

---

## 3. 설계 접근 방식

### 3.1 팀 설정 파일 구조

**결정**: `config/teams/` 디렉토리에 팀별 YAML 파일

```
config/
├── teams/
│   ├── synos.yml           # Synos 팀 설정
│   ├── cloud-infra.yml     # 클라우드인프라 팀
│   ├── ragos.yml           # RagOS 팀
│   └── ...
├── field_mappings.yml      # 기본 필드 매핑 (팀별 오버라이드 가능)
└── ...
```

**팀 설정 파일 스키마**:
```yaml
# config/teams/synos.yml
team:
  id: "synos"
  name: "Synos"
  
github:
  org: "ThakiCloud"
  project_number: 5
  token_env: "GH_TOKEN"  # 환경변수 참조

notion:
  database_id: "xxx-xxx-xxx"
  token_env: "NOTION_TOKEN"  # 환경변수 참조

field_mappings: null  # null이면 기본값 사용, 또는 커스텀 매핑

user_mappings:
  "github-user": "notion-user-id"
```

### 3.2 하위 호환성 전략

**결정**: 레거시 모드 지원

1. `config/teams/` 디렉토리가 없으면 레거시 모드 활성화
2. 레거시 모드에서는 기존 환경변수로 단일 팀 구성
3. 마이그레이션 스크립트 제공 (`scripts/migrate_to_multi_team.py`)

### 3.3 CLI 인터페이스

**결정**: Typer 기반 CLI 확장 (또는 argparse 사용)

```bash
# 기본 사용법
python -m src.main sync --team synos

# 전체 팀 동기화
python -m src.main sync --all

# 병렬 실행
python -m src.main sync --all --parallel

# 팀 목록 조회
python -m src.main teams list

# 팀 설정 검증
python -m src.main teams validate synos
```

---

## 4. 패턴 및 모범 사례

### 4.1 설정 관리 패턴

**Strategy Pattern 적용**:
- `TeamConfigLoader`: 팀 설정 로딩 전략
- `LegacyConfigLoader`: 레거시 환경변수 로딩
- `MultiTeamConfigLoader`: 멀티 팀 YAML 로딩

### 4.2 서비스 컨텍스트 패턴

**TeamContext 도입**:
```python
@dataclass
class TeamContext:
    team_id: str
    github_config: GitHubConfig
    notion_config: NotionConfig
    field_mappings: dict
    user_mappings: dict
```

각 서비스가 TeamContext를 주입받아 팀별 동작

### 4.3 에러 격리 패턴

**결정**: 팀별 try-catch로 격리

```python
for team in teams:
    try:
        sync_team(team)
    except TeamSyncError as e:
        log_error(team, e)
        continue  # 다른 팀 계속 처리
```

---

## 5. 기술 선택

### 5.1 설정 파일 형식

**Decision**: YAML (기존과 동일)

**Rationale**:
- 기존 `field_mappings.yml`과 일관성
- 사람이 읽기 쉬움
- 주석 지원

### 5.2 스키마 검증

**Decision**: Pydantic 모델

**Rationale**:
- 기존 코드에서 Pydantic 사용 중
- 타입 안전성
- 자동 문서화

### 5.3 CLI 프레임워크

**Decision**: 기존 방식 유지 (argparse 또는 직접 구현)

**Rationale**:
- 새로운 의존성 추가 최소화
- 기존 main.py 구조 확장

---

## 6. 마이그레이션 계획

### 6.1 단계별 마이그레이션

1. **Phase 1**: 멀티 팀 구조 추가 (레거시 호환)
2. **Phase 2**: Synos 팀 설정 파일 생성
3. **Phase 3**: 다른 팀 설정 추가
4. **Phase 4**: (선택) 레거시 모드 deprecation

### 6.2 롤백 전략

- 환경변수 방식 완전 지원 유지
- `config/teams/` 삭제하면 레거시 모드로 자동 전환

---

## 7. 리스크 및 완화

| 리스크 | 확률 | 영향 | 완화 방안 |
|--------|------|------|----------|
| 설정 파일 오류 | 중 | 높음 | Pydantic 검증 + 시작 시 validate |
| 레거시 호환성 깨짐 | 낮 | 높음 | 단위 테스트 + 통합 테스트 |
| 병렬 실행 경합 | 낮 | 중 | 기본 순차, 병렬은 옵션 |
| 토큰 관리 복잡성 | 중 | 중 | 환경변수 참조 방식 |

---

## 8. 결론

### NEEDS CLARIFICATION 해결 상태

| 항목 | 결정 | 상태 |
|------|------|------|
| FR-004: 환경변수 이름 | `DEFAULT_TEAM` | ✅ 해결 |
| FR-009: 일괄 동기화 방식 | 순차 기본 + `--parallel` 옵션 | ✅ 해결 |

### 다음 단계

- Phase 1로 진행: 데이터 모델 및 계약 정의

