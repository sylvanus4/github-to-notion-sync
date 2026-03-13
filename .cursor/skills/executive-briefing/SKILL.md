---
name: executive-briefing
description: >
  Synthesize multiple role-perspective analysis documents into a unified CEO executive briefing
  report in Korean. Identifies cross-role consensus, conflicting perspectives, prioritized action
  items, and a risk matrix. Outputs structured markdown and a .docx executive summary.
  Composes agency-executive-summary-generator, anthropic-docx, and visual-explainer.
  Use when the role-dispatcher invokes this skill after collecting role analyses, or when the
  user asks to "create executive briefing", "CEO 종합 보고서", "경영진 브리핑 생성",
  "synthesize role analyses", "cross-role summary".
  Do NOT use for single-role analysis (use the specific role-{name} skill), daily morning
  briefing (use morning-ship), or investor presentation (use presentation-strategist).
  Korean triggers: "CEO 종합 보고서", "경영진 브리핑", "직무별 종합".
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "synthesis"
---

# Executive Briefing Generator

Synthesizes analysis documents from multiple role-perspective skills into a comprehensive
CEO executive briefing with cross-functional insights, consensus mapping, and prioritized actions.

## Input Requirements

This skill expects a collection of role-perspective analysis documents, each following this structure:
- Role name and relevance score
- Executive summary bullets
- Detailed domain-specific analysis
- Risks & concerns
- Recommendations

Documents are typically located in `outputs/role-analysis/{topic-slug}/` or passed as context.

## Synthesis Pipeline

Execute sequentially:

### Phase 1: Content Aggregation
- Collect all role-perspective documents
- Record participation: which roles analyzed (relevance >= 5) vs skipped
- Extract key findings, risks, and recommendations from each

### Phase 2: Cross-Role Analysis (via `agency-executive-summary-generator`)
Apply McKinsey SCQA framework:
- **Situation**: Topic context and scope
- **Complication**: Key tensions revealed by cross-role analysis
- **Question**: What decision must the CEO make?
- **Answer**: Synthesized recommendation with confidence level

Identify:
- **Consensus**: Points where 3+ roles agree
- **Conflicts**: Points where roles disagree (and why)
- **Blind spots**: Important dimensions no role covered

### Phase 3: Risk Matrix
Aggregate risks from all roles into a unified matrix:
- Deduplicate similar risks
- Assign composite severity (impact x probability)
- Map mitigation owners by role

### Phase 4: Action Item Prioritization
Merge all role recommendations:
- Deduplicate and group by theme
- Prioritize by: urgency (time-sensitive), impact (business value), dependency (blocking others)
- Assign owner role and timeline

### Phase 5: Document Generation (via `anthropic-docx`)
Generate a professional .docx executive briefing with:
- Table of contents
- Executive summary (1 page)
- Cross-role analysis (2-3 pages)
- Risk matrix table
- Action items with owners
- Appendix: individual role summaries

### Phase 6: Visual Summary (via `visual-explainer`)
Create a self-contained HTML dashboard showing:
- Role participation heatmap
- Risk matrix scatter plot
- Action item timeline

## Output Format

```markdown
# CEO 종합 브리핑: {Topic}

## 날짜: {YYYY-MM-DD}

## 한눈에 보기 (Dashboard)
- 분석 주제: {Topic}
- 참여 직무: {N}개 / 10개
- 종합 영향도: {Critical/High/Medium/Low}
- 핵심 의사결정: {one-line decision statement}

## 직무별 핵심 요약
| 직무 | 관련도 | 핵심 메시지 |
|------|--------|-------------|
| CEO | {N}/10 | {one-line} |
| CTO | {N}/10 | {one-line} |
| PM | {N}/10 | {one-line} |
| ... | ... | ... |

## SCQA 분석
### Situation (상황)
### Complication (핵심 과제)
### Question (의사결정 포인트)
### Answer (종합 권고)

## 공통 합의 사항
- {Agreement 1}: 근거 — {roles that agree}
- {Agreement 2}: 근거 — {roles that agree}

## 상충되는 관점
| 쟁점 | 관점 A | 관점 B | 권고 |
|------|--------|--------|------|
| ... | ... | ... | ... |

## 우선순위 액션 아이템
| # | 액션 | 담당 직무 | 기한 | 영향도 | 긴급도 |
|---|------|-----------|------|--------|--------|
| 1 | ... | ... | ... | ... | ... |

## 리스크 매트릭스
| 리스크 | 출처 직무 | 영향 | 확률 | 완화 방안 | 담당 |
|--------|-----------|------|------|-----------|------|
| ... | ... | ... | ... | ... | ... |

## 블라인드 스팟 (미분석 영역)
- {Area not covered by any role}

## 부록: 직무별 상세 분석
### CEO 관점 (요약)
### CTO 관점 (요약)
### ...
```

## Slack Delivery Format

When posting to Slack `#효정-할일` (ID: `C0AA8NT4T8T`):

**Main message**:
```
📋 *CEO 종합 브리핑: {Topic}*
참여 직무: {N}/10 | 종합 영향도: {Level}

*핵심 의사결정*: {one-line}

*합의 사항*:
• {agreement 1}
• {agreement 2}

*우선 액션 아이템*:
1. {action 1} — {owner} ({deadline})
2. {action 2} — {owner} ({deadline})
```

**Thread replies** (one per participating role):
```
*{Role} 관점* (관련도: {N}/10)
{3-5 bullet summary from that role's analysis}
```

**File upload**: Executive briefing .docx attachment

## Error Handling

- If fewer than 2 role analyses are available, warn that cross-role synthesis may be shallow
- If a role document is malformed or missing sections, extract what is available and note gaps
- If the .docx generation fails, produce markdown-only output and log the failure
- If Slack posting fails, save all outputs locally and notify the user with file paths
- Always produce output in Korean regardless of the input language

## Example

**Input**: 8 role-perspective documents about "New GPU inference service launch"

**Output highlights**:
- Participation: 8/10 roles relevant (HR 5/10, Finance 8/10 — included)
- Consensus: All 8 roles agree on strategic importance and timing
- Conflict: CTO wants phased rollout (3 sprints) vs Sales wants fast launch (1 sprint)
- Top Action: Approve $200K GPU capex (Finance) + start hiring 2 ML engineers (HR)
- Risk: Competitive response from hyperscalers within 3 months (CSO + Sales)
