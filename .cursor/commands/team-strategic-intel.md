## Team: Strategic Intelligence

6명의 전문가 에이전트를 Fan-out/Fan-in 패턴으로 오케스트레이션하여 시장 스캐닝, 경쟁 분석, 전략 수립, 리스크 평가, 임원 브리프를 병렬로 수행한다.

### Usage

```
/team-strategic-intel {topic or question}

# 예시
/team-strategic-intel "2026 하반기 AI 인프라 시장 포지셔닝 전략"
/team-strategic-intel "ThakiCloud vs 하이퍼스케일러 경쟁 우위 분석"
```

### Workflow

1. **[Parallel Fan-out]**
   - **Market Scanner** — 시장 트렌드, 규모 데이터, 신호 스캔
   - **Competitive Analyst** — 경쟁사 포지셔닝, 움직임, 강약점 분석
2. **[Fan-in] Strategic Planner** — 시장 + 경쟁 분석을 전략 프레임워크로 종합
3. **Risk Assessor** — 확률-영향 스코어링, 시나리오 분석, 완화 계획
4. **Executive Brief Writer** — 모든 팀 산출물을 C-suite 의사결정용 인텔리전스 브리프로 종합

### Execution

코디네이터 스킬을 읽고 프로토콜을 따른다:

```
.cursor/skills/agent-teams/strategic-intel/coordinator/SKILL.md
```

모든 전문가 에이전트는 `Task(subagent_type="generalPurpose")`로 디스패치된다.
워크스페이스: `_workspace/strategic-intel/`
