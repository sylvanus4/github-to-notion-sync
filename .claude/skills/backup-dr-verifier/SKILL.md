---
name: msp-backup-dr-verifier
description: >-
  MSP read-only skill that verifies backup policies, job completion, retention
  compliance, and disaster recovery configurations across AWS and GCP,
  producing a compliance report with identified gaps and remediation
  recommendations — without modifying any backup or DR configurations. Uses
  AWS Backup/RDS snapshots/EBS snapshots/S3 versioning and GCP Backup for
  GKE/Cloud SQL backups/Persistent Disk snapshots/Cloud Storage lifecycle.
  Composes compliance-governance and evaluation-engine. Use when the user asks
  to verify backup compliance, check DR readiness, audit backup policies,
  validate retention, backup health report, or needs to assess backup and DR
  posture for MSP-managed accounts. Do NOT use for configuring backups or DR
  (handle directly), incident investigation (use incident-triage-summarizer),
  cost analysis of backup storage (use cost-anomaly-explainer), or restore
  testing execution (handle manually). Korean triggers: 백업 검증, DR 준비 상태, 백업 정책
  감사, 리텐션 확인, 백업 건강 점검.
disable-model-invocation: true
---

# MSP Backup and DR Verifier

Read-only MSP skill that audits backup policies, job success rates, retention compliance, and DR configurations across MSP-managed cloud accounts, producing a structured compliance report with gap identification and remediation recommendations—without modifying any configurations.

## Usage

```
/msp-backup-dr-verifier --tenant acme-corp --cloud aws --check backups
/msp-backup-dr-verifier --tenant acme-corp --cloud gcp --check dr
/msp-backup-dr-verifier --tenant acme-corp --cloud aws --check all "full backup and DR audit"
/msp-backup-dr-verifier --tenant acme-corp --retention-policy "7d daily, 4w weekly, 12m monthly"
```

## Prerequisites

- **Identity**: `tenant_id`, cloud account/project scope, customer-defined retention policy (or use MSP defaults).
- **AWS credentials (read-only)**:
  - AWS Backup: `backup:ListBackupPlans`, `backup:ListBackupJobs`, `backup:ListRecoveryPoints`, `backup:DescribeBackupVault`.
  - RDS: `rds:DescribeDBSnapshots`, `rds:DescribeDBClusterSnapshots`, `rds:DescribeDBInstances`.
  - EC2: `ec2:DescribeSnapshots`, `ec2:DescribeVolumes`.
  - S3: `s3:GetBucketVersioning`, `s3:GetBucketLifecycleConfiguration`.
  - Elastic Disaster Recovery: `drs:DescribeSourceServers`, `drs:DescribeJobs`, `drs:DescribeRecoveryInstances`.
- **GCP credentials (read-only)**:
  - Backup for GKE: `gkebackup.backupPlans.list`, `gkebackup.backups.list`, `gkebackup.restorePlans.list`.
  - Cloud SQL: `cloudsql.backupRuns.list`, `cloudsql.instances.list`.
  - Compute Engine: `compute.snapshots.list`, `compute.disks.list`.
  - Cloud Storage: `storage.buckets.getIamPolicy`, lifecycle configuration read.

## Pipeline Overview

```
Sequential Pipeline (read-only)

  1. Resource inventory           → List all backup-eligible resources
  2. Backup policy audit          → Check policy existence, schedule, retention settings
  3. Job completion analysis      → Audit backup job success/failure rates over 30 days
  4. Retention compliance         → Verify actual retention meets declared policy
  5. DR configuration audit       → Check cross-region replication, failover config, RPO/RTO
  6. Gap analysis                 → Identify unprotected resources, policy violations
  7. Compliance scoring           → evaluation-engine multi-dimension scoring
  8. Remediation recommendations  → Prioritized fix list

  Output: JSON compliance report + Markdown audit summary
```

## Detailed Workflow

1. **Resource inventory** — Enumerate backup-eligible resources:
   - **AWS**: EC2 instances, EBS volumes, RDS instances/clusters, S3 buckets, DynamoDB tables, EFS file systems.
   - **GCP**: GKE clusters, Cloud SQL instances, Persistent Disks, Cloud Storage buckets, Filestore instances.

