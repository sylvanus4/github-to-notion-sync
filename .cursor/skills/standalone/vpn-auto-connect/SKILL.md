---
name: vpn-auto-connect
description: >-
  FortiClient VPN 자동 접속 — 앱 실행, .env 비밀번호 입력, Gmail 2FA 인증 코드 자동 추출 및
  입력까지 원클릭 수행. macOS 전용 (AppleScript GUI 자동화 + gws CLI Gmail 연동).
  Use when the user asks to "connect VPN", "VPN 접속", "VPN 켜줘", "포티클라이언트 접속",
  "vpn-auto-connect", "VPN 자동 접속", "FortiClient 연결", "VPN 연결해줘", "회사 VPN",
  or any request to automate FortiClient VPN connection with 2FA.
  Do NOT use for non-FortiClient VPN clients (OpenVPN, WireGuard 등).
  Do NOT use for VPN disconnection (FortiClient UI에서 수동 해제).
  Do NOT use for VPN 설정 변경 (vpn.plist 직접 편집).
  Do NOT use for Linux/Windows VPN 자동화.
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "standalone"
  platform: "macOS"
---

# VPN Auto-Connect

FortiClient VPN 자동 접속 스킬.

## Prerequisites

1. **macOS 접근성 권한**: System Settings > Privacy & Security > Accessibility →
   Terminal.app (또는 Cursor/VS Code) 추가
2. **FortiClient**: `/Applications/FortiClient.app` 설치됨
3. **`.env`**: 프로젝트 루트에 `VPN_PASSWORD=<비밀번호>` 설정
4. **`gws` CLI**: Gmail 읽기 권한(`gmail.readonly`) 포함 인증 완료

## VPN Profile

| 항목 | 값 |
|------|-----|
| Profile | `tkvpn` |
| Server | `211.239.114.100:10443` |
| User | `hyojung.han` |
| Mode | SSL-VPN |

## Workflow

```bash
# 접속
scripts/vpn/vpn-connect.sh

# 상태 확인만
scripts/vpn/vpn-connect.sh --check
```

파이프라인:

```
.env → VPN_PASSWORD 로드
  → FortiClient.app 실행/활성화
  → AppleScript: 패스워드 입력 + Connect 클릭
  → 2FA 창 감지 대기 (최대 60초)
  → gws: Gmail에서 인증 코드 검색 (3회 재시도)
  → AppleScript: 인증 코드 입력 + Enter
  → 접속 확인 (최대 30초)
```

## Examples

### 이미 접속된 상태

```
$ scripts/vpn/vpn-connect.sh
[09:31:15] === FortiClient VPN 자동 접속 시작 ===
[09:31:15] 프로필: tkvpn | 서버: 211.239.114.100:10443 | 사용자: hyojung.han
[09:31:16] 이미 VPN에 접속되어 있습니다.
```

### 정상 접속 플로우

```
$ scripts/vpn/vpn-connect.sh
[09:31:15] === FortiClient VPN 자동 접속 시작 ===
[09:31:15] FortiClient 실행 중...
[09:31:20] FortiClient 프로세스 확인됨
[09:31:23] VPN 접속 시도 (GUI 자동화)...
[09:31:26] VPN 접속 버튼 클릭 완료. 2FA 대기 중...
[09:31:28] 2FA 입력 필드 감지됨: extra-fields
[09:31:35] Gmail에서 인증 코드 검색 중...
[09:31:37] 인증 코드 발견: 482916
[09:31:38] 2FA 코드 입력 중: 482916
[09:31:39] 2FA 코드 입력 완료
[09:31:45] VPN 접속 성공!
[09:31:45] === VPN 접속 완료 ===
```

## Troubleshooting

### 접근성 권한 오류 (-25211)

```
System Events에 오류 발생: osascript에 보조 접근이 허용되지 않습니다.
```

System Settings > Privacy & Security > Accessibility에서 터미널 앱을 추가하세요.
변경 후 터미널을 재시작해야 합니다.

### Gmail 권한 부족

```
Request had insufficient authentication scopes.
```

```bash
gws auth logout
gws auth login  # gmail.readonly scope 포함 선택
```

### 인증 코드를 찾을 수 없음

이메일 도착까지 5~10초 소요될 수 있습니다. 스크립트가 최대 3회 (5초 간격) 재시도합니다.
계속 실패하면 Gmail에서 수동으로 코드를 확인하세요.

## Files

| 파일 | 용도 |
|------|------|
| `scripts/vpn/vpn-connect.sh` | 메인 자동화 스크립트 |
| `.env` | `VPN_PASSWORD` 저장 (git-ignored) |
