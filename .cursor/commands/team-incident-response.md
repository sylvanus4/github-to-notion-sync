## Team: Incident Response

5명의 전문가 에이전트를 Severity-Based Routing 패턴으로 오케스트레이션하여 인시던트 트리아지, 증거 수집, 근본 원인 분석, 수정 구현, 고객 커뮤니케이션을 수행한다.

### Usage

```
/team-incident-response {incident description}

# 예시
/team-incident-response "vLLM 서빙 노드 OOM 발생으로 추론 요청 전체 실패"
/team-incident-response "API 게이트웨이 504 타임아웃 다수 발생, 대시보드 로딩 불가"
```

### Workflow

1. **Triage Agent** — 심각도(SEV1-4) 분류, 블래스트 반경 결정, 인시던트 유형 카테고리화
2. **[Severity-Based Routing]**
   - SEV1/2 → Evidence Collector + Root Cause Analyzer 병렬 실행
   - SEV3/4 → Root Cause Analyzer만 실행
3. **[Confidence Gate]** — RCA 신뢰도 점수 기반 게이트
4. **Fix Implementer** — 확인된 근본 원인 기반 최소 수정 적용 + 롤백 전략
5. **Customer Comms Drafter** — (SEV1/2만) 고객 대상 인시던트 커뮤니케이션 초안

### Execution

코디네이터 스킬을 읽고 프로토콜을 따른다:

```
.cursor/skills/agent-teams/incident-response/coordinator/SKILL.md
```

모든 전문가 에이전트는 `Task(subagent_type="generalPurpose")`로 디스패치된다.
워크스페이스: `_workspace/incident-response/`
