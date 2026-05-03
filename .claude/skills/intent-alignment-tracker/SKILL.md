---
name: intent-alignment-tracker
description: >-
  Measures Intent Alignment (IA) — the semantic gap between user goals and
  agent-executed actions. Use when the user asks to "check intent alignment",
  "IA score", "session evaluation", "skill performance", "의도 정렬 점수", "세션 평가",
  "스킬 성능 추적", or wants post-session evaluation and trend dashboards. Do NOT
  use for AI report quality (use ai-quality-evaluator), code review (use
  deep-review), or general LLM evaluation (use evals-skills).
---

# Intent Alignment Tracker

Measures and tracks **Intent Alignment (IA)** — the semantic gap between a user's goal and the agent's executed actions. Based on AgentOS paper's evaluation framework (§3.4) with Tri-Agent evaluation concepts.

## Instructions

1. **Post-Session Evaluation**: After a task session, analyze:
   - User's original intent (from first message)
   - Actions taken by agent (tool calls, file edits, commands)
   - Final outcome (success/partial/failure)

2. **IA Score Calculation** (0-100):
   - **Task Completion (40%)**: Were all requested tasks completed?
   - **Context Relevance (20%)**: Were the right files/skills used?
   - **Efficiency (20%)**: Minimal unnecessary actions?
   - **Side Effect Control (20%)**: No unintended changes?

3. **Per-Skill Tracking**: Log which skills were invoked and their individual IA scores

4. **Trend Analysis**: Compare IA scores over time to identify:
   - Improving skills (score trending up)
   - Degrading skills (score trending down)
   - Consistently low-performing skills (candidates for improvement/deprecation)

5. **Report Generation**: Produce a weekly/monthly IA dashboard

6. **Integration with autoskill**: Feed IA data into autoskill-evolve for evidence-based skill evolution

## Output

- IA score card with per-dimension scores
- Trend chart
- Actionable recommendations

## Triggers

- "check intent alignment"
- "IA score"
- "session evaluation"
- "skill performance"
- "intent alignment"
- "의도 정렬 점수"
- "세션 평가"
- "스킬 성능 추적"

## Do NOT use for

- AI report quality scoring (use ai-quality-evaluator)
- Code review (use deep-review)
- General LLM evaluation (use evals-skills)
