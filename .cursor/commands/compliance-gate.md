---
description: "Run a unified compliance quality gate — SAST, CVE scan, IaC policy check, and SBOM generation with framework mapping"
---

## Compliance Gate

Unified compliance quality gate aggregating security and policy checks into a single pass/fail report.

### Usage

```
/compliance-gate                            # run all compliance checks
/compliance-gate --framework soc2           # map findings to SOC 2 controls
/compliance-gate --framework iso27001       # map findings to ISO 27001
/compliance-gate --skip-iac                 # skip IaC validation
/compliance-gate --sbom-only                # generate SBOM without other checks
```

### Execution

Read and follow the skill at `.cursor/skills/compliance-gate/SKILL.md`.

User input: $ARGUMENTS

1. Run SAST scans (gitleaks, bandit/semgrep/gosec, eslint-plugin-security)
2. Run CVE scans (pip-audit, npm audit, nancy sleuth)
3. Run IaC policy checks via iac-review-agent
4. Generate SBOM (syft) and vulnerability scan (grype)
5. Map findings to compliance framework controls
6. Generate consolidated compliance report with pass/fail verdict
