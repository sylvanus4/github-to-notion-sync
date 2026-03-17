# AutoResearchClaw — 23-Stage Pipeline Reference

## Phase A: Research Scoping (Stages 1-2)

### Stage 1: TOPIC_INIT

- **Purpose**: Parse the research topic, identify the field, and generate initial research questions
- **Input**: `config.research.topic`, `config.research.domains`
- **Output**: `stage-01/topic_analysis.json` — parsed topic, field classification, initial questions
- **Gate**: None

### Stage 2: PROBLEM_DECOMPOSE

- **Purpose**: Decompose the research problem into sub-problems and identify key variables
- **Input**: Stage 1 topic analysis
- **Output**: `stage-02/problem_tree.json` — hierarchical problem decomposition
- **Gate**: None

## Phase B: Literature Discovery (Stages 3-6)

### Stage 3: SEARCH_STRATEGY

- **Purpose**: Generate search queries for OpenAlex, Semantic Scholar, and arXiv
- **Input**: Problem tree from Stage 2
- **Output**: `stage-03/search_plan.json` — queries, source priorities, dedup rules
- **Gate**: None

### Stage 4: LITERATURE_COLLECT

- **Purpose**: Execute search queries across all configured sources
- **Input**: Search plan from Stage 3
- **Output**: `stage-04/papers/` — downloaded paper metadata and abstracts
- **Sources**: OpenAlex API, Semantic Scholar API, arXiv API
- **Gate**: None
- **Note**: Uses circuit breaker pattern for API failures; query expansion on low results

### Stage 5: LITERATURE_SCREEN (GATE)

- **Purpose**: Screen collected papers for relevance and quality
- **Input**: Collected papers from Stage 4
- **Output**: `stage-05/screened_papers.json` — filtered paper set with relevance scores
- **Gate**: **YES** — Requires approval (auto-approvable with `--auto-approve`)
- **Rollback on rejection**: → Stage 4 (LITERATURE_COLLECT)

### Stage 6: KNOWLEDGE_EXTRACT

- **Purpose**: Extract key findings, methods, and gaps from screened papers
- **Input**: Screened papers from Stage 5
- **Output**: `stage-06/knowledge_base.json` — structured knowledge entries
- **Gate**: None

## Phase C: Knowledge Synthesis (Stages 7-8)

### Stage 7: SYNTHESIS

- **Purpose**: Synthesize extracted knowledge into themes, identify research gaps
- **Input**: Knowledge base from Stage 6
- **Output**: `stage-07/synthesis.json` — themes, gaps, opportunities
- **Gate**: None

### Stage 8: HYPOTHESIS_GEN

- **Purpose**: Generate research hypotheses via multi-agent debate
- **Input**: Synthesis from Stage 7
- **Output**: `stage-08/hypotheses.json` — ranked hypotheses with rationale
- **Gate**: None
- **Note**: Uses multi-agent debate pattern for hypothesis diversity

## Phase D: Experiment Design (Stages 9-11)

### Stage 9: EXPERIMENT_DESIGN (GATE)

- **Purpose**: Design experiments to test generated hypotheses
- **Input**: Hypotheses from Stage 8
- **Output**: `stage-09/experiment_plan.json` — experiment specs, metrics, baselines
- **Gate**: **YES** — Requires approval
- **Rollback on rejection**: → Stage 8 (HYPOTHESIS_GEN)

### Stage 10: CODE_GENERATION

- **Purpose**: Generate executable experiment code using multi-phase CodeAgent
- **Input**: Experiment plan from Stage 9
- **Output**: `stage-10/experiment.py`, `stage-10/requirements.txt`
- **Gate**: None
- **Phases**: Blueprint planning → sequential file gen → AST validation → exec-fix loop → review dialog

### Stage 11: RESOURCE_PLANNING

- **Purpose**: Assess hardware requirements, estimate time/cost
- **Input**: Experiment code from Stage 10, hardware profile
- **Output**: `stage-11/resource_plan.json` — GPU/CPU requirements, estimated runtime
- **Gate**: None

## Phase E: Experiment Execution (Stages 12-13)

### Stage 12: EXPERIMENT_RUN

- **Purpose**: Execute experiments in the configured sandbox environment
- **Input**: Code from Stage 10, resource plan from Stage 11
- **Output**: `stage-12/runs/` — individual run results (JSON per run)
- **Gate**: None
- **Modes**: `simulated` (synthetic), `sandbox` (local subprocess), `docker` (container), `ssh_remote`

