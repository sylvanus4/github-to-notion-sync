---
name: sefo-governance
description: >-
  Manage Trusted Skill Governance (TSG) operations: sign skills with Ed25519
  cryptographic keys, verify provenance chains, check and update trust scores,
  scan for threats, apply differential privacy to statistics, and manage
  quarantine. Use when the user asks to "sign a skill", "verify provenance",
  "check trust scores", "generate keypair", "threat scan", "SEFO 거버넌스",
  "스킬 서명", "신뢰 점수", "위협 탐지", "프로비넌스 검증", or any trust and
  security operation on skills. Do NOT use for task routing (use sefo-orchestrator),
  federation sync (use sefo-federation), or general security review (use
  security-expert).
metadata:
  author: thaki
  version: "0.1.0"
  category: sefo
---

# SEFO Governance

Manage Trusted Skill Governance (TSG) for cryptographic integrity, Bayesian trust scoring, differential privacy, and threat detection across the skill ecosystem.

## Instructions

### Operations

#### 1. Generate Keypair
Create a new Ed25519 keypair for signing skills:
`POST /api/v1/sefo/tsg/keypair`

Returns `private_key_hex` and `public_key_hex`. Store the private key securely — it signs all skills from this orchestrator instance.

#### 2. Sign a Skill
After creating or modifying a skill, sign it to establish provenance:
`POST /api/v1/sefo/tsg/sign` with:
```json
{
  "skill_id": "<uuid>",
  "private_key_hex": "<hex>",
  "orchestrator_id": "local-instance"
}
```

This computes `Sign(sk, H(grammar_rule || composition_dag || version))` and extends the Merkle-linked provenance chain.

#### 3. Verify Skill Integrity
Before trusting a skill (especially from federation):
`POST /api/v1/sefo/tsg/verify` with:
```json
{
  "skill_id": "<uuid>",
  "public_key_hex": "<hex>"
}
```

Returns:
- `signature_valid`: Whether the Ed25519 signature matches
- `provenance_valid`: Whether the Merkle chain is intact
- `provenance_issues`: Specific chain integrity failures
- `threat_alerts`: Detected threats (poisoning, manipulation, etc.)

#### 4. Check Trust Scores
View Bayesian trust for peer-skill pairs:
`GET /api/v1/sefo/tsg/trust?peer_id=<uuid>`

Trust uses Beta-Binomial model: `Trust = alpha / (alpha + beta)`
- Fresh skills start at `Beta(1,1)` = 0.5
- Each successful validation: alpha += 1
- Each failure: beta += 1
- Convergence: O(1/sqrt(n)) (Proposition 3)

#### 5. Update Trust
Record validation outcomes:
`POST /api/v1/sefo/tsg/trust/update` with:
```json
{
  "peer_id": "<uuid>",
  "skill_id": "<uuid>",
  "success": true
}
```

#### 6. Apply Differential Privacy
Before sharing performance statistics with federation peers:
`POST /api/v1/sefo/tsg/privacy/noise` with `perf_stats` and `epsilon`.

Applies Laplace mechanism: `s_tilde = s + Lap(delta_s / epsilon)` to protect sensitive execution metrics.

#### 7. View Threat Alerts
Check recent security events:
`GET /api/v1/sefo/tsg/alerts`

Monitors 4 attack vectors:
- **Skill poisoning**: Quality drift detection via held-out validation
- **Metadata inference**: Enforced by DP module
- **Version manipulation**: Provenance chain verification
- **Sybil gossip**: Peer rate limiting and identity verification

### Quarantine Policy

Skills with trust score below 0.3 are quarantined:
- Extended validation before execution
- Flagged in composition graph
- Not shared via federation until trust recovers
- Requires manual review for promotion
