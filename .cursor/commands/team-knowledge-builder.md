## Team: Knowledge Builder

5명의 전문가 에이전트를 Pipeline + Gap-Fill Loop 패턴으로 오케스트레이션하여 원시 소스 수집, 개념 추출, 위키 컴파일, 크로스링크 발견, 품질 감사를 수행한다.

### Usage

```
/team-knowledge-builder {topic or scope}

# 예시
/team-knowledge-builder "sales-playbook 주간 빌드"
/team-knowledge-builder "engineering-standards 전체 재컴파일"
/team-knowledge-builder "competitive-intel 신규 소스 통합"
```

### Workflow

1. **Source Collector** — URL, PDF, 레포, 피드에서 원시 소스 수집 → clean markdown 변환
2. **Content Extractor** — 원시 소스에서 구조화된 개념, 엔티티, 관계, 핵심 사실 추출
3. **Wiki Compiler** — 추출된 콘텐츠를 크로스레퍼런스와 계층 구조의 위키 문서로 컴파일
4. **Cross-Linker** — 명시적 링크가 없는 위키 문서 간 암묵적 연결 발견
5. **Quality Auditor** — 신선도, 깨진 링크, 커버리지 갭, 증거 밀도, 일관성 감사
6. **[Gap-Fill Loop]** — 감사에서 발견된 커버리지 갭을 Source Collector로 재라우팅

### Execution

코디네이터 스킬을 읽고 프로토콜을 따른다:

```
.cursor/skills/agent-teams/knowledge-builder/coordinator/SKILL.md
```

모든 전문가 에이전트는 `Task(subagent_type="generalPurpose")`로 디스패치된다.
워크스페이스: `_workspace/knowledge-builder/`
