## Team: Research & Report

4명의 전문가 에이전트(Research, Analysis, Writing, Reviewer)를 Pipeline + Review Loop 패턴으로 오케스트레이션하여 연구 기반 보고서를 생성한다.

### Usage

```
/team-research-report {topic}

# 옵션
/team-research-report "AI 에이전트 시장 분석" --depth=deep --format=docx
/team-research-report "GPU 클라우드 가격 비교" --depth=quick --lang=en
```

| Option | Values | Default |
|--------|--------|---------|
| `--depth` | quick (1p), standard (3-5p), deep (10+p) | standard |
| `--format` | markdown, docx, both | markdown |
| `--lang` | ko, en | ko |

### Workflow

1. **Goal Decomposition** — topic, scope, depth, format, language 파싱
2. **Research Expert** — 웹 리서치, 논문, KB 검색으로 원시 자료 수집
3. **Analysis Expert** — 패턴 식별, 모순 분석, 인사이트 도출
4. **Writing Expert** — 구조화된 보고서 초안 작성 (revision 피드백 반영)
5. **Reviewer Expert** — 6개 차원 품질 평가 (정확성, 깊이, 구조, 실행가능성, 인용, 명확성)
6. **Quality Gate** — score >= 80 통과, 미달 시 Writing으로 재라우팅 (최대 2회)
7. **Final Assembly** — 최종 보고서 생성 및 선택적 docx 변환

### Execution

코디네이터 스킬을 읽고 프로토콜을 따른다:

```
.cursor/skills/agent-teams/research-report/coordinator/SKILL.md
```

모든 전문가 에이전트는 `Task(subagent_type="generalPurpose")`로 디스패치된다.
워크스페이스: `_workspace/research-report/`
