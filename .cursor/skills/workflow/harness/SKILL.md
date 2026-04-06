---
name: harness
description: "Design and generate coordinated multi-agent skill architectures for any domain or project. Analyzes domain requirements, designs agent team patterns (Pipeline, Fan-out/Fan-in, Expert Pool, Producer-Reviewer, Supervisor, Hierarchical Delegation, Composite), generates specialized agent skills as .cursor/skills/ files, creates orchestrator workflows using Cursor's Task tool for parallel and sequential agent execution, and validates the complete system with trigger conflict detection and dry-run testing. Supports --single-file mode for generating autoagent-compatible single-file harnesses with editable/fixed boundary sections via HarnessTemplate. Based on revfactory/harness methodology. Use when the user asks to 'build a harness', 'design agent team', 'harness', 'agent team architecture', 'multi-agent workflow design', 'generate agent skills for domain', 'skill architecture', 'orchestrate agents', 'create agent pipeline', 'design agent system', 'agent workflow', 'build agent team for', 'scaffold multi-agent', 'single-file harness', 'scaffold harness', '하네스 구성해줘', '하네스 구축해줘', '하네스 설계', '에이전트 팀 설계', '에이전트 아키텍처', '멀티에이전트 워크플로우', '스킬 아키텍처 설계', '에이전트 시스템 구축', '팀 기반 자동화', '에이전트 파이프라인', '단일 파일 하네스', or wants to create a coordinated multi-agent system for a new domain/project, or scaffold a single-file agent harness for autoagent optimization. Do NOT use for running an existing harness — invoke the generated orchestrator skill directly. Do NOT use for single-skill creation without team context (use create-skill). Do NOT use for optimizing existing individual skills (use skill-optimizer or skill-autoimprove). Do NOT use for ad-hoc orchestration of existing skills at runtime (use mission-control). Do NOT use for multi-agent design theory only without file generation (use ce-multi-agent-patterns). Do NOT use for converting natural language to skill chains from existing skills (use skill-composer)."
metadata:
  version: "1.2.0"
  tags: ["meta-skill", "agent-team", "skill-architect", "orchestration", "multi-agent"]
  source: "https://github.com/revfactory/harness"
---

# Harness — Agent Team & Skill Architect

도메인/프로젝트에 맞는 멀티에이전트 하네스를 설계하고, 전문 에이전트 스킬 파일을 생성하며, 오케스트레이션 워크플로우를 구축하는 메타 스킬.

## Quick Start

```
사용자: "코드 리뷰를 위한 에이전트 팀을 설계해줘"

→ harness 스킬이 6-Phase 워크플로우를 실행:
  Phase 1: 도메인 분석 (코드 리뷰 작업 유형, 기존 스킬 확인)
  Phase 2: 팀 아키텍처 설계 (팬아웃/팬인 패턴 선택)
  Phase 3: 에이전트 스킬 정의 + 파일 생성
           → .cursor/skills/security-reviewer/SKILL.md
           → .cursor/skills/performance-reviewer/SKILL.md
           → .cursor/skills/quality-reviewer/SKILL.md
  Phase 4: 오케스트레이터 생성
           → .cursor/skills/code-review-orchestrator/SKILL.md
  Phase 5: 검증 (트리거 충돌, 데이터 흐름, 드라이런)

산출물: 즉시 사용 가능한 에이전트 팀 스킬 세트
```

## 핵심 원칙

1. 전문 에이전트를 `.cursor/skills/{name}/SKILL.md`로 정의한다.
2. Task 도구의 병렬/순차 호출 패턴으로 에이전트 팀을 오케스트레이션한다.
3. 파일 기반 데이터 전달로 에이전트 간 협업을 구현한다.
4. **에이전트 팀을 기본 실행 모드로 사용한다** — 단일 에이전트보다 팀이 우선.

## Cursor 환경 매핑

| Claude Code | Cursor 등가물 | 핵심 차이 |
|---|---|---|
| `Agent` 도구 | `Task` 도구 (`subagent_type` 파라미터) | subagent_type으로 역할 구분 |
| `TeamCreate` + `SendMessage` | 한 메시지에 여러 병렬 `Task` 호출 | 최대 4개 동시 권장 |
| `TaskCreate`/`TaskUpdate` | `TodoWrite` 도구 + 파일 기반 상태 관리 | — |
| `.claude/agents/{name}.md` | `.cursor/skills/{name}/SKILL.md` | — |
| `.claude/commands/` | `.cursor/commands/` | — |
| `model: "opus"` | Task의 `model` 파라미터 | `fast`, 기본, 상위 모델 선택 |

