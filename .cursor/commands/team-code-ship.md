## Team: Code Ship

5명의 전문가 에이전트를 Fan-out/Fan-in + Sequential 패턴으로 오케스트레이션하여 코드 리뷰, 보안 감사, 테스트 검증을 병렬 수행 후 문서 업데이트와 PR 패키징을 순차 실행한다.

### Usage

```
/team-code-ship {scope}

# 스코핑 모드
/team-code-ship                    # diff — 커밋되지 않은 변경사항
/team-code-ship diff               # diff — 명시적 지정
/team-code-ship today              # today — 오늘 변경된 모든 파일
/team-code-ship full               # full — 전체 프로젝트
```

### Workflow

1. **[Parallel Fan-out]** — 3개 전문가 동시 실행
   - **Code Reviewer** — 정확성, 유지보수성, 성능, 아키텍처 리뷰
   - **Security Auditor** — OWASP Top 10, 시크릿 탐지, 의존성 취약점
   - **Test Validator** — 테스트 커버리지, 누락 경로, 테스트 품질
2. **Quality Gate** — 3개 모두 score >= 8/10 통과 필요 (최대 2회 재시도)
3. **Documentation Updater** — 코드 변경에 영향받는 ADR, API 문서, 체인지로그 업데이트
4. **PR Packager** — 모든 산출물을 domain-split 커밋 + PR 설명으로 패키징

### Execution

코디네이터 스킬을 읽고 프로토콜을 따른다:

```
.cursor/skills/agent-teams/code-ship/coordinator/SKILL.md
```

모든 전문가 에이전트는 `Task(subagent_type="generalPurpose")`로 디스패치된다.
워크스페이스: `_workspace/code-ship/`
