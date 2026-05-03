---
name: skill-recommender
description: >-
  Detect project tech stack from package.json, go.mod, Helm charts,
  Dockerfiles, and config files, then recommend the most relevant local skills
  by keyword and category scoring. Outputs a ranked markdown report. Korean
  triggers: "스킬 추천", "기술 스택 스킬", "프로젝트 스킬 추천", "어떤 스킬이 맞아?", "스택 기반 추천".
  English triggers: "skill recommender", "recommend skills for stack",
  "stack-aware skills", "what skills fit my project", "tech stack skills". Do
  NOT use for interactive skill discovery without stack context (use
  skill-guide). Do NOT use for auditing skill quality (use skill-optimizer).
  Do NOT use for creating new skills (use create-skill). Do NOT use for SEFO
  plan routing (use sefo-plan-router).
---

# Skill Recommender

Detect the project's tech stack and recommend the most relevant installed skills.

## Output Language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

## When to Use

- Starting a new project and wondering which existing skills are relevant
- Onboarding to a codebase and need skill discovery filtered by actual tech stack
- After adding new dependencies and wanting to check if matching skills exist
- When `skill-guide` returns too many generic results and stack-aware filtering is needed

## Procedure

### Step 1: Run the recommender script

```bash
python scripts/skill_recommender.py --top=25
```

Options:
- `--top=N` — show top N recommendations (default: 20)
- `--output=FILE` — write report to a file instead of stdout

### Step 2: Review the detected stack

The report shows:
1. **Detected Tech Stack** — technologies found by scanning project files
2. **Detected Combos** — technology combinations that unlock additional skill relevance
3. **Top N Recommended Skills** — ranked by relevance score with matched technologies

### Step 3: Act on recommendations

For each recommended skill, the user can:
- Invoke it directly if the task matches
- Chain multiple recommended skills for complex workflows
- Identify gaps where no relevant skill exists (candidate for `create-skill`)

## Detection Sources

| Source | Technologies Detected |
|--------|----------------------|
| `package.json` | React, Vite, Tailwind, TanStack Query, Zod, i18next, Recharts, Playwright |
| `go.mod` | Go Fiber, PostgreSQL, Redis, NATS, JWT, Prometheus, Swagger |
| `Dockerfile` / `docker-compose.yml` | Docker |
| `Chart.yaml` / `helm/` | Kubernetes, Helm |
| Directory patterns | ArgoCD, Keycloak, Kueue |
| `requirements.txt` / `pyproject.toml` | Python |
| MCP server config | Notion, Slack |

## Scoring Algorithm

Each skill receives a relevance score based on:
- **Keyword match** (+2 per match): skill name/description matches tech keywords
- **Combo bonus** (+3 per match): skill matches multi-technology combo keywords
- **Category bonus** (+1.5): skill category matches detected tech categories

## Integration with Other Skills

- **skill-guide**: Use `skill-guide` for interactive intent-based discovery; use `skill-recommender` for automated stack-based filtering
- **skill-optimizer**: After identifying relevant skills, audit their quality with `skill-optimizer`
- **setup-doctor**: Verify prerequisites for recommended skills with `setup-doctor`
- **agents-md-generator**: Generate the full skill inventory with `python scripts/agents_md_generator.py`
