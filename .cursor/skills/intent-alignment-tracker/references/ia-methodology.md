# Intent Alignment Methodology

## 1. IA Scoring Rubric

### Task Completion (40 points)

| Score | Criteria | Example |
|-------|----------|---------|
| 36-40 | All explicit and implicit subtasks completed; user goal fully satisfied | User asked for "add login and tests" → both implemented and passing |
| 28-35 | Major tasks done; minor omissions or edge cases missed | Login added; forgot password reset edge case |
| 20-27 | Partial completion; core functionality present but incomplete | Login UI only; no backend/auth |
| 10-19 | Minimal progress; significant scope left unaddressed | Only created stub files |
| 0-9 | No meaningful completion; wrong direction or abandoned | Implemented unrelated feature |

### Context Relevance (20 points)

| Score | Criteria | Example |
|-------|----------|---------|
| 18-20 | Optimal file/skill selection; minimal search waste | Used existing patterns; invoked correct skill on first try |
| 14-17 | Good selection; occasional detours | Opened 2-3 irrelevant files before finding correct one |
| 10-13 | Mixed; some wrong choices | Invoked generic skill instead of domain-specific; needed correction |
| 5-9 | Poor relevance; many unnecessary reads | Read 10+ files outside scope |
| 0-4 | Wrong context; off-domain actions | Edited unrelated modules; used non-project skills |

### Efficiency (20 points)

| Score | Criteria | Example |
|-------|----------|---------|
| 18-20 | Minimal steps; no redundant tool calls | Single focused edit; one test run |
| 14-17 | Slight overhead | 2-3 extra searches; one unnecessary read |
| 10-13 | Moderate waste | Repeated similar searches; multiple build attempts |
| 5-9 | Significant inefficiency | Many failed attempts; large iteration loops |
| 0-4 | Severe waste | Excessive retries; duplicate work; context overflow |

### Side Effect Control (20 points)

| Score | Criteria | Example |
|-------|----------|---------|
| 18-20 | No unintended changes | Only requested files modified; tests stable |
| 14-17 | Minor side effects; easily reversible | Extra whitespace; one unrelated import |
| 10-13 | Notable side effects | Broke unrelated test; changed shared constant |
| 5-9 | Significant collateral | Broke CI; regressed other features |
| 0-4 | Severe damage | Broke production path; deleted user data |

---

## 2. Data Collection Methodology

### Transcript Parsing

1. **Intent extraction**: Parse first user message for:
   - Imperative verbs (add, fix, implement, refactor)
   - Scope keywords (file paths, feature names, modules)
   - Implicit requirements (tests, docs, conventions)

2. **Action logging**: From agent transcript (`.jsonl`):
   - Tool calls: `Read`, `Grep`, `Write`, `StrReplace`, `Shell`
   - Skills invoked: Extract from `agent_skill` or equivalent
   - File paths touched: Aggregate from tool parameters

3. **Outcome classification**:
   - **Success**: User confirmed; tests pass; no follow-up fix
   - **Partial**: Some subtasks done; user requested changes
   - **Failure**: Wrong solution; abandoned; user rejected

### Required Data Points

- `session_id`, `timestamp`, `duration`
- `user_intent_raw`, `user_intent_parsed`
- `tools_used`, `files_touched`, `skills_invoked`
- `outcome`, `ia_score`, `dimension_scores`

---

## 3. Trend Analysis Algorithms

### Rolling Window

- **Window**: Last N sessions (default N=10)
- **Metric**: Mean IA score per skill
- **Threshold**: ±5 points change vs. prior window

### Skill Classification

| Class | Condition | Action |
|-------|-----------|--------|
| Improving | Score up ≥5 vs. prior window | Monitor; consider promotion |
| Stable | Score change &lt;5 | No change |
| Degrading | Score down ≥5 vs. prior window | Flag for audit |
| Consistently Low | Mean &lt;60 over 20+ sessions | Candidate for deprecation or rewrite |

### Trend Chart Format

- X-axis: Time (sessions or dates)
- Y-axis: IA score (0-100)
- Series: Overall IA, Task Completion, Context Relevance, Efficiency, Side Effect Control
- Annotations: Skill invocations, outcome markers

---

## 4. AgentOS Evaluation Framework (Table 2 Comparison)

| AgentOS Metric | IA Tracker Equivalent | Notes |
|----------------|----------------------|-------|
| Task Success Rate | Task Completion (40%) | Direct mapping |
| Context Retrieval Quality | Context Relevance (20%) | File/skill selection vs. RAG retrieval |
| Turn Efficiency | Efficiency (20%) | Tool call count, iteration depth |
| Harm/Safety | Side Effect Control (20%) | Scope: codebase harm, not general safety |

---

## 5. Sample IA Report Format

```markdown
# Intent Alignment Report — [YYYY-MM-DD] to [YYYY-MM-DD]

## Summary

| Metric | Value |
|--------|-------|
| Sessions analyzed | 47 |
| Mean IA score | 72 |
| Best session | 89 (session_abc123) |
| Worst session | 41 (session_def456) |

## Dimension Breakdown

| Dimension | Mean | Trend |
|-----------|------|-------|
| Task Completion | 75 | → |
| Context Relevance | 70 | ↑ |
| Efficiency | 68 | ↓ |
| Side Effect Control | 76 | → |

## Per-Skill Performance

| Skill | Invocations | Mean IA | Trend |
|-------|-------------|---------|-------|
| backend-expert | 12 | 78 | ↑ |
| frontend-expert | 8 | 65 | ↓ |
| daily-stock-check | 5 | 82 | → |

## Actionable Recommendations

1. **frontend-expert**: Degrading trend; run skill-optimizer audit
2. **Efficiency**: Down-trending; review tool call patterns in recent sessions
3. **Consistently low**: skill-X (mean 52); consider deprecation or merge

## Integration with autoskill-evolve

- 3 sessions with IA &lt;50 fed as evolution candidates
- Skills with mean IA &lt;60 tagged for judge review
```
