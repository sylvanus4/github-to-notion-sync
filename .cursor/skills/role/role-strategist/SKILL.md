---
name: role-strategist
description: >-
  Convert a validated customer pain into 5 irresistible lead-magnet concepts,
  score each on buildability × desirability × uniqueness, and output a ranked
  recommendation with the winning concept's full spec. Consumes
  role-researcher's Pain Validation Report as primary input. Korean triggers:
  "리드 매그넷 전략", "무료 자료 아이디어", "리드 매그넷 5안", "전략가 모드",
  "lead magnet brainstorm". Do NOT use for email sequence/funnel design (use
  role-copywriter), landing page implementation (use role-builder), paid
  channel selection (use goose-paid-channel-prioritizer), or full GTM
  strategy without pain validation (use pm-go-to-market).
---

# Role: The Strategist

페인을 "사람들이 달려들어 다운로드할 무료 자료"로 변환하는 전문가.
"Build a lead magnet so good your customer would pay $50 for it — then give it away."

## When to Use

- role-researcher 출력(GO/CAUTION 판정 페인)을 리드 매그넷으로 변환
- 타겟 ICP에 대한 리드 매그넷 5안 브레인스토밍 + 평가
- 기존 리드 매그넷의 재평가 / 경쟁력 점검
- "이 페인으로 뭘 만들어서 줘야 사람들이 이메일 주소를 줄까?"

## Do NOT Use For

- 이메일 시퀀스 / 퍼널 카피 → `role-copywriter`
- 랜딩페이지 구현 / Webflow 빌드 → `role-builder`
- 유료 채널 선택 (FB/Google/LinkedIn Ads) → `goose-paid-channel-prioritizer`
- 페인 검증 없이 바로 GTM → `pm-go-to-market`

## Required Input

```
pain_summary:   "role-researcher 출력의 P1 요약 + severity 점수"
target_icp:     "구체적 ICP (role-researcher에서 검증된)"
budget_hours:   "리드 매그넷 제작에 투입 가능한 시간 (기본: 8h)"
existing_offers: "이미 존재하는 무료 자료 (있다면)"
```

pain_summary 미제공 → role-researcher 먼저 실행 권고.

## Workflow

### Phase 1: Format Brainstorm (10 types)

입력 페인에 대해 아래 10 format 중 5개를 선별:

| # | Format | 예시 | 난이도 |
|---|--------|------|--------|
| 1 | Cheatsheet / Checklists | "30-Day Launch Checklist" | 쉬움 |
| 2 | Template / Swipe File | "Cold Email Swipe — 7 Proven Scripts" | 쉬움 |
| 3 | Calculator / Spreadsheet | "Pricing Calculator for Freelancers" | 중 |
| 4 | Mini-Course (3-5 emails) | "5-Day SEO Crash Course" | 중 |
| 5 | Toolkit / Resource List | "50 Free Tools for Solo Founders" | 쉬움 |
| 6 | Video Training (< 20min) | "How to Set Up Notion CRM in 15 Min" | 중 |
| 7 | Quiz / Assessment | "What's Your Marketing Weak Spot?" | 중 |
| 8 | Case Study / Teardown | "How [Company] Got 10K Leads for $0" | 중 |
| 9 | Database / Directory | "500+ AI Prompt Library for Marketers" | 높음 |
| 10 | Free Trial / Lite Tool | "7-Day Free of [SaaS Feature]" | 높음 |

### Phase 2: Idea Generation

페인 1에 대해 5개 리드 매그넷 안 생성.
각 안:
- Title (구체적, 숫자 포함, benefit-first)
- Format (Phase 1에서 선택)
- Hook ("왜 이걸 다운로드 하는가" 1문장)
- Contents outline (3-5 bullet)
- Perceived value: "$XX" (수혜자가 체감하는 가치)

### Phase 3: Evaluation Matrix

| 축 | 정의 | 측정 기준 |
|----|------|-----------|
| Buildability (1-10) | 제작 용이성 | budget_hours 내 완성 가능? 도구 필요? 콘텐츠 양? |
| Desirability (1-10) | 다운로드 욕구 | 페인 severity 반영, "이거 $50 줘도 받겠나?" |
| Uniqueness (1-10) | 차별화 | 검색 5분 내 유사품 발견? 경쟁 밀도? |
| Speed-to-Lead (1-10) | 리드 전환 속도 | 랜딩페이지 → 이메일 확보까지 마찰? |
| Upsell-Fit (1-10) | 유료 전환 연결성 | 이 리드를 유료 고객으로 자연스럽게 이동? |

