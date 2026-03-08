---
name: ai-quality-evaluator
description: >-
  Score and validate AI-generated financial reports for accuracy, hallucination
  detection, data consistency, coverage completeness, and actionability.
  Implements a 5-dimension quality gate before Slack distribution. Use when the
  user asks to "check report quality", "validate AI output", "score this
  report", "detect hallucinations", "quality gate", "ai quality", "AI 품질
  평가", "리포트 검증", "환각 감지", or wants to verify AI-generated stock
  analysis before publishing.
  Do NOT use for evaluating LLM prompts or judge prompts (use evals-skills).
  Do NOT use for code quality review (use simplify or deep-review).
  Do NOT use for general AI output evaluation outside finance (use evals-skills).
  Do NOT use for running the daily pipeline (use today).
metadata:
  author: thaki
  version: 1.0.0
  category: review
---

# AI Quality Evaluator

Validate AI-generated financial reports and analysis outputs against ground truth data, scoring across 5 quality dimensions. Acts as a quality gate between report generation and Slack distribution.

## Quality Dimensions

| Dimension | Weight | What It Measures |
|-----------|--------|------------------|
| **Accuracy** | 30% | Do numbers match DB data? Are signals correct? |
| **Consistency** | 20% | Do conclusions align with the underlying data? |
| **Coverage** | 20% | Are all tracked tickers and categories represented? |
| **Actionability** | 20% | Are buy/sell recommendations clear and justified? |
| **Tone** | 10% | Is the language professional, balanced, and disclaimer-compliant? |

Final score: weighted average on a 0-10 scale.

| Score Range | Gate Decision |
|-------------|---------------|
| 8.0 - 10.0 | PASS — publish directly |
| 6.0 - 7.9 | REVIEW — flag issues, suggest fixes, ask for confirmation |
| 0.0 - 5.9 | FAIL — do not publish, list all critical issues |

## Workflow

### Step 1: Identify Artifacts to Evaluate

Locate the AI-generated outputs:

1. **Analysis JSON**: `outputs/analysis-{date}.json`
2. **Report file**: `outputs/reports/daily-{date}.docx` (read via `anthropic-docx` skill or the PDF skill)
3. **Discovery JSON**: `outputs/discovery-{date}.json` (optional)
4. **News JSON**: `outputs/news-{date}.json` (optional)

If no date is specified, use today's date. If files don't exist, report which artifacts are missing.

### Step 2: Gather Ground Truth

Collect reference data to validate against:

1. **DB prices**: Run `backend/scripts/weekly_stock_update.py --status` to get latest ticker data
2. **Analysis script**: Run `backend/scripts/daily_stock_check.py --source db` to get raw signal data
3. **Ticker list**: Read `backend/app/core/constants.py` for `DEFAULT_STOCKS` and `TICKER_CATEGORY_MAP`

### Step 3: Score Each Dimension

#### 3a: Accuracy (30%)

Cross-reference report claims against ground truth:

| Check | Method | Deduction |
|-------|--------|-----------|
| Price values | Compare report prices vs DB latest close | -2 per wrong price |
| Signal labels | Compare report signals vs analysis JSON | -3 per wrong signal |
| Indicator values | Compare SMA/RSI/MACD vs analysis JSON | -1 per significant deviation |
| Date correctness | Verify report date matches analysis date | -5 if wrong date |
| Ticker names | Verify ticker symbols and company names | -1 per wrong name |

Hallucination detection:
- Any claim not traceable to analysis JSON, DB data, or web research = hallucination
- Each hallucination: -3 points
- Common hallucinations: invented price targets, fabricated news, wrong sector attribution

Score: Start at 10, apply deductions, floor at 0.

#### 3b: Consistency (20%)

Check internal coherence:

| Check | Method | Deduction |
|-------|--------|-----------|
| Signal-recommendation alignment | BUY signal should have bullish commentary | -2 per mismatch |
| Cross-indicator consistency | If RSI says overbought, recommendation shouldn't be STRONG_BUY without explanation | -1 per unexplained conflict |
| Category grouping | Stocks in same category should have consistent framing | -1 per inconsistency |
| Summary vs detail alignment | Summary signal counts must match detailed section | -3 if mismatched |

#### 3c: Coverage (20%)

Verify completeness:

