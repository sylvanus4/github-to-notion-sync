# patent-kr-strategy autoimprove changelog

## v1-mutations (2026-04-13)

| Mutation | Target EVAL | Description | Size Impact |
|----------|-------------|-------------|-------------|
| M1 | EVAL 1 | 타임라인 완전성 게이트 — 날짜/잔여일/필요조치 행별 점검 | +230B |
| M2 | EVAL 2 | 비용-권고 교차검증 게이트 — 권고별 ₩ 비용 추정 존재 확인 | +210B |
| M3 | EVAL 3 | 지연심사 경고 게이트 — 심사청구 기한/잔여일/도과 결과 인라인 명시 | +350B |
| M4 | EVAL 4 | 가속심사 자격 게이트 — 자격 유형(시행령 제9조) 및 충족 근거 명시 | +561B |

**Size**: 10031B (baseline) → 11382B (v1) — +13.5% (limit 20%)
**Performance**: 50% → 95% (+45%p)
