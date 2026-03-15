## AutoSkill Extract

Manually extract skill candidates from a specific session transcript or the current session.

### Usage

```bash
/autoskill-extract                          # extract from current session
/autoskill-extract --transcript <uuid>      # extract from specific session
/autoskill-extract --hint "focus area"      # guide extraction focus
```

### What it does

1. Loads the specified transcript (or current session if none specified)
2. Analyzes user messages for reusable patterns, corrections, and workflows
3. Extracts up to 2 skill candidates with confidence >= 0.6
4. Saves candidates to `outputs/autoskill-candidates/`
5. Displays extracted candidates with confidence scores and source turns

### Skill

Read and follow `.cursor/skills/autoskill-extractor/SKILL.md`
