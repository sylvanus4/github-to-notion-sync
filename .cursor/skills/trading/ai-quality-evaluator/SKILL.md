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

## Meta-Orchestration

Use this section for multi-skill runs: **delegation order**, **failure handling**, **how sub-outputs merge**, and **user-facing overrides**.

### Prompt router (representative user phrases)

| # | Example prompt | This skill? | Delegation order (numbered) | Output merge strategy | User overrides |
|---|----------------|-------------|------------------------------|------------------------|----------------|
| 1 | AI 리포트 품질을 자동 평가해줘 | Yes | 1) Resolve `DATE` → 2) Load artifacts (docx/json) → 3) Ground truth (`weekly_stock_update.py --status`, `daily_stock_check.py --source db`, constants) → 4) Score 5 dimensions → 5) Emit gate markdown → 6) Optional: hand off to Slack MCP only if user asks and gate PASS/REVIEW | **Single** evaluation doc: gate line + weighted table + issues + hallucinations + recommendations (do not split across files) | `DATE=YYYY-MM-DD`; optional explicit paths for report/docx and `analysis-{date}.json`; `SKIP_DB=1` to run reduced accuracy mode (must label REVIEW) |
| 2 | 데일리 파이프라인을 설계해줘 | No | 1) `today` SKILL (run path) **or** `ai-workflow-integrator` (custom design) — pick one based on “run existing” vs “design new” | Downstream skill defines merge | As in target skill |
| 3 | 이 프로세스를 자동화할지 결정해줘 | No | 1) `automation-strategist` → 2) if implement: `pipeline-builder` (cron/GHA) or `ai-workflow-integrator` (AI stages) | Strategist doc + optional build artifacts | ARIA thresholds user-adjustable |
| 4 | 시스템 데이터 흐름을 분석해줘 | No | 1) `system-thinker` (map/bottleneck) → 2) optional `visual-explainer` | Map + bottleneck appendix | Diagram depth / scope from user |
| 5 | 프로젝트 컨텍스트를 업데이트해줘 | No | 1) `context-engineer` Mode 1 (MEMORY) or Mode 2 (package) | MEMORY.md + optional `references/*-context.md` | `PRUNE_DAYS` default 30 |

### Error recovery (this skill)

| Failure mode | Retry | Fallback | Abort |
|--------------|-------|----------|-------|
| Artifact missing | — | Ask user for path or adjacent `DATE` | If no inputs after 1 clarification |
| DB/script error | 2×, 5s backoff | Run JSON-only scoring; mark Accuracy/Consistency **REVIEW** | User requires full DB gate and DB down |
| docx read fails | — | Use `anthropic-docx` or JSON-only | — |
| Comparison mode second date missing | — | Run single-date eval | — |

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

## Error Handling

| Issue | Resolution |
|-------|-----------|
| Unexpected input format | Validate input before processing; ask user for clarification |
| External service unavailable | Retry with exponential backoff; report failure if persistent |
| Output quality below threshold | Review inputs, adjust parameters, and re-run the workflow |

## Verification Protocol

Before reporting any review or audit complete, verify findings with evidence:

    ### Check: [what you are verifying]
    **Command run:** [exact command executed]
    **Output observed:** [actual output — copy-paste, not paraphrased]
    **Result:** PASS or FAIL (with Expected vs Actual if FAIL)

A check without a command-run block is not a PASS — it is a skip.

Before issuing PASS: must include at least one adversarial probe (boundary input, concurrent request, missing data, permission edge case).

Before issuing FAIL: check if the issue is already handled elsewhere, intentional by design, or not actionable without breaking an external contract.

End verification with: `VERDICT: PASS`, `VERDICT: FAIL`, or `VERDICT: PARTIAL`.

## Honest Reporting

- Report review outcomes faithfully: if a check fails, say so with the relevant output
- Never claim "all checks pass" when output shows failures
- Never suppress or simplify failing checks to manufacture a green result
- When a check passes, state it plainly without unnecessary hedging
- The final report must accurately reflect what was found — not what was hoped

## Rationalization Detection

Recognize these rationalizations and do the opposite:

| Rationalization | Reality |
|----------------|---------|
| "The code looks correct based on my reading" | Reading is not verification. Run it. |
| "The implementer's tests already pass" | The implementer is an LLM. Verify independently. |
| "This is probably fine" | Probably is not verified. Run it. |
| "I don't have access to test this" | Did you check all available tools? |
| "This would take too long" | Not your call. Run the check. |
| "Let me check the code structure" | No. Start the server and hit the endpoint. |

If you catch yourself writing an explanation instead of running a command, stop. Run the command.
