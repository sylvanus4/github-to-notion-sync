---
name: ce-project-development
description: >-
  Methodology for LLM-powered project development — Task-Model Fit recognition,
  manual prototype step, pipeline architecture, file system as state machine,
  structured output design, agent-assisted development, and cost estimation. Use
  when the user asks to "build LLM project", "design AI pipeline", "estimate AI
  costs", "manual prototype before automating", or mentions task-model fit, pipeline
  architecture, structured output, LLM project methodology, or agent-assisted
  development lifecycle. Do NOT use for general project planning (use full-stack-planner
  or sp-writing-plans). Do NOT use for existing pipeline execution (use mission-control
  or today). Do NOT use for prompt optimization (use prompt-architect).
  Korean triggers: "LLM 프로젝트 개발", "파이프라인 아키텍처", "태스크 모델 핏",
  "구조화 출력", "에이전트 개발 방법론".
metadata:
  upstream: "muratcankoylan/Agent-Skills-for-Context-Engineering/skills/project-development"
  author: "Agent Skills for Context Engineering Contributors"
  version: "1.1.0"
  license: MIT
  category: knowledge
---

# LLM Project Development Methodology

Building production LLM systems requires a different development methodology than traditional software. The core difference: you must discover the right architecture empirically rather than designing it entirely upfront.

## Core Concepts

### Task-Model Fit Recognition

Not every task benefits from LLMs. Evaluate fit before committing:

| Signal | Good Fit | Bad Fit |
|--------|----------|---------|
| Determinism needed | Tolerates variation | Must be exact every time |
| Data structure | Unstructured → structured | Already structured |
| Decision complexity | Requires judgment | Rule-based logic suffices |
| Error tolerance | Graceful degradation OK | Zero-error required |
| Scale economics | Cost per call < human cost | Volume makes LLM cost prohibitive |

### The Manual Prototype Step

Before building any automation:
1. **Do the task manually** at least 10 times
2. Document the exact steps, inputs, and outputs
3. Identify where judgment is needed vs. where rules suffice
4. Write down the "obvious" knowledge you use (domain expertise)
5. This becomes your system prompt and evaluation criteria

### Pipeline Architecture

Every LLM project follows: **Acquire → Prepare → Process → Parse → Render**

| Stage | Purpose | Key Decision |
|-------|---------|-------------|
| Acquire | Get raw input | Sources, freshness, format |
| Prepare | Clean and structure | Token budget, chunking strategy |
| Process | LLM inference | Model selection, prompt design |
| Parse | Extract structured output | Schema validation, error handling |
| Render | Deliver to user/system | Format, channel, feedback loop |

### File System as State Machine

Use files as persistent state between pipeline stages:
- Each stage reads from and writes to well-defined file paths
- State is inspectable, debuggable, and replayable
- Failures resume from the last successful stage
- No hidden state in memory or databases

### Structured Output Design

Force LLM outputs into schemas:
- Define JSON schemas for every LLM output
- Validate outputs immediately after generation
- Retry with error context on validation failure
- Log schema violations for prompt improvement

### Agent-Assisted Development

Use AI agents as development accelerators:
1. **Research phase**: Agent searches docs, examples, APIs
2. **Prototype phase**: Agent generates first drafts of code
3. **Refinement phase**: Human reviews, agent iterates
4. **Testing phase**: Agent generates test cases from specs
5. **Documentation phase**: Agent writes docs from implementation

### Cost and Scale Estimation

Before production, estimate:
- **Per-call cost**: Input tokens × price + output tokens × price
- **Daily volume**: Calls per day × per-call cost
- **Monthly budget**: Daily cost × 30 + buffer (2-3×)
- **Scale ceiling**: At what volume does cost exceed value?
- **Optimization headroom**: Can caching, batching, or smaller models reduce cost?

## Examples

### Example 1: Evaluating task-model fit for a summarization feature
Before committing to an LLM-based approach, you run 10 manual summaries to discover the judgment calls involved, quantify error tolerance, and check whether cost per call is lower than the human alternative. This skill provides the fit-evaluation framework.

### Example 2: Evolving from prompt prototype to pipeline
A single-prompt proof-of-concept works but is slow and brittle. This skill guides you through decomposing the monolith into Acquire-Prepare-Process-Parse-Render stages with file-based state between them, making each stage independently debuggable.

## Troubleshooting

1. **Skipping manual prototype**: Building automation before understanding the task leads to wrong architecture.
2. **Monolithic LLM calls**: One huge prompt doing everything. Break into pipeline stages.
3. **Ignoring cost at prototype stage**: A pipeline that costs $50/run won't scale.
4. **No structured output**: Parsing free-text LLM output is fragile.
5. **No evaluation from day one**: Without metrics, you can't tell if changes help or hurt.

## References

- [Case Studies Reference](./references/case-studies.md)
- [Pipeline Patterns Reference](./references/pipeline-patterns.md)
- Related CE skills: ce-evaluation, ce-context-fundamentals, ce-tool-design
