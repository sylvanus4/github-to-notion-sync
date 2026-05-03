---
name: game-studio-brainstorm
description: >-
  Structured game ideation using SDT, Flow State, and Bartle Player Types. Use
  when the user asks to 'brainstorm game ideas', 'ideate game concept',
  'game-brainstorm', '게임 아이디어', '게임 브레인스토밍', '게임 컨셉 구상'. Do NOT use for
  refining an already-chosen concept (use game-studio-design-system). Do NOT
  use for project scaffolding (use game-studio-start). Do NOT use for
  implementation planning (use game-studio-dev-story).
---

# Game Brainstorm — Structured Ideation

Structured ideation process using Self-Determination Theory, Flow State Design, and Bartle Player Types to generate and evaluate game concepts. Produces a ranked list of ideas with feasibility and engagement scores.

Use when the user asks to "brainstorm game ideas", "ideate game concept", "game-brainstorm", "게임 아이디어", or wants structured creative exploration for a new game. Do NOT use for refining an already-chosen concept (use design-system instead).

## Frameworks Applied

### Self-Determination Theory (SDT)
Score each idea on how well it satisfies:
- **Autonomy** — Player has meaningful choices (1-5)
- **Competence** — Skill development and mastery curve (1-5)
- **Relatedness** — Social connection or shared experience (1-5)

### Flow State Design
Evaluate the balance between:
- **Challenge vs. Skill** — Does difficulty scale with player growth?
- **Clear Goals** — Are objectives unambiguous at every moment?
- **Immediate Feedback** — Does the player know the effect of each action?

### Bartle Player Types
Check appeal to each type:
- **Achiever** — Score/streak/collection systems
- **Explorer** — Discovery, hidden mechanics, depth
- **Socializer** — Sharing, competition, collaboration
- **Killer** — Dominance, leaderboard, PvP elements

## Workflow

### Phase 1: Divergent — Generate Ideas (15 min)
1. Research trending game concepts (Reddit r/WebGames, r/gamedev, itch.io)
2. List 8-12 raw ideas without filtering
3. For each idea, write a one-sentence pitch

### Phase 2: Convergent — Score and Filter
For each idea, score across the 3 frameworks:
| Idea | SDT (A/C/R) | Flow | Achiever | Explorer | Socializer | Killer | Feasibility |
Create a scoring table and rank by total weighted score.

### Phase 3: Deep Dive — Top 3
For each top-3 idea, expand:
- **Core Loop** — What does the player do repeatedly?
- **Session Length** — How long is one play session?
- **Retention Hook** — Why does the player come back?
- **Unique Twist** — What makes this different from existing games?
- **Technical Complexity** — Estimated dev effort (S/M/L)

### Phase 4: Recommendation
Present the top-ranked idea with:
- Pitch paragraph (2-3 sentences)
- Core mechanic description
- Engagement prediction per Bartle type
- Risk assessment (what could make this unfun?)

## Output
A structured markdown document with:
1. Full scoring table
2. Top-3 deep dives
3. Final recommendation with rationale
