---
description: "Run 199 Deep Research — enterprise-grade autonomous research pipeline producing citation-backed reports with source credibility scoring, multi-provider search, and automated validation"
---

# 199 Deep Research — Citation-Backed Research Reports

## Skill Reference

Read and follow the skill at `.cursor/skills/199-deep-research/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Parse Request

Extract from user arguments:

- **topic** (required): The research topic to investigate
- **mode**: `quick`, `standard` (default), `deep`, `ultradeep` — research depth
- **format**: `md` (default), `html`, `pdf` — output format
- **language**: `en` (default), `ko` — report language (Korean adds translation step)

Mode detection shorthand:
- "간단히", "quick", "overview" → Quick mode
- No modifier or "research" → Standard mode
- "deep", "심층", "comprehensive" → Deep mode
- "exhaustive", "thorough", "철저히" → UltraDeep mode

### Step 2: Read Reference Documents

Read ALL reference documents before starting:

```
.cursor/skills/199-deep-research/references/methodology.md
.cursor/skills/199-deep-research/references/quality-gates.md
.cursor/skills/199-deep-research/references/report-assembly.md
.cursor/skills/199-deep-research/references/html-generation.md
.cursor/skills/199-deep-research/references/continuation.md
```

### Step 3: Create Output Directory

```bash
mkdir -p ~/Documents/"$(echo "$TOPIC" | tr ' ' '_')_Research_$(date +%Y%m%d)"
```

### Step 4: Execute Research Pipeline

Follow the 8-phase pipeline (or subset based on mode) from the SKILL.md:

1. **SCOPE** — Define boundaries, stakeholder perspectives, success criteria
2. **PLAN** — Create search strategy with 10-15 query variations
3. **RETRIEVE** — Execute WebSearch (10+ queries), WebFetch (5-10 sources), spawn parallel subagents
4. **TRIANGULATE** — Validate claims across 3+ independent sources
5. **SYNTHESIZE** — Connect insights, identify patterns
6. **CRITIQUE** — Red team analysis, identify gaps
7. **REFINE** — Fill gaps, strengthen arguments
8. **PACKAGE** — Progressive report assembly

### Step 5: Validate Report

Run validation scripts:

```bash
python .cursor/skills/199-deep-research/scripts/validate_report.py --report "$OUTPUT_DIR/report.md"
python .cursor/skills/199-deep-research/scripts/verify_citations.py --report "$OUTPUT_DIR/report.md"
```

Fix any failures (max 3 retries).

### Step 6: Generate HTML/PDF (if requested)

If `--format html` or `--format pdf`:

```bash
python .cursor/skills/199-deep-research/scripts/md_to_html.py --input "$OUTPUT_DIR/report.md" --output "$OUTPUT_DIR/report.html"
```

For PDF, additionally run WeasyPrint (requires `pip install weasyprint`).

### Step 7: Report Results

1. Report: research mode, phases completed, source count, word count, validation status
2. List output files with full paths
3. Summarize key findings (3-5 bullets)

### Step 8: Offer Distribution (Optional)

Ask if user wants to:
- Upload to Notion (use md-to-notion)
- Post summary to Slack
- Generate presentation slides (use nlm-slides or anthropic-pptx)

## Constraints

- Every factual claim MUST cite a source with [N] notation
- Never fabricate citations — admit gaps instead
- Bibliography must list ALL cited sources individually (no ranges, no "etc.")
- Progressive section assembly: ≤2,000 words per write operation
- For reports >18,000 words, use auto-continuation protocol
