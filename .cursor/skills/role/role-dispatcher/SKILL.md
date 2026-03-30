---
name: role-dispatcher
description: >
  Cross-role mission control that dispatches a given topic to all 12 role-perspective analyzer
  skills in parallel batches, collects results, invokes executive-briefing for CEO synthesis,
  and posts the final report to Slack #효정-할일. Orchestrates role-ceo, role-cto, role-pm,
  role-developer, role-ux-designer, role-security-engineer, role-cso, role-sales, role-hr,
  role-finance, role-data-scientist, role-trading-expert, and executive-briefing.
  Use when the user runs /role-dispatch, asks for "cross-role analysis", "직무별 분석",
  "종합 분석", "multi-perspective analysis", "all roles analyze", "12개 직무 관점",
  or wants comprehensive multi-role analysis of any business topic.
  Do NOT use for single-role analysis (use the specific role-{name} skill),
  general code review (use deep-review), or financial report generation (use today).
  Korean triggers: "직무별 분석", "종합 분석", "크로스롤 분석", "전 직무 관점".
metadata:
  author: "thaki"
  version: "1.1.0"
  category: "orchestration"
---

# Cross-Role Topic Analysis Dispatcher

Orchestrates a comprehensive multi-perspective analysis of any business topic by dispatching
to 12 role-specific analyzer skills, filtering by relevance, synthesizing into a CEO executive
briefing, and delivering results to Slack.

## Input Parsing

Extract from user input:
- **Topic** (required): The business topic to analyze
- **Scope constraints** (optional): Additional context or boundaries
- **Role whitelist** (optional): Analyze only specific roles (e.g., "CTO, PM, Security only")
- **Role blacklist** (optional): Skip specific roles (e.g., "skip HR, Finance")

## Orchestration Flow

### Step 1: Preparation

Create output directory:
```bash
mkdir -p outputs/role-analysis/{topic-slug}
```

Generate a topic slug from the topic (lowercase, hyphens, max 50 chars).

### Step 2: Fan-Out — Role Analysis (Parallel Batches)

Dispatch to role skills using Task tool subagents. Max 4 concurrent subagents.

**Batch 1** (parallel):
| # | Skill | Subagent Prompt |
|---|-------|-----------------|
| 1 | `role-ceo` | "Read .cursor/skills/role/role-ceo/SKILL.md. Analyze this topic from CEO perspective: {topic}. {scope}. Follow the skill instructions. Output structured Korean markdown. Start with relevance scoring. If score < 5, return only: '## 관련도: {N}/10\n관련 없음 — {brief reason}'" |
| 2 | `role-cto` | (same pattern with role-cto) |
| 3 | `role-pm` | (same pattern with role-pm) |
| 4 | `role-developer` | (same pattern with role-developer) |

Wait for Batch 1 to complete.

**Batch 2** (parallel):
| # | Skill | Subagent Prompt |
|---|-------|-----------------|
| 5 | `role-ux-designer` | (same pattern) |
| 6 | `role-security-engineer` | (same pattern) |
| 7 | `role-cso` | (same pattern) |
| 8 | `role-sales` | (same pattern) |

Wait for Batch 2 to complete.

**Batch 3** (parallel):
| # | Skill | Subagent Prompt |
|---|-------|-----------------|
| 9 | `role-hr` | (same pattern) |
| 10 | `role-finance` | (same pattern) |

Wait for Batch 3 to complete.

**Batch 4** (parallel):
| # | Skill | Subagent Prompt |
|---|-------|-----------------|
| 11 | `role-data-scientist` | (same pattern with role-data-scientist) |
| 12 | `role-trading-expert` | (same pattern with role-trading-expert) |

Wait for Batch 4 to complete.

### Subagent Template

For each role subagent, use this prompt template:

```
You are analyzing a business topic from the {ROLE_NAME} perspective.

**Topic**: {topic}
**Additional context**: {scope_constraints}

Instructions:
1. Read the skill file at .cursor/skills/role-{role}/SKILL.md
2. Follow the relevance criteria to score the topic (1-10)
3. If score >= 5: Execute the analysis pipeline described in the skill and produce
   the full output in Korean following the output format template
4. If score < 5: Return only the relevance score and a one-line reason

Write your analysis to: outputs/role-analysis/{topic-slug}/role-{role}.md

Return the relevance score and a 3-line summary of your analysis.
```

### Step 3: Collection & Filtering

