---
description: "Run pipeline skills in air-gap mode — route LLM calls to on-premises endpoints with approval gates and audit logging"
---

## Air Gap

Run any pipeline skill in air-gap mode with on-premises LLM routing and data exfiltration controls.

### Usage

```
/air-gap /today                             # run daily pipeline in air-gap mode
/air-gap /deep-review                       # run code review in air-gap mode
/air-gap /ship                              # run ship pipeline in air-gap mode
/air-gap --config .air-gap-config.json      # use custom endpoint configuration
/air-gap --approve-all                      # skip manual approval gates (use with caution)
```

### Execution

Read and follow the skill at `.cursor/skills/air-gap-orchestrator/SKILL.md`.

User input: $ARGUMENTS

1. Load air-gap configuration (endpoint URLs, model mappings, approval policies)
2. Intercept all LLM API calls and route to configured on-prem endpoints
3. Apply data classification — block sensitive data from leaving the network
4. Execute the target pipeline skill with air-gap routing active
5. Generate audit log of all LLM interactions (prompts, responses, routing decisions)
