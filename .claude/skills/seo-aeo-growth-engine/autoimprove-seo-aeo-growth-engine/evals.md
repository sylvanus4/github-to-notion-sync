# Eval Suite (synthetic, generated from SKILL.md)

Total: 6 evals · 5 runs each · max score = 30
Train: 4 evals (E1-E4) · max 20
Holdout: 2 evals (E5-E6) · max 10

---

## Train

### EVAL 1: Pillar coverage
**Question:** Does the skill provide a copy-pasteable prompt template for each of the 4 pillars (Content / AEO / Audit / CWV)?
**Pass:** Each pillar contains at least one fenced code block with a Claude prompt the user can paste verbatim.
**Fail:** Any pillar lacks a prompt template, or templates are missing concrete instructions.

### EVAL 2: Concrete thresholds
**Question:** Does every pillar prompt include measurable numeric thresholds (impressions, position, CTR delta, LCP ms, byte size)?
**Pass:** Every pillar includes ≥ 2 numeric thresholds the LLM can act on without further interpretation.
**Fail:** Any pillar uses vague qualifiers ("high impressions", "slow LCP") without numbers.

### EVAL 3: Reproducible inputs
**Question:** Does each pillar specify exact input file formats (CSV column names, JSON shape, tool flags)?
**Pass:** All 4 pillars name the file format AND list expected columns/keys.
**Fail:** Any pillar leaves input ambiguous ("provide GSC data") without naming columns/keys.

### EVAL 4: Anti-pattern → pillar mapping
**Question:** Are anti-patterns explicitly mapped to the pillar they apply to, with at least one anti-pattern per pillar?
**Pass:** Anti-pattern section groups items by pillar and covers all 4 pillars.
**Fail:** Anti-pattern section is a flat list, OR any pillar has zero anti-patterns.

## Holdout

### EVAL 5: Trigger preservation
**Question:** Do all triggers from the frontmatter `description` (GSC analysis, AEO setup, llms.txt, FAQ schema, LCP optimization, weekly audit) appear in the body with concrete guidance?
**Pass:** Each trigger keyword resolves to a body section with ≥ 1 actionable instruction.
**Fail:** Any trigger keyword is named in description but absent or shallow in the body.

### EVAL 6: Cadence + kill switch
**Question:** Does the skill specify both a delivery cadence (weekly / monthly / per-article) AND quantitative stop conditions for the sprint?
**Pass:** Both are present with concrete dates/numbers.
**Fail:** Either missing or fuzzy ("after a while", "if not working").
