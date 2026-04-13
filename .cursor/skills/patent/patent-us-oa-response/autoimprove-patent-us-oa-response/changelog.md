# patent-us-oa-response Autoimprove Changelog

## v1-mutations (2026-04-13)

**Baseline → v1: 52% → 100% (+48%p)**

### Mutations Applied

1. **M1: 보정 마크업 일관성 게이트** — Step 3에 Markup Consistency Gate 추가: 모든 보정 청구항이 `[[...--]]` (추가), `[[--...--]]` (삭제) 마크업을 동일하게 사용하는지 확인, 불일치 시 수정 후 진행
2. **M2: 명세 단락 인용 완전성 게이트** — Step 3 Rules에 모든 `[[...--]]` 추가 뒤 `(Support: ¶[xxxx])` 형식 명세 인용 필수 규칙 추가, 인용 없는 보정 라인 최종 패키지 포함 불가
3. **M3: 거절별 차별화된 논증 필수 게이트** — Differentiation Gate 추가: 각 거절 근거(101/102/103/112)마다 고유한 1차 논증 필수, 동일 논증 복사 금지
4. **M4: 103 결합 동기 논증 필수 게이트** — 103 거절마다 "No Motivation to Combine" 전용 하위 섹션 필수: Examiner 결합 근거 식별, PHOSITA 비결합 논증, 판례 인용(KSR, Kahn 등) 최소 1건
5. **M5: clean-claims.md 일치 검증 게이트** — Pre-Delivery Check #3 강화: amended-claims.md와 clean-claims.md 라인별 비교 필수, 마크업 잔여·누락 청구·구문 불일치 시 재생성 후 제출

### Size

- Baseline: 11016 bytes
- Final: 13192 bytes (+19.8%, within 20% gate)
