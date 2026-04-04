# hermes-mixture-of-agents

---
name: hermes-mixture-of-agents
version: 1.0.0
description: Multi-model consensus via parallel LLM queries and aggregation for complex reasoning tasks
triggers:
  - "mixture of agents"
  - "multi-model consensus"
  - "MoA analysis"
  - "cross-model verification"
  - "다중 모델 합의"
  - "MoA 분석"
  - "크로스 모델 검증"
  - "모델 합의"
  - "hermes-moa"
  - "consensus analysis"
category: standalone
composable_with:
  - deep-review
  - paper-review
  - trading-intel-orchestrator
  - alphaear-deepear-lite
  - critical-review
  - first-principles-analysis
do_not_use_for:
  - Simple questions with clear answers (use single model directly)
  - Code generation that needs consistent style (style varies across models)
  - Cost-sensitive tasks where one model suffices
  - Tasks requiring tool use (reference models lack tool access)
  - General parallel agent dispatch (use workflow-parallel)
---

## Purpose

Leverage the collective intelligence of multiple frontier LLMs through a
layered architecture to achieve higher-quality reasoning on complex tasks.
Based on the Mixture-of-Agents (MoA) methodology from arXiv:2406.04692
as implemented in nousresearch/hermes-agent.

Reference models generate diverse initial responses in parallel. An
aggregator model then synthesizes these into a single high-quality output,
critically evaluating each response for accuracy, bias, and completeness.

## When to Use

- Complex reasoning tasks where a single model might have blind spots
- High-stakes decisions requiring cross-validation (architecture decisions, security analysis)
- Trading strategy analysis where diverse perspectives improve signal quality
- Paper review where methodological critique benefits from multiple viewpoints
- First-principles analysis where model-specific training biases could skew conclusions

## Architecture

```
User Query
    │
    ├──► Model A (Claude)  ──┐
    ├──► Model B (Gemini)  ──┤
    ├──► Model C (GPT)     ──┼──► Aggregator (strongest model)
    └──► Model D (DeepSeek)──┘          │
                                    Synthesized
                                     Response
```

## Workflow

### Step 1: Classify Query Complexity

Before invoking MoA, verify the task justifies the cost:
- **Skip MoA** if the answer is factual/deterministic (use single model)
- **Use MoA** if the task requires judgment, analysis, or multi-perspective reasoning

### Step 2: Fan Out to Reference Models (Subagent Contract)

Dispatch the user's query to 3-4 frontier models in parallel using the
Task tool with different model slugs.

**Subagent Contract — each reference model MUST receive:**
```
Prompt components:
  1. Original user query (verbatim, no paraphrasing)
  2. System instruction: "Analyze independently. Provide your reasoning chain,
     confidence level (1-10), and key uncertainties."
  3. Output format: "Return a structured response with:
     - main_conclusion: string
     - reasoning_chain: string[]
     - confidence: number (1-10)
     - key_uncertainties: string[]
     - dissenting_considerations: string[]"
```

**Model selection:**
```
Reference Models (parallel):
  - claude-4.6-sonnet-medium-thinking  (balanced reasoning)
  - gpt-5.4-medium                    (strong analytical)
  - claude-4.6-opus-high-thinking     (deep reasoning)
```

**Contract enforcement:**
- Each subagent prompt MUST include all 3 components above — partial prompts produce unreliable results
- Return format MUST be parseable — reject free-form responses that lack the structured fields
- Minimum 2 successful responses required to proceed (graceful degradation if one model fails)
- Set `readonly: true` on all reference model subagents (they analyze, not execute)

### Step 3: Aggregate Responses

Feed all reference responses to the aggregator model with this system prompt:

```
You have been provided with a set of responses from various models to the
latest user query. Your task is to synthesize these responses into a single,
high-quality response. It is crucial to critically evaluate the information
provided in these responses, recognizing that some of it may be biased or
incorrect. Your response should not simply replicate the given answers but
should offer a refined, accurate, and comprehensive reply. Ensure your
response is well-structured, coherent, and adheres to the highest standards
of accuracy and reliability.

Responses from models:
1. [Model A response]
2. [Model B response]
3. [Model C response]
```

