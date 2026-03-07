---
description: 로컬 개발 환경 전체 스택 시작 (인프라 + 백엔드 + 프론트엔드)
---

로컬 개발 환경을 시작합니다.

## 실행 순서

1. **사전 확인**: 필수 도구(Docker, Node, Python, Go), `.env` 파일 확인
2. **프로세스 정리**: 포트 충돌 확인 → 기존 스테일 프로세스 종료 (이미 정상 실행 중인 서비스는 유지)
3. **인프라 시작**: `docker compose up -d postgres pgbouncer redis qdrant minio`
4. **DB 마이그레이션**: `make db-migrate` (필요 시)
5. **Python 의존성**: `pip install -e shared/python` 및 각 서비스 설치
6. **백엔드 서비스**: 각 Python 서비스를 uvicorn으로 백그라운드 시작
7. **Call Manager**: Go 서비스 시작 (포트 8010)
8. **Frontend**: `npm run dev` (포트 5173)
9. **헬스체크**: 모든 서비스 `/health` 엔드포인트 확인

## 실행 명령

```bash
bash scripts/dev-start.sh
```

## 옵션

- `--infra-only`: Docker 인프라만 시작
- `--skip-infra`: 인프라는 건너뛰고 서비스만 시작
- `--services "admin frontend call-manager"`: 특정 서비스만 시작

## 참고 사항

- **OTEL**: 로컬 개발 환경에는 OTEL 컬렉터가 포함되지 않습니다. 스크립트가 자동으로 `OTEL_EXPORTER_OTLP_ENDPOINT`를 해제하므로 로그의 trace export 에러는 무시해도 됩니다.
- **Python 버전**: macOS에서는 Python 3.13+ 권장. Python 3.12는 RAG 엔진 시작 시 abseil mutex deadlock 이슈가 있습니다.
- **INTERNAL_API_KEY**: 챗봇/RAG 기능에 필수. `.env`에 설정되어야 합니다.

## 관련 명령

- 중지: `bash scripts/dev-stop.sh`
- 상태: `bash scripts/dev-status.sh`
- 인프라만 중지: `bash scripts/dev-stop.sh --keep-infra`
