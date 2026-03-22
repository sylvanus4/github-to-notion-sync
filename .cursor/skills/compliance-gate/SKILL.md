---
name: compliance-gate
description: >-
  Unified compliance quality gate that aggregates secret scanning, SAST
  (Bandit/Semgrep), dependency CVEs, IaC policy violations, and SBOM
  generation into a single compliance report with pass/fail per standard
  (SOC2, ISO27001, CIS). Use when the user asks to "run compliance check",
  "compliance gate", "security compliance scan", "컴플라이언스 게이트",
  "보안 컴플라이언스", "compliance-gate", or needs unified compliance
  validation before deployment. Do NOT use for code quality review (use
  deep-review), individual dependency audits (use dependency-auditor),
  or IaC validation only (use iac-review-agent).
metadata:
  version: "1.0.0"
  category: "review"
  author: "thaki"
---
# Compliance Gate

Unified compliance validation combining multiple security and policy checks into a single pass/fail report mapped to compliance frameworks.

## When to Use

- Before production deployments (mandatory gate)
- As part of the `release-commander` pipeline
- For periodic compliance audits
- When preparing for SOC2/ISO27001 certification

## Compliance Frameworks Covered

| Framework | Checks | Source |
|-----------|--------|--------|
| SOC2 Type II | Access control, logging, encryption, change mgmt | Checkov, custom rules |
| ISO 27001 | Information security controls | tfsec, KubeLinter |
| CIS Benchmarks | K8s, Docker, AWS/Azure hardening | kube-score, Checkov |
| OWASP Top 10 | Application security vulnerabilities | Semgrep, Bandit |
| Supply Chain | Dependency integrity, SBOM, provenance | Syft, Grype |

## Workflow

### Step 1: Secret Scanning

Scan for exposed secrets in code and configuration:

```bash
gitleaks detect --source . --report-format json --report-path /tmp/secrets.json
```

Checks: API keys, passwords, tokens, private keys, connection strings.

### Step 2: Static Application Security Testing (SAST)

**Python** (Bandit + Semgrep):
```bash
bandit -r . -f json -o /tmp/bandit.json
semgrep scan --config auto --json --output /tmp/semgrep.json
```

**Go** (gosec):
```bash
gosec -fmt json -out /tmp/gosec.json ./...
```

**Frontend** (eslint-plugin-security):
```bash
npx eslint --plugin security --format json -o /tmp/eslint-security.json
```

### Step 3: Dependency Vulnerability Scan

```bash
pip-audit --format json --output /tmp/pip-audit.json
npm audit --json > /tmp/npm-audit.json
go list -json -m all | nancy sleuth > /tmp/nancy.json
```

### Step 4: IaC Policy Validation

Delegate to `iac-review-agent` for:
- Helm chart policy checks (kube-score)
- Terraform compliance (Checkov)
- K8s manifest security (KubeLinter)

### Step 5: SBOM Generation

Generate Software Bill of Materials:

```bash
syft . -o spdx-json > /tmp/sbom.spdx.json
grype sbom:/tmp/sbom.spdx.json -o json > /tmp/grype.json
```

### Step 6: Map to Compliance Frameworks

Map each finding to applicable compliance controls:

| Finding | SOC2 | ISO27001 | CIS | OWASP |
|---------|------|----------|-----|-------|
| Hardcoded API key | CC6.1 | A.9.4.3 | — | A02 |
| No encryption at rest | CC6.7 | A.10.1.1 | 4.1.1 | A02 |
| SQL injection | CC6.6 | A.14.2.5 | — | A03 |
| Missing resource limits | — | — | 5.2.1 | — |
| Outdated dependency | CC7.1 | A.12.6.1 | — | A06 |

### Step 7: Generate Report

```
Compliance Gate Report
======================
Date: 2026-03-19
Branch: issue/123-add-auth
Compliance Target: SOC2 Type II + CIS K8s

OVERALL: FAIL (2 critical findings)

Stage                    Status    Findings
──────────────────────── ───────── ──────────
Secret Scan              PASS      0 secrets
SAST (Python)            WARN      2 medium (SQL parameterization)
SAST (Go)                PASS      0 findings
SAST (Frontend)          PASS      0 findings
Dependency CVEs          FAIL      1 critical (jsonwebtoken CVE-2024-XXXX)
IaC Policy               WARN      3 medium (missing probes)
SBOM                     PASS      Generated (247 components)

CRITICAL FINDINGS (must fix):
1. [CVE-2024-XXXX] jsonwebtoken 8.x — Remote code execution
   Control: SOC2 CC7.1, ISO27001 A.12.6.1
   Fix: Upgrade to jsonwebtoken >= 9.0.0

COMPLIANCE MAPPING:
SOC2 Type II:  14/16 controls passing (87%)
CIS K8s 1.28:  22/25 checks passing (88%)
ISO 27001:     Partial — 2 controls need attention
```

## Error Handling

| Error | Action |
|-------|--------|
| Security scanner (gitleaks, bandit, semgrep) not installed | Skip that stage; report missing tool in summary; suggest install command |
| SBOM generation fails (syft/grype error) | Continue other stages; mark SBOM as FAIL in report; log raw error for debugging |
| CVE database outdated or unreachable | Use cached data if available; warn in report; recommend `grype db update` |
| IaC validator returns no results (empty diff) | Treat as PASS; note "no IaC files in scope" if no Helm/Terraform/K8s manifests found |
| Report generation fails (template or write error) | Emit findings to stdout as fallback; retry report write once; log failure path |

## Examples

### Example 1: Pre-deployment gate
User says: "Run compliance gate before deploy"
Actions:
1. Execute all 6 scan stages
2. Map findings to compliance frameworks
3. Generate report with pass/fail per standard
Result: Compliance report determining deploy readiness

### Example 2: Audit preparation
User says: "Generate compliance report for SOC2 audit"
Actions:
1. Full scan with SOC2 control focus
2. Generate detailed control mapping
3. Produce evidence artifacts (SBOM, scan results)
Result: Audit-ready compliance evidence package
