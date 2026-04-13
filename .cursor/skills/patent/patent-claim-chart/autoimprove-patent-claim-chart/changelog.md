# patent-claim-chart autoimprove changelog

## v1-mutations (2026-04-13)

### M1 — Citation Completeness Scan (EVAL 1)
- "Met" 판정에 반드시 page/paragraph/figure 인용을 포함하도록 강제
- 인용 없는 "Met"은 invalid로 명시

### M2 — Gap Specificity Scan (EVAL 2)
- "Not Met" 판정에 구체적 갭 서술을 강제
- "absent" 같은 모호한 서술 invalid로 명시

### M3 — Independent-First Gate (EVAL 3)
- 독립항 차트 완료 전 종속항 차트 시작 금지 강화
- "Independent-First Gate" 검증 절차 추가

### M4 — Preamble Row Gate (EVAL 4)
- Preamble을 반드시 row P로 차트하도록 강제
- 생략 시 hard error로 명시

### M5 — Summary Count Consistency Check (EVAL 5)
- Pre-Delivery Check에 수학적 검증 절차 추가
- 상세 행 카운트와 요약 테이블 불일치 시 delivery 차단
- Preamble row 존재 확인 항목 추가

### Results
- Baseline: 64% avg pass rate
- v1-mutations: 100% avg pass rate
- Size: 8751 → 10026 bytes (+14.6%, within 20% gate)