After all batches complete:
1. Read each role's output file from `outputs/role-analysis/{topic-slug}/`
2. Parse relevance scores
3. Separate: relevant roles (score >= 5) and skipped roles (score < 5)
4. Log participation stats: "{N}/12 roles participated"

### Step 3.5: Cross-Role Consistency Gate

Before invoking executive-briefing, verify:
- [ ] At least 3 role analyses completed with score >= 5 (not just 2)
- [ ] All output files in `outputs/role-analysis/{topic-slug}/` are non-empty and contain the required sections (relevance score, analysis body, recommendations)
- [ ] No two role analyses contain directly contradicting recommendations without explanation (e.g., CTO says "delay launch" while Sales says "launch immediately" — flag for executive-briefing to address)
- [ ] Relevance score distribution is reasonable (not all identical scores, which suggests template copying)

If fewer than 3 roles participated, append a "⚠️ Limited Perspective Warning" note to the executive-briefing input indicating which perspectives are missing and why the analysis may be incomplete.

### Step 4: Synthesis — Executive Briefing

Invoke the `executive-briefing` skill:

```
Read .cursor/skills/role/executive-briefing/SKILL.md and follow its instructions.

Input documents are in outputs/role-analysis/{topic-slug}/.
The following roles produced analyses: {list of participating roles with scores}.
The following roles were not relevant: {list of skipped roles with scores}.

Topic: {topic}

Synthesize all role analyses into a CEO executive briefing following the skill's
output format. Generate both markdown and .docx outputs.
Save to: outputs/role-analysis/{topic-slug}/executive-briefing.md
```

### Step 5: Slack Delivery

Post to Slack `#효정-할일` channel (ID: `C0AA8NT4T8T`) using the Slack MCP tools:

1. **Main message**: CEO executive briefing summary
   ```
   📋 *CEO 종합 브리핑: {Topic}*
   📅 {date} | 참여 직무: {N}/12 | 종합 영향도: {level}

   *핵심 의사결정*: {one-line decision}

   *합의 사항*:
   • {agreement 1}
   • {agreement 2}

   *우선 액션 아이템*:
   1. {action 1} — {owner} ({deadline})
   2. {action 2} — {owner} ({deadline})
   3. {action 3} — {owner} ({deadline})
   ```

2. **Thread replies** (one per participating role):
   ```
   *{Role Name} 관점* (관련도: {N}/10)
   {3-5 bullet summary from that role's analysis}
   ```

3. **File upload**: .docx executive briefing attachment (if generated)

### Step 6: Summary Report

Print a completion report:
```
## Cross-Role Analysis Complete

**Topic**: {topic}
**Participating roles**: {N}/12
- {role1} ({score}/10): {one-line summary}
- {role2} ({score}/10): {one-line summary}
- ...

**Skipped roles**: {list with scores}

**Output files**:
- outputs/role-analysis/{topic-slug}/role-{name}.md (per role)
- outputs/role-analysis/{topic-slug}/executive-briefing.md
- outputs/role-analysis/{topic-slug}/executive-briefing.docx

**Slack**: Posted to #효정-할일 with {N+1} messages (main + {N} thread replies)
```

## Error Handling

- If a role subagent fails, log the error and continue with remaining roles
- If fewer than 2 roles are relevant, warn the user that the topic may be too narrow
- If executive-briefing synthesis fails, post individual role summaries to Slack instead
- If Slack posting fails, save all outputs locally and inform the user

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| Relevance threshold | 5 | Minimum score (1-10) for full analysis |
| Max concurrent subagents | 4 | Parallel subagent limit per batch |
| Slack channel | `#효정-할일` (C0AA8NT4T8T) | Delivery channel |
| Output directory | `outputs/role-analysis/` | Base output path |

## Example

**User**: `/role-dispatch New GPU inference service launch for enterprise customers`

**Execution**:
1. Topic slug: `gpu-inference-service-launch`
2. Batch 1: CEO (9/10), CTO (9/10), PM (8/10), Developer (9/10) — all relevant
3. Batch 2: UX (7/10), Security (8/10), CSO (9/10), Sales (9/10) — all relevant
4. Batch 3: HR (5/10), Finance (8/10) — both relevant
5. Batch 4: Data Scientist (8/10), Trading Expert (3/10) — DS relevant, Trading skipped
6. Result: 11/12 roles participated
7. Executive briefing generated with SCQA analysis
8. Slack: 12 messages (1 main + 11 thread replies + .docx upload)
