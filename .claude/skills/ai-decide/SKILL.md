---
name: ai-decide
description: >-
  Decision support with provenance-separated evidence from MemKraft and LLM
  Wiki. Retrieves relevant official policies, past decisions from personal
  memory, and unresolved context, then presents a structured decision brief
  with clear source attribution. Applies the Karpathy Opposite Direction Test
  to prevent sycophantic agreement. Use when the user asks "ai decide", "help
  me decide", "decision support", "what should I do about", "ai-decide", "AI
  의사결정", "결정 도와줘", "어떻게 해야 할까", "의사결정 지원", "판단 도와줘", or wants evidence-backed
  decision support with provenance. Do NOT use for automated decision
  execution without human review (always present options). Do NOT use for
  trading decisions (use daily-stock-check or trading-agent-desk). Do NOT use
  for simple recall without decision framing (use ai-recall). Do NOT use for
  strategic analysis without personal context (use role-dispatcher).
---

# ai-decide — Provenance-Tagged Decision Support

Retrieves official policies (Wiki), past decisions and preferences (MemKraft),
and related unresolved items, then presents a structured decision brief with
options, evidence sources, and a recommendation that explicitly accounts for
potential conflicts between personal history and official policy.

## Output Language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

## Architecture

```
ai-decide (decision question)
  │
  ├─→ ai-context-router (query: decision context)
  │     ├─ MemKraft: past decisions, preferences, unresolved
  │     └─ Wiki: policies, procedures, precedents
  │
  ├─→ Conflict Detection (personal vs. official)
  │
  ├─→ Option Generation (2-4 options with evidence)
  │
  └─→ Opposite Direction Test (strongest counter-argument)
```

## Workflow

### Step 1: Decision Framing

Parse the decision question and extract:
- The core decision to be made
- Stakeholders affected
- Time constraints
- Domain (engineering, product, personal, etc.)

### Step 2: Context Assembly

Invoke `ai-context-router` with the decision question.
Always include `--deep` for decisions affecting multiple domains.

### Step 3: Conflict Detection

Compare personal context (MemKraft) with official policy (Wiki) to identify:
- Alignment: personal practice matches policy
- Divergence: personal preference differs from policy
- Gaps: no policy exists, only personal precedent

### Step 4: Option Generation

Generate 2-4 options, each grounded in retrieved evidence:
- Option A: aligned with official policy
- Option B: aligned with personal preference/history
- Option C: synthesis/compromise (when A and B conflict)
- Option D: "do nothing" / defer (when applicable)

### Step 5: Opposite Direction Test

For the recommended option, construct the strongest counter-argument.
If the counter-argument is comparably strong, flag the ambiguity.

### Step 6: Decision Brief

```markdown
## 🎯 의사결정 지원: "{decision question}"

### Official Knowledge (LLM Wiki)
- [COMPANY] <relevant company policies>
- [TEAM:<domain>] <team-specific guidelines>

### Personal Context (MemKraft)
- [RECENT] <past similar decisions and outcomes>
- [PREFERENCE] <established personal patterns>
- [UNRESOLVED] <related open items>

### 충돌 분석
- {where personal context aligns with / diverges from official policy}

### 옵션
| 옵션 | 근거 | 출처 | 리스크 |
|------|------|------|--------|
| A: {option} | {evidence} | [COMPANY] | {risk} |
| B: {option} | {evidence} | [PREFERENCE] | {risk} |
| C: {option} | {evidence} | Mixed | {risk} |

### 반론 (Opposite Direction Test)
{strongest argument against the recommended option}

### Recommendation
{recommended option with reasoning, explicitly noting provenance of
 supporting evidence and any unresolved tensions}
```

## Integration

- **Upstream**: User invocation
- **Core dependency**: `ai-context-router` for provenance-tagged context
- **Complements**: `decision-tracker` for logging the final decision
- **Output**: Structured Korean decision brief with provenance and counter-arguments
