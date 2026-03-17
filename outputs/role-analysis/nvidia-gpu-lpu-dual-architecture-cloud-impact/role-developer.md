# 개발자 관점 분석: NVIDIA GPU+LPU 이중 구조 도입 — ThakiCloud 플랫폼

## 관련도: 9/10

**분석 일자**: 2026-03-17

**근거**: LPU 지원 추가는 백엔드 API, 리소스 스케줄링 로직, Device Plugin/CDI 통합, CI/CD 파이프라인, 테스트 인프라 전반에 직접적인 코드 변경을 요구한다. ThakiCloud 스택(Go Fiber, PostgreSQL, NATS, Kueue, Slinky)의 핵심 레이어가 모두 영향받으며, 신규 런타임(Groq SDK)과 이원화된 추론 스택 운영으로 인한 개발/테스트 부담이 크다.

---

## 1. 구현 복잡도

### 예상 난이도: **High**

LPU 도입 시 필요한 코드 변경 범위는 다음과 같다.

| 레이어 | 변경 범위 | 예상 LOC | 비고 |
|--------|--------|----------|------|
| **리소스 타입 정의** | 신규 | 200~500 | `accelerator` enum 확장, LPU 리소스 스키마 추가 |
| **Device Plugin / CDI** | 신규 | 500~2000 | 공식 LPU 플러그인 미확인, CDI 기반 커스텀 개발 필요 가능성 |
| **Kueue 큐/클러스터** | 수정 | 100~300 | extended resource 제약으로 추가 개발 필요 (2024 기준) |
| **Slinky GRES** | 수정 | 200~800 | `gres.conf` 커스텀, Slinky 포크 또는 플러그인 검토 |
| **API 게이트웨이** | 수정 | 300~500 | 추론 엔드포인트 라우팅 (GPU vs LPU), 모델–가속기 매핑 |
| **백엔드 서비스** | 수정 | 400~800 | 작업 생성/조회 API에 가속기 타입 필드, 라우팅 정책 |
| **DB 스키마** | 수정 | 50~150 | `accelerator_type`, `lpu_count` 등 컬럼 추가 |
| **모니터링 익스포터** | 신규 | 200~400 | LPU 전용 메트릭 (TTFT, 토큰/초, 대역폭) |

**총 예상 범위**: 2,000~5,000 LOC (신규 + 수정)

### 주요 기술 결정 포인트

1. **Device Plugin 전략**
   - 공식 NVIDIA/Kubernetes LPU 플러그인 미확인 → CDI(Container Device Interface) 기반 커스텀 개발 필요 가능성
   - Groq SDK와의 통합 시점, `device-plugin` API 버전 호환성 검증 필요

2. **Kueue extended resource**
   - 2024 기준 extended resource 지원 제한 → Kueue 최신 버전(2025) 재평가 후 네이티브 지원 여부 확인
   - 미지원 시 GPU/LPU 분리 클러스터 + API 레벨 라우팅으로 우회 구현 가능하나, 운영 복잡도 증가

3. **이원화된 추론 스택**
   - GPU: vLLM, TGI, Triton 등 기존 파이프라인
   - LPU: Groq API, vLLM-Groq, ONNX Runtime LPU 백엔드 등
   - CI/CD·테스트·배포 파이프라인이 2배로 분기될 수 있음

---

## 2. 테스트 요구사항

### 필요 테스트 유형

| 유형 | 범위 | 우선순위 |
|------|------|----------|
| **단위 테스트** | 리소스 타입 파싱, 라우팅 정책 로직, 가속기 매핑 검증 | P0 |
| **통합 테스트** | API → Kueue 큐 제출, Slinky GRES 할당, Pod 스케줄링 | P0 |
| **E2E 테스트** | GPU/LPU 워크로드 end-to-end (추론 요청 → 응답) | P0 |
| **성능 테스트** | TTFT, 토큰/초, 대기 시간 벤치마크 | P1 |
| **회귀 테스트** | 기존 GPU 워크로드 동작 영향 없음 검증 | P0 |

### 커버리지 목표

