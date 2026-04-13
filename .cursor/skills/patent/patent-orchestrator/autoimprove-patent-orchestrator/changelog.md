# patent-orchestrator autoimprove changelog

## v1-mutations (2026-04-13)

| Mutation | Target EVAL | Description | Size Impact |
|----------|-------------|-------------|-------------|
| M1 | EVAL 1 | Classification Output Gate — Step 1 후 `JURISDICTION: [US\|KR\|BOTH]` 구조화 블록 강제 출력 | +220B |
| M2 | EVAL 2 | Classification Output Gate — Step 1 후 `TASK_TYPE: [search\|scan\|draft\|review\|oa\|strategy]` 구조화 블록 강제 출력 | (M1에 포함) |
| M3 | EVAL 3 | Ambiguity Gate — 모호 요청 시 관할 또는 작업유형 우선순위로 정확히 1개 질문 강제 | +180B |
| M4 | EVAL 4 | Delegation Enforcement Gate — Step 3 디스패치 후 인라인 생성이 아닌 스킬 호출 검증 | +350B |
| M5 | EVAL 5 | Routing Log Completeness Gate — routing-log.json 필수 6개 필드 존재 확인 | +310B |

**Size**: 8600B (baseline) → 10060B (v1) — +17.0% (limit 20%)
**Performance**: 50% → 96% (+46%p)
