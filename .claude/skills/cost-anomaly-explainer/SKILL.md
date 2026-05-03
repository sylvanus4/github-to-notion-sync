---
name: msp-cost-anomaly-explainer
description: >-
  MSP read-only skill that detects cost anomalies across MSP-managed cloud
  accounts, explains root causes by correlating billing data with
  infrastructure events and configuration changes, and produces an actionable
  report with cost impact and recommended remediation — without making any
  changes to billing or infrastructure. Uses AWS Cost Explorer/CUR/Budgets and
  GCP Billing export/BigQuery/Recommender API. Use when the user asks to
  explain cost spike, analyze billing anomaly, investigate unexpected charges,
  cost anomaly report, spending spike analysis, or needs to understand why
  cloud costs increased. Do NOT use for applying cost optimizations (use
  rightsizing-recommender for compute, idle-resource-cleanup-planner for
  cleanup), setting up budgets or alerts (configure directly), general
  financial analysis (use kwp-finance skills), or incident investigation
  unrelated to cost (use incident-triage-summarizer). Korean triggers: 비용 이상,
  과금 급증, 비용 스파이크 분석, 클라우드 비용 설명, 청구 이상 분석.
disable-model-invocation: true
---

# MSP Cost Anomaly Explainer

Read-only MSP skill that detects, explains, and reports cloud cost anomalies by correlating billing data with infrastructure events—without modifying any billing configurations or cloud resources.

## Usage

```
/msp-cost-anomaly-explainer --tenant acme-corp --cloud aws --period 7d
/msp-cost-anomaly-explainer --tenant acme-corp --cloud gcp --account billing-acct-001 "explain cost spike last 3 days"
/msp-cost-anomaly-explainer --tenant acme-corp --threshold 20 "flag anomalies above 20% deviation"
/msp-cost-anomaly-explainer --tenant acme-corp --service ec2 "why did EC2 costs increase this week"
```

## Prerequisites

- **Identity**: `tenant_id`, billing account/linked account scope, analysis period.
- **AWS credentials (read-only)**:
  - Cost Explorer: `ce:GetCostAndUsage`, `ce:GetCostForecast`, `ce:GetAnomalies`.
  - CUR (optional): S3 read access to Cost and Usage Reports for line-item detail.
  - Budgets: `budgets:DescribeBudgets`, `budgets:DescribeBudgetPerformanceHistory`.
  - CloudTrail: `cloudtrail:LookupEvents` for infrastructure change correlation.
  - Config: `config:GetResourceConfigHistory` for resource configuration changes.
- **GCP credentials (read-only)**:
  - Billing export BigQuery dataset: read access for `SELECT` queries.
  - Recommender API: `recommender.*.list` for optimization suggestions.
  - Cloud Audit Logs: read access for infrastructure change correlation.
  - Asset Inventory: `cloudasset.assets.searchAllResources` for resource context.

## Pipeline Overview

```
Sequential Pipeline (read-only)

  1. Billing data collection        → Fetch daily/hourly cost by service, region, tag
  2. Anomaly detection              → Statistical deviation, budget breach, forecast overshoot
  3. Event correlation              → Match cost spikes to infra events (deploys, scaling, new resources)
  4. Root cause classification      → Categorize: config change, scaling event, pricing change, data transfer, new resource, attack
  5. Impact quantification          → Calculate $ impact, projected monthly run-rate delta
  6. Remediation recommendation     → Suggest actions (all advisory, no execution)

  Output: JSON anomaly report + Markdown executive summary
```

## Detailed Workflow

1. **Collect billing data** — Fetch cost data for the specified period, grouped by service, region, usage type, and resource tags. Compute daily run-rate and compare against baseline (previous 30-day average or budget target).

2. **Detect anomalies** — Apply three detection methods:
   - **Statistical**: Flag services/regions where daily spend exceeds 2σ from 30-day moving average.
   - **Budget-relative**: Flag budget categories where spend-to-date exceeds expected pro-rata allocation by >10%.
   - **Forecast breach**: Flag when updated forecast exceeds budget by >5%.

