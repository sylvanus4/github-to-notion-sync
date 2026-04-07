# Cross-Axis Synergy Detection Rules

Rules for the GM axis Phase 2 synergy detection. Each rule scans outputs from
two or more axes and flags overlapping signals.

## Rule Format

Each rule produces a JSON entry:

```json
{
  "rule_id": "R001",
  "source_axes": [1, 2],
  "type": "company_overlap",
  "confidence": 0.85,
  "summary": "Company X appears in recruitment targets and investment watchlist",
  "action": "Research company deeper — potential employer AND investment"
}
```

## Detection Rules

### R001: Company Overlap (Axis 1 ↔ Axis 2)

**Source**: `outputs/axis/recruitment/{date}/job-pipeline.json` × `outputs/axis/investment/{date}/morning-summary.json`

**Logic**: Extract company names from job pipeline entries. Compare against
investment watchlist tickers and screener results. Match on:
- Exact company name
- Ticker symbol to company name mapping (e.g., NVDA → NVIDIA)
- Korean ↔ English name variants (e.g., 삼성전자 → Samsung Electronics)

**Action**: Flag for deeper research — understanding a company as both an
employer and investment target provides unique insight.

### R002: Topic-Project Alignment (Axis 3 ↔ Axis 5)

**Source**: `outputs/axis/learning/{date}/learning-briefing.md` × `outputs/axis/sidepm/{date}/dev-briefing.md`

**Logic**: Extract topics from learning queue and active papers. Compare against
side project tech stacks and open issues. Match on:
- Technology keywords (e.g., "RAG", "vector search", "fine-tuning")
- Framework names (e.g., "LangChain", "Gradio", "FastAPI")
- Problem domain overlap (e.g., learning about caching while sidepm has a caching issue)

**Action**: Prioritize learning topics that directly apply to active project needs.

### R003: Calendar-Deadline Conflict (Axis 6 ↔ Axis 1/5)

**Source**: `outputs/axis/life/{date}/morning-briefing.md` × `outputs/axis/recruitment/{date}/recruitment-briefing.md` + `outputs/axis/sidepm/{date}/dev-briefing.md`

**Logic**: Extract today's calendar events (meetings, interviews, deadlines).
Cross-reference against:
- Interview schedules from recruitment
- Sprint deadlines and release dates from sidepm
- Application deadlines from recruitment

**Action**: Flag time conflicts. Suggest rescheduling non-critical items.

### R004: News-Investment Signal (Axis 3 ↔ Axis 2)

**Source**: `outputs/axis/learning/{date}/learning-briefing.md` × `outputs/axis/investment/{date}/morning-summary.json`

**Logic**: Papers and research topics may signal investment opportunities:
- A new AI model release (learning) may affect GPU stocks (investment)
- A breakthrough in a specific domain may create sector opportunities
- HF trending models may indicate emerging market segments

**Action**: Flag potential alpha signals discovered through research.

### R005: Interview Prep Boost (Axis 1 ↔ Axis 3)

**Source**: `outputs/axis/recruitment/{date}/recruitment-briefing.md` × `outputs/axis/learning/{date}/learning-queue.json`

**Logic**: If an interview is scheduled within 3 days, scan the learning queue
for topics relevant to the company's tech stack or domain.

**Action**: Auto-prioritize relevant learning topics as "interview prep" items.

### R006: Side Project Demo → Recruitment (Axis 5 ↔ Axis 1)

**Source**: `outputs/axis/sidepm/{date}/dev-briefing.md` × `outputs/axis/recruitment/{date}/job-pipeline.json`

**Logic**: Completed side project features or shipped releases can strengthen
job applications. Scan for recently merged PRs, shipped features, or demo-ready
projects that match job requirements.

**Action**: Suggest updating portfolio or resume with recent accomplishments.

### R007: Email → Multi-Axis Routing (Axis 6 → All)

**Source**: `outputs/axis/life/{date}/email-triage.json`

**Logic**: Emails triaged by Axis 6 may contain items for other axes:
- Job-related emails → Axis 1
- Financial newsletters → Axis 2
- Paper recommendations → Axis 3
- Meeting requests about projects → Axis 5

**Action**: Route extracted items to the appropriate axis's inbox.

### R008: Market Event → Calendar Block (Axis 2 ↔ Axis 6)

**Source**: `outputs/axis/investment/{date}/morning-summary.json` × `outputs/axis/life/{date}/morning-briefing.md`

**Logic**: Major market events (earnings, FOMC, macro data releases) should
be reflected in the calendar for awareness.

**Action**: Suggest calendar event for key market dates.

## Fuzzy Matching Strategy

Company and topic matching uses a 3-tier approach:

1. **Exact match**: Direct string equality (case-insensitive)
2. **Alias match**: Lookup in `outputs/axis/gm/entity-aliases.json` for known
   mappings (e.g., `{ "NVDA": ["NVIDIA", "엔비디아"], "005930.KS": ["삼성전자", "Samsung Electronics"] }`)
3. **Semantic match**: For topics, use keyword overlap scoring (Jaccard similarity
   ≥ 0.3 threshold)

## Entity Alias Registry

Maintain a growing alias file at `outputs/axis/gm/entity-aliases.json`:

```json
{
  "companies": {
    "NVDA": ["NVIDIA", "엔비디아", "Nvidia Corp"],
    "AAPL": ["Apple", "애플"],
    "005930.KS": ["삼성전자", "Samsung Electronics", "Samsung"]
  },
  "topics": {
    "RAG": ["retrieval augmented generation", "검색 증강 생성"],
    "fine-tuning": ["파인튜닝", "미세조정", "finetuning", "SFT", "DPO"]
  }
}
```

This file grows as new aliases are discovered. The GM axis appends new entries
when it encounters unmatched variants that a human later confirms.

## Output: synergies.json

```json
{
  "date": "2026-04-07",
  "synergies_detected": 3,
  "synergies": [
    {
      "rule_id": "R001",
      "source_axes": [1, 2],
      "type": "company_overlap",
      "confidence": 0.92,
      "entities": ["NVIDIA"],
      "summary": "NVIDIA appears in job pipeline (AI Engineer role) and investment watchlist (NVDA buy signal)",
      "action": "Research NVIDIA as employer — insider perspective strengthens investment thesis"
    }
  ]
}
```
