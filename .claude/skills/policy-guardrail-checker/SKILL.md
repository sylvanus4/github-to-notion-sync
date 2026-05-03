---
name: msp-policy-guardrail-checker
description: >-
  MSP tier-1 policy guardrail checker. Fan-out compliance and IaC/K8s
  validation into a unified violation report with optional PR-ready patches.
  Triggers (EN): policy guardrail check, governance check, compliance
  violation scan, policy enforcement. Triggers (KO): 정책 가드레일, 거버넌스 점검, 정책 위반
  검사, 컴플라이언스 체크. Does NOT apply live Terraform apply, mutate cloud resources,
  or auto-merge PRs; auto-fix is repo-only via proposed diffs. Use for static
  analysis of repo artifacts and customer policy profiles. Do NOT use for
  one-off compliance-gate without MSP context, or for live cluster mutation.
disable-model-invocation: true
---

# MSP Skill #7 — Policy Guardrail Checker

**Summary:** Unified multi-layer policy enforcement for managed service delivery. Takes tenant-scoped inputs (Terraform, Helm, raw Kubernetes manifests, optional customer policy profiles) and produces a single **violation report** with severities, evidence, fix suggestions, and **PR-ready patches**. Tier 1: automatic **detection and reporting**; remediation is **repository-only** (proposed code changes), never direct infrastructure mutation.

## Usage examples

- "Run a **policy guardrail check** on this release branch for tenant `acme` (AWS + EKS)."
- "**Governance check** on the diff since `main` — merge `compliance-gate` + IaC validators."
- "**정책 가드레일** 점검: 고객 프로필 `profiles/acme.yaml` 적용해서 위반 목록만."
- "**Compliance violation scan** before Tuesday RC — fan-out three checkers, one JSON report."
- "**Policy enforcement** report for `infrastructure/` and `deploy/helm/` with PR-ready fixes."

## Customer policy profiles

Per-tenant policies are **declarative** (JSON or YAML), versioned with the repo or loaded from a trusted path at invocation time.

**Typical fields:**

| Field | Purpose |
|-------|---------|
| `tenant_id` | Required scope for all evaluation and audit logs |
| `clouds` | e.g. `aws`, `gcp` — narrows cloud-specific rule hints |
| `severity_overrides` | Map rule id → `critical` / `high` / `medium` / `low` / `info` |
| `rule_packs` | Which named packs to enable (org baseline + customer add-ons) |
| `allowlist` / `denylist` | Resource patterns, namespaces, or rule ids to include or exclude |
| `custom_rules` | Optional inline or path-referenced checks (naming, labels, network policy presence) |

**Loading order:** default org profile → customer profile merge (later wins on conflicts) → CLI/skill parameters. Unknown keys are ignored with a warning in the run metadata.

## Pipeline overview (fan-out / fan-in)

**Fan-out — three parallel checker agents** (same input scope, independent execution):

1. **Agent A — Terraform / IaC policy** — routes through `iac-review-agent` → `terraform-reviewer` (and related IaC paths in diff or tree).
2. **Agent B — Kubernetes & Helm policy** — `iac-review-agent` → `helm-validator` + `k8s-manifest-validator` for chart and manifest paths.
3. **Agent C — Security & dependency baseline** — `compliance-gate` (secrets, SAST, CVEs, SBOM-style outputs) plus **custom profile rules** applied to merged findings.

**Fan-in:** Normalize all outputs to the **unified violation schema** (below), dedupe by `(resource, rule_id, file)`, apply **customer severity overrides**, sort by severity, attach **fix_suggestion** and **pr_ready_patch** where safe.

```text
                    ┌─────────────────────┐
                    │ Load profile + scope │
                    └──────────┬──────────┘
           ┌────────────────────┼────────────────────┐
           ▼                    ▼                    ▼
    ┌──────────────┐    ┌──────────────┐    ┌──────────────────┐
    │ Agent A      │    │ Agent B      │    │ Agent C          │
    │ Terraform/   │    │ Helm + K8s   │    │ compliance-gate  │
    │ IaC (router) │    │ validators   │    │ + custom rules   │
    └──────┬───────┘    └──────┬───────┘    └────────┬─────────┘
           │                   │                     │
           └───────────────────┼─────────────────────┘
                               ▼
                    ┌─────────────────────┐
                    │ Fan-in: merge,      │
                    │ dedupe, severities  │
                    └──────────┬──────────┘
                               ▼
                    ┌─────────────────────┐
                    │ Violation report +  │
                    │ optional PR patches │
                    └─────────────────────┘
```

