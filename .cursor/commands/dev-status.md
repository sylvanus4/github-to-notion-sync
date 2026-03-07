---
description: 로컬 개발 환경 전체 서비스 상태 확인
---

모든 서비스의 상태를 확인합니다.

## 실행 명령

```bash
bash scripts/dev-status.sh
```

## 확인 항목

- **인프라**: PostgreSQL(5433), PgBouncer(5434), Redis(6379), Qdrant(6333), MinIO(9000)
- **백엔드**: 20개 마이크로서비스 (8010-8028)
- **프론트엔드**: Vite dev server (5173)

## 상태 표시

- **HEALTHY**: `/health` 엔드포인트 정상 응답
- **STARTING**: 포트 사용 중이지만 아직 헬스체크 미응답
- **DOWN**: 실행되지 않음
