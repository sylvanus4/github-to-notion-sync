---
name: skill-composer
description: Converts natural language workflow descriptions into persistent, reusable skill chains. Use when the user wants to define workflows through natural language that compose modular skills (AgentOS-style). Do NOT use for creating individual skills from scratch (use create-skill), running existing workflows (use mission-control), or optimizing existing skills (use skill-optimizer).
metadata:
  author: thaki
  version: "0.1.0"
  category: self-improvement
---

# Skill Composer

## Purpose

Converts natural language workflow descriptions into persistent, reusable skill chains. Based on the AgentOS paper's concept of users defining software through natural language rules that compose modular skills.

## Triggers

- "compose workflow"
- "create workflow from description"
- "natural language workflow"
- "skill composer"
- "chain skills"
- "워크플로우 조합"
- "스킬 체인"
- "자연어 워크플로우"
- "NL workflow definition"

## Instructions

1. **Accept a natural language workflow description** from the user (e.g., "Whenever I finish a code review, commit changes, create a PR, and post to Slack").

2. **Parse the description** to identify:
   - **Trigger condition** (when/whenever/after/before)
   - **Required skills** from the existing skill ecosystem (match by description)
   - **Input/output data flow** between skills
   - **Error handling requirements**

3. **Validate** that all referenced skills exist in `.cursor/skills/`. If any skill is missing, report the gap and suggest alternatives or a manual skill creation path.

4. **Generate a workflow definition** as a new SKILL.md that:
   - Uses `workflow-sequential` or `workflow-parallel` patterns (see `references/composition-patterns.md`)
   - Specifies skill dependencies and execution order
   - Defines input/output contracts between skills
   - Includes error recovery and rollback instructions

5. **Optionally create** the corresponding `.cursor/commands/*.md` trigger command if the workflow should be invokable via a slash command.

6. **Report the composition** to the user:
   - Skills used (with paths)
   - Execution flow (mermaid or ordered list)
   - Estimated runtime (based on typical skill execution times)

## Do NOT Use For

- Creating individual skills from scratch → use `create-skill`
- Running existing workflows → use `mission-control`
- Optimizing existing skills → use `skill-optimizer`
