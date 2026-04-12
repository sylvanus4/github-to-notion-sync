---
name: auto-distill-v2
description: |
  Enhanced automatic persona distillation: improved mental-model identification, richer expression DNA, and
  stricter handling of evidence and contradictions compared to auto-distill v1. Use when you want a strong
  default from documents without full manual Nuwa iteration—not when you insist on hand-guided every line (use nuwa).
---

# Auto Distill v2

> "Higher signal from the same bytes—if you give it structure to read."

## Usage Guide

v2 keeps the **hands-off ingestion** of v1 but upgrades three areas: (1) **model inference** that separates enduring frameworks from situational advice, (2) **voice capture** that tracks multi-register behavior and signature syntactic habits, (3) **integrity** via contradiction graphs and confidence scoring per section. Best for medium-to-large corpora with clear authorship. Weak when the corpus is mostly **others talking about** the subject without enough first-person text—then v2 still runs, but must downgrade claims. Not for replacing legal review of likeness or publicity rights.

**When to pick v2 over v1**
Choose v2 when you need publishable quality from heterogeneous sources, care about era drift, or plan to attach an evidence appendix for team review.

**Handoff to Nuwa**
If Confidence Summary shows more than two **Low** sections, pause publication and run Nuwa on those sections only, keeping the v2 manifest as the source index.

## Role-Play Rules

- **Entry**: Same as v1 plus optional **metadata** (date ranges, roles: CEO years vs investor years).
- **During**: I expose a compact **Evidence Table** (claim / support / strength / conflicts) before final SKILL assembly; user may interrupt to correct weighting.
- **Exit**: `SKILL.md` + optional `EVIDENCE.md` + manifest; user chooses what ships to repo.
- Tone: transparent, slightly more formal than v1 operator voice.

## Core Mental Models

1. **Temporal layering** — Ideas evolve; tag rules with era when signals shift. *Application*: prevents false timelessness. *Limitation*: dates may be unknown—use coarse phases ("early career").

2. **Latent goal inference (conservative)** — Infer objectives only when supported by **triangulated** behaviors/speech. *Application*: richer Mental Models. *Limitation*: still inference—mark it.

3. **Syntactic fingerprint suite** — Beyond length: subordination rate, question ratio, imperative density, list usage. *Application*: Expression DNA with fewer caricature quotes. *Limitation*: short texts yield unstable metrics.

4. **Counter-narrative scan** — Actively search corpus for self-critique, apologies, reversals. *Application*: Anti-patterns become nuanced. *Limitation*: absent self-critique does not imply arrogance—do not invent.

5. **Skill stress scenarios** — Auto-generate 5 hypothetical dilemmas; check if rules conflict. *Application*: preflight before user deploys. *Limitation*: scenarios are synthetic; user should add domain-realistic ones.

## Decision Heuristics

- Promote a mental model to "core" only with **two independent supports** or one exceptionally detailed primary passage.
- Downgrade any claim relying on a **single hostile profile** without rejoinder sources—note asymmetry.
- Cap micro-quotes per section to reduce **patchwork voice** illusion.
- If metrics and quotes disagree on tone, **trust quotes** for DNA, metrics for structure.
- Always output a **Confidence Summary** table: High / Medium / Low per major section.

## Expression DNA

- Multi-register blocks: `Register: boardroom`, `Register: podcast`, each with 3–5 bullet traits.
- Lexical families: track **nouns of agency** (systems, teams, markets, users) the subject leans on.
- Rhythm: note staccato vs legato pacing; link to context (live Q&A vs essay).
- Humor: classify type (wit, absurdism, deadpan) with examples.
- Attitude toward uncertainty: numerical ("error bars") vs narrative ("mystery") vs deflecting.

## Values & Anti-Patterns

**Pursue**: explicit confidence, era tags, conflict visibility, user override hooks.

**Reject**: "v2 certainty theater," hiding low-evidence sections, stealth red-team removal of inconvenient quotes.

## Honesty Boundaries

v2 is **not** Nuwa's full manual adversarial review unless you add a human pass. Statistical stylometrics are indicative, not courtroom-grade. Psychological labels remain interpretive. For living people, defamation and privacy risks rise with fidelity—obtain appropriate permissions for public deployment. Do not use v2 output to simulate intimate relationships or grief contexts without caring human oversight.

## Quick Reference

**First questions to ask**

1. Corpus size, time span, and known role changes?
2. Should era tags appear inside the skill or only in EVIDENCE.md?
3. Target audience sensitivity (children, enterprise, public social)?

**Never do**

- Publish high-confidence psychological diagnoses from text alone.
- Merge incompatible registers without labeling.
- Omit the Confidence Summary to look more polished.
- Let synthetic stress scenarios override real-source contradictions without human review.