- **기존 GPU 경로**: LPU 추가 시 회귀 없음 보장 — 기존 테스트 100% 통과
- **LPU 신규 경로**: `accelerator_type=lpu` 분기 커버리지 80% 이상
- **라우팅 정책**: 경계값 테스트 (GPU/LPU 선택, fallback, 미지원 모델 요청)

### 핵심 엣지 케이스

1. **LPU 미지원 모델 요청** → GPU로 fallback 또는 400 에러 응답
2. **LPU 노드 부재 시** → 큐 대기 또는 503 에러
3. **혼합 워크로드** (학습+추론) → LPU는 학습 미지원, GPU로 라우팅
4. **Device Plugin 장애** → LPU 리소스 미노출, 스케줄러 무시
5. **Kueue extended resource 미지원** → 분리 클러스터 모드로 동작

### LPU 통합 테스트 전략

- **Mock 기반**: LPU 하드웨어 없이 Groq API mock 또는 로컬 스텁으로 단위/통합 테스트
- **실기기**: LPU 1노드 파일럿에서 E2E·성능 테스트 (CI 외부, 별도 스테이징)
- **테스트 데이터**: 고정 시드 추론 요청, TTFT·토큰/초 재현 가능한 벤치마크 스크립트

---

## 3. CI/CD 영향

### 파이프라인 변경 필요

| 단계 | 변경 내용 |
|------|----------|
| **빌드** | LPU 전용 이미지 추가 (Groq SDK, LPU 런타임 포함), multi-stage 빌드 분기 |
| **테스트** | GPU/LPU 워크로드별 테스트 job 분리 또는 매트릭스 빌드 |
| **배포** | LPU 노드 풀 별도 Helm values, ArgoCD ApplicationSet 추가 |
| **검증** | LPU 노드 라벨·리소스 노출 확인 검증 스텝 추가 |

### 빌드 시간 영향

- **LPU 전용 이미지**: Groq SDK·런타임 추가로 이미지 크기 500MB~1GB 증가 가능
- **테스트 매트릭스**: GPU + LPU 분기 시 테스트 시간 1.5~2배 증가
- **권장**: LPU 테스트를 선택적(optional) job으로 두고, main 브랜치·릴리스 시에만 실행

### 배포 전략

- **단계적 롤아웃**: GPU 클러스터 유지, LPU 노드 풀을 별도 노드 그룹으로 추가
- **Feature flag**: `LPU_ENABLED` 플래그로 API 라우팅·큐 제출 활성화 제어
- **롤백**: LPU 노드 풀 비활성화, API에서 LPU 라우팅 제거로 즉시 복귀 가능

---

## 4. 문서화 필요

### 개발자 온보딩 문서 항목

1. **LPU 아키텍처 개요**
   - LPU vs GPU 차이, 워크로드 분류(학습 vs 추론)

2. **로컬 개발 환경**
   - LPU 없이 Mock/Groq Cloud API로 개발하는 방법
   - GPU vs LPU 분기 테스트 실행 방법

3. **리소스 타입·라우팅 정책**
   - `accelerator_type` enum, 모델–가속기 매핑 테이블
   - API 요청 시 GPU/LPU 선택 로직

4. **Device Plugin / CDI**
   - LPU Device Plugin 설치·설정 (확정 시)
   - CDI 디바이스 노출 확인 방법

5. **Kueue·Slinky 설정**
   - LPU 큐 정의, GRES 설정 예시
   - 트러블슈팅: 큐 대기, 리소스 미할당 시 점검

6. **모니터링·디버깅**
   - LPU 메트릭 (TTFT, 토큰/초, 대역폭)
   - VictoriaMetrics 대시보드, 로그 수집 경로

7. **API 문서**
   - 추론 엔드포인트에 `accelerator_preference` 파라미터 추가
   - 에러 코드 (LPU 미지원, 노드 부재 등)

### ADR 작성 필요 여부

- **예**: `ADR-XXX: LPU 이종 가속기 도입 및 라우팅 정책` — 아키텍처 결정·대안 비교·선택 근거 기록

### Changelog 항목

- `[feat] LPU 추론 엔드포인트 및 리소스 스케줄링 지원`
- `[feat] accelerator_type: gpu | lpu 선택 옵션 추가`
- `[enhance] Kueue/Slinky LPU 큐 및 GRES 설정`

