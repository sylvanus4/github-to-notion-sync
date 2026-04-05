---
description: "Start an adaptive tutoring session — 10 teaching modes, visual companion, live code execution, and interactive exercises for any topic"
---

# Adaptive Tutor — Interactive Learning Session

## Skill Reference

Read and follow the skill at `.cursor/skills/standalone/adaptive-tutor/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Parse Request

Determine from the user input:

- **Topic**: What the learner wants to study (e.g., "Rust ownership", "K8s networking", "React hooks")
- **Mode override**: If the user specifies a mode (e.g., "socratic", "visual", "project"), use it; otherwise auto-select
- **Visual companion**: If the user says "with visuals" or "visual companion", start the companion server

If no topic is provided, ask the learner what they want to learn.

### Step 2: Execute

Follow the SKILL.md instructions to:

1. Assess the learner's current level via 2-3 diagnostic questions
2. Select the optimal teaching mode (or use the override)
3. Begin the teaching session with active tools (code execution, diagrams, exercises)
4. Optionally start the visual companion if requested or beneficial

### Step 3: Continuous Adaptation

Throughout the session:

- Monitor comprehension signals (correct/incorrect answers, question complexity)
- Adjust difficulty and switch modes if needed
- Use the visual companion to push diagrams, quizzes, and walkthroughs when helpful
