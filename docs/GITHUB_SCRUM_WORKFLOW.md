# GitHub Scrum Workflow Guide

**Version: 1.0**

GitHub Project와 Notion Database 간의 동기화를 위한 워크플로우 가이드입니다.

## 목차

1. [개요](#개요)
2. [complete_resync.py 사용법](#complete_resyncpy-사용법)
3. [담당자 매핑](#담당자-매핑)
4. [스프린트 기반 동기화](#스프린트-기반-동기화)
5. [문제 해결](#문제-해결)

## 개요

이 시스템은 GitHub Project의 Issues와 Pull Requests를 Notion Database로 동기화하여 팀의 스크럼 프로세스를 지원합니다.

### 주요 기능

- **완전 동기화**: GitHub Project의 모든 항목을 Notion으로 동기화
- **스프린트 필터링**: 특정 스프린트의 항목만 선별적으로 동기화
- **담당자 매핑**: GitHub 사용자명을 한국어 이름으로 자동 변환
- **상태 매핑**: GitHub 상태를 Notion 상태로 자동 변환
- **우선순위 매핑**: GitHub Priority를 Notion 우선순위로 변환

## complete_resync.py 사용법

### 기본 명령어

```bash
# 전체 동기화 (확인 프롬프트 포함)
PYTHONPATH=. python scripts/complete_resync.py

# Dry-run (실제 변경 없이 확인만)
PYTHONPATH=. python scripts/complete_resync.py --dry-run

# 강제 실행 (확인 프롬프트 없이)
PYTHONPATH=. python scripts/complete_resync.py --force

# 조용한 모드 (에러만 출력)
PYTHONPATH=. python scripts/complete_resync.py --quiet
```

### 스프린트 필터링

특정 스프린트의 항목만 동기화:

```bash
# 25-07-Sprint4 스프린트만 동기화
PYTHONPATH=. python scripts/complete_resync.py --sprint-filter "25-07-Sprint4"

# Dry-run으로 스프린트 항목 확인
PYTHONPATH=. python scripts/complete_resync.py --sprint-filter "25-07-Sprint4" --dry-run

# 강제 실행으로 스프린트 동기화
PYTHONPATH=. python scripts/complete_resync.py --sprint-filter "25-07-Sprint4" --force
```

### 배치 크기 조정

대량의 항목을 처리할 때 배치 크기를 조정할 수 있습니다:

```bash
# 배치 크기를 10으로 설정 (기본값: 50)
PYTHONPATH=. python scripts/complete_resync.py --batch-size 10
```

### 명령어 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--dry-run` | 실제 변경 없이 분석만 수행 | False |
| `--force` | 확인 프롬프트 없이 실행 | False |
| `--quiet` | 에러 메시지만 출력 | False |
| `--batch-size N` | 배치 처리 크기 설정 | 50 |
| `--sprint-filter "NAME"` | 특정 스프린트만 필터링 | 모든 항목 |

### 실행 예시

#### 1. 안전한 테스트 실행

```bash
# 먼저 dry-run으로 확인
PYTHONPATH=. python scripts/complete_resync.py --sprint-filter "25-07-Sprint4" --dry-run

# 결과가 만족스러우면 실제 실행
PYTHONPATH=. python scripts/complete_resync.py --sprint-filter "25-07-Sprint4" --force
```

#### 2. 전체 프로젝트 동기화

```bash
# 경고: 모든 기존 Notion 페이지가 삭제됩니다!
PYTHONPATH=. python scripts/complete_resync.py --force
```

#### 3. 배치 크기 조정하여 실행

```bash
# 느린 네트워크나 대량 데이터시 사용
PYTHONPATH=. python scripts/complete_resync.py --batch-size 10 --sprint-filter "25-07-Sprint4"
```

## 담당자 매핑

**✅ 성공적으로 구현됨 (2025-07-29)**

GitHub 사용자명을 실제 Notion 워크스페이스 사용자로 자동 매핑합니다.

### 현재 매핑 테이블

| GitHub 사용자명 | Notion 사용자 | 사용자 ID |
|----------------|--------------|-----------|
| duyeol-yu | 유두열 | `229d872b-594c-8104-b58b-000212f60087` |
| jaehoonkim | Jae-Hoon Kim (김재훈) | `229d872b-594c-8150-879d-00022f27519e` |
| sylvanus4 | HJ (한효정) | `229d872b-594c-816d-ae7c-0002f11615c0` |
| thaki-yakhyo | yakhyo | `23ed872b-594c-811f-8e2f-0002687c8ce2` |
| thakicloud-jotaeyang | 조태양 | `229d872b-594c-81b5-906f-00020b52c301` |
| yunjae-park1111 | Park YunJae (박윤재) | `225d872b-594c-81ba-9e42-0002b46f091a` |

### 지원 기능

- ✅ **단일 담당자 매핑**: 한 명의 사용자가 할당된 작업
- ✅ **다중 담당자 매핑**: 여러 사용자가 공동으로 할당된 작업
- ✅ **실제 Notion 사용자 ID 사용**: 완벽한 호환성 보장
- ✅ **자동 변환**: GitHub assignees → Notion people 필드

### 매핑 설정 변경

새로운 사용자를 추가하거나 기존 매핑을 변경하려면:

1. **Notion 사용자 ID 확인**:
   ```bash
   PYTHONPATH=. python get_notion_users.py
   ```

2. **`config/field_mappings.yml` 수정**:
   ```yaml
   assignees:
     github_field: "Assignees"
     notion_property: "담당자"
     type: "people"
     value_mappings:
       "새로운-github-username": "notion-user-id"
   ```

### 테스트 완료된 시나리오

✅ **25-07-Sprint4 스프린트 동기화 성공** (2025-07-29)
- 25개 GitHub 항목 → 25개 Notion 페이지 생성
- 모든 담당자 매핑 정상 작동
- 다중 담당자 작업도 완벽 처리

## 스프린트 기반 동기화

### 스프린트 명명 규칙

스프린트는 다음과 같은 형식으로 명명됩니다:
- `25-07-Sprint4` (연도-월-Sprint번호)
- `25-08-Sprint1`
- `25-08-Sprint2`

### 스프린트별 작업 흐름

1. **스프린트 시작 시**:
   ```bash
   # 새 스프린트 항목들을 동기화
   PYTHONPATH=. python scripts/complete_resync.py --sprint-filter "25-08-Sprint1" --dry-run
   PYTHONPATH=. python scripts/complete_resync.py --sprint-filter "25-08-Sprint1" --force
   ```

2. **스프린트 중간 업데이트**:
   ```bash
   # 기존 항목들을 다시 동기화 (상태 변경 반영)
   PYTHONPATH=. python scripts/complete_resync.py --sprint-filter "25-08-Sprint1" --force
   ```

3. **스프린트 완료 후**:
   ```bash
   # 완료된 스프린트의 최종 상태 동기화
   PYTHONPATH=. python scripts/complete_resync.py --sprint-filter "25-08-Sprint1" --force
   ```

## 동기화 프로세스

### 실행 단계

1. **Step 1: Notion 데이터베이스 초기화**
   - 기존 페이지들을 아카이브 처리
   - 새로운 동기화를 위한 공간 확보

2. **Step 2: GitHub 항목 동기화**
   - GitHub Project에서 항목 조회
   - 필드 매핑 및 변환 적용
   - Notion 페이지 생성 및 내용 업데이트

### 필드 매핑

| GitHub 필드 | Notion 필드 | 변환 |
|-------------|-------------|------|
| Title | 작업 | 직접 매핑 |
| Status | 진행상태 | 상태 값 매핑 |
| Priority | 우선순위 | P0→높음, P1→중간, P2→낮음 |
| Assignees | 팀원 | 사용자명→한국어 이름 |
| Labels | 태그 | 다중 선택 |
| Due Date | 마감일 | 날짜 형식 |

## 문제 해결

### 일반적인 오류

#### 1. "팀원 is not a property that exists"

**원인**: Notion 데이터베이스에 "팀원" 필드가 없음

**해결책**:
1. Notion 데이터베이스에서 "팀원" 필드를 `Multi-select` 타입으로 추가
2. 또는 `config/field_mappings.yml`에서 `notion_property`를 기존 필드명으로 변경

#### 2. "담당자 is expected to be people"

**원인**: 필드 타입 불일치

**해결책**:
1. Notion에서 해당 필드 타입을 `Multi-select`로 변경
2. 또는 새로운 필드명 사용

#### 3. 동기화 속도가 느림

**해결책**:
```bash
# 배치 크기를 줄여서 실행
PYTHONPATH=. python scripts/complete_resync.py --batch-size 10
```

#### 4. 메모리 부족

**해결책**:
```bash
# 특정 스프린트만 동기화
PYTHONPATH=. python scripts/complete_resync.py --sprint-filter "현재스프린트"
```

### 로그 확인

실행 시 자세한 로그를 확인하려면:

```bash
# 모든 로그 출력
PYTHONPATH=. python scripts/complete_resync.py --sprint-filter "25-07-Sprint4" 2>&1 | tee sync.log

# 에러만 확인
PYTHONPATH=. python scripts/complete_resync.py --quiet
```

### 백업 권장사항

중요한 동기화 전에는 다음을 권장합니다:

1. **Notion 데이터베이스 백업**
2. **Dry-run 실행으로 사전 확인**
3. **작은 배치로 테스트 실행**

## 예제 시나리오

### 새로운 스프린트 시작

```bash
# 1. 새 스프린트 항목 확인
PYTHONPATH=. python scripts/complete_resync.py --sprint-filter "25-08-Sprint2" --dry-run

# 2. 결과가 만족스러우면 실제 동기화
PYTHONPATH=. python scripts/complete_resync.py --sprint-filter "25-08-Sprint2" --force

# 3. 결과 확인
echo "동기화 완료: $(date)"
```

### 주간 상태 업데이트

```bash
# 현재 스프린트의 상태 업데이트
PYTHONPATH=. python scripts/complete_resync.py --sprint-filter "현재스프린트명" --force
```

### 전체 프로젝트 재동기화

```bash
# 경고: 모든 데이터가 다시 생성됩니다!
PYTHONPATH=. python scripts/complete_resync.py --dry-run
# 확인 후
PYTHONPATH=. python scripts/complete_resync.py --force
```

---

**주의사항**: 
- `--force` 옵션은 확인 없이 모든 기존 Notion 페이지를 삭제합니다.
- 중요한 데이터가 있다면 반드시 백업을 먼저 수행하세요.
- 첫 실행 시에는 반드시 `--dry-run`으로 테스트하세요. 