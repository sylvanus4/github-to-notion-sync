---
name: sra-bench
description: >-
  SRA-Bench implementation for evaluating skill retrieval quality in this
  project. Measures retrieval accuracy, incorporation precision (hallucination
  rate), and need-awareness across the installed skill corpus. Use when the
  user asks "sra-bench", "SRA 벤치마크", "스킬 검색 평가", "skill retrieval eval",
  "measure skill hallucination", "스킬 환각 측정", or wants to evaluate how well
  the agent selects skills. Do NOT use for skill quality auditing (use
  skill-autoimprove). Do NOT use for token cost measurement (use token-diet).
---

# SRA-Bench -- Skill Retrieval Quality Evaluator

Evaluates how accurately the agent retrieves and incorporates skills from the
installed corpus. Based on SRA-Bench (arXiv:2604.24594) adapted for local
Claude Code environments.

## Metrics

| Metric | What it measures | Target |
|--------|-----------------|--------|
| **Retrieval Recall@5** | Gold skill appears in top-5 candidates | > 80% |
| **Incorporation Precision** | Loaded skill is actually the gold skill | > 70% |
| **Hallucination Rate** | Skill loaded when no gold skill exists | < 20% |
| **Need-Awareness Delta** | Difference in skill-load rate: skill-needed vs not-needed tasks | > 30% |
| **Noise Resistance** | Accuracy with 0 vs 4 vs 8 distractor skills injected | < 10% drop |

## Procedure

### Step 1: Generate Test Cases

Create test cases from the installed skill corpus:

```bash
# Count total skills
total=$(ls .claude/skills/*/SKILL.md 2>/dev/null | wc -l | tr -d ' ')
echo "Total skills in corpus: $total"

# Sample 20 skills as gold skills
ls .claude/skills/*/SKILL.md | shuf | head -20 > /tmp/sra-bench-gold.txt
```

For each gold skill, generate:
- **Positive case**: A task description that should trigger this skill (derived from the skill's trigger phrases)
- **Negative case**: A task that sounds similar but should NOT use this skill (derived from Do NOT use clauses)
- **Native case**: A task that sounds related but can be solved without any skill

Write test cases to `/tmp/sra-bench-cases.json`:

```json
[
  {
    "id": 1,
    "task": "Run the full engineering review pipeline on current diff",
    "gold_skill": "engineering-harness",
    "type": "positive",
    "distractors": ["sales-harness", "legal-harness", "finance-harness"]
  },
  {
    "id": 2,
    "task": "Fix a typo in README.md",
    "gold_skill": null,
    "type": "native",
    "distractors": []
  }
]
```

### Step 2: Run Evaluation Loop

For each test case, simulate the SRA pipeline:

1. **Retrieval**: Search corpus, record top-5 candidates
2. **Incorporation**: Apply need-check, record whether a skill was loaded
3. **Score**:
   - If `type=positive`: Did the gold skill appear in top-5? Was it the one loaded?
   - If `type=native`: Was NO skill loaded? (loading any = hallucination)
   - If `type=negative`: Was the gold skill NOT loaded? (loading it = false positive)

### Step 3: Compute Metrics

```
Retrieval Recall@5 = (positive cases where gold in top-5) / (total positive cases)
Incorporation Precision = (positive cases where gold was loaded) / (total cases where any skill loaded)
Hallucination Rate = (native cases where a skill was loaded) / (total native cases)
Need-Awareness Delta = (skill-load rate for positive) - (skill-load rate for native)
```

### Step 4: Noise Resistance Test

Re-run positive cases with increasing distractor counts:
- 0 distractors: baseline accuracy
- 4 distractors: moderate noise
- 8 distractors: heavy noise

Record accuracy at each level. Plot degradation curve.

### Step 5: Report

Write results to `outputs/sra-bench/sra-bench-{date}.md`:

```markdown
# SRA-Bench Report -- {date}

## Corpus Stats
- Total skills: {N}
- Test cases: {M} (positive: X, native: Y, negative: Z)

## Results

| Metric | Score | Target | Status |
|--------|-------|--------|--------|
| Retrieval Recall@5 | X% | >80% | PASS/FAIL |
| Incorporation Precision | X% | >70% | PASS/FAIL |
| Hallucination Rate | X% | <20% | PASS/FAIL |
| Need-Awareness Delta | X% | >30% | PASS/FAIL |

## Noise Resistance
| Distractors | Accuracy | Delta from baseline |
|-------------|----------|---------------------|
| 0 | X% | -- |
| 4 | X% | -Y% |
| 8 | X% | -Z% |

## Top Failure Cases
[List cases where the wrong skill was selected, with analysis]

## Recommendations
[Actionable improvements: rename skills, improve descriptions, add exclusions]
```

## Modes

| Mode | Trigger | Behavior |
|------|---------|----------|
| `quick` | default | 10 test cases, no noise test |
| `full` | "full bench" | 30 test cases + noise resistance |
| `targeted` | "bench {skill-name}" | Test a specific skill's retrievability |

## Constraints

- Do NOT modify any skill files during evaluation
- Do NOT invoke skills -- only simulate retrieval and incorporation logic
- Test cases must be generated fresh each run (no cached gold answers)
- Report numbers honestly; do not round to manufacture passing scores
