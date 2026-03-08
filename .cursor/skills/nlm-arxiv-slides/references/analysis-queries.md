# Paper Analysis Query Templates

Predefined `notebook_query` templates for analyzing arXiv papers uploaded to NotebookLM. Run these sequentially in Phase 8 and compile responses into the analysis summary document.

## Core Analysis Queries

### Query 1 — Key Contributions

```
What are the 3-5 most important contributions of this paper? For each contribution, explain: (1) what exactly is novel, (2) how it advances the current state of the art, and (3) what practical impact it enables. Distinguish between incremental improvements and fundamental breakthroughs.
```

### Query 2 — Technical Innovations

```
What are the key technical innovations or novel methods introduced in this paper? For each: (1) describe the core mechanism in simple terms, (2) explain why existing approaches were insufficient, and (3) identify the key insight that makes this approach work. Include any important equations or algorithms, simplified to their core intuition.
```

### Query 3 — Limitations & Future Directions

```
What are the main limitations acknowledged or implied by this paper? For each limitation: (1) how does it constrain the applicability of the results, (2) what would need to change to overcome it, and (3) what are the most promising future research directions? Also identify any limitations the authors may have overlooked.
```

## Optional Deep Analysis Queries

Use these when `--skip-analysis` is NOT set and deeper analysis is desired.

### Query 4 — Methodology Assessment

```
Evaluate the experimental methodology: (1) Are the baselines fair and comprehensive? (2) Are the evaluation metrics appropriate for the claims made? (3) Are there potential confounding factors or selection biases? (4) How reproducible is this work based on the information provided?
```

### Query 5 — Broader Impact & Positioning

```
How does this paper position itself within the broader research landscape? (1) What existing paradigm does it challenge or extend? (2) Which research communities would find this most relevant and why? (3) What are the potential real-world applications and ethical considerations? (4) If this paper's claims hold up, what does it change about how we think about this problem?
```

## Analysis Summary Template

Compile query responses into a structured analysis document:

```markdown
# arXiv Paper Analysis: {Paper Title}

**Paper ID:** {arXiv ID}
**Authors:** {authors}
**Date:** {date}
**Analyzed:** {today's date}

## Key Contributions
{Response from Query 1}

## Technical Innovations
{Response from Query 2}

## Limitations & Future Directions
{Response from Query 3}

## Methodology Assessment (Optional)
{Response from Query 4, if run}

## Broader Impact & Positioning (Optional)
{Response from Query 5, if run}

---
*Analysis generated via nlm-arxiv-slides pipeline using NotebookLM.*
```
