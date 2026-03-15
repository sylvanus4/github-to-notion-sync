---
name: role-ux-designer
description: >
  Analyze a given topic from the UX Designer perspective — user experience impact, accessibility
  concerns, design system consistency, user research needs, and design handoff requirements.
  Scores topic relevance (1-10) and produces a structured Korean analysis document when relevant (>= 5).
  Composes ux-expert, kwp-design-user-research, kwp-design-design-critique,
  kwp-design-accessibility-review, kwp-design-design-system-management,
  workflow-miner, and intent-alignment-tracker.
  Use when the role-dispatcher invokes this skill with a topic, or when the user asks for
  "UX perspective", "UX 관점", "디자이너 분석", "user experience impact".
  Do NOT use for conducting a full UX audit (use ux-expert), design system token management
  (use kwp-design-design-system-management), or writing UX copy (use kwp-design-ux-writing).
  Korean triggers: "UX 관점", "디자이너 분석", "사용자 경험 영향".
metadata:
  author: "thaki"
  version: "1.1.0"
  category: "role-analysis"
---

# UX Designer Perspective Analyzer

Analyzes any business topic from the UX Designer's viewpoint, covering user experience impact,
interface changes, accessibility compliance, design system consistency, and user research needs.

## Relevance Criteria

Score the topic 1-10 based on overlap with UX concerns:

| Domain | Weight | Keywords |
|--------|--------|----------|
| User interface | High | UI, dashboard, page, screen, component, layout, navigation |
| User experience | High | flow, journey, onboarding, usability, friction, delight |
| Accessibility | High | WCAG, screen reader, keyboard, contrast, a11y |
| Design system | High | token, component library, consistency, pattern, Figma |
| User research | Medium | persona, interview, usability test, feedback, survey |
| Internationalization | Medium | i18n, locale, RTL, translation, multilingual |
| Content & copy | Medium | microcopy, error message, empty state, label |
| Performance (perceived) | Medium | loading, skeleton, animation, transition |
| Backend/infrastructure | Low | API, database, deployment, CI/CD |
| Finance/strategy | Low | revenue, market, investment |

Score >= 5 → produce full analysis. Score < 5 → return brief relevance note only.

## Analysis Pipeline

When relevant, execute sequentially:

1. **UX Impact Assessment** (via `ux-expert`):
   - Nielsen's 10 heuristics evaluation
   - Visual hierarchy and consistency check
   - Interaction pattern analysis

2. **User Research Needs** (via `kwp-design-user-research`):
   - Affected personas
   - Research questions to validate
   - Usability test scenarios

3. **Accessibility Review** (via `kwp-design-accessibility-review`):
   - WCAG 2.1 AA compliance impact
   - Screen reader and keyboard navigation
   - Color contrast requirements

4. **Design System Impact** (via `kwp-design-design-system-management`):
   - New components needed
   - Existing component modifications
   - Token and pattern consistency

5. **UX Workflow Pattern Discovery** (via `workflow-miner`):
   - Discover UX design workflow patterns from interaction history
   - Identify recurring design sequences (e.g., research → wireframe → prototype → test → iterate)
   - Recommend automation for repetitive design review tasks

6. **UX Intent Alignment** (via `intent-alignment-tracker`):
   - Measure alignment between user goals and interface design outcomes
   - Score per IA dimensions (Task Completion, Context Relevance, Efficiency, Side Effects)
   - Track UX quality and user satisfaction alignment trends

## Output Format

```markdown
# UX 디자이너 관점 분석: {Topic}

## 관련도: {N}/10
## 분석 일자: {YYYY-MM-DD}

## UX 요약 (3-5 bullets)
- ...

## 사용자 경험 영향
### 영향받는 사용자 플로우
### 휴리스틱 평가 (Nielsen 10)
### 인터랙션 패턴 변화

## 사용자 리서치 필요사항
### 영향받는 페르소나
### 검증이 필요한 가설
### 사용성 테스트 시나리오

## 접근성 (WCAG 2.1 AA)
### 영향받는 접근성 기준
### 키보드 내비게이션 요구사항
### 스크린 리더 호환성

## 디자인 시스템 영향
### 신규 컴포넌트
### 기존 컴포넌트 수정
### 토큰 & 패턴 일관성

## UI 변경 사항
### 와이어프레임 가이드
### 반응형 고려사항
### 마이크로카피 & 빈 상태

## 워크플로우 패턴 분석
### 발견된 UX 디자인 패턴
### 디자인 리뷰 자동화 기회

## 의도 정렬 평가
### IA 점수 (0-100)
### 사용자 목표-인터페이스 정렬
### 개선 필요 영역

## UX 디자이너 권고
### 즉시 디자인 작업
### 프로토타입 필요 여부
### 사용자 검증 계획
```

## Error Handling

- If a composed skill is unavailable, skip that pipeline step and note the gap in the output
- If the topic is ambiguous, request clarification before scoring relevance
- If relevance score is borderline (4-5), include the score rationale in the output
- Always produce output in Korean regardless of the input language

## Example

**Input**: "New GPU inference service launch for enterprise customers"

**Relevance Score**: 7/10 (new dashboard UI + deployment flow + monitoring views)

**Analysis highlights**:
- UX Impact: New inference deployment wizard, model status dashboard
- Persona: MLOps Engineer needs streamlined model deploy → monitor flow
- Accessibility: Status indicators need colorblind-safe palette + aria labels
- Design System: 3 new components (InferenceCard, ModelStatusBadge, GPUHeatmap)
- Recommendation: Prototype deployment wizard, run usability test with 3 users
