## Evals Skills

Orchestrate LLM product evaluation tasks: audit pipelines, analyze errors, build judges, validate evaluators, and more.

### Usage

```
<sub-skill> [context]
```

### Sub-Skills

| Sub-Skill | Shorthand | What it does |
|-----------|-----------|--------------|
| eval-audit | `audit` | Audit an eval pipeline across 6 diagnostic areas |
| error-analysis | `errors` | Categorize failure modes from LLM traces |
| generate-synthetic-data | `synthetic` | Create diverse test inputs via dimension-based tuples |
| write-judge-prompt | `judge` | Design binary pass/fail LLM-as-Judge evaluators |
| validate-evaluator | `validate` | Calibrate LLM judges against human labels (TPR/TNR) |
| evaluate-rag | `rag` | Evaluate retrieval and generation quality |
| build-review-interface | `review-ui` | Build browser-based trace annotation interface |

### Execution

Read and follow the `evals-skills` skill (`.cursor/skills/evals-skills/SKILL.md`) for the full workflow, sub-skill selection, and error handling.

### Examples

```bash
# Audit existing eval pipeline
/evals-skills audit

# Analyze errors in LLM traces
/evals-skills errors -- categorize failure modes from our support bot traces

# Generate synthetic test data
/evals-skills synthetic -- create test inputs for our RAG pipeline

# Write a judge prompt for tone mismatch
/evals-skills judge -- build a binary pass/fail evaluator for tone

# Validate a judge against human labels
/evals-skills validate -- measure TPR/TNR for our tone judge

# Evaluate RAG pipeline
/evals-skills rag -- measure retrieval quality and generation faithfulness

# Build trace review UI
/evals-skills review-ui -- build an annotation interface for our traces

# Bootstrap from scratch (no evals exist)
/evals-skills audit -- we have no eval infrastructure, help us start
```
