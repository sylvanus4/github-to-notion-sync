---
name: msp-patch-maintenance-planner
description: >-
  MSP skill that assesses OS and package patch compliance, identifies missing
  critical/security patches, generates a prioritized patch plan with
  maintenance windows and rollback procedures, and optionally schedules patch
  operations via approval gate. Tier 1 for assessment and planning
  (read-only); Tier 2 for scheduling maintenance windows with approval.
  Explicitly PROHIBITS any automatic patch application — patches are planned
  and scheduled only, never executed by this skill. Uses AWS SSM Patch
  Manager/Compliance/Maintenance Windows/Inspector v2 and GCP OS Config/OS
  Inventory/Patch Deployments/Security Command Center. Composes
  compliance-governance, infra-runbook-generator, and evaluation-engine. Use
  when the user asks to check patch compliance, plan maintenance window,
  missing patches report, patch readiness assessment, security patch audit, or
  needs to plan OS/package patching for MSP-managed infrastructure. Do NOT use
  for applying patches directly (execute via SSM/OS Config with separate
  approval), security vulnerability scanning only (use security-expert),
  application-level dependency updates (use dependency-auditor), or incident
  investigation (use incident-triage-summarizer). Korean triggers: 패치 관리, 유지보수
  계획, 패치 준수, 보안 패치 감사, 메인터넌스 윈도우 계획.
disable-model-invocation: true
---

# MSP Patch and Maintenance Planner

MSP skill that assesses OS and package patch compliance, generates a prioritized patch plan with maintenance windows and rollback procedures, and optionally schedules maintenance windows via approval gate. Assessment mode is read-only (Tier 1); scheduling mode requires human approval (Tier 2).

**Automatic patch application is explicitly PROHIBITED. This skill plans and schedules only.**

## Usage

```
/msp-patch-maintenance-planner --tenant acme-corp --cloud aws --mode assess
/msp-patch-maintenance-planner --tenant acme-corp --cloud gcp --mode assess --severity critical,high
/msp-patch-maintenance-planner --tenant acme-corp --cloud aws --mode plan "generate full patch plan"
/msp-patch-maintenance-planner --tenant acme-corp --cloud aws --mode schedule --approve "schedule maintenance window"
```

## Prerequisites

- **Identity**: `tenant_id`, cloud account/project scope, optional instance/patch-group filter.
- **AWS credentials**:
  - (Read-only): SSM: `ssm:DescribeInstancePatches`, `ssm:DescribePatchBaselines`, `ssm:DescribePatchGroups`, `ssm:GetPatchBaseline`, `ssm:DescribeInstancePatchStates`. Inspector v2: `inspector2:ListFindings`. EC2: `ec2:DescribeInstances`.
  - (Tier 2 — scheduling): `ssm:CreateMaintenanceWindow`, `ssm:RegisterTaskWithMaintenanceWindow`, `ssm:UpdateMaintenanceWindowTarget`.
- **GCP credentials**:
  - (Read-only): OS Config: `osconfig.patchJobs.list`, `osconfig.patchDeployments.list`. OS Inventory: `osconfig.inventories.get`. SCC: `securitycenter.findings.list`. Compute: `compute.instances.list`.
  - (Tier 2 — scheduling): `osconfig.patchDeployments.create`.

## Pipeline Overview

```
Sequential Pipeline

  Phase 1: Assessment (Tier 1 — Read-Only)
  1. Instance inventory            → List managed instances with OS info
  2. Patch compliance scan         → Query patch status per instance
  3. Vulnerability correlation     → Cross-reference with Inspector v2 / SCC findings
  4. Compliance scoring            → evaluation-engine multi-dimension scoring

  Phase 2: Planning (Tier 1 — Read-Only)
  5. Patch prioritization          → Rank patches by severity × exploitability × blast radius
  6. Maintenance window design     → Propose windows per environment/group
  7. Rollback procedure            → infra-runbook-generator for rollback steps
  8. Plan document generation      → Full patch plan document

  Phase 3: Scheduling (Tier 2 — Approval-Gated)
  9. Approval gate                 → Human approval for window creation
  10. Schedule creation            → Create SSM Maintenance Window / GCP Patch Deployment
  11. Verification                 → Confirm schedule created correctly

  Output: JSON compliance report + Markdown patch plan (+ schedule confirmation if Tier 2)
```

## Detailed Workflow

### Phase 1: Assessment

1. **Instance inventory** — List all managed instances:
   - **AWS**: SSM-managed instances with OS type, platform, agent version, patch group assignment.
   - **GCP**: OS Config-managed VMs with OS type, OS inventory data.
   - Flag unmanaged instances (no SSM agent / no OS Config agent).

2. **Patch compliance scan**:
   - **AWS**: Query `DescribeInstancePatches` for each instance. Categorize patches: installed, missing, failed, not-applicable.
   - **GCP**: Query OS inventory for installed packages vs. available updates. Check patch deployment history.
   - Classify missing patches by severity: Critical, Important/High, Moderate/Medium, Low.