### ⚠️ 컨텍스트 격리 — Cursor의 핵심 제약

Task로 호출된 서브에이전트는 **부모의 대화 컨텍스트를 전혀 받지 못한다.** 서브에이전트가 알아야 하는 모든 정보를 `prompt` 파라미터에 명시적으로 전달해야 한다:

- 작업 목표와 배경
- 입력 파일 경로 (서브에이전트가 Read로 읽을 수 있도록)
- 출력 파일 경로 (Write로 저장할 위치)
- 품질 기준과 형식 요구사항
- 참고해야 할 스킬 파일 경로 (`.cursor/skills/{name}/SKILL.md`)

이 제약이 하네스 설계의 핵심이다 — **"서브에이전트에게 필요한 모든 것을 prompt에 담는다"**가 성공의 전제조건.

## 6-Phase 워크플로우

### Phase 1: 도메인 분석

1. **요구사항 파악** — 사용자 요청에서 도메인, 목표, 제약조건 식별
2. **작업 유형 분류** — 핵심 작업 식별 (생성, 검증, 편집, 분석, 배포 등)
3. **기존 스킬 스캔** — `Glob("**/.cursor/skills/*/SKILL.md")`로 설치된 스킬 목록화, `Grep`으로 트리거 충돌 탐지
4. **코드베이스 탐색** — `Task(subagent_type="explore")`로 기술 스택, 디렉토리 구조 파악
5. **팀 규모 판단**:

| 프로젝트 규모 | 에이전트 수 | 적합한 패턴 |
|---|---|---|
| 소규모 (단일 도메인) | 2–3 | 파이프라인 또는 생성-검증 |
| 중규모 (복수 도메인) | 4–6 | 팬아웃/팬인 또는 전문가 풀 |
| 대규모 (엔터프라이즈) | 7–12 | 감독자 또는 계층적 위임 |

### Phase 2: 팀 아키텍처 설계

#### 패턴 선택

| 패턴 | Cursor 구현 | 적합한 경우 |
|---|---|---|
| **파이프라인** | 순차 Task 호출 | 명확한 단계별 의존성 |
| **팬아웃/팬인** | 병렬 Task 호출 → 결과 합성 | 독립적 분석 2+ 동시 필요 |
| **전문가 풀** | 조건부 Task 호출 | 입력 유형에 따라 다른 처리 |
| **생성-검증** | 순차 Task + 품질 게이트 | 품질 보장 필수 |
| **감독자** | 메인 에이전트의 조건부 Task 분배 | 동적 라우팅 필요 |
| **계층적 위임** | Task 내에서 추가 Task 호출 | 복잡한 다층 분해 (2단계 이내) |
| **복합** | 혼합 (예: 팬아웃 + 파이프라인) | 대규모 시스템 |

의사결정 트리:
```
1. 단일 에이전트로 충분한가?
   → YES: 단일 Task 호출. 팀 불필요.
   → NO: 계속.
2. 순차 의존성이 있는가? (B가 A 결과 필요)
   → YES: 파이프라인.
3. 독립 서브태스크가 있는가?
   → YES: 팬아웃/팬인.
4. 첫 결과 품질이 일관되게 부족한가?
   → YES: 생성-검증 루프 추가.
5. 입력 유형별 라우팅이 필요한가?
   → YES: 전문가 풀 또는 감독자.
```

상세 패턴 비교와 코드 예시: `references/agent-patterns.md` 참조.

#### 에이전트 분리 기준

4축으로 분리 필요성을 판단한다:

- **전문성**: 서로 다른 전문 지식이 필요한가?
- **병렬성**: 동시 실행 가능한가?
- **컨텍스트**: 별도 컨텍스트 윈도우가 유리한가?
- **재사용성**: 다른 워크플로우에서도 독립 사용 가능한가?

4개 중 2개 이상 YES면 별도 에이전트로 분리.

### Phase 3: 에이전트 스킬 생성

각 에이전트를 `.cursor/skills/{agent-name}/SKILL.md`로 정의하고 Write 도구로 파일을 생성한다.

#### 에이전트 스킬 필수 구조

```markdown
---
name: {agent-name}
description: "{역할 + 트리거 + Do NOT use}"
metadata:
  tags: ["{domain}", "{role}"]
---
# {Agent Name}

## 역할
{핵심 역할과 전문 분야 — why-first로 이유 포함}

## 원칙
{작업 품질 기준, 판단 기준}

## 입력/출력
- 입력: {예상 입력 형식과 위치 — `_workspace/` 경로 명시}
- 출력: {산출물 형식과 저장 경로}

## 프로토콜
{에러 핸들링, 출력 없는 경우 처리, 다른 에이전트와 협업 방식}
```