2. **Backup policy audit** — For each resource:
   - Is a backup policy assigned? (AWS Backup plan, GCP backup plan)
   - Backup schedule frequency (daily, hourly, weekly).
   - Retention period configured vs. customer-defined policy.
   - Encryption at rest for backup vault/storage.

3. **Job completion analysis** — For the past 30 days:
   - Success rate per backup plan.
   - Failed jobs: error message, resource affected, timestamp.
   - Missed schedules (no backup attempt when expected).
   - Backup size trends (sudden increases/decreases may indicate issues).

4. **Retention compliance** — Verify:
   - Oldest available recovery point meets minimum retention.
   - No premature deletions (lifecycle rules too aggressive).
   - Compliance with customer-specific retention tiers (daily/weekly/monthly/annual).

5. **DR configuration audit**:
   - **Cross-region replication**: RDS read replicas, S3 CRR, GCS dual-region/multi-region.
   - **Failover configuration**: RDS Multi-AZ, Cloud SQL HA, GKE multi-zonal.
   - **RPO/RTO assessment**: Estimated RPO from backup frequency, estimated RTO from last restore test (if available).
   - **DR runbook existence**: Check for documented DR procedures.

6. **Gap analysis** — Identify:
   - Unprotected resources (no backup policy assigned).
   - Single-region resources with no cross-region backup.
   - Critical resources with >24h RPO.
   - Resources where last successful backup >48h ago.

7. **Compliance scoring** — Use `evaluation-engine` with dimensions:
   | Dimension | Weight |
   |-----------|--------|
   | Backup coverage (% of resources protected) | 25% |
   | Job success rate (30-day) | 20% |
   | Retention compliance | 20% |
   | DR readiness (cross-region, failover) | 20% |
   | Encryption and access control | 15% |

8. **Generate remediation recommendations** — Prioritized by: unprotected critical resources first, then failed backups, then retention gaps, then DR improvements.

## Output Schema

```json
{
  "schema_version": "1.0.0",
  "skill": "backup-dr-verifier",
  "generated_at": "ISO-8601",
  "tenant_id": "string",
  "cloud": "aws|gcp",
  "check_type": "backups|dr|all",
  "summary": {
    "total_resources": 0,
    "protected_resources": 0,
    "unprotected_resources": 0,
    "backup_coverage_percent": 0.0,
    "job_success_rate_30d": 0.0,
    "retention_compliant_percent": 0.0,
    "dr_ready_percent": 0.0,
    "compliance_score": 0.0,
    "compliance_grade": "A|B|C|D|F",
    "critical_gaps": 0
  },
  "backup_audit": {
    "policies": [],
    "job_results_30d": {
      "total": 0, "succeeded": 0, "failed": 0, "missed": 0
    },
    "failed_jobs": [],
    "retention_violations": []
  },
  "dr_audit": {
    "cross_region_replication": [],
    "failover_configs": [],
    "estimated_rpo": "string",
    "estimated_rto": "string",
    "dr_runbook_exists": false
  },
  "gaps": [
    {
      "resource_id": "string",
      "resource_type": "string",
      "gap_type": "unprotected|failed_backup|retention_violation|no_dr|no_encryption",
      "severity": "CRITICAL|HIGH|MEDIUM|LOW",
      "description": "string",
      "remediation": {
        "action": "string",
        "priority": "immediate|this_week|next_cycle",
        "read_only": true
      }
    }
  ],
  "data_completeness": {
    "aws_backup_enabled": true,
    "gcp_backup_for_gke_enabled": true,
    "missing_inputs": ["string"],
    "degraded_mode": false
  }
}
```

## Error Handling

- **AWS Backup not enabled** — Fall back to service-native snapshot enumeration (EBS snapshots, RDS snapshots). Note reduced coverage.
- **GCP Backup for GKE not enabled** — Report GKE clusters as unprotected; recommend enabling backup plans.
- **Large account with 10K+ resources** — Sample top-tagged critical resources first; full scan as time permits. Note sampling in report.
- **Missing retention policy** — Use MSP defaults (7-day daily, 4-week weekly, 12-month monthly) and flag that customer policy is not defined.

## Governance

- **Tier 1 — read-only** per `metadata.approval_spec`. No backup configuration changes, no vault modifications, no restore operations.
- All remediation recommendations are advisory. Implementation requires human review and execution via appropriate change management processes.
