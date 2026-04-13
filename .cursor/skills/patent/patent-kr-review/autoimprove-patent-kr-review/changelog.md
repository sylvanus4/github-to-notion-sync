# patent-kr-review Autoimprove Changelog

## v1-mutations (2026-04-13)

**Baseline → v1: 60% → 100% (+40%p)**

### Mutations Applied

1. **M1: 워크플로우 순서 강화** — Step 2(청구항 파싱) 직후 뒷받침 요건을 최우선 분석하도록 Step 5 우선 수행 지시 추가
2. **M2: 뒷받침 요건 완전성 게이트** — Step 5에 모든 청구항 구성요소가 매트릭스에 포함되었는지 확인하는 게이트 추가, ❌ 항목 필수 보완 목록 반영
3. **M3: 후견적 고찰 방지 체크리스트** — Step 3 진보성 분석에 4-item 후견적 고찰 방지 체크리스트 추가 (결합 동기 역추적 금지 등)
4. **M4: 종속항 참조 체인 검증** — Step 2에 종속항 참조 관계 파싱 및 체인 검증 지시 추가 (순환 참조, 존재하지 않는 항 번호 검출)
5. **M5: Anti-Pattern #2 강화 + Pre-Delivery Check** — Anti-Patterns에 조항 근거 없는 "필수 보완" 라벨 금지 규칙 강화, Step 11 Pre-Delivery Check 4-item 체크리스트 추가

### Compaction Applied

- Worked Example 섹션 축약
- Gotchas 섹션에서 워크플로우와 중복되는 항목 제거
- Step 8 교차 점검에서 종속항 참조 오류 제거 (Step 2에서 이미 검증)
- Step 10 파일 목록을 Output Artifacts 테이블 참조로 대체

### Size

- Baseline: 9695 bytes
- Final: 11538 bytes (+19.0%, within 20% gate)
