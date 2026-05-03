---
name: msp-terraform-module-generator
description: >-
  MSP skill that generates production-quality Terraform modules (HCL,
  structure, docs, examples) from natural-language infrastructure
  requirements. Produces complete module directories (main.tf, variables.tf,
  outputs.tf, versions.tf, README.md, examples/) locally, self-validates with
  terraform-reviewer (validate, plan dry-run, Checkov/tfsec), optionally runs
  policy-guardrail- checker, and can create a PR for review. Supports AWS and
  GCP providers. NEVER runs terraform apply or terraform destroy. Use when the
  user asks to generate terraform module, scaffold terraform, create IaC
  module, terraform from requirements, generate HCL from description, MSP
  terraform scaffold, create infrastructure module, or needs Terraform module
  generation from natural language. Do NOT use for reviewing existing
  terraform plans (use terraform-plan-reviewer), checking policy compliance
  only (use policy-guardrail-checker), executing terraform apply/destroy
  (prohibited), IaC drift detection (use argocd-drift-analyzer or
  infra-drift-detector), or runbook generation (use infra-runbook-generator).
  Korean triggers: 테라폼 모듈 생성, IaC 모듈 생성, 테라폼 스캐폴드, 인프라 코드 생성, 테라폼 생성.
disable-model-invocation: true
---

# MSP Terraform Module Generator

Generates production-quality Terraform modules from natural-language infrastructure requirements. Produces complete, reviewable module directories on disk. The maximum automated side effect is optional PR creation. **NEVER** runs `terraform apply`, `terraform destroy`, or any operation that mutates live cloud resources.

## Usage

```
/msp-terraform-module-generator --cloud aws "Create an S3 bucket with versioning, lifecycle (IA after 30d, expire 365d), SSE-S3, block public access, tags: Environment, Project, Owner"
/msp-terraform-module-generator --cloud gcp --naming-prefix "myapp" "VPC with custom subnet, private Google access, default firewall deny except IAP TCP 22, labels: environment, app"
/msp-terraform-module-generator --cloud aws --extend ./modules/existing-vpc "Add NAT Gateway and private route table"
/msp-terraform-module-generator --cloud gcp --policy-profile customer-strict --pr-target main "Cloud SQL with private IP and authorized networks"
```

## Prerequisites

- **Terraform CLI**: For `terraform validate` and `terraform fmt` during self-review.
- **Checkov / tfsec**: For security static analysis during self-review (via `terraform-reviewer`).
- **Git** (optional): Only needed if PR creation is requested.
- **Cloud credentials**: Not required for generation; only needed if `terraform plan` dry-run is configured against a sandbox.

## Governance

| Action | Tier | Notes |
|--------|------|-------|
| Generate Terraform files to local/sandbox path | **Tier 1** | Read/analyze + produce drafts stored locally |
| Create or update PR in team/customer repo | **Tier 2** | Human-in-the-loop before merge |
| `terraform apply` / `terraform destroy` | **Prohibited** | NEVER invoked by this skill |
| Policy bypass (skip guardrail checker when profile mandates it) | **Prohibited** | Must not evade org guardrails |

## Pipeline Overview

```
Natural Language Requirements
        ↓
1. Parse requirements + clarify ambiguities
        ↓
2. Determine cloud provider + resource types
        ↓
3. Generate module scaffolding (directory layout, versions.tf)
        ↓
4. Generate main.tf (resources, locals, data sources)
        ↓
5. Extract variables.tf + outputs.tf
        ↓
6. Generate README.md + examples/default.tfvars
        ↓
7. Self-review with terraform-reviewer (validate, plan, Checkov, tfsec)
        ↓ iterate until pass or document hard failures
8. Optional: policy-guardrail-checker (when policy profile provided)
        ↓
9. Optional: Create PR (Tier 2)
        ↓
Output: Complete Terraform module directory + generation report
```

## Detailed Workflow

1. **Parse requirements** — Extract target resources, constraints, and ambiguities from natural language. Ask follow-up questions if blocking details are missing (region, encryption default, network boundaries).

2. **Determine cloud and resources** — Identify provider (`aws` / `gcp`) and target resource types. Reject or scope unsupported combinations.

3. **Generate scaffolding** — Create directory layout with `versions.tf` containing `terraform` block and `required_providers` with version constraints.

4. **Generate `main.tf`** — Resources, `locals`, `data` sources. Follow cloud-specific patterns (see below). Modules only if consistent with single-module scope. No hardcoded account/project IDs.

5. **Extract `variables.tf` and `outputs.tf`** — From what `main.tf` needs. All public inputs have descriptions and types. Defaults only where safe. Outputs documented with descriptions.

