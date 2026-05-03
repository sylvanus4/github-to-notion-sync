---
name: tab-report-generate
description: >-
  Generate a daily Korean .docx stock analysis report via POST
  /reports/generate/daily and list past reports with GET /reports. Use when
  generating daily report, '일일 리포트 생성', 'tab-report-generate', 'generate
  report'. Do NOT use for daily stock signals only (use daily-stock-check),
  stock price sync (use tab-stock-sync), or news fetch only (use
  tab-news-fetch).
---

# tab-report-generate

## Purpose

Generate comprehensive daily stock analysis reports in .docx format combining technical analysis, news sentiment, market environment, and signal data. The report is produced in Korean.

## When to Use

- generate daily report
- 일일 리포트 생성
- tab-report-generate
- produce stock report
- daily analysis document

## When NOT to Use

- Daily stock signals without report — use daily-stock-check
- Stock price sync — use tab-stock-sync
- News fetch only — use tab-news-fetch
- LLM agent pipeline — use tab-llm-agents

## Workflow

1. Run prerequisite data refreshes first:
   - `POST /api/v1/market-breadth/refresh` (tab-market-breadth)
   - `POST /api/v1/news/fetch` (tab-news-fetch)
   - `POST /api/v1/turtle/indicators/daily-refresh` (tab-turtle-refresh)
   - `POST /api/v1/bollinger-bands/daily-refresh` (tab-bollinger-refresh)
2. Call `POST /api/v1/reports/generate/daily` (body: optional date, symbols list, include_sections)
3. Report is generated as .docx and stored
4. List past reports with `GET /api/v1/reports` (params: start_date, end_date, limit)
5. Download specific report with `GET /api/v1/reports/{report_id}/download`

## Endpoints Used

- `POST /api/v1/reports/generate/daily` — generate daily analysis report
- `GET /api/v1/reports` — list past reports
- `GET /api/v1/reports/{report_id}` — report metadata
- `GET /api/v1/reports/{report_id}/download` — download .docx file

## Dependencies

- Requires backend server running on port 4567
- Requires PostgreSQL with recent data from breadth, news, and indicator refreshes
- Requires python-docx for document generation

## Report Structure

See [references/report-template.md](references/report-template.md) for the standard report structure, section order, formatting standards, and data requirements.

## Output

Korean-language daily analysis .docx report with technical analysis, market environment, and signals.
