# Implementation Plan: 멀티 팀 구조 지원 - Daily Sprint Sync 확장

**Branch**: `issue/#39-multi-team-support` | **Date**: 2025-12-03 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/issue--39-multi-team-support/001-github-notion/spec.md`
**Scope**: Daily Sprint Sync 워크플로우 및 관련 설정 파일 (MVP)

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path → ✅ Complete
2. Fill Technical Context → ✅ Complete
3. Fill the Constitution Check section → ✅ Complete
4. Evaluate Constitution Check section → ✅ Complete
5. Execute Phase 0 → research.md → ✅ Complete
6. Execute Phase 1 → contracts, data-model.md, quickstart.md → ✅ Complete
7. Re-evaluate Constitution Check section → ✅ Complete
8. Plan Phase 2 → Describe task generation approach → ✅ Complete
9. STOP - Ready for /tasks command
```

---

## Summary

**Primary Requirement**: Daily Sprint Sync 워크플로우가 팀별로 동작할 수 있도록 설정 구조 확장

**MVP Scope**:
- `.github/workflows/daily-sprint-sync.yml` - 팀 선택 기능 추가
- `config/teams/{team-id}/sprint_config.yml` - 팀별 스프린트 설정
- `config/teams/{team-id}/field_mappings.yml` - 팀별 필드 매핑 (선택적)
- 기존 스크립트에 `--team` 옵션 추가

**Technical Approach**: 
- `config/teams/` 디렉토리에 팀별 설정 파일
- 공통 설정은 `config/field_mappings.yml` 유지
- 워크플로우에서 팀 선택 시 해당 팀 설정 로드
- 기존 방식 하위 호환성 유지

---

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: 
- pydantic, pydantic-settings (설정 검증)
- PyYAML (설정 파일 파싱)
- notion-client (Notion API)
- requests (GitHub API)

**Storage**: YAML 파일 기반 설정 (`config/teams/*.yml`)
**Testing**: pytest, pytest-asyncio
**Target Platform**: Linux/macOS (CLI 도구)
**Project Type**: single (Python CLI + webhook server)

**Performance Goals**: 
- 팀 설정 로딩: <100ms
- 팀별 동기화 시작: <1s
- 전체 팀 순차 동기화: 팀 수 × 개별 동기화 시간

**Constraints**:
- 기존 환경변수 방식 하위 호환성 필수
- 새 팀 추가 시 코드 수정 없이 설정 파일만 추가
- 팀 간 동기화 독립성 보장

**Scale/Scope**: 7-10개 팀, 팀당 100-500개 이슈

---

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Data Structure First (Principle I)
- [x] N/A - This is a new feature (기존 DB 스키마 변경 없음)
- [x] Entity relationships and constraints documented? → `data-model.md` 참조
- [x] Performance implications assessed → In-memory dict O(1) lookup

### API Contracts (Principle IV)
- [x] CLI interface defined in `contracts/cli-interface.md`
- [x] Configuration schema defined in `contracts/team-config-schema.md`
- [x] Request/response schemas validated at boundaries (Pydantic)
- [x] Error envelope follows standard format

### Test-Driven Change Management (Principle VII)
- [ ] Tests written BEFORE implementation → /tasks에서 TDD 순서로 생성
- [x] Test pyramid followed (unit > integration > e2e)
- [ ] All tests currently FAILING → 구현 전 테스트 작성 예정

### Security by Default (Principle VI)
- [x] Authentication/authorization requirements identified → 기존 토큰 방식 유지
- [x] Input validation beyond schema → Pydantic validator 정의됨
- [x] Secrets management strategy defined → 환경변수 참조 방식 (토큰 직접 저장 안함)
- [x] Rate limiting requirements documented → 기존 rate limiter 재사용

### Multi-Language Standards (Principle III)
- [x] **Python**: Pydantic models for validation ✅
- [N/A] **TypeScript**: Not applicable
- [N/A] **Go**: Not applicable

### Kubernetes Native (Principle V - if applicable)
- [x] N/A - No Kubernetes resources (로컬 CLI 도구)

### Monorepo Consistency (Principle II - if applicable)
- [x] N/A - Single project

---

**Violations & Justifications**: None

---

## Project Structure

### Documentation (this feature)
```
specs/issue--39-multi-team-support/001-github-notion/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output ✅
├── data-model.md        # Phase 1 output ✅
├── quickstart.md        # Phase 1 output ✅
├── contracts/           # Phase 1 output ✅
│   ├── cli-interface.md
│   └── team-config-schema.md
└── tasks.md             # Phase 2 output (/tasks command)
```