6. **Generate `README.md` and `examples/default.tfvars`** — README includes purpose, inputs/outputs table, usage snippet. Example tfvars with safe placeholder values (no secrets).

7. **Self-review** — Run `terraform-reviewer` for `terraform validate`, `terraform fmt`, Checkov, and tfsec. Iterate on generated HCL until static stages pass or document hard failures. This is a mandatory gate.

8. **Optional policy check** — When a customer policy profile is supplied, run `policy-guardrail-checker`. Address or explicitly list waived items (waivers are human decisions, not automatic).

9. **Optional PR creation** — Create PR to specified repo/branch (Tier 2). Include generation report in PR body.

## Cloud-Specific Patterns

### AWS

- **Provider**: `hashicorp/aws` with version constraints; regional configuration via variables, not hardcoded.
- **Naming**: Consistent `name` / `name_prefix` patterns; S3 bucket global uniqueness; IAM naming that avoids collisions.
- **Tagging**: Single `var.tags` (map) merged with `default_tags`; support mandatory MSP/customer tag keys.
- **Common patterns**: VPC (subnets, IGW, NAT, routes), EC2 (launch template + ASG), S3 (encryption, public access block, lifecycle), RDS (subnet group, SG, storage encryption), least-privilege IAM roles (avoid `*`), KMS keys.

### GCP

- **Provider**: `hashicorp/google` / `google-beta` as needed; `project`, `region`, `zone` as variables.
- **Labels**: `var.labels` (map) aligned with org standards; avoid duplicating project ID in every label unless required.
- **Resource hierarchy**: Explicit `project` on resources; VPC and subnetwork patterns consistent with shared VPC or standalone.
- **Common patterns**: VPC + subnets + firewall rules, GCE (instance template / MIG), GCS (uniform access, encryption), Cloud SQL (private IP + authorized networks or PSC), IAM bindings with minimal roles (no `roles/owner` unless explicitly justified and still blocked by policy checker).

**Cross-cloud**: No provider-specific magic strings in `main.tf` for environment names — variables only for environment, region, and naming base.

## Output

### Module Directory Structure

```
<module-name>/
  main.tf
  variables.tf
  outputs.tf
  versions.tf
  README.md
  examples/
    default.tfvars
```

### Generation Report (optional, markdown or JSON)

- Provider and resource list
- Assumptions made
- Open questions
- terraform-reviewer findings (pass/fail per check)
- policy-guardrail-checker findings (if run)
- PR URL (if created)

## Composed Skills

| Skill | Role |
|-------|------|
| **terraform-reviewer** | Mandatory self-review: `terraform validate`, plan dry-run, Checkov, tfsec, structured pass/fail. Generator must not ship a "green" result if validate fails. |
| **policy-guardrail-checker** (Skill #7) | Optional organizational gate when customer policy profile is provided. Static policy compliance on generated module tree. |

**Order**: Generate → `terraform-reviewer` → (optional) `policy-guardrail-checker` → (optional) PR.

## Error Handling

- **Ambiguous requirements** — Ask clarifying questions before generation; do not guess at security-relevant defaults.
- **terraform validate failure** — Iterate on generated HCL (up to 3 attempts); if persistent failure, report with error details and stop.
- **Security findings** — Checkov/tfsec critical findings block PR creation; report findings with fix suggestions.
- **Unsupported provider/resource** — Reject with clear message about supported scope.
- **Hallucinated resource arguments** — `terraform validate` and `terraform plan` as hard gates; pin provider versions in `versions.tf`.

## Evaluation Criteria

| Criterion | Target |
|-----------|--------|
| `terraform validate` | 100% pass for shipped artifacts |
| `terraform plan` (dry-run) | Succeeds in sandbox where provider auth is available |
| Policy compliance | Zero unaddressed critical findings when policy profile is active |
| Code quality | No hardcoded secrets; minimal magic strings; variable descriptions on all public inputs |
| Documentation | README matches actual variables/outputs; example tfvars symmetric with `variables.tf` |

## Governance

- **Tier 1** for local generation; **Tier 2** for PR creation per `metadata.approval_spec`.
- `terraform apply` and `terraform destroy` are **PROHIBITED** in this skill. Operators may run them outside this skill under separate Tier 2+ governance.
- All generated code logs (inputs hash, output paths, PR URL) for audit.
- **English triggers**: `generate terraform`, `scaffold terraform`, `create IaC module`, `terraform from requirements`.
- **Korean triggers**: `테라폼 모듈 생성`, `IaC 모듈 생성`, `테라폼 스캐폴드`, `인프라 코드 생성`, `테라폼 생성`.
