# Phase별 실패 복구 전략

각 Phase에서 발생할 수 있는 실패 유형과 복구 방법. Fix Loop(CP2 이후)는 [fix-loop.md](fix-loop.md) 참조.

---

## 1. 실패 분류

| 등급 | 정의 | 기본 행동 |
|------|------|----------|
| **Recoverable** | 자동 복구 가능 | 대안 시도 후 진행 |
| **Degraded** | 품질 저하되지만 진행 가능 | 사용자 알림 후 진행 |
| **Blocking** | 진행 불가 | 사용자 개입 요청 |

---

## 2. Phase별 실패 복구

### Phase 0.5 (Auto-Discovery)

| 실패 유형 | 등급 | 복구 전략 |
|----------|------|----------|
| Swagger localhost 연결 실패 | Recoverable | 정적 swagger.json 탐색으로 전환 |
| 정적 swagger.json도 없음 | Degraded | Phase 1, 4 스킵. CP 0.5에서 사용자 알림 |
| 도메인명 추론 실패 | Blocking | 사용자에게 "영문 도메인명을 알려주세요" 질문 |
| 유사 화면 없음 (새 패턴) | Degraded | 화면 유형 기본 TDS 구성으로 대체 (auto-discovery.md §3.3) |

### Phase 1 (API Spec)

| 실패 유형 | 등급 | 복구 전략 |
|----------|------|----------|
| Swagger URL 응답 실패 (404/timeout) | Recoverable | 사용자에게 URL 재확인 요청. 재실패 → Phase 1 스킵 |
| Swagger 파싱 오류 (잘못된 JSON) | Recoverable | `jq` 또는 수동 파싱 시도. 실패 → 사용자에게 올바른 Swagger 요청 |
| 도메인 관련 엔드포인트 없음 | Degraded | Phase 1, 4 스킵. "API가 아직 구현되지 않은 것 같습니다" 알림 |

### Phase 2 (Screen Spec)

| 실패 유형 | 등급 | 복구 전략 |
|----------|------|----------|
| 기획서 생성 시 정보 부족 | Degraded | 최소 기획서(화면 유형 + 기본 구성)로 생성 → 사용자 확인 |
| screen-description 스킬 호출 실패 | Recoverable | API Spec + 유사 화면 기반으로 인라인 기획서 생성 |

### Phase 3 (Figma)

| 실패 유형 | 등급 | 복구 전략 |
|----------|------|----------|
| Figma MCP 서버 미연결 | Degraded | Phase 3 스킵 → 유사 화면 레이아웃 참조로 대체 |
| Figma URL 파싱 실패 (잘못된 형식) | Recoverable | URL 형식 안내 후 재입력 요청 |
| get_design_context truncated | Recoverable | get_metadata로 구조 파악 → 하위 노드별 개별 호출 |
| 노드 ID 존재하지 않음 | Blocking | "Figma에서 해당 노드를 찾을 수 없습니다" → URL 재확인 요청 |

### Phase 3.5 (유사 컴포넌트 스캔)

| 실패 유형 | 등급 | 복구 전략 |
|----------|------|----------|
| 유사 컴포넌트 0건 | Degraded | 화면 유형 기본 구성으로 대체. 정상 진행. |

### Phase 4 (Entity)

| 실패 유형 | 등급 | 복구 전략 |
|----------|------|----------|
| Swagger 스키마 없음 | Degraded | Phase 4 스킵. Phase 5에서 인라인 타입 사용 → 나중에 Entity 추가 |
| DTO 필드 타입 추론 실패 | Recoverable | 해당 필드 `unknown`으로 설정 + CP1에서 사용자 확인 |
| allOf/oneOf 복합 스키마 | Recoverable | 가장 유력한 해석으로 생성 + CP1에서 사용자 확인 |
| 기존 Entity 존재 (충돌) | Blocking | "이미 Entity가 존재합니다. 덮어쓸까요?" 질문 |

### Phase 5 (Code Generation)

| 실패 유형 | 등급 | 복구 전략 |
|----------|------|----------|
| Entity 타입 import 실패 | Recoverable | Phase 4 미실행 확인 → Phase 4 먼저 실행 |
| TDS 컴포넌트 Props 불일치 | Recoverable | `10-tds-detail-catalog.mdc` Rule 재확인 후 수정 |
| 기획서 인터랙션 해석 모호 | Degraded | 가장 일반적인 패턴으로 구현 + 사용자에게 "이 동작이 맞나요?" 확인 |
| Sub-phase 간 import 순환 | Blocking | FSD 의존성 방향 위반 감지 → 구조 재설계 후 재생성 |

### Phase 6 (i18n)

| 실패 유형 | 등급 | 복구 전략 |
|----------|------|----------|
| en/ko 키 불일치 | Recoverable | 한쪽 기준으로 자동 동기화 (en 기준, ko에 키 추가) |
| 네임스페이스 충돌 | Recoverable | 기존 JSON 병합 (새 키만 추가, 기존 키 유지) |
| 하드코딩 텍스트 잔존 | Recoverable | Phase 7(tsc) 후 코드 스캔으로 감지 → 자동 t() 변환 |

### Phase 7 (TypeScript 검증)

| 실패 유형 | 등급 | 복구 전략 |
|----------|------|----------|
| 타입 에러 < 5건 | Recoverable | 에러별 자동 수정 시도 (import 추가, 타입 캐스팅 등) |
| 타입 에러 5~15건 | Degraded | 카테고리별 그룹화 → 순차 수정 → 재검증 |
| 타입 에러 > 15건 | Blocking | 구조적 문제. Phase 5 산출물 재검토 필요 → 사용자에게 리포트 |

---

## 3. 복구 흐름도

```
Phase 실패 발생
  │
  ├─ Recoverable
  │   ├─ 대안 시도 (최대 2회)
  │   │   ├─ 성공 → 다음 Phase 진행
  │   │   └─ 실패 → Degraded로 격상
  │   └─ (대안 없음) → Degraded로 격상
  │
  ├─ Degraded
  │   ├─ 사용자에게 알림: "⚠️ {Phase}: {상황}. {대안}으로 진행합니다."
  │   ├─ 품질 저하 항목 기록 (CP에서 보고)
  │   └─ 다음 Phase 진행
  │
  └─ Blocking
      ├─ 사용자에게 질문: "🛑 {Phase}: {상황}. {필요한 정보}를 알려주세요."
      ├─ 사용자 응답 대기
      └─ 응답 수신 → Phase 재시도
```

---

## 4. Checkpoint에서의 실패 보고

각 Checkpoint에서 이전 Phase의 Degraded 항목을 요약 보고:

```
━━━ CHECKPOINT 1: Plan Review ━━━

⚠️ 품질 저하 항목:
- Phase 1: Swagger 미발견 → API 없이 진행 (Entity 수동 생성 필요)
- Phase 3: Figma MCP 미연결 → workloads 레이아웃 패턴 참조

위 상태로 진행할까요? [진행] [Swagger URL 제공] [Figma URL 제공]
```

---

## 5. 전체 파이프라인 중단 조건

다음 상황에서는 파이프라인을 즉시 중단하고 사용자에게 보고:

| 조건 | 중단 시점 |
|------|----------|
| 도메인명 확정 불가 | Phase 0.5 |
| 사용자가 CP 0.5에서 "중단" 선택 | CP 0.5 |
| 사용자가 CP 1에서 "중단" 선택 | CP 1 |
| Phase 5 Blocking 에러 + 사용자 미응답 | Phase 5 |
| tsc 에러 15건 초과 + 자동 수정 불가 | Phase 7 |
