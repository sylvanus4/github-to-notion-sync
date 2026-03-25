# Eval Criteria: ux-copy-audit

## Binary Evals

EVAL 1: File-Line References
Question: Does the audit report include specific file paths and line numbers (or component keys) for each finding?
Pass condition: Every finding has a traceable location reference (file:line or component.key format)
Fail condition: Findings described vaguely without locatable references

EVAL 2: Severity Classification
Question: Is each finding classified with a severity level (Critical/High/Medium/Low)?
Pass condition: Every finding has an explicit severity label with consistent classification criteria
Fail condition: Findings listed without severity, or severity assigned inconsistently

EVAL 3: Policy Linkage
Question: Are policy violations linked to the specific policy rule or guideline being violated?
Pass condition: Each policy-related finding cites the rule name, section, or convention being breached
Fail condition: Findings say "violates policy" without specifying which policy or rule

EVAL 4: Actionable Fix Suggestions
Question: Does every finding include a concrete, implementable fix suggestion?
Pass condition: Each finding has a specific suggestion the developer can directly apply
Fail condition: Findings only describe the problem without suggesting how to fix it

## Test Scenarios

1. "Audit UI strings in the cloud dashboard for tone consistency"
2. "Scan this React component file for hardcoded strings and i18n compliance"
3. "Check all error messages against our UX writing policy"
4. "Audit tooltip texts across the settings page for clarity and completeness"
