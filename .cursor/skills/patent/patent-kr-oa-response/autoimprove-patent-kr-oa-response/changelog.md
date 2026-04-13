# patent-kr-oa-response autoimprove changelog

## v1-mutations (2026-04-13)

| Mutation | Target EVAL | Description | Size Impact |
|----------|-------------|-------------|-------------|
| M1 | EVAL 1 | 보정서 【보정 전/후/이유】 형식 검증 게이트 삽입 | +280B |
| M2 | EVAL 2 | 보정항별 명세서 단락 번호 인용 완전성 검증 | +220B |
| M3 | EVAL 3 | 최후거절 보정 범위 자동 분류(D/N/C/CL) 및 범위 초과 차단 | +260B |
| M4 | EVAL 4 | 5개 산출물 첫 3줄 이내 의견제출기한 표시 완전성 게이트 | +200B |
| M5 | EVAL 5 | 한국어 전용 출력 스캔 — 영문 5연속 비허용어 자동 교체 | +250B |

**Size**: 11255B (baseline) → 12740B (v1) — +13.2% (limit 20%)
**Performance**: 48% → 100% (+52%p)