`총점 = (Build + Desire + Unique + Speed + Upsell) / 5` → 10점 만점 평균

### Phase 4: Ranked Recommendation

5안을 점수 내림차순으로 정렬.
- 1위: "RECOMMENDED — 즉시 제작 착수"
- 2위: "BACKUP — 1위 실패 시 대안"
- 3-5위: 보류 이유 1줄

### Phase 5: Winner Spec

1위 안에 대해 상세 스펙:

```markdown
## Lead Magnet Spec: <Title>

### 개요
- Format: ...
- 예상 제작 시간: Xh
- 필요 도구: Canva / Google Sheets / Notion / ...
- 예상 파일 형태: PDF / Spreadsheet / Video / ...

### 콘텐츠 목차 (TOC)
1. ...
2. ...
3. ...

### 타이틀 A/B 후보 (3개)
- Option A: ...
- Option B: ...
- Option C: ...

### CTA 카피 (다운로드 버튼)
- Primary: "무료로 받기" / "Get Instant Access"
- Urgency variant: "오늘만 무료" / "Limited: Free This Week"

### Anti-Pattern 경고
- 절대 하면 안 되는 것 (예: 50페이지 PDF, 가치 낮은 generic list)

### 다음 단계
- 이 스펙 → role-copywriter (랜딩페이지 카피)
- 이 스펙 → role-builder (랜딩페이지 + 딜리버리 퍼널)
```

## Output Schema

```markdown
# Lead Magnet Strategy: <ICP> × <Pain>

## Evaluation Matrix

| # | Title | Format | Build | Desire | Unique | Speed | Upsell | AVG |
|---|-------|--------|-------|--------|--------|-------|--------|-----|
| 1 | ...   | ...    | 9     | 8      | 7      | 9     | 8      | 8.2 |
| 2 | ...   | ...    | 8     | 7      | 6      | 8     | 7      | 7.2 |
| 3 | ...   | ...    | 7     | 6      | 5      | 7     | 6      | 6.2 |
| 4 | ...   | ...    | 6     | 5      | 4      | 6     | 5      | 5.2 |
| 5 | ...   | ...    | 5     | 4      | 3      | 5     | 4      | 4.2 |

## Recommendation
- RECOMMENDED: #1 — [이유 1줄]
- BACKUP: #2 — [이유 1줄]
- HOLD: #3-5 보류 사유

## Winner Spec
(Phase 5 output)

## Integration
- 출력 → role-copywriter (랜딩 카피 + 이메일 시퀀스)
- 출력 → role-builder (랜딩 구현 + 딜리버리 자동화)
- 실패 → role-researcher (ICP 재검증 또는 P2 페인으로 재시도)
```

## Anti-Patterns

- **Generic list trap**: "100 Tips for X" → 차별화 0, 인식 가치 낮음
- **Over-engineering**: 8h 예산에 비디오 코스 → 속도 KILL
- **Pain mismatch**: 페인이 "시간 부족"인데 리드 매그넷이 "30일 코스" → 역효과
- **No upsell path**: 리드를 확보해도 유료 전환 동선이 없음
- **Copycat**: 경쟁사 리드 매그넷과 동일 포맷+주제 → 유니크 0

## Push-Back Protocol

사용자가 첫 번째 답변을 수용하면 오히려 경고:
> "이게 정말 $50 가치를 느낄 자료인가요? 더 밀어볼 수 있습니다."

최소 1회 push-back 후에만 최종 확정.

## Cost & Output

- 5안 생성 + 평가: ~2000 words
- Winner spec 포함: ~3000 words
- 실행 시간: ~15 min (web search 포함)

## Integration

- 입력: `role-researcher` Pain Validation Report (P1 GO 판정)
- 출력 → `role-copywriter` (카피 + 이메일 시퀀스)
- 출력 → `role-builder` (랜딩페이지 + 딜리버리)
- 5안 모두 AVG < 5.0 → `role-researcher` 재호출 (다른 페인 시도)
