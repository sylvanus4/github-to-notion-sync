## SEFO Plan

SEFO-enhanced planning mode: discovers relevant skills via BM25/Hybrid retrieval and generates a dependency-ordered execution DAG before creating the plan.

### Usage

```bash
/sefo-plan <task description>
```

### Examples

```bash
# Daily pipeline planning
/sefo-plan "run daily stock analysis with report generation and Slack distribution"

# Release preparation
/sefo-plan "prepare release with code review, security scan, and changelog"

# Research pipeline
/sefo-plan "deep research on market trends, create presentation, and publish to Notion"

# Morning routine
/sefo-plan "morning pipeline: email triage, calendar briefing, stock analysis, news digest"
```

### What Happens

1. **SEFO Routing**: Runs `python scripts/sefo_plan_router.py` with your task description
2. **Skill Discovery**: BM25/Hybrid retrieval finds the top-k most relevant skills from the corpus
3. **DAG Composition**: Builds a dependency graph from `composable_skills` edges
4. **Phase Generation**: Groups skills into parallel execution phases (topologically ordered)
5. **Plan Creation**: Presents the skill-ordered plan with a Mermaid DAG diagram for your approval

### Options

You can specify options inline:

```bash
# Use BM25-only retrieval
/sefo-plan --method bm25 "create PRD from meeting notes"

# Return more skill candidates
/sefo-plan --top-k 15 "comprehensive code review with multi-domain analysis"

# Force corpus rebuild (after adding/modifying skills)
/sefo-plan --rebuild "design system audit and component tracking"
```

### Output

The command produces a structured plan with:

- **Ranked skill list**: Skills ordered by relevance to your task
- **Execution DAG**: Mermaid diagram showing skill dependencies
- **Phase breakdown**: Which skills run in parallel vs sequentially
- **User confirmation gate**: You approve before any execution begins

### Notes

- SEFO routing is advisory — you can override any skill selection
- The corpus auto-builds on first run; use `--rebuild` after adding new skills
- Falls back to manual skill selection if the router is unavailable
- Complements existing Plan Mode workflows (`plan-mode-review.mdc`, `workflow-planning.mdc`)