3. **Vulnerability correlation**:
   - **AWS**: Cross-reference missing patches with Inspector v2 CVE findings. Map CVE-IDs to patch KBs.
   - **GCP**: Cross-reference with Security Command Center vulnerability findings.
   - Identify actively exploited CVEs (CISA KEV catalog cross-reference via web search).

4. **Compliance scoring** — Use `evaluation-engine`:
   | Dimension | Weight |
   |-----------|--------|
   | Critical patch compliance (% installed) | 30% |
   | High patch compliance | 25% |
   | Agent coverage (% of instances managed) | 20% |
   | Patch freshness (days since last patch cycle) | 15% |
   | Reboot pending resolution | 10% |

### Phase 2: Planning

5. **Prioritize patches**:
   - **P1 (Immediate)**: Critical CVEs with known exploits, CISA KEV listed.
   - **P2 (Within 7 days)**: Critical/High severity without known exploits.
   - **P3 (Next maintenance cycle)**: Medium severity, feature updates.
   - **P4 (Deferred)**: Low severity, optional updates.

6. **Design maintenance windows** — Propose per environment:
   | Environment | Window | Duration | Approach |
   |-------------|--------|----------|----------|
   | Dev/Test | Weekday business hours | 2h | Batch all patches |
   | Staging | Weekday off-hours | 3h | Mirror production plan |
   | Production | Weekend off-hours | 4h | Rolling, canary first |

7. **Generate rollback procedures** — Using `infra-runbook-generator` patterns:
   - Pre-patch snapshot/AMI creation steps.
   - Health check criteria (post-patch verification).
   - Rollback trigger conditions.
   - Rollback execution steps (restore from snapshot, revert patch).

8. **Emit patch plan document** — Full plan with instance lists, patch details, window proposals, rollback procedures, and communication plan.

### Phase 3: Scheduling (Tier 2)

9. **Approval gate** — Present plan to approver with:
   - Window timing and duration.
   - Affected instance count per group.
   - Risk assessment summary.
   - Rollback procedure confirmation.

10. **Create schedule** — After approval:
    - **AWS**: Create SSM Maintenance Window with registered tasks for `AWS-RunPatchBaseline`.
    - **GCP**: Create Patch Deployment with the specified schedule and instance filter.
    - Note: This creates the *schedule*. Actual patch execution happens at the scheduled time via the cloud provider's native mechanism.

11. **Verify** — Confirm schedule creation. Record window ID/deployment ID for tracking.

## Output Schema

```json
{
  "schema_version": "1.0.0",
  "skill": "patch-maintenance-planner",
  "generated_at": "ISO-8601",
  "tenant_id": "string",
  "cloud": "aws|gcp",
  "mode": "assess|plan|schedule",
  "summary": {
    "total_instances": 0,
    "managed_instances": 0,
    "unmanaged_instances": 0,
    "compliance_score": 0.0,
    "compliance_grade": "A|B|C|D|F",
    "missing_patches": {
      "critical": 0, "high": 0, "medium": 0, "low": 0
    },
    "instances_needing_reboot": 0,
    "cisa_kev_matches": 0
  },
  "patch_details": [
    {
      "instance_id": "string",
      "instance_name": "string",
      "os": "string",
      "patch_group": "string",
      "missing_patches": [
        {
          "patch_id": "string",
          "title": "string",
          "severity": "CRITICAL|HIGH|MEDIUM|LOW",
          "cve_ids": ["string"],
          "cisa_kev": false,
          "classification": "SecurityUpdates|CriticalUpdates|BugFixes"
        }
      ],
      "reboot_required": false
    }
  ],
  "patch_plan": {
    "priority_groups": [],
    "maintenance_windows": [],
    "rollback_procedure": "string",
    "communication_plan": "string"
  },
  "schedule": {
    "created": false,
    "window_id": "string|null",
    "deployment_id": "string|null",
    "approved_by": "string|null",
    "scheduled_start": "ISO-8601|null"
  },
  "data_completeness": {
    "ssm_agent_coverage": 0.0,
    "os_config_agent_coverage": 0.0,
    "inspector_enabled": true,
    "scc_enabled": true,
    "missing_inputs": ["string"],
    "degraded_mode": false
  }
}
```

## Error Handling

- **SSM/OS Config agent not installed** — Report instances as unmanaged; recommend agent deployment as P1 action.
- **Inspector v2 / SCC not enabled** — Proceed without CVE correlation; note reduced risk assessment quality.
- **Large fleet (1000+ instances)** — Process in batches of 200; aggregate results. Note if sampling was used.
- **Conflicting patch baselines** — Report conflicts; recommend baseline consolidation.

## Governance

- **Tier 1 (assess/plan mode)** — Read-only. No patch application, no schedule creation.
- **Tier 2 (schedule mode)** — Creates maintenance window schedule only after human approval. **Does NOT execute patches** — execution happens at scheduled time via cloud-native patch mechanisms.
- Actual patch application is explicitly outside this skill's scope. This skill *plans* and *schedules*; the cloud provider's native service *executes*.
