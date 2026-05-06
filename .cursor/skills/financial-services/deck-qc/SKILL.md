# Deck QC — Presentation Quality Control

Systematic quality check for investment banking pitch decks, board presentations, and client-facing financial documents. Catches formatting errors, data inconsistencies, and compliance issues before delivery.

Adapted from [anthropics/financial-services](https://github.com/anthropics/financial-services) `financial-analysis` vertical plugin.

## Triggers

Use when the user asks to "QC this deck", "review presentation", "check deck quality", "deck quality control", "pitch book review", "presentation review", "덱 QC", "프레젠테이션 점검", "피치북 검토", "발표 자료 품질 체크", or needs a systematic review of a financial presentation before sending to clients or stakeholders.

Do NOT use for creating presentations from scratch (use pitch-deck or anthropic-pptx). Do NOT use for general UX/design review of web UIs (use design-architect). Do NOT use for non-financial document quality checks (use doc-quality-gate).

## QC Dimensions (10-Point Checklist)

### 1. Data Consistency
- Cross-check all financial figures across slides
- Verify totals sum correctly in all tables
- Confirm year labels are consistent throughout
- Check that the same metric uses the same value everywhere

### 2. Source Verification
- Every data point must have a source footnote
- Sources must be dated within the last 12 months (unless historical)
- Proprietary data must be marked as such
- Public data must reference the original filing or report

### 3. Formatting Standards
- Font sizes: titles ≥ 20pt, body ≥ 12pt, footnotes ≥ 8pt
- Consistent color palette throughout
- Logo placement follows brand guidelines
- Page numbers on every slide
- Consistent date format (use one format throughout)

### 4. Numerical Formatting
- All currency values include denomination ($, ₩, €)
- Consistent decimal places (typically 1 for multiples, 0 for large numbers)
- Percentages formatted consistently (1 decimal place)
- Use "NM" or "N/A" consistently for non-meaningful values
- Units clearly stated (millions, billions, thousands)

### 5. Chart & Graph Integrity
- Axis labels present and readable
- Legend included for multi-series charts
- Scale starts at appropriate value (no misleading truncation)
- Chart title matches the data shown
- Color coding consistent with legend

### 6. Table Quality
- Headers clearly labeled with units
- Alternating row shading for readability
- Totals/subtotals highlighted or separated
- No orphaned rows across page breaks
- Column alignment (numbers right-aligned, text left-aligned)

### 7. Disclaimer & Compliance
- Required disclaimers present (confidentiality notice, forward-looking statement warning)
- "Draft" or "Preliminary" watermark if applicable
- Regulatory disclosures if required
- Non-public information properly marked

### 8. Narrative Coherence
- Executive summary aligns with detailed slides
- Section transitions are logical
- Key messages are consistent across sections
- Conclusions supported by preceding analysis

### 9. Spelling & Grammar
- Company names spelled correctly
- Industry terminology used accurately
- No broken sentences or orphaned text
- Korean/English consistency (no unintentional language switching)

### 10. Completeness
- Table of contents matches actual slide order
- All referenced appendices exist
- Contact information current and accurate
- Date of document and version number present

## Workflow

### Phase 1: Automated Scan
Run through dimensions 1-6 systematically, flagging issues with severity:
- **CRITICAL**: Data inconsistency, wrong numbers, missing disclaimers
- **MAJOR**: Formatting violations, missing sources, chart errors
- **MINOR**: Typos, alignment issues, style inconsistencies

### Phase 2: Manual Review Points
Flag items requiring human judgment for dimensions 7-10.

### Phase 3: QC Report
Generate a structured report:

```
## Deck QC Report: {Deck Name}
Date: {date} | Reviewer: AI Assistant

### Summary
- Critical issues: {N}
- Major issues: {N}
- Minor issues: {N}
- Overall grade: {PASS / CONDITIONAL PASS / FAIL}

### Critical Issues
1. [Slide X] {description} — {recommended fix}

### Major Issues
1. [Slide X] {description} — {recommended fix}

### Minor Issues
1. [Slide X] {description} — {recommended fix}

### Checklist Sign-off
- [ ] Data consistency verified
- [ ] Sources validated
...
```

## Pass Criteria

| Grade | Condition |
|-------|-----------|
| PASS | 0 critical, ≤ 2 major |
| CONDITIONAL PASS | 0 critical, 3-5 major (requires review) |
| FAIL | Any critical issue, or > 5 major issues |

## Composed Skills

| Skill | Purpose |
|-------|---------|
| `anthropic-pdf` | Read and parse PDF presentations |
| `anthropic-pptx` | Read and parse PPTX files |
| `trading-data-quality-checker` | Cross-reference financial data accuracy |
