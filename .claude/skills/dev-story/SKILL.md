---
name: game-studio-dev-story
description: >-
  Break a GDD into sprint-ready development stories with acceptance criteria
  and dependency ordering. Use when the user asks to 'break down GDD', 'create
  dev stories', 'game-dev-story', 'sprint plan for game', '게임 스프린트 분해', '개발
  스토리 생성', '게임 태스크 분해'. Do NOT use for initial concept design (use
  game-studio-design-system). Do NOT use for QA planning (use
  game-studio-qa-plan). Do NOT use for brainstorming (use
  game-studio-brainstorm).
---

# Game Dev Story — Feature Decomposition

Break a Game Design Document into sprint-ready development stories with acceptance criteria, dependency ordering, and effort estimates. Produces an implementation backlog that a lead-programmer agent can execute sequentially.

Use when the user asks to "break down GDD", "create dev stories", "game-dev-story", "sprint plan for game", "게임 스프린트 분해", or wants to convert a design document into actionable development tasks. Do NOT use for initial concept design (use design-system) or QA planning (use qa-plan).

## Story Format

Each story follows this template:

```
### [CATEGORY-NUMBER] Story Title
**Priority:** P0 (must-have) | P1 (should-have) | P2 (nice-to-have)
**Effort:** S (< 1hr) | M (1-3hr) | L (3-8hr) | XL (8hr+)
**Dependencies:** [list of story IDs this depends on]

**As a** [player/developer],
**I want** [capability],
**So that** [benefit].

**Acceptance Criteria:**
- [ ] Criterion 1 (testable, specific)
- [ ] Criterion 2
- [ ] Criterion 3

**Technical Notes:**
- Implementation hints
- Key files to create/modify
```

## Story Categories

### ENGINE — Core game logic
- Seed RNG implementation
- Puzzle data structures
- Puzzle generation algorithm
- Clue generation system
- Game state machine
- Validation logic

### UI — User interface components
- Game layout shell
- Suspect grid component
- Clue panel component
- Deduction board component
- Result/share screen
- Stats modal

### DATA — Content and persistence
- Puzzle bank creation (30+ puzzles)
- Suspect pool definition
- localStorage persistence
- Daily puzzle selection

### SOCIAL — Engagement features
- Share card generation
- Stats tracking
- Streak system
- Archive mode

### POLISH — Visual and UX refinement
- Theme/styling application
- Animations and transitions
- Responsive design
- Accessibility compliance

## Workflow

### Step 1: Extract Features from GDD
Read the GDD and list every distinct feature or system.

### Step 2: Decompose into Stories
Break each feature into the smallest independently deliverable unit. Each story should be completable in a single focused session.

### Step 3: Assign Dependencies
Map which stories must complete before others can start. Create a dependency graph.

### Step 4: Prioritize
Assign P0/P1/P2 priorities. P0 stories form the minimum playable game.

### Step 5: Order for Implementation
Produce a linear execution order that respects dependencies and prioritizes P0 stories first.

### Step 6: Estimate Effort
Assign S/M/L/XL effort estimates to each story.

## Output
A structured markdown backlog with:
1. Summary table (ID, title, priority, effort, dependencies)
2. Full story details in execution order
3. Dependency graph (Mermaid)
4. Sprint groupings (Sprint 1 = playable prototype, Sprint 2 = full feature, Sprint 3 = polish)
