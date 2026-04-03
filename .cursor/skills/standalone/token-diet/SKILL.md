---
name: token-diet
description: >-
  Diagnose per-turn token consumption from always-applied rules, AGENTS.md,
  MEMORY.md, MCP server schemas, and skill descriptions, then recommend and
  optionally apply cost-saving optimizations. Use when the user asks to "check
  token usage", "token diet", "diagnose tokens", "토큰 다이어트", "토큰 진단",
  "토큰 비용", "per-turn cost", "reduce token overhead", "token audit",
  "how much context am I using", or wants to understand and reduce their
  per-turn token footprint. Do NOT use for CLI output compression (handled by
  rtk-token-optimization rule and rtk skill). Do NOT use for model routing
  strategy design (use ecc-token-strategy rule). Do NOT use for context
  compaction timing advice (use ecc-strategic-compact skill).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "optimization"
---

# Token Diet — Per-Turn Token Consumption Diagnostic

Measures the fixed overhead injected into every agent turn — rules, memory files,
MCP schemas, and skill metadata — then estimates session cost and produces
actionable diet recommendations. Complements `ecc-token-strategy.mdc` (behavior
guidelines) and `rtk` (CLI output compression) by providing **measurement** and
**diagnosis**.

## Role

You are a token budget analyst. You measure, grade, and recommend — you do not restructure projects or redesign skill architectures.

## Modes

Parse user input for the mode keyword:

| Mode | Trigger | Behavior |
|------|---------|----------|
| `diagnose` | default / "diagnose" | Measure all sources, display report |
| `apply` | "apply" | Diagnose, then apply safe optimizations with backup |
| `report` | "report" | Diagnose, then save to `outputs/token-diet/token-diet-{date}.md` |

## Constraints

- Do NOT modify files without explicit `apply` mode
- Do NOT auto-split or restructure `AGENTS.md` without user confirmation
- Do NOT add per-turn overhead itself — the companion rule `token-diet-hygiene.mdc` is `alwaysApply: false`
- Do NOT duplicate guidance from `ecc-token-strategy.mdc` — reference it
- Report numbers honestly; do not round down to manufacture a green result

## Workflow

### Step 1: Measure Per-Turn Token Sources

Measure each source by reading its content and counting bytes. Estimate tokens as `~bytes / 4`.

#### 1a. Always-Applied Rules

```bash
# List all .mdc files with alwaysApply: true, sum byte sizes
for f in .cursor/rules/*.mdc .cursor/rules/**/*.mdc; do
  if head -10 "$f" 2>/dev/null | grep -q 'alwaysApply:.*true'; then
    wc -c < "$f"
  fi
done
```

Count the number of matching files and their total byte size.

#### 1b. AGENTS.md

```bash
wc -c < AGENTS.md
```

#### 1c. MEMORY.md

```bash
wc -c < MEMORY.md
```

Note: MEMORY.md may not be injected every turn depending on Cursor's behavior.
Include it as a "potential overhead" line item.

#### 1d. MCP Server Schemas

Count MCP server directories under the project MCP config folder:

```bash
ls ~/.cursor/projects/*/mcps/ 2>/dev/null | grep -c ''
```

Each enabled MCP server injects its tool schemas (~500-2000 tokens per server).
Estimate conservatively as `count × 1000 tokens`.

#### 1e. Skill Descriptions

Count SKILL.md files across `.cursor/skills/`:

```bash
find .cursor/skills -name 'SKILL.md' | wc -l
```

Each skill's `description` field (from YAML frontmatter) is injected per-turn.
Average description length is ~200 bytes. Estimate as `count × 50 tokens`.

#### 1f. Grade Each Source

| Source | GREEN | YELLOW | RED |
|--------|-------|--------|-----|
| Always-applied rules | < 20 KB total | 20-50 KB | > 50 KB |
| AGENTS.md | < 8 KB | 8-15 KB | > 15 KB |
| MEMORY.md | < 20 KB | 20-50 KB | > 50 KB |
| MCP servers | ≤ 5 | 6-10 | > 10 |
| Skill count | < 200 | 200-500 | > 500 |

### Step 2: Cost Estimation

Use these pricing references (per 1M tokens):

| Model | Input (cache miss) | Input (cache hit) | Output |
|-------|--------------------|--------------------|--------|
| Haiku / fast | $0.25 | $0.03 | $1.25 |
| Sonnet / default | $3.00 | $0.30 | $15.00 |
| Opus | $15.00 | $1.50 | $75.00 |

