# 보안 엔지니어 관점 분석: NVIDIA GPU+LPU 이중 구조 도입 — ThakiCloud 플랫폼 보안 영향

## 관련도: 9/10

**분석 일자**: 2026-03-17

**근거**: 이종 가속기(GPU+LPU) 도입은 인증·인가, 데이터 격리, 공격 표면, 컴플라이언스 전반에 직접적 영향을 미친다. Thaki Suite(IAM, ABAC, STS, VXLAN)와 AI Platform(RBAC, Keycloak JWT)의 이원화된 보안 모델에 LPU 레이어가 추가되며, B2B 에어갭 정책과 멀티테넌시 분리 요구사항이 강화된다. 드라이버·펌웨어·런타임 공격 표면 확대로 위협 모델 재정의가 필수이다.

---

## 1. 위협 모델 (STRIDE): LPU 도입 시 신규/변경 위협

### Spoofing (스푸핑)
- **신규 위협**: LPU Device Plugin 또는 GRES 스케줄러를 사칭하여 LPU 리소스를 부당 할당받는 워크로드
- **변경 위협**: Keycloak JWT 기반 인증이 GPU/LPU 이원화된 엔드포인트에 적용될 때, LPU 전용 API 경로에서 토큰 검증 누락 가능성
- **완화**: Device Plugin 서비스 계정 RBAC 강화, LPU 엔드포인트에 동일한 JWT 검증 미들웨어 적용

### Tampering (변조)
- **신규 위협**: Groq LPU 드라이버/펌웨어 업데이트 시 무결성 검증 없이 배포될 경우, 악성 펌웨어 주입
- **변경 위협**: Spectrum-X 인터커넥트를 통한 GPU↔LPU 간 데이터 전송 시 중간자 변조(MITM) 가능성
- **완화**: 펌웨어 서명 검증, 인터커넥트 구간 TLS/mTLS 적용, 이미지·아티팩트 무결성 검증(SBOM, cosign)

### Repudiation (부인)
- **신규 위협**: LPU 리소스 할당·해제, 추론 요청·응답에 대한 감사 로그 미수집
- **변경 위협**: 기존 GPU 감사 로그와 LPU 이벤트가 분리되어 포렌식 시 시퀀스 재구성 어려움
- **완화**: 통합 감사 로그 스키마(가속기 타입, 노드 ID, 테넌트, 타임스탬프), VictoriaLogs/VictoriaMetrics에 LPU 이벤트 통합

### Information Disclosure (정보 유출)
- **신규 위협**: LPU 노드 간 메모리 공유 또는 컨테이너 이스케이프 시 다른 테넌트의 추론 입력/출력 노출
- **변경 위협**: Groq SDK/런타임 로그에 모델 가중치·프롬프트·PII가 평문으로 기록될 위험
- **완화**: LPU 전용 네임스페이스 격리, 로그 PII 스크러빙, 런타임 메모리 격리 검증

### Denial of Service (서비스 거부)
- **신규 위협**: LPU 큐를 고의로 점유하여 다른 테넌트의 추론 요청 지연/실패 유도
- **변경 위협**: Spectrum-X 대역폭 고갈로 GPU↔LPU 간 통신 병목, 전체 클러스터 성능 저하
- **완화**: 테넌트별 LPU 할당 쿼터, rate limiting, 대역폭 QoS 정책

### Elevation of Privilege (권한 상승)
- **신규 위협**: LPU Device Plugin 또는 Kubelet 확장이 privileged 컨테이너로 실행될 경우 호스트 권한 탈취
- **변경 위협**: Slinky GRES 커스텀 플러그인이 root 권한으로 LPU 리소스 제어 시 컨테이너→호스트 이스케이프
- **완화**: 최소 권한 원칙, Device Plugin을 non-root로 실행 가능한지 검토, Pod Security Standards(restricted) 적용

---

## 2. 공격 표면 분석

### Groq 드라이버
- **위치**: LPU 노드의 커널/유저스페이스 드라이버
- **리스크**: 드라이버 버그를 통한 커널 메모리 읽기/쓰기, DMA 기반 공격
- **대응**: 드라이버 버전 고정, CVE 모니터링, Groq 보안 권고 구독

### Device Plugin
- **위치**: K8s Device Plugin API를 통해 LPU 리소스 노출
- **리스크**: 플러그인 로직 오류로 잘못된 리소스 할당, 플러그인 자체가 악성 코드일 경우 클러스터 전체 제어
- **대응**: 공식/검증된 Device Plugin 사용, 플러그인 이미지 서명 검증, 네트워크 정책으로 플러그인 통신 제한

### GRES (Generic Resource)
- **위치**: Slurm/Slinky GRES 메커니즘
- **리스크**: GRES 설정 오류로 테넌트 간 LPU 리소스 오버레이, 스케줄러 우회
- **대응**: GRES 설정 검증, Slinky 업스트림 LPU 지원 여부 확인 후 커스텀 확장 시 보안 리뷰

