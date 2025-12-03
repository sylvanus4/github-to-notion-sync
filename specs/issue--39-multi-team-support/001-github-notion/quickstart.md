# Quickstart: 멀티 팀 구조 설정 가이드

**Feature**: issue/#39-multi-team-support
**Date**: 2025-12-03

---

## 🚀 빠른 시작

### 1단계: 팀 설정 디렉토리 생성

```bash
mkdir -p config/teams
```

### 2단계: 팀 설정 파일 생성

#### Synos 팀 (기존 설정 마이그레이션)

```bash
cat > config/teams/synos.yml << 'EOF'
team:
  id: "synos"
  name: "Synos"
  description: "Synos 팀 GitHub-Notion 동기화"

github:
  org: "ThakiCloud"
  project_number: 5

notion:
  database_id: "YOUR_NOTION_DATABASE_ID"

# 기존 field_mappings.yml 사용
field_mappings: null

# 기존 사용자 매핑 사용
user_mappings:
  "sylvanus4": "229d872b-594c-816d-ae7c-0002f11615c0"
  "duyeol-yu": "229d872b-594c-8104-b58b-000212f60087"
EOF
```

#### RagOS 팀 (새 팀 추가 예시)

```bash
cat > config/teams/ragos.yml << 'EOF'
team:
  id: "ragos"
  name: "RagOS"
  description: "RagOS 팀 GitHub-Notion 동기화"

github:
  org: "ThakiCloud"
  project_number: 10  # RagOS 팀의 GitHub 프로젝트 번호

notion:
  database_id: "YOUR_RAGOS_NOTION_DATABASE_ID"
EOF
```

### 3단계: 환경변수 설정

```bash
# .env 파일
export GH_TOKEN="ghp_your_github_token"
export NOTION_TOKEN="secret_your_notion_token"
export DEFAULT_TEAM="synos"  # 기본 팀 (선택)
```

### 4단계: 설정 검증

```bash
# 모든 팀 설정 검증
python -m src.main teams validate

# 특정 팀 설정 검증
python -m src.main teams validate synos
```

예상 출력:
```
✅ synos: 설정 유효
  ├── GitHub 연결: OK (ThakiCloud/Project #5)
  ├── Notion 연결: OK (database accessible)
  └── 필드 매핑: OK (10 fields mapped)

✅ ragos: 설정 유효
  ├── GitHub 연결: OK (ThakiCloud/Project #10)
  ├── Notion 연결: OK (database accessible)
  └── 필드 매핑: OK (default mappings)
```

### 5단계: 동기화 실행

```bash
# 특정 팀 동기화
python -m src.main sync --team synos

# 모든 팀 동기화
python -m src.main sync --all

# 시뮬레이션 (변경 없이)
python -m src.main sync --team synos --dry-run
```

---

## 📋 팀 목록 확인

```bash
python -m src.main teams list
```

예상 출력:
```
┌───────────────┬──────────────────┬─────────┬─────────────────┐
│ ID            │ Name             │ Enabled │ Last Sync       │
├───────────────┼──────────────────┼─────────┼─────────────────┤
│ synos         │ Synos            │ ✓       │ 2025-12-03 10:00│
│ ragos         │ RagOS            │ ✓       │ -               │
│ cloud-infra   │ 클라우드인프라    │ ✓       │ -               │
└───────────────┴──────────────────┴─────────┴─────────────────┘
```

---

## 🏢 전체 팀 설정 예시

### 기획/디자인팀
```yaml
# config/teams/planning-design.yml
team:
  id: "planning-design"
  name: "기획/디자인팀"

github:
  org: "ThakiCloud"
  project_number: 11

notion:
  database_id: "planning_design_db_id"
```

### 클라우드인프라
```yaml
# config/teams/cloud-infra.yml
team:
  id: "cloud-infra"
  name: "클라우드인프라"

github:
  org: "ThakiCloud"
  project_number: 12

notion:
  database_id: "cloud_infra_db_id"
```

### 클라우드개발
```yaml
# config/teams/cloud-dev.yml
team:
  id: "cloud-dev"
  name: "클라우드개발"

github:
  org: "ThakiCloud"
  project_number: 13

notion:
  database_id: "cloud_dev_db_id"
```

### 보안팀
```yaml
# config/teams/security.yml
team:
  id: "security"
  name: "보안"

github:
  org: "ThakiCloud"
  project_number: 14

notion:
  database_id: "security_db_id"
```

### 네트워크팀
```yaml
# config/teams/network.yml
team:
  id: "network"
  name: "네트워크"

github:
  org: "ThakiCloud"
  project_number: 15

notion:
  database_id: "network_db_id"
```

---

## ✅ 검증 체크리스트

### 기본 설정 확인

- [ ] `config/teams/` 디렉토리 생성됨
- [ ] 최소 1개 이상의 팀 설정 파일 존재
- [ ] `GH_TOKEN` 환경변수 설정됨
- [ ] `NOTION_TOKEN` 환경변수 설정됨

### 팀별 확인

각 팀에 대해:
- [ ] GitHub Organization 접근 가능
- [ ] GitHub Project 번호 유효
- [ ] Notion Database ID 유효
- [ ] Notion Database 접근 권한 있음

### 동기화 테스트

```bash
# 1. 검증
python -m src.main teams validate

# 2. 드라이런
python -m src.main sync --team YOUR_TEAM --dry-run

# 3. 실제 동기화
python -m src.main sync --team YOUR_TEAM
```

---

## 🔄 레거시 마이그레이션

기존 단일 팀 설정에서 마이그레이션:

```bash
# 자동 마이그레이션 스크립트
python scripts/migrate_to_multi_team.py

# 수동 마이그레이션:
# 1. 기존 환경변수 확인
echo $GH_ORG
echo $GH_PROJECT_NUMBER
echo $NOTION_DB_ID

# 2. 팀 설정 파일 생성 (위 예시 참조)
# 3. 검증
python -m src.main teams validate
```

---

## ❓ 문제 해결

### "Team not found" 오류

```bash
# 팀 목록 확인
python -m src.main teams list

# 설정 파일 위치 확인
ls -la config/teams/
```

### "Connection failed" 오류

```bash
# 환경변수 확인
echo $GH_TOKEN
echo $NOTION_TOKEN

# 토큰 권한 확인
gh auth status
```

### "Invalid database ID" 오류

```bash
# Notion 데이터베이스 ID 확인
# URL에서: https://notion.so/workspace/DATABASE_ID?v=VIEW_ID
# DATABASE_ID 부분 (32자 hex)
```

