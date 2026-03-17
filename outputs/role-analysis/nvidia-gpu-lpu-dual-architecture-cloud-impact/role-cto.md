# CTO 관점 분석: NVIDIA GPU+LPU 이중 구조 도입 — ThakiCloud 전략적 대응

## 관련도: 9/10

**분석 일자**: 2026-03-17

**근거**: GPU 클라우드 제공사의 핵심 인프라 전략 결정. 아키텍처·성능·보안·엔지니어링 역량 전반에 직접 영향. Slinky/Kueue 기반 스택 변경 범위가 큼.

---

## 기술 요약

- **Vera Rubin LPX 랙**: 256 Groq 3 LPU, 150 TB/s 대역폭 (GPU 22 TB/s 대비 약 7배) — 추론 워크로드 TTFT(Time To First Token)에 유리
- **NVIDIA–Groq $20B 라이선스**: 2027년까지 LPU/LPX 10배 성장 전망, 생태계 표준화 가속
- **Slinky GRES**: Slurm-on-K8s GRES 메커니즘으로 LPU 이론적 지원 가능하나 공식 플러그인 미확인
- **Kueue 제약**: 2024 기준 extended resource 지원 제한 — GPU/LPU 이원화 스케줄링에 추가 개발 필요
- **TTFT 격차**: LPU 10ms vs GPU 50–100ms — AI 에이전트·실시간 추론 SLO 충족에 LPU가 필수에 가까움

---

## 1. 아키텍처 영향 평가 (관련도: 9/10)

### 현재 스택 대비 변경 범위

ThakiCloud는 K8s + Slinky(Slurm-on-K8s) 기반으로 H100/B200 GPU를 오케스트레이션하고 있다. LPU 도입 시 영향 범위는 다음과 같다.

| 레이어 | 영향 수준 | 변경 포인트 |
|--------|-----------|-------------|
| **스케줄러** | 높음 | Slinky GRES에 LPU 리소스 타입 추가, Kueue extended resource 확장 또는 별도 큐 |
| **노드 레이블/테인트** | 중간 | `accelerator=nvidia-lpu` 등 신규 라벨링, 워크로드 배치 정책 |
| **런타임** | 높음 | LPU 전용 드라이버/런타임 (Groq SDK), GPU와 다른 메모리/컨텍스트 모델 |
| **API 게이트웨이** | 중간 | 추론 엔드포인트 라우팅 (GPU vs LPU 선택), 모델–가속기 매핑 |
| **모니터링** | 중간 | LPU 전용 메트릭 (토큰/초, TTFT, 대역폭), 기존 VictoriaMetrics 대시보드 확장 |

**시스템 설계 변경**: 단일 GPU 클러스터에서 **이종 가속기 하이브리드 클러스터**로 전환. 워크로드 분류(학습/파인튜닝 vs 추론/에이전트)에 따라 GPU/LPU 라우팅 결정 필요.

**의존성 분석**: Slinky GRES 플러그인 공식 지원 여부가 핵심. 미지원 시 Slurm `gres.conf` 커스텀 확장 또는 Slinky 포크 검토 필요 — SchedMD 업스트림 의존성 리스크 존재.

---

## 2. 기술 부채 및 마이그레이션 리스크

### 주요 기술 결정 포인트

1. **스케줄러 전략**
   - **옵션 A**: Kueue extended resource로 LPU 큐 추가 → Kueue 2024 제약으로 추가 개발 필요
   - **옵션 B**: Slinky GRES에 LPU 타입 등록 → Slurm 플러그인 생태계 의존
   - **옵션 C**: GPU/LPU 분리 클러스터 + API 레벨 라우팅 → 운영 복잡도 증가, 비용 최적화 어려움

2. **런타임 통합**
   - Groq LPU는 CUDA 호환 아님. Triton/ONNX Runtime 등 추론 스택의 LPU 백엔드 지원 여부 확인 필요
   - 기존 GPU 기반 파이프라인(vLLM, TGI 등)과 LPU 전용 스택(vLLM-Groq, Groq API) 이원화 시 CI/CD·테스트 부담 증가

3. **마이그레이션 리스크**
   - **Vendor Lock-in**: NVIDIA–Groq 라이선스 구조에 따른 장기 공급·가격 리스크
   - **플러그인 미성숙**: Slinky GRES LPU 지원이 커뮤니티/비공식 수준일 경우 유지보수 부담
   - **이원화 부채**: GPU/LPU 두 스택 병행 운영 시 인시던트 대응·온콜 복잡도 2배화

---

## 3. 성능/SLO 영향

### 추론 워크로드 SLO 관점

| 지표 | GPU (H100) | LPU (Groq 3) | ThakiCloud SLO 영향 |
|------|------------|--------------|---------------------|
| **TTFT** | 50–100ms | ~10ms | 에이전트·챗봇 대화형 SLO 충족에 LPU 유리 |
| **토큰/초** | 높음 (긴 시퀀스) | 매우 높음 (짧은 시퀀스) | 배치 추론 vs 실시간 추론 워크로드 분리 |
| **대역폭** | 22 TB/s | 150 TB/s | 메모리 바운드 추론에서 LPU 우위 |
| **학습/파인튜닝** | 지원 | 미지원 | GPU 전용 유지, LPU는 추론 전용 |