Calculate for a 10-turn session:
- **Cache-hit scenario** (80% hit rate): `total_tokens × 10 × (0.8 × cache_hit + 0.2 × cache_miss) / 1M`
- **Cache-miss scenario** (0% hit): `total_tokens × 10 × cache_miss / 1M`

Present estimates for the default model tier (Sonnet).

### Step 3: Generate Recommendations

Analyze each source and produce ranked recommendations by estimated savings:

#### AGENTS.md Diet
- Classify each section as "every-turn essential" vs "move to agent-requestable rule"
- Flag sections > 2 KB that could be separate `.mdc` files with `alwaysApply: false`
- Estimate token savings if sections were moved

#### Rules Diet
- Identify the top 5 largest `alwaysApply: true` rules by byte size
- For each: assess whether it truly needs every-turn injection or could be `alwaysApply: false`
- Flag duplicate or near-duplicate rules (e.g., `git-rules.mdc` and `git-rules copy.mdc`)

#### MCP Diet
- List all enabled MCP servers
- For each, check if it was used in the last session (not measurable — flag as "verify manually")
- Recommend disabling servers that are project-irrelevant

#### Skills Diet
- If skill count > 500, flag that description injection overhead is significant
- Scan for skills with descriptions > 1024 characters and list the top 10 longest
- Recommend shortening or using `>-` folded block for verbose descriptions

#### Session Habits

Refer users to the **Composability** table below for complementary skills/rules — do not duplicate their guidance here.

### Step 4: Apply (only in `apply` mode)

Only perform safe, reversible changes:

1. **Backup**: Copy `AGENTS.md` to `AGENTS.md.bak.{date}`
2. **Trim whitespace**: Remove trailing whitespace and collapse 3+ consecutive blank lines to 2
3. **Flag duplicates**: If `git-rules copy.mdc` exists alongside `git-rules.mdc`, recommend deletion
4. **Generate split suggestions**: For AGENTS.md sections > 2 KB, draft the extracted rule file content but do NOT write it — present to user for approval

Report what was changed and what requires manual approval.

### Step 5: Save Report (only in `report` mode)

Write the full diagnostic to `outputs/token-diet/token-diet-{date}.md` using the output format below.

## Output Format

Present results in Korean with this structure:

```
## Token Diet 진단 리포트

### 턴당 입력 토큰 추정

| 소스 | 바이트 | ~토큰 | 등급 | 비고 |
|------|--------|-------|------|------|
| Always-applied rules ({count}개) | {bytes} | {tokens} | {grade} | |
| AGENTS.md | {bytes} | {tokens} | {grade} | |
| MEMORY.md | {bytes} | {tokens} | ⚠️ | 조건부 주입 |
| MCP 서버 스키마 ({count}개) | - | ~{tokens} | {grade} | 추정치 |
| 스킬 설명 ({count}개) | - | ~{tokens} | {grade} | 추정치 |
| **합계** | | **~{total}** | | |

### 10턴 세션 비용 추정 (Sonnet 기준)

| 시나리오 | 비용 |
|----------|------|
| 캐시 히트 (80%) | ${cost} |
| 캐시 미스 (100%) | ${cost} |

### 상위 권장 사항

1. {recommendation} — 예상 절감: ~{tokens} 토큰
2. {recommendation} — 예상 절감: ~{tokens} 토큰
3. {recommendation} — 예상 절감: ~{tokens} 토큰

### 상세 분석

[Per-source detailed findings from Step 3]
```

## Output Artifacts

| Phase | Stage Name | Output File | Skip Flag |
|-------|-----------|-------------|-----------|
| 5 | Save Report | `outputs/token-diet/token-diet-{date}.md` | `report` mode only |

## Composability

| Skill / Rule | Relationship |
|-------------|-------------|
| `ecc-token-strategy.mdc` | Referenced for model routing recommendations |
| `rtk-token-optimization.mdc` | Referenced for CLI compression |
| `rtk` skill | Complementary — CLI-level analytics |
| `skill-optimizer` | Composable — audit skill descriptions for length |
| `setup-doctor` | Composable — MCP server inventory |
| `ecc-strategic-compact` | Referenced for compaction timing |
| `token-diet-hygiene.mdc` | Companion rule — quick-reference checklist |

## Error Recovery

If measurement fails for a specific source (e.g., missing MEMORY.md), skip that
row with a note "파일 없음" and continue with remaining sources.

## Verification

After completing the diagnostic:
1. Confirm all measured files exist and were readable
2. Confirm token estimates use the `bytes / 4` formula consistently
3. Confirm cost calculations match the pricing table
4. Confirm recommendations are ranked by estimated savings (largest first)
