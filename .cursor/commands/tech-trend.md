## Tech Trend Analyzer

Analyze technology trends, open-source projects, and industry shifts through a structured 6-dimension pipeline with ThakiCloud relevance scoring.

### Usage

```
/tech-trend <URL or paste content>
/tech-trend --deep <URL>                # Force deep-dive analysis
/tech-trend --skip-kb <URL>             # Skip KB ingestion
/tech-trend --skip-slack <URL>          # Skip Slack posting
/tech-trend --with-notion <URL>         # Enable Notion publishing
/tech-trend --with-roles <URL>          # Trigger full 12-role analysis
/tech-trend --deep --with-roles <URL>   # Full analysis + all roles
```

### Flags

| Flag | Effect |
|------|--------|
| `--deep` | Force deep-dive analysis (first-principles + competitive comparison) regardless of relevance score |
| `--skip-kb` | Skip knowledge base ingestion |
| `--skip-slack` | Skip Slack posting |
| `--skip-notion` | Skip Notion publishing (default behavior) |
| `--with-notion` | Enable Notion page publishing |
| `--with-roles` | Trigger full role-dispatcher (12-role perspective) analysis |

### Workflow

1. **Parse input** — Extract URL/content and flags from `$ARGUMENTS`
2. **Content extraction** — Fetch via defuddle/FxTwitter, run web research
3. **Structured analysis** — 6 dimensions: Tech Stack, Market, Competition, Relevance, Risk, Actions
4. **Deep dive** — First-principles and competitive comparison (if score >= 7 or `--deep`)
5. **Distribution** — KB ingest, Slack thread, optional Notion page, decision routing

### Execution

Read and follow `.cursor/skills/research/tech-trend-analyzer/SKILL.md`.

### Examples

Open-source project from tweet:
```
/tech-trend https://x.com/heygurisingh/status/2035674710005187065
```

GitHub project with deep analysis:
```
/tech-trend --deep https://github.com/nicbarker/clay
```

Technology trend article without Slack:
```
/tech-trend --skip-slack https://example.com/webgpu-future-2026
```

Pasted content analysis:
```
/tech-trend WebGPU + React Three Fiber 조합으로 브라우저에서 네이티브 수준 3D 렌더링이 가능해진 사례가 등장했습니다...
```

Full analysis with all roles:
```
/tech-trend --deep --with-roles https://github.com/nicbarker/clay
```
