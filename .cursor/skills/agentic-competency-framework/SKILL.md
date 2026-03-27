---
name: agentic-competency-framework
description: >-
  Self-assess and develop the 7 core agentic engineering competencies demanded
  by the AI job market ($400K+ roles, 1.6M openings vs 500K qualified).
  Three modes: self-assessment with radar chart, skill-to-competency mapping,
  and personalized development plan. Maps each competency to existing project
  skills for hands-on practice.
  Use when the user asks to "assess agentic competencies", "AI engineer
  competency", "competency self-assessment", "skill competency map",
  "development plan for AI skills", "agentic competency assessment",
  "7 core competencies", "competency radar chart", "agentic engineer skills",
  "에이전틱 역량 진단", "AI 엔지니어 역량", "7대 역량", "역량 자가 진단",
  "스킬 역량 매핑", "AI 역량 개발 계획", "에이전틱 엔지니어 역량 평가".
  Do NOT use for executing individual skills (invoke the skill directly).
  Do NOT use for skill quality auditing (use skill-optimizer).
  Do NOT use for hiring interview question generation (use HR skills).
  Do NOT use for prompt optimization without competency context (use prompt-architect).
metadata:
  author: thaki
  version: "1.2.0"
  category: meta
---

# Agentic Competency Framework

Assess and develop the 7 core competencies that define a high-value agentic engineer. Based on analysis of 1.6M AI job postings where only 500K qualified candidates exist and compensation averages $400K+.

## The 7 Competencies

| # | Competency | Core Question |
|---|------------|---------------|
| 1 | Specification Accuracy | Can you translate intent into unambiguous instructions for AI? |
| 2 | Evaluation & Quality Judgment | Can you tell when AI output is wrong, even when it sounds confident? |
| 3 | Task Decomposition & Delegation | Can you break large projects into agent-sized units and assign them effectively? |
| 4 | Failure Pattern Recognition | Can you diagnose and resolve common AI system failure modes? |
| 5 | Trust & Security Design | Can you decide what authority to give agents and where humans must intervene? |
| 6 | Context Architecture | Can you design data structures and retrieval systems so agents find the right info at the right time? |
| 7 | Cost & Token Economics | Can you calculate whether deploying an agent is worth it and which model mix is cost-optimal? |

## Competency-to-Skill Mapping

Each competency maps to existing project skills as practice resources.

### 1. Specification Accuracy

| Skill | Practice Focus |
|-------|---------------|
| `prompt-architect` | 8 research-backed frameworks (CO-STAR, RISEN, etc.) for structured prompt design |
| `prompt-transformer` | Converting rough prompts into professional-grade instructions |
| `spec-quality-gate` | Verifying specification completeness across 7 dimensions |
| `code-spec-comparator` | Detecting gaps between written specs and actual implementation |

### 2. Evaluation & Quality Judgment

| Skill | Practice Focus |
|-------|---------------|
| `ai-quality-evaluator` | 5-dimension quality gate for AI-generated financial reports |
| `evals-skills` | Building LLM judge prompts, validating evaluators against human labels |
| `doc-quality-gate` | Scoring documents on 7 weighted dimensions with A-D grades |
| `workflow-eval-opt` | Designing evaluator-optimizer loops with measurable quality criteria |

### 3. Task Decomposition & Delegation

| Skill | Practice Focus |
|-------|---------------|
| `mission-control` | Decomposing high-level goals into sub-tasks delegated to specialist skills |
| `plans` | Prompt optimization + skill-based execution plan decomposition |
| `workflow-parallel` | Fan-out independent tasks to parallel subagents with aggregation strategies |
| `workflow-sequential` | Executing dependent task chains with checkpoints and error recovery |
| `role-dispatcher` | Dispatching topics to 12 role-perspective analyzers in parallel batches |

### 4. Failure Pattern Recognition

| Skill | Practice Focus |
|-------|---------------|
| `diagnose` | 3 parallel analysis agents (Root Cause, Error Context, Impact) for bug diagnosis |
| `sp-debugging` | Systematic debugging workflow with hypothesis formation before fixes |
| `incident-to-improvement` | 7-skill pipeline from incident triage to lasting prevention |
| `codebase-archaeologist` | Git history analysis for ownership maps, churn hotspots, bus factor |

### 5. Trust & Security Design

| Skill | Practice Focus |
|-------|---------------|
| `security-expert` | STRIDE threat modeling, OWASP Top 10, secret detection |
| `semantic-guard` | Runtime prompt injection detection, PII scanning, data flow validation |
| `safe-mode` | Destructive command interception, directory file locks, guard mode |
| `sefo-governance` | Cryptographic skill signing, trust scores, provenance verification |
| `compliance-gate` | Unified compliance check (SOC2, ISO27001, CIS) with pass/fail per standard |

### 6. Context Architecture

