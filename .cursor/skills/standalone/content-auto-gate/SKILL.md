# Content Auto-Gate

## Description

Automated content quality gate that scores AI-generated stock content drafts on 5 dimensions (accuracy, compliance, tone, completeness, originality) and auto-approves drafts scoring above a configurable threshold. Drafts below the threshold are rejected with actionable feedback. Replaces manual Slack-based approval workflow.

## Triggers

Use when the user asks to:
- "quality check content", "auto-approve content", "run quality gate"
- "content auto-gate", "score content drafts", "check content quality"
- "콘텐츠 품질 검사", "콘텐츠 자동 승인", "품질 게이트"

Do NOT use for:
- Running the content generation pipeline (use `stock-content-printer`)
- Manual Slack approval (deprecated)
- AI report quality evaluation (use `ai-quality-evaluator`)
- Code quality review (use `deep-review` or `simplify`)

## Procedure

### 1. Locate drafts

```bash
ls outputs/content/drafts/drafts-$(date +%Y-%m-%d).json
```

If no drafts exist, run the content generation pipeline first via `/stock-content` or the `daily-content.yml` workflow.

### 2. Run the quality gate

```bash
cd backend
python scripts/content_quality_gate.py --date $(date +%Y-%m-%d)
```

Options:
- `--threshold 7.0` — Minimum score for auto-approval (default: 7.0)
- `--dry-run` — Score without writing approved/rejected files

### 3. Review results

Check the gate report:
```bash
cat outputs/content/gate-report-$(date +%Y-%m-%d).json
```

The report contains:
- Per-draft scores across 5 dimensions
- Issues found (compliance violations, hallucinations, missing disclaimers)
- Approval/rejection count

### 4. Manual override (if needed)

For rejected drafts that should be approved:
```bash
# Move from rejected to approved
mv outputs/content/rejected/{channel}-{date}.json outputs/content/approved/
```

## Scoring Dimensions

| Dimension      | Weight | What it checks                                    |
|----------------|--------|---------------------------------------------------|
| Accuracy       | 1x     | Claims match provided data, no hallucinated numbers|
| Compliance     | 1x     | Disclaimers present, no return promises            |
| Tone           | 1x     | Professional, not sensational or clickbait         |
| Completeness   | 1x     | Actionable context beyond raw tickers              |
| Originality    | 1x     | Not generic AI-sounding filler content             |

## Pipeline Integration

This skill is integrated into the `daily-content.yml` GitHub Actions workflow as the `quality-gate` job, running between content generation and distribution. It replaces the previous `slack-approval` job.

```
generate-content → quality-gate → distribute-content
```

## Output

- `outputs/content/approved/{channel}-{date}.json` — Auto-approved drafts
- `outputs/content/rejected/{channel}-{date}.json` — Rejected drafts with reasons
- `outputs/content/gate-report-{date}.json` — Full scoring report
