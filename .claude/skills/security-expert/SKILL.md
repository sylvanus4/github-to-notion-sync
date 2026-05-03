---
name: security-expert
description: >-
  Perform threat modeling (STRIDE), vulnerability assessments (OWASP Top 10), secret
  detection, LLM/AI-specific security checks, and PII handling reviews. Supports daily
  (quick scan) and comprehensive (full audit) modes with 8/10 confidence gate and
  exploit verification. Use when reviewing code for security, modeling threats, or
  auditing secrets.
---

# Security Expert

Security review skill for a Go/Python microservices platform with LLM inference, RAG, PII handling, and multi-tenant architecture.

## Scan Modes

| Mode | Trigger | Scope | Duration |
|------|---------|-------|----------|
| `daily` (default) | `/security-expert` | Changed files, secret scan, OWASP quick checks | ~2 min |
| `comprehensive` | `/security-expert comprehensive` | Full STRIDE + OWASP + LLM security + PII + deps | ~10 min |

## Confidence Gate (8/10)

- **8-10**: Report with severity and fix recommendation
- **5-7**: Log internally, surface only with `--show-low-confidence`
- **1-4**: Discard (filter test fixtures, allowlisted patterns, placeholders)

## Exploit Verification

For Critical/High findings (confidence >= 8):
1. Construct a proof-of-concept demonstrating the vulnerability
2. For injection: craft test payload and trace through code
3. For auth bypass: trace auth chain to confirm gap is reachable
4. Mark as **Verified** (PoC works) or **Theoretical** (plausible but unconfirmed)

## Threat Modeling (STRIDE)

| Threat | Question |
|--------|----------|
| **S**poofing | Can an attacker impersonate a user/service? |
| **T**ampering | Can data be modified in transit/at rest? |
| **R**epudiation | Can actions be denied without evidence? |
| **I**nformation Disclosure | Can sensitive data leak? |
| **D**enial of Service | Can the service be overwhelmed? |
| **E**levation of Privilege | Can a user gain unauthorized access? |

## OWASP Top 10 Checklist

- [ ] A01 Broken Access Control: RBAC, tenant isolation, CORS
- [ ] A02 Cryptographic Failures: TLS, password hashing, secrets not in code
- [ ] A03 Injection: parameterized queries, command injection, template injection
- [ ] A04 Insecure Design: threat model, rate limiting
- [ ] A05 Security Misconfiguration: debug mode, default credentials
- [ ] A06 Vulnerable Components: dependency scanning
- [ ] A07 Auth Failures: JWT validation, session management
- [ ] A08 Data Integrity: CI/CD integrity, dependency pinning
- [ ] A09 Logging & Monitoring: security event logging
- [ ] A10 SSRF: URL validation, egress filtering

## LLM/AI-Specific Checks

- [ ] Prompt injection filtering (system/user prompt boundary)
- [ ] Model output sanitization before rendering
- [ ] RAG context injection prevention
- [ ] PII redaction in LLM inputs/outputs
- [ ] Rate limiting on inference endpoints
- [ ] Model access control (per-tenant model permissions)

## Output Format

```markdown
## Security Review Report

### Mode: [daily/comprehensive]
### Scan Date: [date]

### Critical Findings
[verified exploits requiring immediate action]

### High Findings
[significant vulnerabilities]

### Medium Findings
[best practice violations]

### Recommendations
[prioritized action items]

### Compliance Notes
[regulatory implications if any]
```

## Test Invocation

```
/security-expert
/security-expert comprehensive
```
