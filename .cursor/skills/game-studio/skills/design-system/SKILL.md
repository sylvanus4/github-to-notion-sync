---
name: game-studio-design-system
description: "Generate a comprehensive Game Design Document (GDD) using the MDA framework. Use when the user asks to 'write GDD', 'design document', 'game-design-system', 'game design doc', '게임 기획서', '게임 디자인 문서', 'GDD 작성'. Do NOT use for initial brainstorming (use game-studio-brainstorm). Do NOT use for implementation breakdown (use game-studio-dev-story). Do NOT use for project scaffolding (use game-studio-start)."
---

# Game Design System — Game Design Document Generator

Generate a comprehensive Game Design Document (GDD) from a game concept, covering mechanics, dynamics, aesthetics, content specification, and technical requirements. Uses the MDA framework as the structural backbone.

Use when the user asks to "write GDD", "design document", "game-design-system", "game design doc", "게임 기획서", or wants to formalize a game concept into a full specification. Do NOT use for initial brainstorming (use brainstorm) or implementation breakdown (use dev-story).

## MDA Framework Structure

### Mechanics (Rules & Systems)
Define every system the player interacts with:
- **Core Loop** — The primary action cycle
- **Win/Loss Conditions** — How the game ends
- **Scoring System** — How performance is measured
- **Progression System** — How difficulty or content advances
- **Input Mechanics** — What actions the player can take
- **State Transitions** — All possible game states and transitions between them

### Dynamics (Emergent Behavior)
Describe the play experience that emerges from mechanics:
- **Decision Space** — Types of choices the player faces
- **Information Asymmetry** — What the player knows vs. doesn't know
- **Risk/Reward** — Trade-offs in player decisions
- **Tension Curve** — How engagement builds through a session
- **Replayability** — What changes between sessions

### Aesthetics (Player Emotion)
Define the target emotional experience:
- **Primary Emotion** — The core feeling (e.g., curiosity, tension, satisfaction)
- **Theme & Tone** — Visual and narrative style
- **Audio Direction** — Sound design intent
- **Feedback Feel** — How actions feel (snappy, smooth, weighty)

## Workflow

### Step 1: Concept Card
Write a structured concept summary:
- Title, tagline, genre, platform
- 1-paragraph elevator pitch
- Target audience
- Session length and frequency

### Step 2: Mechanics Specification
For each mechanic, define:
- **Name** and **description**
- **Rules** (precise, unambiguous)
- **Parameters** (tunable values with defaults)
- **Edge cases** (what happens in unusual states)

### Step 3: Content Specification
Define all content types:
- Characters/entities and their attributes
- Levels/puzzles and their structure
- Clue/hint systems and their rules
- Difficulty progression curve

### Step 4: UI/UX Specification
- Screen-by-screen wireframe descriptions
- Interaction patterns (tap, swipe, hover)
- Animation requirements
- Accessibility requirements (WCAG AA)

### Step 5: Technical Requirements
- Performance targets (load time, frame rate)
- Data persistence strategy (localStorage, server)
- State management architecture
- Sharing/social integration

### Step 6: Validation Criteria
- Minimum solvability guarantee for puzzles
- Fairness metrics (no puzzle requires guessing)
- Difficulty distribution targets
- Accessibility compliance checklist

## Output
A single markdown GDD file containing all sections above, structured as a living document with version markers. Target length: 2000-4000 words.
