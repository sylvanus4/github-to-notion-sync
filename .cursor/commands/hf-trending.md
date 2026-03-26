---
description: "Run HF trending intelligence — 논문 중심 트렌드 리포트 + 토픽 모델/스페이스 레이더"
---

# HF Trending — AI Research Radar

## Skill Reference

Read and follow the skill at `.cursor/skills/hf-trending-intelligence/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Parse Request

Determine mode from user input:

- **Default (no args)**: 논문 스캔 + 토픽 레이더(`LLM, video-generation`) 실행. 리더보드 비활성.
- **With explicit topics** (e.g., "topics=multi-LLM"): 지정된 토픽으로 Phase 1.5 실행
- **"--leaderboard"**: Phase 2.5 (리더보드 크로스-레퍼런스) 명시적 활성화
- **"--skip-topics"**: Phase 1.5 비활성 (논문 전용 v1 레거시)
- **Date override** (e.g., "yesterday"): 지정 날짜 사용

**Default topics:** `LLM, video-generation` (from `hf-topic-radar/references/topic-config.md`)

### Step 2: Execute Pipeline

Run the full pipeline as specified in the skill:

1. Paper Scan (30 trending papers)
1.5. Topic-Focused Model & Space Trending (default: LLM, video-generation; skip with --skip-topics)
2. Cross-Reference (top 10 papers — models, datasets, discussions)
3. Web Enrichment (top 5 papers)
4. Trend Scoring (composite score)
5. Intelligence Report Generation (HOT/WARM/COOL 분류)
6. Curate (add HOT items to monthly HF collection)
7. Distribute to Slack `#deep-research-trending` + Notion

**Optional:** `--leaderboard` 전달 시 Phase 2.5 (리더보드 크로스-레퍼런스) 추가 실행

### Step 3: Report Results

Summarize:
- 수집 논문 수
- HOT / WARM / COOL 카운트
- Top 3 트렌드 (점수 포함)
- 토픽별 하이라이트 (토픽 사용 시)
- Report file, Slack thread, Notion page URLs

## Constraints

- Always verify `hf` CLI auth before running
- Max 4 concurrent subagents during cross-reference phase
- Respect rate limits on all external APIs
- 모든 아웃풋은 한글로 작성 (기술 용어는 영어 병기)