#### Description 작성 — "Pushy" 원칙

description은 스킬의 유일한 트리거 메커니즘이므로 적극적으로 작성한다:

- 모든 관련 동사를 나열 (analyze, generate, validate, review, ...)
- Korean + English 트리거 모두 포함
- 구체적 Do NOT use 명시 (경계 스킬 구분, `(use {대안})` 형태)
- 1% 확률의 트리거도 포착하도록 넓게 작성

#### 스킬 작성 원칙

| 원칙 | 설명 |
|---|---|
| **Why-First** | "ALWAYS/NEVER" 대신 이유를 전달. LLM은 이유를 이해하면 엣지 케이스에서도 판단 |
| **Lean** | SKILL.md 본문 500줄 이내, 초과 시 references/로 분리 |
| **일반화** | 특정 예시 맞춤 규칙보다 원리 설명으로 다양한 입력 대응 |
| **명령형** | "~한다", "~하라" 형태의 직접 지시 |
| **스크립트 번들링** | 에이전트들이 반복 작성하는 코드는 `references/scripts/`에 미리 포함 |
| **Progressive Disclosure** | Metadata → SKILL.md → references/ 3단계 점진적 로딩 |

상세 작성 가이드: `references/skill-authoring.md` 참조.

#### 모델 라우팅

| 에이전트 유형 | Cursor Task model | 이유 |
|---|---|---|
| 탐색/검색 | `model: "fast"` | 비용 절감, 빠른 응답 |
| 구현/분석 | 기본 모델 | 균형 |
| 아키텍처/추론 | 더 높은 모델 지정 | 복잡한 판단 필요 |

### Phase 4: 오케스트레이션 통합

오케스트레이터 스킬을 생성하여 개별 에이전트를 하나의 워크플로우로 엮는다.

#### Cursor 오케스트레이션 패턴

**병렬 팬아웃** (한 메시지에서 여러 Task 동시 호출):
```
Task(agent-1, subagent_type="generalPurpose",
     prompt="당신은 {역할}입니다. {배경 설명}.
     입력: _workspace/00_input.md를 Read하세요.
     작업: {구체적 지시}
     출력: _workspace/01_agent1_result.md에 Write하세요.")

Task(agent-2, ..., prompt="...")  // 동시 실행
Task(agent-3, ..., prompt="...")  // 동시 실행
→ 모든 결과 파일 Read → 취합
```

**순차 파이프라인:**
```
Phase 1: Task(analyst, prompt="... → _workspace/01_analysis.md")
    ↓ 결과 파일 읽기
Phase 2: Task(builder, prompt="01_analysis.md를 Read하고 구현 → _workspace/02_build.md")
    ↓ 결과 파일 읽기
Phase 3: Task(qa, prompt="02_build.md를 Read하고 검증 → _workspace/03_qa.md")
```

#### 에이전트 간 데이터 전달

Cursor에서는 파일 기반 전달이 주요 방식:

1. 작업 루트에 `_workspace/` 폴더 생성 (`Shell: mkdir -p _workspace/00_input`)
2. 파일명: `{phase}_{agent}_{artifact}.{ext}` (예: `01_analyst_domain-analysis.md`)
3. 최종 산출물만 사용자 지정 경로에 출력
4. 중간 파일은 보존 (감사 추적 + 사후 검증)

#### Task 프롬프트 템플릿

서브에이전트는 부모 컨텍스트 없이 시작하므로 prompt가 자기 완결적이어야 한다:

```
"당신은 {역할}입니다. {도메인에 대한 배경 설명}.

## 참고 스킬
.cursor/skills/{name}/SKILL.md를 Read하여 작업 가이드를 확인하세요.

## 입력
{입력 파일 경로}를 Read하세요. {내용 설명}.

## 작업
{구체적이고 측정 가능한 지시}

## 출력
결과를 `{출력 경로}`에 Write 도구로 저장하세요.
형식: {마크다운/JSON/기타}

## 제약
- {금지 사항}
- {품질 기준}

## 완료
작업이 끝나면 '{요약 한 줄}'을 반환하세요."
```

#### 에러 핸들링

- 1회 재시도 후 재실패 시 해당 결과 없이 진행 (보고서에 누락 명시)
- 상충 데이터는 삭제하지 않고 출처 병기
- Phase 실패 시 전체 중단하지 않고 degraded 결과 생성

