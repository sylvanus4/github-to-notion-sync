---
name: msp-terraform-plan-reviewer
description: >-
  MSP Tier-1 read-only Terraform plan risk review. Ingests terraform show
  -json output, classifies IAM/networking/storage/compute changes, scores risk
  1–10, flags replace/recreate and destructive changes, merges Checkov/tfsec
  with terraform-reviewer, and emits approval recommendations (draft only).
  Does NOT apply, destroy, or mutate state. Use when the user asks for
  "terraform plan review", "IaC risk review", "plan risk assessment", "테라폼 플랜
  리뷰", "IaC 검토", "변경 위험 분석", "msp terraform plan", or MSP change-board risk
  summary before apply. Composes terraform-reviewer and adds deterministic MSP
  risk grading. Do NOT use for terraform apply/destroy (Tier 2), Helm-only
  review (use helm-validator), or K8s YAML only (use k8s-manifest-validator).
disable-model-invocation: true
---

# MSP Terraform Plan Reviewer

**Tier 1 — Read-only.** Structured, evidence-backed risk assessment of proposed infrastructure changes **before** any `terraform apply` or automated deployment. Answers: *What is changing, how risky is it, and what is a reasonable approval stance?*

This skill **reviews plans**; it **does not** run `terraform apply`, `terraform destroy`, or any operation that mutates cloud or remote state.

## Summary

| Aspect | Detail |
|--------|--------|
| **Extends** | [`terraform-reviewer`](../../infra/terraform-reviewer/SKILL.md) — validate, Checkov, tfsec, optional LLM narrative |
| **Adds** | Plan JSON parsing, replace/recreate detection, MSP risk taxonomy (1–10), approval recommendation enum, cloud-specific AWS/GCP rules |
| **Pattern** | Sequential: parse plan JSON → classify changes → score risk → merge static analysis → generate approval opinion |
| **Spec** | [`docs/msp-skills/APPROVAL_BOUNDARY_SPEC.md`](../../../../docs/msp-skills/APPROVAL_BOUNDARY_SPEC.md) |

## Usage

- MSP operators or customers need a **change-board ready** risk summary from a saved plan
- Before merge or apply: **structured** per-resource scoring, not only pass/fail static analysis
- Highlights **replace**, **delete**, IAM / security group / firewall changes, and broad network exposure
- Korean: 테라폼 플랜 리뷰, IaC 검토, 변경 위험 분석
- English: terraform plan review, IaC risk review, plan risk assessment

## When NOT to Use

- Executing **apply** or **destroy** (Tier 2 + human approval)
- **Helm-only** validation → `helm-validator`
- **Kubernetes manifests** without Terraform → `k8s-manifest-validator`
- Replacing full `terraform-reviewer` when no plan JSON exists and only static HCL review is needed — invoke `terraform-reviewer` directly

## How It Extends `terraform-reviewer`

| `terraform-reviewer` stage | Role in this skill |
|----------------------------|-------------------|
| Discover roots / scope | Align Checkov/tfsec directory with plan’s module root |
| `terraform validate` | Gate: invalid config → plan not trustworthy |
| Plan (text or binary) | MSP skill **prefers** `terraform show -json` for machine-readable `resource_changes` |
| Checkov / tfsec | Merged into `static_analysis`; may **boost** overall risk when critical/high |
| LLM review | **Optional** supplement; MUST NOT override deterministic replace/IAM/SG flags without plan evidence |

**New (MSP layer):**

