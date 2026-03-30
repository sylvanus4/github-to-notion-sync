---
name: meeting-type-classifier
description: Heuristics for classifying meeting content into types that determine which PM sub-skills to activate.
---

# Meeting Type Classifier

## Table of Contents

- [Classification Rules](#classification-rules) — 5 meeting types with keyword signals
- [Disambiguation Rules](#disambiguation-rules) — Resolving overlapping signals
- [Sentiment Analysis Trigger](#sentiment-analysis-trigger) — When to activate sentiment analysis

---

Classify meeting content into one of five types by scanning for keyword
signals. The first type with 3+ signal matches wins. If no type reaches
the threshold, default to `operational`.

## Classification Rules

### Type: `discovery`

Interview, user research, or product discovery meetings.

**Signal keywords** (case-insensitive, check title + body):
- interview, user research, customer feedback, user testing
- hypothesis, assumption, validate, invalidate
- persona, JTBD, jobs to be done, pain point
- prototype, concept test, usability
- discovery, ideation, brainstorm

**Activated PM skills**:
- `pm-product-discovery/summarize-interview`
- `pm-product-discovery/identify-assumptions-existing`

### Type: `strategy`

Strategy, vision, competitive positioning, or business model meetings.

**Signal keywords**:
- strategy, vision, mission, pivot, roadmap
- competitive, positioning, differentiation, moat
- market, TAM, SAM, pricing, business model
- SWOT, value proposition, investment, VC, pitch
- IRR, unit economics, gross margin, revenue model

**Activated PM skills**:
- `pm-product-strategy/swot-analysis`
- `pm-product-strategy/value-proposition`

### Type: `gtm`

Go-to-market, launch, sales, or marketing meetings.

**Signal keywords**:
- go-to-market, GTM, launch, release
- sales, marketing, channel, distribution
- ICP, ideal customer, beachhead, segment
- pricing tier, freemium, enterprise, SMB
- battlecard, competitive intelligence, demo

**Activated PM skills**:
- `pm-go-to-market/gtm-strategy`
- `pm-go-to-market/ideal-customer-profile`

### Type: `sprint`

Sprint planning, retrospective, or agile ceremony meetings.

**Signal keywords**:
- sprint, backlog, velocity, story point
- retrospective, retro, what went well
- standup, daily sync, blocker
- kanban, scrum, agile, epic, ticket
- deployment, release candidate, QA

**Activated PM skills**:
- `pm-execution/sprint-plan` (for planning meetings)
- `pm-execution/retro` (for retrospective meetings)

### Type: `operational`

General status updates, syncs, or meetings without strong PM signals.

**Signal keywords**: (fallback — no specific keywords needed)

**Activated PM skills**:
- `pm-execution/summarize-meeting` only (core analysis)

## Disambiguation Rules

1. If both `strategy` and `gtm` signals are strong, prefer `strategy`
   (GTM analysis can be surfaced within strategy context)
2. If both `discovery` and `strategy` signals are present, check whether
   the meeting includes user/customer quotes — if yes, prefer `discovery`
3. A `sprint` classification requires at least one of: "sprint", "retro",
   "backlog", "velocity" explicitly present
4. Meetings with fewer than 500 words of content default to `operational`
   regardless of signal matches

## Sentiment Analysis Trigger

Additionally, regardless of meeting type, activate sentiment analysis
(`pm-market-research/sentiment-analysis`) when the content contains:
- 3+ instances of disagreement language: "however", "but I think",
  "on the other hand", "disagree", "concern", "risk", "worried"
- Multiple participants expressing opposing viewpoints on the same topic
- Explicit voting or decision-making with split opinions
