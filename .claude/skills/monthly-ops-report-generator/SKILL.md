---
name: msp-monthly-ops-report-generator
description: >-
  MSP monthly operations report: aggregate one calendar month of incidents,
  changes, cost trends, security posture, SLA metrics, capacity utilization,
  and patch compliance from cloud APIs and other MSP skill outputs, then
  generate a professional customer-facing DOCX report with executive summary,
  trend analysis, and prioritized recommendations — composing anthropic-docx
  for document rendering and evaluation-engine for section-level quality
  scoring. All operations read-only (Tier 1). Use when the user asks to
  generate monthly ops report, monthly operations report, MSP monthly summary,
  customer monthly report, monthly SLA report, or needs a comprehensive
  monthly operations review document. Do NOT use for real-time incident triage
  (use msp-incident-triage- summarizer), daily operational dashboards,
  cost-only analysis (use msp-cost-anomaly-explainer), single-incident
  post-mortem reports (use incident-to-improvement), or ad-hoc DOCX creation
  without MSP ops data (use anthropic-docx). Korean triggers: 월간 운영 리포트, MSP
  월간 보고서, 운영 월간 요약, SLA 리포트.
disable-model-invocation: true
---

# Monthly Ops Report Generator

## Usage

- Monthly operations review is due for an MSP-managed customer
- Customer stakeholders need a comprehensive monthly health report
- SLA performance reporting is required
- Monthly cost, security, and capacity trends need documentation
- `/msp-monthly-report` with tenant_id and report_month

## Prerequisites

- AWS: CloudWatch, Cost Explorer, Security Hub, SSM, Config enabled
- GCP: Cloud Monitoring, Billing export, SCC, OS Config enabled
- `tenant_id` and at least one `account_id`/`project_id`
- `report_month` in YYYY-MM format
- `customer_name` for report branding

## Workflow

### Step 1 — Data Collection (Parallel Fan-out)

Launch 7 parallel data collection agents:

#### Agent 1 — Incident Data
```
AWS: SSM OpsCenter OpsItems + CloudWatch Alarm history for report_month
GCP: Cloud Monitoring alert history + Error Reporting for report_month
Collect: total incidents, by severity, MTTR per incident, categories
```

#### Agent 2 — Change Management Data
```
AWS: CloudTrail events (filtered: CreateStack, UpdateStack, RunCommand,
     StartAutomationExecution) + SSM Automation execution history
GCP: Audit Logs (Admin Activity) + Deployment Manager operations
Collect: total changes, success/failure counts, emergency changes
```

#### Agent 3 — Cost Data
```
AWS: Cost Explorer GetCostAndUsage (monthly granularity, group by SERVICE)
     + Budgets DescribeBudgets for variance
GCP: Billing export via BigQuery (monthly aggregation by service)
     + Recommender API for savings opportunities
Collect: total spend, by-service breakdown, vs-previous, vs-budget
```

#### Agent 4 — Security Data
```
AWS: Security Hub GetFindings (created/updated in report_month)
     + GuardDuty finding statistics
GCP: Security Command Center ListFindings (report_month filter)
Collect: open/closed findings, critical items, compliance score
```

#### Agent 5 — Capacity Data
```
AWS: Compute Optimizer recommendations + CloudWatch CPU/Memory metrics
GCP: Recommender API + Monitoring CPU/Memory metrics
Collect: avg utilization, rightsizing opportunities, idle count, ASG events
```

#### Agent 6 — Patch Compliance Data
```
AWS: SSM PatchComplianceSummary + Inspector v2 findings
GCP: OS Config PatchDeployment results
Collect: compliance rate, missing critical patches, windows completed
```

#### Agent 7 — SLA Data
```
AWS: CloudWatch Synthetics canary results + Route 53 health checks
GCP: Monitoring Uptime Checks + SLO monitoring
Collect: availability %, downtime minutes, SLA breaches
```

### Step 2 — Data Aggregation

```
Merge all 7 agent outputs
Calculate derived metrics:
  - MTTR (p50, p95) from incident data
  - Change success rate from change data
  - Compliance rate from patch data
  - Overall health score (weighted composite of all sections)
Compute month-over-month trends (if previous_report provided):
  - Incident trend (improved/stable/degraded)
  - Cost delta (% change)
  - Security posture trend
  - Capacity utilization trend
Identify top-N items per category for highlight sections
```

