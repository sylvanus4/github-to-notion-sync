# GitHub to Notion Sync Pipeline

**GitHub Project와 Notion Database 간의 자동 동기화 시스템**

GitHub Project의 Issues와 Pull Requests를 Notion Database로 실시간 동기화하여 팀의 스크럼 프로세스를 지원합니다.

![Status: Production Ready](https://img.shields.io/badge/Status-Production%20Ready-green)
![Language: Python](https://img.shields.io/badge/Language-Python-blue)
![Sync: Assignees](https://img.shields.io/badge/Assignees-✅%20Mapped-success)

## 🎯 핵심 기능

### ✅ 완벽한 담당자 매핑 (2025-07-29 구현 완료)
- **GitHub 사용자명** → **실제 Notion 워크스페이스 사용자** 자동 매핑
- **단일/다중 담당자** 모두 지원
- **실시간 동기화**로 담당자 변경 즉시 반영

### 📝 스마트 데이터베이스 제목 관리 (NEW!)
- **자동 제목 생성**: 스프린트명 + 타임스탬프
- **커스텀 제목 지정**: 팀/프로젝트별 구분 가능
- **버전 관리**: 타임스탬프로 동기화 이력 추적

### 🔄 스프린트 기반 동기화
- **특정 스프린트만 선별 동기화** 가능
- **전체 프로젝트 동기화** 지원
- **안전한 Dry-run 모드** 제공

### 📊 완전한 필드 매핑
- **상태**: GitHub Status → Notion 진행상태
- **우선순위**: GitHub Priority → Notion 우선순위  
- **태그**: GitHub Labels → Notion 태그
- **마감일**: GitHub Due Date → Notion 마감일

## 🚀 빠른 시작

### 1. 특정 스프린트 동기화

```bash
# 1. 먼저 안전하게 확인 (자동으로 데이터베이스 제목도 생성됩니다)
PYTHONPATH=. python scripts/complete_resync.py --sprint-filter "25-07-Sprint4" --dry-run

# 2. 결과가 만족스러우면 실제 동기화
# → 데이터베이스 제목: "GitHub Sync - 25-07-Sprint4 - 20251022153045"
PYTHONPATH=. python scripts/complete_resync.py --sprint-filter "25-07-Sprint4" --force
```

### 2. 커스텀 데이터베이스 제목으로 동기화

```bash
# 원하는 제목으로 데이터베이스 제목을 지정
PYTHONPATH=. python scripts/complete_resync.py \
  --sprint-filter "25-07-Sprint4" \
  --database-title "2025년 7월 스프린트 4" \
  --force
```

### 3. 전체 프로젝트 동기화

```bash
# ⚠️ 주의: 모든 기존 Notion 페이지가 삭제됩니다!
# → 데이터베이스 제목: "GitHub Sync - All Items - 20251022153045"
PYTHONPATH=. python scripts/complete_resync.py --force
```

### 4. 조용한 실행 (에러만 출력)

```bash
PYTHONPATH=. python scripts/complete_resync.py --sprint-filter "현재스프린트" --quiet
```

## 👥 담당자 매핑 시스템

### 성공적으로 매핑된 사용자들

| GitHub 사용자명 | Notion 사용자 | 상태 |
|----------------|--------------|------|
| `duyeol-yu` | 유두열 | ✅ |
| `jaehoonkim` | Jae-Hoon Kim (김재훈) | ✅ |
| `sylvanus4` | HJ (한효정) | ✅ |
| `thaki-yakhyo` | yakhyo | ✅ |
| `thakicloud-jotaeyang` | 조태양 | ✅ |
| `yunjae-park1111` | Park YunJae (박윤재) | ✅ |

### 테스트 완료된 시나리오

**✅ 25-07-Sprint4 스프린트 동기화 성공** (2025-07-29)
- 📊 **25개 GitHub 항목** → **25개 Notion 페이지** 생성
- 👥 **모든 담당자 매핑** 정상 작동  
- 🤝 **다중 담당자 작업**도 완벽 처리
- ⏱️ **실행 시간**: 108.93초

## 📋 스프린트 워크플로우

### 새로운 스프린트 시작

```bash
# 1. 새 스프린트 항목 확인 (자동으로 제목 생성됩니다)
PYTHONPATH=. python scripts/complete_resync.py --sprint-filter "25-08-Sprint1" --dry-run
# → 제목 미리보기: "GitHub Sync - 25-08-Sprint1 - 20251022153045"

# 2. 실제 동기화 실행
PYTHONPATH=. python scripts/complete_resync.py --sprint-filter "25-08-Sprint1" --force

# 3. (선택) 커스텀 제목으로 실행
PYTHONPATH=. python scripts/complete_resync.py \
  --sprint-filter "25-08-Sprint1" \
  --database-title "2025년 8월 스프린트 1" \
  --force

# 4. 결과 확인
echo "✅ 동기화 완료: $(date)"
```

### 스프린트 중간 업데이트

```bash
# 상태 변경사항 반영 (자동으로 새로운 타임스탬프 생성)
PYTHONPATH=. python scripts/complete_resync.py --sprint-filter "현재스프린트" --force
```

### 스프린트 완료 후

```bash
# 최종 상태 동기화
PYTHONPATH=. python scripts/complete_resync.py \
  --sprint-filter "완료된스프린트" \
  --database-title "완료 - 완료된스프린트" \
  --force
```

## ⚙️ 명령어 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--dry-run` | 🔍 실제 변경 없이 분석만 수행 | False |
| `--force` | ⚡ 확인 프롬프트 없이 실행 | False |
| `--quiet` | 🔇 에러 메시지만 출력 | False |
| `--batch-size N` | 📦 배치 처리 크기 설정 | 50 |
| `--sprint-filter "NAME"` | 🎯 특정 스프린트만 필터링 | 모든 항목 |
| `--database-title "TITLE"` | 📝 데이터베이스 제목 지정 | 자동 생성 (스프린트명-타임스탬프) |

## 🔧 고급 사용법

### 데이터베이스 제목 자동 생성 규칙

데이터베이스 제목을 지정하지 않으면 자동으로 생성됩니다:

```bash
# Sprint 필터 사용 시
# → "GitHub Sync - {sprint_filter} - {timestamp}"
# 예: "GitHub Sync - 25-07-Sprint4 - 20251022153045"

# Sprint 필터 없이 전체 동기화 시  
# → "GitHub Sync - All Items - {timestamp}"
# 예: "GitHub Sync - All Items - 20251022153045"
```

### 데이터베이스 제목 커스터마이징

```bash
# 1. 월별 구분
PYTHONPATH=. python scripts/complete_resync.py \
  --database-title "2025년 10월 백로그" \
  --force

# 2. 팀별 구분
PYTHONPATH=. python scripts/complete_resync.py \
  --sprint-filter "25-07-Sprint4" \
  --database-title "백엔드팀 Sprint 4" \
  --force

# 3. 프로젝트별 구분
PYTHONPATH=. python scripts/complete_resync.py \
  --database-title "프로젝트 X - 진행중인 작업" \
  --force
```

### 배치 크기 조정

```bash
# 느린 네트워크나 대량 데이터시 사용
PYTHONPATH=. python scripts/complete_resync.py --batch-size 10 --sprint-filter "25-07-Sprint4"
```

### 로그 확인

```bash
# 모든 로그 출력 및 파일 저장
PYTHONPATH=. python scripts/complete_resync.py --sprint-filter "25-07-Sprint4" 2>&1 | tee sync.log
```

### 새로운 사용자 추가

```bash
# 1. Notion 워크스페이스 사용자 ID 확인
PYTHONPATH=. python get_notion_users.py

# 2. config/field_mappings.yml에 매핑 추가
# assignees:
#   value_mappings:
#     "새로운-github-username": "notion-user-id"
```

## 📁 프로젝트 구조

```
github-to-notion-sync/
├── 🎯 scripts/
│   └── complete_resync.py              # 🚀 메인 동기화 스크립트
├── 📋 docs/
│   └── GITHUB_SCRUM_WORKFLOW.md        # 📖 핵심 워크플로우 가이드
├── ⚙️ config/
│   ├── field_mappings.yml              # 👥 담당자 매핑 설정
│   ├── sync_config.yml                 # 🔄 동기화 설정
│   └── webhook_events.yml              # 🎣 웹훅 이벤트 설정
├── 🧠 src/
│   ├── services/
│   │   ├── github_service.py           # 🐙 GitHub API 클라이언트
│   │   ├── notion_service.py           # 📝 Notion API 클라이언트  
│   │   └── sync_service.py             # 🔄 동기화 로직
│   └── utils/
│       ├── mapping.py                  # 🗺️ 필드 매핑 유틸리티
│       └── logger.py                   # 📊 로깅 시스템
└── 🧪 tests/                           # ✅ 테스트 코드
```

## 🛠️ 설치 및 설정

### 1. 환경 설정

```bash
# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일 편집
```

### 2. 필수 환경 변수

```bash
# API 토큰
NOTION_TOKEN=secret_...
GH_TOKEN=github_pat_...

# 프로젝트 설정  
GH_ORG=ThakiCloud
GH_PROJECT_NUMBER=5
NOTION_DATABASE_ID=...

# 보안
GH_WEBHOOK_SECRET=...
```

### 3. 설정 검증

```bash
# 연결 테스트
python scripts/validate_setup.py
```

## 🔧 동기화 프로세스

### 실행 단계

1. **📝 Step 0: 데이터베이스 제목 업데이트**
   - 자동 생성 또는 지정된 제목으로 업데이트
   - 타임스탬프 기반 버전 관리

2. **🗑️ Step 1: Notion 데이터베이스 초기화**
   - 기존 페이지들을 아카이브 처리
   - 새로운 동기화를 위한 공간 확보

3. **📥 Step 2: GitHub 항목 동기화**  
   - GitHub Project에서 항목 조회
   - 필드 매핑 및 변환 적용
   - Notion 페이지 생성 및 내용 업데이트

### 필드 매핑

| GitHub 필드 | Notion 필드 | 변환 |
|-------------|-------------|------|
| Title | 작업 | 직접 매핑 |
| Status | 진행상태 | 상태 값 매핑 |
| Priority | 우선순위 | P0→높음, P1→중간, P2→낮음 |
| **Assignees** | **담당자** | **사용자명→실제 사용자 ID** ✅ |
| Labels | 태그 | 다중 선택 |
| Due Date | 마감일 | 날짜 형식 |

## 🚨 문제 해결

### 일반적인 오류

#### "담당자 is expected to be people"
```bash
# 해결: 이미 해결됨! 실제 Notion 사용자 ID 사용
✅ 2025-07-29 완전 해결
```

#### 동기화 속도가 느림
```bash
# 해결: 배치 크기를 줄여서 실행
PYTHONPATH=. python scripts/complete_resync.py --batch-size 10
```

#### 메모리 부족
```bash
# 해결: 특정 스프린트만 동기화
PYTHONPATH=. python scripts/complete_resync.py --sprint-filter "현재스프린트"
```

### 백업 권장사항

중요한 동기화 전에는 다음을 권장합니다:

1. **📋 Notion 데이터베이스 백업**
2. **🔍 Dry-run 실행으로 사전 확인**  
3. **📦 작은 배치로 테스트 실행**

## 📖 추가 문서

- 📋 **[스크럼 워크플로우 가이드](docs/GITHUB_SCRUM_WORKFLOW.md)** - 핵심 사용법
- 🏗️ **[아키텍처 문서](docs/ARCHITECTURE.md)** - 시스템 구조
- 🚀 **[배포 가이드](docs/DEPLOYMENT.md)** - 배포 방법
- 🔧 **[설정 가이드](docs/SETUP.md)** - 상세 설정
- 🆘 **[문제 해결](docs/TROUBLESHOOTING.md)** - 트러블슈팅

## 📈 성공 사례

**✅ 25-07-Sprint4 스프린트 동기화 완료**
- **처리 항목**: 25개 GitHub Issues/PRs
- **생성된 페이지**: 25개 Notion 페이지  
- **담당자 매핑**: 100% 성공
- **다중 담당자**: 완벽 지원
- **실행 시간**: 108.93초
- **상태**: Production Ready 🚀

---

## ⚠️ 주의사항

- `--force` 옵션은 확인 없이 모든 기존 Notion 페이지를 삭제합니다
- 중요한 데이터가 있다면 반드시 백업을 먼저 수행하세요  
- 첫 실행 시에는 반드시 `--dry-run`으로 테스트하세요

## 🤝 기여하기

1. 이슈 생성 또는 기능 제안
2. Fork 후 개발  
3. 테스트 작성 및 실행
4. Pull Request 제출

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

