## Team: Content Production

6명의 전문가 에이전트를 Pipeline + Quality Gate 패턴으로 오케스트레이션하여 리서치 기반 멀티 플랫폼 콘텐츠를 생산한다.

### Usage

```
/team-content-production {topic or brief}

# 예시
/team-content-production "ThakiCloud GPU 클러스터 자동 스케일링 기능 소개"
/team-content-production "AI 에이전트 오케스트레이션 베스트 프랙티스" --platforms=blog,linkedin,twitter
```

### Workflow

1. **Topic Researcher** — 대상 주제의 오디언스 인사이트, 트렌딩 앵글, 경쟁 콘텐츠 갭 조사
2. **Outline Architect** — 훅, 섹션 흐름, 핵심 논점, CTA가 포함된 구조화 아웃라인 설계
3. **Draft Writer** — 아웃라인 + 리서치 데이터를 기반으로 전체 초안 작성
4. **Editor** — 6개 품질 차원 평가 및 구조화된 피드백 생성 (품질 게이트)
5. **Quality Gate** — 통과 시 진행, 미달 시 Draft Writer로 재라우팅 (최대 2회)
6. **Platform Formatter** — 승인된 초안을 플랫폼별 포맷(Twitter, LinkedIn, 블로그 등)으로 변환

### Execution

코디네이터 스킬을 읽고 프로토콜을 따른다:

```
.cursor/skills/agent-teams/content-production/coordinator/SKILL.md
```

모든 전문가 에이전트는 `Task(subagent_type="generalPurpose")`로 디스패치된다.
워크스페이스: `_workspace/content-production/`
