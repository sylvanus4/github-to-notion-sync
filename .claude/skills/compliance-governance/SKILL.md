---
name: compliance-governance
description: >-
  Review data classification, access control policies, audit logging, and
  regulatory compliance documentation. Use when the user asks about data
  governance, compliance audits, access control reviews, GDPR, SOC2, or policy
  documentation. Do NOT use for vulnerability scanning or threat modeling (use
  security-expert) or general code review (use backend-expert). Korean
  triggers: "감사", "리뷰", "스캔", "보안".
---

# Compliance & Governance

Review governance posture for a multi-tenant SaaS platform with LLM/AI capabilities. Key services: `admin` (8018), `pii-redaction` (8021), `analytics` (8022).

## Data Classification

### Classification Levels

| Level | Definition | Examples in this system | Handling |
|-------|-----------|----------------------|---------|
| **Restricted** | Regulatory/legal protection required | PII, call recordings, auth tokens | Encrypted at rest + transit, access logged, retention enforced |
| **Confidential** | Business-sensitive | Tenant configs, model parameters, analytics | Encrypted at rest, role-restricted access |
| **Internal** | Internal use only | Service logs, deployment configs | Access restricted to team, no public exposure |
| **Public** | No restrictions | API docs, public-facing UI content | No special handling |

### Review Checklist

- [ ] Each data store has a classification label
- [ ] Restricted data encrypted at rest (PostgreSQL TDE or column-level)
- [ ] Restricted data encrypted in transit (TLS 1.2+)
- [ ] Data classification documented per service

## Access Control Review

### RBAC Audit

- [ ] Roles defined and documented (admin, manager, agent, viewer)
- [ ] Role assignments follow least-privilege principle
- [ ] Service-to-service auth uses mTLS or signed tokens (not shared secrets)
- [ ] API endpoints enforce authorization (not just authentication)
- [ ] Admin endpoints restricted to admin role only
- [ ] Tenant isolation enforced at data layer (not just API layer)

### Privilege Escalation Checks

- [ ] No API allows self-promotion to higher role
- [ ] Role changes require admin approval + audit log
- [ ] Service accounts have scoped permissions (not superuser)
- [ ] Database credentials per-service (not shared root password)

## Audit Logging

### What Must Be Logged

| Event category | Examples | Required fields |
|---------------|---------|----------------|
| Authentication | Login, logout, token refresh, failed auth | user_id, ip, timestamp, result |
| Authorization | Access denied, role check | user_id, resource, action, result |
| Data access | PII viewed, report exported | user_id, resource_id, action |
| Admin actions | User created/deleted, config changed | actor_id, target, before/after |
| System events | Service start/stop, migration run | service, event, timestamp |

### Audit Log Checklist

- [ ] Audit logs are immutable (append-only, separate from app logs)
- [ ] Logs include `who`, `what`, `when`, `where`, `result`
- [ ] Logs shipped to centralized system (ELK, CloudWatch, Loki)
- [ ] Log retention meets regulatory requirements (e.g., 1 year minimum)
- [ ] Logs do NOT contain sensitive data (passwords, tokens, PII in plaintext)
- [ ] Log access restricted to security/compliance team

## Data Retention

### Policy Template

| Data type | Retention period | Deletion method | Legal basis |
|-----------|-----------------|-----------------|-------------|
| Call recordings | 90 days | Auto-delete job | Contractual |
| STT transcripts | 90 days | Cascade from call delete | Contractual |
| User accounts | Account lifetime + 30 days | Soft-delete then hard-delete | Consent |
| Audit logs | 1 year | Archive to cold storage | Regulatory |
| Analytics aggregates | 2 years | N/A (anonymized) | Legitimate interest |

### Checklist

- [ ] Retention periods documented per data type
- [ ] Automated deletion jobs scheduled and monitored
- [ ] Deletion is verifiable (not just soft-delete forever)
- [ ] Backup retention aligns with data retention policy

## Examples

### Example 1: Full compliance audit
User says: "Run a compliance audit on the platform"
Actions:
1. Review data classification labels across all data stores
2. Audit RBAC enforcement and tenant isolation
3. Check audit logging coverage and retention policies
Result: Compliance & Governance Report with gap analysis and priority fixes

### Example 2: GDPR readiness check
User says: "Are we GDPR compliant?"
Actions:
1. Check PII handling and data classification
2. Verify data retention and deletion automation
3. Review consent management and access logging
Result: Regulatory alignment assessment with specific remediation items

## Troubleshooting

### Missing data classification labels
Cause: New data stores added without classification
Solution: Review each store and assign a classification level (Restricted/Confidential/Internal/Public)

### Audit logs contain PII
Cause: Logging middleware captures request bodies with sensitive data
Solution: Add PII scrubbing to the logging pipeline before storage

## Output Format

```
Compliance & Governance Report
==============================
Scope: [Service / Data store / Full system]
Date: [YYYY-MM-DD]

1. Data Classification
   Stores reviewed: [N]
   Unclassified: [N]
   Issues:
   - [Store]: [Missing classification / Incorrect handling]

2. Access Control
   Roles defined: [N]
   RBAC coverage: [XX%]
   Issues:
   - [Endpoint/Service]: [Issue] → [Fix]

3. Audit Logging
   Coverage: [XX% of required events]
   Gaps:
   - [Event type]: [Not logged] → [Implement in service X]

4. Data Retention
   Policies documented: [XX% of data types]
   Automated deletion: [Active / Not configured]
   Issues:
   - [Data type]: [No retention policy] → [Recommended: X days]

5. Compliance Summary
   Regulatory alignment: [GDPR / SOC2 / HIPAA / N/A]
   Open items: [N]
   Priority:
   1. [Item] — [Risk: High]
   2. [Item] — [Risk: Medium]
```
