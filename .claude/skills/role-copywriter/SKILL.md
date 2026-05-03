---
name: role-copywriter
description: >-
  Sequential Prompt Chain that converts a lead-magnet spec into conversion-ready
  copy: hook headline → pain-agitate bullets → landing page sections → 5-email
  welcome sequence → CTA variants. Consumes role-strategist's Winner Spec as
  primary input. Korean triggers: "카피라이터 모드", "랜딩 카피", "이메일
  시퀀스", "후크 헤드라인", "lead magnet copy", "landing page copywriting",
  "email welcome sequence". Do NOT use for lead-magnet ideation/scoring (use
  role-strategist), landing page implementation/deployment (use role-builder),
  paid ad copy optimization (use goose-messaging-ab-tester), full brand voice
  guideline creation (use kwp-brand-voice-guideline-generation), or general
  article/blog editing (use edit-article).
---

# Role: The Copywriter

리드 매그넷 스펙을 "다운로드 안 할 수 없는" 랜딩 카피 + 이메일 시퀀스로 변환하는 전문가.
Sequential Prompt Chain: hook → bullets → landing → email sequence → CTA test.

## When to Use

- role-strategist 출력(Winner Spec)을 랜딩페이지 카피로 변환
- 리드 매그넷 다운로드 페이지 헤드라인/서브헤드/CTA 작성
- 5-email 웰컴 시퀀스 설계 (다운로드 → 교육 → 세일즈)
- CTA 버튼 카피 A/B 변형 생성
- "사람들이 이메일 주소를 기꺼이 내놓을 카피"

## Do NOT Use For

- 리드 매그넷 아이디어 생성/평가 → `role-strategist`
- 랜딩페이지 코드 구현/배포 → `role-builder`
- 광고 카피 A/B 테스트 인프라 → `goose-messaging-ab-tester`
- 브랜드 보이스 가이드라인 생성 → `kwp-brand-voice-guideline-generation`
- 블로그/아티클 편집 → `edit-article`
- 전체 마케팅 캠페인 플래닝 → `kwp-marketing-campaign-planning`

## Required Input

```
winner_spec:      "role-strategist Winner Spec (title, format, TOC, hook)"
target_icp:       "구체적 ICP — 직업, 페인, 목표"
brand_tone:       "브랜드 톤 (기본: conversational, direct, no-BS)"
competitor_pages:  "경쟁 랜딩페이지 URL (있다면, 차별화 참조)"
```

winner_spec 미제공 → role-strategist 먼저 실행 권고.

## Workflow: Sequential Prompt Chain

각 Phase는 이전 Phase 출력을 입력으로 받는 엄격한 순차 체인.
Phase 건너뛰기 금지. 순서 변경 금지.

### Phase 1: Hook Headlines (5 variants)

입력: Winner Spec의 title + ICP 페인
출력: 5개 헤드라인 변형

| Type | 패턴 | 예시 |
|------|-------|------|
| Curiosity Gap | "The [X] That [Surprising Result]" | "The Checklist That Turned Cold Leads Into Paying Clients" |
| Direct Benefit | "[Get/Stop/Start] [Specific Outcome] [Timeframe]" | "Get 50 Qualified Leads This Week Without Spending a Dollar" |
| Social Proof | "[Number] [People] Already [Result]" | "2,847 Founders Already Use This Pricing Framework" |
| Pain Poke | "Still [Pain Action]? There's a [Better Way]" | "Still Guessing Your Prices? There's a Calculator for That" |
| Contrarian | "Why [Common Advice] Is Killing Your [Goal]" | "Why Free Trials Are Killing Your SaaS Revenue" |

선택 기준: ICP의 인식 수준(problem-aware vs solution-aware) 기반.

### Phase 2: Pain-Agitate Bullets

입력: Phase 1 best headline + role-researcher의 verbatim pain quotes
출력: 5-7 bullet points (PAS micro-structure per bullet)

각 bullet 구조:
```
✗ [Pain — ICP가 직접 말한 표현 인용]
  → [Agitate — 방치 시 결과]
  → [Solve hint — 이 리드 매그넷이 해결]
```

Pain quote가 없으면 Phase 실패 → role-researcher 재호출.

### Phase 3: Landing Page Sections

입력: Phase 1 headline + Phase 2 bullets
출력: 완성된 랜딩페이지 카피 (7 sections)

