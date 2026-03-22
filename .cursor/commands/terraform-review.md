---
description: "Review Terraform modules with validate, plan analysis, Checkov/tfsec security scan, and LLM HCL review"
---

## Terraform Review

Review Terraform modules through a 4-stage pipeline: validate → plan → security scan → LLM review.

### Usage

```
/terraform-review <module-path>              # review a specific module
/terraform-review infra/terraform/           # review all modules in directory
/terraform-review --plan-only                # skip security scanners, analyze plan output only
```

### Execution

Read and follow the skill at `.cursor/skills/terraform-reviewer/SKILL.md`.

User input: $ARGUMENTS

1. Parse the module path from arguments (default: scan for `*.tf` files)
2. Run the 4-stage pipeline per the skill workflow
3. Present the consolidated report with findings by severity
