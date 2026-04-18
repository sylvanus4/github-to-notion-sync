# Autoreason — Borda Count Scoring

The aggregation method for combining multiple judge rankings into a single
winner per tournament round.

---

## Algorithm

### Point Assignment

For a 3-candidate tournament with `N` judges (default N=3):

| Rank | Points |
|------|--------|
| 1st  | 3      |
| 2nd  | 2      |
| 3rd  | 1      |

For a 2-candidate tournament (when one version failed the anti-scope-creep gate):

| Rank | Points |
|------|--------|
| 1st  | 2      |
| 2nd  | 1      |

### Aggregation

```
For each candidate ∈ {A, B, AB}:
  total_score[candidate] = sum(points from each judge's ranking)

winner = argmax(total_score)
```

### Tie-Breaking Rule

When two or more candidates have equal total scores, the **incumbent (A)
wins the tie**. This encodes the "do nothing" bias: a revision must
demonstrably improve upon the original to replace it.

Tie-break priority order:
1. A (incumbent)
2. AB (synthesis — partial preservation of A)
3. B (full revision — highest bar to win)

### Example

3 judges rank {A, B, AB}:

```
Judge 1: AB > A > B  → AB=3, A=2, B=1
Judge 2: A > AB > B  → A=3, AB=2, B=1
Judge 3: AB > B > A  → AB=3, B=2, A=1

Totals: A=6, B=4, AB=8
Winner: AB
```

AB becomes the new A for the next round.

### Tie example

```
Judge 1: A > B > AB  → A=3, B=2, AB=1
Judge 2: B > A > AB  → B=3, A=2, AB=1
Judge 3: A > AB > B  → A=3, AB=2, B=1

Totals: A=8, B=6, AB=4
Winner: A (also highest score, no tie)
```

```
Judge 1: A > B > AB  → A=3, B=2, AB=1
Judge 2: B > AB > A  → B=3, AB=2, A=1
Judge 3: AB > A > B  → AB=3, A=2, B=1

Totals: A=6, B=6, AB=6
Winner: A (tie broken in favor of incumbent)
```

---

## Convergence

### Survival Counter

Track `consecutive_a_wins`:

```
If winner == current_A:
  consecutive_a_wins += 1
Else:
  consecutive_a_wins = 0
  current_A = winner
```

### Termination Condition

```
If consecutive_a_wins >= k:
  CONVERGED — output current_A as final result
```

Default `k = 2`. Higher k (e.g., 3) produces more robust results at the
cost of more tournament rounds.

### Safety Exit

```
If total_rounds >= max_passes:
  FORCE STOP — output current_A regardless of convergence
```

Default `max_passes = 15`.

---

## Quorum

- Default judge panel size: 3
- Minimum quorum for valid round: 2 judges with parseable rankings
- If fewer than 2 judges produce valid rankings, re-dispatch failed judges
  once; if still below quorum, skip the round and increment
  `consecutive_a_wins` (conservative "do nothing" default)

---

## Output Format

Each round records to `pass_{n}/result.json`:

```json
{
  "round": 3,
  "candidates": ["A", "B", "AB"],
  "judge_rankings": [
    {"judge_id": 1, "ranking": ["AB", "A", "B"], "raw_response_file": "judge_1.md"},
    {"judge_id": 2, "ranking": ["A", "AB", "B"], "raw_response_file": "judge_2.md"},
    {"judge_id": 3, "ranking": ["AB", "B", "A"], "raw_response_file": "judge_3.md"}
  ],
  "scores": {"A": 6, "B": 4, "AB": 8},
  "winner": "AB",
  "tie_broken": false,
  "consecutive_a_wins": 0
}
```
