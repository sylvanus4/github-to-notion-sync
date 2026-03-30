# Agentic Competency Detail Reference

Detailed descriptions, level-specific criteria, and practice scenarios for each of the 7 agentic engineering competencies.

---

## 1. Specification Accuracy

### What It Is

The ability to translate human intent into unambiguous, concrete instructions that AI systems execute correctly on the first attempt. This goes beyond "writing good prompts" — it encompasses structured specification design, constraint engineering, and iterative refinement through evaluation.

### Why It Matters

AI systems follow instructions literally. Ambiguous specifications lead to wasted compute, incorrect outputs, and dangerous false confidence. As agents gain more autonomy, specification precision becomes the primary control mechanism — it replaces direct supervision.

### Level Progression

| Level | Behavioral Indicator | Output Quality |
|-------|---------------------|----------------|
| 1 | Free-form natural language requests; no structure | AI misinterprets intent >50% of the time |
| 2 | Includes basic constraints and examples in prompts | Correct output ~60-70% of the time |
| 3 | Uses established frameworks (CO-STAR, RISEN); includes evaluation criteria in the spec itself | Correct output ~85% with predictable failure modes |
| 4 | Designs reusable prompt templates with parameterized slots; runs eval loops to validate specs | Correct output >95%; failures are edge cases with clear recovery |
| 5 | Creates meta-specifications that generate optimal prompts for specific domains; trains others | Systematically achieves near-perfect output quality across domains |

### Practice Scenarios

**Scenario 1 (Beginner):** Take a vague request like "create a stock analysis report" and use `prompt-architect` to restructure it with the CO-STAR framework. Compare the original output vs the restructured output.

**Scenario 2 (Intermediate):** Use `spec-quality-gate` to audit an existing PRD or technical spec document. Identify missing dimensions and rewrite sections to pass all 7 quality checks.

**Scenario 3 (Advanced):** Use `code-spec-comparator` to find gaps between a production feature's spec and its actual implementation. Draft specification amendments that close every gap.

**Scenario 4 (Expert):** Build a prompt template library for a specific domain using `prompt-transformer`. Measure quality improvement across 10+ prompts using before/after scoring.

---

## 2. Evaluation & Quality Judgment

### What It Is

The ability to critically assess AI-generated outputs for correctness, completeness, and reliability — especially when the output appears confident and well-structured but contains subtle errors, hallucinations, or logical inconsistencies.

### Why It Matters

AI systems produce plausible-sounding output even when wrong. Without robust evaluation skills, teams ship hallucinated data, fabricated citations, and logically broken workflows. This competency is the last line of defense between AI output and production impact.

### Level Progression

| Level | Behavioral Indicator | Detection Rate |
|-------|---------------------|----------------|
| 1 | Accepts AI output without verification | Catches <10% of errors |
| 2 | Manually spot-checks obvious claims; basic sanity checks | Catches ~30-40% of errors |
| 3 | Designs evaluation rubrics; uses LLM-as-judge with validation against human labels | Catches ~70-80% of errors |
| 4 | Builds automated quality gates; creates evaluator-optimizer pipelines; measures inter-rater reliability | Catches >90% of errors; false positive rate <5% |
| 5 | Designs organization-wide eval infrastructure; publishes evaluation methodologies; creates novel judge architectures | Systematically prevents error classes through pipeline design |

### Practice Scenarios

**Scenario 1 (Beginner):** Run `ai-quality-evaluator` on a daily stock analysis report. Review each of the 5 quality dimensions (accuracy, hallucination, consistency, coverage, actionability). Identify at least 3 issues the evaluator catches.

**Scenario 2 (Intermediate):** Use `evals-skills` to create a judge prompt for a specific output type (e.g., meeting summaries). Test the judge against 5 human-labeled examples and calculate agreement rate.

**Scenario 3 (Advanced):** Use `workflow-eval-opt` to set up an evaluator-optimizer loop for report generation. Define quality threshold (score >= 8.0), max iterations (3), and stopping criteria. Measure quality improvement across iterations.

