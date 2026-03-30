# Comparator Protocol

A/B blind comparison protocol for skill evaluation. An independent Comparator agent judges two outputs without knowing which came from which skill version, eliminating confirmation bias.

## Table of Contents

- [When to Use](#when-to-use)
- [Anonymization Protocol](#anonymization-protocol)
- [Comparator Agent Specification](#comparator-agent-specification)
- [Execution Protocol](#execution-protocol)
- [Report Format](#report-format)
- [Interpreting Results](#interpreting-results)
- [Error Handling](#error-handling)

## When to Use

- **Version comparison**: Skill v1 vs Skill v2 after edits
- **Skill vs baseline**: Skill-assisted output vs unassisted output
- **Approach comparison**: Two different skills addressing the same problem
- **Regression check**: Current model + skill vs previous model + skill

## Anonymization Protocol

Context contamination is the primary threat to blind comparison. The Comparator must not be able to infer which output came from which version.

### What to strip

Before sending outputs to the Comparator, remove or replace:

1. **Skill name references**: Replace "Using [skill-name] skill..." with generic phrasing
2. **Version identifiers**: Remove "v1", "v2", version numbers, dates
3. **Skill-specific section headers**: If the skill prescribes unique headers, note them but don't strip (they are part of the quality signal)
4. **Meta-commentary about the skill**: "As instructed by the skill...", "Following the skill's workflow..."
5. **Tool call references** that reveal skill identity

### What to preserve

- All substantive output content
- Structure and formatting
- Code blocks and examples
- Error handling and edge case coverage

### Anonymization template

```
## Output [A/B]

The following was produced by an AI assistant in response to the prompt below.

### Prompt
[Original test prompt — identical for both]

### Response
[Anonymized agent output]
```

### Randomization

Randomly assign which version gets label "A" and which gets "B" for each test case. Record the mapping but do not reveal it to the Comparator.

```
Mapping (hidden from Comparator):
  Test 1: A = with-skill,    B = without-skill
  Test 2: A = without-skill, B = with-skill
  Test 3: A = skill-v2,      B = skill-v1
```

## Comparator Agent Specification

### Prompt template

```
You are an impartial quality judge. You will evaluate two AI assistant outputs
that responded to the same prompt. You do NOT know which output was produced
by which method. Judge purely on output quality.

## Evaluation Criteria
[List of criteria from test case]

## Output A
[Anonymized output A]

## Output B
[Anonymized output B]

## Instructions

For EACH criterion, provide:
1. Winner: A, B, or Tie
2. Confidence: 1 (uncertain) to 5 (definitive)
3. Reasoning: One sentence explaining your judgment

Then provide:
- Overall winner: A, B, or Tie
- Overall confidence: 1-5
- Summary: 2-3 sentences explaining the overall verdict

IMPORTANT:
- Judge ONLY on the quality of the outputs, not on length or verbosity
- A longer output is not automatically better
- Focus on accuracy, relevance, completeness, and clarity
- If both outputs are roughly equal, say Tie — do not force a winner
```

### Subagent configuration

- Type: `generalPurpose`
- Model: inherited from parent (judgment quality matters)
- Readonly: `true`
- Key constraint: Comparator MUST NOT have access to the skill files or the version mapping

## Execution Protocol

### Phase 1: Prepare Test Cases

1. Define or reuse test cases from the eval framework
2. For each test case, verify that the prompt is identical for both versions

### Phase 2: Run Executors

For each test case:
1. Launch Executor subagent with Version A's skill → capture Output-A
2. Launch Executor subagent with Version B's skill (or no skill) → capture Output-B
3. Both Executors run in parallel (independent contexts)

### Phase 3: Anonymize

For each test case:
1. Apply anonymization protocol to both outputs
2. Randomly assign A/B labels (record the hidden mapping)
3. Verify no skill-identifying information remains

### Phase 4: Blind Judgment

For each test case:
1. Launch Comparator subagent with anonymized Output A and Output B
2. Comparator returns per-criterion verdict and overall winner

### Phase 5: De-anonymize and Aggregate

1. Reveal the hidden mapping for each test case
2. Tally results:

```
Version Comparison Summary
==========================
Total test cases: [N]

Per-criterion results:
  [criterion-1]: Version-X wins [N], Version-Y wins [N], Tie [N]
  [criterion-2]: Version-X wins [N], Version-Y wins [N], Tie [N]

Overall:
  Version-X wins: [N] / [total] ([%])
  Version-Y wins: [N] / [total] ([%])
  Ties:           [N] / [total] ([%])

Confidence-weighted score:
  Version-X: [weighted win score]
  Version-Y: [weighted win score]
```

Confidence-weighted score: each win is multiplied by the Comparator's confidence (1-5), then summed and normalized.

## Report Format

```
A/B Comparison Report
=====================
Skill: [skill-name]
Date: [YYYY-MM-DD]
Comparison: [Version-X label] vs [Version-Y label]

Test Cases: [N]
Overall Winner: [Version-X / Version-Y / Tie]

Detailed Results:
┌─────────────┬────────────┬────────┬──────────┬────────────────────────────┐
│ Test Case   │ Criterion  │ Winner │ Conf(1-5)│ Reasoning                  │
├─────────────┼────────────┼────────┼──────────┼────────────────────────────┤
│ test-1      │ accuracy   │ A      │ 4        │ More precise data handling  │
│ test-1      │ format     │ Tie    │ 3        │ Both follow structure well  │
│ test-2      │ accuracy   │ B      │ 5        │ Catches edge case missed   │
│ ...         │ ...        │ ...    │ ...      │ ...                        │
└─────────────┴────────────┴────────┴──────────┴────────────────────────────┘

Summary:
  [Version-X]: [N] wins ([%]), confidence-weighted: [score]
  [Version-Y]: [N] wins ([%]), confidence-weighted: [score]
  Ties: [N] ([%])

Recommendation: [Ship Version-X / Keep Version-Y / No significant difference]
```

## Interpreting Results

| Win Rate | Confidence | Recommendation |
|----------|------------|----------------|
| > 70% one version | >= 3 avg | Clear winner — ship the winner |
| 55-70% one version | >= 3 avg | Likely better — consider merging strengths |
| 45-55% split | Any | No significant difference — keep simpler version |
| Any | < 2 avg | Low confidence — add more test cases or refine criteria |

## Common Pitfalls

| Pitfall | Mitigation |
|---------|------------|
| Comparator identifies skill from output style | Strengthen anonymization; strip meta-commentary |
| Length bias (longer = better) | Add explicit instruction: "longer is not automatically better" |
| Forced winners when quality is equal | Allow Tie verdicts; do not penalize ties |
| Too few test cases (< 3) | Minimum 3 test cases for meaningful comparison |
| Criteria too vague | Use specific, measurable criteria (not "is it good?") |

## Error Handling

| Error | Action |
|-------|--------|
| Comparator returns incomplete verdict | Re-run with explicit format instructions |
| Anonymization leaks skill identity | Re-anonymize more aggressively, re-run comparison |
| One Executor fails | Report partial results, note missing test case |
| All verdicts are Tie | Not necessarily an error — report as "no significant difference" |
