# Tasks: 멀티 팀 구조 지원 - Daily Sprint Sync 확장

**Input**: Design documents from `/specs/issue--39-multi-team-support/001-github-notion/`
**Scope**: Daily Sprint Sync 워크플로우 및 관련 설정 파일 (MVP)
**Branch**: `issue/#39-multi-team-support`

---

## Phase 3.1: Setup - 팀별 설정 구조 (T001-T005)

- [x] **T001** Create teams config directory structure ✅
  - Action: `mkdir -p config/teams/synos config/teams/ragos`
  - Files: `config/teams/` 디렉토리 생성

- [x] **T002** Create Synos team sprint config (마이그레이션) ✅
  - File: `config/teams/synos/sprint_config.yml`
  - Action: 기존 `config/sprint_config.yml` 내용을 새 스키마로 마이그레이션
  - Include: team info, github config, notion config, sprint settings

- [x] **T003** [P] Create Synos team field mappings (복사) ✅
  - File: `config/teams/synos/field_mappings.yml`
  - Action: 기존 `config/field_mappings.yml`에서 Synos 관련 사용자 매핑 분리

- [x] **T004** [P] Create RagOS team sprint config template ✅
  - File: `config/teams/ragos/sprint_config.yml`
  - Action: RagOS 팀용 설정 템플릿 생성 (값은 TODO로 표시)

- [x] **T005** [P] Create team config template ✅
  - File: `config/teams/_template/sprint_config.yml`
  - Action: 새 팀 추가 시 참조할 템플릿 생성

---

## Phase 3.2: Tests First (TDD) - 설정 로딩 (T006-T010)

- [ ] **T006** [P] Write unit tests for team config loading
  - File: `tests/unit/test_team_config.py`
  - Test cases:
    - Load team sprint_config.yml
    - Load team field_mappings.yml (있을 때)
    - Fallback to common field_mappings.yml (없을 때)
    - Invalid YAML handling

- [ ] **T007** [P] Write unit tests for legacy mode detection
  - File: `tests/unit/test_team_config.py`
  - Test cases:
    - config/teams/ 없으면 레거시 모드
    - config/teams/ 있으면 멀티팀 모드
    - 레거시 모드에서 기존 설정 로드

- [ ] **T008** [P] Write integration tests for team-based sync
  - File: `tests/integration/test_team_sync.py`
  - Test cases:
    - `--team synos` 옵션으로 Synos 설정 로드
    - `--team ragos` 옵션으로 RagOS 설정 로드
    - 팀 미지정 시 기본 동작

- [ ] **T009** [P] Write tests for script --team option
  - File: `tests/unit/test_script_team_option.py`
  - Test cases:
    - complete_resync.py --team 파싱
    - sprint_stats.py --team 파싱
    - daily_scrum_sync.py --team 파싱

- [ ] **T010** [P] Write tests for workflow config loading
  - File: `tests/integration/test_workflow_config.py`
  - Test cases:
    - 팀 설정 파일에서 환경변수 추출
    - 올바른 Notion ID 로딩

---

## Phase 3.3: Core Implementation - 설정 로더 (T011-T014)

- [x] **T011** Create team config loader utility ✅
  - File: `src/utils/team_config.py`
  - Functions:
    - `load_team_config(team_id: str) -> TeamConfig`
    - `get_team_sprint_config(team_id: str) -> dict`
    - `get_team_field_mappings(team_id: str) -> dict`
    - `list_available_teams() -> list[str]`
    - `is_multi_team_mode() -> bool`

- [x] **T012** Create TeamConfig dataclass ✅
  - File: `src/utils/team_config.py`
  - Include:
    - team_id, team_name
    - github_org, github_project_number
    - notion_database_id
    - sprint settings (current, parent IDs)

- [x] **T013** Add fallback logic for field mappings ✅
  - File: `src/utils/team_config.py`
  - Logic:
    - `config/teams/{team}/field_mappings.yml` 확인
    - 없으면 `config/field_mappings.yml` 사용
    - 팀별 user_mappings 머지

- [x] **T014** Update src/config.py for multi-team support ✅
  - File: `src/config.py`
  - Changes:
    - Add `DEFAULT_TEAM` setting
    - Add `get_team_config(team_id)` method
    - Maintain backward compatibility

---

## Phase 3.4: Script Updates - --team 옵션 추가 (T015-T020)

- [x] **T015** Update complete_resync.py with --team option ✅
  - File: `scripts/complete_resync.py`
  - Changes:
    - Add `--team` argument
    - Load team config instead of global config
    - Set GH_ORG, GH_PROJECT_NUMBER, NOTION_DB_ID from team config

- [x] **T016** Update sprint_pr_review_check.py with --team option ✅
  - File: `scripts/sprint_pr_review_check.py`
  - Changes:
    - Add `--team` argument
    - Load notion_parent_id from team config

- [x] **T017** Update sprint_stats.py with --team option ✅
  - File: `scripts/sprint_stats.py`
  - Changes:
    - Add `--team` argument
    - Load team-specific settings