### Phase 5: 검증 및 테스트

#### 구조 검증
- [ ] 모든 에이전트 스킬 파일이 `.cursor/skills/`에 존재
- [ ] SKILL.md frontmatter (name, description) 유효
- [ ] `Grep`으로 기존 스킬과 트리거 충돌 없음 확인
- [ ] 오케스트레이터 스킬의 데이터 흐름에 빈 구간 없음

#### 트리거 검증
- Should-trigger 쿼리 8–10개 (공식/캐주얼, 명시적/암시적, Korean/English)
- Should-NOT-trigger 쿼리 8–10개 (경계가 모호한 near-miss)

#### 드라이런 테스트
1. 테스트 프롬프트 2–3개로 오케스트레이터 실행
2. Phase 순서 논리성 검토
3. 데이터 전달 경로 검증 (파일이 실제 생성되는가)
4. 에러 시나리오별 폴백 경로 확인

#### 스킬 품질 평가
1. **With-skill vs Without-skill** — 스킬 유무 비교로 부가가치 확인
2. **정성적** — 사용자 리뷰 (유용성, 정확성, 완결성)
3. **정량적** — assertion 기반 (특정 출력 포함 여부, 형식 준수 등)

상세 테스트 방법론: `references/skill-authoring.md`의 "테스트" 섹션 참조.

### Phase 6: Post-Deploy Monitoring (Optional)

If the harness includes observable endpoints or metrics, set up canary monitoring with existing skills (`canary-monitor`, `ops-kpi-autopilot`).

### Phase 7: Outer-Loop Optimization with Meta-Harness (Optional)

Once a harness is deployed and producing execution traces, apply the Meta-Harness outer-loop to automatically optimize the harness code itself — not just prompts.

#### When to Apply

- The harness has been running for 5+ iterations with measurable quality metrics
- Prompt-level tuning (`skill-autoimprove`) has plateaued
- Multi-objective trade-offs (accuracy vs cost, speed vs depth) need systematic exploration

#### How It Works

1. **Enable trace capture** — Run inner-loop skills with `--trace-aware` to store execution traces via `TraceArchive` (see `scripts/meta_harness_trace.py`)
2. **Invoke meta-harness-optimizer** — Target the orchestrator or individual agent SKILL.md:
   ```
   /meta-harness optimize --target .cursor/skills/{domain}-orchestrator/SKILL.md --inner-loop
   ```
3. **Review Pareto frontier** — The optimizer proposes code-level mutations (retrieval logic, memory management, prompt construction, tool orchestration) and evaluates each against multiple objectives
4. **Accept or reject** — Each candidate is logged with full source, diff, scores, and proposer reasoning for audit

#### Architecture (from Meta-Harness paper, arXiv:2603.28052)

```
┌─────────────────────────────────────────────┐
│              Meta-Harness Loop              │
│                                             │
│  ┌─────────────┐    ┌──────────────────┐   │
│  │   Proposer   │───▶│  Code Mutation   │   │
│  │  (Agentic)   │    │  (Skill/Script)  │   │
│  └──────▲───────┘    └───────┬──────────┘   │
│         │                    │              │
│         │ uncompressed       ▼              │
│         │ traces      ┌──────────────┐      │
│         │             │  Evaluator   │      │
│         └─────────────│  (Inner Loop │      │
│                       │  + Metrics)  │      │
│                       └──────┬───────┘      │
│                              │              │
│                              ▼              │
│                       ┌──────────────┐      │
│                       │ TraceArchive │      │
│                       │ (Filesystem) │      │
│                       └──────────────┘      │
└─────────────────────────────────────────────┘
```

#### Key Differentiator from skill-autoimprove

| Dimension | skill-autoimprove (Inner) | meta-harness-optimizer (Outer) |
|-----------|--------------------------|-------------------------------|
| Search space | Prompt text mutations | Code-level changes (retrieval, tools, memory) |
| Feedback | Binary pass/fail scores | Full execution traces (~450× richer) |
| Optimization | Single objective (score) | Multi-objective Pareto frontier |
| Scope | One skill at a time | Orchestrator + constituent agents |

#### Integration Checklist

- [ ] Enable `--trace-aware` on inner-loop evals
- [ ] Verify `TraceArchive` writes to `_workspace/meta-harness/`
- [ ] Define 2+ measurable objectives for Pareto ranking
- [ ] Set iteration budget (default: 20, start conservative)
- [ ] Review generated `report.md` after each run

