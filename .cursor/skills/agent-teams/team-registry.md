# Agent Team Registry

8 multi-agent teams following the Hub-and-Spoke architecture. Each team has
one Coordinator (Hub) and 4-5 Expert Agents (Spokes) with explicit context
passing via `_workspace/{team}/` file-based handoff.

## Teams

| # | Team | Coordinator | Experts | Pattern | Trigger Examples |
|---|------|-------------|---------|---------|------------------|
| 1 | Research & Report | `research-report/coordinator` | research-expert, analysis-expert, writing-expert, reviewer-expert | Pipeline + review loop | "deep research with report", "연구 리포트" |
| 2 | Content Production | `content-production/coordinator` | topic-researcher, outline-architect, draft-writer, editor, platform-formatter | Pipeline + editor quality gate (≥80) | "create content", "콘텐츠 제작" |
| 3 | Strategic Intelligence | `strategic-intel/coordinator` | market-scanner, competitive-analyst, strategic-planner, risk-assessor, executive-brief-writer | Fan-out → fan-in → sequential | "strategic analysis", "전략 분석" |
| 4 | Incident Response | `incident-response/coordinator` | triage-agent, evidence-collector, root-cause-analyzer, fix-implementer, customer-comms-drafter | Severity-based routing + confidence gate | "incident response", "장애 대응" |
| 5 | Code Ship | `code-ship/coordinator` | code-reviewer-expert, security-auditor-expert, test-validator-expert, doc-updater-expert, pr-packager-expert | Fan-out (3 parallel) → quality gate → sequential | "ship code", "코드 출시" |
| 6 | Knowledge Builder | `knowledge-builder/coordinator` | source-collector, content-extractor, wiki-compiler, cross-linker, quality-auditor | Pipeline + gap-fill iteration (≥70 freshness) | "build knowledge base", "KB 구축" |
| 7 | Meeting Intelligence | `meeting-intel/coordinator` | transcript-analyzer, decision-extractor, action-tracker, summary-writer, distribution-agent | Parallel extraction → synthesis → distribute | "analyze meeting", "회의 분석" |
| 8 | Sales Deal | `sales-deal/coordinator` | account-researcher, competitive-intel-agent, proposal-drafter, security-qa-agent, deal-reviewer | Fan-out → pipeline + accumulated context | "prepare deal package", "딜 준비" |

## Architecture

```
.cursor/skills/agent-teams/{team-name}/
  coordinator/SKILL.md     — Hub: decomposes, dispatches, gates, loops
  {expert-name}/SKILL.md   — Spoke: focused role, strict I/O contract
```

### Shared Conventions

- **Context passing**: All accumulated outputs are passed explicitly in
  each `Task` tool `prompt` parameter.
- **File-based handoff**: Experts read/write to `_workspace/{team}/`.
- **Quality gates**: Coordinators score expert outputs before proceeding.
  Failures route back to the responsible expert (max 2 iterations).
- **Composable skills**: Experts compose existing project skills internally.

## How to Invoke

Invoke any team by reading its coordinator SKILL.md and following its protocol:

```
Read: .cursor/skills/agent-teams/{team}/coordinator/SKILL.md
```

The coordinator handles all expert dispatch, context management, and quality
gates internally.

## Relationship to Existing Skills

| Existing Skill | Agent Team Equivalent | Improvement |
|----------------|----------------------|-------------|
| `role-dispatcher` | Strategic Intel Team | Collaborative synthesis vs independent parallel |
| `engineering-harness` | Code Ship Team | Doc update agent + explicit quality routing |
| `kb-orchestrator` | Knowledge Builder Team | Quality auditor with gap-fill loop |
| `meeting-digest` | Meeting Intel Team | Parallel extraction + decision/action routing |
| `sales-agent-harness` | Sales Deal Team | Accumulated context passing + deal review |
| `incident-to-improvement` | Incident Response Team | Severity routing + confidence gating |
| `content-graph-produce` | Content Production Team | Editor quality gate + platform formatting |
| `paper-review` | Research & Report Team | Isolated review loop with reviewer agent |
