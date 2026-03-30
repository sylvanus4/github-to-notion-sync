# Critical Review — Output Templates

File structure templates for each deliverable produced by the critical-review pipeline.

## Table of Contents

- [CTO Review](#cto-review-cto-review-yyyy-mmmd)
- [CEO Review](#ceo-review-ceo-review-yyyy-mmmd)
- [PRD](#prd-prd-platform-quality-uplift-v1md)
- [OKRs](#okrs-okrs-platform-quarter-yearmd)
- [Strategy](#strategy-strategy-lean-canvas-swotmd)
- [Remediation Summary](#remediation-summary-remediation-summary-yyyy-mmmd)
- [Executive Summary DOCX](#executive-summary-docx-executive-summary-yyyy-mmdocx)

---

## CTO Review: `cto-review-{YYYY-MM}.md`

```markdown
# CTO Critical Review — {YYYY년 MM월}

> 작성일: {YYYY-MM-DD}
> 대상: {Project Name}
> 관점: CTO / 기술 리더십

## Executive Summary

{2-3 paragraph overview of critical technical findings}

## 1. Architecture Review

### Issue 1-1: {Issue Title}
**심각도**: {Critical|High|Medium|Low}
**파일**: `{file path}:{line numbers}`

**문제 설명**: {Description}

**옵션 분석**:
| 옵션 | 구현 난이도 | 리스크 | 영향 범위 | 유지보수 부담 |
|------|-----------|--------|----------|-------------|
| A. {Option} | {effort} | {risk} | {impact} | {burden} |
| B. {Option} | {effort} | {risk} | {impact} | {burden} |
| C. Do nothing | - | {risk} | - | {burden} |

**권장**: {Recommended option with reasoning}

### Issue 1-2: ...
### Issue 1-3: ...
### Issue 1-4: ...

## 2. Code Quality Review
{Same structure: 4 issues with options analysis}

## 3. Test Review
{Same structure: 4 issues with options analysis}

## 4. Performance Review
{Same structure: 4 issues with options analysis}

## Summary Table

| # | Section | Issue | Severity | Recommendation |
|---|---------|-------|----------|----------------|
| 1 | Architecture | {title} | {sev} | {rec} |
| ... | ... | ... | ... | ... |
| 16 | Performance | {title} | {sev} | {rec} |
```

---

## CEO Review: `ceo-review-{YYYY-MM}.md`

```markdown
# CEO Strategic Review — {YYYY년 MM월}

> 작성일: {YYYY-MM-DD}
> 대상: {Project Name}
> 관점: CEO / 경영 전략

## Executive Summary

{2-3 paragraph strategic assessment}

## 1. Product-Market Fit 분석

### 현재 상태
{Assessment of current feature set vs market need}

### 핵심 문제
{Feature sprawl, unclear target user, etc.}

### 권장 사항
{Specific actions to achieve PMF}

## 2. 비즈니스 모델 & 수익화

### 현재 상태
{Current monetization status}

### 잠재적 수익 모델
{Pricing models, revenue streams}

### 권장 사항
{Actions for revenue path}

## 3. 사용자 대면 품질

### 현재 상태
{UX quality assessment}

### 개선 필요 영역
{Loading states, error handling, onboarding}

### 권장 사항
{Specific UX improvements}

## 4. 경쟁 차별화

### 경쟁 우위
{What makes this product unique}

### 상품화 위험
{Commodity features easily replicated}

### 차별화 전략
{How to build defensible advantages}

## SWOT 분석

| | 긍정적 | 부정적 |
|---|--------|--------|
| **내부** | **강점 (S)**: {bullets} | **약점 (W)**: {bullets} |
| **외부** | **기회 (O)**: {bullets} | **위협 (T)**: {bullets} |

## 시장 포지셔닝 권장안

{2-3 paragraphs on recommended positioning}

## Top 3 전략적 액션

1. {Action with expected impact}
2. {Action with expected impact}
3. {Action with expected impact}
```

---

## PRD: `PRD-platform-quality-uplift-v1.md`

```markdown
# PRD: Platform Quality Uplift v1

## 1. Summary
**Problem**: {From CTO/CEO reviews}
**Solution**: {3-sprint remediation plan}

## 2. Contacts
| Role | Name |
|------|------|
| Owner | {name} |
| PM | {name} |
| Engineering Lead | {name} |

## 3. Background & Strategic Context
{Synthesized from review findings}

## 4. Objectives
### SMART OKRs
{3 objectives with measurable KRs}

## 5. Market Segments
{From CEO analysis}

## 6. Value Propositions
{Differentiation points}

## 7. Solution Detail

### Sprint 1: Foundation Fixes (Week 1-2)
| Task | Priority | Effort | Owner |
|------|----------|--------|-------|
| {task} | {P0-P3} | {S/M/L} | {role} |

### Sprint 2: Test Quality Uplift (Week 3-4)
| Task | Priority | Effort | Owner |
|------|----------|--------|-------|

### Sprint 3: UX & Performance (Week 5-6)
| Task | Priority | Effort | Owner |
|------|----------|--------|-------|

## 8. Success Metrics
| Metric | Before | Target | Sprint |
|--------|--------|--------|--------|

## 9. Risks and Mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
```

---

## OKRs: `OKRs-platform-{QUARTER}-{YEAR}.md`

```markdown
# Platform OKRs — {QUARTER} {YEAR}

## Objective 1: {Title}
**Rationale**: {Why this matters, linked to review findings}

- KR 1.1: {Measurable key result} — Baseline: {X} → Target: {Y}
- KR 1.2: {Measurable key result} — Baseline: {X} → Target: {Y}
- KR 1.3: {Measurable key result} — Baseline: {X} → Target: {Y}

## Objective 2: {Title}
{Same structure}

## Objective 3: {Title}
{Same structure}
```

---

## Strategy: `strategy-lean-canvas-swot.md`

```markdown
# Platform Strategy — Lean Canvas, SWOT & Value Proposition

## Lean Canvas

### 1. Problem
- {Problem 1}
- {Problem 2}
- {Problem 3}

### 2. Customer Segments
- {Segment 1}
- {Segment 2}

### 3. Unique Value Proposition
{One-liner UVP}

### 4. Solution
- {Solution 1}
- {Solution 2}
- {Solution 3}

### 5. Channels
### 6. Revenue Streams
### 7. Cost Structure
### 8. Key Metrics
### 9. Unfair Advantage

## SWOT Analysis
{Table format}

## Value Proposition Statement
{Structured value prop}

## Key Hypotheses
1. {Hypothesis with validation method}
2. {Hypothesis with validation method}
3. {Hypothesis with validation method}
```

---

## Remediation Summary: `remediation-summary-{YYYY-MM}.md`

```markdown
# Remediation Summary — {YYYY년 MM월}

## Executive Summary
{2-3 paragraph overview of what was done and impact}

## Sprint 1: Foundation Fixes

### {Change Title}
- **파일**: `{file path}`
- **변경 내용**: {Description of change}
- **영향**: {Impact on system}

{Repeat for each change}

## Sprint 2: Test Quality Uplift
{Same structure}

## Sprint 3: UX & Performance
{Same structure}

## Metrics

| Metric | Before | After | Target | Status |
|--------|--------|-------|--------|--------|
| Backend test coverage | {X}% | {Y}% | {Z}% | {✅/⚠️} |
| Frontend test coverage | {X}% | {Y}% | {Z}% | {✅/⚠️} |
| Bundle size | {X} KB | {Y} KB | {Z} KB | {✅/⚠️} |
| API p95 latency | {X} ms | {Y} ms | {Z} ms | {✅/⚠️} |

## Remaining Recommendations
1. {Recommendation with priority}
2. {Recommendation with priority}
3. {Recommendation with priority}
```

---

## Executive Summary DOCX: `executive-summary-{YYYY-MM}.docx`

The Word document should contain the following sections with professional formatting:

1. **Title Page**: "Platform Critical Review & Remediation — Executive Summary"
2. **Background**: 2-3 paragraphs on why the review was conducted
3. **Key Findings**: Bulleted list of top CTO + CEO findings
4. **Actions Taken**: Table with Sprint / Action / Impact columns
5. **Results Metrics**: Formatted table with before/after/target
6. **Strategic Deliverables**: List of PM documents produced
7. **Next Steps**: Prioritized list of remaining work

### DOCX Generation Script Pattern

```javascript
const { Document, Packer, Paragraph, Table, TableRow, TableCell,
        TextRun, HeadingLevel, AlignmentType, BorderStyle } = require("docx");
const fs = require("fs");

const doc = new Document({
  sections: [{
    properties: { page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
    children: [
      // Title
      new Paragraph({ heading: HeadingLevel.TITLE, children: [
        new TextRun({ text: "Platform Critical Review & Remediation", bold: true })
      ]}),
      // Sections follow...
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("docs/reviews/executive-summary-{YYYY-MM}.docx", buffer);
});
```
