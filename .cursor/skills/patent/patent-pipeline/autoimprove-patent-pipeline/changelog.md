# patent-pipeline autoimprove changelog

## v1-mutations (2026-04-13)

| Mutation | Target EVAL | Description | Size Impact |
|----------|-------------|-------------|-------------|
| M1 | EVAL 1 | Gate 1 Enforcement — `GATE 1 — Score: [X]/10 — Verdict: [PASS\|FAIL]` 구조화 블록 강제 출력 | +290B |
| M2 | EVAL 2 | Gate 2 Enforcement — CRITICAL 이슈 카운트·열거 및 패키징 차단 블록 강제 출력 | +340B |
| M3 | EVAL 3 | Persistence Checkpoint Gate — 각 Phase 후 기대 파일 존재 여부 디스크 검증 | +250B |
| M4 | EVAL 4 | Revision Cap Enforcement — `revision_iteration` 카운터로 Phase 5 최대 2회 제한 | +350B |
| M5 | EVAL 5 | Mandatory File Checklist Gate — 8개 필수 파일 존재 확인 후 Phase 6 완료 선언 | +523B |

**Size**: 11730B (baseline) → 13483B (v1) — +14.9% (limit 20%)
**Performance**: 45% → 96% (+51%p)