| Skill | Practice Focus |
|-------|---------------|
| `context-engineer` | 3-tier knowledge architecture (working memory → domain → project) |
| `recall` | Cross-session context restoration via BM25/semantic/hybrid search |
| `cognee` | Document-to-knowledge-graph pipeline with semantic RAG search |
| `ecc-iterative-retrieval` | Progressive context building (broad → narrow with successive searches) |
| `ecc-strategic-compact` | Context compaction at logical workflow boundaries |

### 7. Cost & Token Economics

| Skill | Practice Focus |
|-------|---------------|
| `ecc-agentic-engineering` | Cost-aware model routing (Haiku for boilerplate → Sonnet → Opus for architecture) |
| `rtk` | CLI token compression proxy achieving 60-90% reduction |
| `sefo-orchestrator` | Cost-constrained DAG optimization for multi-skill composition |

Related rule: `ecc-token-strategy.mdc` — subagent cost control, MCP server budget, LLM API call routing.

## Workflow

### Mode 1: Self-Assessment

Guided self-assessment producing a scored competency profile.

**Step 1 — Present assessment questionnaire.**

For each of the 7 competencies, ask the user to rate themselves 1-5 using the Assessment Rubric below. Use the `AskQuestion` tool with structured options per competency. Present all 7 questions in a single batch for efficiency.

**Step 2 — Score and analyze.**

- Calculate total score (out of 35)
- Identify top 2 strengths (highest scores) and top 2 gaps (lowest scores)
- Classify overall level: Junior (7-14), Mid (15-21), Senior (22-28), Staff+ (29-35)

**Step 3 — Generate radar chart.**

Use `visual-explainer` to create a self-contained HTML page with:
- Radar chart (7 axes, one per competency) using Chart.js
- Score table with level labels per competency
- Gap analysis section highlighting weakest competencies with specific skill recommendations
- Overall level badge and percentile estimate

Save to `output/competency/assessment-{YYYY-MM-DD}.html` and open in the browser.

### Mode 2: Skill Mapping

Interactive exploration of which project skills develop which competencies.

**Step 1 — Determine focus.**

Ask the user which competency (1-7) they want to explore, or "all" for a full mapping overview.

**Step 2 — Present mapping with practice scenarios.**

For each selected competency:
1. List the mapped skills from the Competency-to-Skill Mapping table above
2. Read each skill's SKILL.md description to confirm current capabilities
3. Present 2-3 concrete practice scenarios from `references/competency-detail.md`
4. Show the level progression table for the competency

**Step 3 — Suggest skill chain.**

Recommend a sequence of skills the user can invoke to practice the competency end-to-end. Example for "Task Decomposition":

```
plans → workflow-parallel → mission-control → role-dispatcher
(design → delegate → orchestrate → multi-perspective)
```

**Step 4 — Save mapping report and suggest next steps.**

Save the mapping exploration as a structured markdown file to `output/competency/skill-map-{YYYY-MM-DD}.md` containing:
- Competencies explored (specific or all 7)
- Mapped skills with practice focus descriptions
- Recommended skill chains
- Practice scenarios presented

End with at least 2 concrete, immediately-executable next steps. Examples:
- "Run `/agentic-competency assess` to baseline your current level"
- "Invoke `prompt-architect` with a vague request to practice Specification Accuracy"
- "Try `workflow-parallel` on two independent code reviews to practice Task Decomposition"

### Mode 3: Development Plan

Generate a personalized weekly learning plan based on assessment results.

**Step 1 — Gather or recall assessment.**

If Mode 1 was already run in this session, use those scores. Otherwise, run a quick 7-question assessment first.

**Step 2 — Generate plan.**

For each competency scoring below 3 (priority gaps):
1. Assign 1-2 recommended skills to practice
2. Define a concrete exercise from `references/competency-detail.md`
3. Set a measurable outcome (e.g., "Run prompt-architect on 3 different prompts and compare framework scores")
4. Estimate time investment in hours

For competencies scoring 3-4 (growth areas):
1. Assign one advanced skill to deepen mastery
2. Define a stretch exercise

For competencies scoring 5 (strengths):
1. Suggest mentoring/teaching opportunities
2. Recommend building a new skill that extends this competency

**Step 3 — Output plan.**

Generate a structured markdown development plan and save to `output/competency/dev-plan-{YYYY-MM-DD}.md`.

## Assessment Rubric

### Level 1 — Awareness (Junior)

| Competency | Indicator |
|------------|-----------|
| Specification Accuracy | Writes vague prompts; AI frequently misinterprets intent |
| Evaluation & Quality | Accepts AI output at face value; misses hallucinations |
| Task Decomposition | Gives entire projects to AI as one prompt; no structuring |
| Failure Patterns | Surprised by AI failures; no mental model of failure modes |
| Trust & Security | Gives AI full access without thinking about guardrails |
| Context Architecture | Dumps all info into one prompt; context window overflow |
| Cost & Token Economics | No awareness of model costs; uses expensive models for everything |