- [x] **T018** Update sprint_summary_sync.py with --team option ✅
  - File: `scripts/sprint_summary_sync.py`
  - Changes:
    - Add `--team` argument
    - Load sprint_checker_parent_id from team config

- [x] **T019** Update daily_scrum_sync.py with --team option ✅
  - File: `scripts/daily_scrum_sync.py`
  - Changes:
    - Add `--team` argument
    - Load daily_scrum_parent_id from team config

- [x] **T020** Create common script argument parser ✅
  - File: `scripts/common/team_args.py`
  - Functions:
    - `add_team_argument(parser)` - 공통 --team 인자 추가
    - `get_team_config_from_args(args)` - 인자에서 팀 설정 로드

---

## Phase 3.5: Workflow Update (T021-T024)

- [x] **T021** Update daily-sprint-sync.yml with team input ✅
  - File: `.github/workflows/daily-sprint-sync.yml`
  - Changes:
    - Add `team` input to workflow_dispatch
    - Options: '', 'synos', 'ragos', 'cloud-infra'

- [x] **T022** Update workflow config loading step ✅
  - File: `.github/workflows/daily-sprint-sync.yml`
  - Changes:
    - Check if team is specified
    - Load from `config/teams/{team}/sprint_config.yml`
    - Fallback to `config/sprint_config.yml` if no team

- [x] **T023** Update workflow environment variables ✅
  - File: `.github/workflows/daily-sprint-sync.yml`
  - Changes:
    - Set GH_ORG, GH_PROJECT_NUMBER from team config
    - Set NOTION_DB_ID from team config
    - Set sprint-related IDs from team config

- [x] **T024** Add team parameter to script calls ✅
  - File: `.github/workflows/daily-sprint-sync.yml`
  - Changes:
    - Pass `--team $TEAM` to all scripts when team is specified

---

## Phase 3.6: Polish & Documentation (T025-T028)

- [x] **T025** [P] Verify all tests pass ✅
  - Command: `make test`
  - Ensure: All unit and integration tests green

- [x] **T026** [P] Create team config migration script ✅
  - File: `scripts/migrate_to_multi_team.py`
  - Action: 기존 설정을 팀별 구조로 자동 변환

- [x] **T027** [P] Update README with multi-team usage ✅
  - File: `README.md`
  - Section: "Multi-Team Configuration"
  - Include: 팀 설정 방법, 워크플로우 사용법

- [x] **T028** [P] Update docs/daily-sprint-sync/README.md ✅
  - File: `docs/daily-sprint-sync/README.md`
  - Changes: 팀별 설정 및 워크플로우 실행 가이드

---

## Dependencies

```
Setup:      T001 → T002 → (T003, T004, T005) parallel
Tests:      T006-T010 all parallel (different files)
Config:     T011 → T012 → T013 → T014 sequential
Scripts:    T014 → T015-T019 can be parallel (different files)
            T020 should be done first if shared
Workflow:   T021 → T022 → T023 → T024 sequential (same file)
Polish:     T025-T028 parallel after all above
```

---

## Parallel Execution Examples

### Phase 3.1 Setup (partial parallel)
```
Task: "Create Synos team field mappings"
Task: "Create RagOS team sprint config template"
Task: "Create team config template"
```

### Phase 3.2 Tests (all parallel)
```
pytest tests/unit/test_team_config.py &
pytest tests/integration/test_team_sync.py &
pytest tests/unit/test_script_team_option.py &
wait
```

### Phase 3.4 Scripts (parallel after T020)
```
Task: "Update complete_resync.py with --team option"
Task: "Update sprint_pr_review_check.py with --team option"
Task: "Update sprint_stats.py with --team option"
Task: "Update sprint_summary_sync.py with --team option"
Task: "Update daily_scrum_sync.py with --team option"
```

---

## Validation Checklist

- [x] 린트 에러 수정 완료
- [x] Synos 팀 설정 파일 생성됨
- [x] `--team` 옵션 모든 스크립트에 추가됨
- [x] 워크플로우에서 팀 선택 기능 추가됨
- [ ] 실제 동작 테스트 (수동 확인 필요)

---

## Notes

- **MVP Focus**: Daily Sprint Sync 워크플로우만 우선 지원
- **Backward Compatibility**: `config/teams/` 없으면 기존 방식 동작
- **Common Config**: `config/field_mappings.yml`은 공통으로 유지, 팀별은 선택적 오버라이드

---

## Summary

| Phase | Tasks | 설명 |
|-------|-------|------|
| Setup | T001-T005 | 팀별 설정 파일 구조 생성 |
| Tests | T006-T010 | TDD - 설정 로딩 테스트 |
| Config | T011-T014 | 팀 설정 로더 구현 |
| Scripts | T015-T020 | 스크립트 --team 옵션 추가 |
| Workflow | T021-T024 | GitHub Actions 워크플로우 수정 |
| Polish | T025-T028 | 테스트 검증, 문서화 |
| **Total** | **28** | |