3. **Correlate with infrastructure events** — For each detected anomaly, search a ±24h window for:
   - **AWS**: CloudTrail events (`RunInstances`, `CreateDBInstance`, `PutScalingPolicy`, `CreateNatGateway`, security group changes), Config configuration item changes, Auto Scaling group events.
   - **GCP**: Audit Log events (compute instance creation, GKE node pool scaling, Cloud SQL instance modifications), Asset Inventory changes.

4. **Classify root cause** — Assign each anomaly to a category:
   | Category | Example | Typical Fix |
   |----------|---------|-------------|
   | Config change | Instance type upgrade, new RDS multi-AZ | Review necessity, downsize |
   | Scaling event | ASG/MIG scale-out, GKE node pool expansion | Review scaling policies |
   | New resource | New NAT Gateway, Load Balancer, EIP | Verify intentional creation |
   | Data transfer | Cross-region/AZ transfer spike | Review architecture |
   | Pricing change | RI/SP expiration, rate increase | Renew commitments |
   | Anomalous usage | Crypto mining, runaway Lambda, EBS snapshot accumulation | Investigate immediately |

5. **Quantify impact** — Calculate:
   - Daily incremental cost vs baseline.
   - Projected monthly run-rate impact if anomaly persists.
   - Percentage of total account spend affected.

6. **Generate remediation recommendations** — All advisory, no execution:
   - Specific actions per anomaly (e.g., "Downsize i3.4xlarge → i3.2xlarge", "Delete orphaned EBS volumes").
   - Estimated savings per recommendation.
   - Urgency classification (immediate/this-week/next-cycle).

7. **Emit JSON report and Markdown summary**.

## Output Schema

```json
{
  "schema_version": "1.0.0",
  "skill": "cost-anomaly-explainer",
  "generated_at": "ISO-8601",
  "tenant_id": "string",
  "cloud": "aws|gcp",
  "analysis_period": { "start": "ISO-8601", "end": "ISO-8601" },
  "baseline_period": { "start": "ISO-8601", "end": "ISO-8601" },
  "summary": {
    "total_anomalies": 0,
    "total_daily_impact_usd": 0.0,
    "projected_monthly_impact_usd": 0.0,
    "top_service": "string",
    "severity_distribution": { "CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0 }
  },
  "anomalies": [
    {
      "id": "string",
      "service": "string",
      "region": "string",
      "detection_method": "statistical|budget|forecast",
      "severity": "CRITICAL|HIGH|MEDIUM|LOW",
      "daily_baseline_usd": 0.0,
      "daily_actual_usd": 0.0,
      "deviation_percent": 0.0,
      "projected_monthly_impact_usd": 0.0,
      "root_cause": {
        "category": "config_change|scaling|new_resource|data_transfer|pricing|anomalous_usage",
        "description": "string",
        "correlated_events": [
          { "timestamp": "ISO-8601", "event_type": "string", "resource": "string", "actor": "string" }
        ],
        "confidence": 0.0
      },
      "remediation": {
        "action": "string",
        "estimated_savings_monthly_usd": 0.0,
        "urgency": "immediate|this_week|next_cycle",
        "read_only": true
      }
    }
  ],
  "budget_status": {
    "budgets_checked": 0,
    "budgets_breached": 0,
    "details": []
  },
  "data_completeness": {
    "cur_available": false,
    "audit_logs_available": true,
    "missing_inputs": ["string"],
    "degraded_mode": false
  }
}
```

## Error Handling

- **CUR data unavailable** — Fall back to Cost Explorer API (lower granularity). Note in `data_completeness`.
- **Audit log gaps** — Report anomalies without event correlation; set `root_cause.confidence` to low.
- **Cross-account billing** — Scope queries to the tenant's linked accounts only. Never cross tenant boundaries.
- **Noisy anomalies** — Apply minimum dollar threshold ($10/day or 5% of baseline) to filter noise.

## Governance

- **Tier 1 — read-only** per `metadata.approval_spec`. No budget modifications, no resource changes, no purchasing actions (RI/SP).
- All remediation recommendations are advisory. Implementation requires human action via appropriate skills (e.g., `rightsizing-recommender`, `idle-resource-cleanup-planner`).