### Step 3 — Executive Summary Generation

```
Compute overall health: GREEN/YELLOW/RED based on:
  GREEN: SLA met, no P1 incidents, cost within budget, no critical security
  YELLOW: Any SLA near-miss, 1+ P1 incidents resolved, cost 5-15% over
  RED: SLA breached, unresolved P1, cost >15% over, critical security open

Generate 5-7 highlight bullets covering:
  - Most impactful incident (if any)
  - Cost trend headline
  - Security posture change
  - Key achievement
  - Top recommendation

Identify top 3 action items for next month
Create trend indicators (↑ improved, → stable, ↓ degraded)
```

### Step 4 — Recommendations Synthesis

```
Aggregate recommendations from:
  - Cost section: savings opportunities from Skill #11/#12
  - Security section: open critical findings
  - Capacity section: rightsizing from Skill #12, idle cleanup from Skill #13
  - Patch section: overdue patches from Skill #16
  - Backup section: compliance gaps from Skill #15

Prioritize by impact and urgency (HIGH/MEDIUM/LOW)
Carry over unresolved items from previous_report
Cap at top 10 actionable items
```

### Step 5 — Report Assembly

```
Apply 9-section report structure:
  1. Executive Summary
  2. Incident Management
  3. Change Management
  4. SLA Performance
  5. Cost Overview
  6. Security Posture
  7. Capacity & Performance
  8. Patch Compliance
  9. Recommendations

Generate narrative text for each section (customer-safe language)
Redact internal infrastructure details (account IDs, IPs, hostnames)
Run evaluation-engine quality check per section (completeness, accuracy)
```

### Step 6 — Document Generation

```
Generate DOCX via anthropic-docx:
  - Professional formatting with tables and section headers
  - Customer name branding
  - Month/year in title
  - Table of contents
  - Executive summary on page 1

Save to: outputs/msp-reports/{tenant_id}/{report_month}-ops-report.docx

If output_format includes 'notion':
  Publish via md-to-notion to configured Notion workspace
```

## Output Schema

```json
{
  "schema_version": "1.0.0",
  "skill": "monthly-ops-report-generator",
  "report_month": "YYYY-MM",
  "report_file": "outputs/msp-reports/{tenant_id}/{report_month}-ops-report.docx",
  "report_sections": {
    "executive_summary": {"overall_health": "", "highlights": [], "action_items": []},
    "incident_summary": {"total_incidents": 0, "by_severity": {}, "mttr_minutes": {}},
    "change_management": {"total_changes": 0, "change_success_rate": 0.0},
    "sla_performance": {"availability": 0.0, "target": 0.0, "met": true},
    "cost_overview": {"total_spend": 0.0, "vs_previous_month": 0.0},
    "security_posture": {"findings_open": 0, "compliance_score": 0.0},
    "capacity_utilization": {"compute_avg_utilization": 0.0},
    "patch_compliance": {"compliance_rate": 0.0},
    "recommendations": []
  },
  "audit_entry": {"skill_version": "1.0.0", "tier": 1, "mutations": []}
}
```

## Governance

**Tier 1 — Read-only report generation.** No infrastructure changes.

Customer-safe content only — automated redaction of internal details.

## Error Handling

| Error | Recovery |
|-------|----------|
| Cloud API unavailable for data source | Mark section as "partial data — {source} unavailable"; proceed |
| No data for a section (e.g., zero incidents) | Include section with "No incidents recorded this month" |
| Previous report not provided | Skip trend comparison; note "baseline month" |
| Report generation exceeds timeout | Return partial report with sections completed so far |
| Cost data delayed (billing lag) | Note "cost data may be incomplete for last 2-3 days of month" |

## Subagent Contract

When invoked via `Task`:
- Caller provides: `tenant_id`, `account_ids`/`project_ids`, `report_month`, `customer_name`
- Optional: `sla_targets`, `previous_report`, `output_format`, `include_sections`
- Returns: Full JSON output with `report_file` path and structured `report_sections`