**Scenario 4 (Expert):** Use `doc-quality-gate` to score documents across 7 weighted dimensions. Build a dashboard tracking quality scores over time. Identify systemic quality issues and propose pipeline changes.

---

## 3. Task Decomposition & Delegation

### What It Is

The ability to break large, complex projects into units that AI agents can process effectively, then orchestrate their execution through appropriate delegation patterns — knowing when to use parallel execution, sequential chains, or human-in-the-loop checkpoints.

### Why It Matters

AI agents work best on focused, well-scoped tasks. Giving an agent an entire project results in hallucinated architecture, inconsistent decisions, and unrecoverable failures. Decomposition skill determines whether agents amplify your productivity 10x or waste time producing throwaway output.

### Level Progression

| Level | Behavioral Indicator | Project Scope |
|-------|---------------------|--------------|
| 1 | Single monolithic prompt for entire projects | Small scripts and one-off tasks only |
| 2 | Breaks work into 2-3 sequential steps; manual handoff between steps | Simple features with clear boundaries |
| 3 | Designs multi-agent workflows; understands parallel vs sequential tradeoffs; uses subagents | Medium features; can orchestrate 3-5 agents |
| 4 | Implements DAG-based orchestration with checkpoints; handles agent failures and retries | Complex multi-domain projects; orchestrates 10+ agents |
| 5 | Designs self-improving autonomous loops; builds orchestration frameworks used by others | Enterprise-scale programs; designs the orchestration layer itself |

### Practice Scenarios

**Scenario 1 (Beginner):** Take a multi-step task (e.g., "review code, write tests, create PR") and use `plans` to decompose it into a structured execution plan with skill assignments.

**Scenario 2 (Intermediate):** Use `workflow-parallel` to fan out a code review to 3 independent agents (frontend, backend, security) and aggregate their findings. Compare the merged result against a single-agent review.

**Scenario 3 (Advanced):** Use `mission-control` to orchestrate a full feature implementation spanning 5+ skills (spec → code → test → review → PR). Track completion rate and identify bottlenecks.

**Scenario 4 (Expert):** Use `role-dispatcher` to dispatch a strategic topic to 12 role-perspective analyzers in parallel. Evaluate how the executive synthesis captures cross-role consensus and conflicts.

---

## 4. Failure Pattern Recognition

### What It Is

The ability to anticipate, diagnose, and resolve the characteristic failure modes of AI systems — from context window overflow and hallucination cascades to tool misuse, circular reasoning, and silent data corruption.

### Why It Matters

AI systems fail in predictable patterns that differ fundamentally from traditional software failures. Understanding these patterns transforms debugging from hours of confusion into minutes of targeted diagnosis. This competency separates engineers who "get lucky" from those who reliably ship.

### Level Progression

| Level | Behavioral Indicator | Resolution Speed |
|-------|---------------------|-----------------|
| 1 | Surprised by failures; no understanding of AI-specific failure modes | Hours per incident; often unresolved |
| 2 | Recognizes common failures after they happen; applies basic retries | 30-60 minutes per incident |
| 3 | Predicts failure modes before deployment; builds recovery mechanisms | 10-15 minutes; prevents most recurrences |
| 4 | Maintains failure taxonomy; designs self-healing systems; builds monitoring | Minutes; systematic prevention through architecture |
| 5 | Discovers novel failure classes; publishes prevention patterns; contributes to field knowledge | Prevents entire failure classes through system design |

### Common AI Failure Patterns

1. **Hallucination cascade**: One fabricated fact propagates through multi-step reasoning
2. **Context window overflow**: Too much context dilutes critical information
3. **Tool misuse**: Agent calls wrong tool or passes incorrect parameters
4. **Circular reasoning**: Agent cites its own output as evidence
5. **Scope creep**: Agent modifies files outside the intended scope
6. **Silent degradation**: Quality drops gradually without clear error signals
7. **A-B loop**: Fix for A breaks B; fix for B breaks A

