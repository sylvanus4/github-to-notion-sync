# patent-kr-ai-invention Autoimprove Changelog

## v1-mutations (2026-04-13)

**Baseline → v1: 56% → 100% (+44%p)**

### Mutations Applied

1. **M1: AI 유형 사전 분류 필수 출력 게이트** — Step 0(b)에 분류 결과를 `> AI 유형: [선택]` 형식으로 분석 최상단에 명시하도록 강제, 분류 없이 Step 1 진행 불가
2. **M2: HW-SW 협동 점검 파일 생성 필수 게이트** — Step 2 완료 시 `hw-sw-cooperation-check.md` 반드시 생성, 5개 체크 항목의 ✅/❌ 판정과 근거 포함 필수, 미생성 시 Step 3 진행 불가
3. **M3: 10항목 체크리스트 완전 충족 게이트** — Step 6 체크리스트 10개 항목 전부에 ✅/❌ 판정 기록 필수, 비고란에 판정 근거 명시, 빈 셀 있으면 Step 7 진행 불가
4. **M4: ❌ 항목 필수 보완 문안 제시 게이트** — Step 7에서 ❌ 판정 모든 항목에 before/after 또는 보강 문안 필수 제시, 누락 시 Step 8 진행 불가
5. **M5: 프로세서 단독 통과 금지 Pre-Delivery Check** — Pre-Delivery Check에 4번 항목 추가: "프로세서에 의해 수행되는" 문구만으로 HW-SW ✅ 처리 금지, 구체적 정보처리 과정 결합 기재 확인 필수

### Size

- Baseline: 12329 bytes
- Final: 13600 bytes (+10.3%, within 20% gate)