```markdown
## Landing Page Copy

### Section 1: Hero
- Headline: [Phase 1 winner]
- Subheadline: [1 sentence — what they get + how fast]
- CTA button: [Primary CTA text]
- Hero image direction: [what the image should convey]

### Section 2: Problem Stack
- [Phase 2 bullets, reformatted for visual scanning]

### Section 3: Solution Reveal
- "What You'll Get" — TOC from Winner Spec, benefit-reframed
- Each item: [Feature] → [Benefit] format

### Section 4: Social Proof / Credibility
- [Authority signal: expertise, data, testimonials if available]
- [If no testimonials: "Built from [X hours] of research / [Y] interviews"]

### Section 5: Objection Handling
- "Is this really free?" → Yes, no catch.
- "Will this work for my [niche]?" → [Specificity answer]
- "How is this different from [competitor]?" → [Unique angle]

### Section 6: Final CTA
- Urgency angle (if honest — no fake scarcity)
- CTA button text (variant from Primary)
- One-line reassurance: "No spam. Unsubscribe anytime."

### Section 7: Below-fold FAQ (optional)
- 3-5 FAQ pairs addressing remaining friction
```

### Phase 4: Welcome Email Sequence (5 emails)

입력: Phase 3 landing copy + Winner Spec 내용
출력: 5-email 시퀀스

| # | Timing | Purpose | Subject Line Pattern |
|---|--------|---------|---------------------|
| E1 | Immediate | Delivery + quick win | "[Name], here's your [Lead Magnet]" |
| E2 | Day 1 | Teach one concept | "The #1 mistake with [Topic]" |
| E3 | Day 3 | Case study / proof | "How [Person] got [Result] using this" |
| E4 | Day 5 | Soft pitch | "Ready to [Next Level]?" |
| E5 | Day 7 | Direct offer + scarcity | "Last chance: [Offer]" |

각 이메일: Subject + Preview text + Body (< 200 words) + CTA

### Phase 5: CTA Variant Matrix

입력: Phase 3-4의 모든 CTA
출력: 6 CTA 변형 × 2 tone

| # | CTA Text | Tone | Urgency |
|---|----------|------|---------|
| 1 | "무료로 받기" | Neutral | None |
| 2 | "지금 다운로드" | Direct | Low |
| 3 | "내 [결과] 시작하기" | Benefit | None |
| 4 | "이번 주만 무료" | Neutral | High |
| 5 | "Yes, send me the [Asset]!" | Conversational | None |
| 6 | "[숫자]명이 이미 받았습니다" | Social proof | Medium |

## Output Schema

```markdown
# Conversion Copy: <Lead Magnet Title>

## 1. Hook Headlines (5)
| # | Headline | Type | ICP Awareness |
|---|----------|------|---------------|

## 2. Pain-Agitate Bullets
(7 bullets with PAS micro-structure)

## 3. Landing Page Copy
(7 sections — Hero through FAQ)

## 4. Email Welcome Sequence
(5 emails — delivery through direct offer)

## 5. CTA Variant Matrix
(6 variants × 2 tones = 12 options)

## Integration
- 출력 → role-builder (랜딩페이지 구현 + 이메일 자동화 연결)
- A/B 테스트 대상: Headlines #1 vs #2, CTA #1 vs #3
- 실패 시 → role-strategist 재호출 (다른 리드 매그넷으로 피벗)
```

## Anti-Patterns

- **Feature-dump**: "이 PDF에는 50페이지 분량의..." → 아무도 관심 없음. Benefit 먼저.
- **Jargon overload**: ICP가 모르는 전문용어 남발 → 7th grader test 통과 필수
- **Weak CTA**: "제출" / "Submit" → 죽은 버튼. Benefit-verb 필수.
- **No urgency, fake urgency**: 정직한 urgency만 사용 (실제 마감, 실제 수량 제한)
- **Copy-paste from competitor**: 경쟁 랜딩 참조하되 카피 복사 금지
- **Skipping phases**: Phase 2 bullets 없이 Phase 3 진행 → 랜딩이 공허해짐

## Quality Gates

1. **7th-Grader Test**: 모든 카피를 중학생이 읽어도 이해 가능한가?
2. **So-What Test**: 매 문장 끝에 "So what?"을 붙여서 답이 나오는가?
3. **Screenshot Test**: 랜딩을 스크린샷으로 5초간 보여줬을 때 행동 유도가 명확한가?
4. **Voice Consistency**: Hero → CTA까지 톤이 일관적인가?

## Cost & Output

- Full chain (Phase 1-5): ~3500 words
- 실행 시간: ~10 min
- 웹 검색: 경쟁 랜딩 분석 시에만 (선택적)

## Integration

- 입력: `role-strategist` Winner Spec
- 출력 → `role-builder` (구현 + 배포)
- A/B 테스트 → `goose-messaging-ab-tester`
- 실패 (전환율 < 15%) → `role-strategist` 재호출 (다른 안 피벗)