Aggregator settings:
- Model: `claude-4.6-opus-high-thinking` (strongest synthesis capability)
- Temperature: 0.4 (focused synthesis for consistency)

### Step 4: Structure the Output

Present the synthesized response with:
1. **Consensus points** — where all models agreed
2. **Divergence points** — where models disagreed (with reasoning)
3. **Synthesized conclusion** — the aggregator's refined answer
4. **Confidence assessment** — based on inter-model agreement level

## Output Format

```markdown
## MoA Analysis: <Topic>

### Consensus (all models agreed)
- Point 1
- Point 2

### Divergence (models disagreed)
| Point | Model A | Model B | Model C |
|---|---|---|---|
| ... | ... | ... | ... |

### Synthesized Conclusion
<Aggregator's refined answer>

### Confidence: HIGH / MEDIUM / LOW
- Agreement level: X/Y models aligned on core conclusion
- Key uncertainty: <what remains ambiguous>

---
*MoA: 3 reference models → 1 aggregator | Total cost: ~$X.XX*
```

## Cost Awareness

| Configuration | Approximate Cost | Use When |
|---|---|---|
| 3 Sonnet refs + Opus aggregator | ~$0.50-2.00 per query | Default for important decisions |
| 2 Sonnet refs + Sonnet aggregator | ~$0.15-0.50 per query | Budget mode |
| 3 Opus refs + Opus aggregator | ~$2.00-8.00 per query | Maximum quality, rare use |

Always report estimated cost in the output footer.

## Retry and Failure Handling

1. **Single model failure**: Continue with remaining models if ≥ 2 succeed
2. **Rate limit**: Exponential backoff (2s, 4s, 8s, 16s, 32s, max 60s)
3. **All models fail**: Fall back to single-model response with a note
4. **Empty responses**: Retry once, then exclude from aggregation

## Verification (Mandatory)

Before presenting MoA results as final:

1. **Count check**: Confirm ≥ 2 reference model responses were received and parsed
2. **Format check**: Each response contains `main_conclusion`, `confidence`, and `key_uncertainties` fields
3. **Divergence check**: If all models agree with confidence > 8, verify this isn't confirmation bias — run the Karpathy Opposite Direction Test on the consensus conclusion
4. **Cost check**: Calculate actual token cost and compare against the pre-estimate; flag if > 150% of estimate

Never present "Consensus: HIGH" when only 2 out of 3 models responded unless both models explicitly agree with confidence ≥ 7.

## Anti-Gold-Plating

MoA is expensive. Do NOT use it when:
- The query has a deterministic answer (code compilation, math, lookup)
- A single model with confidence ≥ 8 would suffice
- The user wants speed over thoroughness
- The total conversation already used > $5.00 in MoA costs this session

Default to budget mode (2 Sonnet refs + Sonnet aggregator). Escalate to Opus-heavy configuration ONLY when the user explicitly requests "maximum quality" or the topic is a $100K+ financial decision.

## Safety Rules

1. **Never use MoA for simple tasks** — classify complexity first
2. **Report cost** — always show estimated token cost in output
3. **Preserve attribution** — note which model contributed which insight
4. **No recursive MoA** — aggregator output is final, no further rounds
5. **User opt-in** — inform the user that MoA will be used and the approximate cost before proceeding

## Examples

### Example 1: Architecture Decision
```
User: "마이크로서비스 vs 모놀리스 아키텍처, 우리 프로젝트에 뭐가 맞아?"
Agent: Dispatches to 3 models → aggregates → presents consensus/divergence matrix
```

### Example 2: Trading Strategy Validation
```
User: "이 매매 전략의 논리적 결함을 찾아줘"
Agent: Each model independently analyzes the strategy → aggregator synthesizes
       flaws that multiple models identified (high confidence) vs single-model
       findings (lower confidence)
```

### Example 3: Paper Review Enhancement
```
User: "이 논문의 methodology 강점과 약점을 크로스 모델로 검증해줘"
Agent: MoA analysis of methodology → presents where models converge on
       strengths/weaknesses vs where they diverge
```
