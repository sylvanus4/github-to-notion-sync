## Team: Meeting Intelligence

6명의 전문가 에이전트를 Parallel Extraction + Content-Based Routing 패턴으로 오케스트레이션하여 회의 트랜스크립트 분석, 의사결정 추출, 액션 아이템 추출, 요약 작성, 멀티채널 배포를 수행한다.

### Usage

```
/team-meeting-intel {Notion URL | file path | pasted transcript}

# 예시
/team-meeting-intel https://www.notion.so/meeting-2026-04-24-abc123
/team-meeting-intel ./transcripts/sprint-retro-2026-04-24.md
```

### Workflow

1. **Transcript Analyzer** — 참석자, 주제, 핵심 포인트, 감성, 대화 흐름 구조화 분석
2. **[Parallel Extraction]**
   - **Decision Extractor** — 공식/비공식 의사결정 추출 + 유형/영향 분류
   - **Action Tracker** — 액션 아이템 추출 + 오너/기한/의존성 할당
3. **Summary Writer** — 모든 누적 컨텍스트를 기반으로 포괄적 한국어 요약 작성
4. **Distribution Agent** — 콘텐츠 유형별 채널 라우팅 (Notion, Slack, Drive)

### Execution

코디네이터 스킬을 읽고 프로토콜을 따른다:

```
.cursor/skills/agent-teams/meeting-intel/coordinator/SKILL.md
```

모든 전문가 에이전트는 `Task(subagent_type="generalPurpose")`로 디스패치된다.
워크스페이스: `_workspace/meeting-intel/`
