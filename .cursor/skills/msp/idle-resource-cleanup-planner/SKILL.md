---
name: msp-idle-resource-cleanup-planner
description: >-
  MSP skill that identifies idle and orphaned cloud resources, estimates
  ongoing waste cost, and produces a cleanup plan. Tier 1 for discovery and
  recommendation (read-only); Tier 2 for deletion with mandatory human
  approval gate. Enforces strict safety rules — never auto-deletes RDS
  instances, S3 buckets with data, production-tagged resources, or encrypted
  volumes without key verification. Uses AWS Cost Explorer/Config/EC2/EBS/ELB
  and GCP Asset Inventory/Recommender API/Compute Engine. Composes
  rightsizing-recommender (MSP #12) for utilization cross-check and
  incident-lifecycle-manager for approval patterns. Use when the user asks
  to find idle resources, cleanup orphaned resources, waste report, unused
  resource scan, cloud cleanup plan, or needs to identify and plan removal
  of unused cloud resources. Do NOT use for compute rightsizing only (use
  rightsizing-recommender), cost anomaly investigation (use
  cost-anomaly-explainer), active resource management or scaling (handle
  directly), or incident investigation (use incident-triage-summarizer).
  Korean triggers: 유휴 리소스, 고아 리소스, 클라우드 정리, 낭비 비용 분석, 리소스
  정리 계획.
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "msp/finops"
  approval_tier: "tier-1/tier-2"
  approval_spec: "docs/msp-skills/APPROVAL_BOUNDARY_SPEC.md"
  mutations:
    - "resource_deletion (tier-2, approval-gated)"
  clouds:
    - "aws"
    - "gcp"
  composes:
    - "msp-rightsizing-recommender"
    - "incident-lifecycle-manager"
---

# MSP Idle Resource Cleanup Planner

MSP skill that discovers idle and orphaned cloud resources, quantifies ongoing waste, and produces a prioritized cleanup plan. Discovery mode is read-only (Tier 1); deletion mode requires mandatory human approval per resource (Tier 2).

## Usage

```
/msp-idle-resource-cleanup-planner --tenant acme-corp --cloud aws --mode discover
/msp-idle-resource-cleanup-planner --tenant acme-corp --cloud gcp --mode discover --min-waste 100
/msp-idle-resource-cleanup-planner --tenant acme-corp --cloud aws --mode cleanup --approve "execute approved cleanup items"
```

## Prerequisites

- **Identity**: `tenant_id`, cloud account/project scope, optional region filter.
- **AWS credentials (read-only for discover; write for cleanup)**:
  - EC2: `DescribeInstances`, `DescribeVolumes`, `DescribeAddresses`, `DescribeSnapshots`, `DescribeLoadBalancers`, `DescribeNatGateways`.
  - Config: `GetResourceConfigHistory`, `SelectAggregateResourceConfig`.
  - Cost Explorer: `GetCostAndUsage` for per-resource cost estimation.
  - CloudWatch: `GetMetricStatistics` for usage metrics (NetworkIn/Out, VolumeRead/WriteOps).
  - Cleanup (Tier 2): `ec2:TerminateInstances`, `ec2:DeleteVolume`, `ec2:ReleaseAddress`, `ec2:DeleteSnapshot`, `elasticloadbalancing:DeleteLoadBalancer`.
- **GCP credentials (read-only for discover; write for cleanup)**:
  - Asset Inventory: `cloudasset.assets.searchAllResources`.
  - Recommender API: `recommender.computeInstanceIdleResourceRecommendations.list`.
  - Compute Engine: `compute.instances.list`, `compute.disks.list`, `compute.addresses.list`.
  - Cloud Monitoring: `monitoring.timeSeries.list`.
  - Cleanup (Tier 2): `compute.instances.delete`, `compute.disks.delete`, `compute.addresses.delete`.

## Pipeline Overview

```
Sequential Pipeline

  1. Resource inventory scan     → List all resources by type across account/project
  2. Idle detection              → Apply per-type idle criteria (metrics, age, attachment)
  3. Cross-check utilization     → rightsizing-recommender (MSP #12) for borderline cases
  4. Waste quantification        → Monthly cost per idle resource
  5. Safety classification       → Never-auto-delete, approval-required, safe-to-delete
  6. Cleanup plan generation     → Prioritized plan with estimated total savings

  [Optional, Tier 2 only]
  7. Approval gate               → incident-lifecycle-manager pattern — human approval per resource
  8. Deletion execution          → Execute approved deletions with rollback safety
  9. Post-cleanup verification   → Confirm deletion, update cost estimate

  Output: JSON idle report + Markdown cleanup plan (+ execution log if Tier 2)
```

## Detailed Workflow

### Phase 1: Discovery (Tier 1 — Read-Only)

1. **Resource inventory** — Enumerate resources by type: EC2/GCE instances, EBS/Persistent Disk volumes, Elastic IPs/Static IPs, ELB/Cloud Load Balancers, NAT Gateways, EBS/PD snapshots (>90 days), unused security groups/firewall rules.

2. **Apply idle detection criteria**:
   | Resource Type | Idle Criteria |
   |--------------|---------------|
   | EC2/GCE instances | Stopped >14 days, or running with CPU p95 <2% for 14 days |
   | EBS volumes | Unattached >7 days |
   | Persistent Disks | Unattached >7 days |
   | Elastic IPs / Static IPs | Unassociated |
   | Load Balancers | Zero healthy targets for >7 days |
   | NAT Gateways | Zero bytes processed for >7 days |
   | Snapshots | Age >90 days AND parent volume deleted |
   | Security Groups | Unreferenced by any ENI or resource |

3. **Cross-check** — For borderline instances (CPU 2–10%), query `rightsizing-recommender` for utilization context. Mark as "review" rather than "idle" if utilization is ambiguous.

4. **Quantify waste** — Calculate monthly cost per idle resource using on-demand rates.

5. **Safety classification** — Categorize each resource:
   - **NEVER_AUTO_DELETE**: RDS/Cloud SQL instances, S3 buckets/GCS buckets with data, production-tagged resources, encrypted volumes without verified key access, resources with deletion protection enabled.
   - **APPROVAL_REQUIRED**: Running instances (even if idle), volumes with snapshots, resources in shared VPCs.
   - **SAFE_TO_DELETE**: Unattached EBS volumes with no snapshots, unassociated EIPs, orphaned snapshots with deleted parent.

6. **Generate cleanup plan** — Prioritized list sorted by monthly waste (highest first). Each item includes resource ID, type, idle criteria met, monthly cost, safety classification, and recommended action.

### Phase 2: Cleanup Execution (Tier 2 — Approval-Gated)

7. **Approval gate** — Present cleanup plan to approver. Each `APPROVAL_REQUIRED` resource requires individual approval. `SAFE_TO_DELETE` resources can be batch-approved. `NEVER_AUTO_DELETE` resources are excluded from execution and flagged for manual review only.

8. **Execute deletions** — For approved resources only:
   - Create snapshot before deleting EBS volumes (safety net).
   - Execute deletion with retry logic.
   - Log each action with timestamp, resource ID, approver, and execution result.

9. **Post-cleanup verification** — Confirm resources are deleted. Update estimated monthly savings.

## Output Schema

```json
{
  "schema_version": "1.0.0",
  "skill": "idle-resource-cleanup-planner",
  "generated_at": "ISO-8601",
  "tenant_id": "string",
  "cloud": "aws|gcp",
  "mode": "discover|cleanup",
  "summary": {
    "total_resources_scanned": 0,
    "idle_resources_found": 0,
    "total_monthly_waste_usd": 0.0,
    "safety_distribution": {
      "NEVER_AUTO_DELETE": 0,
      "APPROVAL_REQUIRED": 0,
      "SAFE_TO_DELETE": 0
    }
  },
  "idle_resources": [
    {
      "resource_id": "string",
      "resource_type": "string",
      "resource_name": "string",
      "region": "string",
      "idle_criteria": "string",
      "idle_since": "ISO-8601",
      "monthly_cost_usd": 0.0,
      "safety_class": "NEVER_AUTO_DELETE|APPROVAL_REQUIRED|SAFE_TO_DELETE",
      "tags": {},
      "recommended_action": "delete|review|snapshot_then_delete|manual_review_only"
    }
  ],
  "cleanup_execution": {
    "executed": false,
    "approved_count": 0,
    "deleted_count": 0,
    "failed_count": 0,
    "monthly_savings_realized_usd": 0.0,
    "actions": [
      {
        "resource_id": "string",
        "action": "string",
        "status": "approved|executed|failed|skipped",
        "approver": "string",
        "timestamp": "ISO-8601",
        "error": "string|null"
      }
    ]
  },
  "data_completeness": {
    "missing_inputs": ["string"],
    "degraded_mode": false
  }
}
```

## Deletion Safety Rules (Non-Negotiable)

1. **NEVER auto-delete**: RDS/Cloud SQL instances, S3/GCS buckets with objects, resources tagged `env:production` or `do-not-delete:true`, encrypted volumes without confirmed key access, resources with deletion protection enabled.
2. **Always snapshot before delete**: EBS volumes and Persistent Disks (even those marked `SAFE_TO_DELETE`).
3. **Cross-tenant isolation**: Never operate across tenant boundaries.
4. **Audit trail**: Every deletion logged with approver identity, timestamp, and resource details.

## Error Handling

- **Metric data gaps** — Use last-known state + tag-based heuristics. Flag with reduced confidence.
- **Deletion protection enabled** — Skip resource, log as "deletion protection active."
- **Cross-account resource** — Skip, log, and flag for manual review.
- **Partial execution failure** — Continue with remaining approved items; report failures separately.

## Governance

- **Tier 1 (discover mode)** — Read-only. No mutations.
- **Tier 2 (cleanup mode)** — Approval-gated per `metadata.approval_spec`. Each `APPROVAL_REQUIRED` resource needs individual human approval. `NEVER_AUTO_DELETE` resources are never executed, only reported.
