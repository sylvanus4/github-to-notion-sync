---
name: leadership-writing-refiner
description: >-
  Transform Korean text with leadership communication principles — soften
  delivery while maintaining standards, prioritize context over judgment,
  clarify expectations, and insert structured growth guidance for juniors.
  Use when the user asks to "리더십 글 다듬기", "refine leadership", "팀
  커뮤니케이션 개선", "글 변환", "전달 방식 정제", "리더십 글 변환",
  "leadership tone refine", "리더십 톤 변환", "팀 피드백 다듬기",
  "주니어 피드백 개선", or pastes text that needs leadership-aware
  rewriting. Do NOT use for general grammar-only fixes (use
  sentence-polisher). Do NOT use for full document rewriting without
  leadership context (use prompt-transformer). Do NOT use for brand voice
  enforcement (use kwp-brand-voice-brand-voice-enforcement).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "generation"
---

# Leadership Writing Refiner

## Core Philosophy

This skill embodies four leadership communication principles:

1. **기준과 속도는 유지하되 전달 방식을 정제한다** — Preserve substance, soften delivery
2. **판단보다 맥락 이해를 우선한다** — Context before judgment
3. **기대치와 배경을 명확히 공유한다** — Make the implicit explicit
4. **주니어에게는 최소한의 성장 가이드를 구조적으로 제공한다** — Structured micro-guidance for juniors

## Output Language

All output (refined text, transformation log, tone assessment) is in **Korean**.

## Workflow

### Step 1 — Classify the Text

Analyze the input to determine:

| Dimension        | Categories                                                                 |
|------------------|---------------------------------------------------------------------------|
| **Text type**    | self-reflection, team feedback, direct message to junior, email to peer, Slack update, meeting note, 1:1 note, performance review comment |
| **Target audience** | junior, peer, leadership, self, mixed                                  |
| **Emotional register** | frustration, encouragement, neutral, critical, disappointed, appreciative |
| **Formality**    | formal (존댓말), casual (반말), mixed                                     |

Record the classification silently — it drives which lenses apply in Step 3.

### Step 2 — Diagnose Communication Anti-patterns

Scan the text for these four anti-pattern families:

**A. Judgment Leakage (판단 누출)**
Language that reveals internal evaluation rather than constructive framing.
- "역량이 부족해서", "프로페셔널하지 않아서", "기대에 못 미쳐서"
- Implicit superiority markers: "당연히 ~해야 하는데", "기본적인 건데"

**B. Speed-over-Empathy (속도 우선 공감 결여)**
Terse directives without context or acknowledgment.
- One-line rejections: "이건 안 돼요", "다시 해주세요"
- Missing "why": feedback without reasoning

**C. Missing Expectation Anchors (기대치 부재)**
Feedback given without a clearly stated baseline or goal.
- "완성도가 낮아요" without defining what "complete" looks like
- Implicit standards the reader cannot infer

**D. Psychological Distance Signals (심리적 거리 신호)**
Distancing language, passive-aggressive tone, withdrawal cues.
- Sudden formality shifts, cold enumeration without warmth
- "알아서 해주세요" without support offer

For each detected anti-pattern, note the location and category.

### Step 3 — Apply 4 Transformation Lenses

Apply each lens **only where relevant** based on the Step 1 classification and Step 2 diagnosis.

#### Lens A — Delivery Refinement (전달 방식 정제)

Preserve the core message but replace sharp edges with observation + impact framing.

| Before pattern | After pattern |
|----------------|---------------|
| Direct judgment ("~가 부족해요") | Observation + impact ("~한 부분이 있어서 ~에 영향을 줄 수 있어요") |
| Blame framing ("왜 ~를 안 했어요?") | Gap framing ("~가 빠져 있는데, 어떤 상황이었는지 궁금해요") |
| Absolute language ("항상", "전혀") | Scoped language ("이번에는", "이 부분에서는") |

Maintain assertiveness — this is refinement, not dilution.

#### Lens B — Context-First Reframing (맥락 우선 재구성)

Add context or background **before** any critique. Use the pattern:

```
상황 → 갭 → 제안
(situation → gap → suggestion)
```

instead of:

```
문제 → 책임
(problem → blame)
```

If the original text jumps straight to a problem, prepend the situational context that makes the feedback understandable.

#### Lens C — Expectation Clarity (기대치 명확화)

Where the original assumes shared understanding, make it explicit:

- Add "기대 수준" (expected level) when critiquing quality
- Add "배경" (background) when giving direction
- Add "이유" (reasoning) when making requests
- Convert "더 잘 해주세요" into specific, observable behaviors

#### Lens D — Growth Guide Insertion (성장 가이드 삽입)

**Only for junior-facing text** (as classified in Step 1).

Add structured micro-guidance with three elements:

1. **좋은 예시** — What good looks like (concrete example or reference)
2. **다음 한 걸음** — One concrete next step the junior can take immediately
3. **지원 제안** — An offered resource, check-in point, or help channel

Keep guidance brief — 2-3 sentences maximum. Avoid patronizing tone.

### Step 4 — Compose the Refined Text

Rewrite the full text applying all applicable lenses:

- Preserve the author's voice and core message
- Match the input's formality level (존댓말/반말)
- Mark subjective rewrites with `[REVIEW]` where the user should verify intent
- Do not add lenses that weren't triggered — minimal intervention principle

### Step 5 — Final Polish via `sentence-polisher`

Pass the rewritten text through the `sentence-polisher` skill workflow:

1. Grammar, spacing, and punctuation cleanup
2. Honorific/politeness level consistency check
3. Konglish and awkward phrasing correction
4. Logical flow verification

### Output Format

Return a structured response with these sections:

```
## 변환된 글

[Refined text — ready to use]

## 변환 로그

| 위치 | 원문 | 변환 후 | 적용 렌즈 | 이유 |
|------|------|---------|-----------|------|
| ...  | ...  | ...     | A/B/C/D   | ...  |

## 톤 평가

- **원문 톤**: [e.g., 비판적, 직설적]
- **변환 후 톤**: [e.g., 건설적, 맥락 중심]
- **유지된 요소**: [e.g., 명확한 기준, 결과 지향]

## 성장 가이드 (주니어 대상인 경우)

[Growth guide section — only included when junior-facing text is detected]
```

## Composability

- **Always chains with**: `sentence-polisher` (Step 5)
- **Optional composition with**: `scqa-writing-framework` (if user requests structured narrative rewrite)
- **Optional composition with**: `long-form-compressor` (if text needs shortening after transformation)
