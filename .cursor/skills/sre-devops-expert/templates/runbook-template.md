# Runbook: [Incident/Procedure Title]

## Metadata

| Field | Value |
|-------|-------|
| Service | [service name] |
| Severity | [P1 / P2 / P3 / P4] |
| Author | [name] |
| Last updated | [YYYY-MM-DD] |
| Reviewers | [names] |

## Description

[Brief description of the incident scenario or operational procedure.]

## Detection

- **Alert name**: [alert rule name]
- **Source**: [Prometheus / Grafana / PagerDuty / manual]
- **Threshold**: [metric > X for Y minutes]
- **Dashboard**: [link to monitoring dashboard]

## Impact

- **User-facing**: [Yes / No] — [description of user impact]
- **Data integrity**: [At risk / Not affected]
- **Dependent services**: [list of affected downstream services]

## Prerequisites

- [ ] Access to Kubernetes cluster (`kubectl` configured)
- [ ] Access to PostgreSQL (via `psql` or admin tool)
- [ ] Access to monitoring dashboards
- [ ] Incident channel created in Slack

## Steps

### 1. Assess

```bash
# Check pod status
kubectl get pods -n <namespace> -l app=<service>

# Check recent logs
kubectl logs -n <namespace> deployment/<service> --tail=100

# Check metrics
curl -s http://<service>:PORT/health
```

### 2. Mitigate

```bash
# Option A: Restart pods
kubectl rollout restart deployment/<service> -n <namespace>

# Option B: Scale up
kubectl scale deployment/<service> --replicas=<N> -n <namespace>

# Option C: Rollback
kubectl rollout undo deployment/<service> -n <namespace>
```

### 3. Verify

- [ ] Health endpoint returns 200
- [ ] Error rate returns to baseline
- [ ] No new alerts firing
- [ ] Dependent services recovered

### 4. Communicate

- [ ] Update incident channel with status
- [ ] Notify stakeholders if user-facing
- [ ] Update status page if applicable

## Rollback Plan

If mitigation fails:

1. [Step 1]
2. [Step 2]
3. Escalate to [team/person]

## Post-Incident

- [ ] Create post-mortem document
- [ ] Identify root cause
- [ ] Create follow-up tickets for preventive measures
- [ ] Update this runbook with lessons learned
