---
name: security-expert
description: >-
  Perform threat modeling (STRIDE), vulnerability assessments (OWASP Top 10),
  secret detection, LLM/AI-specific security checks, and PII handling reviews.
  Use when the user asks for a security review, threat model, vulnerability
  scan, or secret audit. Do NOT use for data governance or regulatory compliance
  documentation (use compliance-governance) or dependency CVE scanning only (use
  dependency-auditor). Korean triggers: "보안", "감사", "리뷰", "체크".
metadata:
  version: "1.0.0"
  category: "review"
  author: "thaki"
---
# Security Expert

Procedural security skill for a FastAPI microservices platform with LLM inference, RAG, PII redaction, and multi-tenant architecture.

## Threat Modeling (STRIDE)

For each component or feature under review, evaluate:

| Threat | Question | Example in this system |
|--------|----------|----------------------|
| **S**poofing | Can an attacker impersonate a user/service? | JWT forgery, service-to-service auth bypass |
| **T**ampering | Can data be modified in transit/at rest? | WebSocket message injection, DB record tampering |
| **R**epudiation | Can actions be denied without evidence? | Missing audit logs in admin service |
| **I**nformation Disclosure | Can sensitive data leak? | PII in logs, model config in error responses |
| **D**enial of Service | Can the service be overwhelmed? | Unbounded file upload, missing rate limits |
| **E**levation of Privilege | Can a user gain unauthorized access? | Tenant isolation bypass, role escalation |

## OWASP Top 10 Checklist

- [ ] **A01 Broken Access Control**: Verify RBAC enforcement, tenant isolation, CORS policy
- [ ] **A02 Cryptographic Failures**: TLS everywhere, passwords hashed (bcrypt/argon2), secrets not in code
- [ ] **A03 Injection**: SQL (parameterized queries), command injection, template injection
- [ ] **A04 Insecure Design**: Threat model exists, abuse cases considered, rate limiting
- [ ] **A05 Security Misconfiguration**: Debug mode off in production, default credentials removed
- [ ] **A06 Vulnerable Components**: Dependencies scanned (`pip audit`, `npm audit`), CVE monitoring
- [ ] **A07 Auth Failures**: JWT validation (expiry, audience, issuer), session management
- [ ] **A08 Data Integrity Failures**: CI/CD pipeline integrity, dependency pinning, signed artifacts
- [ ] **A09 Logging & Monitoring Failures**: Security events logged, alerting on anomalies
- [ ] **A10 SSRF**: URL validation for external calls, blocklist for internal IPs

## LLM / AI Security (OWASP Top 10 for LLM)

Critical for `llm-inference`, `rag-engine`, `stt-pipeline`, `nlp-state`:

- [ ] **LLM01 Prompt Injection**: Input sanitization, system prompt protection, output filtering
- [ ] **LLM02 Sensitive Info Disclosure**: PII scrubbing before LLM calls, output scanning
- [ ] **LLM05 Improper Output Handling**: Validate/escape LLM output before rendering or executing
- [ ] **LLM06 Excessive Agency**: Limit tool/API access scope, require approval for destructive actions
- [ ] **LLM08 Vector DB Security**: Access control on Qdrant collections, embedding integrity
- [ ] **LLM09 Misinformation**: RAG retrieval quality checks, confidence thresholds

## Secret Detection

### Scan Targets

- Source code: API keys, passwords, tokens in `.py`, `.go`, `.ts`, `.env` files
- Git history: `git log -p | grep -i 'password\|secret\|api_key\|token'`
- Docker images: Inspect layers for leaked build args
- Config files: `docker-compose.yml`, `alembic.ini`, Helm values

### Patterns to Flag

```
AWS_ACCESS_KEY_ID=AKIA...
OPENAI_API_KEY=sk-...
DATABASE_URL=postgresql://user:password@host/db
JWT_SECRET=hardcoded-value
Bearer [A-Za-z0-9\-._~+/]+=*
```

### Recommended Tools

- `gitleaks` for git history scanning
- `trufflehog` for comprehensive secret detection
- `pip audit` / `safety` for Python dependency CVEs
- `npm audit` for Node dependency CVEs

## PII Handling Review

Relevant services: `pii-redaction` (8021), `stt-pipeline` (8011), `summary-crm` (8016)

- [ ] PII detected and masked before storage
- [ ] PII never logged in plaintext
- [ ] PII redaction applied before LLM inference
- [ ] Data retention policies enforced (auto-delete after period)
- [ ] PII access requires elevated permissions + audit trail

## Examples

### Example 1: Security review for a new service
User says: "Review the chat-channel service for security"
Actions:
1. Apply STRIDE threat model to the service
2. Check OWASP Top 10 compliance (access control, injection, auth)
3. Scan for secrets and PII handling issues
Result: Security Review Report with threat model and prioritized findings

### Example 2: Secret audit
User says: "Check if there are any leaked secrets in the codebase"
Actions:
1. Run gitleaks on the repository
2. Scan git history for secret patterns
3. Check Docker images and config files
Result: Secret scan results with rotation recommendations

## Troubleshooting

### gitleaks not installed
Cause: Tool not available on the system
Solution: Install via `brew install gitleaks` (macOS) or download from GitHub releases

### False positive secrets
Cause: Test fixtures or example values flagged as secrets
Solution: Add patterns to `.gitleaksignore` for known false positives

## Output Format

```
Security Review Report
======================
Scope: [Component / Service / Full system]
Date: [YYYY-MM-DD]

1. Threat Model (STRIDE)
   Component: [name]
   Threats identified: [N]
   - [S/T/R/I/D/E]: [Threat] → [Mitigation]

2. OWASP Top 10
   Compliance: [XX / 10 categories addressed]
   Critical findings:
   - [A0X]: [Finding] at [File:Line] → [Fix]

3. LLM Security
   Services reviewed: [list]
   Findings:
   - [LLM0X]: [Finding] → [Mitigation]

4. Secret Scan
   Files scanned: [N]
   Secrets found: [N]
   - [File:Line]: [Type] → [Action: rotate + remove]

5. PII Handling
   Compliance: [Compliant / Gaps found]
   Gaps:
   - [Service]: [Issue] → [Fix]

6. Risk Summary
   Critical: [N] | High: [N] | Medium: [N] | Low: [N]
   Top 3 priority fixes:
   1. [Fix] — CVSS: [X.X]
   2. [Fix] — CVSS: [X.X]
   3. [Fix] — CVSS: [X.X]
```

## Additional Resources

For detailed OWASP checklists and LLM threat matrices, see [references/reference.md](references/reference.md).
