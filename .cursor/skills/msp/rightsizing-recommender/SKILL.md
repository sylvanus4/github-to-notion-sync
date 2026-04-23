---
name: msp-rightsizing-recommender
description: >-
  MSP read-only skill that analyzes compute resource utilization across
  MSP-managed accounts and generates specific rightsizing recommendations
  (downsize, upsize, switch instance family, convert to Arm/Graviton) with
  projected monthly savings — without making any infrastructure changes. Uses
  AWS Compute Optimizer/CloudWatch and GCP Recommender API/Cloud Monitoring.
  Use when the user asks to rightsize instances, optimize compute costs,
  review resource utilization, find oversized instances, compute
  optimization report, or needs utilization-based resize recommendations.
  Do NOT use for applying instance changes (use Terraform or console
  directly), idle resource identification (use idle-resource-cleanup-planner),
  cost anomaly investigation (use cost-anomaly-explainer), non-compute
  optimization (storage, network — handle separately), or incident
  investigation (use incident-triage-summarizer). Korean triggers: 라이트사이징,
  인스턴스 최적화, 컴퓨트 비용 절감, 리소스 사용률 분석, 과프로비저닝 분석.
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "msp/finops"
  approval_tier: "tier-1"
  approval_spec: "docs/msp-skills/APPROVAL_BOUNDARY_SPEC.md"
  mutations: []
  clouds:
    - "aws"
    - "gcp"
  composes: []
---

# MSP Rightsizing Recommender

Read-only MSP skill that analyzes compute resource utilization metrics across MSP-managed cloud accounts and generates specific rightsizing recommendations with projected monthly savings, without modifying any infrastructure.

## Usage

```
/msp-rightsizing-recommender --tenant acme-corp --cloud aws --region us-east-1
/msp-rightsizing-recommender --tenant acme-corp --cloud gcp --project prod-project "rightsizing report"
/msp-rightsizing-recommender --tenant acme-corp --min-savings 50 "only show recommendations saving >$50/mo"
/msp-rightsizing-recommender --tenant acme-corp --instance-family c5 "check all c5 instances"
```

## Prerequisites

- **Identity**: `tenant_id`, cloud account/project scope, optional region/instance filters.
- **AWS credentials (read-only)**:
  - Compute Optimizer: `compute-optimizer:GetEC2InstanceRecommendations`, `GetAutoScalingGroupRecommendations`, `GetECSServiceRecommendations`.
  - CloudWatch: `cloudwatch:GetMetricStatistics` for CPU, memory (via CloudWatch Agent), network, disk I/O.
  - EC2: `ec2:DescribeInstances`, `ec2:DescribeInstanceTypes` for current configuration.
  - Cost Explorer: `ce:GetCostAndUsage` for current hourly cost.
- **GCP credentials (read-only)**:
  - Recommender API: `recommender.computeInstanceMachineTypeRecommendations.list`.
  - Cloud Monitoring: `monitoring.timeSeries.list` for CPU, memory, network metrics.
  - Compute Engine: `compute.instances.list`, `compute.machineTypes.list`.

## Pipeline Overview

```
Sequential Pipeline (read-only)

  1. Inventory collection       → List all compute instances/VMs with current specs
  2. Utilization analysis       → Fetch 14-day metrics (CPU, memory, network, disk)
  3. Cloud-native recommender   → Query Compute Optimizer / Recommender API
  4. Custom analysis layer      → Apply MSP-specific rules (Arm migration, burstable, spot eligibility)
  5. Savings projection         → Calculate per-recommendation monthly savings
  6. Prioritization             → Rank by savings, risk, and implementation ease

  Output: JSON recommendation report + Markdown summary
```

## Detailed Workflow

1. **Inventory collection** — List all compute resources in scope:
   - **AWS**: EC2 instances, ECS services, RDS instances (compute component).
   - **GCP**: Compute Engine VMs, GKE node pools, Cloud SQL instances (compute component).
   Record current instance type, vCPUs, memory, pricing tier, tags.

2. **Utilization analysis** — For each resource, fetch 14-day metrics:
   - **CPU**: p50, p95, p99, max.
   - **Memory**: p50, p95, p99, max (requires CloudWatch Agent on AWS; native on GCP).
   - **Network**: average throughput in/out.
   - **Disk I/O**: average IOPS, throughput.

