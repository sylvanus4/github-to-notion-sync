---
description: 로컬 개발 환경 전체 스택 중지
---

로컬 개발 환경을 중지합니다.

## 실행 명령

```bash
bash scripts/dev-stop.sh
```

## 옵션

- `--keep-infra`: Docker 인프라(PostgreSQL, Redis 등)는 유지하고 서비스만 중지

## 동작

1. PID 파일을 사용해 서비스 프로세스 종료
2. 서비스 포트(8010-8028, 5173)에 남아있는 프로세스 정리
3. Docker 인프라 중지 (`--keep-infra`가 아닌 경우)
