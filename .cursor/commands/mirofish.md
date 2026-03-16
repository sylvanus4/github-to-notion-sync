---
description: Run MiroFish multi-agent swarm simulation — daily stock mode (auto-seed from today's analysis) or ad-hoc scenarios
argument-hint: "[daily report file or custom scenario description]"
---

## MiroFish Simulation

Run the MiroFish multi-agent swarm intelligence simulation pipeline (~60 min total).

### Usage

`/mirofish [context]`

- **No argument or daily report file**: Daily Stock Mode — auto-generate seed from `outputs/analysis-{date}.json` + `outputs/news-{date}.json`
- **Custom description**: Ad-hoc mode — use the provided scenario as seed

### Daily Stock Mode (Default)

1. Reads today's `analysis-{date}.json` + `news-{date}.json`
2. Synthesizes seed document with 6 standard stakeholder groups
3. Builds knowledge graph (~4 min) → generates 26 agent personas (~10 min)
4. Runs 20-round dual-platform simulation (~35 min)
5. Generates prediction report (~10 min)
6. Saves to `outputs/mirofish-report-{date}.md`

### Sub-Skills

| Shorthand | What it does | Time |
|-----------|-------------|------|
| `graph` | Build GraphRAG knowledge graph | ~4 min |
| `setup` | Generate agent personas | ~10 min |
| `sim` | Run multi-agent simulation | ~35 min |
| `report` | Generate prediction report | ~10 min |
| `chat` | Interview agents or ReportAgent | interactive |

### Execution

Read and follow the `mirofish` skill. Use **Daily Stock Mode** as the primary workflow.

### Examples

```bash
/mirofish -- Run daily stock simulation from today's data
/mirofish @outputs/reports/daily-2026-03-16.docx -- Simulate based on today's daily report
/mirofish -- What if NVIDIA announces a 10:1 stock split? Simulate market reactions.
/mirofish sim -- Rerun simulation with same graph (same-day rerun)
/mirofish report -- Generate report from the latest completed simulation
/mirofish chat -- Ask "BlackRock Fund Manager" about their portfolio allocation
```