| Check | Method | Deduction |
|-------|--------|-----------|
| Ticker coverage | All tickers in `DEFAULT_STOCKS` should appear | -1 per missing ticker |
| Category coverage | All categories in `TICKER_CATEGORY_MAP` represented | -1 per missing category |
| Signal distribution | BUY/NEUTRAL/SELL counts present in summary | -3 if missing |
| Indicator coverage | Turtle + Bollinger + Oscillator all mentioned | -2 per missing group |
| Hot stocks section | Discovery results included (if discovery ran) | -1 if missing |

#### 3d: Actionability (20%)

Evaluate decision-support quality:

| Check | Method | Deduction |
|-------|--------|-----------|
| Clear recommendations | Each BUY/SELL stock has a stated rationale | -2 per missing rationale |
| Risk factors | Risks mentioned for BUY recommendations | -1 per missing risk |
| Entry/exit context | Price levels or conditions mentioned | -1 per missing context |
| Time horizon | Implicit or explicit time frame stated | -1 if completely absent |

#### 3e: Tone (10%)

Evaluate professional standards:

| Check | Method | Deduction |
|-------|--------|-----------|
| Disclaimer present | "투자 권유가 아닙니다" or equivalent | -5 if missing |
| Balanced language | No hyperbolic claims ("guaranteed", "must buy") | -2 per instance |
| Korean quality | Natural Korean, not machine-translated | -1 per awkward phrasing |
| Professional format | Consistent formatting, proper headers | -1 per issue |

### Step 4: Generate Quality Report

Produce a structured evaluation:

```markdown
## AI Quality Evaluation — {date}

### Overall Score: {weighted_score}/10 — {PASS/REVIEW/FAIL}

| Dimension | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Accuracy | {score}/10 | 30% | {weighted} |
| Consistency | {score}/10 | 20% | {weighted} |
| Coverage | {score}/10 | 20% | {weighted} |
| Actionability | {score}/10 | 20% | {weighted} |
| Tone | {score}/10 | 10% | {weighted} |

### Issues Found

#### Critical (blocks publishing)
- {issue description with specific location}

#### High (should fix before publishing)
- {issue description}

#### Medium (nice to fix)
- {issue description}

### Hallucinations Detected
- {claim} — not traceable to {expected source}

### Recommendations
- {specific fix suggestion}
```

### Step 5: Apply Gate Decision

Based on the overall score:

- **PASS (8.0+)**: Report "Quality gate passed. Safe to publish." and proceed with Slack posting if requested.
- **REVIEW (6.0-7.9)**: List issues with suggested fixes. Ask the user whether to publish as-is, fix and re-evaluate, or abort.
- **FAIL (below 6.0)**: List all critical issues. Recommend re-generating the report. Do not publish.

## Comparison Mode

Compare two reports (e.g., today vs yesterday) to track quality trends:

```
/ai-quality compare 2026-03-06 2026-03-07
```

Compare scores across all 5 dimensions and highlight:
- Improving dimensions (arrow up)
- Declining dimensions (arrow down)
- New issue patterns not seen in the previous report

## Examples

### Example 1: Evaluate today's report

User says: "Check the quality of today's report"

Actions:
1. Read `outputs/reports/daily-2026-03-07.docx`
2. Read `outputs/analysis-2026-03-07.json`
3. Run `weekly_stock_update.py --status` for ground truth
4. Score all 5 dimensions
5. Generate quality report

### Example 2: Pre-publish quality gate

User says: "Run quality gate before posting to Slack"

Actions:
1. Evaluate the latest report
2. If PASS: confirm and offer to post
3. If REVIEW: list fixes needed
4. If FAIL: recommend re-generation

### Example 3: Investigate a specific hallucination

User says: "Yesterday's report said NVDA hit $200 but that seems wrong"

Actions:
1. Read the report and find the NVDA price claim
2. Check DB for NVDA's actual latest close
3. Report: hallucination detected (report says $200, DB says ${actual})
4. Score accuracy dimension with this finding

## Integration

- **Analysis outputs**: `outputs/analysis-{date}.json`, `outputs/discovery-{date}.json`
- **Reports**: `outputs/reports/daily-{date}.docx`
- **Ground truth**: `backend/scripts/weekly_stock_update.py`, `backend/scripts/daily_stock_check.py`
- **Constants**: `backend/app/core/constants.py`
- **Related skills**: `today` (generates reports), `alphaear-reporter` (report content), `evals-skills` (LLM evaluation)
