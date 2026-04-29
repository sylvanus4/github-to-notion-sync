---
name: feynman-peer-review
description: "Simulate a tough but constructive AI research peer review with severity-graded weaknesses, inline annotations, and a concrete revision plan. Use when the user asks to 'review a paper', 'peer review', 'critique this paper', 'simulate reviewer feedback', 'find weaknesses', 'submission review', '논문 리뷰', '피어 리뷰', '논문 비평', '약점 분석', '학회 리뷰 시뮬레이션', 'feynman-peer-review', '/review', 'review before submission'. Do NOT use for paper-code consistency checks (use feynman-paper-audit). Do NOT use for deep paper analysis with structured Korean review + peer review (use paper-review). Do NOT use for paper analysis + PM/business perspectives + distribution pipeline (use paper-review-pipeline). Do NOT use for comparing multiple papers (use feynman-source-comparison). Do NOT use for paper summarization only (use alphaxiv-paper-lookup)."
---

# Simulated Peer Review

Produce a venue-quality peer review of an AI research artifact with structured feedback, severity grading, inline annotations quoting specific passages, and a prioritized revision plan.

## Prerequisites

- The user provides a paper (arXiv URL/ID, PDF path, markdown draft, or Notion page).
- Determine the target venue if known (NeurIPS, ICML, ACL, CVPR, etc.) to calibrate review standards.

## Workflow

### Phase 1: Plan

1. Derive a short slug from the artifact name.
2. Outline the review scope:
   - What will be reviewed (full paper, specific sections, or draft)
   - Review criteria: novelty, empirical rigor, baselines, reproducibility, clarity, significance
   - Verification checks needed for claims, figures, and reported metrics
   - Target venue standards (if applicable)
3. Present the plan to the user and **wait for confirmation**.

### Phase 2: Evidence Gathering (Subagent)

For non-trivial artifacts, spawn a `generalPurpose` subagent:

```
You are a research evidence agent. Your task:

1. Read the paper/artifact thoroughly
2. For each major claim, search for:
   - Cited works — do they actually support the claim?
   - Missing baselines — what should have been compared?
   - Related work gaps — what important papers are missing?
   - Benchmark contamination risks
   - Statistical significance of reported results
3. Build an evidence file at `outputs/feynman/<slug>-review-evidence.md` with:
   - Evidence table (source, claim, verification status)
   - List of missing references
   - Baseline comparison gaps
4. Return a one-line summary.

Skip this phase for short drafts or early-stage work where evidence gathering is overkill.
```

### Phase 3: Review Generation (Subagent)

Spawn a `generalPurpose` subagent (or use the same context for simple artifacts):

```
You are a skeptical but fair AI research peer reviewer.

Read the artifact and evidence file (if available). Produce a review with TWO parts:

## Part 1: Structured Review

### Summary
1-2 paragraph summary of contributions and approach.

### Strengths
- [S1] Specific strength with evidence...
- [S2] ...

### Weaknesses
- [W1] **FATAL:** Issue that would block acceptance. Cite specific section/passage.
- [W2] **MAJOR:** Significant concern requiring revision. Cite specific section/passage.
- [W3] **MINOR:** Polish issue or suggestion. Cite specific section/passage.

### Questions for Authors
- [Q1] Specific question tied to a claim or method choice...

### Verdict
Overall assessment, confidence score (1-5), and venue-calibrated recommendation:
- Strong Accept / Accept / Weak Accept / Borderline / Weak Reject / Reject

### Revision Plan
Prioritized, concrete steps to address each weakness, ordered by severity.

## Part 2: Inline Annotations

Quote specific passages and annotate them:

> "We achieve state-of-the-art results on all benchmarks"
**[W1] FATAL:** Table 3 shows the method underperforms on 2 of 5 benchmarks.

> "Our approach is novel in combining X with Y"
**[W3] MINOR:** Z et al. (2024) combined X with Y. Clarify the distinction.

Rules:
- Every weakness MUST reference a specific passage or section
- Keep looking after the first major problem — do not stop at one issue
- Distinguish fatal/major/minor clearly
- Preserve uncertainty — if it might pass depending on venue norms, say so
- Do not praise vaguely — tie positives to specific evidence
- Challenge "verified" or "confirmed" statements that lack the actual check
- Check for notation drift, inconsistent terminology, conclusions stronger than evidence

Save to `outputs/feynman/<slug>-review.md`
```

### Phase 4: Verification Pass (Optional)

If Phase 3 found FATAL issues:
1. Inform the user of the critical findings
2. If the user provides fixes, run one more verification-style review pass
3. Save the updated review

### Phase 5: Delivery

1. Present the structured review summary to the user
2. Highlight top 3 most impactful findings
3. End with a `Sources` section for any additionally inspected external sources

## Output Structure

```
outputs/feynman/
├── <slug>-review-evidence.md  # Phase 2 evidence (if gathered)
└── <slug>-review.md           # Phase 3 final review
```

## Severity Classification Guide

| Level | Criteria | Impact |
|-------|----------|--------|
| **FATAL** | Incorrect claims, fabricated results, fundamental methodology flaws | Blocks acceptance at any venue |
| **MAJOR** | Missing baselines, insufficient ablations, overclaimed novelty, reproducibility gaps | Requires revision before acceptance |
| **MINOR** | Writing clarity, missing citations, notation inconsistency, cosmetic issues | Should fix but not blocking |

## Verification Before Completion

- [ ] Every weakness cites a specific passage or section
- [ ] Inline annotations quote exact text from the paper
- [ ] Severity levels are consistently applied
- [ ] Revision plan is actionable and prioritized
- [ ] Output files exist at documented paths
