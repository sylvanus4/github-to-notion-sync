---
name: security-expert
description: >-
  Perform threat modeling (STRIDE), vulnerability assessments (OWASP Top 10),
  secret detection, LLM/AI-specific security checks, and PII handling reviews.
  Supports daily (quick scan) and comprehensive (full audit) modes with 8/10
  confidence gate and exploit verification. Use when the user asks for a
  security review, threat model, vulnerability scan, or secret audit. Do NOT
  use for data governance or regulatory compliance documentation (use
  compliance-governance) or dependency CVE scanning only (use
  dependency-auditor). Korean triggers: "보안", "감사", "리뷰", "체크".
metadata:
  version: "1.1.0"
  category: "review"
  author: "thaki"
---
# Security Expert

Procedural security skill for a FastAPI microservices platform with LLM inference, RAG, PII redaction, and multi-tenant architecture.

## Scan Modes

| Mode | Trigger | Scope | Duration |
|------|---------|-------|----------|
| `daily` | `/security daily` or default | Changed files only (git diff), secret scan, OWASP quick checks | ~2 min |
| `comprehensive` | `/security comprehensive` or `/security full` | Full STRIDE + OWASP Top 10 + LLM security + PII review + dependency scan | ~10 min |

Default mode is `daily` for fast feedback. Use `comprehensive` before releases or after major architecture changes.

## Confidence Gate (8/10 Threshold)

Every finding must include a confidence score (1-10):

- **Confidence 8-10**: Report as a finding with severity and fix recommendation
- **Confidence 5-7**: Log internally, only surface if `--show-low-confidence` is set
- **Confidence 1-4**: Discard silently to prevent false positive noise

### False Positive Filtering

Before reporting, check each finding against:
1. **Known safe patterns**: Test fixtures, example values, commented-out code
2. **Project allowlist**: Patterns in `.gitleaksignore` or `security-allowlist.json`
3. **Context check**: Is the "secret" actually a hash, placeholder, or test value?

If a finding matches any filter, downgrade confidence to 4 (auto-discard).

## Exploit Verification

For Critical and High severity findings (confidence >= 8):
1. Attempt to construct a proof-of-concept (PoC) demonstrating the vulnerability
2. For injection findings: craft a test payload and trace its path through the code
3. For auth bypass: trace the auth chain to confirm the gap is reachable
4. Mark as **Verified** (PoC works) or **Theoretical** (plausible but unconfirmed)

Only **Verified** findings require immediate action. **Theoretical** findings are tracked for follow-up.

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
Mode: [daily / comprehensive]
Scope: [Component / Service / Full system]
Date: [YYYY-MM-DD]
Confidence Gate: 8/10 (filtered [N] low-confidence findings)

1. Threat Model (STRIDE) [comprehensive only]
   Component: [name]
   Threats identified: [N]
   - [S/T/R/I/D/E]: [Threat] → [Mitigation]

2. OWASP Top 10
   Compliance: [XX / 10 categories addressed]
   Critical findings:
   - [A0X]: [Finding] at [File:Line] (confidence: X/10, verified: ✓/✗) → [Fix]

3. LLM Security [comprehensive only]
   Services reviewed: [list]
   Findings:
   - [LLM0X]: [Finding] (confidence: X/10) → [Mitigation]

4. Secret Scan
   Files scanned: [N]
   Secrets found: [N] (after false positive filtering)
   False positives filtered: [N]
   - [File:Line]: [Type] (confidence: X/10) → [Action: rotate + remove]

5. PII Handling [comprehensive only]
   Compliance: [Compliant / Gaps found]
   Gaps:
   - [Service]: [Issue] → [Fix]

6. Exploit Verification Summary
   Verified (PoC confirmed): [N]
   Theoretical (unconfirmed): [N]

7. Risk Summary
   Critical: [N] | High: [N] | Medium: [N] | Low: [N]
   Top 3 priority fixes:
   1. [Fix] — CVSS: [X.X] — [Verified/Theoretical]
   2. [Fix] — CVSS: [X.X] — [Verified/Theoretical]
   3. [Fix] — CVSS: [X.X] — [Verified/Theoretical]
```

## Additional Resources

For detailed OWASP checklists and LLM threat matrices, see [references/reference.md](references/reference.md).

## Verification Protocol

Before reporting any review or audit complete, verify findings with evidence:

```text
### Check: [what you are verifying]
**Command run:** [exact command executed]
**Output observed:** [actual output — copy-paste, not paraphrased]
**Result:** PASS or FAIL (with Expected vs Actual if FAIL)
```

A check without a command-run block is not a PASS — it is a skip.

Before issuing PASS: must include at least one adversarial probe (boundary input, concurrent request, missing data, permission edge case).

Before issuing FAIL: check if the issue is already handled elsewhere, intentional by design, or not actionable without breaking an external contract.

End verification with: `VERDICT: PASS`, `VERDICT: FAIL`, or `VERDICT: PARTIAL`.

## Honest Reporting

- Report review outcomes faithfully: if a check fails, say so with the relevant output
- Never claim "all checks pass" when output shows failures
- Never suppress or simplify failing checks to manufacture a green result
- When a check passes, state it plainly without unnecessary hedging
- The final report must accurately reflect what was found — not what was hoped

## Rationalization Detection

Recognize these rationalizations and do the opposite:

| Rationalization | Reality |
|----------------|---------|
| "The code looks correct based on my reading" | Reading is not verification. Run it. |
| "The implementer's tests already pass" | The implementer is an LLM. Verify independently. |
| "This is probably fine" | Probably is not verified. Run it. |
| "I don't have access to test this" | Did you check all available tools? |
| "This would take too long" | Not your call. Run the check. |
| "Let me check the code structure" | No. Start the server and hit the endpoint. |

If you catch yourself writing an explanation instead of running a command, stop. Run the command.