### Source Code (repository root)
```
src/
├── utils/
│   └── team_config.py        # NEW: 팀 설정 로더
├── config.py                 # MODIFY: DEFAULT_TEAM 추가

scripts/
├── common/
│   └── team_args.py          # NEW: 공통 --team 인자 처리
├── complete_resync.py        # MODIFY: --team 옵션 추가
├── sprint_pr_review_check.py # MODIFY: --team 옵션 추가
├── sprint_stats.py           # MODIFY: --team 옵션 추가
├── sprint_summary_sync.py    # MODIFY: --team 옵션 추가
├── daily_scrum_sync.py       # MODIFY: --team 옵션 추가
└── migrate_to_multi_team.py  # NEW: 마이그레이션 스크립트

config/
├── teams/                    # NEW: 팀별 설정
│   ├── synos/
│   │   ├── sprint_config.yml
│   │   └── field_mappings.yml (선택)
│   ├── ragos/
│   │   └── sprint_config.yml
│   └── _template/
│       └── sprint_config.yml
├── field_mappings.yml        # KEEP: 공통 기본 필드 매핑
├── sprint_config.yml         # KEEP: 레거시 호환용
└── ...

.github/workflows/
└── daily-sprint-sync.yml     # MODIFY: 팀 선택 기능 추가

tests/
├── unit/
│   ├── test_team_config.py   # NEW
│   └── test_script_team_option.py  # NEW
└── integration/
    ├── test_team_sync.py     # NEW
    └── test_workflow_config.py  # NEW
```

**Structure Decision**: 기존 구조 최소 변경. 설정 파일 구조 확장에 집중.

---

## Phase 0: Outline & Research

✅ **Complete** - See [research.md](./research.md)

**Key Decisions**:
1. 환경변수 이름: `DEFAULT_TEAM`
2. 일괄 동기화: 순차 기본, `--parallel` 옵션
3. 설정 파일 형식: YAML
4. 하위 호환성: 레거시 모드 자동 감지

---

## Phase 1: Design & Contracts

✅ **Complete**

### Generated Artifacts:

1. **data-model.md**: 
   - Team, GitHubConfig, NotionConfig, TeamConfiguration 엔티티
   - Pydantic 검증 모델
   - 상태 전이 다이어그램

2. **contracts/cli-interface.md**:
   - `sync`, `teams list`, `teams validate`, `status` 명령어
   - 옵션, 환경변수, 종료 코드 정의

3. **contracts/team-config-schema.md**:
   - 팀 설정 YAML 스키마
   - JSON Schema (검증용)
   - 마이그레이션 가이드

4. **quickstart.md**:
   - 5단계 빠른 시작 가이드
   - 팀 설정 예시
   - 검증 체크리스트

---

## Affected Spec Areas

*이 기능은 새 프로젝트 구조를 추가하므로 기존 spec 파일 업데이트 불필요*

```yaml
service: github-to-notion-sync
structure: single-file
files:
  - path: README.md
    reason: "멀티 팀 사용법 문서화"
    changes: "Quick Start에 팀 설정 가이드 추가, CLI 사용법 업데이트"
  - path: docs/SETUP.md
    reason: "설정 가이드 업데이트"
    changes: "멀티 팀 설정 섹션 추가, 마이그레이션 가이드"
```

---

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- TDD 순서: 테스트 먼저, 구현 나중
- 의존성 순서: 모델 → 서비스 → CLI → 통합

**Estimated Tasks** (~25-30):

1. **모델 계층** (5 tasks)
   - [P] Team 모델 + 테스트
   - [P] GitHubConfig 모델 + 테스트
   - [P] NotionConfig 모델 + 테스트
   - [P] TeamConfiguration 모델 + 테스트
   - [P] TeamContext 모델 + 테스트

2. **서비스 계층** (8 tasks)
   - TeamConfigLoader 인터페이스 정의
   - MultiTeamConfigLoader 구현 + 테스트
   - LegacyConfigLoader 구현 + 테스트
   - TeamService 구현 + 테스트
   - SyncService TeamContext 리팩토링
   - GitHubService TeamContext 지원
   - NotionService TeamContext 지원

3. **CLI 계층** (6 tasks)
   - CLI 엔트리포인트 구조
   - `sync` 명령어 + 테스트
   - `teams list` 명령어 + 테스트
   - `teams validate` 명령어 + 테스트
   - `teams show` 명령어 + 테스트
   - `status` 명령어 + 테스트

4. **통합** (5 tasks)
   - 기존 main.py 통합
   - 레거시 호환성 테스트
   - 전체 팀 동기화 테스트
   - 마이그레이션 스크립트
   - 문서 업데이트

**Ordering Strategy**:
- [P] 표시: 병렬 실행 가능 (독립 파일)
- 모델 완료 후 서비스
- 서비스 완료 후 CLI
- CLI 완료 후 통합

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

---

## Progress Tracking
*This checklist is updated during execution flow*

**Phase Status**:
- [x] Phase 0: Research complete (/plan command)
- [x] Phase 1: Design complete (/plan command)
- [x] Phase 2: Task planning complete (/plan command - describe approach only)
- [x] Phase 3: Tasks generated (/tasks command) - 49 tasks created
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS
- [x] Post-Design Constitution Check: PASS
- [x] All NEEDS CLARIFICATION resolved
- [x] Complexity deviations documented (None)

---
*Based on Constitution v2.0.0 - See `.specify/memory/constitution.md`*

