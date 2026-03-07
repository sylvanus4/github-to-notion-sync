# Service Inventory

| Service | Port | Purpose |
|---------|------|---------|
| call-manager (Go) | 8010 | Call lifecycle, WebSocket, events |
| stt-pipeline | 8011 | Audio-to-text, PII masking |
| nlp-state | 8012 | Intent detection, slot extraction |
| rag-engine | 8013 | Embedding, vector search |
| llm-inference | 8014 | LLM recommendations/summaries |
| knowledge-manager | 8015 | Document CRUD, approval |
| summary-crm | 8016 | Post-call summary, CRM |
| feedback | 8017 | Feedback collection |
| admin | 8018 | User mgmt, config, audit |
| memory-service | 8019 | Rolling summary, fact store |
| orchestration | 8020 | Event routing |
| pii-redaction | 8021 | PII redaction |
| analytics | 8022 | KPI calculation |
| ingress-telephony | 8023 | Telephony ingress |
| vad-diarization | 8024 | VAD, diarization |
| chat-channel | 8025 | Web chat, WebSocket, Redis pub/sub |
| email-channel | 8026 | Inbound/outbound email (webhook) |
| sms-channel | 8027 | SMS via Twilio |
| routing-engine | 8028 | Omnichannel routing, skills-based |
| tts-service | 8030 | Text-to-speech synthesis |