1. Parse `resource_changes` from plan JSON (`change.actions`, replace semantics).
2. Classify each change: `IAM`, `NETWORKING`, `STORAGE`, `COMPUTE`, `OTHER`.
3. Score 1–10 per resource and aggregate using the [Risk Classification Matrix](#risk-classification-matrix).
4. Emit `approval_recommendation` and draft ITSM text — **recommendation only**.

## Inputs

| Input | Required | Notes |
|-------|----------|--------|
| **Terraform plan JSON** | **Yes** | `terraform plan -out=tfplan.binary && terraform show -json tfplan.binary` |
| Plan binary path | Optional | Document commands; stay read-only |
| tfvars / labels | Optional | Context only (env, region) — not for applying |
| Provider context | Optional | e.g. `hashicorp/aws`, `hashicorp/google` for classification |
| Tenant / customer ID | Recommended | MSP multi-tenancy; no cross-tenant mixing |
| Module root path | Optional | Same tree as Checkov/tfsec |

**Minimum:** plan JSON + primary provider hint (AWS or GCP).

## Workflow (Sequential)

| Step | Action |
|------|--------|
| **1** | Obtain plan JSON (operator/CI): `terraform plan -out=tfplan.binary && terraform show -json tfplan.binary > plan.json` |
| **2** | Parse `resource_changes`: create / update / delete / **replace** (`delete`+`create`, forces replacement) |
| **3** | Classify each resource: IAM, NETWORKING, STORAGE, COMPUTE, OTHER (provider + type + [Cloud-specific rules](#cloud-specific-risk-rules)) |
| **4** | Apply MSP risk scoring matrix; apply escalation floors (e.g. RDS replace ≥8) |
| **5** | Run **Checkov** and **tfsec** on module directory (same as `terraform-reviewer`) — can parallelize after path known |
| **6** | Merge static analysis into overall score; generate structured output + human appendix — **no apply** |

**Order note:** Validate → plan JSON → parse/classify/score in sequence; static analysis after module path is known, then merge.

## Risk Classification Matrix

Default **risk band** by **category** × **change type**. Final 1–10 combines this with Checkov/tfsec severity and environment (e.g. prod +1–2).

| Change type | IAM | Networking (SG / FW / NACL / routes) | Storage (DB, bucket, vol) | Compute (VM, ASG, MIG) | Other |
|-------------|-----|--------------------------------------|-----------------------------|-------------------------|--------|
| **Create** | Medium 4–6 | Medium 4–6 | Medium 4–6 | Low–Med 3–5 | Low 2–4 |
| **Update** (in-place) | High 6–8 if policy broadens | High 6–9 if exposure increases | Med–High 5–8 if encryption/backup weakened | Med 4–7 if disruption | Med 3–6 |
| **Replace / recreate** | High 7–9 if binding changes | High 7–9 | **Very high 8–10** stateful | High 6–9 | Med–High 5–8 |
| **Delete** | Med–High 5–8 | High 6–9 if path removed | **Very high 8–10** data | High 6–9 | Med 4–7 |

**Escalation (floor examples):**

- Replace on `aws_db_instance` / `google_sql_database_instance`: floor **8**
- SG/firewall: `0.0.0.0/0` to 22, 3389, or broad `/0`: floor **8** unless documented exception ID
- IAM `*:*` or admin-equivalent on production: floor **9–10** → may map to `NOT_RECOMMENDED` until reviewed

**Must surface in output:**

- Any **delete**, **replace**, or `forces replacement`
- IAM policy changes that **broaden** access (statement count/effect)
- SG/FW rule adding `0.0.0.0/0` or IPv6 equivalent any

## Output Schema

Machine-readable results SHOULD follow this shape (JSON or equivalent YAML for humans).

```json
{
  "skill": "msp-terraform-plan-reviewer",
  "version": "1.0.0",
  "approval_tier": "T1_READ_ONLY",
  "inputs": {
    "provider_primary": "aws",
    "plan_source": "terraform_show_json",
    "module_path": "environments/prod"
  },
  "overall": {
    "risk_score": 8,
    "risk_band": "HIGH",
    "destructive_change_present": true,
    "approval_recommendation": "CONDITIONAL_APPROVE",
    "approval_recommendation_rationale": "Replace on stateful resource + SG ingress change; require peer review before apply."
  },
  "resource_changes": [
    {
      "address": "aws_instance.app",
      "provider_name": "registry.terraform.io/hashicorp/aws",
      "type": "aws_instance",
      "actions": ["delete", "create"],
      "is_replace": true,
      "risk_category": "COMPUTE",
      "risk_score": 8,
      "flags": {
        "iam": false,
        "networking": true,
        "storage": false,
        "destructive": true
      },
      "notes": "Replace forces instance recreation; expect downtime unless blue/green outside Terraform."
    }
  ],
  "static_analysis": {
    "checkov": { "summary": "42 passed, 3 failed", "highest_severity": "HIGH" },
    "tfsec": { "summary": "1 critical, 2 high", "highest_severity": "CRITICAL" }
  },
  "composed_skill": {
    "terraform_reviewer_stages_run": ["validate", "plan_dry_run_or_json", "checkov", "tfsec"],
    "llm_review": "optional_supplement"
  }
}
```

### Field definitions

| Field | Description |
|-------|-------------|
| `overall.risk_score` | Integer **1–10**; 10 = critical (e.g. prod destroy, org-wide IAM, world admin ports) |
| `overall.destructive_change_present` | `true` if any delete, replace, or must-recreate |
| `overall.approval_recommendation` | `APPROVE` \| `CONDITIONAL_APPROVE` \| `DEFER` \| `NOT_RECOMMENDED` |
| `resource_changes[].actions` | From plan JSON `change.actions` |
| `resource_changes[].is_replace` | `true` for replace/recreate (e.g. `delete`+`create`) |
| `resource_changes[].risk_category` | `IAM` \| `NETWORKING` \| `STORAGE` \| `COMPUTE` \| `OTHER` |
| `resource_changes[].flags` | `iam`, `networking`, `storage`, `destructive` booleans |

### Human-readable deliverables

- **Executive risk summary:** score, band, destructive flag, top 3 drivers
- **Draft approval text** for ITSM/change ticket
- **Detailed table:** per-resource classification and scores (appendix)

## Cloud-Specific Risk Rules

### AWS (`hashicorp/aws`)

**High sensitivity (typical floor ≥6 without mitigation):**

- `aws_iam_*` policy attachments, role policies, SSO permission sets, Org/SCP-related resources where in plan
- `aws_security_group`, `aws_security_group_rule`, `aws_network_acl*`, `aws_vpc_network_*` — broadening ingress (`0.0.0.0/0`), admin ports, flattening egress
- `aws_route53_record`, `aws_globalaccelerator_*`, `aws_lb_listener*` — public exposure or TLS changes
- `aws_db_instance`, `aws_rds_cluster*`, `aws_elasticache_*` — **replace** or params affecting availability/data
- `aws_s3_bucket`, `aws_s3_bucket_policy`, `aws_s3_bucket_public_access_block` — public access or policy loosening

**Destructive / replace:** `aws_instance`, `aws_launch_template`, ASG/LT changes forcing replacement; `aws_cloudformation_stack` when plan shows nested replace

### GCP (`hashicorp/google`)

**High sensitivity:**

- `google_project_iam_*`, `google_organization_iam_*`, `google_service_account_iam_*`, custom roles
- `google_compute_firewall` — `0.0.0.0/0`, broad tags, default-VPC relaxations
- `google_compute_instance`, `google_compute_instance_group_manager` — recreate or disruptive type/disk changes
- `google_sql_database_instance` — tier, autoresize off, deletion protection off
- `google_storage_bucket*`, `google_storage_bucket_iam_*` — public ACL/IAM `allUsers`

**Networking:** `google_compute_router_nat`, `google_compute_forwarding_rule`, LB URL maps when SSL/path exposure changes

### Default

- Unknown types: `OTHER`; score from **action** (delete/replace > update > create) + static analysis

## Governance

| Allowed | Forbidden |
|---------|-----------|
| Parse plan JSON; `terraform validate`; Checkov; tfsec; read tfvars for labels | `terraform apply`, `terraform destroy`, state push/pull that mutates remote state |
| Reports and **draft** approval text | Any provider create/update/delete via this skill |
| | Customer email send without separate Tier-2 workflow |

This skill **recommends**; **Tier 2** (human + pipeline) applies per customer MSP policy. Automation allowlists MUST exclude apply/destroy for this skill identity.

## Prerequisites

Same as [`terraform-reviewer`](../../infra/terraform-reviewer/SKILL.md): `terraform`, `checkov`, `tfsec` as applicable. Missing tools → mark stages `SKIPPED` and note in `static_analysis`.

## Reference Commands (Read-Only)

```bash
terraform plan -out=tfplan.binary
terraform show -json tfplan.binary > plan.json
```

## Examples

### Example 1: Korean request

**User:** "프로드 테라폼 플랜 JSON 줬어. 변경 위험 분석해줘."

**Actions:**

1. Ingest `plan.json` from `terraform show -json`
2. For each `resource_change`, set `is_replace`, `risk_category`, `risk_score`, `flags`
3. Run Checkov/tfsec on declared module root
4. Set `overall.risk_score`, `approval_recommendation`, Korean + English executive summary

**Result:** Structured JSON + change-ticket draft; **no apply**

### Example 2: English — plan risk assessment

**User:** "Run an IaC risk review on this AWS plan.json before the CAB."

**Actions:** Same pipeline; emphasize `NOT_RECOMMENDED` / `CONDITIONAL_APPROVE` when destructive + open ingress + critical tfsec

### Example 3: Replace security group (from plan)

Input shows `aws_security_group.web` with `actions: ["delete","create"]` and `0.0.0.0/0:22`.

**Output excerpt:**

- `overall.risk_score`: 9, `destructive_change_present`: true
- `approval_recommendation`: `NOT_RECOMMENDED` until CIDR restricted
- Flags: `networking`, `destructive`

## Error Handling

| Situation | Action |
|----------|--------|
| Invalid JSON / missing `resource_changes` | Report parse error; suggest regenerating with `terraform show -json` |
| No plan JSON; only HCL on disk | Run `terraform-reviewer` validate + Checkov/tfsec; state plan JSON as preferred follow-up |
| State/auth unavailable for new plan | Review user-supplied **existing** `plan.json` only; do not require live `terraform plan` for Tier-1 analysis |

## Composed Agent Flow

```text
plan.json → parse/classify/score
     ↘
      merge ← terraform-reviewer (validate, checkov, tfsec) + optional LLM
     ↘
  structured output + approval draft (Tier 1 only)
```

## Related

- [`terraform-reviewer`](../../infra/terraform-reviewer/SKILL.md) — base pipeline
- [`iac-review-agent`](../../infra/iac-review-agent/SKILL.md) — unified IaC entry; this skill is the **plan-JSON–aware** MSP specialist
- [`docs/msp-skills/plans/terraform-plan-reviewer.md`](../../../../docs/msp-skills/plans/terraform-plan-reviewer.md) — planning spec
