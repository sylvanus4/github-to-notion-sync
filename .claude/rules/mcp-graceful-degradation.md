# MCP Graceful Degradation

MCP 서버 의존 스킬 작성/실행 시 반드시 fallback 경로를 확보한다.

## 원칙

MCP 서버는 항상 가용하지 않다. 서버 다운, 네트워크 장애, 인증 만료 등으로 실패할 수 있다.
**MCP 실패가 전체 워크플로 실패로 이어져서는 안 된다.**

## Path A / Path B 패턴

모든 MCP 의존 스킬은 두 경로를 가진다:

- **Path A (MCP)**: 구조화된 도구 호출로 최적 실행
- **Path B (Fallback)**: MCP 없이 prompt/agent 기반으로 동일 결과 달성

## 스킬 작성 시

MCP 도구를 사용하는 스킬의 SKILL.md에 다음 구조 포함:

```md
## Path A: MCP Mode
[MCP tool 사용 워크플로]

## Path B: Fallback (MCP 불가 시)
[대체 방법 - Bash/Agent/WebFetch 등]
```

## 판단 기준

```
MCP tool 호출 시도
  |-- 성공 -> Path A 계속
  |-- 실패 (timeout/auth/not found) -> Path B 전환
  |-- ToolSearch에서 tool 미발견 -> Path B 전환
```

## Fallback 전략 (우선순위)

1. **CLI 도구**: `gh` (GitHub), `hf` (HuggingFace), `slack` (Slack CLI)
2. **WebFetch**: 공개 API endpoint 직접 호출
3. **Agent subagent**: prompt 기반으로 동일 작업 수행
4. **수동 안내**: 사용자에게 대체 방법 제시

## 예시

| MCP 도구 | Path A | Path B (Fallback) |
|----------|--------|-------------------|
| `mcp__slack__slack_send_message` | MCP 호출 | `curl` Slack webhook 또는 사용자에게 메시지 텍스트 제공 |
| `mcp__hf__hub_repo_search` | MCP 호출 | `hf` CLI 또는 WebFetch HF API |
| `mcp__claude_ai_Google_Calendar__list_events` | MCP 호출 | 사용자에게 확인 요청 |
| GitHub MCP tools | MCP 호출 | `gh` CLI (거의 100% 동등) |

## 금지 사항

- MCP 실패 시 "MCP 서버가 없어서 할 수 없습니다" 응답 금지
- Path B 없이 MCP-only 스킬 작성 금지 (hard dependency면 setup 안내 필수)
- 동일 MCP 호출 3회 이상 재시도 금지 (2회 실패 후 Path B 전환)
