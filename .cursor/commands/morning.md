## Morning Routine

Run the full morning routine: Google Daily (calendar, Gmail, Drive, Slack) then Today (stock data sync, screening, analysis, report). Posts a consolidated briefing to Slack.

### Usage

```
/morning                                          # full routine (google-daily + today + briefing)
/morning --skip-today                              # Google Daily only (weekends/holidays)
/morning --skip-google                             # Today pipeline only
/morning --skip-screener --skip-news --skip-docx   # lightweight morning
/morning --dry-run                                 # no Slack posting
```

### Pipeline

1. **Google Daily** — Calendar briefing → Gmail triage → Drive upload → Slack notify → Memory sync
2. **Today** — Data sync → Fundamentals → Hot stock discovery → Screening → Analysis → Report
3. **Morning Briefing** — Consolidated summary to `#효정-할일`

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--skip-google` | Skip Google Daily | enabled |
| `--skip-today` | Skip Today pipeline | enabled |
| `--skip-briefing` | Skip consolidated briefing | enabled |
| `--dry-run` | No Slack posting | Slack enabled |
| `--skip-sync` | Skip data sync (Today) | enabled |
| `--skip-fundamentals` | Skip fundamentals (Today) | enabled |
| `--skip-discover` | Skip hot stock discovery (Today) | enabled |
| `--skip-screener` | Skip screening (Today) | enabled |
| `--skip-news` | Skip market news (Today) | enabled |
| `--skip-sentiment` | Skip sentiment (Today) | enabled |
| `--skip-docx` | Skip .docx report (Today) | enabled |
| `--skip-quality-gate` | Skip quality eval (Today) | enabled |

### Execution

1. Read and follow `.cursor/skills/morning/SKILL.md`
2. Execute Phase 1 (google-daily) then Phase 2 (today) sequentially
3. Post Phase 3 consolidated briefing

MCP tools: `slack_send_message`, `slack_search_channels`.
Shell tools: `gws` CLI, Python scripts, Node.js report generator.

### Examples

Full morning:
```
/morning
```

Weekend (no market):
```
/morning --skip-today
```

Quick check (skip heavy analysis):
```
/morning --skip-google --skip-screener --skip-news --skip-sentiment --skip-docx
```
