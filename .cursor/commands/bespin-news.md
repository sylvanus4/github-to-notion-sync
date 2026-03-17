## Bespin News Digest

최신 Bespin Global 뉴스클리핑 이메일을 가져와 각 기사에 대해 전체 연구 파이프라인을
적용합니다. Jina Reader 콘텐츠 추출 → 웹 검색 → AI GPU Cloud 분류 → #press에
3-message Slack 쓰레드 게시 → DOCX 생성 → Google Drive 업로드 → #효정-할일 요약 게시.

### Usage

```
/bespin-news
```

### Execution

Read and follow the `bespin-news-digest` skill:
`.cursor/skills/bespin-news-digest/SKILL.md`

### What this does

1. **Gmail Fetch**: `bespin_news@bespinglobal.com`의 최신 뉴스레터 이메일 조회
2. **HTML Parse**: 이메일에서 모든 기사 URL과 제목 추출 (탐색/풋터 링크 제외)
3. **Per-Article Pipeline** (기사별 순차 처리):
   - Jina Reader(`r.jina.ai`)로 본문 전문 추출
   - WebSearch 2-3회 — 배경, 트렌드, AI/클라우드 영향 조사
   - AI GPU Cloud 관련 여부 분류 (5가지 기준)
   - `#press` 채널에 3-message Slack 쓰레드 게시
   - 기사 간 12초 대기 (Slack rate limit 준수)
4. **DOCX 생성**: 전체 기사 + 조사 결과 + 인사이트 포함 상세 문서
5. **Drive 업로드**: `Google Daily - YYYY-MM-DD` 폴더에 DOCX 저장
6. **요약 게시**: `#효정-할일`에 처리 결과와 Drive 링크 게시

### Quality Standard

각 기사 쓰레드는 반드시:
- 기사 출처 및 날짜 포함
- 본문 전문 추출 기반 상세 요약 (최소 4문장)
- WebSearch 결과 2건 이상 (구체적 수치/사실 포함)
- 참고 링크 2건 이상
- Message 3: 주제별 맞춤 인사이트 (AI GPU Cloud 또는 토픽별)

### Slack Channels

| Channel | Purpose |
|---------|---------|
| `#press` | 기사별 3-message 쓰레드 |
| `#효정-할일` | 최종 요약 (건수 + 테마 + Drive 링크) |