Related skills: `meta-harness-optimizer` (outer loop), `skill-autoimprove --trace-aware` (inner loop), `scripts/meta_harness_trace.py` (archive library).

## Single-File Harness Mode (`--single-file`)

Generate a single-file agent harness with clear editable and fixed boundary sections, compatible with `autoagent-loop` optimization. Uses `HarnessTemplate` from `scripts/autoagent/`.

### Activation

```
사용자: "단일 파일 하네스 생성해줘" / "scaffold single-file harness"
→ harness 스킬이 --single-file 모드로 실행
```

Or explicitly:
```
/harness --single-file --sdk openai --output agent.py
/harness --single-file --sdk claude --output agent.py
```

### What It Produces

Instead of multiple SKILL.md files and an orchestrator, this mode generates a single `agent.py` file with:

1. **Editable section** (above the boundary marker) — agent logic, tools, prompts that the meta-agent can modify
2. **Fixed adapter boundary** (below the marker) — CLI interface, Docker glue, scoring hooks that must never change

```python
# ═══════════════ EDITABLE SECTION ═══════════════
# The meta-agent may modify everything above the boundary.

SYSTEM_PROMPT = "..."
TOOLS = [...]

async def solve(task: str) -> str:
    ...

# ═══════════════ FIXED ADAPTER BOUNDARY ═══════════════
# Everything below is infrastructure. Do NOT modify.

if __name__ == "__main__":
    ...
```

### SDK Support

| SDK | Template | Agent Framework |
|-----|----------|-----------------|
| `openai` | OpenAI Agents SDK (`agents` package) | `Agent`, `Runner`, `function_tool` |
| `claude` | Claude Agent SDK (`claude_agent_sdk`) | `create_agent`, `run_agent`, `tool` |

### Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--sdk` | `openai` | Target SDK: `openai` or `claude` |
| `--output` | `agent.py` | Output file path |
| `--model` | SDK default | Model to use in the harness |
| `--tools` | `[]` | Comma-separated tool names to include |
| `--name` | `"agent"` | Agent name in the generated code |

### How It Connects

- The generated harness feeds directly into `autoagent-loop` for optimization
- `autoagent-benchmark` can build a Docker image from the harness and run task suites
- `skill-autoimprove --harness-mode` can mutate the editable section
- `meta-harness-optimizer --atif-import` can consume benchmark trajectories

### Generation Flow

1. Read `HarnessTemplate` from `scripts/autoagent/harness_template.py`
2. Call `HarnessTemplate.generate(sdk=sdk, model=model, tools=tools, agent_name=name)`
3. Write the output file
4. Optionally generate a Dockerfile via `HarnessTemplate.generate_dockerfile()`
5. Optionally generate a starter task suite in Harbor format

---

## 산출물 체크리스트

Phase 완료 후 다음을 확인한다:

- [ ] `.cursor/skills/{agent}/SKILL.md` — 에이전트별 스킬 정의
- [ ] `.cursor/skills/{domain}-orchestrator/SKILL.md` — 오케스트레이터 스킬
- [ ] `.cursor/commands/{domain}.md` — 진입점 커맨드 (선택)
- [ ] 실행 모드 명시 (병렬 팬아웃 / 순차 파이프라인 / 혼합)
- [ ] 기존 스킬과 트리거 충돌 없음 확인
- [ ] description이 pushy 스타일로 작성됨
- [ ] SKILL.md 본문 500줄 이내, 초과 시 references/ 분리
- [ ] 서브에이전트 prompt가 자기 완결적 (컨텍스트 격리 대응)
- [ ] 테스트 프롬프트 2–3개로 실행 검증 완료

## 참고 자료

| 참고 문서 | 내용 |
|---|---|
| `references/agent-patterns.md` | 7개 아키텍처 패턴 상세 + 오케스트레이터 템플릿 |
| `references/skill-authoring.md` | 스킬 작성 가이드 + 테스트 방법론 |
| `references/team-examples.md` | 실제 하네스 구성 예시 3종 (코드 리뷰, 문서 생성, 리서치) |
| `references/qa-guide.md` | QA 에이전트 설계 가이드 (경계면 교차 비교) |

## Subagent Contract

When spawning Task tool subagents:

- Always pass **absolute file paths** — subagent working directories are unpredictable
- Share only **load-bearing code snippets** — omit boilerplate the subagent can discover itself
- Require subagents to return: `{ status, file, summary }` — not full analysis text
- Include a **purpose statement** in every subagent prompt: "You are a subagent whose job is to [specific goal]"
- Never say "do everything" — list the 3-5 specific outputs expected
