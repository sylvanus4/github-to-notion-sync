---
name: game-studio-balance-check
description: "Verify puzzle difficulty distribution, scoring curves, and clue fairness. Use when the user asks to 'check game balance', 'validate difficulty', 'game-balance-check', 'difficulty audit', '게임 밸런스', '난이도 검증', '밸런스 체크'. Do NOT use for QA test planning (use game-studio-qa-plan). Do NOT use for simulated playtesting (use game-studio-playtest-report). Do NOT use for GDD authoring (use game-studio-design-system)."
---

# Game Balance Check — Difficulty & Fairness Validator

Verify that puzzle difficulty distribution, scoring curves, and clue systems produce fair and engaging gameplay. Analyzes the puzzle bank for statistical balance and flags outliers.

Use when the user asks to "check game balance", "validate difficulty", "game-balance-check", "difficulty audit", "게임 밸런스", or wants to ensure puzzles are fair and well-distributed across difficulty levels. Do NOT use for QA test planning (use qa-plan) or simulated playtesting (use playtest-report).

## Balance Dimensions

### 1. Puzzle Difficulty Distribution
- **Easy** (solvable in 1-2 clues): ~30% of puzzle bank
- **Medium** (solvable in 3-4 clues): ~50% of puzzle bank
- **Hard** (requires 5+ clues): ~20% of puzzle bank
- No puzzle should be unsolvable
- No puzzle should be trivially solvable with 0 clues

### 2. Clue Effectiveness
- Each clue must eliminate at least 1 suspect (no "dead" clues)
- No single clue should be a "silver bullet" (immediately solve the puzzle alone)
- Clue ordering should progressively narrow the suspect pool
- Information value of clues should vary to create decision tension

### 3. Scoring Fairness
- Score formula rewards fewer clues used
- Score difference between adjacent clue counts is meaningful but not punitive
- Perfect score (1-clue solve) is achievable but rare (~5% of puzzles)
- No negative scores or scoring cliffs

### 4. Session Length
- Average solve time: 2-5 minutes
- No puzzle takes > 10 minutes for a reasonable player
- Daily commitment feels light (under 5 minutes)

### 5. Streak & Engagement Balance
- Streak doesn't punish timezone differences
- Archive mode exists for catch-up
- Difficulty doesn't spike unpredictably day-to-day

## Workflow

### Step 1: Audit Puzzle Bank
Scan the puzzle bank and categorize each puzzle by minimum clues needed to solve.

### Step 2: Difficulty Distribution Report
Generate a histogram of puzzle difficulty. Flag if distribution violates the 30/50/20 target.

### Step 3: Clue Effectiveness Audit
For each puzzle, verify:
- Every clue eliminates ≥1 suspect
- No single clue is a silver bullet
- Clue sequence forms a logical narrowing

### Step 4: Scoring Curve Analysis
Plot the score-vs-clues-used curve. Verify it's monotonically decreasing and has no cliffs.

### Step 5: Outlier Flagging
Flag puzzles that are:
- Too easy (solvable with 0 additional clues beyond grid layout)
- Too hard (requires all clues and still ambiguous)
- Unfair (solution requires meta-knowledge outside the clue system)

### Step 6: Recommendations
Produce specific tuning recommendations:
- Puzzles to replace or adjust
- Clue rewording suggestions
- Scoring parameter adjustments

## Output
A structured markdown balance report with:
1. Difficulty distribution histogram (ASCII or Mermaid bar chart)
2. Per-puzzle difficulty classification
3. Flagged outliers with specific issues
4. Scoring curve assessment
5. Actionable tuning recommendations
