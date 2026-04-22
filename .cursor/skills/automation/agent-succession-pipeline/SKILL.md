---
name: agent-succession-pipeline
description: >-
  Fine-tune replacement models from agent decision history, evaluate candidates
  against the base model, and manage the model switch with rollback capability.
  Reads training data from icarus-memory-fabric, launches fine-tune jobs via
  Together AI or HuggingFace, runs head-to-head evaluations, and switches to
  the best model.
  Use when the user asks to "train successor model", "fine-tune from history",
  "replace model", "model succession", "evaluate candidate model", "switch
  model", "rollback model", "agent succession", "self-training", "후임 모델 훈련",
  "모델 교체", "모델 평가", "후임 파이프라인", "자기 훈련", "모델 롤백",
  "agent-succession-pipeline", or wants to create a cheaper/specialized model
  trained on the agent's own high-quality decisions.
  Do NOT use for skill prompt optimization (use skill-autoimprove).
  Do NOT use for general model training without agent history (use hf-model-trainer).
  Do NOT use for model search and discovery (use hf-models or hf-model-arena).
  Do NOT use for memory operations (use icarus-memory-fabric).
  Do NOT use for evaluating LLM prompts (use evals-skills).
  Korean triggers: "후임 모델", "모델 자기 훈련", "모델 교체 파이프라인", "에이전트 후임".
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "automation"
  source: "esaradev/icarus-plugin"
---

# Agent Succession Pipeline — Model Self-Training and Replacement

Train a cheaper or specialized model from an agent's own decision history,
evaluate it against the current model, and switch over with rollback safety.
The agent literally trains its own successor while working.

Adapted from [esaradev/icarus-plugin](https://github.com/esaradev/icarus-plugin)'s
model replacement pipeline.

---

## Why Succession

Premium models (Claude Opus, GPT-4) produce excellent decisions but cost more.
After accumulating enough high-quality decisions in the memory fabric, a smaller
model can be fine-tuned to replicate those decision patterns at a fraction of
the cost — for specific, well-understood tasks.

This is NOT about replacing the primary model for all tasks. It is about
creating specialized successors for repetitive, well-defined workflows where
the decision patterns are stable.

---

## Pipeline Stages

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│  1. Extract  │───▶│  2. Train    │───▶│  3. Evaluate │
│  Training    │    │  Fine-tune   │    │  Head-to-   │
│  Data        │    │  Job         │    │  Head       │
└─────────────┘    └──────────────┘    └──────┬──────┘
                                              │
                                    ┌─────────▼─────────┐
                                    │  4. Switch / Keep  │
                                    │  (with rollback)   │
                                    └───────────────────┘
```

---

### Stage 1: Extract Training Data

Read from `icarus-memory-fabric` and produce training pairs:

```bash
# Extract high-precision pairs from fabric
fabric export --mode=high-precision --format=openai > training.jsonl
```

**Quality gates before training:**
- Minimum 50 high-value entries required
- At least 30% must be `verified: true`
- Decision-to-note ratio must be > 0.3
- No single session should contribute > 40% of entries (diversity check)

If gates fail, report what's missing and suggest how to accumulate more data.

### Stage 2: Fine-Tune Job

Launch a fine-tuning job on the extracted data:

**Together AI (default):**
```python
import together
job = together.fine_tuning.create(
    model="meta-llama/Meta-Llama-3.1-8B-Instruct",
    training_file="training.jsonl",
    n_epochs=3,
    learning_rate=1e-5,
    suffix="agent-successor-v1"
)
```

**HuggingFace (alternative):**
```bash
hf jobs run train.py \
  --model meta-llama/Meta-Llama-3.1-8B-Instruct \
  --dataset training.jsonl \
  --method sft \
  --hardware gpu.a100
```

**Job tracking:**
- Poll status every 60 seconds
- Log progress (epoch, loss, examples processed)
- Alert on failure with error details

### Stage 3: Head-to-Head Evaluation

Compare the candidate model against the base model:

1. Select 20 high-value fabric entries as evaluation prompts
2. For each prompt, call BOTH models
3. Score responses on 3 dimensions:

| Dimension | Weight | Method |
|-----------|--------|--------|
| Task completion | 0.5 | Response length ratio vs expected |
| Format compliance | 0.3 | Regex pattern matching per entry type |
| Style match | 0.2 | Token frequency cosine similarity |

4. Compute aggregate score for each model
5. Candidate must score within 90% of base model to be considered viable

**Format compliance patterns** (from Icarus):
- Decision entries: must contain "decided", "chose", or "selected"
- Correction entries: must contain "instead" or "should have"
- Review entries: must contain "suggest", "recommend", or "consider"
- Learning entries: must contain "discovered", "learned", or "pattern"

### Stage 4: Model Switch

If candidate passes evaluation:

1. Record current model as fallback in model registry
2. Update model configuration to use candidate
3. Set a probation period (default: 7 days or 20 sessions)
4. Monitor quality metrics during probation

**Rollback triggers:**
- User explicitly requests rollback
- 3 consecutive sessions score below quality threshold
- Principle gate failure rate exceeds 30%
- User override: "rollback model", "모델 롤백"

---

## Model Registry

Track all models (active, candidates, retired):

```yaml
# .cursor/model-registry.yaml
active:
  model: "ft:together/agent-successor-v2"
  switched_at: "2026-04-20T14:00:00Z"
  probation_until: "2026-04-27T14:00:00Z"
  sessions_since_switch: 8
  quality_scores: [0.85, 0.82, 0.88, 0.79, 0.91, 0.84, 0.87, 0.83]

fallback:
  model: "claude-sonnet-4-20250514"
  reason: "original base model"

candidates:
  - model: "ft:together/agent-successor-v1"
    trained_at: "2026-04-15T10:00:00Z"
    eval_score: 0.72
    status: "rejected"  # below 90% threshold
    reason: "Format compliance too low (0.58)"

retired:
  - model: "ft:together/agent-successor-v0"
    retired_at: "2026-04-10T12:00:00Z"
    reason: "Superseded by v1 training data"
```

---

## Safety Model

1. **Never replace for critical tasks**: Model succession only applies to
   well-defined, repetitive workflows — never for architecture decisions,
   security reviews, or production deployments
2. **Human approval required**: Model switch requires explicit user confirmation
3. **Probation period**: New model is monitored for 7 days before considered stable
4. **Instant rollback**: One command to revert to the fallback model
5. **Training data audit**: User can review all training data before fine-tuning

---

## Integration with Other Skills

| Skill | Integration |
|---|---|
| `icarus-memory-fabric` | Source of training data (fabric export) |
| `agent-behavioral-principles` | Principle scores feed quality monitoring |
| `hf-model-trainer` | Alternative training backend (HuggingFace Jobs) |
| `hf-evaluation` | Extended evaluation capabilities |
| `maestro-conductor` | Succession can be a mission milestone |

---

## Commands

| Command | Action |
|---------|--------|
| `succession status` | Show model registry and probation status |
| `succession extract` | Export training data from fabric |
| `succession train` | Launch fine-tuning job |
| `succession eval` | Run head-to-head evaluation |
| `succession switch` | Switch to candidate model (requires approval) |
| `succession rollback` | Revert to fallback model |
| `succession history` | Show all model transitions |

---

## Prerequisites

- `icarus-memory-fabric` must have 50+ high-value entries
- Together AI API key (`TOGETHER_API_KEY`) or HuggingFace token (`HF_TOKEN`)
- Sufficient fabric diversity (multiple sessions, projects, decision types)
