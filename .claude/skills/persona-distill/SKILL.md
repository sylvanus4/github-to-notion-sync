---
name: persona-distill
description: >-
  Discover, install, and create persona distillation agent skills that extract
  cognitive frameworks, decision heuristics, expression DNA, and interaction
  patterns from public figures, colleagues, mentors, or personal records.
  Provides a curated catalog of 40+ persona skills across 5 categories and the
  Nuwa extraction methodology for distilling new personas.
---

# Persona Distill Skills

Discover, install, and create agent skills that extract cognitive operating systems from people — their mental models, decision heuristics, expression patterns, and value boundaries.

"Persona distillation" extracts expressive style, decision frameworks, and interaction patterns from conversations, works, materials, or digital traces. It is not role-playing or impersonation — it is cognitive architecture extraction.

## Source

Curated catalog from [awesome-persona-distill-skills](https://github.com/xixu-me/awesome-persona-distill-skills) (1,689+ stars) and the [Nuwa](https://github.com/alchaincyf/nuwa-skill) extraction methodology.

## When to Use

- User asks to "think like [person]" or wants a specific person's perspective on a problem
- User wants to discover available persona skills for installation
- User wants to create a new persona distillation skill from a public figure or personal contact
- User asks for cognitive framework or mental model extraction from any source
- User wants to understand the persona distillation methodology

## When NOT to Use

- General code review or debugging (use project-specific review skills)
- Role-playing or impersonation without cognitive framework extraction
- Generic prompt optimization (use prompt-architect)
- Stock/financial analysis using existing analyst perspectives (use role-trading-expert)

## Modes

### Mode 1: Discover — Browse the Catalog

When the user asks to find or browse persona skills.

**Steps:**

1. Read `references/catalog.md` for the full categorized catalog
2. Present relevant entries based on the user's domain or interest
3. Provide installation commands: `npx skills add owner/repo-name`

**Categories available:**
- **Self Distillation & Meta Tools** — Tools for distilling yourself or building distillation frameworks
- **Workplace & Academic** — Boss, colleague, mentor, professor, HR patterns
- **Intimate & Family** — Family memories, relationship patterns, commemorative companions
- **Public Figures & Methodology** — Buffett, Musk, Feynman, Karpathy, Jobs, Munger, Naval, Taleb, and more
- **Spiritual & Specialized** — Domain-specific distillation skills

### Mode 2: Install — Set Up a Persona Skill

When the user wants to install a specific persona skill.

**Steps:**

1. Look up the skill in `references/catalog.md`
2. Provide the installation command:
   ```bash
   npx skills add <owner>/<repo-name>
   ```
3. Verify installation succeeded
4. Show example usage prompts for the installed persona

### Mode 3: Create — Distill a New Persona

When the user wants to create a new persona distillation skill.

**Steps:**

1. Read `references/methodology.md` for the Nuwa extraction framework
2. Identify the target: public figure, personal contact, or self
3. Execute the 4-phase pipeline:
   - **Phase 1: Parallel Research** — 6 concurrent research streams (writings, interviews, social media, critics, decisions, timeline)
   - **Phase 2: Triple Verification** — Each candidate mental model must pass 3 gates: cross-domain appearance (2+ domains), predictive power, exclusivity
   - **Phase 3: Skill Construction** — Assemble 3-7 mental models + 5-10 decision heuristics + expression DNA + anti-patterns + honesty boundaries
   - **Phase 4: Quality Validation** — Test with 3 known answers + 1 novel question (expect appropriate uncertainty)
4. Generate the SKILL.md file following the persona template
5. Install to `.cursor/skills/` and run post-creation checks

### Mode 4: Apply — Use an Installed Persona

When the user wants to invoke a specific persona's perspective on a problem.

**Steps:**

1. Identify which persona skill is installed or requested
2. Activate the persona's cognitive framework:
   - Apply their mental models to the problem
   - Use their decision heuristics
   - Adopt their expression DNA (tone, rhythm, word choice)
   - Respect their anti-patterns (what they would never do)
   - Acknowledge honesty boundaries (what the framework cannot address)
3. Deliver the analysis in the persona's voice with their reasoning framework

## Five Layers of Persona Distillation

Every well-distilled persona captures these five layers:

| Layer | What It Captures | Example |
|-------|-----------------|---------|
| **Expression DNA** | Tone, rhythm, word preferences | Jobs: "insanely great", "one more thing" |
| **Mental Models** | Cognitive frameworks for reasoning | Musk: first-principles, asymptotic limits |
| **Decision Heuristics** | Rules for making judgments | Munger: inversion, multi-disciplinary lattice |
| **Anti-Patterns** | What they refuse to do | Buffett: never invest in what you don't understand |
| **Honesty Boundaries** | What the framework cannot address | All: intuition cannot be distilled; snapshot in time |

## Honesty Boundaries (Always Disclose)

- Distillation captures frameworks, not intuition
- Results are a snapshot at research time, not a living update
- Public expression does not equal private thought
- A skill that does not tell you its limitations is not trustworthy

## Quality Validation Checklist

Before declaring a persona skill complete:

- [ ] 3-7 mental models identified with cross-domain evidence
- [ ] 5-10 decision heuristics with concrete examples
- [ ] Expression DNA captured (tone, rhythm, vocabulary)
- [ ] Anti-patterns documented (what the persona avoids)
- [ ] Honesty boundaries explicitly stated
- [ ] Tested with 3 known answers — direction matches
- [ ] Tested with 1 novel question — shows appropriate uncertainty
- [ ] SKILL.md follows the standard template structure

## References

- `references/catalog.md` — Full categorized catalog of 40+ persona distillation skills
- `references/methodology.md` — Nuwa extraction framework and skill template