3. **Cloud-native recommendations** — Merge with provider recommendations:
   - **AWS Compute Optimizer**: Include finding reason codes, estimated savings.
   - **GCP Recommender**: Include machine type suggestions with estimated savings.

4. **Custom MSP analysis layer** — Apply additional rules:
   - **Arm/Graviton migration**: Flag x86 instances with <60% CPU p95 as Graviton candidates (AWS) or T2A candidates (GCP). Estimate 20-40% savings.
   - **Burstable eligibility**: Instances with <20% average CPU → recommend t3/t4g (AWS) or e2 (GCP).
   - **Generation upgrade**: Older generations (m4→m6i, n1→n2) with equivalent or better price-performance.
   - **Over-provisioned memory**: CPU utilized but memory <30% p95 → recommend compute-optimized family.
   - **Over-provisioned CPU**: Memory utilized but CPU <20% p95 → recommend memory-optimized family.

5. **Savings projection** — For each recommendation:
   - Current monthly cost (on-demand equivalent).
   - Recommended monthly cost.
   - Monthly savings and percentage reduction.
   - Aggregate total monthly savings for the tenant.

6. **Risk assessment and prioritization** — Rank recommendations:
   - **Ease**: Same-family downsize (easy) > family switch (moderate) > Arm migration (requires testing).
   - **Risk**: Stateless compute (low) > stateful (medium) > database (high).
   - **Savings**: Higher savings rank higher within the same risk tier.

7. **Emit JSON report and Markdown summary**.

## Output Schema

```json
{
  "schema_version": "1.0.0",
  "skill": "rightsizing-recommender",
  "generated_at": "ISO-8601",
  "tenant_id": "string",
  "cloud": "aws|gcp",
  "scope": { "accounts": ["string"], "regions": ["string"] },
  "summary": {
    "total_resources_analyzed": 0,
    "resources_with_recommendations": 0,
    "total_monthly_savings_usd": 0.0,
    "recommendation_distribution": {
      "downsize": 0, "upsize": 0, "family_switch": 0, "arm_migration": 0, "generation_upgrade": 0
    }
  },
  "recommendations": [
    {
      "rank": 1,
      "resource_id": "string",
      "resource_name": "string",
      "resource_type": "ec2|gce|rds|cloudsql|ecs|gke_nodepool",
      "current_spec": {
        "instance_type": "string",
        "vcpus": 0,
        "memory_gb": 0.0,
        "monthly_cost_usd": 0.0
      },
      "recommended_spec": {
        "instance_type": "string",
        "vcpus": 0,
        "memory_gb": 0.0,
        "monthly_cost_usd": 0.0
      },
      "action": "downsize|upsize|family_switch|arm_migration|generation_upgrade",
      "utilization": {
        "cpu_p95": 0.0,
        "memory_p95": 0.0,
        "network_avg_mbps": 0.0
      },
      "monthly_savings_usd": 0.0,
      "savings_percent": 0.0,
      "risk": "LOW|MEDIUM|HIGH",
      "ease": "easy|moderate|requires_testing",
      "rationale": "string",
      "source": "compute_optimizer|recommender_api|msp_custom_rule",
      "read_only": true
    }
  ],
  "excluded_resources": [
    {
      "resource_id": "string",
      "reason": "string"
    }
  ],
  "data_completeness": {
    "memory_metrics_available": false,
    "cloud_recommender_available": true,
    "missing_inputs": ["string"],
    "degraded_mode": false
  }
}
```

## Error Handling

- **Memory metrics unavailable** — Proceed with CPU-only analysis; flag in `data_completeness`. Note that memory-based recommendations are absent.
- **Compute Optimizer / Recommender not enabled** — Fall back to custom utilization-based analysis only. Record in `data_completeness`.
- **Spot/Reserved instances** — Note current pricing model in `current_spec`. Savings calculated against on-demand equivalent for comparability.
- **Recently launched instances** (<14 days) — Exclude from recommendations; list in `excluded_resources` with reason.

## Governance

- **Tier 1 — read-only** per `metadata.approval_spec`. No instance modifications, no scaling policy changes, no purchasing actions.
- All recommendations are advisory. Implementation requires human review and execution via appropriate change management processes.
