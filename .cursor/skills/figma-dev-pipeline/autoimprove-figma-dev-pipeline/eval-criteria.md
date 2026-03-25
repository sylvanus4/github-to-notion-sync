# Eval Criteria: figma-dev-pipeline

## Binary Evals

EVAL 1: Phase Completeness
Question: Does the output cover all 5 pipeline phases (Extract, Spec, Scaffold, Guide, Verify)?
Pass condition: Each phase produces its specified deliverable with no phases skipped
Fail condition: Any phase missing or marked as "skipped" without explicit reason

EVAL 2: Token and Spacing Accuracy
Question: Are design tokens (colors, spacing, typography) extracted with specific values (not approximations)?
Pass condition: Token values are exact (hex codes, pixel values, font sizes) as read from Figma
Fail condition: Approximate values like "around 16px" or "some shade of blue"

EVAL 3: Component Mapping
Question: Does the output map each Figma component to its closest existing code component or mark it as "new"?
Pass condition: Every component has a mapping entry (existing match or "new component needed")
Fail condition: Components listed without code mapping or "new" designation

EVAL 4: Verification Checklist
Question: Does Phase 5 produce a concrete verification checklist comparing implementation to design?
Pass condition: Numbered checklist with pass/fail items covering layout, tokens, interactions, and responsive behavior
Fail condition: Vague verification like "check if it looks right"

## Test Scenarios

1. "이 Figma 디자인을 코드로 변환하는 파이프라인을 실행해줘"
2. "Extract design specs from this Figma URL and generate implementation guide"
3. "피그마 컴포넌트를 분석하고 코드 스캐폴딩을 생성해줘"
4. "Run the full Figma-to-dev pipeline for the settings page redesign"