### 컨테이너 런타임
- **위치**: containerd/CRI-O, LPU 디바이스 마운트
- **리스크**: `/dev/groq*` 등 LPU 디바이스 노드가 과도하게 노출되면 컨테이너 내부에서 호스트 리소스 직접 접근
- **대응**: 필요한 디바이스만 cgroup으로 제한, seccomp/AppArmor 프로파일로 syscall 제한

---

## 3. 멀티테넌시 분리: LPU 노드에서 테넌트 간 데이터 격리

### 네임스페이스 격리
- K8s 네임스페이스별 RBAC으로 LPU 리소스 접근 제한
- NetworkPolicy로 LPU 노드 간 테넌트 트래픽 분리
- VXLAN(Thaki Suite)과 K8s 네트워크 정책 연동하여 논리적 격리

### 리소스 할당 격리
- Slinky/Kueue에서 테넌트별 LPU 쿼터(예: tenant-a: 32 LPU, tenant-b: 64 LPU) 설정
- GPU와 동일하게 `nvidia.com/gpu` 패턴으로 `groq.com/lpu` 리소스 타입 등록 후 요청/제한 적용

### 메모리·컨텍스트 격리
- Groq LPU의 메모리 모델이 GPU와 다를 수 있음 — LPU 내부 메모리 분할이 하드웨어/펌웨어 수준에서 지원되는지 확인
- 컨테이너당 전용 LPU 인스턴스 할당으로 소프트웨어적 멀티테넌시 회피(단일 테넌트 per LPU)

### 데이터 인라인 격리
- 추론 입력/출력이 네트워크·스토리지 구간에서 암호화(TLS, 암호화된 볼륨)
- NATS JetStream 등 메시지 큐에서 테넌트별 채널/스트림 분리

---

## 4. B2B 에어갭 정책: LPU 환경에서의 이그레스 제한 전략

### 네트워크 이그레스 제한
- LPU 노드에 NetworkPolicy 적용: 외부 인터넷, 공용 API 엔드포인트 차단
- B2B 전용 LPU 풀은 GPU 풀과 동일하게 에어갑 네트워크 세그먼트에 배치
- Spectrum-X 인터커넥트는 GPU↔LPU 간 내부 통신만 허용, 외부 이그레스 불가

### BYOK 라우팅 제한
- B2C의 BYOK(고객 API 키 라우팅)는 LPU 풀에서 비활성화 — B2B LPU는 Thaki 분산 모델만 허용
- LPU 노드에서 외부 LLM API 호출(OpenAI, Anthropic 등) 차단

### 펌웨어·드라이버 업데이트
- 에어갭 환경에서는 오프라인 패키지로 업데이트, 외부 다운로드 금지
- 업데이트 전 SBOM·서명 검증, 변경 이력 감사 로그

### 모니터링 이그레스
- VictoriaMetrics/VictoriaLogs 수집이 내부 전용 네트워크로 제한
- 알럿·대시보드 접근은 Thaki Suite IAM으로 통제

---

## 5. 보안 강화 우선순위 3가지: 즉각 실행 가능한 조치

### 1. LPU 리소스 타입 및 Device Plugin 보안 기준 수립
- LPU Device Plugin 도입 전 **보안 체크리스트** 작성: 이미지 서명, non-root 실행 가능성, 네트워크 정책
- Slinky GRES LPU 확장 시 **코드 리뷰** 및 **최소 권한** 원칙 적용
- **실행 시점**: LPU POC/파일럿 시작 전

### 2. 통합 감사 로그 및 LPU 이벤트 수집
- LPU 할당/해제, 추론 요청(테넌트, 모델, 타임스탬프)을 기존 GPU 감사 로그와 동일 스키마로 수집
- VictoriaLogs에 `accelerator_type=lpu` 필드 추가, 보안 이벤트 알럿(비정상 할당, 권한 오류) 설정
- **실행 시점**: LPU 베타 배포와 동시

### 3. B2B LPU 풀 네트워크 정책 및 에어갭 검증
- B2B 전용 LPU 노드 풀에 **기본 거부** NetworkPolicy 적용 후 필요한 내부 통신만 화이트리스트
- 에어갭 검증: LPU 노드에서 `curl`/`wget`으로 외부 도메인 접근 시도 시 실패하는지 확인
- **실행 시점**: B2B LPU 서비스 오픈 전 필수 검증

---

## 보안 요약

- LPU 도입은 **드라이버·펌웨어·Device Plugin·GRES·컨테이너 런타임** 공격 표면을 확대하며, STRIDE 위협 모델 재정의 필요
- **멀티테넌시**는 네임스페이스·리소스 쿼터·메모리 격리로 보완하며, LPU 메모리 모델 검증 필요
- **B2B 에어갭**은 네트워크 이그레스 차단, BYOK 비활성화, 오프라인 업데이트로 유지
- **즉시 조치**: Device Plugin 보안 기준, 통합 감사 로그, B2B LPU 네트워크 정책 검증
