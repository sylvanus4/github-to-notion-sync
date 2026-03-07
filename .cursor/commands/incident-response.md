## Incident Response

Orchestrated workflow for diagnosing and recovering from service failures — health check, root cause analysis, auto-fix, verification, and postmortem documentation.

### Usage

```
/incident-response [symptom description, e.g. "admin service returns 500" or "can't connect to database"]
```

### Workflow

1. Read the mission-control skill at `.cursor/skills/mission-control/SKILL.md`
2. Follow **WF-4: Incident Response** defined there
3. Execute sequentially (time-critical):

**Step 1: Triage**
- **service-health-doctor** (`.cursor/skills/service-health-doctor/SKILL.md`): Run full status check, identify all DOWN/UNHEALTHY services
- Categorize severity:
  - **P1 Critical**: Core services down (admin, call-manager, orchestration)
  - **P2 High**: AI/data services down (stt-pipeline, llm-inference, rag-engine)
  - **P3 Medium**: Channel services down (chat, email, sms)
  - **P4 Low**: Auxiliary services degraded (analytics, metering)

**Step 2: Root Cause Analysis (Parallel)**
Use Task subagents based on the affected component:
- **backend-expert** (`.cursor/skills/backend-expert/SKILL.md`): Analyze application-level errors, stack traces, async patterns
- **db-expert** (`.cursor/skills/db-expert/SKILL.md`): Check database connectivity, connection pool, migration state, locks

**Step 3: Auto-Recovery**
Apply fixes in order of safety (per service-health-doctor protocol):
1. Start missing Docker containers
2. Re-source environment variables
3. Reinstall dependencies
4. Restart crashed services
5. Clear stale locks or connections

Never perform destructive actions without user confirmation.

**Step 4: Verification**
- **service-health-doctor**: Re-run full status check
- Confirm previously DOWN services are now HEALTHY
- Verify the original symptom is resolved

**Step 5: Postmortem**
- **technical-writer** (`.cursor/skills/technical-writer/SKILL.md`): Generate a postmortem document with:
  - Timeline of events
  - Root cause
  - Fix applied
  - Prevention recommendations

### Output

```
Incident Response Report
========================
Incident: [symptom description]
Date: [YYYY-MM-DD HH:MM]
Severity: [P1/P2/P3/P4]
Duration: [time from detection to resolution]

Root Cause:
  [description of what went wrong]

Services Affected:
  [list of services and their status]

Actions Taken:
  1. [action] — result: [success/failed]
  2. [action] — result: [success/failed]

Current Status:
  [N]/[TOTAL] services healthy
  Original symptom: [Resolved / Partially resolved / Unresolved]

Prevention:
  1. [recommendation]
  2. [recommendation]
```
