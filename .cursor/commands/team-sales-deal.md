## Team: Sales Deal

6명의 전문가 에이전트를 Parallel Research + Pipeline 패턴으로 오케스트레이션하여 계정 조사, 경쟁 인텔, 제안서 작성, 보안 QA, 딜 리뷰를 수행한다.

### Usage

```
/team-sales-deal {deal context or customer name}

# 예시
/team-sales-deal "고객사 A의 AI 인프라 구축 RFP 대응"
/team-sales-deal "B은행 온프레미스 GPU 클러스터 PoC 제안"
```

### Workflow

1. **[Parallel Research]**
   - **Account Researcher** — 회사 인텔, 의사결정자, 기술 스택, 페인 포인트, 구매 신호 조사
   - **Competitive Intel Agent** — 경쟁사 평가 현황, 강약점, 포지셔닝 배틀카드
2. **Proposal Drafter** — 계정 조사 + 경쟁 인텔 기반 세그먼트 맞춤 제안서 초안
3. **Security QA Agent** — 고객 세그먼트와 제안 아키텍처 기반 보안/주권/컴플라이언스 QA
4. **Deal Reviewer** — 전체 딜 패키지 완성도, 포지셔닝 품질, 딜 레디니스 품질 게이트
5. **[Review Loop]** — 미달 시 Proposal Drafter로 재라우팅 (최대 2회)

### Execution

코디네이터 스킬을 읽고 프로토콜을 따른다:

```
.cursor/skills/agent-teams/sales-deal/coordinator/SKILL.md
```

모든 전문가 에이전트는 `Task(subagent_type="generalPurpose")`로 디스패치된다.
워크스페이스: `_workspace/sales-deal/`
