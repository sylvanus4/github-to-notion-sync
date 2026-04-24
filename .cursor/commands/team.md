## Agent Team Dispatcher

통합 에이전트 팀 디스패처. 8개 멀티에이전트 팀 중 적절한 팀을 선택하고 코디네이터를 통해 Hub-and-Spoke 오케스트레이션을 실행한다.

### Usage

```
/team {team-name} {goal}

# 팀 목록 조회
/team list

# 특정 팀 실행
/team research-report "AI 에이전트 플랫폼 시장 분석 보고서 작성"
/team content-production "ThakiCloud 신규 GPU 기능 소개 콘텐츠"
/team strategic-intel "2026 하반기 AI 인프라 시장 전략"
/team incident-response "API 게이트웨이 504 타임아웃 다수 발생"
/team code-ship diff
/team knowledge-builder "sales-playbook 주간 빌드"
/team meeting-intel {Notion URL 또는 transcript}
/team sales-deal "고객사 A RFP 대응 패키지"
```

### Teams

| Team | Pattern | Experts | Trigger |
|------|---------|---------|---------|
| `research-report` | Pipeline + Review Loop | Research → Analysis → Writing → Reviewer | 연구 보고서, 리서치 리포트 |
| `content-production` | Pipeline + Quality Gate | Topic Research → Outline → Draft → Editor → Platform Formatter | 콘텐츠 생산, 블로그 시리즈 |
| `strategic-intel` | Fan-out/Fan-in | Market Scanner ∥ Competitive Analyst → Strategic Planner → Risk Assessor → Exec Brief | 전략 분석, 시장 인텔리전스 |
| `incident-response` | Severity-Based Routing | Triage → Evidence ∥ RCA → Fix → Customer Comms | 인시던트, 장애 대응 |
| `code-ship` | Fan-out/Fan-in + Sequential | Code Review ∥ Security ∥ Test → Docs → PR Package | 코드 리뷰+PR, 코드 출시 |
| `knowledge-builder` | Pipeline + Gap-Fill Loop | Source Collector → Extractor → Wiki Compiler → Cross-Linker → Quality Auditor | KB 빌드, 위키 구축 |
| `meeting-intel` | Parallel + Routing | Transcript Analyzer → Decision ∥ Action → Summary → Distribution | 회의 분석, 미팅 인텔리전스 |
| `sales-deal` | Parallel + Pipeline | Account Research ∥ Competitive Intel → Proposal → Security QA → Deal Review | 딜 패키지, 제안서 |

### Workflow

1. **팀 선택**: `{team-name}`으로 직접 지정하거나 `list`로 목록 확인
2. **코디네이터 로딩**: 해당 팀의 coordinator SKILL.md를 읽고 프로토콜을 따름
3. **워크스페이스 초기화**: `_workspace/{team}/`에 goal.md와 context.json 생성
4. **전문가 에이전트 디스패치**: Task 서브에이전트(subagent_type: generalPurpose)로 각 전문가를 순차/병렬 실행
5. **품질 게이트**: 코디네이터가 결과를 평가하고 기준 미달 시 재작업 루프 실행
6. **최종 산출물 조립**: 모든 결과를 통합하여 최종 산출물 생성

### Execution

**팀 목록 조회 (`/team list`):**
위 Teams 테이블을 출력한다.

**특정 팀 실행 (`/team {team-name} {goal}`):**

1. 해당 팀의 코디네이터 스킬을 읽는다:
   ```
   .cursor/skills/agent-teams/{team-name}/coordinator/SKILL.md
   ```
2. 코디네이터 스킬의 오케스트레이션 프로토콜을 **그대로** 따른다.
3. 각 전문가 에이전트는 **Task 서브에이전트**로 디스패치하여 병렬/순차 실행한다.
4. 서브에이전트에게는 반드시 다음을 전달한다:
   - 전문가 스킬 파일 경로
   - 누적된 전체 컨텍스트 (goal, 이전 에이전트 출력물)
   - 입출력 파일 경로 (`_workspace/{team}/`)

### Subagent Dispatch Protocol

코디네이터가 전문가 에이전트를 디스패치할 때 반드시 따르는 프로토콜:

```
Task(subagent_type="generalPurpose", description="{team} - {expert role}"):
  prompt:
    1. 스킬 파일 읽기: .cursor/skills/agent-teams/{team}/{expert}/SKILL.md
    2. 목표: {goal.md 전체 내용}
    3. 이전 출력: {누적된 모든 파일 내용 또는 경로}
    4. 입력 파일: _workspace/{team}/{input-files}
    5. 출력 파일: _workspace/{team}/{output-file}
```

서브에이전트는 이전 대화 컨텍스트에 접근할 수 없으므로 **모든 정보를 명시적으로 전달**해야 한다.

### Examples

```
# 리서치 보고서 생성
/team research-report "2026년 AI 에이전트 오케스트레이션 프레임워크 비교 분석"

# 코드 출시 파이프라인
/team code-ship diff

# 인시던트 대응
/team incident-response "vLLM 서빙 노드 OOM 발생, 사용자 요청 실패"

# 전략 인텔리전스
/team strategic-intel "ThakiCloud vs AWS SageMaker vs Azure AI Studio 경쟁 분석"
```
