---
name: feynman-paper-audit
description: >-
  Compare a paper's claims against its public codebase to identify mismatches,
  omissions, and reproducibility risks. Spawns evidence-gathering and
  verification subagents for rigorous claim-code comparison. Use when the user
  asks to 'audit a paper', 'check code-claim consistency', 'verify
  reproducibility', 'find mismatches between paper and code', 'paper code
  audit', 'claim verification', '논문 코드 감사', '논문-코드 불일치', '재현성 검증', '클레임 검증',
  'feynman-paper-audit', 'code vs paper', '/audit'. Do NOT use for general
  paper review or critique without code comparison (use feynman-peer-review).
  Do NOT use for paper summarization or reading (use alphaxiv-paper-lookup or
  paper-review). Do NOT use for comparing multiple papers against each other
  (use feynman-source-comparison). Do NOT use for experiment replication (use
  feynman-replication).
---

# Paper-Code Audit

Audit a research paper against its public codebase to surface mismatches, missing implementations, ambiguous defaults, and reproducibility risks.

## Prerequisites

- The user must provide a paper identifier (arXiv ID, URL, or title) AND a code repository (GitHub URL or local path).
- If the user provides only a paper, search for its linked repository before proceeding.
- If no public codebase exists, report this finding and suggest feynman-peer-review instead.

## Workflow

### Phase 1: Plan

1. Derive a short slug from the audit target (lowercase, hyphens, ≤5 words).
2. Outline the audit plan in a structured format:
   - Paper identity (title, arXiv ID, venue)
   - Repository URL
   - Claims to check (methods, defaults, metrics, data handling)
   - Scope boundaries (which sections/modules are in scope)
3. Save the plan to `outputs/feynman/<slug>-audit-plan.md`.
4. Present the plan to the user and **wait for confirmation** before proceeding.

### Phase 2: Evidence Gathering (Subagent)

Spawn a `generalPurpose` subagent with these instructions:

```
You are an evidence-gathering research agent. Your task:

1. Read the paper content:
   - Use alphaxiv-paper-lookup or WebFetch to retrieve the paper
   - Extract: claimed methods, hyperparameter defaults, reported metrics, dataset descriptions, training procedures

2. Read the repository code:
   - Clone or browse the repository
   - Extract: actual implementations, default configs, metric computations, data loading/processing code

3. Build a structured evidence table:

| # | Claim (Paper) | Code Location | Match? | Details |
|---|--------------|---------------|--------|---------|
| 1 | "Learning rate 1e-4" | config/defaults.yaml:12 | MATCH | ... |
| 2 | "Adam optimizer" | train.py:45 | MISMATCH | Code uses AdamW |

4. Save findings to `outputs/feynman/<slug>-evidence.md`
5. Return a one-line summary of findings count and severity.

Integrity rules:
- Never fabricate a source or code reference
- Every claim must cite a specific paper section or code file:line
- Distinguish: directly verified, inferred, unresolved
- If code is private/unavailable, report this clearly
```

### Phase 3: Verification (Subagent)

Spawn a second `generalPurpose` subagent:

```
You are a verification agent. Read `outputs/feynman/<slug>-evidence.md` and:

1. Verify every URL resolves (paper, repo, referenced files)
2. Cross-check each MISMATCH entry — confirm the discrepancy is real, not a misread
3. Add inline citations [1], [2] linking claims to specific paper sections
4. Flag dead links, missing files, or ambiguous references
5. Classify each finding:
   - MISMATCH: paper says X, code does Y
   - MISSING: paper describes X, code has no implementation
   - AMBIGUOUS: paper is vague, code could be interpreted either way
   - UNDOCUMENTED: code has feature/behavior not mentioned in paper
6. Save verified results to `outputs/feynman/<slug>-audit.md`
```

### Phase 4: Report Assembly

1. Read the verified audit from `outputs/feynman/<slug>-audit.md`.
2. Present a summary to the user with:
   - Total claims checked
   - Mismatches found (with severity: CRITICAL / MAJOR / MINOR)
   - Missing implementations
   - Ambiguous areas
   - Overall reproducibility risk assessment (HIGH / MEDIUM / LOW)
3. End with a `Sources` section containing paper and repository URLs.

## Output Structure

```
outputs/feynman/
├── <slug>-audit-plan.md    # Phase 1 plan
├── <slug>-evidence.md      # Phase 2 raw evidence
└── <slug>-audit.md         # Phase 3+4 final audit report
```

## Quality Criteria

- Every mismatch must cite both the paper passage AND the code location
- No fabricated code references — if a file path cannot be verified, mark it
- Distinguish between "code differs from paper" vs "code is absent"
- The audit report must be actionable: someone should be able to fix each issue

## Verification Before Completion

Before delivering the final report:
- [ ] All paper claims in scope have been checked against code
- [ ] Every MISMATCH has both paper citation and code location
- [ ] URLs in Sources section resolve
- [ ] Output files exist at the documented paths
- [ ] Summary severity counts match the detailed findings
