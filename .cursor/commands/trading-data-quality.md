---
description: "Validate data quality in market analysis reports before publication"
argument-hint: "Path to markdown report file (e.g., outputs/reports/trading/weekly_review_2026-03-08.md)"
---

# Trading Data Quality Check

## Skill Reference

Read and follow `.cursor/skills/trading-data-quality-checker/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Identify Target File

- If `$ARGUMENTS` contains a file path, use that file
- If `$ARGUMENTS` is empty, scan `outputs/reports/trading/` for the most recent `.md` file

### Step 2: Run Quality Checks

Run the data quality checker:

```bash
python3 .cursor/skills/trading-data-quality-checker/scripts/check_data_quality.py \
  --file TARGET_FILE \
  --output-dir outputs/reports/trading/
```

### Step 3: Report Findings

Present results:
- Pass/warn count per category
- Specific findings with line references
- Recommended corrections

## Categories Checked

1. Price scale inconsistencies (ETF vs futures digit hints)
2. Instrument notation consistency
3. Date/weekday mismatches
4. Allocation total errors
5. Unit mismatches

## Constraints

- Advisory mode: flags issues for human review
- No API keys required
- Works offline on local markdown files