### Stage 13: ITERATIVE_REFINE

- **Purpose**: Iteratively refine experiments based on results
- **Input**: Run results from Stage 12
- **Output**: `stage-13/refined_results.json` — aggregated improved results
- **Gate**: None
- **Max iterations**: `config.experiment.max_iterations` (default: 10)

## Phase F: Analysis & Decision (Stages 14-15)

### Stage 14: RESULT_ANALYSIS

- **Purpose**: Analyze experiment results, compute statistics, generate visualizations
- **Input**: Results from Stage 12-13
- **Output**: `stage-14/experiment_summary.json`, `stage-14/results_table.tex`
- **Gate**: None

### Stage 15: RESEARCH_DECISION

- **Purpose**: Decide whether to PROCEED, REFINE, or PIVOT
- **Input**: Analysis from Stage 14, quality metrics
- **Output**: `stage-15/decision.json` — decision with rationale
- **Gate**: None
- **Decisions**:
  - `proceed` → Continue to paper writing (Stage 16)
  - `refine` → Rollback to Stage 13 (keep hypotheses, re-run experiments)
  - `pivot` → Rollback to Stage 8 (discard hypotheses, re-generate)
- **Max pivots**: 2 (prevents infinite loops)

## Phase G: Paper Writing (Stages 16-19)

### Stage 16: PAPER_OUTLINE

- **Purpose**: Generate structured paper outline based on results
- **Input**: Analysis from Stage 14, decision from Stage 15
- **Output**: `stage-16/outline.json` — section hierarchy with planned content
- **Gate**: None

### Stage 17: PAPER_DRAFT

- **Purpose**: Write full paper draft (5,000-6,500 words) with anti-slop detection
- **Input**: Outline from Stage 16, all prior stage outputs
- **Output**: `stage-17/paper_draft.md` — complete paper in Markdown
- **Gate**: None
- **Quality**: Template ratio check (detects AI slop phrases)

### Stage 18: PEER_REVIEW

- **Purpose**: Multi-agent peer review simulating conference reviewers
- **Input**: Paper draft from Stage 17
- **Output**: `stage-18/reviews.md` — structured reviews with scores
- **Gate**: None

### Stage 19: PAPER_REVISION

- **Purpose**: Revise paper based on peer review feedback
- **Input**: Draft from Stage 17, reviews from Stage 18
- **Output**: `stage-19/paper_revised.md` — revised paper
- **Gate**: None

## Phase H: Finalization (Stages 20-23)

### Stage 20: QUALITY_GATE (GATE)

- **Purpose**: Final quality assessment (score 1-10) before export
- **Input**: Revised paper from Stage 19
- **Output**: `stage-20/quality_report.json` — quality score and detailed breakdown
- **Gate**: **YES** — Requires approval
- **Rollback on rejection**: → Stage 16 (PAPER_OUTLINE — full rewrite)

### Stage 21: KNOWLEDGE_ARCHIVE

- **Purpose**: Archive findings to knowledge base for future runs
- **Input**: All pipeline outputs
- **Output**: Knowledge base entries in `config.knowledge_base.root`
- **Gate**: None
- **Non-critical**: Can be skipped on failure without aborting pipeline

### Stage 22: EXPORT_PUBLISH

- **Purpose**: Generate conference-ready LaTeX and package deliverables
- **Input**: Final paper, references, experiment code, charts
- **Output**: `stage-22/paper.tex`, `stage-22/references.bib`, `stage-22/code/`, `stage-22/charts/`
- **Gate**: None
- **Templates**: NeurIPS 2025, ICLR 2026, ICML 2026

### Stage 23: CITATION_VERIFY

- **Purpose**: 4-layer citation verification (arXiv, CrossRef, DataCite, LLM fallback)
- **Input**: Paper and references from Stage 22
- **Output**: `stage-23/verification_report.json`, `stage-23/paper_final_verified.md`
- **Gate**: None (but blocks export if verification fails)
- **Layers**:
  1. arXiv ID lookup
  2. CrossRef DOI verification
  3. DataCite DOI fallback
  4. LLM-based existence check (last resort)

## State Machine

```
PENDING → RUNNING → DONE (→ next stage)
                  → BLOCKED_APPROVAL → APPROVED → DONE
                                     → REJECTED → PENDING (rollback target)
                                     → PAUSED (timeout)
                  → FAILED → RETRYING → RUNNING
                           → PAUSED
```
