# CLI Interface Contract

**Feature**: issue/#39-multi-team-support
**Date**: 2025-12-03

---

## 1. Command Structure

### 1.1 Root Command

```bash
python -m src.main [OPTIONS] COMMAND [ARGS]...
```

### 1.2 Global Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--team`, `-t` | string | `$DEFAULT_TEAM` | 대상 팀 ID |
| `--config-dir` | path | `config/` | 설정 디렉토리 경로 |
| `--log-level` | enum | `INFO` | 로그 레벨 (DEBUG, INFO, WARNING, ERROR) |
| `--help`, `-h` | flag | - | 도움말 표시 |

---

## 2. Commands

### 2.1 `sync` - 동기화 실행

```bash
python -m src.main sync [OPTIONS]
```

**Options**:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--team`, `-t` | string | `$DEFAULT_TEAM` | 대상 팀 ID |
| `--all`, `-a` | flag | false | 모든 활성 팀 동기화 |
| `--parallel`, `-p` | flag | false | 병렬 실행 (--all과 함께 사용) |
| `--batch-size` | int | 100 | 배치 크기 |
| `--dry-run` | flag | false | 실제 변경 없이 시뮬레이션 |

**Examples**:

```bash
# 특정 팀 동기화
python -m src.main sync --team synos

# 모든 팀 순차 동기화
python -m src.main sync --all

# 모든 팀 병렬 동기화
python -m src.main sync --all --parallel

# 시뮬레이션 실행
python -m src.main sync --team synos --dry-run
```

**Exit Codes**:

| Code | Meaning |
|------|---------|
| 0 | 성공 |
| 1 | 일반 오류 |
| 2 | 설정 오류 |
| 3 | 연결 오류 (GitHub/Notion) |
| 4 | 부분 실패 (일부 팀 실패) |

**Output Format**:

```json
{
  "success": true,
  "team": "synos",
  "duration_seconds": 12.5,
  "total_items": 150,
  "created": 5,
  "updated": 10,
  "failed": 0,
  "errors": []
}
```

---

### 2.2 `teams` - 팀 관리

#### 2.2.1 `teams list` - 팀 목록 조회

```bash
python -m src.main teams list [OPTIONS]
```

**Options**:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--all` | flag | false | 비활성 팀 포함 |
| `--format` | enum | `table` | 출력 형식 (table, json, yaml) |

**Output (table)**:

```
┌───────────────┬──────────────────┬─────────┬─────────────────┐
│ ID            │ Name             │ Enabled │ Last Sync       │
├───────────────┼──────────────────┼─────────┼─────────────────┤
│ synos         │ Synos            │ ✓       │ 2025-12-03 10:00│
│ cloud-infra   │ 클라우드인프라    │ ✓       │ -               │
│ ragos         │ RagOS            │ ✓       │ 2025-12-02 15:30│
└───────────────┴──────────────────┴─────────┴─────────────────┘
```

**Output (json)**:

```json
{
  "teams": [
    {
      "id": "synos",
      "name": "Synos",
      "enabled": true,
      "last_sync": "2025-12-03T10:00:00Z"
    }
  ]
}
```

#### 2.2.2 `teams validate` - 팀 설정 검증

```bash
python -m src.main teams validate [TEAM_ID]
```

**Arguments**:

| Argument | Required | Description |
|----------|----------|-------------|
| TEAM_ID | No | 검증할 팀 ID (없으면 전체 검증) |

**Output**:

```
✅ synos: 설정 유효
  ├── GitHub 연결: OK (ThakiCloud/Project #5)
  ├── Notion 연결: OK (database accessible)
  └── 필드 매핑: OK (10 fields mapped)

❌ cloud-infra: 설정 오류
  └── Notion 연결: FAILED (Invalid database ID)
```

**Exit Codes**:

| Code | Meaning |
|------|---------|
| 0 | 모든 팀 검증 성공 |
| 1 | 하나 이상의 팀 검증 실패 |

#### 2.2.3 `teams show` - 팀 상세 정보

```bash
python -m src.main teams show TEAM_ID
```

**Output**:

```yaml
team:
  id: synos
  name: Synos
  enabled: true

github:
  org: ThakiCloud
  project_number: 5
  
notion:
  database_id: abc123...
  
sync_status:
  last_sync: 2025-12-03T10:00:00Z
  total_synced: 150
  last_result: success
```

---

### 2.3 `status` - 동기화 상태 조회

```bash
python -m src.main status [OPTIONS]
```

**Options**:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--team`, `-t` | string | all | 대상 팀 ID |
| `--format` | enum | `table` | 출력 형식 |

**Output**:

```
┌───────────┬─────────┬─────────────────┬─────────┬─────────┬────────┐
│ Team      │ Status  │ Last Sync       │ Created │ Updated │ Failed │
├───────────┼─────────┼─────────────────┼─────────┼─────────┼────────┤
│ synos     │ ✓ OK    │ 2025-12-03 10:00│ 5       │ 10      │ 0      │
│ ragos     │ ✓ OK    │ 2025-12-02 15:30│ 3       │ 7       │ 1      │
│ cloud-dev │ ⚠ WARN  │ -               │ -       │ -       │ -      │
└───────────┴─────────┴─────────────────┴─────────┴─────────┴────────┘
```

---

## 3. Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DEFAULT_TEAM` | No | - | 기본 팀 ID |
| `GH_TOKEN` | Yes | - | GitHub API 토큰 |
| `NOTION_TOKEN` | Yes | - | Notion API 토큰 |
| `CONFIG_DIR` | No | `config/` | 설정 디렉토리 |
| `LOG_LEVEL` | No | `INFO` | 로그 레벨 |

---

## 4. Configuration Priority

설정 우선순위 (높은 것이 낮은 것을 오버라이드):

1. CLI 옵션 (`--team`, `--batch-size`)
2. 환경변수 (`DEFAULT_TEAM`)
3. 팀 설정 파일 (`config/teams/{team}.yml`)
4. 전역 설정 파일 (`config/field_mappings.yml`)
5. 하드코딩된 기본값

---

## 5. Error Messages

### 5.1 설정 오류

```
Error: Team 'unknown-team' not found.
Available teams: synos, ragos, cloud-infra

Hint: Use 'python -m src.main teams list' to see all teams.
```

### 5.2 연결 오류

```
Error: GitHub connection failed for team 'synos'.
Reason: Invalid token or insufficient permissions.

Hint: Check GH_TOKEN environment variable.
```

### 5.3 동기화 오류

```
Warning: Partial sync completed for team 'synos'.
- 145/150 items synced successfully
- 5 items failed (see errors below)

Errors:
  - Item #123: Notion rate limit exceeded
  - Item #456: Invalid field mapping for 'Status'
```

