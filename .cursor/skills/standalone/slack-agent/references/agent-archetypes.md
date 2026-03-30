# Agent Archetypes

Common Slack agent patterns for generating implementation plans in Phase 1.

## Support Agent

- **Purpose**: Answer questions from internal docs or knowledge base
- **Tools**: RAG search, ticket creation, document lookup
- **State**: Conversation history per thread
- **HITL**: Escalation to human agent
- **Example prompt**: "내부 문서에서 답변을 찾아주는 지원 봇"

## Standup Bot

- **Purpose**: Collect daily standup updates from team members
- **Tools**: DM collection, summary generation, channel posting
- **State**: Standup entries per user per day
- **HITL**: None (fully automated)
- **Cron**: Daily at 9am, collect responses, post summary at 10am
- **Example prompt**: "매일 아침 팀원들에게 스탠드업을 수집하는 봇"

## Ops/Incident Bot

- **Purpose**: Monitor alerts, create incidents, coordinate response
- **Tools**: PagerDuty/OpsGenie integration, channel creation, status updates
- **State**: Incident lifecycle tracking
- **HITL**: Approve incident escalation, close incident
- **Example prompt**: "인시던트 생성하고 대응을 조율하는 봇"

## Approval Workflow Bot

- **Purpose**: Route approval requests (PTO, expenses, access)
- **Tools**: Form submission, approval routing, status tracking
- **State**: Request status, approver chain
- **HITL**: Core functionality (approve/reject buttons via Block Kit)
- **Example prompt**: "승인 요청을 관리하는 워크플로우 봇"

## Onboarding Bot

- **Purpose**: Guide new hires through onboarding checklist
- **Tools**: Checklist tracking, channel invites, resource sharing
- **State**: Onboarding progress per user
- **HITL**: Manager approval for access requests
- **Example prompt**: "신규 입사자 온보딩을 안내하는 봇"

## Analytics Reporter

- **Purpose**: Generate and share reports on demand or scheduled
- **Tools**: Database queries, chart generation, Slack file upload
- **State**: Report history, scheduled report configs
- **HITL**: None
- **Cron**: Weekly/monthly report generation
- **Example prompt**: "주간 매출 리포트를 자동으로 공유하는 봇"

## Custom Agent Plan Template

When generating a plan for the user's specific use case:

```markdown
# Agent: [Name]

## Purpose
[One-sentence description]

## System Prompt
[Draft system prompt defining personality and constraints]

## Tools
### Built-in
- [ ] Read channel messages
- [ ] Fetch thread context
- [ ] Post messages / Block Kit

### Custom (to implement)
- [ ] [toolName]: [description]
- [ ] [toolName]: [description]

## State Requirements
- [What needs to persist across messages]

## Human-in-the-Loop
- [Actions requiring approval via Block Kit buttons]

## Cron Jobs
- [Scheduled tasks, if any]

## Architecture
- Framework: Bolt for JavaScript
- AI Provider: [Anthropic / OpenAI / etc.]
- Deployment: [Docker/K8s / Railway / Lambda / etc.]
- External APIs: [list]
```
