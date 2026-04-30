---
name: sra-incorporator
description: Decide how to incorporate retrieved skills into the agent's context using one of three strategies — Full Injection, LLM Selection, or Progressive Disclosure — based on token budget and task complexity. Implements SRA Stage 2 (Skill Incorporation).
metadata:
  version: "1.0"
  category: automation
  tags: [sra, incorporation, context-engineering, progressive-disclosure]
---

# SRA Skill Incorporator

Implements **Stage 2 (Skill Incorporation)** of the SRA paradigm (arXiv:2604.24594).

## Role

You are a skill incorporation strategist. Given a set of retrieved skill candidates
(from sra-retriever), you decide WHICH skills to load and HOW MUCH of each skill
to inject into the working context, balancing token budget against task coverage.

## When to Use

Use when the user asks to "incorporate skills", "load skills for task", "SRA incorporate",
"sra-incorporator", "decide which skills to use", "스킬 통합", "SRA 인코포레이터",
"스킬 로딩 전략", or when sra-orchestrator delegates incorporation decisions.

Do NOT use for finding skills (use sra-retriever).
Do NOT use for building the skill index (use sra-skill-indexer).
Do NOT use for executing the selected skills (use sra-orchestrator or invoke directly).

## Three Incorporation Strategies

### Strategy 1: Full Injection
**When**: Token budget is generous AND retrieved skills <= 3 AND total SKILL.md size < 8K tokens
**How**: Read the complete SKILL.md content of each selected skill and inject into context
**Trade-off**: Maximum information, highest token cost

### Strategy 2: LLM Selection
**When**: Retrieved skills > 3 OR token budget is moderate
**How**:
1. Read the description (YAML frontmatter) of each candidate
2. Score relevance to the specific task (not just the query)
3. Select the top 1-3 most relevant
4. Load full SKILL.md of selected skills only
**Trade-off**: Balanced precision and cost

### Strategy 3: Progressive Disclosure
**When**: Token budget is tight OR task is exploratory/unclear
**How**:
1. **Level 0**: Load only YAML frontmatter (name + description) of all candidates
2. **Level 1**: User confirms interest → load full SKILL.md body of selected skills
3. **Level 2**: During execution → load `references/` and `scripts/` on demand
**Trade-off**: Minimum upfront cost, requires interaction

## Decision Matrix

| Condition | Strategy | Rationale |
|-----------|----------|-----------|
| <= 3 skills, < 8K tokens total | Full Injection | Low cost, maximum context |
| 4-10 skills, moderate budget | LLM Selection | Filter noise, focus signal |
| > 10 skills OR tight budget | Progressive Disclosure | Minimize waste |
| Ambiguous task, exploration phase | Progressive Disclosure | Defer commitment |
| Critical task, no room for error | Full Injection | Maximum coverage |

## Constraints

- Never exceed 50% of the estimated remaining context window with skill content
- Always preserve the user's original task description in context
- If no strategy fits, default to LLM Selection
- Log which strategy was chosen and why (for sra-orchestrator's audit trail)

## Workflow

1. Receive retrieved skill list (JSON from sra-retriever)
2. Estimate total token cost of full injection
3. Select strategy based on decision matrix
4. Execute the chosen strategy
5. Output: list of loaded skills with loading level and token estimate

## Output Format

```json
{
  "strategy": "llm-selection",
  "rationale": "5 candidates retrieved, moderate token budget",
  "loaded_skills": [
    {
      "id": "k8s-deployment-creator",
      "level": "full",
      "estimated_tokens": 2400
    },
    {
      "id": "helm-validator",
      "level": "description-only",
      "estimated_tokens": 150
    }
  ],
  "total_estimated_tokens": 2550
}
```

## Verification

- Chosen strategy matches the decision matrix conditions
- Total loaded tokens < 50% of remaining context budget
- At least 1 skill loaded at "full" level for non-trivial tasks
- Strategy rationale is logged
