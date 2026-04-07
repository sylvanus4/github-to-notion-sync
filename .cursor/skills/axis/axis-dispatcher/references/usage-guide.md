# 6-Axis Personal Assistant — 활용 가이드

## 목차

1. [빠른 시작](#1-빠른-시작)
2. [일과 흐름](#2-일과-흐름)
3. [개별 축 수동 실행](#3-개별-축-수동-실행)
4. [온디맨드 명령어](#4-온디맨드-명령어)
5. [산출물 확인 방법](#5-산출물-확인-방법)
6. [자동화 레벨 관리](#6-자동화-레벨-관리)
7. [장애 대응](#7-장애-대응)
8. [엔티티 별칭 관리](#8-엔티티-별칭-관리)
9. [시너지 규칙 확장](#9-시너지-규칙-확장)
10. [Cursor Automations 설정](#10-cursor-automations-설정)
11. [자주 쓰는 시나리오 레시피](#11-자주-쓰는-시나리오-레시피)
12. [문제 해결](#12-문제-해결)

---

## 1. 빠른 시작

### 최초 실행 전 체크리스트

```
[ ] outputs/axis/ 디렉토리 구조 확인
[ ] outputs/axis/automation-levels.json 존재 여부
[ ] outputs/axis/gm/entity-aliases.json 존재 여부
[ ] Slack MCP 연결 확인
[ ] gws CLI 인증 확인 (gws auth status)
[ ] gh CLI 인증 확인 (gh auth status)
[ ] tossctl 인증 확인 (해당 시)
```

### 첫 실행

Cursor 에이전트에게 다음과 같이 말합니다:

```
6축 디스패처 아침 루틴 실행해줘
```

또는 영어로:

```
Run the axis-dispatcher morning routine
```

디스패처가 6개 축을 순서대로 실행하고, `#효정-할일`에 종합 브리핑을 올립니다.

---

## 2. 일과 흐름

### 아침 (07:00 KST)

```
┌─────────────────────────────────────────────────────────┐
│ Phase 0: axis-life (순차)                                │
│   → 캘린더 브리핑, 이메일 트리아지, 심부름 체크             │
├─────────────────────────────────────────────────────────┤
│ Phase 1: 4축 병렬 실행                                    │
│   axis-recruitment  → 채용 파이프라인, 면접 준비            │
│   axis-investment   → today 파이프라인, 증권사 연동         │
│   axis-learning     → HF 트렌딩, 학습 큐                  │
│   axis-sidepm       → Git 상태, 스프린트 트리아지           │
├─────────────────────────────────────────────────────────┤
│ Phase 2: axis-gm (순차)                                  │
│   → 크로스축 집계, 시너지 탐지, 종합 브리핑 작성             │
├─────────────────────────────────────────────────────────┤
│ Phase 3: Slack 종합 브리핑 (#효정-할일)                    │
│   → 메인: 6축 상태 그리드                                 │
│   → 쓰레드: 우선순위 / 의사결정 / 에러                     │
└─────────────────────────────────────────────────────────┘
```

### 저녁 (17:00 KST)

```
Phase 0: axis-life 저녁 (내일 준비, 이메일 팔로업)
Phase 1: 병렬 — investment EOD, sidepm EOD 배포, learning 논문 처리, recruitment 팔로업
Phase 2: axis-gm 일일 다이제스트
Phase 3: EOD Slack 요약
```

### 주간 (금요일 PM)

```
Phase W1: 병렬 — learning 주간 진도, sidepm 주간 리포트
Phase W2: axis-gm OKR 진도 + 개선 추천 + 경영진 브리핑
Phase W3: 주간 Slack 요약 + Notion 동기화
```

### 호출 방법

| 루틴 | 한국어 | 영어 |
|------|--------|------|
| 아침 전체 | "6축 아침 루틴 실행" | "Run axis-dispatcher morning" |
| 저녁 전체 | "6축 저녁 루틴 실행" | "Run axis-dispatcher evening" |
| 주간 리뷰 | "6축 주간 리뷰 실행" | "Run axis-dispatcher weekly" |

---

## 3. 개별 축 수동 실행

전체 디스패처를 돌리지 않고 특정 축만 실행할 수 있습니다.

| 축 | 트리거 예시 |
|----|-------------|
| Axis 1: 채용 | "axis recruitment 아침 실행" / "채용 축 실행" |
| Axis 2: 투자 | "axis investment 실행" / "투자 축 돌려줘" |
| Axis 3: 학습 | "axis learning 아침" / "학습 축 실행" |
| Axis 4: GM | "axis gm 실행" / "총괄 축 돌려줘" |
| Axis 5: Side PM | "axis sidepm 실행" / "사이드PM 축 돌려줘" |
| Axis 6: 생활 | "axis life 실행" / "생활 축 돌려줘" |

개별 축 실행 시 해당 축의 산출물만 갱신됩니다.
GM 축은 다른 축들의 산출물을 읽으므로, 다른 축들이 먼저 실행된 상태에서 돌리는 것이 좋습니다.

---

## 4. 온디맨드 명령어

일과와 별개로 수시로 사용할 수 있는 명령어입니다.

### Axis 1: 채용

```
/job add Anthropic "AI Research Engineer" https://anthropic.com/careers/...
/job update job-001 phone_screen
/job prep job-001                    ← 면접 준비 자료 생성
/job research Anthropic              ← 회사 심층 리서치
```

**파이프라인 스테이지:**
`discovered` → `researching` → `applied` → `phone_screen` → `technical` → `onsite` → `offer` → `accepted` / `rejected` / `withdrawn`

### Axis 2: 투자

투자 축은 기존 스킬을 직접 호출합니다:

```
daily-stock-check 실행해줘              ← 일일 주식 분석
toss-ops-orchestrator 실행해줘          ← 토스증권 종합 점검
투자 인텔리전스 종합 분석해줘             ← trading-intel-orchestrator
```

### Axis 3: 학습

```
논문 리뷰 큐에 추가: arxiv:2401.12345
학습 큐에 "RAG 최적화" 토픽 추가해줘
KB 빌드해줘                            ← kb-orchestrator
논문 아카이브 검색: attention mechanism
```

### Axis 5: Side PM

```
5개 레포 git 상태 확인해줘              ← axis-sidepm Phase 1
eod-ship 실행해줘                      ← 전체 레포 커밋 + 푸시
cursor-sync 실행해줘                   ← .cursor/ 에셋 동기화
```

### Axis 6: 생활

```
/errand add "세탁물 찾기" --due 2026-04-08
/errand done errand-001
/errand list
오늘 일정 알려줘                        ← calendar-daily-briefing
메일 정리해줘                           ← gmail-daily-triage
```

---

## 5. 산출물 확인 방법

### 디렉토리 구조

```
outputs/axis/
├── automation-levels.json          ← 6축 자동화 레벨 중앙 관리
├── dispatch/                       ← (dispatcher가 사용)
├── recruitment/
│   ├── job-pipeline.json           ← 영구 파일: 채용 파이프라인
│   ├── criteria-config.json        ← 영구 파일: 점수 기준
│   └── 2026-04-07/                 ← 일별 산출물
│       ├── pipeline-status.json
│       ├── new-opportunities.json
│       ├── interview-prep.json
│       ├── recruitment-briefing.md  ← 핵심 산출물
│       └── errors.json             ← 에러 (있을 때만)
├── investment/
│   └── 2026-04-07/
│       ├── morning-summary.json     ← 핵심 산출물
│       ├── toss-ops.json
│       ├── content/                 ← 콘텐츠 초안들
│       ├── eod-summary.json
│       └── strategy-review.json
├── learning/
│   ├── learning-queue.json         ← 영구 파일: 학습 큐
│   ├── topics-config.json          ← 영구 파일: 추적 토픽
│   └── 2026-04-07/
│       ├── ai-radar.json
│       ├── queue-status.json
│       ├── learning-briefing.md     ← 핵심 산출물
│       └── papers-processed.json
├── gm/
│   ├── entity-aliases.json         ← 영구 파일: 엔티티 별칭
│   └── 2026-04-07/
│       ├── cross-axis-scan.json
│       ├── synergies.json           ← 시너지 탐지 결과
│       ├── decisions-pending.json
│       ├── morning-digest.md        ← 핵심 산출물 (아침)
│       ├── daily-digest.md          ← 핵심 산출물 (저녁)
│       ├── axis-health.json         ← 축별 건강 점수
│       ├── dispatch-morning.json    ← 디스패치 매니페스트
│       └── dispatch-evening.json
├── sidepm/
│   └── 2026-04-07/
│       ├── git-status.json
│       ├── sprint-triage.json
│       ├── ci-health.json
│       └── dev-briefing.md          ← 핵심 산출물
└── life/
    ├── errands-queue.json           ← 영구 파일: 심부름 큐
    └── 2026-04-07/
        ├── calendar.json
        ├── email-triage.json
        ├── errands.json
        └── morning-briefing.md      ← 핵심 산출물
```

### 핵심 산출물 빠르게 보기

```
오늘 GM 아침 다이제스트 읽어줘
→ outputs/axis/gm/2026-04-07/morning-digest.md

오늘 투자 요약 보여줘
→ outputs/axis/investment/2026-04-07/morning-summary.json

시너지 탐지 결과 확인
→ outputs/axis/gm/2026-04-07/synergies.json

디스패치 매니페스트 확인
→ outputs/axis/gm/2026-04-07/dispatch-morning.json
```

### Slack 채널 라우팅

| 채널 | 내용 |
|------|------|
| `#효정-할일` | 종합 브리핑, 축별 알림, 심부름 리마인더 |
| `#효정-의사결정` | 개인 의사결정 (매매, 이메일 답장, 도구 도입) |
| `#7층-리더방` | 팀/CTO 의사결정 (인프라, 전략, 파트너십) |
| `#h-report` | 투자 시그널, 일일 리포트 (today 파이프라인) |
| `#deep-research-trending` | AI 연구 레이더 |

---

## 6. 자동화 레벨 관리

### 현재 레벨 확인

```
outputs/axis/automation-levels.json 열어줘
```

### 3단계 레벨 설명

| 레벨 | 설명 | 예시 |
|------|------|------|
| **0 — 보고만** | 분석 + 리포트만 생성, 사람이 직접 행동 | 주식 시그널 보고 → 사람이 매매 |
| **1 — 제안 + 확인** | 구체적 행동 제안 후 `#효정-의사결정`에서 승인 대기 | "NVDA 매수 제안 → ✅/❌ 대기" |
| **2 — 실행 + 알림** | 사전 승인된 범주의 행동을 자동 실행 후 알림 | 논문 점수 8.5 이상 자동 리뷰 시작 |

### 레벨 업그레이드 조건

```
Level 0 → 1: 7일 연속 클린 실행 (S1/S2 에러 없음)
Level 1 → 2: Level 1에서 14일 연속 클린 + 사람 승인
```

### 레벨 변경 방법

**자동 다운그레이드:**
- S1 에러 발생 → 자동으로 현재 레벨 - 1
- 3일 연속 S1 → 서킷 브레이커 작동 (Level -1: 비활성화)

**수동 업그레이드:**
```
automation-levels.json에서 axis-investment 레벨을 1로 올려줘
```

또는 `#효정-의사결정`에서 "axis-investment Level 1 승인" 메시지 후 변경.

### 안전 제약 (레벨 2에서도 자동 실행 불가)

- 금융 거래 (매매, 결제)
- 외부 커뮤니케이션 (이메일 발송, 메시지)
- 파괴적 작업 (삭제, force push)
- 이들은 항상 Level 1 (확인 필요) 최대입니다.

---

## 7. 장애 대응

### 장애 등급

| 등급 | 라벨 | 의미 | 알림 채널 |
|------|------|------|-----------|
| S1 | CRITICAL | 축 시작 불가 (인증 실패 등) | `#효정-의사결정` |
| S2 | DEGRADED | 일부 페이즈 실패, 나머지 완료 | `#효정-할일` |
| S3 | WARNING | 비차단 이슈 (데이터 미갱신 등) | `#효정-할일` (쓰레드) |
| S4 | INFO | 예상된 스킵 (시장 휴장 등) | 로그만 기록 |

### 장애 발생 시 확인 방법

```
오늘 투자 축 에러 확인해줘
→ outputs/axis/investment/2026-04-07/errors.json

디스패치 매니페스트 에러 섹션 확인
→ outputs/axis/gm/2026-04-07/dispatch-morning.json의 errors 필드
```

### 개별 축 재실행

디스패처 전체를 다시 돌릴 필요 없이 실패한 축만 재실행합니다:

```
axis-investment 아침 루틴 다시 실행해줘
```

동일 날짜 키로 파일을 덮어쓰므로 (idempotent) 중복 걱정 없습니다.

### 서킷 브레이커 해제

3일 연속 S1으로 비활성화된 축을 복구하려면:

```
automation-levels.json에서 axis-recruitment 레벨을 0으로 리셋해줘
```

근본 원인 (인증 만료, API 키 등)을 먼저 해결한 후 리셋합니다.

---

## 8. 엔티티 별칭 관리

`outputs/axis/gm/entity-aliases.json`에서 GM 축의 퍼지 매칭에 사용하는 별칭을 관리합니다.

### 별칭 추가 예시

```
entity-aliases.json에 "PLTR": ["Palantir", "팔란티어", "Palantir Technologies"] 추가해줘
```

### 별칭 카테고리

| 카테고리 | 예시 |
|----------|------|
| `companies` | 티커 → 회사명, 한글명, 정식명 |
| `topics` | 약어 → 풀네임, 한글명, 변형 |

### 매칭 전략 (3-Tier)

1. **Exact**: 문자열 완전 일치
2. **Alias**: `entity-aliases.json`의 별칭 목록에서 매칭
3. **Semantic**: 문맥 기반 유사도 (예: "GPU 클라우드" ↔ "AI 인프라")

---

## 9. 시너지 규칙 확장

`.cursor/skills/axis/axis-gm/references/synergy-rules.md`에 정의된 8개 규칙을 확장할 수 있습니다.

### 현재 규칙 목록

| ID | 이름 | 관련 축 |
|----|------|---------|
| R001 | 기업 겹침 | 채용 ↔ 투자 |
| R002 | 토픽-프로젝트 정렬 | 학습 ↔ SidePM |
| R003 | 캘린더-데드라인 충돌 | 생활 ↔ 채용/SidePM |
| R004 | 뉴스-투자 시그널 | 학습 ↔ 투자 |
| R005 | 면접 준비 부스트 | 채용 ↔ 학습 |
| R006 | 사이드 프로젝트 데모 → 채용 | SidePM ↔ 채용 |
| R007 | 이메일 → 멀티축 라우팅 | 생활 → 전체 |
| R008 | 시장 이벤트 → 캘린더 블록 | 투자 ↔ 생활 |

### 새 규칙 추가 요청 예시

```
시너지 규칙에 R009 추가해줘:
"학습에서 발견한 오픈소스 프로젝트가 SidePM의 기존 프로젝트와 기술 스택이 겹치면 통합 가능성 알림"
관련 축: 학습 ↔ SidePM
출력 형식: { rule: "R009", name: "Open Source Integration", ... }
```

---

## 10. Cursor Automations 설정

완전 자동화를 위해 Cursor Automations에 3개 크론 작업을 등록합니다.
상세 가이드: `axis-dispatcher/references/automation-setup.md`

### 요약

| 자동화 | 크론 (UTC) | KST | 요일 |
|--------|-----------|-----|------|
| 아침 디스패치 | `0 22 * * 0-4` | 07:00 | 월-금 |
| 저녁 디스패치 | `0 8 * * 1-5` | 17:00 | 월-금 |
| 주간 리뷰 | `30 8 * * 5` | 17:30 | 금 |

### 설정 위치

[cursor.com/automations/new](https://cursor.com/automations/new)에서 등록

### 수동 실행 대안

Automations를 설정하지 않더라도, 매일 Cursor를 열고 다음과 같이 말하면 됩니다:

```
아침이야. 6축 아침 루틴 실행해줘.
```

```
퇴근할게. 6축 저녁 루틴 실행해줘.
```

---

## 11. 자주 쓰는 시나리오 레시피

### 시나리오 1: 아침에 빠르게 현황 파악

```
6축 아침 루틴 실행해줘
```

실행 후 `#효정-할일`에 올라오는 종합 브리핑을 확인합니다.
급한 경우 GM 다이제스트만 읽습니다: "오늘 GM 아침 다이제스트 읽어줘"

### 시나리오 2: 면접 준비

```
/job update job-003 technical
axis recruitment으로 job-003 면접 준비 자료 만들어줘
```

또는:

```
/job prep job-003
```

### 시나리오 3: 오늘의 주식 시그널만 빠르게

전체 축이 아닌 투자 축만 실행합니다:

```
axis investment 아침 실행해줘
```

### 시나리오 4: 특정 논문을 학습 큐에 추가

```
학습 큐에 추가해줘: arxiv:2604.03128, depth: full, priority: high
```

저녁 루틴에서 자동으로 paper-review가 실행됩니다 (하루 최대 2편).

### 시나리오 5: 심부름 관리

```
/errand add "다이소에서 수납 박스 사기" --due 2026-04-09
/errand list
/errand done errand-003
```

아침 브리핑에 당일 심부름이 자동 포함됩니다.

### 시나리오 6: 크로스축 시너지 직접 확인

```
오늘 시너지 탐지 결과 보여줘
```

→ `outputs/axis/gm/{date}/synergies.json` 내용을 요약해서 보여줍니다.

### 시나리오 7: 축 건강 상태 대시보드

```
축 건강 대시보드 생성해줘
```

→ `visual-explainer`로 6축 레이더 차트 + 타임라인 + 의사결정 큐를 HTML로 생성합니다.

### 시나리오 8: 주간 회고

금요일 저녁 루틴 후:

```
6축 주간 리뷰 실행해줘
```

### 시나리오 9: 특정 축의 자동화 레벨 올리기

7일 이상 에러 없이 운영된 축의 레벨을 올립니다:

```
axis-life 자동화 레벨 1로 올려줘. 7일간 클린 실행 확인됨.
```

### 시나리오 10: 기존 파이프라인과의 관계

| 기존 명령 | 6축 대응 | 비고 |
|-----------|---------|------|
| "morning 실행" | "6축 아침 루틴" | 6축이 기존 morning 파이프라인을 감싸서 실행 |
| "today 실행" | "axis investment 실행" | 투자 축이 today를 Phase 1에서 호출 |
| "google-daily 실행" | "axis life 실행" | 생활 축이 google-daily를 Phase 1-2에서 호출 |
| "eod-ship 실행" | "axis sidepm 저녁" | SidePM 축이 eod-ship을 Phase E1에서 호출 |

기존 스킬들은 그대로 독립 실행 가능합니다. 6축은 이들을 **래핑**할 뿐, 대체하지 않습니다.

---

## 12. 문제 해결

### Q: 특정 축만 계속 실패해요

1. 에러 로그 확인: `outputs/axis/{axis}/{date}/errors.json`
2. 원인 분류 확인 (AUTH_FAILURE, API_TIMEOUT 등)
3. 해당 스킬의 사전 조건 확인:
   - `gws auth status` (생활 축)
   - `gh auth status` (SidePM 축)
   - `tossctl session` (투자 축)
4. 원인 해결 후 해당 축만 재실행

### Q: Slack에 알림이 안 올라와요

1. Slack MCP 서버 연결 상태 확인
2. `.env`에서 Slack 토큰 확인
3. 채널 ID 확인: `#효정-할일` = `C0AA8NT4T8T`

### Q: 디스패처를 돌렸는데 GM 다이제스트가 비어있어요

GM 축은 다른 축들의 산출물을 읽습니다. 다른 축이 실행되지 않았으면 "NO DATA"로 표시됩니다.
해결: 전체 디스패처를 실행하거나, 다른 축 실행 후 GM 축만 실행합니다.

### Q: 주말에도 실행되나요?

크론은 평일만 (`Mon-Fri`). 주말에는 자동 실행되지 않습니다.
수동으로 "axis life 실행"처럼 개별 축 실행은 가능합니다.
투자 축은 주말에 시장이 휴장이므로 S4 (INFO)로 스킵됩니다.

### Q: 이전에 쓰던 morning-ship / daily-am-orchestrator와 뭐가 달라요?

6축 시스템이 이들을 **상위 레벨에서 대체**합니다:
- `daily-am-orchestrator` → `axis-dispatcher` 아침 루틴이 대체
- `daily-pm-orchestrator` → `axis-dispatcher` 저녁 루틴이 대체
- `morning-ship` → `axis-sidepm`이 git sync 부분을 감싸서 호출

기존 스킬들은 삭제되지 않았으며, 독립적으로도 사용 가능합니다.

### Q: 처음 실행할 때 영구 파일이 없다고 에러가 나요

최초 실행 시 다음 파일들이 빈 배열/객체로 초기화되어야 합니다:

```json
outputs/axis/recruitment/job-pipeline.json    → []
outputs/axis/recruitment/criteria-config.json → {}
outputs/axis/learning/learning-queue.json     → []
outputs/axis/learning/topics-config.json      → {}
outputs/axis/life/errands-queue.json          → []
```

다음 명령으로 초기화합니다:

```
6축 영구 파일 초기화해줘
```

---

## Phase Guard — 기존 스킬과 중복 방지

6축 시스템은 기존 파이프라인(`today`, `google-daily`, `hf-trending-intelligence` 등)을
래핑하여 실행합니다. 하지만 이미 해당 파이프라인을 수동으로 실행한 경우, 축 디스패치 시
동일한 작업이 **중복 실행**될 위험이 있습니다 (API 비용 이중 청구, Slack 이중 포스팅 등).

### 작동 원리

각 축의 SKILL.md에 **Phase Guard**가 적용되어 있습니다:

1. 축이 서브 파이프라인을 실행하기 전에, 오늘 날짜의 출력 파일이 이미 존재하는지 확인
2. 파일이 있으면 해당 Phase를 **SKIP**하고 기존 출력물을 재사용
3. 파일이 없으면 정상적으로 서브 파이프라인을 실행

**예시 — 투자축(axis-investment):**

| Phase | 가드 파일 | 스킵 조건 |
|-------|----------|----------|
| 1 (today) | `outputs/daily/{date}/daily_report_{date}.docx` | 파일 존재 |
| 2 (Toss ops) | `outputs/axis/investment/{date}/toss-ops.json` | 파일 존재 |

아침에 `today` 파이프라인을 먼저 수동 실행했다면, 축 디스패치 시 Phase 1은 자동으로
건너뛰고 기존 리포트를 읽어서 사용합니다.

### 강제 재실행

특정 상황에서 전체 재실행이 필요하면 `--force` 플래그를 전달합니다:

```
6축 디스패치 --force    → 모든 가드를 무시하고 전체 재실행
axis-investment --force → 투자축만 전체 재실행
```

### 가드 현황 추적

스킵된 Phase는 디스패치 매니페스트에 `REUSED — {guard_file}`로 기록됩니다.
Slack 브리핑에도 "N개 Phase 재사용됨"이 표시되어, 어떤 작업이 실제로 실행되고
어떤 작업이 기존 결과를 재활용했는지 투명하게 확인할 수 있습니다.

### 축별 가드 파일 요약

| 축 | Phase | 가드 파일 |
|----|-------|----------|
| Life | Calendar | `outputs/google-daily/{date}/phase-1-calendar.json` |
| Life | Email | `outputs/google-daily/{date}/phase-2-gmail.json` |
| Investment | today | `outputs/daily/{date}/daily_report_{date}.docx` |
| Investment | Toss | `outputs/axis/investment/{date}/toss-ops.json` |
| Learning | AI Radar | `outputs/hf-trending/{date}/hf-trending-intelligence-report.md` |
| Learning | KB Router | `outputs/axis/learning/{date}/kb-routing.json` |
| Side PM | Git sync | `outputs/axis/sidepm/{date}/git-status.json` |
| Side PM | EOD ship | `outputs/axis/sidepm/{date}/shipped.json` |
| Side PM | Cursor sync | `outputs/axis/sidepm/{date}/cursor-sync.json` |
| Recruitment | Portal | `outputs/axis/recruitment/{date}/portal-scan.json` |
| Recruitment | Inbox | `outputs/axis/recruitment/{date}/inbox-candidates.json` |
| GM | Collect | `outputs/axis/gm/{date}/axis-outputs.json` |
| GM | Synergy | `outputs/axis/gm/{date}/synergies.json` |
| GM | Briefing | `outputs/axis/gm/{date}/daily-briefing.md` |
| Dispatcher | 전체 | `outputs/axis/dispatch/{date}/dispatch-manifest.json` |

---

## 참조 문서

| 문서 | 경로 |
|------|------|
| 디스패처 SKILL | `.cursor/skills/axis/axis-dispatcher/SKILL.md` |
| 자동화 레벨 프로토콜 | `.cursor/skills/axis/axis-dispatcher/references/automation-levels.md` |
| 장애 알림 프로토콜 | `.cursor/skills/axis/axis-dispatcher/references/failure-alerting.md` |
| Cursor Automations 설정 | `.cursor/skills/axis/axis-dispatcher/references/automation-setup.md` |
| 시너지 규칙 | `.cursor/skills/axis/axis-gm/references/synergy-rules.md` |
| 엔티티 별칭 | `outputs/axis/gm/entity-aliases.json` |
| 자동화 레벨 상태 | `outputs/axis/automation-levels.json` |