### Practice Scenarios

**Scenario 1 (Beginner):** Use `sp-debugging` on a failing test. Follow the systematic debugging workflow (hypothesis → evidence → verify) instead of random changes. Document the failure pattern.

**Scenario 2 (Intermediate):** Use `diagnose` with 3 parallel agents to diagnose a complex bug. Compare the Root Cause, Error Context, and Impact analyses. Note which failure pattern category the bug falls into.

**Scenario 3 (Advanced):** Use `incident-to-improvement` to run the full 7-step pipeline on a production issue. Evaluate whether the resulting prevention measures address the root failure pattern.

**Scenario 4 (Expert):** Use `codebase-archaeologist` to analyze git history for churn hotspots and "bus factor" risks. Correlate high-churn files with past incident frequency. Propose architectural changes that eliminate the failure pattern class.

---

## 5. Trust & Security Design

### What It Is

The ability to design appropriate permission boundaries, human intervention points, and guardrails for AI agents — determining what agents can do autonomously, what requires approval, and what must remain human-only.

### Why It Matters

Over-permissioning creates catastrophic risk (agent deletes production database). Under-permissioning wastes the agent's value (human approval for every file edit). The optimal boundary is task-specific and evolves with trust — designing this boundary correctly is a core engineering judgment.

### Level Progression

| Level | Behavioral Indicator | Risk Management |
|-------|---------------------|----------------|
| 1 | No guardrails; gives agents unrestricted access | High risk; incidents from uncontrolled actions |
| 2 | Basic awareness; manually reviews agent output before applying | Medium risk; catches obvious dangers |
| 3 | Designs human-in-the-loop checkpoints; implements input validation and output scanning | Low risk; systematic approval gates at critical points |
| 4 | Architects trust frameworks with graduated permissions; cryptographic verification of agent identity | Very low risk; defense in depth with audit trails |
| 5 | Designs federated trust systems; contributes to industry security standards for autonomous agents | Minimal risk; shapes the safety standards others follow |

### Practice Scenarios

**Scenario 1 (Beginner):** Use `safe-mode` to enable command interception while debugging a production issue. Review the blocked commands to understand what destructive operations you might have accidentally triggered.

**Scenario 2 (Intermediate):** Use `semantic-guard` to scan a data pipeline for prompt injection patterns, PII exposure, and data flow violations. Design a remediation plan for each finding.

**Scenario 3 (Advanced):** Use `security-expert` to perform STRIDE threat modeling on an agent-powered workflow. Identify the top 3 attack vectors and design mitigation strategies.

**Scenario 4 (Expert):** Use `sefo-governance` to sign skills with Ed25519 keys, verify provenance chains, and set up trust score thresholds. Design a graduated trust model where new skills start with restricted permissions and earn autonomy through verified behavior.

---

## 6. Context Architecture

### What It Is

The ability to design information systems that ensure AI agents can find the right context at the right time — organizing knowledge across session boundaries, building retrieval systems, and managing the finite context window as a scarce resource.

### Why It Matters

An agent's output quality is bounded by its input quality. No amount of model capability compensates for missing context or information overload. Context architecture is the invisible infrastructure that determines whether agents produce insightful analysis or generic responses.

### Level Progression

| Level | Behavioral Indicator | Context Effectiveness |
|-------|---------------------|-----------------------|
| 1 | Dumps everything into one prompt; no organization | Context window overflow; critical info buried |
| 2 | Organizes context into sections; uses basic copy-paste from docs | Adequate for single-turn tasks; fails on complex work |
| 3 | Designs tiered context systems (working → domain → project); uses retrieval tools | Good relevance; handles multi-session work |
| 4 | Builds knowledge graphs; implements progressive disclosure; designs compaction strategies | Excellent relevance even on large projects; efficient token usage |
| 5 | Architects enterprise-scale knowledge systems; designs cross-agent memory protocols | Enables organizational-level AI memory and learning |

### Practice Scenarios

