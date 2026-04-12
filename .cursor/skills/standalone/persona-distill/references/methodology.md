# Persona Distillation Methodology

> Based on the [Nuwa](https://github.com/alchaincyf/nuwa-skill) extraction framework

## What Is Persona Distillation?

Persona distillation extracts a person's **cognitive operating system** — not a character sheet, not a role-play prompt. It produces a reusable Agent Skill that thinks the way the target person thinks.

### What Gets Distilled (5 Layers)

| Layer | What It Captures | Verification Method |
|-------|-----------------|-------------------|
| **Expression DNA** | Tone, rhythm, word preferences, rhetorical patterns | Cross-reference 10+ texts for recurring stylistic markers |
| **Mental Models** | Cognitive frameworks used for reasoning | Must appear in 2+ domains to qualify |
| **Decision Heuristics** | Rules and shortcuts for making judgments | Must have concrete historical examples |
| **Anti-Patterns** | What the person refuses to do, value boundaries | Must be explicit or inferable from repeated behavior |
| **Honesty Boundaries** | What the framework cannot address | Must be stated in the final skill |

### What Does NOT Get Distilled

- Private thoughts or feelings (only public expression is accessible)
- Real-time adaptation (skills are snapshots, not living updates)
- Intuition (only articulable frameworks transfer)
- Physical presence or charisma

---

## The 4-Phase Pipeline

### Phase 1: Parallel Research (6 Concurrent Streams)

Launch 6 research streams simultaneously:

| Stream | Source Type | What to Extract |
|--------|-----------|-----------------|
| **Writings** | Books, articles, blog posts, essays | Core arguments, recurring themes, vocabulary |
| **Interviews** | Video, podcast, text interviews | Spontaneous reasoning, off-script moments |
| **Social Media** | Twitter/X, LinkedIn, public posts | Unfiltered opinions, real-time reactions |
| **Critics** | Reviews, analyses, biographies | Blind spots, contradictions, evolution over time |
| **Decisions** | Business moves, career choices, public stances | Revealed preferences vs stated preferences |
| **Timeline** | Chronological evolution | How thinking changed; what caused shifts |

**For personal contacts** (not public figures), replace public sources with:
- Private conversations, messages, emails
- Shared experiences and decisions
- Observations from close interactions
- Stories they tell repeatedly

### Phase 2: Triple Verification

Every candidate mental model or heuristic must pass 3 gates:

| Gate | Criterion | Failure Mode |
|------|----------|-------------|
| **Cross-Domain** | Appears in 2+ different contexts | Single-instance patterns are anecdotes, not models |
| **Predictive Power** | Can predict the person's response to a new situation | Descriptions without predictive value are summaries |
| **Exclusivity** | Distinguishes this person from generic advice | Generic wisdom ("work hard") is noise |

**Discard** anything that fails any gate. Better to have 3 verified models than 10 unverified ones.

### Phase 3: Skill Construction

Assemble the verified components into a structured SKILL.md:

```markdown
---
name: [person]-perspective
description: >-
  Cognitive framework distilled from [Person Name]'s publicly available
  writings, interviews, and decisions. Provides their mental models,
  decision heuristics, and expression patterns for analyzing problems
  from their perspective.
triggers:
  - think like [person]
  - [person]'s perspective
  - what would [person] do
  - [person] analysis
tags:
  - persona
  - [domain]
  - cognitive-framework
version: "1.0.0"
---

# [Person Name] — Cognitive Framework

## Mental Models (3-7)

### Model 1: [Name]
- **Definition**: One sentence
- **Application**: When and how to apply
- **Evidence**: 2+ examples from different domains
- **Counter-indication**: When this model fails

[Repeat for each model]

## Decision Heuristics (5-10)

### Heuristic 1: [Name]
- **Rule**: The decision shortcut
- **Example**: Concrete historical case
- **Boundary**: When not to apply

[Repeat for each heuristic]

## Expression DNA

- **Tone**: [e.g., direct, contrarian, Socratic]
- **Rhythm**: [e.g., short punchy sentences, long dialectical chains]
- **Vocabulary**: [signature phrases and word choices]
- **Rhetoric**: [preferred argument structures]

## Anti-Patterns

What [Person] would never do:
1. [Behavior] — because [reasoning]
2. [Behavior] — because [reasoning]

## Honesty Boundaries

This skill cannot:
- [Limitation 1]
- [Limitation 2]
- Replicate intuition, only articulable frameworks
- Guarantee accuracy beyond the research snapshot date
```

### Phase 4: Quality Validation

Run 4 tests before declaring the skill complete:

| Test | Method | Pass Criteria |
|------|--------|--------------|
| **Known Answer 1** | Ask about a topic the person has publicly addressed | Direction and reasoning align |
| **Known Answer 2** | Ask about a different domain the person has addressed | Consistent framework application |
| **Known Answer 3** | Ask about a controversial stance the person has taken | Captures nuance, not just headline position |
| **Novel Question** | Ask about a topic the person has NOT addressed publicly | Shows appropriate uncertainty; applies frameworks without fabricating positions |

**Failure at any test** means return to Phase 2 and re-verify the models.

---

## Tips for High-Quality Distillation

### Do

- Focus on **frameworks over facts** — you want how they think, not what they know
- Look for **repeated patterns** across different time periods and contexts
- Capture **anti-patterns** — what someone avoids is as revealing as what they do
- Test with **adversarial scenarios** — does the framework produce non-obvious but consistent responses?
- State **honesty boundaries** explicitly — a skill that claims no limitations is not trustworthy

### Do Not

- Confuse **famous quotes with mental models** — "Move fast and break things" is a slogan, not a decision framework
- Include **generic advice** that anyone might give — every heuristic must pass the exclusivity gate
- Role-play or impersonate — the goal is cognitive architecture, not character acting
- Fabricate positions on topics the person never addressed
- Skip the quality validation phase

---

## Composition with Project Skills

Persona distillation skills compose well with existing project skills:

| Combination | Use Case |
|------------|----------|
| persona + `first-principles-analysis` | Apply the persona's reasoning to decompose a problem |
| persona + `sun-tzu-analyzer` | Overlay strategic thinking with persona-specific judgment |
| persona + `role-dispatcher` | Add the persona as a virtual role in multi-role analysis |
| persona + `presentation-strategist` | Present findings in the persona's communication style |
| persona + `prompt-architect` | Use persona frameworks to structure prompts |
