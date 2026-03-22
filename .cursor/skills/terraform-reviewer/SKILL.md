---
name: terraform-reviewer
description: >-
  Review Terraform modules using terraform validate, terraform plan dry-run,
  Checkov/tfsec static analysis, and LLM-based HCL review for security, cost,
  and AWS Well-Architected patterns. Produces a structured pass/fail report.
  Use when the user asks to "review Terraform", "validate Terraform",
  "Terraform security check", "Terraform 리뷰", "테라폼 검증", "terraform-reviewer",
  or any Terraform/IaC quality validation. Do NOT use for Helm chart validation
  (use helm-validator), K8s manifest validation (use k8s-manifest-validator),
  or general infrastructure design (use sre-devops-expert).
metadata:
  version: "1.0.0"
  category: "review"
  author: "thaki"
---
# Terraform Reviewer

Review Terraform configurations through a 4-stage pipeline: syntax validation, plan analysis, static security scanning, and LLM-augmented best-practice review.

## When to Use

- Before merging PRs that modify `.tf`, `.tfvars`, or `.terraform.lock.hcl` files
- As part of the `iac-review-agent` unified IaC review pipeline
- When onboarding new Terraform modules or upgrading provider versions
- Security review of infrastructure changes

## Prerequisites

| Tool | Install | Purpose |
|------|---------|---------|
| `terraform` | `brew install terraform` | Validate and plan |
| `checkov` | `pip install checkov` | Static analysis (CIS, SOC2, HIPAA) |
| `tfsec` | `brew install tfsec` | Security-focused static analysis |

Missing tools are reported as `SKIPPED` in the output.

## Workflow

### Step 1: Discover Terraform Roots

Detect Terraform root modules in the target scope:

```bash
find <scope> -name "*.tf" -type f | xargs dirname | sort -u
```

For each root module, run Steps 2-6.

### Step 2: Terraform Validate

Initialize and validate syntax without accessing remote state:

```bash
cd <module-dir>
terraform init -backend=false
terraform validate
```

Capture validation errors (missing variables, type mismatches, syntax errors).

### Step 3: Terraform Plan (Dry-Run)

If credentials/state are available, run a plan to detect drift and preview changes:

```bash
terraform plan -no-color -input=false 2>&1
```

Parse output for: resources to add/change/destroy, potential data loss, and security group changes.

If state is unavailable, skip this step and note it in the report.

### Step 4: Checkov Static Analysis

Run Checkov for compliance framework checks:

```bash
checkov -d <module-dir> --output json --compact --quiet
```

Checkov covers: CIS benchmarks, SOC2, HIPAA, PCI-DSS, AWS/Azure/GCP best practices.

Parse JSON output for passed/failed/skipped checks with severity levels.

### Step 5: tfsec Security Scan

Run tfsec for security-focused analysis:

```bash
tfsec <module-dir> --format json --no-color
```

Key checks: public access, encryption at rest/transit, IAM overprivilege, logging gaps.

### Step 6: LLM-Augmented Review

After automated tools, perform an LLM review of:
- **Security**: IAM policies for least privilege, security group rules for overly permissive access
- **Cost**: Instance sizing, reserved capacity opportunities, storage class selection
- **Reliability**: Multi-AZ configuration, backup policies, auto-scaling setup
- **State management**: Remote state backend configuration, state locking, sensitive outputs
- **Module design**: Variable validation, output documentation, version constraints

### Step 7: Aggregate Report

```
Terraform Review Report
=======================
Module: <module-path>
Provider(s): aws v5.31, kubernetes v2.24
Terraform: >= 1.5.0

Stage                  Status    Details
────────────────────── ───────── ──────────────────────
Validate               PASS      Configuration is valid
Plan                   SKIPPED   No state backend configured
Checkov                WARN      42 passed, 3 failed, 5 skipped
tfsec                  FAIL      1 critical, 2 high findings
LLM Review             WARN      2 recommendations

FINDINGS:
- severity: Critical
  file: main.tf:23
  rule: CKV_AWS_24
  issue: Security group allows ingress from 0.0.0.0/0 on port 22
  fix: Restrict SSH access to known CIDR blocks

- severity: High
  file: s3.tf:8
  rule: aws-s3-encryption-customer-key
  issue: S3 bucket not using CMK encryption
  fix: Add server_side_encryption_configuration with aws:kms
```

## Examples

### Example 1: Full module review
User says: "Review our Terraform modules"
Actions:
1. Discover all Terraform roots
2. Run 4-stage pipeline on each module
3. Aggregate results
Result: Comprehensive report with compliance and security findings

### Example 2: PR-scoped review
User says: "Check Terraform changes in this diff"
Actions:
1. Identify changed `.tf` files from git diff
2. Determine affected root modules
3. Run validation and scanning on affected modules
Result: Focused report on changed infrastructure

## Error Handling

| Error | Action |
|-------|--------|
| terraform not installed | Report SKIPPED for Terraform stages; suggest `brew install terraform` |
| terraform init required | Run `terraform init -backend=false` before validate; if init fails, report and skip plan |
| Checkov/tfsec not found | Report SKIPPED for static analysis; suggest `pip install checkov` and `brew install tfsec` |
| state file locked | Skip plan stage; note "State locked" in report; suggest retry or manual unlock |
| provider auth failure | Skip plan stage; validation and static analysis still run; note auth issue in report |

## Troubleshooting

### terraform init fails
Cause: Provider plugins unavailable or version constraints conflict
Solution: Run with `-backend=false` to skip remote state; validation still checks syntax

### Checkov false positives
Cause: Custom conventions not matching CIS benchmarks
Solution: Use `.checkov.yaml` skip list or inline `#checkov:skip=CKV_AWS_XX` comments
