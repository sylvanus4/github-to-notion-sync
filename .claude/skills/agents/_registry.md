# Agent Type Registry

Master index of all 30 agent-type orchestrator skills. Each agent composes 3-8 existing specialist skills into a domain-specific workflow.

## Tier A: Full Coverage (Thin Wrappers)

| # | Agent | Slug | Primary Domain |
|---|-------|------|---------------|
| 1 | Planning Agent | `planning-agent` | Project planning, task decomposition |
| 2 | Agent Workflow System | `agent-workflow-system` | Multi-agent orchestration |
| 3 | Data Analysis Agent | `data-analysis-agent` | Data exploration, statistics, dashboards |
| 4 | Code Generation Agent | `code-generation-agent` | Automated code from specs/issues |
| 5 | Security Enhancement Agent | `security-enhancement-agent` | Threat modeling, vulnerability scanning |
| 6 | Content Creation Agent | `content-creation-agent` | Multi-platform content production |
| 7 | Financial Advisory Agent | `financial-advisory-agent` | Investment intelligence, trading |
| 8 | Legal Intelligence Agent | `legal-intelligence-agent` | Contract review, patents, compliance |
| 9 | Self-Improvement Agent | `self-improvement-agent` | Skill evolution, prompt optimization |

## Tier B: Partial Coverage (Compose + Augment)

| # | Agent | Slug | Primary Domain |
|---|-------|------|---------------|
| 10 | Autonomous Decision Agent | `autonomous-decision-agent` | Confidence-gated decisions |
| 11 | Memory Augmentation Agent | `memory-augmentation-agent` | Unified memory lifecycle |
| 12 | Knowledge Retrieval Agent | `knowledge-retrieval-agent` | Multi-source RAG search |
| 13 | Document Intelligence Agent | `document-intelligence-agent` | Document parsing, conversion |
| 14 | Scientific Research Agent | `scientific-research-agent` | Literature review, paper analysis |
| 15 | Verification & Validation Agent | `verification-validation-agent` | Multi-domain quality gates |
| 16 | General Problem Solving Agent | `general-problem-solving-agent` | Methodology-routed problem solving |
| 17 | Conversational Agent | `conversational-agent` | Multi-mode dialogue |
| 18 | Scientific Discovery Agent | `scientific-discovery-agent` | Hypothesis-experiment-publish |
| 19 | Education Intelligence Agent | `education-intelligence-agent` | Curriculum, tutoring, assessment |
| 20 | Collective Intelligence Agent | `collective-intelligence-agent` | Swarm consensus, adversarial debate |
| 21 | Tool Usage Agent | `tool-usage-agent` | Tool discovery, MCP routing |
| 22 | Domain Transformation Agent | `domain-transformation-agent` | Cross-domain translation |

## Tier C: New Creation (Substantial New Content)

| # | Agent | Slug | Primary Domain |
|---|-------|------|---------------|
| 23 | Recommendation Agent | `recommendation-agent` | Scored alternative comparison |
| 24 | Vision Language Agent | `vision-language-agent` | Image analysis, visual QA |
| 25 | Audio Processing Agent | `audio-processing-agent` | Transcription, video production |
| 26 | Physical World Sensing Agent | `physical-world-sensing-agent` | Real-world data, inventory |
| 27 | Ethical Reasoning Agent | `ethical-reasoning-agent` | Multi-framework ethical analysis |
| 28 | Explainable Agent | `explainable-agent` | Reasoning transparency, visual explanation |
| 29 | Healthcare Intelligence Agent | `healthcare-intelligence-agent` | Clinical research, biomedical data |
| 30 | Embodied Intelligence Agent | `embodied-intelligence-agent` | Environment perception-action loops |

## Usage

Invoke any agent via its slug in natural language or Korean triggers documented in each SKILL.md.

```
"planning agent" / "계획 에이전트" -> planning-agent
"run security audit" / "보안 감사" -> security-enhancement-agent
```

All agents are accessible via Jarvis meta-orchestrator Tier 5 routing.
