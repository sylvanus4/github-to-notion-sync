---
name: korean-tone-reviewer
description: >
  한국어 비즈니스 문서의 직급별 경어 검증 및 톤 적절성 검토. 격식 수준 5단계 기준으로
  호칭, 경어, 어투를 검토하고 교정안을 제시한다. sentence-polisher, gws-email-reply,
  leadership-writing-refiner, policy-text-generator 등 한국어 출력 스킬의 후처리
  단계로 호출하거나 독립 실행 가능.
triggers:
  - "경어 검토"
  - "톤 리뷰"
  - "korean tone review"
  - "korean-tone-reviewer"
  - "직급별 경어"
  - "호칭 검증"
  - "비즈니스 톤"
  - "격식 수준 검토"
  - "존댓말 체크"
  - "경어 수준 확인"
  - "honorifics check"
  - "tone appropriateness"
  - "business tone review"
  - "formality level check"
do_not_use_for:
  - General grammar-only fixes without tone context (use sentence-polisher)
  - Full document rewriting (use prompt-transformer)
  - Brand voice enforcement for marketing (use kwp-brand-voice-brand-voice-enforcement)
  - English-only text tone review
  - Code review (use deep-review or simplify)
version: 1.0.0
---

# Korean Tone Reviewer

한국 직장 문화에 맞는 직급별 경어 사용과 비즈니스 톤 적절성을 검토한다.

## When to Use

- 고객 대상 이메일, 제안서, 공문서 작성 후 최종 검수
- 사내 공지, 회의록, 상급자 보고서의 어투 점검
- `sentence-polisher`, `gws-email-reply`, `leadership-writing-refiner` 후처리 단계
- 한국어 비즈니스 문서의 직급/상황별 톤 가이드가 필요할 때

## Formality Levels (격식 수준 5단계)

| Level | Name | Use Cases | Sentence Endings |
|-------|------|-----------|------------------|
| 1 | 공식 격식체 | 공문서, 계약서, 대외 제안서 | ~합니다, ~드립니다, ~하겠습니다 |
| 2 | 정중 격식체 | 고객 응대, 공식 메일 | ~합니다, ~해 드리겠습니다 |
| 3 | 정중 비격식체 | 사내 상급자 메일, 회의록 | ~해요, ~드려요 |
| 4 | 비격식체 | 동료 간 소통, 팀 채팅 | ~해요, ~할게요 |
| 5 | 반말 | 친밀한 동료 간 (문서에 사용 부적절) | ~해, ~할게 |

## Title & Honorifics Rules (직급별 호칭)

| Rank | Correct Form | Notes |
|------|-------------|-------|
| 대표/사장 | 대표님, 사장님 | Never omit 님 |
| 임원 (부사장, 전무, 상무) | {직함}님 | 부사장님, 전무님, 상무님 |
| 팀장 | 팀장님, {이름} 팀장님 | |
| 동료 (same level) | {이름} {직함}님, {이름}님 | |
| 주니어 (연하) | {이름}씨, {이름}님 | 씨 is acceptable for juniors |

## Common Honorific Errors (자주 틀리는 경어)

| Incorrect | Correct | Context |
|-----------|---------|---------|
| 식사하셨어요? | 식사하셨습니까? | Level 1-2 formal |
| 확인해주세요 | 확인 부탁드립니다 | Level 1-2 formal |
| 알겠어요 | 알겠습니다 | Level 1-2 formal |
| 수고하세요 | 수고하셨습니다 | Only at end of day (퇴근 시) |
| 죄송합니다요 | 죄송합니다 | Remove extraneous 요 |
| ~하시면 됩니다 | ~하시면 되겠습니다 | Level 1 requires 겠 |
| ~인 것 같습니다 | ~입니다 / ~로 판단됩니다 | Avoid hedging in formal docs |
| 제가 생각하기에는 | (삭제) or 검토 결과 | Avoid first-person hedging in official |

## Workflow

### Step 1: Context Detection

Determine the document type and audience:

1. **Read** the target text
2. **Identify** document type: 공문서, 이메일, 사내 공지, 회의록, 제안서, Slack 메시지, etc.
3. **Identify** recipient rank/relationship if available
4. **Select** the appropriate formality level (1-5)

If context is ambiguous, default to Level 2 (정중 격식체) as the safest business default.

### Step 2: Scan for Violations

Check for:

1. **Formality inconsistency**: Mixed levels within the same document (e.g., ~합니다 and ~해요 in the same paragraph)
2. **Honorific errors**: Incorrect title usage, missing 님, wrong sentence endings
3. **Tone misalignment**: Overly casual for the context, or unnecessarily stiff
4. **Foreign-word mixing**: Excessive English/외래어 when Korean equivalents exist in formal documents
5. **Subject-verb honorific agreement**: 부장님이 말했다 (wrong) vs 부장님께서 말씀하셨습니다 (correct)

### Step 3: Generate Report

Output format:

```markdown
## 한국어 톤 검토 결과

**대상**: {문서명 or 텍스트 설명}
**적용 기준**: {격식 수준 (1-5단계)} - {수준 이름}
**종합 판정**: PASS / NEEDS_REVISION

### 수정 필요 항목
| # | 위치 | 현재 표현 | 권장 표현 | 이유 |
|---|------|----------|----------|------|
| 1 | ... | ... | ... | ... |

### 전체 어투 평가
- 격식 수준 일관성: PASS/FAIL
- 경어 수준 적합성: PASS/FAIL
- 직급 호칭 정확성: PASS/FAIL
- 외래어 혼용 적절성: PASS/FAIL
- 주어-서술어 높임 일치: PASS/FAIL

### 교정 후 전문 (NEEDS_REVISION인 경우)
{교정 완료된 전체 텍스트}
```

### Step 4: Auto-fix (Optional)

When invoked as a pipeline sub-step (e.g., from `sentence-polisher` or `gws-email-reply`):

1. Apply all corrections automatically
2. Return the corrected text with a brief change summary
3. Do NOT output the full report format; return only corrected text + change list

## Integration Points

| Caller Skill | When to Invoke | Mode |
|-------------|---------------|------|
| `sentence-polisher` | After Step 4 auto-fix, before final output | Auto-fix (silent) |
| `gws-email-reply` | Before sending draft to user for approval | Auto-fix (silent) |
| `leadership-writing-refiner` | After leadership tone transformation | Report (full) |
| `policy-text-generator` | After policy text generation | Report (full) |
| Standalone | User directly requests tone review | Report (full) |

## Constraints

- Regional/generational differences exist; provide multiple alternatives when applicable
- Never downgrade formality without explicit user request
- When uncertain about recipient rank, default to higher formality
- Flag but do not auto-correct stylistic choices that are valid in context (e.g., intentionally casual team Slack)

## Source

Adapted from `modu-ai/cowork-plugins` `moai-hr/skills/employment-manager/references/korean-tone-reviewer.md`, expanded with integration points for the project's existing Korean text pipeline skills.
