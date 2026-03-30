# Service Registry

## Infrastructure (Docker)

| Service | Port | Health Check |
|---------|------|-------------|
| PostgreSQL | 5433 | `lsof -ti :5433` or `docker compose ps postgres` |
| PgBouncer | 5434 | `lsof -ti :5434` |
| Redis | 6379 | `lsof -ti :6379` or `redis-cli -p 6379 ping` |
| Qdrant | 6333 | `curl -sf http://localhost:6333/healthz` |
| MinIO | 9000 | `curl -sf http://localhost:9000/minio/health/live` |

## Application Services (HTTP /health)

| Service | Port | Tier |
|---------|------|------|
| call-manager | 8010 | Gateway |
| stt-pipeline | 8011 | AI/ML |
| nlp-state | 8012 | AI/ML |
| rag-engine | 8013 | AI/ML |
| llm-inference | 8014 | AI/ML |
| knowledge-manager | 8015 | Data |
| summary-crm | 8016 | Data |
| feedback | 8017 | Stateless |
| admin | 8018 | Core |
| memory-service | 8019 | Data |
| orchestration | 8020 | Core |
| pii-redaction | 8031 | Stateless |
| analytics | 8022 | Data |
| ingress-telephony | 8023 | Telephony |
| vad-diarization | 8024 | AI/ML |
| chat-channel | 8025 | Channel |
| email-channel | 8026 | Channel |
| sms-channel | 8027 | Channel |
| routing-engine | 8028 | Core |
| recording-service | 8029 | Data |
| tts-service | 8030 | AI/ML |
| metering-service | 8032 | Data |
| esl-bridge | 9100 | Telephony |
| frontend | 5173 | UI |