**Scenario 1 (Beginner):** Use `recall` to restore context from a previous session. Evaluate how much information was preserved vs lost. Identify gaps in the memory capture.

**Scenario 2 (Intermediate):** Use `context-engineer` to create a context package for a specific analysis type. Include domain glossary, relevant MEMORY.md entries, and skill references. Measure agent output quality with vs without the package.

**Scenario 3 (Advanced):** Use `cognee` to build a knowledge graph from project documents. Run semantic searches and evaluate retrieval precision. Compare against keyword-based search.

**Scenario 4 (Expert):** Use `ecc-iterative-retrieval` to design a progressive context building strategy for exploring an unfamiliar codebase. Document the search narrowing pattern and the optimal number of refinement steps.

---

## 7. Cost & Token Economics

### What It Is

The ability to calculate the economic value of deploying AI agents for specific tasks, select cost-optimal model combinations, and manage token budgets at project and organizational scale.

### Why It Matters

An unconstrained agent can burn thousands of dollars in minutes on tasks that could be done with a cheaper model or a simple script. Cost awareness transforms AI from an unpredictable expense into a managed resource with clear ROI. Senior roles increasingly require demonstrating that AI investment generates measurable returns.

### Level Progression

| Level | Behavioral Indicator | Cost Efficiency |
|-------|---------------------|----------------|
| 1 | No cost awareness; uses the most expensive model for everything | 10-100x overspend vs optimal |
| 2 | Aware of model tiers; makes basic "expensive vs cheap" decisions | 2-5x overspend |
| 3 | Routes by task complexity (Haiku/Sonnet/Opus); tracks cost per task | ~1.5x optimal; diminishing waste |
| 4 | Designs cost-constrained orchestration; builds ROI models; uses caching and compression | Near-optimal; demonstrates positive ROI |
| 5 | Builds token economy models for entire organizations; optimizes at infrastructure level | Creates cost frameworks used by others |

### Practice Scenarios

**Scenario 1 (Beginner):** Use `rtk` to check current token savings. Run `rtk gain` to see compression analytics. Identify 3 commands that benefit most from token compression.

**Scenario 2 (Intermediate):** Review `ecc-token-strategy.mdc` rule. Apply the model routing table to 5 recent tasks: was the correct tier used? Calculate actual vs optimal cost for each task.

**Scenario 3 (Advanced):** Use `ecc-agentic-engineering` principles to redesign a multi-agent workflow. Replace Opus calls with Sonnet where acceptable; replace Sonnet with Haiku for exploration. Measure quality impact vs cost savings.

**Scenario 4 (Expert):** Use `sefo-orchestrator` to route a complex task through cost-constrained DAG optimization. Compare the cost-optimal skill composition against an unconstrained version. Document the cost-quality Pareto frontier.

---

## Cross-Competency Practice

### Integration Exercise 1: End-to-End Pipeline

Combine competencies 1, 2, 3, and 7 by:
1. Writing a precise specification (C1) for a daily stock analysis
2. Decomposing it into a multi-agent workflow (C3)
3. Building evaluation criteria for each stage (C2)
4. Optimizing model routing for cost efficiency (C7)

Skills: `prompt-architect` → `plans` → `workflow-sequential` → `ai-quality-evaluator` → `ecc-agentic-engineering`

### Integration Exercise 2: Secure Autonomous Loop

Combine competencies 4, 5, and 6 by:
1. Designing a self-healing agent loop (C4)
2. Adding security guardrails and approval gates (C5)
3. Building context architecture for cross-session persistence (C6)

Skills: `incident-to-improvement` → `safe-mode` → `semantic-guard` → `context-engineer` → `recall`

### Integration Exercise 3: Full Assessment Cycle

Run all 7 competencies by:
1. Self-assessing with Mode 1
2. Picking weakest 2 competencies for deep dive with Mode 2
3. Generating a 2-week development plan with Mode 3
4. Executing the plan's first week of exercises
5. Re-assessing to measure improvement
