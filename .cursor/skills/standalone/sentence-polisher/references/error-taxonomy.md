---
name: error-taxonomy
description: "Full error taxonomy for the sentence-polisher skill with examples and fix patterns for both Korean and English."
---
# Error Taxonomy

## 1. Grammar Errors

### English

| Error Type | Example | Fix |
|-----------|---------|-----|
| Spelling | "buisness" | "business" |
| Punctuation — missing comma | "However we decided" | "However, we decided" |
| Punctuation — run-on | "We launched it was successful" | "We launched it. It was successful." or use semicolon |
| Subject-verb agreement | "The team are working" | "The team is working" |
| Tense consistency | "We launched and are seeing" | Keep tense consistent within timeframe |
| Article usage | "We need meeting" | "We need a meeting" |
| Preposition | "discuss about the issue" | "discuss the issue" |
| Dangling modifier | "After reviewing, the decision seemed obvious" | "After reviewing, we found the decision obvious" |

### Korean

| Error Type | Example | Fix |
|-----------|---------|-----|
| 조사 (particle) — 은/는 vs 이/가 | "저는 생각이 합니다" | "저는 생각합니다" |
| 조사 — 을/를 | "회의 참석하겠습니다" | "회의에 참석하겠습니다" |
| 조사 — 에/에서 | "회사에 일합니다" | "회사에서 일합니다" |
| 이중 주어 | "이 프로젝트는 일정이 진행이 됩니다" | "이 프로젝트는 일정대로 진행됩니다" |
| 피동 중복 | "보여지다", "만들어지다" | "보이다", "만들다" (if active is natural) |

## 2. Logic Errors

| Error Type | Example | Fix |
|-----------|---------|-----|
| Contradiction | "We prioritize privacy" + "We share data with 50+ partners" | Flag contradiction; suggest reconciliation |
| Unsupported claim | "Our product is the best" | Add evidence or soften: "Our product leads in X metric" |
| Incomplete thought | "Because of the deadline" (fragment) | Complete the sentence |
| Vague quantifier | "많은 고객이", "다양한 기능" | Specify: "200명 이상의 고객이", "12개 주요 기능" |
| Circular reasoning | "It's important because it matters" | Provide actual reasoning |

## 3. Flow Errors

| Error Type | Example | Fix |
|-----------|---------|-----|
| Missing transition | Topic jump between paragraphs | Add: "이에 따라", "Additionally", "However" |
| Choppy sentences | "We launched. We got feedback. We improved." | "After launching, we gathered feedback and improved the feature." |
| Passive voice overuse (EN) | "The decision was made by the team" | "The team made the decision" |
| Nominalization overuse (KO) | "검토를 진행하였습니다" | "검토했습니다" |
| Redundancy | "simple and easy to use; straightforward" | "simple and easy to use" |
| Filler phrases | "In order to", "at this point in time" | "To", "now" |

## 4. Korean-specific Errors

### Honorific Level (경어법)

| Error | Example | Fix |
|-------|---------|-----|
| 존댓말/반말 mixing | "검토해 주세요. 내일까지 보내줘." | Unify to one level: "검토해 주세요. 내일까지 보내 주세요." |
| -합니다/-해요 mixing | "진행합니다. 확인해요." | Unify: "진행합니다. 확인합니다." |
| Inappropriate casual in formal context | "감사해요" (to a client) | "감사합니다" |

### Spacing (띄어쓰기)

| Error | Fix | Rule |
|-------|-----|------|
| "진행 할 수 있습니다" | "진행할 수 있습니다" | 보조 용언 붙여쓰기 |
| "해봤는데요" | "해 봤는데요" | 본용언+보조용언 띄기 (both accepted) |
| "것같습니다" | "것 같습니다" | 의존명사 띄기 |
| "할수있습니다" | "할 수 있습니다" | 의존명사 + 보조용언 띄기 |

### Konglish

| Konglish | Acceptable? | Korean Alternative |
|----------|-------------|-------------------|
| 미팅 | Yes (widely used) | 회의 (formal docs) |
| 핸들링하다 | No | 처리하다, 대응하다 |
| 스케줄 | Contextual | 일정 (formal), 스케줄 (casual OK) |
| 리뷰하다 | Contextual | 검토하다 (formal), 리뷰 (tech OK) |
| 피드백 | Yes (no good KO equivalent) | — |
| 업데이트하다 | Contextual | 갱신하다 (formal), 업데이트 (tech OK) |
| 컨펌하다 | No | 확인하다 |
| 어사인하다 | No | 배정하다, 할당하다 |

## Priority Classification

| Priority | When to Apply |
|----------|--------------|
| Critical | Grammar or logic errors that confuse readers or change meaning |
| Important | Flow issues that hurt readability; honorific inconsistency in formal context |
| Minor | Stylistic suggestions; Konglish in informal context; optional spacing variants |