### Level 2 — Practitioner (Mid)

| Competency | Indicator |
|------------|-----------|
| Specification Accuracy | Uses basic prompt structure; includes examples and constraints |
| Evaluation & Quality | Spot-checks AI output; catches obvious errors |
| Task Decomposition | Breaks work into 2-3 steps; manually sequences them |
| Failure Patterns | Recognizes common failures after they happen; basic retry strategies |
| Trust & Security | Understands some risks; applies basic review before executing AI suggestions |
| Context Architecture | Organizes context into sections; uses basic retrieval |
| Cost & Token Economics | Aware of cost differences between models; makes basic tier decisions |

### Level 3 — Competent (Senior)

| Competency | Indicator |
|------------|-----------|
| Specification Accuracy | Uses frameworks (CO-STAR, RISEN); iterates on prompt quality with evals |
| Evaluation & Quality | Builds evaluation rubrics; uses LLM-as-judge patterns with validation |
| Task Decomposition | Designs multi-agent workflows; understands parallel vs sequential tradeoffs |
| Failure Patterns | Predicts failure modes before deployment; builds recovery mechanisms |
| Trust & Security | Designs human-in-the-loop checkpoints; implements guardrails proactively |
| Context Architecture | Designs tiered context systems; optimizes retrieval for relevance |
| Cost & Token Economics | Routes models by task complexity; tracks cost per task; optimizes token usage |

### Level 4 — Expert (Staff)

| Competency | Indicator |
|------------|-----------|
| Specification Accuracy | Designs reusable prompt templates; builds eval-driven prompt optimization loops |
| Evaluation & Quality | Creates automated quality gates; designs evaluator-optimizer pipelines |
| Task Decomposition | Orchestrates complex DAG workflows; implements checkpoint recovery |
| Failure Patterns | Builds systematic failure taxonomies; designs self-healing systems |
| Trust & Security | Architects trust frameworks with cryptographic verification; designs RBAC for agents |
| Context Architecture | Builds knowledge graphs; implements progressive disclosure and compaction strategies |
| Cost & Token Economics | Designs cost-constrained orchestration; builds ROI models for agent deployment |

### Level 5 — Master (Principal+)

| Competency | Indicator |
|------------|-----------|
| Specification Accuracy | Creates meta-frameworks that generate optimal prompts; teaches prompt architecture |
| Evaluation & Quality | Designs organization-wide eval infrastructure; publishes evaluation methodologies |
| Task Decomposition | Designs autonomous loop architectures; builds self-improving orchestration systems |
| Failure Patterns | Discovers novel failure classes; contributes to field knowledge of AI reliability |
| Trust & Security | Designs federated trust systems across organizations; shapes industry security standards |
| Context Architecture | Architects enterprise-scale knowledge systems; designs cross-agent memory protocols |
| Cost & Token Economics | Builds token economy models for entire organizations; optimizes at infrastructure level |

## Examples

### Example 1: Quick self-assessment

**User:** "Assess my agentic competencies"

**Actions:**
1. Present 7-question assessment using AskQuestion tool (single batch)
2. Calculate scores, identify gaps, classify overall level
3. Generate radar chart HTML via visual-explainer
4. Present summary with recommended skills for each gap

### Example 2: Explore a specific competency

**User:** "I want to improve my task decomposition skills"

**Actions:**
1. Present Task Decomposition competency detail and level progression
2. List mapped skills: mission-control, plans, workflow-parallel, workflow-sequential, role-dispatcher
3. Show practice scenarios from references/competency-detail.md
4. Recommend skill chain: plans → workflow-parallel → mission-control

### Example 3: Generate development plan

**User:** "Create an agentic competency development plan"

**Actions:**
1. Run quick 7-question assessment (or reuse existing scores)
2. Identify gaps (score < 3) and strengths (score >= 4)
3. Generate weekly plan with specific skill exercises per gap
4. Save plan to output/competency/dev-plan-{date}.md

## Integration

- **Visual output**: `visual-explainer` for radar charts and competency dashboards
- **Assessment storage**: `output/competency/` directory
- **Skill discovery**: Cross-references `.cursor/skills/*/SKILL.md` descriptions
- **Detailed references**: `references/competency-detail.md` for level criteria and practice scenarios
- **Related skills**: `ecc-agentic-engineering` (engineering methodology), `skill-guide` (skill discovery), `context-engineer` (knowledge architecture)

## Error Handling

| Issue | Resolution |
|-------|-----------|
| User skips assessment questions | Use default score of 2 for skipped items; note in output |
| Referenced skill not installed | Note the missing skill; suggest alternative from same competency |
| output/competency/ directory missing | Create it before writing files |
| Assessment scores all equal | Ask if user wants more granular questions per competency |