**Composed validators (via iac-review-agent):** `helm-validator`, `k8s-manifest-validator` (and Terraform branch as applicable). **compliance-gate** covers the security/dependency plane in parallel.

## Detailed workflow

1. **Detect scope** — Branch, commit range, or paths; optional `tenant_id` and profile path.
2. **Load customer policy profile** — Merge defaults; validate required `tenant_id`.
3. **Fan-out (parallel)** — Invoke:
   - `compliance-gate` on the scoped tree (or CI-equivalent stages).
   - `iac-review-agent` on the same scope so Terraform / Helm / K8s files route to `helm-validator` and `k8s-manifest-validator` (and Terraform tools where present).
4. **Fan-in** — Map each source finding to the unified schema; apply overrides and allow/deny lists.
5. **Tier-1 fix generation** — For remediations that are **file edits only**, produce `pr_ready_patch` (unified diff hunks or file-scoped patch text). **Never** emit apply commands, live `kubectl` mutations, or Terraform apply.
6. **Output** — JSON report + human-readable summary (markdown) suitable for PR description or MSP ticket.
7. **Audit** — Log structured entry per `APPROVAL_BOUNDARY_SPEC` (correlation_id, tenant_id, tier=1, no cloud mutations).

## Output schema (violations)

Top-level object:

| Field | Type | Description |
|-------|------|-------------|
| `schema_version` | string | e.g. `1.0.0` |
| `tenant_id` | string | Customer tenant |
| `generated_at` | string | ISO 8601 |
| `summary` | object | Counts by severity, `pass` boolean if policy defines gates |
| `violations` | array | See row below |
| `metadata` | object | Profile hash, tool versions, scope paths |

**Each `violations[]` item:**

| Field | Type | Description |
|-------|------|-------------|
| `violation_id` | string | Stable id (e.g. hash of rule + resource + path) |
| `severity` | string | `critical` \| `high` \| `medium` \| `low` \| `info` |
| `resource` | string | Logical resource (e.g. `aws_s3_bucket.logs`, `Deployment/app`) |
| `file` | string | Repo-relative path |
| `rule` | string | Rule id and human name |
| `source` | string | `compliance-gate` \| `iac-review-agent` \| `helm-validator` \| `k8s-manifest-validator` \| `custom_profile` |
| `evidence` | string | Snippet, tool output, or line reference |
| `fix_suggestion` | string | One or more concrete remediation steps |
| `pr_ready_patch` | string \| null | **Unified diff** or patch block safe to open as PR; `null` if auto-fix not applicable or unsafe |

**Tier-1 rule:** `pr_ready_patch` may only change **version-controlled** configuration (Terraform, YAML, Helm values, manifests). It must not reference or imply live API calls to change infrastructure state.

## Composed skills orchestration

| Skill | Role in this skill |
|-------|-------------------|
| `compliance-gate` | Parallel **Agent C**: secrets, SAST, dependency CVEs, SBOM, framework mapping; feeds normalized violations. |
| `iac-review-agent` | **Router** for the IaC/Helm/K8s plane: detects file types in scope and runs `helm-validator`, `k8s-manifest-validator`, Terraform-oriented tools as applicable. |
| `helm-validator` | Chart lint, `helm template`, schema (kubeconform), policy (kube-score) — **Agent B** path. |
| `k8s-manifest-validator` | Kubeconform, KubeLinter, `kubectl` dry-run where applicable — **Agent B** path. |

**Orchestration note:** The implementing agent should call these skills in **parallel** for the same path scope, then run the **fan-in** merge. If a sub-skill is unavailable, record `source_error` in metadata and continue with partial results.

## Governance

- **Approval Tier:** Tier 1 — fully read-only, no human gate required.
- **Mutations:** None. This skill scans IaC files, Helm charts, and K8s manifests against policy rules; it generates proposed diffs but never applies them.
- **Prohibited:** Applying patches, modifying live infrastructure, committing changes, or bypassing policy violations.

## Related documents

- Planning: `docs/msp-skills/plans/policy-guardrail-checker.md`
- Approval model: `docs/msp-skills/APPROVAL_BOUNDARY_SPEC.md`