---

## 5. 기술 스파이크 계획

### 가장 먼저 실험해야 할 코드 레벨 PoC (우선순위)

#### 1. CDI 기반 LPU 디바이스 노출 PoC (2주)

**목표**: Kubernetes에서 LPU를 extended resource로 인식시키는 최소 경로 검증

**작업**:
- CDI(Container Device Interface) 스펙 확인, Groq LPU용 CDI 스펙 작성
- `device-plugin` 또는 CDI 호환 구현체로 LPU 1노드에서 `nvidia.com/lpu` 리소스 노출
- `kubectl describe node`에서 `lpu` 리소스 확인 가능 여부 검증

**산출물**: CDI 스펙 초안, `docker run` 또는 `kubectl run`으로 LPU 디바이스 주입 테스트 스크립트

**결과에 따른 다음 단계**:
- 성공 → Kueue/Slinky GRES 연동 PoC
- 실패 → 분리 클러스터 + API 라우팅 전략으로 전환

---

#### 2. Groq API 호출 래퍼 및 라우팅 로직 PoC (1주)

**목표**: Go 백엔드에서 GPU 추론과 LPU 추론을 분기하는 최소 코드 검증

**작업**:
- Groq Cloud API (또는 온프레미스 Groq SDK) 호출을 위한 Go 클라이언트 래퍼
- `InferenceRequest`에 `AcceleratorPreference: "gpu" | "lpu" | "auto"` 필드 추가
- `auto` 시 워크로드 특성(배치 vs 실시간, TTFT 민감도) 기반 라우팅 로직 스텁

**산출물**: `pkg/inference/` 디렉터리 내 `lpu_client.go`, `routing.go` 프로토타입, 단위 테스트

---

#### 3. Kueue Extended Resource 현황 재평가 (1주)

**목표**: Kueue 2025 기준으로 extended resource 지원 여부 확인

**작업**:
- Kueue 최신 버전(2025) 릴리스 노트·이슈 검색
- `ResourceFlavor`에 `customResource` 또는 `extendedResource` 예시 확인
- GPU/LPU 이원 큐가 Kueue 네이티브로 가능한지 검증

**산출물**: Kueue 로드맵 정리, 가능 시 YAML 예시, 불가 시 커스텀 큐 구현 범위 정의

---

#### 4. Slinky GRES LPU 타입 추가 실험 (3~5일)

**목표**: Slurm `gres.conf`에 `lpu` 타입 추가 후 Slinky에서 인식 여부 테스트

**작업**:
- Slinky 문서·이슈에서 GRES 확장 사례 검색
- `gres.conf`에 `lpu` 타입 추가, `scontrol show node`에서 `Gres=lpu` 확인
- Slinky Pod에서 해당 GRES 요청 시 스케줄링 동작 검증

**산출물**: GRES LPU 지원 가능 여부 보고서, 불가 시 대안(분리 클러스터·API 라우팅) 정리

---

### PoC 실행 순서 권고

1. **Groq API 래퍼** (1주) — 하드웨어 의존 없음, 즉시 착수 가능
2. **Kueue 재평가** (1주) — 스케줄링 전략 결정에 필수
3. **CDI LPU 디바이스 노출** (2주) — LPU 노드 확보 후 진행
4. **Slinky GRES** (3~5일) — CDI 또는 Device Plugin 검증 후 연동

---

## 6. 리스크 및 블로커

| 리스크 | 완화 방안 |
|--------|----------|
| **공식 LPU Device Plugin 부재** | CDI 기반 커스텀 개발, 또는 Groq Cloud API로 우선 지원 |
| **Kueue extended resource 미지원** | 분리 클러스터 + API 라우팅 전략 |
| **이원화된 CI/CD 부담** | LPU 테스트를 optional job, Feature flag로 단계적 도입 |
| **Groq SDK/런타임 미성숙** | Groq Cloud API 우선, 온프레미스는 나중에 검토 |

---

*문서 버전: 1.0 | 작성: 개발자 관점 분석 (role-developer)*