**트레이드오프**: GPU는 범용성·학습·긴 시퀀스에 강점, LPU는 TTFT·짧은 시퀀스·에이전트형 추론에 강점. **하이브리드 라우팅**으로 워크로드 특성에 맞게 분배하는 설계가 필요.

**모니터링 요구사항**: p50/p95/p99 TTFT, 토큰 처리량, 가속기별 큐 대기 시간, OOM/타임아웃 비율. 기존 VictoriaMetrics에 LPU 메트릭 익스포터 추가.

---

## 4. 보안 아키텍처

### 이종 가속기 도입 시 보안 포스처 변화

1. **격리 경계**
   - GPU: K8s namespace + Keycloak JWT 기반 RBAC, 네트워크 정책
   - LPU: 동일 RBAC 적용 시 **LPU 노드 풀의 네트워크 세그멘테이션** 검토 — Groq 드라이버·API 트래픽이 GPU와 다른 경로일 수 있음

2. **모델/가중치 접근**
   - LPU는 전용 메모리 모델. GPU와 다른 **모델 로딩·캐싱 경로** — 보안 스캔·버전 검증 파이프라인 이원화 필요

3. **STRIDE 관점**
   - **Spoofing**: LPU 엔드포인트에 대한 인증·API 키 검증 (GPU와 동일 정책)
   - **Tampering**: 모델 아티팩트 무결성 검증 (LPU 전용 체크섬/서명)
   - **Repudiation**: LPU 추론 로그·감사 추적 — NATS/로그 파이프라인에 LPU 이벤트 포함

4. **컴플라이언스**
   - B2B 에어갭 환경에서 LPU 노드의 **외부 연결 요구사항** (Groq 라이선스/업데이트) — 이그레스 정책과 충돌 가능성 검토

---

## 5. 엔지니어링 역량 요구

### LPU 스택 운영을 위한 신규 역량

| 역량 | 현재 수준 | 필요 수준 | 확보 방안 |
|------|-----------|-----------|-----------|
| **Slurm GRES/플러그인** | Slinky 사용 경험 | GRES 커스텀 타입 설계·디버깅 | SchedMD 문서·커뮤니티, 또는 외부 컨설팅 |
| **Groq SDK/런타임** | 없음 | LPU 추론 파이프라인 구축 | Groq 공식 문서·POC 1–2주 |
| **하이브리드 스케줄링** | Kueue GPU 큐 | GPU+LPU 이원 큐·라우팅 정책 | Kueue 이슈 트래킹, 커스텀 개발 |
| **LPU 메트릭/관측** | GPU Operator 기반 | LPU 전용 익스포터·대시보드 | Prometheus exporter 개발 또는 Groq 제공 도구 |

**온보딩/교육**: LPU 아키텍처·Groq API 워크샵 1회, Slurm GRES 심화 세션. 예상 2–3일 집중 교육.

---

## 6. 즉각적 기술 액션 아이템 (3가지)

### 1. Slinky GRES LPU 지원 가능성 검증 (2주)

- SchedMD Slinky 이슈/문서에서 LPU·Groq·GRES 확장 사례 검색
- Slurm `gres.conf`에 `lpu` 타입 추가 후 Slinky에서 인식 여부 테스트
- **산출물**: GRES LPU 지원 가능 여부 보고서, 불가 시 대안(분리 클러스터·API 라우팅) 정리

### 2. Groq LPU 추론 POC (3주)

- Groq Cloud API 또는 온프레미스 LPU 1노드로 vLLM/ONNX 기반 추론 파이프라인 구축
- TTFT·토큰/초 벤치마크, ThakiCloud 목표 SLO와 비교
- **산출물**: POC 리포트, GPU vs LPU 비용·성능 비교표, 도입 ROI 초안

### 3. Kueue Extended Resource 현황 재평가 (1주)

- Kueue 최신 버전(2025)에서 extended resource·custom resource 지원 상태 확인
- GPU/LPU 이원 큐 설계가 Kueue 네이티브로 가능한지 검증
- **산출물**: Kueue 로드맵 정리, 필요 시 커스텀 큐 구현 범위 정의

---

## 기술 의사결정 권고

| 구분 | 권고 |
|------|------|
| **즉시 조치** | 위 3개 액션 아이템 병렬 착수 (GRES 검증 + Groq POC + Kueue 재평가) |
| **로드맵 반영** | 2026 Q3–Q4 LPU 파일럿 클러스터 검토, 2027 NVIDIA–Groq 생태계 성숙도 모니터링 |
| **위험 완화** | Vendor lock-in 완화를 위해 AMD MI300·Trainium2 등 대안 가속기 동시 검토, 멀티벤더 전략 수립 |

---

*문서 버전: 1.0 | 작성: CTO 관점 분석 (role-cto)*
