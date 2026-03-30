# Frontmatter Description Patterns

Good and bad examples for the `description` field, derived from Anthropic's official guide.

## Formula

```
[WHAT it does] + [WHEN to use — trigger phrases] + [Do NOT use for — negative triggers]
```

## Good vs Bad Examples

### Too Vague (Bad)

```yaml
description: Helps with projects.
```

Problem: No trigger phrases, no scope — will never trigger automatically.

### Missing Triggers (Bad)

```yaml
description: Creates sophisticated multi-page documentation systems.
```

Problem: Explains WHAT but not WHEN. No user-facing trigger phrases.

### Too Technical (Bad)

```yaml
description: Implements the Project entity model with hierarchical relationships.
```

Problem: Internal implementation detail, not a user-facing task description.

### Good — MCP-Enhanced Skill

```yaml
description: >-
  Analyzes Figma design files and generates developer handoff documentation.
  Use when user uploads .fig files, asks for "design specs", "component
  documentation", or "design-to-code handoff".
  Do NOT use for general image editing, wireframing, or non-Figma design tools.
```

### Good — Workflow Automation Skill

```yaml
description: >-
  End-to-end meeting digest: analyzes Notion meeting pages or transcripts,
  produces Korean summaries and action items, uploads to Notion.
  Use when user says "회의 다이제스트", "meeting digest", "미팅 요약",
  or shares a Notion meeting URL.
  Do NOT use for simple one-line notes without PM-style analysis.
```

### Good — Orchestrator Skill

```yaml
description: >-
  Orchestrate multi-skill planning workflows — digest, research, PRD, quality gate.
  Use when the user invokes /prd-from-meeting or asks for full pipeline from meeting to PRD.
  Do NOT use for single-step tasks one specialist skill can handle alone.
```

## Templates by Skill Type

### Template: MCP-Enhanced Skill

```yaml
description: >-
  [Action verb] [what it does] using [MCP service]. Use when user
  [trigger phrase 1], [trigger phrase 2], or asks for "[keyword]".
  Do NOT use for [exclusion 1], [exclusion 2], or [exclusion 3].
```

### Template: Standalone Workflow Skill

```yaml
description: >-
  [Action verb] [multi-step process description]. Use when the user asks to
  [trigger phrase 1], [trigger phrase 2], or says "[natural language trigger]".
  Do NOT use for [exclusion 1], [exclusion 2], or [exclusion 3].
```

### Template: Orchestrator Skill

```yaml
description: >-
  Orchestrate [scope of coordination] — [decomposition strategy]. Use when the
  user asks for [trigger 1], [trigger 2], or invokes [command triggers].
  Do NOT use for [single-domain exclusion] or [specific exclusions].
```

## Negative Trigger Patterns

Negative triggers prevent over-triggering. Common patterns:

| Skill Type | Negative Trigger Pattern |
|------------|------------------------|
| File processing | "Do NOT use for [other file types]" |
| Service integration | "Do NOT use for [related but different services]" |
| Code automation | "Do NOT use for [simpler variant of the task]" |
| Orchestrator | "Do NOT use for single-domain tasks that one skill handles" |
| Analysis/audit | "Do NOT use for [creation tasks] or [unrelated analysis]" |

## Character Limit

The `description` field must be under 1024 characters. If approaching the limit:
- Prioritize trigger phrases over exhaustive feature lists
- Use concise negative triggers (one sentence)
- Omit implementation details — those belong in the SKILL.md body
